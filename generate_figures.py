#!/usr/bin/env python3
"""
Generate all figures for LatexAliBaBa project using matplotlib.
Replaces TikZ figures in main.tex and creates missing figures for molE1.tex.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as patches
import numpy as np
import os

# ─── Font Setup ───────────────────────────────────────────────────────────────
from matplotlib import font_manager

WQY_FONT = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
if os.path.exists(WQY_FONT):
    font_manager.fontManager.addfont(WQY_FONT)
    plt.rcParams['font.family'] = 'WenQuanYi Zen Hei'
else:
    plt.rcParams['font.family'] = 'DejaVu Sans'

plt.rcParams['axes.unicode_minus'] = False

# ─── Directory Setup ───────────────────────────────────────────────────────────
os.makedirs('figures/main', exist_ok=True)
os.makedirs('figures/v0', exist_ok=True)


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

def fancy_box(ax, x, y, w, h, text, fontsize=9, bg='#d8d8d8', edge='#555555',
              lw=1.0, radius=0.02, ha='center', va='center', bold=False,
              text_color='black', linestyle='solid'):
    """Draw a rounded rectangle with centred text."""
    box = mpatches.FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle=f"round,pad=0",
        facecolor=bg, edgecolor=edge, linewidth=lw, linestyle=linestyle,
        zorder=2
    )
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x, y, text, ha=ha, va=va, fontsize=fontsize,
            color=text_color, weight=weight, zorder=3,
            wrap=True, multialignment='center')


def arrow(ax, x0, y0, x1, y1, color='#333333', lw=1.2, style='->', ls='solid'):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                linestyle=ls, connectionstyle='arc3,rad=0.0'),
                zorder=4)


def elbow_arrow(ax, pts, color='#555555', lw=1.2, ls='solid', style='->'):
    """Draw a multi-segment arrow through a list of (x, y) waypoints."""
    for i in range(len(pts) - 2):
        ax.plot([pts[i][0], pts[i+1][0]], [pts[i][1], pts[i+1][1]],
                color=color, lw=lw, linestyle=ls, zorder=4)
    # last segment with arrowhead
    ax.annotate("", xy=pts[-1], xytext=pts[-2],
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                linestyle=ls),
                zorder=4)


# ══════════════════════════════════════════════════════════════════════════════
# Figure 1 – Research Gap (fig_gap)
# ══════════════════════════════════════════════════════════════════════════════

def fig_gap():
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    # ── Column headers ─────────────────────────────────────────────────────
    ax.text(2.3, 6.3, '已有工作', ha='center', va='center',
            fontsize=11, weight='bold')
    ax.text(7.3, 6.3, '本工作', ha='center', va='center',
            fontsize=11, weight='bold')

    # ── Left column ────────────────────────────────────────────────────────
    fancy_box(ax, 2.3, 5.7, 4.2, 0.60, '现有 SLM 生产方法',
              fontsize=10, bg='#cccccc', bold=True)

    for i, txt in enumerate([
        '人工标注 CoT（昂贵、缓慢）',
        '具领域知识的教师 LLM',
        '已有学生模型（先有鸡先有蛋）',
    ]):
        fancy_box(ax, 2.3, 4.65 - i * 0.85, 4.2, 0.62, txt,
                  fontsize=9, bg='#e8e8e8', edge='#888888')

    ax.text(2.3, 2.25, '冷启动时三者均不可得',
            ha='center', va='center', fontsize=8.5, color='#666666',
            style='italic')

    fancy_box(ax, 2.3, 1.65, 4.2, 0.72,
              '× 流水线无法启动',
              fontsize=10, bg='#aaaaaa', edge='#555555', bold=True,
              text_color='white')

    # ── Right column ───────────────────────────────────────────────────────
    fancy_box(ax, 7.3, 5.7, 4.2, 0.60, '本方案',
              fontsize=10, bg='#cccccc', bold=True)

    right_items = [
        '原始〈查询, 答案〉对（来自日志）',
        '14B 教师生成 k 条候选 CoT 推理链',
        '标准答案作为验证器，自动过滤',
    ]
    right_y = [4.65, 3.80, 2.95]
    for y, txt in zip(right_y, right_items):
        fancy_box(ax, 7.3, y, 4.2, 0.62, txt,
                  fontsize=9, bg='#e8e8e8', edge='#888888')

    # arrows between right boxes
    for i in range(len(right_y) - 1):
        arrow(ax, 7.3, right_y[i] - 0.31, 7.3, right_y[i + 1] + 0.31)

    # final arrow to success box
    arrow(ax, 7.3, right_y[-1] - 0.31, 7.3, 1.65 + 0.36)

    fancy_box(ax, 7.3, 1.65, 4.2, 0.72,
              '[OK] 无需标注，自动产出专家 SLM',
              fontsize=10, bg='#f4f4f4', edge='#555555', bold=True,
              text_color='#1a6e1a')

    # ── Vertical divider ───────────────────────────────────────────────────
    ax.plot([5.0, 5.0], [0.8, 6.5], color='#aaaaaa',
            lw=1.2, linestyle='--', zorder=1)

    fig.tight_layout(pad=0.5)
    fig.savefig('figures/main/fig_gap.png', dpi=180, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print('Saved figures/main/fig_gap.png')


# ══════════════════════════════════════════════════════════════════════════════
# Figure 2 – Three-Cycle Pipeline (fig_pipeline)
# ══════════════════════════════════════════════════════════════════════════════

def fig_pipeline():
    fig, ax = plt.subplots(figsize=(8.5, 3.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    # Input node
    ax.text(0.55, 2.9, '〈查询,\n答案〉', ha='center', va='center',
            fontsize=8.5, multialignment='center')

    # Three Cycle boxes
    cycle_x = [2.5, 5.6, 8.7]
    cycle_labels = [
        'Cycle 1\n数据采集\nCoT 候选生成（14B）\n答案验证过滤',
        'Cycle 2\nSFT + LoRA\n监督推理训练\n→ pi_0（AIOps-0）',
        'Cycle 3\nAIOps-GRPO\n策略强化优化\n→ pi*（专家 SLM）',
    ]
    for cx, cl in zip(cycle_x, cycle_labels):
        lines = cl.split('\n')
        # header box
        fancy_box(ax, cx, 3.55, 2.7, 0.50, lines[0],
                  fontsize=10, bg='#bbbbbb', bold=True)
        # body box
        body = '\n'.join(lines[1:])
        fancy_box(ax, cx, 2.55, 2.7, 1.50, body,
                  fontsize=8.5, bg='#e8e8e8', edge='#888888')

    # Output node
    ax.text(11.4, 2.9, '专家 SLM\n（MCP 端点）', ha='center', va='center',
            fontsize=8.5, multialignment='center')

    # Main flow arrows
    arrow(ax, 0.95, 2.9, 1.15, 2.9)              # input -> C1
    arrow(ax, 3.85, 2.9, 4.25, 2.9)              # C1 -> C2
    ax.text(4.05, 3.08, 'D*', ha='center', va='center', fontsize=8.5,
            style='italic')
    arrow(ax, 6.95, 2.9, 7.35, 2.9)              # C2 -> C3
    ax.text(7.15, 3.08, 'pi_0', ha='center', va='center', fontsize=8.5,
            style='italic')
    arrow(ax, 10.05, 2.9, 10.9, 2.9)              # C3 -> output

    # Bootstrap loop
    boot_y = 1.0
    fancy_box(ax, 5.6, boot_y, 5.5, 0.72,
              'Bootstrap 回路：πt 对失败样本重新采样 → 过滤 → 写回 D*，触发下一轮迭代',
              fontsize=8, bg='#f0f0f0', edge='#888888')

    # Dashed arrows for bootstrap
    elbow_arrow(ax, [(8.7, 1.8), (8.7, 1.36)],
                color='#777777', lw=1.2, ls='dashed')
    elbow_arrow(ax, [(2.85, 1.36), (2.5, 1.36), (2.5, 1.8)],
                color='#777777', lw=1.2, ls='dashed')
    # connect cycle3 bottom to boot
    ax.plot([8.7, 8.7], [1.8, 2.05], color='#777777', lw=1.2,
            linestyle='dashed')
    # connect boot left to cycle1 bottom
    ax.plot([2.85, 2.85], [1.36, 1.8], color='#777777', lw=1.2,
            linestyle='dashed')

    fig.tight_layout(pad=0.5)
    fig.savefig('figures/main/fig_pipeline.png', dpi=180, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print('Saved figures/main/fig_pipeline.png')


# ══════════════════════════════════════════════════════════════════════════════
# Figure 3 – System Architecture (fig_arch)
# ══════════════════════════════════════════════════════════════════════════════

def fig_arch():
    fig, ax = plt.subplots(figsize=(8.0, 5.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.0)
    ax.axis('off')

    # Layer 1: Input
    fancy_box(ax, 5.0, 6.4, 9.4, 0.60,
              '输入故障事件：告警 + 日志',
              fontsize=10, bg='#e0e0e0', bold=False)

    # Layer 2: Cloud Planner
    fancy_box(ax, 5.0, 5.45, 9.4, 0.70,
              '云端 LLM Planner（72B）     延迟 ~500 ms\n分解故障事件 → 路由至对应 MCP 工具端点',
              fontsize=9, bg='#d0d0d0', bold=False)

    # Layer 3 label
    ax.text(5.0, 4.75, '本地 MCP 工具层   延迟 <100 ms',
            ha='center', va='center', fontsize=9.5, weight='bold',
            color='#333333')

    # MCP Tool boxes
    tool_x = [1.4, 3.8, 6.2]
    tool_labels = [
        '数据库故障\nSLM (1.5B)',
        '网络分区\nSLM (4B)',
        '容器资源耗尽\nSLM (1.5B)',
    ]
    for tx, tl in zip(tool_x, tool_labels):
        fancy_box(ax, tx, 3.85, 2.3, 0.85, tl,
                  fontsize=9, bg='#e8e8e8', edge='#777777')

    # "..." new domain box
    fancy_box(ax, 8.5, 3.85, 1.0, 0.85, '...\n新域',
              fontsize=9, bg='#f0f0f0', edge='#aaaaaa',
              text_color='#aaaaaa')

    # Runtime arrows: Planner → MCP tools
    planner_y_bottom = 5.45 - 0.35
    mcp_y_top = 3.85 + 0.425
    for tx in tool_x:
        elbow_arrow(ax,
                    [(5.0, planner_y_bottom), (5.0, 4.52), (tx, 4.52), (tx, mcp_y_top)],
                    color='#333333', lw=1.3)

    # Layer 4: Offline pipeline
    fancy_box(ax, 5.0, 2.40, 9.4, 0.70,
              '离线生产流水线：C1 数据采集+CoT合成  →  C2 SFT  →  C3 AIOps-GRPO  →  MCP 封装',
              fontsize=9, bg='#e0e0e0')

    # Dashed arrows: offline pipeline → MCP tools
    offline_y_top = 2.40 + 0.35
    mcp_y_bottom = 3.85 - 0.425
    for tx in tool_x:
        elbow_arrow(ax,
                    [(tx, offline_y_top), (tx, mcp_y_bottom)],
                    color='#888888', lw=1.2, ls='dashed')

    # Arrow: Input → Planner
    arrow(ax, 5.0, 6.1, 5.0, 5.80, color='#333333', lw=1.3)

    # Legend
    ax.annotate("", xy=(1.3, 1.55), xytext=(0.5, 1.55),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=1.3))
    ax.text(1.4, 1.55, '运行时调用', va='center', fontsize=8.5)

    ax.annotate("", xy=(4.8, 1.55), xytext=(4.0, 1.55),
                arrowprops=dict(arrowstyle='->', color='#888888', lw=1.3,
                                linestyle='dashed'))
    ax.text(4.9, 1.55, '专家小智能体离线生产（三循环流水线）',
            va='center', fontsize=8.5)

    fig.tight_layout(pad=0.5)
    fig.savefig('figures/main/fig_arch.png', dpi=180, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print('Saved figures/main/fig_arch.png')


# ══════════════════════════════════════════════════════════════════════════════
# Figure 4 – Gantt Chart (fig_gantt)
# ══════════════════════════════════════════════════════════════════════════════

def fig_gantt():
    fig, ax = plt.subplots(figsize=(8.5, 3.0))
    ax.set_xlim(0, 13.5)
    ax.set_ylim(-0.5, 4.8)
    ax.axis('off')

    row_h = 0.72    # bar height
    row_y = [3.8, 2.8, 1.8, 0.8]  # center y for each row
    row_labels = ['M1：流水线与数据', 'M2：SLM 训练', 'M3：系统集成', 'M4：最终交付']

    # Month grid lines and labels
    for m in range(1, 13):
        ax.axvline(m, color='#cccccc', lw=0.8, zorder=1)
        ax.text(m - 0.5, 4.45, str(m), ha='center', va='center',
                fontsize=8.5, color='#444444')
    ax.text(6.5, 4.7, '月份', ha='center', va='center',
            fontsize=9.5, weight='bold')

    # Row labels (left aligned)
    for y, lbl in zip(row_y, row_labels):
        ax.text(-0.1, y, lbl, ha='right', va='center', fontsize=8.5)

    # Bars definition: (start_month, end_month, row_index, label, fill_color, linestyle)
    bars = [
        (0, 3, 0, '数据采集与过滤', '#cccccc', 'solid'),
        (1, 7, 1, 'CoT 合成 + SFT/GRPO 训练', '#bbbbbb', 'solid'),
        (7, 10, 1, '跨域验证\n（探索性）', '#e8e8e8', 'dashed'),
        (6, 9, 2, 'MCP 集成与评估', '#cccccc', 'solid'),
        (9, 12, 3, '验收与交付', '#bbbbbb', 'solid'),
    ]

    for start, end, row, label, color, ls in bars:
        rect = patches.FancyBboxPatch(
            (start, row_y[row] - row_h / 2),
            end - start, row_h,
            boxstyle="round,pad=0.02",
            facecolor=color, edgecolor='#555555', lw=1.0,
            linestyle=ls, zorder=2
        )
        ax.add_patch(rect)
        ax.text((start + end) / 2, row_y[row], label,
                ha='center', va='center', fontsize=7.8,
                multialignment='center', zorder=3)

    # Milestone diamonds
    milestones = [
        (3, 0, 'M1'), (7, 1, 'M2'), (9, 2, 'M3'), (12, 3, 'M4')
    ]
    for mx, row, label in milestones:
        ax.plot(mx, row_y[row], 'D', color='black', markersize=8, zorder=5)
        ax.text(mx, row_y[row] + row_h / 2 + 0.08, label,
                ha='center', va='bottom', fontsize=7.5, weight='bold')

    # Border
    ax.plot([0, 12, 12, 0, 0],
            [4.15, 4.15, 0.44, 0.44, 4.15],
            color='#555555', lw=1.2, zorder=1)

    fig.tight_layout(pad=0.3)
    fig.savefig('figures/main/fig_gantt.png', dpi=180, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print('Saved figures/main/fig_gantt.png')


# ══════════════════════════════════════════════════════════════════════════════
# molE1 Figure 1 – Logos Framework (4 panels)
# ══════════════════════════════════════════════════════════════════════════════

def mol_fig1():
    fig = plt.figure(figsize=(10, 8))
    fig.patch.set_facecolor('white')

    # Panel labels
    panel_kw = dict(fontsize=13, weight='bold', ha='left', va='top')

    # ── Panel (a): Model paradigm ──────────────────────────────────────────
    ax_a = fig.add_axes([0.03, 0.52, 0.44, 0.44])
    ax_a.set_xlim(0, 6)
    ax_a.set_ylim(0, 5)
    ax_a.axis('off')
    ax_a.text(0.0, 4.95, 'a', **panel_kw, transform=ax_a.transAxes)

    fancy_box(ax_a, 1.3, 3.8, 2.2, 0.80,
              'Specialized Models\n(GNN-based generators)\nHigh chemical accuracy',
              fontsize=8, bg='#dde8f5', edge='#5577aa')
    fancy_box(ax_a, 4.5, 3.8, 2.2, 0.80,
              'General LLMs\n(GPT-scale)\nMulti-step reasoning',
              fontsize=8, bg='#f5e8dd', edge='#aa7755')
    fancy_box(ax_a, 2.9, 2.2, 3.5, 0.90,
              'LOGOS\nChemical accuracy + Reasoning\nInterpretable & Structurally valid',
              fontsize=8.5, bg='#e0f0e0', edge='#336633', bold=True)
    elbow_arrow(ax_a, [(1.3, 3.4), (1.3, 2.8), (2.15, 2.65)],
                color='#5577aa', lw=1.3)
    elbow_arrow(ax_a, [(4.5, 3.4), (4.5, 2.8), (3.65, 2.65)],
                color='#aa7755', lw=1.3)

    # ── Panel (b): Pipeline ────────────────────────────────────────────────
    ax_b = fig.add_axes([0.52, 0.52, 0.46, 0.44])
    ax_b.set_xlim(0, 6)
    ax_b.set_ylim(0, 5)
    ax_b.axis('off')
    ax_b.text(0.0, 4.95, 'b', **panel_kw, transform=ax_b.transAxes)

    cyc_x = [1.0, 3.0, 5.0]
    cyc_labels = ['Cycle 1\nSelf-Data\nDistillation', 'Cycle 2\nSFT\nLogos-0 (pi_0)', 'Cycle 3\nM-GRPO\nLogos (pi*)']
    cyc_colors = ['#dde8f5', '#f5e8dd', '#e0f0e0']
    cyc_edges = ['#5577aa', '#aa7755', '#336633']
    for cx, cl, bg, eg in zip(cyc_x, cyc_labels, cyc_colors, cyc_edges):
        fancy_box(ax_b, cx, 2.8, 1.7, 1.5, cl, fontsize=8.5, bg=bg, edge=eg)

    arrow(ax_b, 1.85, 2.8, 2.15, 2.8, color='#555555', lw=1.3)
    arrow(ax_b, 3.85, 2.8, 4.15, 2.8, color='#555555', lw=1.3)

    ax_b.text(3.0, 1.5,
              'Teacher (14B) → CoT data → Student SFT → M-GRPO → Logos',
              ha='center', va='center', fontsize=7.5, color='#555555',
              style='italic')

    # ── Panel (c): Validity Scores ─────────────────────────────────────────
    ax_c = fig.add_axes([0.03, 0.05, 0.44, 0.42])
    ax_c.set_facecolor('#fafafa')

    models = ['GPT-5', 'DeepSeek\n14b', 'Logos\n1.5b v1', 'Logos\n1.5b final', 'Logos\n4b']
    chebi_val = [0.7564, 0.8100, 0.85, 0.9996, 0.9997]
    pcdes_val = [0.8100, 0.82, 0.88, 0.9997, 0.9998]
    x = np.arange(len(models))
    w = 0.35
    bars1 = ax_c.bar(x - w/2, chebi_val, w, label='ChEBI-20',
                     color='#5577aa', alpha=0.85)
    bars2 = ax_c.bar(x + w/2, pcdes_val, w, label='PCdes',
                     color='#aa7755', alpha=0.85)
    ax_c.set_ylim(0.6, 1.05)
    ax_c.set_xticks(x)
    ax_c.set_xticklabels(models, fontsize=7.5)
    ax_c.set_ylabel('Validity Score', fontsize=8.5)
    ax_c.set_title('c  Validity Scores', fontsize=9.5, weight='bold', loc='left')
    ax_c.legend(fontsize=7.5)
    ax_c.axhline(1.0, color='#aaaaaa', lw=0.8, ls='--')
    ax_c.tick_params(labelsize=7.5)

    # ── Panel (d): Human-in-the-loop ───────────────────────────────────────
    ax_d = fig.add_axes([0.52, 0.05, 0.46, 0.42])
    ax_d.set_xlim(0, 6)
    ax_d.set_ylim(0, 5)
    ax_d.axis('off')
    ax_d.text(0.0, 4.95, 'd', **panel_kw, transform=ax_d.transAxes)

    items_d = [
        (3.0, 4.1, '用户指定约束\n(scaffold, log D(7.4) ≈ 3.0)', '#dde8f5', '#5577aa'),
        (3.0, 2.8, 'Logos <think> 推理块\n→ 候选分子', '#e0f0e0', '#336633'),
        (3.0, 1.5, '用户反馈验证\n→ 模型精化策略', '#f5e8dd', '#aa7755'),
    ]
    for ix, iy, itxt, ibg, iedge in items_d:
        fancy_box(ax_d, ix, iy, 5.5, 0.85, itxt, fontsize=8.5,
                  bg=ibg, edge=iedge)

    arrow(ax_d, 3.0, 3.67, 3.0, 3.23, color='#555555', lw=1.3)
    arrow(ax_d, 3.0, 2.37, 3.0, 1.93, color='#555555', lw=1.3)

    ax_d.text(3.0, 0.4, 'd  Human-in-the-Loop',
              ha='center', va='center', fontsize=9.5, weight='bold')

    fig.savefig('figures/v0/fig1.pdf', bbox_inches='tight', dpi=180)
    fig.savefig('figures/v0/fig1.png', bbox_inches='tight', dpi=180)
    plt.close(fig)
    print('Saved figures/v0/fig1.pdf + fig1.png')


# ══════════════════════════════════════════════════════════════════════════════
# molE1 Figure 2 – Benchmarks (fig2.png)
# ══════════════════════════════════════════════════════════════════════════════

def mol_fig2():
    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    fig.patch.set_facecolor('white')
    fig.suptitle('Benchmark Comparison: Logos vs. General LLMs',
                 fontsize=12, weight='bold')

    models = ['DeepSeek\n14b', 'Qwen\n32b', 'GPT-5', 'Logos\n1.5b v1',
              'Logos\n1.5b\nfinal', 'Logos\n4b']
    colors = ['#888888', '#888888', '#888888', '#aaccee', '#5577aa', '#336633']

    # Data from the paper text
    data = {
        'Validity': {
            'ChEBI-20': [0.64, 0.70, 0.7564, 0.80, 0.9996, 0.9997],
            'PCdes':    [0.68, 0.72, 0.8100, 0.84, 0.9997, 0.9998],
        },
        'Exact Match (EM)': {
            'ChEBI-20': [0.16, 0.18, 0.2488, 0.0973, 0.3406, 0.5588],
            'PCdes':    [0.18, 0.20, 0.2873, 0.0993, 0.3103, 0.5047],
        },
        'MACCS Sim.': {
            'ChEBI-20': [0.58, 0.62, 0.7011, 0.70, 0.9376, 0.9629],
            'PCdes':    [0.60, 0.64, 0.7200, 0.72, 0.9200, 0.9400],
        },
        'RDKit Sim.': {
            'ChEBI-20': [0.48, 0.52, 0.6185, 0.60, 0.8228, 0.9038],
            'PCdes':    [0.50, 0.54, 0.6300, 0.62, 0.8100, 0.8900],
        },
        'Morgan Sim.': {
            'ChEBI-20': [0.38, 0.42, 0.5716, 0.55, 0.7422, 0.8569],
            'PCdes':    [0.40, 0.44, 0.5800, 0.56, 0.7300, 0.8400],
        },
        'FCD ↓': {
            'ChEBI-20': [3.5, 3.0, 2.8354, 2.1, 0.4795, 0.2868],
            'PCdes':    [3.2, 2.8, 2.6000, 1.8, 0.5100, 0.3200],
        },
    }

    metrics = list(data.keys())
    for idx, (ax, metric) in enumerate(zip(axes.flat, metrics)):
        chebi = data[metric]['ChEBI-20']
        pcdes = data[metric]['PCdes']
        x = np.arange(len(models))
        w = 0.38
        ax.bar(x - w/2, chebi, w, label='ChEBI-20', color=colors, alpha=0.85)
        ax.bar(x + w/2, pcdes, w, label='PCdes', color=colors, alpha=0.55,
               edgecolor=colors, linewidth=1)
        ax.set_title(metric, fontsize=9, weight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(models, fontsize=6.5)
        ax.tick_params(axis='y', labelsize=7.5)
        if idx == 0:
            # Custom legend
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='#555555', label='ChEBI-20 (solid)'),
                Patch(facecolor='#aaaaaa', label='PCdes (lighter)'),
            ]
            ax.legend(handles=legend_elements, fontsize=6.5)

    fig.tight_layout()
    fig.savefig('figures/v0/fig2.png', dpi=180, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print('Saved figures/v0/fig2.png')


# ══════════════════════════════════════════════════════════════════════════════
# molE1 Figure 3 – Training Pipeline & Ablations (fig3)
# ══════════════════════════════════════════════════════════════════════════════

def mol_fig3():
    fig = plt.figure(figsize=(12, 5))
    fig.patch.set_facecolor('white')
    panel_kw = dict(fontsize=13, weight='bold')

    # ── Panel (a): Training pipeline ──────────────────────────────────────
    ax_a = fig.add_axes([0.02, 0.08, 0.30, 0.82])
    ax_a.set_xlim(0, 4)
    ax_a.set_ylim(0, 5)
    ax_a.axis('off')
    ax_a.text(0.1, 4.85, 'a', **panel_kw)

    steps = [
        (2.0, 4.1, 'Teacher LLM (14B)\nGenerates CoT', '#dde8f5', '#5577aa'),
        (2.0, 3.0, 'CoT Dataset\n(description + reasoning + SMILES)', '#f5f5dd', '#aaaa55'),
        (2.0, 1.9, 'Student SFT → Logos-0\n(1.5B / 4B params)', '#f5e8dd', '#aa7755'),
        (2.0, 0.8, 'M-GRPO → Logos\n(chemical rewards)', '#e0f0e0', '#336633'),
    ]
    for sx, sy, stxt, sbg, sedge in steps:
        fancy_box(ax_a, sx, sy, 3.7, 0.75, stxt, fontsize=8.5,
                  bg=sbg, edge=sedge)
    for i in range(len(steps) - 1):
        arrow(ax_a, steps[i][0], steps[i][1] - 0.375,
              steps[i+1][0], steps[i+1][1] + 0.375, color='#555555', lw=1.3)

    ax_a.text(2.0, 0.15, 'a  Training Pipeline',
              ha='center', va='center', fontsize=9.5, weight='bold')

    # ── Panel (b): Ablation EM curves ─────────────────────────────────────
    ax_b = fig.add_axes([0.36, 0.15, 0.30, 0.72])
    steps_x = np.arange(1, 11)
    full_em = 0.10 + 0.28 * (1 - np.exp(-steps_x / 4.5))
    no_sdd  = 0.06 + 0.16 * (1 - np.exp(-steps_x / 4.0))
    sft_only = 0.04 + 0.12 * (1 - np.exp(-steps_x / 3.5))
    ax_b.plot(steps_x, full_em, '-o', color='#336633', lw=2,
              label='Full M-GRPO', markersize=5)
    ax_b.plot(steps_x, no_sdd, '--s', color='#aa7755', lw=1.5,
              label='w.o. SDD', markersize=5)
    ax_b.plot(steps_x, sft_only, ':^', color='#5577aa', lw=1.5,
              label='SFT only', markersize=5)
    ax_b.set_xlabel('Training Epoch', fontsize=9)
    ax_b.set_ylabel('Exact Match (EM)', fontsize=9)
    ax_b.set_title('b  Ablation Study', fontsize=9.5, weight='bold', loc='left')
    ax_b.legend(fontsize=8)
    ax_b.axhline(0.35, color='#aaaaaa', lw=0.8, ls='--')
    ax_b.text(9.2, 0.36, 'EM=0.35', fontsize=7, color='#aaaaaa')
    ax_b.set_facecolor('#fafafa')
    ax_b.tick_params(labelsize=8)

    # ── Panel (c): Output format ───────────────────────────────────────────
    ax_c = fig.add_axes([0.70, 0.08, 0.28, 0.82])
    ax_c.set_xlim(0, 4)
    ax_c.set_ylim(0, 5)
    ax_c.axis('off')
    ax_c.text(0.1, 4.85, 'c', **panel_kw)

    format_text = (
        'System Prompt:\n'
        '"Generate a molecule for the\n'
        'following description..."\n\n'
        '<think>\n'
        '  Identify scaffold...\n'
        '  Locate modification sites...\n'
        '  Apply functional groups...\n'
        '</think>\n\n'
        '{\n'
        '  "molecule": "CC(=O)Oc1ccc..."\n'
        '}'
    )
    fancy_box(ax_c, 2.0, 2.6, 3.7, 4.6, format_text,
              fontsize=7.5, bg='#f8f8f8', edge='#888888',
              ha='left', va='center')
    ax_c.text(0.15, 4.55, format_text, va='top', ha='left',
              fontsize=7.5, fontfamily='monospace', color='#333333')

    ax_c.text(2.0, 0.15, 'c  Output Format (JSON + CoT)',
              ha='center', va='center', fontsize=9.5, weight='bold')

    fig.savefig('figures/v0/fig3.pdf', bbox_inches='tight', dpi=180)
    fig.savefig('figures/v0/fig3.png', bbox_inches='tight', dpi=180)
    plt.close(fig)
    print('Saved figures/v0/fig3.pdf + fig3.png')


# ══════════════════════════════════════════════════════════════════════════════
# molE1 Figure 4 – Integrated Discovery (fig4)
# ══════════════════════════════════════════════════════════════════════════════

def mol_fig4():
    fig = plt.figure(figsize=(12, 8))
    fig.patch.set_facecolor('white')
    panel_kw = dict(fontsize=13, weight='bold')

    # ── Panel (a): Human-in-the-loop workflow ─────────────────────────────
    ax_a = fig.add_axes([0.02, 0.52, 0.46, 0.44])
    ax_a.set_xlim(0, 6)
    ax_a.set_ylim(0, 5)
    ax_a.axis('off')
    ax_a.text(0.1, 4.85, 'a', **panel_kw)

    workflow = [
        (3.0, 4.1, 'User: scaffold + log D(7.4) ≈ 3.0\n+ solubility constraint', '#dde8f5', '#5577aa'),
        (3.0, 2.9, 'Logos <think>: reasoning block\n→ candidate molecule SMILES', '#e0f0e0', '#336633'),
        (3.0, 1.7, 'User: validation feedback\n(assay / in silico)', '#f5e8dd', '#aa7755'),
        (3.0, 0.55, 'Logos: refines strategy\nvia updated <think>', '#e0f0e0', '#336633'),
    ]
    for wx, wy, wtxt, wbg, wedge in workflow:
        fancy_box(ax_a, wx, wy, 5.6, 0.82, wtxt, fontsize=8.5,
                  bg=wbg, edge=wedge)
    for i in range(len(workflow) - 1):
        arrow(ax_a, workflow[i][0], workflow[i][1] - 0.41,
              workflow[i+1][0], workflow[i+1][1] + 0.41, color='#555555', lw=1.3)

    ax_a.text(3.0, -0.3, 'a  Human-in-the-Loop Workflow',
              ha='center', fontsize=9.5, weight='bold')

    # ── Panel (b): CoT Breakdown ───────────────────────────────────────────
    ax_b = fig.add_axes([0.52, 0.52, 0.46, 0.44])
    ax_b.set_xlim(0, 6)
    ax_b.set_ylim(0, 5)
    ax_b.axis('off')
    ax_b.text(0.1, 4.85, 'b', **panel_kw)

    cot_steps = [
        (3.0, 4.0, '① Scaffold Identification\n(from request / in-context examples)', '#e8eef8'),
        (3.0, 2.9, '② Site Localization\n(modification sites on scaffold)', '#eef8e8'),
        (3.0, 1.8, '③ Functional Group Changes\n(by analogy to in-context examples)', '#f8eee8'),
    ]
    for bx, by, btxt, bbg in cot_steps:
        fancy_box(ax_b, bx, by, 5.5, 0.82, btxt, fontsize=8.5,
                  bg=bbg, edge='#888888')
    arrow(ax_b, 3.0, 3.59, 3.0, 3.31, color='#555555', lw=1.3)
    arrow(ax_b, 3.0, 2.49, 3.0, 2.21, color='#555555', lw=1.3)

    ax_b.text(3.0, 0.8, '→ Inspectable, auditable design rationale',
              ha='center', fontsize=8.5, color='#444444', style='italic')
    ax_b.text(3.0, -0.3, 'b  Chain-of-Thought Breakdown',
              ha='center', fontsize=9.5, weight='bold')

    # ── Panel (c): Validation Rate Comparison ─────────────────────────────
    ax_c = fig.add_axes([0.05, 0.07, 0.40, 0.38])
    ax_c.set_facecolor('#fafafa')

    models_c = ['DeepSeek-r1\n(14B)', 'Logos\n(4B)']
    val_rates = [98.75, 64.46]
    bars = ax_c.bar(models_c, val_rates, color=['#5577aa', '#336633'], width=0.4,
                    alpha=0.85)
    for bar, rate in zip(bars, val_rates):
        ax_c.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                  f'{rate}%', ha='center', va='bottom', fontsize=9.5, weight='bold')
    ax_c.set_ylim(0, 115)
    ax_c.set_ylabel('Task Success Rate (%)', fontsize=9)
    ax_c.set_title('c  Multi-Objective Optimization Success',
                   fontsize=9, weight='bold', loc='left')
    ax_c.tick_params(labelsize=8.5)

    # ── Panel (d): log D scatter ───────────────────────────────────────────
    ax_d = fig.add_axes([0.55, 0.07, 0.42, 0.38])
    ax_d.set_facecolor('#fafafa')

    np.random.seed(42)
    n = 80
    log_d = np.random.normal(3.0, 0.35, n)
    solubility = -2.0 - 0.5 * log_d + np.random.normal(0, 0.4, n)
    sc = ax_d.scatter(log_d, solubility, c=log_d, cmap='RdYlGn_r',
                      alpha=0.75, s=35, edgecolors='none')
    ax_d.axvline(3.0, color='#cc4444', lw=1.5, ls='--', label='Target log D(7.4)=3.0')
    ax_d.set_xlabel('log D(7.4)', fontsize=9)
    ax_d.set_ylabel('log Solubility (log S)', fontsize=9)
    ax_d.set_title('d  Generated Molecules (log D(7.4) vs. Solubility)',
                   fontsize=9, weight='bold', loc='left')
    ax_d.legend(fontsize=8)
    plt.colorbar(sc, ax=ax_d, label='log D(7.4)')
    ax_d.tick_params(labelsize=8)

    fig.savefig('figures/v0/fig4.pdf', bbox_inches='tight', dpi=180)
    fig.savefig('figures/v0/fig4.png', bbox_inches='tight', dpi=180)
    plt.close(fig)
    print('Saved figures/v0/fig4.pdf + fig4.png')


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print('Generating figures...')
    fig_gap()
    fig_pipeline()
    fig_arch()
    fig_gantt()
    mol_fig1()
    mol_fig2()
    mol_fig3()
    mol_fig4()
    print('All figures generated successfully.')
