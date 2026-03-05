#!/usr/bin/env python3
"""
直接从 LaTeX 导出 Word 文档（替代 make_docx.py 的手写方式）

流程：
  1. 将每个 .tikz 图用 standalone + xelatex 编译为 PDF，再转为 PNG
  2. 创建临时 tex，将 \input{fig_*.tikz} 替换为 \includegraphics{...}
  3. 调用 pandoc 生成 .docx

依赖（一次性安装）：
  apt-get install -y pandoc texlive-xetex texlive-lang-chinese poppler-utils
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent
OUTPUT = BASE / "申请书_阿里巴巴AI研究资助计划2026.docx"
REFERENCE_DOCX = BASE / "2026 Alibaba-Proposal Template.docx"
TEMP_DIR = BASE / "_pandoc_tmp"

TIKZ_FILES = ["fig_gap", "fig_pipeline", "fig_arch", "fig_gantt"]

# tikzset 定义从 main.tex 中提取，standalone wrapper 需要复制相同的样式
STANDALONE_TEMPLATE = r"""\documentclass[tikz,border=6pt]{standalone}
\usepackage[UTF8]{ctex}
\usepackage{tikz}
\usepackage{amssymb}
\usepackage{amsmath}
\usetikzlibrary{shapes.geometric, arrows.meta, positioning, calc, fit, backgrounds}
\tikzset{
  box/.style={rectangle, draw=black, thick, rounded corners=3pt,
              text width=#1, align=center, minimum height=0.8cm, fill=white},
  box/.default=3cm,
  arrow/.style={-Stealth, thick},
  dasharrow/.style={-Stealth, thick, dashed},
  label/.style={font=\small},
  greybox/.style={box=#1, fill=gray!12},
  greybox/.default=3cm,
}
\begin{document}
\input{__TIKZ_FILE__}
\end{document}
"""


def run(cmd: list, cwd: Path = None):
    print(f"  $ {' '.join(str(c) for c in cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout[-2000:] if result.stdout else "")
        print(result.stderr[-2000:] if result.stderr else "")
        raise RuntimeError(f"Failed: {' '.join(str(c) for c in cmd)}")
    return result


def check_deps():
    missing = []
    for tool in ("pandoc", "xelatex", "pdftoppm"):
        if not shutil.which(tool):
            missing.append(tool)
    if missing:
        print(f"[ERROR] 缺少工具: {', '.join(missing)}")
        print("请运行: apt-get install -y pandoc texlive-xetex texlive-lang-chinese poppler-utils")
        sys.exit(1)


def compile_tikz_to_png(name: str) -> Path:
    """用 standalone + xelatex 将 .tikz 编译为 PNG，返回 PNG 路径。"""
    work = TEMP_DIR / name
    work.mkdir(parents=True, exist_ok=True)

    # 复制 tikz 源文件到临时目录
    shutil.copy(BASE / f"{name}.tikz", work / f"{name}.tikz")

    # 写 standalone 包装 tex
    tex = STANDALONE_TEMPLATE.replace("__TIKZ_FILE__", f"{name}.tikz")
    (work / f"{name}.tex").write_text(tex, encoding="utf-8")

    # xelatex 编译（两次确保布局稳定）
    for _ in range(2):
        run(["xelatex", "-interaction=nonstopmode", f"{name}.tex"], cwd=work)

    # PDF → PNG（200 dpi，单页）
    pdf = work / f"{name}.pdf"
    png_prefix = TEMP_DIR / name            # pdftoppm 输出: <prefix>-1.png
    run(["pdftoppm", "-r", "200", "-png", str(pdf), str(png_prefix)])

    png = TEMP_DIR / f"{name}-1.png"
    if not png.exists():
        raise FileNotFoundError(f"PNG 未生成: {png}")
    return png


def patch_main_tex(fig_pngs: dict) -> Path:
    """将 main.tex 中的 \\input{fig_*.tikz} 替换为 \\includegraphics，返回临时 tex 路径。"""
    src = (BASE / "main.tex").read_text(encoding="utf-8")

    for name, png in fig_pngs.items():
        src = re.sub(
            rf"\\input\{{{re.escape(name)}\.tikz\}}",
            rf"\\includegraphics[width=\\textwidth]{{{png.as_posix()}}}",
            src,
        )

    patched = TEMP_DIR / "main_pandoc.tex"
    patched.write_text(src, encoding="utf-8")
    return patched


def build_docx():
    check_deps()
    TEMP_DIR.mkdir(exist_ok=True)

    # ── 1. 编译 TikZ 图 ───────────────────────────────────────────────────────
    print("=== Step 1: 编译 TikZ 图 ===")
    fig_pngs = {}
    for name in TIKZ_FILES:
        print(f"  {name}.tikz ...")
        fig_pngs[name] = compile_tikz_to_png(name)
        print(f"  -> {fig_pngs[name]}")

    # ── 2. 修补 main.tex ──────────────────────────────────────────────────────
    print("\n=== Step 2: 修补 main.tex ===")
    patched_tex = patch_main_tex(fig_pngs)
    print(f"  -> {patched_tex}")

    # ── 3. Pandoc 生成 DOCX ───────────────────────────────────────────────────
    print("\n=== Step 3: Pandoc → DOCX ===")
    cmd = [
        "pandoc",
        str(patched_tex),
        "--from=latex",
        "--to=docx",
        f"--output={OUTPUT}",
        "--dpi=200",
        f"--resource-path={BASE}:{TEMP_DIR}",
    ]
    if REFERENCE_DOCX.exists():
        cmd += [f"--reference-doc={REFERENCE_DOCX}"]
        print(f"  使用参考样式: {REFERENCE_DOCX.name}")

    run(cmd)
    print(f"\n完成！输出: {OUTPUT}")


if __name__ == "__main__":
    build_docx()
