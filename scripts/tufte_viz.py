#!/usr/bin/env python3
"""Generate Edward Tufte-style SVG charts from Data-Pro-Skill outputs.

Implements high data-ink ratio vector graphics (zero chartjunk, direct labels,
confidence interval whiskers, and subtle reference lines):
  - sparkline(): Inline word-sized trend / distribution graphic
  - dot_plot(): Cleveland dot plot with 95% CI (±MoE) whiskers & mean reference line
  - diverging_bar(): Diverging stacked bar for NPS / Likert sentiment
  - residual_heatmap_svg(): Chi-square standardized residuals (z_ij) matrix
  - priority_matrix_svg(): 4-quadrant Derived Importance x Performance scatter
  - small_multiples(): Multi-panel comparative grid from real segment/crosstab data
  - mermaid_to_svg(): Compiler converting Mermaid xychart-beta & pie blocks into Tufte SVGs

Output: .dps/outputs/export/charts/*.svg
"""

import argparse
import csv
import html
import json
import math
import re
from pathlib import Path


def _esc(text):
    """HTML-escape text for safe SVG embedding."""
    return html.escape(str(text or ""))


def sparkline(values, width=120, height=24, stroke="#111111", stroke_width=1.2, show_endpoints=True):
    """Generate an inline SVG sparkline with min/max endpoint dots."""
    clean = [float(v) for v in values if v is not None and not math.isnan(float(v))]
    if len(clean) < 2:
        return ""
    mn, mx = min(clean), max(clean)
    rng = (mx - mn) if mx != mn else 1.0
    pts = len(clean)
    pad_x = 6
    pad_y = 4
    x_step = (width - 2 * pad_x) / (pts - 1) if pts > 1 else (width - 2 * pad_x)

    coords = []
    for i, v in enumerate(clean):
        x = pad_x + i * x_step
        y = height - pad_y - ((v - mn) / rng * (height - 2 * pad_y))
        coords.append((x, y, v))

    polyline = " ".join(f"{x:.1f},{y:.1f}" for x, y, _ in coords)
    dots = ""
    if show_endpoints:
        fx, fy, _ = coords[0]
        lx, ly, _ = coords[-1]
        min_pt = min(coords, key=lambda c: c[2])
        max_pt = max(coords, key=lambda c: c[2])
        dots = (
            f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="1.8" fill="#555555"/>'
            f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="2.0" fill="#111111"/>'
            f'<circle cx="{min_pt[0]:.1f}" cy="{min_pt[1]:.1f}" r="1.8" fill="#a61c1c"/>'
            f'<circle cx="{max_pt[0]:.1f}" cy="{max_pt[1]:.1f}" r="1.8" fill="#1b4f72"/>'
        )
    return (
        f'<svg class="sparkline" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
        f'<polyline fill="none" stroke="{stroke}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round" points="{polyline}"/>'
        f'{dots}</svg>'
    )


def dot_plot(labels, values, errors=None, title="", subtitle="", unit="", width=580, height=None):
    """Generate a Tufte Cleveland dot plot with optional 95% CI whiskers and mean reference line."""
    if not labels or not values:
        return ""
    n = len(labels)
    row_h = 26
    top_pad = 48 if subtitle else 34
    bottom_pad = 24
    if height is None:
        height = max(110, top_pad + n * row_h + bottom_pad)

    clean_vals = [float(v) for v in values]
    clean_errs = [float(e) if (errors and i < len(errors) and errors[i] is not None) else 0.0 for i, e in enumerate(errors or [0.0] * n)]

    lows = [v - e for v, e in zip(clean_vals, clean_errs)]
    highs = [v + e for v, e in zip(clean_vals, clean_errs)]
    mn = min(lows)
    mx = max(highs)
    if mn > 0 and mn / (mx if mx else 1) < 0.35:
        mn = 0.0
    pad_range = (mx - mn) * 0.12 if mx != mn else 1.0
    axis_min = mn - (0 if mn == 0 else pad_range * 0.5)
    axis_max = mx + pad_range
    rng = axis_max - axis_min if axis_max != axis_min else 1.0

    pad_left = min(210, max(130, max(len(str(l)) for l in labels) * 6 + 18))
    pad_right = 78
    plot_w = max(160, width - pad_left - pad_right)

    def x_pos(val):
        return pad_left + ((val - axis_min) / rng) * plot_w

    mean_val = sum(clean_vals) / len(clean_vals)
    mean_x = x_pos(mean_val)

    elements = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{_esc(title)}">'
    ]

    if title:
        elements.append(
            f'<text x="0" y="18" font-family="Georgia, Palatino, serif" font-size="13.5" '
            f'font-weight="bold" fill="#111111">{_esc(title)}</text>'
        )
    if subtitle:
        elements.append(
            f'<text x="0" y="34" font-family="Georgia, Palatino, serif" font-size="10.5" '
            f'font-style="italic" fill="#555555">{_esc(subtitle)}</text>'
        )

    # Subtle mean reference line
    y_start = top_pad - 6
    y_end = top_pad + (n - 1) * row_h + 8
    elements.append(
        f'<line x1="{mean_x:.1f}" y1="{y_start}" x2="{mean_x:.1f}" y2="{y_end}" '
        f'stroke="#888888" stroke-width="0.9" stroke-dasharray="3,3"/>'
        f'<text x="{mean_x:.1f}" y="{y_end + 14}" text-anchor="middle" '
        f'font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9" '
        f'fill="#666666">Mean: {mean_val:.1f}{_esc(unit)}</text>'
    )

    # Zero line if applicable
    if axis_min < 0 < axis_max:
        zx = x_pos(0)
        elements.append(
            f'<line x1="{zx:.1f}" y1="{y_start}" x2="{zx:.1f}" y2="{y_end}" '
            f'stroke="#a61c1c" stroke-width="0.8" stroke-opacity="0.5"/>'
        )

    for i, (label, val, err) in enumerate(zip(labels, clean_vals, clean_errs)):
        y = top_pad + i * row_h
        cx = x_pos(val)
        trunc_label = str(label) if len(str(label)) <= 30 else str(label)[:28] + "…"
        # Subtle dotted guide from label to dot (classic Cleveland dot plot)
        elements.append(
            f'<line x1="{pad_left}" y1="{y}" x2="{pad_left + plot_w}" y2="{y}" '
            f'stroke="#e6e6de" stroke-width="0.7" stroke-dasharray="1,3"/>'
        )
        elements.append(
            f'<text x="{pad_left - 8}" y="{y + 4}" text-anchor="end" '
            f'font-family="Georgia, Palatino, serif" font-size="11" fill="#222222">'
            f'{_esc(trunc_label)}</text>'
        )
        # 95% CI whisker if error > 0
        if err > 0:
            x1 = max(pad_left, x_pos(val - err))
            x2 = min(pad_left + plot_w, x_pos(val + err))
            elements.append(
                f'<line x1="{x1:.1f}" y1="{y}" x2="{x2:.1f}" y2="{y}" '
                f'stroke="#555555" stroke-width="1.4"/>'
                f'<line x1="{x1:.1f}" y1="{y - 3}" x2="{x1:.1f}" y2="{y + 3}" '
                f'stroke="#555555" stroke-width="1.1"/>'
                f'<line x1="{x2:.1f}" y1="{y - 3}" x2="{x2:.1f}" y2="{y + 3}" '
                f'stroke="#555555" stroke-width="1.1"/>'
            )
        # Dot & direct data label
        dot_color = "#1b4f72" if val >= mean_val else "#a61c1c"
        val_str = f"{val:.1f}{unit}" if abs(val - round(val)) > 0.01 else f"{int(round(val))}{unit}"
        if err > 0:
            val_str += f" (±{err:.1f})"
        elements.append(
            f'<circle cx="{cx:.1f}" cy="{y}" r="3.6" fill="{dot_color}"/>'
            f'<text x="{pad_left + plot_w + 8}" y="{y + 4}" '
            f'font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="10" '
            f'fill="#333333">{_esc(val_str)}</text>'
        )

    elements.append("</svg>")
    return "\n".join(elements)


def diverging_bar(labels, detractors, passives, promoters, title="", subtitle="", width=580):
    """Generate a Tufte diverging horizontal bar chart for NPS / Likert distributions."""
    if not labels:
        return ""
    n = len(labels)
    row_h = 26
    top_pad = 48 if subtitle else 34
    height = top_pad + n * row_h + 26
    pad_left = min(190, max(120, max(len(str(l)) for l in labels) * 6 + 14))
    pad_right = 70
    plot_w = width - pad_left - pad_right
    mid_x = pad_left + plot_w * 0.45

    elements = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{_esc(title)}">'
    ]
    if title:
        elements.append(
            f'<text x="0" y="18" font-family="Georgia, Palatino, serif" font-size="13.5" '
            f'font-weight="bold" fill="#111111">{_esc(title)}</text>'
        )
    if subtitle:
        elements.append(
            f'<text x="0" y="34" font-family="Georgia, Palatino, serif" font-size="10.5" '
            f'font-style="italic" fill="#555555">{_esc(subtitle)}</text>'
        )

    elements.append(
        f'<line x1="{mid_x:.1f}" y1="{top_pad - 8}" x2="{mid_x:.1f}" y2="{height - 18}" '
        f'stroke="#666666" stroke-width="0.9"/>'
    )

    scale = (plot_w * 0.5) / 100.0
    for i, (lbl, det, pas, pro) in enumerate(zip(labels, detractors, passives, promoters)):
        y = top_pad + i * row_h
        det_w = max(0.0, float(det)) * scale
        pas_w = max(0.0, float(pas)) * scale
        pro_w = max(0.0, float(pro)) * scale
        nps = float(pro) - float(det)

        elements.append(
            f'<text x="{pad_left - 8}" y="{y + 4}" text-anchor="end" '
            f'font-family="Georgia, Palatino, serif" font-size="11" fill="#222222">'
            f'{_esc(str(lbl)[:28])}</text>'
        )
        # Left of center: Detractors + half of Passives
        x_det = mid_x - (pas_w / 2.0) - det_w
        x_pas = mid_x - (pas_w / 2.0)
        x_pro = mid_x + (pas_w / 2.0)

        if det_w > 0:
            elements.append(
                f'<rect x="{x_det:.1f}" y="{y - 6}" width="{det_w:.1f}" height="12" fill="#a61c1c" opacity="0.82"/>'
            )
        if pas_w > 0:
            elements.append(
                f'<rect x="{x_pas:.1f}" y="{y - 6}" width="{pas_w:.1f}" height="12" fill="#c8c8be"/>'
            )
        if pro_w > 0:
            elements.append(
                f'<rect x="{x_pro:.1f}" y="{y - 6}" width="{pro_w:.1f}" height="12" fill="#1b4f72" opacity="0.85"/>'
            )
        elements.append(
            f'<text x="{pad_left + plot_w + 6}" y="{y + 4}" '
            f'font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="10" '
            f'font-weight="600" fill="#222222">NPS {nps:+.0f}</text>'
        )

    elements.append("</svg>")
    return "\n".join(elements)


def residual_heatmap_svg(row_labels, col_labels, z_matrix, title="", subtitle="", width=580):
    """Generate a Tufte SVG matrix of Chi-Square Standardized Residuals (z_ij)."""
    if not row_labels or not col_labels or not z_matrix:
        return ""
    n_rows = len(row_labels)
    n_cols = len(col_labels)
    top_pad = 68 if subtitle else 54
    row_h = 26
    pad_left = min(180, max(110, max(len(str(r)) for r in row_labels) * 6 + 14))
    cell_w = max(52, min(95, (width - pad_left - 20) / max(1, n_cols)))
    actual_w = int(pad_left + n_cols * cell_w + 20)
    height = top_pad + n_rows * row_h + 28

    elements = [
        f'<svg viewBox="0 0 {actual_w} {height}" width="100%" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{_esc(title)}">'
    ]
    if title:
        elements.append(
            f'<text x="0" y="18" font-family="Georgia, Palatino, serif" font-size="13.5" '
            f'font-weight="bold" fill="#111111">{_esc(title)}</text>'
        )
    if subtitle:
        elements.append(
            f'<text x="0" y="34" font-family="Georgia, Palatino, serif" font-size="10.5" '
            f'font-style="italic" fill="#555555">{_esc(subtitle)}</text>'
        )

    # Column headers
    for j, c_lbl in enumerate(col_labels):
        cx = pad_left + j * cell_w + cell_w / 2
        elements.append(
            f'<text x="{cx:.1f}" y="{top_pad - 10}" text-anchor="middle" '
            f'font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9.5" '
            f'font-weight="600" fill="#333333">{_esc(str(c_lbl)[:14])}</text>'
        )

    for i, r_lbl in enumerate(row_labels):
        y = top_pad + i * row_h
        elements.append(
            f'<text x="{pad_left - 8}" y="{y + 16}" text-anchor="end" '
            f'font-family="Georgia, Palatino, serif" font-size="10.5" fill="#222222">'
            f'{_esc(str(r_lbl)[:26])}</text>'
        )
        for j in range(n_cols):
            z = float(z_matrix[i][j]) if j < len(z_matrix[i]) else 0.0
            x = pad_left + j * cell_w
            # Highlight cells exceeding |z| >= 1.96 (p < 0.05)
            if z >= 1.96:
                bg = "#d4e6f1" if z < 2.58 else "#a9cce3"
                fg = "#1b4f72"
                fw = "bold"
            elif z <= -1.96:
                bg = "#f5d7d7" if z > -2.58 else "#ebb7b7"
                fg = "#781e1e"
                fw = "bold"
            else:
                bg = "#f9f9f3"
                fg = "#666666"
                fw = "normal"
            elements.append(
                f'<rect x="{x + 1:.1f}" y="{y + 1}" width="{cell_w - 2:.1f}" height="{row_h - 2}" '
                f'fill="{bg}" stroke="#e0e0d8" stroke-width="0.6"/>'
                f'<text x="{x + cell_w / 2:.1f}" y="{y + 16}" text-anchor="middle" '
                f'font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="10" '
                f'font-weight="{fw}" fill="{fg}">{z:+.2f}</text>'
            )

    elements.append(
        f'<text x="{pad_left}" y="{height - 6}" '
        f'font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="8.5" '
        f'fill="#666666">Note: |z| ≥ 1.96 indicates statistically significant cell deviation (p &lt; 0.05).</text>'
        f'</svg>'
    )
    return "\n".join(elements)


def priority_matrix_svg(items, title="Priority Action Matrix (Importance × Performance)", subtitle="", width=580, height=340):
    """Generate a 4-quadrant Derived Importance x Performance scatter plot.

    items: list of dicts with keys {'label', 'importance', 'performance', 'priority_score'}
    """
    if not items:
        return ""
    top_pad = 50 if subtitle else 36
    pad_left = 54
    pad_right = 30
    pad_bottom = 38
    plot_w = width - pad_left - pad_right
    plot_h = height - top_pad - pad_bottom

    imps = [float(it.get("importance", 0)) for it in items]
    perfs = [float(it.get("performance", 0)) for it in items]
    imp_min, imp_max = min(imps), max(imps)
    perf_min, perf_max = min(perfs), max(perfs)

    imp_pad = (imp_max - imp_min) * 0.18 if imp_max != imp_min else 0.2
    perf_pad = (perf_max - perf_min) * 0.18 if perf_max != perf_min else 0.5
    x_min, x_max = perf_min - perf_pad, perf_max + perf_pad
    y_min, y_max = max(0.0, imp_min - imp_pad), imp_max + imp_pad

    mean_perf = sum(perfs) / len(perfs)
    mean_imp = sum(imps) / len(imps)

    def tx(p):
        return pad_left + ((p - x_min) / (x_max - x_min if x_max != x_min else 1)) * plot_w

    def ty(imp):
        return top_pad + plot_h - ((imp - y_min) / (y_max - y_min if y_max != y_min else 1)) * plot_h

    mx_line = tx(mean_perf)
    my_line = ty(mean_imp)

    elements = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{_esc(title)}">'
    ]
    if title:
        elements.append(
            f'<text x="0" y="18" font-family="Georgia, Palatino, serif" font-size="13.5" '
            f'font-weight="bold" fill="#111111">{_esc(title)}</text>'
        )
    if subtitle:
        elements.append(
            f'<text x="0" y="34" font-family="Georgia, Palatino, serif" font-size="10.5" '
            f'font-style="italic" fill="#555555">{_esc(subtitle)}</text>'
        )

    # Frame & Quadrant lines
    elements.append(
        f'<rect x="{pad_left}" y="{top_pad}" width="{plot_w}" height="{plot_h}" '
        f'fill="none" stroke="#999999" stroke-width="0.8"/>'
        f'<line x1="{mx_line:.1f}" y1="{top_pad}" x2="{mx_line:.1f}" y2="{top_pad + plot_h}" '
        f'stroke="#888888" stroke-width="0.9" stroke-dasharray="4,4"/>'
        f'<line x1="{pad_left}" y1="{my_line:.1f}" x2="{pad_left + plot_w}" y2="{my_line:.1f}" '
        f'stroke="#888888" stroke-width="0.9" stroke-dasharray="4,4"/>'
    )

    # Quadrant watermarks
    elements.append(
        f'<text x="{pad_left + 8}" y="{top_pad + 15}" font-family="-apple-system, sans-serif" '
        f'font-size="9" font-weight="bold" fill="#a61c1c">CRITICAL FIX (High Imp / Low Perf)</text>'
        f'<text x="{pad_left + plot_w - 8}" y="{top_pad + 15}" text-anchor="end" '
        f'font-family="-apple-system, sans-serif" font-size="9" font-weight="bold" fill="#1b4f72">'
        f'PROTECT STRENGTH (High Imp / High Perf)</text>'
        f'<text x="{pad_left + 8}" y="{top_pad + plot_h - 8}" font-family="-apple-system, sans-serif" '
        f'font-size="9" fill="#777777">LOW PRIORITY (Low Imp / Low Perf)</text>'
        f'<text x="{pad_left + plot_w - 8}" y="{top_pad + plot_h - 8}" text-anchor="end" '
        f'font-family="-apple-system, sans-serif" font-size="9" fill="#777777">'
        f'MAINTAIN / OVERKILL (Low Imp / High Perf)</text>'
    )

    # Axis labels
    elements.append(
        f'<text x="{pad_left + plot_w / 2:.1f}" y="{height - 8}" text-anchor="middle" '
        f'font-family="Georgia, Palatino, serif" font-size="10.5" fill="#333333">'
        f'Mean Performance Score →</text>'
        f'<text x="14" y="{top_pad + plot_h / 2:.1f}" text-anchor="middle" '
        f'transform="rotate(-90 14 {top_pad + plot_h / 2:.1f})" '
        f'font-family="Georgia, Palatino, serif" font-size="10.5" fill="#333333">'
        f'Derived Importance (|r|) →</text>'
    )

    # Points
    for it in items:
        lbl = str(it.get("label", ""))[:22]
        imp = float(it.get("importance", 0))
        perf = float(it.get("performance", 0))
        px, py = tx(perf), ty(imp)
        is_crit = imp >= mean_imp and perf < mean_perf
        color = "#a61c1c" if is_crit else ("#1b4f72" if imp >= mean_imp else "#555555")
        elements.append(
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.2" fill="{color}"/>'
            f'<text x="{px + 6:.1f}" y="{py + 3:.1f}" '
            f'font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9.5" '
            f'font-weight="{"600" if is_crit else "400"}" fill="#222222">{_esc(lbl)}</text>'
        )

    elements.append("</svg>")
    return "\n".join(elements)


def small_multiples(grid_data, title="", subtitle="", cell_w=140, cell_h=86):
    """Generate small multiples grid from real (label, values) pairs."""
    valid_grid = [(lbl, [float(v) for v in vals if v is not None]) for lbl, vals in grid_data if vals and len(vals) >= 2]
    if not valid_grid:
        return ""
    cols = min(4, len(valid_grid))
    rows = math.ceil(len(valid_grid) / cols)
    total_w = max(420, cols * cell_w)
    top_pad = 44 if subtitle else 28
    total_h = top_pad + rows * cell_h + 12

    cells = []
    for idx, (label, vals) in enumerate(valid_grid):
        col = idx % cols
        row = idx // cols
        cx = col * cell_w
        cy = top_pad + row * cell_h
        sp = sparkline(vals, width=cell_w - 16, height=cell_h - 32)
        mn, mx = min(vals), max(vals)
        cells.append(
            f'<g transform="translate({cx},{cy})">'
            f'<text x="{(cell_w - 16)/2:.1f}" y="12" text-anchor="middle" '
            f'font-family="Georgia, Palatino, serif" font-size="10" font-weight="bold" fill="#222222">'
            f'{_esc(str(label)[:20])}</text>'
            f'<g transform="translate(4, 16)">{sp}</g>'
            f'<text x="{(cell_w - 16)/2:.1f}" y="{cell_h - 4}" text-anchor="middle" '
            f'font-family="-apple-system, sans-serif" font-size="8.5" fill="#666666">'
            f'range: {mn:.1f} – {mx:.1f}</text>'
            f'</g>'
        )

    header = (
        f'<text x="0" y="16" font-family="Georgia, Palatino, serif" font-size="13" '
        f'font-weight="bold" fill="#111111">{_esc(title)}</text>'
    )
    if subtitle:
        header += (
            f'<text x="0" y="31" font-family="Georgia, Palatino, serif" font-size="10" '
            f'font-style="italic" fill="#555555">{_esc(subtitle)}</text>'
        )

    return (
        f'<svg viewBox="0 0 {total_w} {total_h}" width="100%" height="{total_h}" '
        f'xmlns="http://www.w3.org/2000/svg">{header}{"".join(cells)}</svg>'
    )


def mermaid_to_svg(mermaid_code, width=580):
    """Compile Mermaid xychart-beta or pie blocks directly into Tufte inline SVGs."""
    code = mermaid_code.strip()
    title_match = re.search(r'title\s+"([^"]+)"', code)
    title = title_match.group(1) if title_match else ""

    if code.startswith("xychart-beta"):
        x_match = re.search(r'x-axis\s+\[(.*?)\]', code, re.DOTALL)
        bar_match = re.search(r'(?:bar|line)\s+\[(.*?)\]', code, re.DOTALL)
        if x_match and bar_match:
            raw_labels = [x.strip().strip('"').strip("'") for x in x_match.group(1).split(",") if x.strip()]
            raw_vals = []
            for v in bar_match.group(1).split(","):
                v_clean = re.sub(r"[^0-9.\-]", "", v.strip())
                if v_clean:
                    raw_vals.append(float(v_clean))
            if raw_labels and raw_vals and len(raw_labels) == len(raw_vals):
                y_match = re.search(r'y-axis\s+"([^"]+)"', code)
                subtitle = y_match.group(1) if y_match else ""
                unit = "%" if "%" in subtitle else ""
                return dot_plot(raw_labels, raw_vals, title=title, subtitle=subtitle, unit=unit, width=width)

    if code.startswith("pie"):
        pairs = re.findall(r'"([^"]+)"\s*:\s*([0-9.]+)', code)
        if pairs:
            labels = [p[0] for p in pairs]
            vals = [float(p[1]) for p in pairs]
            total = sum(vals) or 1.0
            pcts = [round(v / total * 100, 1) for v in vals]
            return dot_plot(
                labels,
                pcts,
                title=title or "Distribution Breakdown",
                subtitle="Proportion of total (%)",
                unit="%",
                width=width,
            )

    return ""


def generate_charts(input_dir, charts_dir):
    """Scan .dps/outputs (or equivalent directory) and emit real Tufte SVG charts."""
    charts_dir = Path(charts_dir)
    charts_dir.mkdir(parents=True, exist_ok=True)
    input_dir = Path(input_dir)

    charts = []

    # 1. Dot plots from setup_segments.csv (if present)
    seg_candidates = [
        input_dir / "setup" / "setup_segments.csv",
        input_dir / "setup_segments.csv",
    ]
    for seg_file in seg_candidates:
        if seg_file.exists():
            with open(seg_file, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            if rows:
                ignore_cols = {"segment", "variable", "Segment", "Variable", "n", "N", "moe_95", "sd"}
                numeric_cols = [c for c in rows[0].keys() if c not in ignore_cols]
                for col in numeric_cols[:4]:
                    vals = []
                    for r in rows:
                        raw_v = str(r.get(col, "")).strip()
                        try:
                            v_num = float(raw_v)
                            lbl = r.get("segment") or r.get("Segment") or r.get("variable") or "?"
                            moe = float(r["moe_95"]) if r.get("moe_95") else 0.0
                            vals.append((lbl, v_num, moe))
                        except ValueError:
                            continue
                    if len(vals) >= 2:
                        labels = [v[0] for v in vals]
                        values = [v[1] for v in vals]
                        errors = [v[2] for v in vals] if any(v[2] > 0 for v in vals) else None
                        svg = dot_plot(
                            labels,
                            values,
                            errors=errors,
                            title=f"{col.replace('_', ' ').title()} by Segment",
                            subtitle="Cleveland dot plot with 95% confidence intervals & mean reference",
                        )
                        if svg:
                            safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", col)
                            path = charts_dir / f"dotplot_{safe_name}.svg"
                            path.write_text(svg, encoding="utf-8")
                            charts.append(str(path.name))
                            print(f"  ✓ dot plot: {path.name}")
            break

    # 2. Profile numeric metrics dot plot from 00_profile.json
    prof_candidates = [
        input_dir / "setup" / "00_profile.json",
        input_dir / "00_profile.json",
    ]
    for prof_file in prof_candidates:
        if prof_file.exists():
            try:
                profile = json.loads(prof_file.read_text(encoding="utf-8"))
                variables = profile.get("variables", {})
                likert_labels = []
                likert_means = []
                likert_moes = []
                grid_items = []
                for vname, vinfo in variables.items():
                    if isinstance(vinfo, dict) and vinfo.get("mean") is not None:
                        m = float(vinfo["mean"])
                        if 0 <= m <= 10:
                            likert_labels.append(vinfo.get("original_name", vname))
                            likert_means.append(m)
                            likert_moes.append(float(vinfo.get("moe_95", 0.0) or 0.0))
                    # Build real small multiples from value distributions if available
                    dist = vinfo.get("distribution") if isinstance(vinfo, dict) else None
                    if isinstance(dist, dict) and len(dist) >= 3:
                        nums = [float(x) for x in dist.values() if isinstance(x, (int, float))]
                        if len(nums) >= 3:
                            grid_items.append((vinfo.get("original_name", vname), nums))

                if len(likert_labels) >= 2:
                    svg = dot_plot(
                        likert_labels[:12],
                        likert_means[:12],
                        errors=likert_moes[:12],
                        title="Metric Performance Overview (Mean ± 95% CI)",
                        subtitle=f"Total Sample N = {profile.get('sample_size', profile.get('n_rows', '?'))}",
                    )
                    path = charts_dir / "dotplot_profile_means.svg"
                    path.write_text(svg, encoding="utf-8")
                    charts.append(str(path.name))
                    print(f"  ✓ profile dot plot: {path.name}")

                if len(grid_items) >= 2:
                    svg = small_multiples(
                        grid_items[:8],
                        title="Response Distribution Shapes Across Variables",
                        subtitle="Empirical frequency sparklines per variable (min–max scaled)",
                    )
                    if svg:
                        path = charts_dir / "small_multiples_distributions.svg"
                        path.write_text(svg, encoding="utf-8")
                        charts.append(str(path.name))
                        print(f"  ✓ small multiples: {path.name}")
            except Exception as exc:
                print(f"  ⚠ Warning reading {prof_file}: {exc}")
            break

    # 3. Crosstab residual heatmaps from cross/*_stats.json
    cross_dirs = [input_dir / "cross", input_dir]
    for cdir in cross_dirs:
        if cdir.exists():
            for stats_file in sorted(cdir.glob("cross_*_stats.json"))[:4]:
                try:
                    st = json.loads(stats_file.read_text(encoding="utf-8"))
                    res_table = st.get("standardized_residuals")
                    if isinstance(res_table, dict) and res_table.get("rows") and res_table.get("cols"):
                        svg = residual_heatmap_svg(
                            res_table["rows"],
                            res_table["cols"],
                            res_table["z_matrix"],
                            title=f"Standardized Residuals (z_ij): {st.get('index', '')} × {st.get('columns', '')}",
                            subtitle=f"Chi-Square p = {st.get('p_value', 1.0):.4f} · Cramér's V = {st.get('cramers_v', 0.0):.3f}",
                        )
                        if svg:
                            out_name = f"residuals_{stats_file.stem.replace('_stats', '')}.svg"
                            (charts_dir / out_name).write_text(svg, encoding="utf-8")
                            charts.append(out_name)
                            print(f"  ✓ residual heatmap: {out_name}")
                except Exception:
                    continue

    # 4. Priority Matrix SVG from advanced/advanced_metrics.json
    adv_candidates = [
        input_dir / "advanced" / "advanced_metrics.json",
        input_dir / "advanced_metrics.json",
    ]
    for adv_file in adv_candidates:
        if adv_file.exists():
            try:
                adv = json.loads(adv_file.read_text(encoding="utf-8"))
                pmatrix = adv.get("priority_matrix", [])
                if len(pmatrix) >= 2:
                    svg = priority_matrix_svg(
                        pmatrix,
                        title="Priority Action Matrix (Derived Importance × Performance)",
                        subtitle="Priority Score = Importance × (Scale_max − Mean Performance)",
                    )
                    if svg:
                        path = charts_dir / "priority_matrix.svg"
                        path.write_text(svg, encoding="utf-8")
                        charts.append(str(path.name))
                        print(f"  ✓ priority matrix: {path.name}")
            except Exception:
                pass
            break

    if not charts:
        print("  ℹ No standalone chart files emitted (inline SVG compiler remains active)")

    return charts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tufte-style SVG chart generator")
    parser.add_argument("--input", default=".dps/outputs", help="Root outputs directory")
    parser.add_argument("--charts-dir", default=".dps/outputs/export/charts", help="Output SVG directory")
    args = parser.parse_args()
    generate_charts(args.input, args.charts_dir)
