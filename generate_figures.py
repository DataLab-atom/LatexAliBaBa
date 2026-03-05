"""
用 matplotlib 还原 4 张 TikZ 图表，供 Word 文档嵌入
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm
import os

# ── 中文字体 + Unicode 回退 ──────────────────────────────────────────────────
CJK_FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fm.fontManager.addfont(CJK_FONT)
# 优先 CJK，回退 DejaVu Sans（含数学符号和下标）
matplotlib.rcParams['font.family'] = ['Noto Sans CJK JP', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

OUT_DIR = '/home/user/LatexAliBaBa'
DPI = 180


def rbox(ax, x, y, w, h, text, fill='white', edgecolor='black',
         lw=1.2, fontsize=9, bold=False, alpha=1.0, linestyle='-',
         valign='center', halign='center', extra_lines=None):
    """画圆角矩形+文字"""
    box = FancyBboxPatch((x, y), w, h,
                          boxstyle='round,pad=0.02',
                          facecolor=fill, edgecolor=edgecolor,
                          linewidth=lw, linestyle=linestyle,
                          zorder=2, alpha=alpha)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w/2, y + h/2, text,
            ha=halign, va=valign,
            fontsize=fontsize, fontweight=weight,
            wrap=True, zorder=3,
            multialignment='center')


def arrow(ax, x1, y1, x2, y2, label='', lw=1.2, color='black',
          ls='-', fontsize=8):
    """画箭头"""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=lw, linestyle=ls),
                zorder=4)
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.03, label,
                ha='center', va='bottom', fontsize=fontsize)


# ══════════════════════════════════════════════════════════════════════════════
#  图1：fig_gap — 研究空白对比
# ══════════════════════════════════════════════════════════════════════════════
def make_fig_gap():
    fig, ax = plt.subplots(figsize=(7.8, 3.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.axis('off')

    GRAY = '#E0E0E0'
    DARKGRAY = '#BCBCBC'
    W = 4.0
    LX, RX = 0.3, 5.7

    # ── 上方标签 ──────────────────────────────────────────────────────────────
    ax.text(LX + W/2, 4.72, '已有工作', ha='center', va='bottom',
            fontsize=10, fontweight='bold')
    ax.text(RX + W/2, 4.72, '本工作', ha='center', va='bottom',
            fontsize=10, fontweight='bold')

    # ── 竖向分隔线 ────────────────────────────────────────────────────────────
    ax.plot([5.0, 5.0], [0.1, 4.7], color='#AAAAAA', lw=1.2,
            linestyle='--', zorder=1)

    # ── 左列 ──────────────────────────────────────────────────────────────────
    rbox(ax, LX, 4.0, W, 0.55, '现有 SLM 生产方法',
         fill='#DCDCDC', lw=1.4, fontsize=10, bold=True)
    rbox(ax, LX, 3.30, W, 0.55, '人工标注 CoT（昂贵、缓慢）',
         fill=GRAY, fontsize=9)
    rbox(ax, LX, 2.65, W, 0.55, '具领域知识的教师 LLM',
         fill=GRAY, fontsize=9)
    rbox(ax, LX, 2.00, W, 0.55, '已有学生模型（先有鸡先有蛋）',
         fill=GRAY, fontsize=9)
    ax.text(LX + W/2, 1.82, '冷启动时三者均不可得', ha='center',
            va='center', fontsize=8, style='italic', color='#666666')
    rbox(ax, LX, 1.18, W, 0.52, '×  流水线无法启动',
         fill=DARKGRAY, edgecolor='#888888', fontsize=9.5, bold=True)

    # ── 右列 ──────────────────────────────────────────────────────────────────
    rbox(ax, RX, 4.0, W, 0.55, '本方案',
         fill='#DCDCDC', lw=1.4, fontsize=10, bold=True)
    rbox(ax, RX, 3.30, W, 0.55, '原始 ⟨查询, 答案⟩ 对（来自日志）',
         fill=GRAY, fontsize=9)
    rbox(ax, RX, 2.65, W, 0.55, '14B 教师生成 k 条候选 CoT 推理链',
         fill=GRAY, fontsize=9)
    rbox(ax, RX, 2.00, W, 0.55, '标准答案作为验证器，自动过滤',
         fill=GRAY, fontsize=9, bold=False)

    # 右列箭头
    arrow(ax, RX+W/2, 3.30, RX+W/2, 3.22)
    arrow(ax, RX+W/2, 2.65, RX+W/2, 2.57)
    arrow(ax, RX+W/2, 2.00, RX+W/2, 1.75)

    rbox(ax, RX, 1.18, W, 0.52, '✓  无需标注，自动产出专家 SLM',
         fill='#F0F0F0', edgecolor='#888888', fontsize=9.5, bold=True)

    plt.tight_layout(pad=0.3)
    out = os.path.join(OUT_DIR, 'fig_gap.png')
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'Saved {out}')


# ══════════════════════════════════════════════════════════════════════════════
#  图2：fig_pipeline — 三循环迭代流水线
# ══════════════════════════════════════════════════════════════════════════════
def make_fig_pipeline():
    fig, ax = plt.subplots(figsize=(9.5, 3.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(-1.8, 3.0)
    ax.axis('off')

    GRAY = '#E8E8E8'
    BW = 2.5   # box width
    BH = 1.55  # box height
    Y0 = 1.0   # top of cycle boxes

    # ── 输入节点 ──────────────────────────────────────────────────────────────
    ax.text(0.5, Y0 + BH/2, '⟨查询,\n答案⟩', ha='center', va='center',
            fontsize=9)

    # ── 三个 Cycle 方框 ────────────────────────────────────────────────────────
    cx = [1.3, 4.5, 7.7]
    labels = [
        'Cycle 1\n\n数据采集\nCoT 候选生成（14B）\n答案验证过滤',
        'Cycle 2\n\nSFT + LoRA\n监督推理训练\n→ π₀（AIOps-0）',
        'Cycle 3\n\nAIOps-GRPO\n策略强化优化\n→ π*（专家 SLM）',
    ]
    for i, (x, label) in enumerate(zip(cx, labels)):
        rbox(ax, x, Y0, BW, BH, label,
             fill=GRAY, lw=1.2, fontsize=8.2)
        # 第一行加粗（Cycle N）
        lines = label.split('\n')
        # 先画整体框，再在顶部覆盖加粗标题
        ax.text(x + BW/2, Y0 + BH - 0.22, lines[0],
                ha='center', va='top', fontsize=9, fontweight='bold',
                zorder=4)

    # ── 主流向箭头 ────────────────────────────────────────────────────────────
    # 输入 → Cycle1
    arrow(ax, 0.9, Y0 + BH/2, cx[0], Y0 + BH/2)
    # Cycle1 → Cycle2
    arrow(ax, cx[0]+BW, Y0+BH/2, cx[1], Y0+BH/2, label='D*', fontsize=8)
    # Cycle2 → Cycle3
    arrow(ax, cx[1]+BW, Y0+BH/2, cx[2], Y0+BH/2, label='π₀', fontsize=8)
    # Cycle3 → 输出
    arrow(ax, cx[2]+BW, Y0+BH/2, 11.0, Y0+BH/2)

    # ── 输出节点 ──────────────────────────────────────────────────────────────
    ax.text(11.1, Y0 + BH/2, '专家 SLM\n（MCP 端点）',
            ha='left', va='center', fontsize=9)

    # ── Bootstrap 回路 ────────────────────────────────────────────────────────
    boot_y = -0.6
    boot_x = 3.2
    boot_w = 4.6
    rbox(ax, boot_x, boot_y - 0.4, boot_w, 0.7,
         'Bootstrap 回路：πₜ 对失败样本重新采样 →[过滤]→ 写回 D*，触发下一轮迭代',
         fill='#F0F0F0', edgecolor='#999999', lw=1.0, fontsize=7.8)

    # Cycle3下方 → Bootstrap右侧（实线箭头）
    ax.annotate('', xy=(boot_x + boot_w, boot_y - 0.05),
                xytext=(cx[2]+BW/2, Y0),
                arrowprops=dict(arrowstyle='->', color='#777777',
                                lw=1.0, connectionstyle='arc3,rad=-0.3'))
    # Bootstrap左侧 → Cycle1下方（虚线）
    ax.annotate('', xy=(cx[0]+BW/2, Y0),
                xytext=(boot_x, boot_y - 0.05),
                arrowprops=dict(arrowstyle='->', color='#777777',
                                lw=1.0, linestyle='dashed',
                                connectionstyle='arc3,rad=-0.3'))

    plt.tight_layout(pad=0.4)
    out = os.path.join(OUT_DIR, 'fig_pipeline.png')
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'Saved {out}')


# ══════════════════════════════════════════════════════════════════════════════
#  图3：fig_arch — 系统架构
# ══════════════════════════════════════════════════════════════════════════════
def make_fig_arch():
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.set_xlim(0, 10.5)
    ax.set_ylim(-0.8, 5.8)
    ax.axis('off')

    GRAY = '#E8E8E8'
    WIDE = 9.8
    LX = 0.35

    # ── 第1层：输入 ────────────────────────────────────────────────────────────
    rbox(ax, LX, 4.9, WIDE, 0.6, '输入故障事件：告警 + 日志',
         lw=1.3, fontsize=10)

    # ── 箭头 ──────────────────────────────────────────────────────────────────
    arrow(ax, LX+WIDE/2, 4.9, LX+WIDE/2, 4.38)

    # ── 第2层：Planner ─────────────────────────────────────────────────────────
    rbox(ax, LX, 3.55, WIDE, 0.72,
         '云端 LLM Planner（72B）      延迟 ~500ms',
         fill=GRAY, lw=1.3, fontsize=10, bold=True)
    ax.text(LX + WIDE/2, 3.67,
            '分解故障事件  →  路由至对应 MCP 工具端点',
            ha='center', va='top', fontsize=8.5, style='italic', color='#444444',
            zorder=4)
    ax.text(LX + WIDE/2, 3.55+0.72/2 + 0.10,
            '云端 LLM Planner（72B）      ', ha='center', va='center',
            fontsize=10, fontweight='bold', zorder=5)
    ax.text(LX + WIDE/2 + 2.5, 3.55+0.72/2 + 0.10,
            '延迟 ~500ms', ha='center', va='center',
            fontsize=8.5, style='italic', color='#666666', zorder=5)

    # ── 第3层标签 ──────────────────────────────────────────────────────────────
    ax.text(LX + WIDE/2, 3.32,
            '本地 MCP 工具层          延迟 <100ms',
            ha='center', va='center', fontsize=9.5, fontweight='bold')

    # ── 第3层：4个 MCP 工具端点 ────────────────────────────────────────────────
    bw3 = 2.0; bh3 = 0.85; y3 = 2.3
    xs3 = [LX, LX+bw3+0.35, LX+2*(bw3+0.35), LX+3*(bw3+0.35)]
    labels3 = [
        '数据库故障\nSLM（1.5B）',
        '网络分区\nSLM（4B）',
        '容器资源耗尽\nSLM（1.5B）',
        '…\n新域',
    ]
    fills3 = [GRAY, GRAY, GRAY, 'white']
    edges3 = ['black', 'black', 'black', '#AAAAAA']
    for x, lbl, fill, edge in zip(xs3, labels3, fills3, edges3):
        rbox(ax, x, y3, bw3, bh3, lbl,
             fill=fill, edgecolor=edge, fontsize=9,
             bold=(lbl != '…\n新域'))

    # 运行时箭头：Planner → 各端点（直箭头）
    planner_bottom = 3.55
    for x in xs3[:3]:
        ax.annotate('', xy=(x+bw3/2, y3+bh3),
                    xytext=(LX+WIDE/2, planner_bottom),
                    arrowprops=dict(arrowstyle='->', color='black',
                                   lw=1.0, connectionstyle='arc3,rad=0'))

    # ── 第4层：离线生产流水线 ───────────────────────────────────────────────────
    rbox(ax, LX, 1.15, WIDE, 0.75,
         '离线生产流水线：  C1 数据采集+CoT合成  →  C2 SFT  →  C3 AIOps-GRPO  →  MCP 封装',
         lw=1.3, fontsize=9)

    # 虚线箭头：离线流水线 → 各端点（底部）
    for x in xs3[:3]:
        ax.annotate('', xy=(x+bw3/2, y3),
                    xytext=(x+bw3/2, 1.15+0.75),
                    arrowprops=dict(arrowstyle='->', color='#666666',
                                   lw=1.0, linestyle='dashed'))

    # ── 图例 ──────────────────────────────────────────────────────────────────
    ax.annotate('', xy=(1.6, 0.65), xytext=(1.0, 0.65),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
    ax.text(1.7, 0.65, '运行时调用', va='center', fontsize=8.5)
    ax.annotate('', xy=(5.6, 0.65), xytext=(5.0, 0.65),
                arrowprops=dict(arrowstyle='->', color='#666666',
                                lw=1.2, linestyle='dashed'))
    ax.text(5.7, 0.65, '专家小智能体离线生产（三循环流水线）',
            va='center', fontsize=8.5, color='#444444')

    plt.tight_layout(pad=0.4)
    out = os.path.join(OUT_DIR, 'fig_arch.png')
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'Saved {out}')


# ══════════════════════════════════════════════════════════════════════════════
#  图4：fig_gantt — 甘特图
# ══════════════════════════════════════════════════════════════════════════════
def make_fig_gantt():
    fig, ax = plt.subplots(figsize=(9.0, 3.2))
    ax.set_xlim(-3.5, 12.5)
    ax.set_ylim(-4.5, 0.7)
    ax.axis('off')

    LIGHT = '#D8D8D8'
    MID   = '#ABABAB'

    # ── 月份表头 ──────────────────────────────────────────────────────────────
    ax.text(6, 0.45, '月份', ha='center', va='center',
            fontsize=10, fontweight='bold')
    ax.plot([0, 12], [0, 0], 'k-', lw=1.5)
    for m in range(13):
        ax.plot([m, m], [0, -4.2], color='#DDDDDD', lw=0.8, zorder=1)
        if m < 12:
            ax.text(m + 0.5, 0.15, str(m+1), ha='center', va='bottom',
                    fontsize=8.5)

    # ── 行标签 ────────────────────────────────────────────────────────────────
    row_labels = [
        'M1：流水线与数据',
        'M2：SLM 训练',
        'M3：系统集成',
        'M4：最终交付',
    ]
    row_y = [-0.5, -1.5, -2.5, -3.5]
    for lbl, y in zip(row_labels, row_y):
        ax.text(-0.2, y, lbl, ha='right', va='center', fontsize=9,
                fontweight='bold')

    # ── 甘特条 ────────────────────────────────────────────────────────────────
    bars = [
        # (x_start, x_end, row_y, fill, edgecolor, label, ls)
        (0, 3,  -0.5, LIGHT, '#666666', '数据采集与过滤', '-'),
        (1, 7,  -1.5, MID,   '#666666', 'CoT 合成 + SFT/GRPO 训练', '-'),
        (7, 10, -1.5, '#F0F0F0', '#999999', '跨域验证\n（探索性）', '--'),
        (6, 9,  -2.5, LIGHT, '#666666', 'MCP 集成与评估', '-'),
        (9, 12, -3.5, MID,   '#666666', '验收与交付', '-'),
    ]
    bh = 0.7
    for x0, x1, cy, fill, edge, lbl, ls in bars:
        rect = mpatches.FancyBboxPatch(
            (x0, cy - bh/2), x1 - x0, bh,
            boxstyle='square,pad=0',
            facecolor=fill, edgecolor=edge, linewidth=1.2,
            linestyle=ls, zorder=2)
        ax.add_patch(rect)
        mid_x = (x0 + x1) / 2
        ax.text(mid_x, cy, lbl, ha='center', va='center', fontsize=8,
                zorder=3)

    # ── 里程碑菱形 ────────────────────────────────────────────────────────────
    milestones = [(3, -0.5, 'M1'), (7, -1.5, 'M2'),
                  (9, -2.5, 'M3'), (12, -3.5, 'M4')]
    for mx, my, mlbl in milestones:
        ax.plot(mx, my, 'D', color='black', markersize=7, zorder=5)
        ax.text(mx, my + 0.45, mlbl, ha='center', va='bottom',
                fontsize=8.5, fontweight='bold')

    # ── 外框 ──────────────────────────────────────────────────────────────────
    ax.plot([0, 12, 12, 0, 0], [0, 0, -4.2, -4.2, 0], 'k-', lw=1.5)

    plt.tight_layout(pad=0.5)
    out = os.path.join(OUT_DIR, 'fig_gantt.png')
    fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'Saved {out}')


if __name__ == '__main__':
    make_fig_gap()
    make_fig_pipeline()
    make_fig_arch()
    make_fig_gantt()
    print('All figures generated.')
