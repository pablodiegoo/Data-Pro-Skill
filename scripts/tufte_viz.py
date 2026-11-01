#!/usr/bin/env python3
"""Generate Multi-School SVG Data Visualizations from Data-Pro-Skill outputs.

Supports all 5 canonical Data Design Schools selectable during `/dps-setup`:
  1. tufte     — Edward Tufte: Cleveland dot plots with 95% CI whiskers, range-frame axes, supertables & sparklines
  2. few       — Stephen Few: Bullet Graphs with qualitative bands, target crossbars, variance Δ% columns & sparkbars
  3. knaflic   — Cole Knaflic (SWD): Preattentive grey-context + bold focal bars, narrative callouts & highlight tables
  4. swiss     — Swiss Grid / Bertin: Exposed architectural modular grids & Jacques Bertin retinal symbol matrices
  5. editorial — Economist / FT: Newsprint canvas, signature crimson top tag, lollipop range charts & area strips

Output: .dps/outputs/export/charts/*.svg (plus charts/by_school/<school>/*.svg for live multi-school switching)
"""

import argparse
import csv
import html
import json
import math
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

try:
    import design_schools
except ImportError:
    design_schools = None


def _esc(text):
    """HTML-escape text for safe SVG embedding."""
    return html.escape(str(text or ""))


def _norm_school(school="tufte"):
    if design_schools is not None:
        return design_schools.normalize_school(school, default="tufte")
    s = str(school or "tufte").strip().lower()
    return s if s in ("tufte", "few", "knaflic", "swiss", "editorial") else "tufte"


def _school_spec(school="tufte"):
    canon = _norm_school(school)
    if design_schools is not None:
        return design_schools.get_school_spec(canon)
    return {
        "id": canon,
        "short_name": "Edward Tufte",
        "palette": {
            "paper": "#fffff8",
            "ink": "#111111",
            "muted": "#555555",
            "primary": "#1b4f72",
            "secondary": "#555555",
            "accent": "#1c3d5a",
            "alert_neg": "#a61c1c",
            "alert_pos": "#1b4f72",
            "neutral_bar": "#c8c8be",
            "grid_line": "#e6e6de",
        },
        "fonts": {
            "heading": "Georgia, Palatino, serif",
            "body": "Georgia, Palatino, serif",
            "ui": "-apple-system, BlinkMacSystemFont, sans-serif",
            "mono": "Consolas, monospace",
        },
    }


def _clean_label(text, max_len=None):
    """Remove survey instrument boilerplate and normalize mathematical symbols for clean chart typography."""
    s = str(text or "").strip()
    # Remove noisy questionnaire tags like [Espontânea - RU], [Pesquisador - RU], [ESCONDER]
    s = re.sub(r"\[(?i:espont[aâ]nea|pesquisador|estimulada|ru|rm|esconder)[^\]]*\]", "", s)
    s = re.sub(r"\((?i:espont[aâ]nea|pesquisador|estimulada)\s*-\s*(?i:ru|rm)\)", "", s)
    s = re.sub(r"(?i)\bTODAS AS IDADES\b", "(Total)", s)
    # Clean mathematical notation inside SVG text
    s = s.replace("z_ij", "zᵢⱼ").replace("O_ij", "Oᵢⱼ").replace("E_ij", "Eᵢⱼ")
    s = s.replace("Scale_max", "Scaleₘₐₓ").replace("\\times", "×").replace("\\pm", "±")
    s = re.sub(r"\$([^$]+)\$", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip(" -·:")
    if max_len and len(s) > max_len:
        cut = s[: max_len - 1].rsplit(" ", 1)[0]
        s = (cut if len(cut) >= max_len * 0.6 else s[: max_len - 1]) + "…"
    return s


def _wrap_svg_title(title, max_chars=62):
    """Wrap a long chart title into at most 2 balanced lines so SVG headers never clip on the right."""
    clean = _clean_label(title)
    if len(clean) <= max_chars:
        return [clean]
    words = clean.split(" ")
    line1 = []
    cur_len = 0
    for idx, w in enumerate(words):
        if cur_len + len(w) + (1 if line1 else 0) <= max_chars or not line1:
            line1.append(w)
            cur_len += len(w) + (1 if len(line1) > 1 else 0)
        else:
            rest = " ".join(words[idx:])
            if len(rest) > max_chars + 6:
                rest = rest[: max_chars + 3].rsplit(" ", 1)[0] + "…"
            return [" ".join(line1), rest]
    return [" ".join(line1)]


def _render_svg_title_block(title, subtitle, width, fonts, pal, canon="tufte"):
    """Render a multi-line-safe SVG header block and return (svg_elements_list, top_pad_y)."""
    elements = []
    y_cursor = 0

    if canon == "editorial":
        elements.append(
            f'<rect x="0" y="0" width="{width}" height="100%" fill="#fcf8f2" rx="1"/>'
            f'<line x1="0" y1="1.5" x2="{width}" y2="1.5" stroke="#e3120b" stroke-width="2"/>'
            f'<rect x="0" y="1.5" width="34" height="5.5" fill="#e3120b"/>'
        )
        y_cursor = 10
    elif canon == "swiss":
        elements.append(
            f'<rect x="0" y="0" width="{width}" height="100%" fill="#ffffff"/>'
            f'<rect x="0" y="0" width="{width}" height="4.5" fill="#0a0a0a"/>'
        )
        y_cursor = 8
    elif canon == "few":
        elements.append(
            f'<rect x="0" y="0" width="{width}" height="100%" fill="#ffffff"/>'
            f'<rect x="0" y="0" width="5" height="28" fill="#0f766e"/>'
        )
        y_cursor = 2
    elif canon == "knaflic":
        elements.append(
            f'<rect x="0" y="0" width="{width}" height="100%" fill="#ffffff"/>'
        )
        y_cursor = 2

    x_offset = 12 if canon == "few" else 0
    if title:
        t_txt = title.upper() if canon == "swiss" else title
        lines = _wrap_svg_title(t_txt, max_chars=58 if canon == "swiss" else 64)
        for idx, line in enumerate(lines):
            y_cursor += 16 if idx == 0 else 15
            fw = "900" if canon == "swiss" else ("800" if canon == "knaflic" else "700")
            fsize = "12.5" if canon == "swiss" else "13.2"
            elements.append(
                f'<text x="{x_offset}" y="{y_cursor}" font-family="{_esc(fonts["heading"])}" '
                f'font-size="{fsize}" font-weight="{fw}" fill="{pal["ink"]}">{_esc(line)}</text>'
            )

    if subtitle:
        y_cursor += 15
        sub_clean = _clean_label(subtitle, max_len=88)
        if canon == "swiss":
            elements.append(
                f'<text x="{x_offset}" y="{y_cursor}" font-family="{_esc(fonts["mono"])}" '
                f'font-size="9.2" fill="{pal["muted"]}">// {_esc(sub_clean.upper())}</text>'
            )
        elif canon in ("tufte", "editorial"):
            elements.append(
                f'<text x="{x_offset}" y="{y_cursor}" font-family="{_esc(fonts["body"])}" '
                f'font-size="10.2" font-style="italic" fill="{pal["muted"]}">{_esc(sub_clean)}</text>'
            )
        else:
            elements.append(
                f'<text x="{x_offset}" y="{y_cursor}" font-family="{_esc(fonts["ui"])}" '
                f'font-size="10" fill="{pal["muted"]}">{_esc(sub_clean)}</text>'
            )

    top_pad = y_cursor + 20
    return elements, top_pad


def human_caption_for_chart(stem, school="tufte", is_pt=False):
    """Return a clean, publication-grade figure caption from an SVG filename stem."""
    spec = _school_spec(school)
    sname = spec.get("short_name", "Tufte")
    s = str(stem or "")
    if s == "dotplot_profile_means":
        return (
            f" Perfil Geral de Métricas Quantitativas (Média ± IC 95% · Padrão {sname})"
            if is_pt
            else f" Overall Quantitative Metric Profile (Mean ± 95% CI · {sname} Standard)"
        )
    if s == "small_multiples_distributions":
        return (
            f" Distribuição Empírica de Respostas por Variável (Small Multiples · {sname})"
            if is_pt
            else f" Empirical Response Distributions Across Variables (Small Multiples · {sname})"
        )
    if s == "priority_matrix":
        return (
            f" Matriz de Prioridade Estratégica: Importância Derivada × Desempenho ({sname})"
            if is_pt
            else f" Strategic Priority Action Matrix: Derived Importance × Performance ({sname})"
        )
    if s.startswith("residuals_cross_"):
        raw = s.replace("residuals_cross_", "").replace("_", " ")
        clean = _clean_label(raw, max_len=65)
        return (
            f" Matriz de Resíduos Padronizados Qui-Quadrado (zᵢⱼ) — {clean} ({sname})"
            if is_pt
            else f" Chi-Square Standardized Residuals Matrix (zᵢⱼ) — {clean} ({sname})"
        )
    if s.startswith("dotplot_"):
        raw = s.replace("dotplot_", "").replace("_", " ")
        clean = _clean_label(raw, max_len=65)
        return (
            f" Comparação por Segmento (IC 95%): {clean} ({sname})"
            if is_pt
            else f" Segment Comparison (95% CI): {clean} ({sname})"
        )
    return _clean_label(s.replace("_", " ").title(), max_len=75)


def sparkline(values, width=120, height=24, stroke=None, stroke_width=1.2, show_endpoints=True, school="tufte"):
    """Generate an inline SVG sparkline with min/max endpoint dots."""
    clean = [float(v) for v in values if v is not None and not math.isnan(float(v))]
    if len(clean) < 2:
        return ""
    spec = _school_spec(school)
    pal = spec["palette"]
    canon = _norm_school(school)
    line_stroke = stroke or (pal["primary"] if canon in ("knaflic", "editorial", "few") else pal["ink"])

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
    area = ""
    if canon == "editorial":
        area_pts = f"{coords[0][0]:.1f},{height - pad_y} " + polyline + f" {coords[-1][0]:.1f},{height - pad_y}"
        area = f'<polygon points="{area_pts}" fill="rgba(0, 86, 137, 0.14)"/>'

    dots = ""
    if show_endpoints:
        fx, fy, _ = coords[0]
        lx, ly, _ = coords[-1]
        min_pt = min(coords, key=lambda c: c[2])
        max_pt = max(coords, key=lambda c: c[2])
        dots = (
            f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="1.8" fill="{pal["muted"]}"/>'
            f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="2.0" fill="{pal["ink"]}"/>'
            f'<circle cx="{min_pt[0]:.1f}" cy="{min_pt[1]:.1f}" r="1.9" fill="{pal["alert_neg"]}"/>'
            f'<circle cx="{max_pt[0]:.1f}" cy="{max_pt[1]:.1f}" r="2.1" fill="{pal["alert_pos"]}"/>'
        )
    return (
        f'<svg class="sparkline" data-school="{_esc(canon)}" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
        f"{area}"
        f'<polyline fill="none" stroke="{line_stroke}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round" points="{polyline}"/>'
        f"{dots}</svg>"
    )


def bullet_plot(labels, values, errors=None, title="", subtitle="", unit="", width=600, height=None):
    """Stephen Few School: Bullet Graph with 3 qualitative bands, target crossbar, 95% CI & Δ% variance column."""
    if not labels or not values:
        return ""
    spec = _school_spec("few")
    pal = spec["palette"]
    fonts = spec["fonts"]
    n = len(labels)
    row_h = 30
    header_els, top_pad = _render_svg_title_block(title, subtitle, width, fonts, pal, canon="few")
    bottom_pad = 30
    if height is None:
        height = max(130, top_pad + n * row_h + bottom_pad)

    clean_vals = [float(v) for v in values]
    clean_errs = [
        float(e) if (errors and i < len(errors) and errors[i] is not None) else 0.0
        for i, e in enumerate(errors or [0.0] * n)
    ]
    clean_labels = [_clean_label(l, max_len=28) for l in labels]

    highs = [v + e for v, e in zip(clean_vals, clean_errs)]
    axis_min = min(0.0, min(v - e for v, e in zip(clean_vals, clean_errs)))
    axis_max = max(highs) * 1.12 if max(highs) > 0 else 10.0
    rng = axis_max - axis_min if axis_max != axis_min else 1.0

    pad_left = min(195, max(125, max(len(l) for l in clean_labels) * 6 + 16))
    pad_right = 135  # Space for Value ± CI + Variance Δ% badge
    plot_w = max(160, width - pad_left - pad_right)

    def x_pos(val):
        return pad_left + ((max(axis_min, val) - axis_min) / rng) * plot_w

    mean_val = sum(clean_vals) / len(clean_vals)
    target_x = x_pos(mean_val)

    elements = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" data-school="few" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{_esc(_clean_label(title))}">'
    ] + header_els

    # Column sub-headers (Stephen Few dashboard table-graph hybrid)
    elements.append(
        f'<text x="{pad_left - 8}" y="{top_pad - 11}" text-anchor="end" font-family="{_esc(fonts["ui"])}" '
        f'font-size="8.5" font-weight="700" fill="#64748b">SEGMENT / METRIC</text>'
        f'<text x="{pad_left}" y="{top_pad - 11}" font-family="{_esc(fonts["ui"])}" '
        f'font-size="8.5" font-weight="700" fill="#64748b">BULLET TRACK (POOR / SATISFACTORY / GOOD)</text>'
        f'<text x="{pad_left + plot_w + 8}" y="{top_pad - 11}" font-family="{_esc(fonts["ui"])}" '
        f'font-size="8.5" font-weight="700" fill="#64748b">ACTUAL ± CI</text>'
        f'<text x="{width - 6}" y="{top_pad - 11}" text-anchor="end" font-family="{_esc(fonts["ui"])}" '
        f'font-size="8.5" font-weight="700" fill="#64748b">Δ VS MEAN</text>'
    )

    for i, (trunc_label, val, err) in enumerate(zip(clean_labels, clean_vals, clean_errs)):
        y = top_pad + i * row_h
        b1_w = plot_w * 0.55
        b2_w = plot_w * 0.80
        elements.append(
            f'<rect x="{pad_left:.1f}" y="{y - 9}" width="{plot_w:.1f}" height="18" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="0.5"/>'
            f'<rect x="{pad_left:.1f}" y="{y - 9}" width="{b2_w:.1f}" height="18" fill="#e2e8f0"/>'
            f'<rect x="{pad_left:.1f}" y="{y - 9}" width="{b1_w:.1f}" height="18" fill="#cbd5e1"/>'
        )
        elements.append(
            f'<text x="{pad_left - 8}" y="{y + 3.5}" text-anchor="end" '
            f'font-family="{_esc(fonts["ui"])}" font-size="10" font-weight="600" fill="#0f172a">'
            f"{_esc(trunc_label)}</text>"
        )
        bar_w = max(2.0, x_pos(val) - pad_left)
        is_alert = (val + err) < mean_val * 0.92
        bar_color = "#dc2626" if is_alert else ("#0f766e" if val >= mean_val * 1.03 else "#1e293b")
        elements.append(
            f'<rect x="{pad_left:.1f}" y="{y - 3.5}" width="{bar_w:.1f}" height="7" fill="{bar_color}"/>'
        )
        if err > 0:
            x1 = max(pad_left, x_pos(val - err))
            x2 = min(pad_left + plot_w, x_pos(val + err))
            elements.append(
                f'<line x1="{x1:.1f}" y1="{y}" x2="{x2:.1f}" y2="{y}" stroke="#334155" stroke-width="1.3"/>'
                f'<line x1="{x2:.1f}" y1="{y - 3}" x2="{x2:.1f}" y2="{y + 3}" stroke="#334155" stroke-width="1.2"/>'
            )
        # Perpendicular target / benchmark marker (Stephen Few signature)
        elements.append(
            f'<line x1="{target_x:.1f}" y1="{y - 8}" x2="{target_x:.1f}" y2="{y + 8}" '
            f'stroke="#0f172a" stroke-width="2.2"/>'
        )
        val_str = f"{val:.2f}{unit}" if abs(val) < 10 and abs(val - round(val)) > 0.01 else f"{val:.1f}{unit}"
        if err > 0:
            val_str += f" ±{err:.2f}" if err < 1 else f" ±{err:.1f}"
        elements.append(
            f'<text x="{pad_left + plot_w + 8}" y="{y + 3.5}" '
            f'font-family="{_esc(fonts["mono"])}" font-size="9.5" font-weight="600" '
            f'fill="#0f172a">{_esc(val_str)}</text>'
        )
        # Variance Δ% vs benchmark
        delta_pct = ((val - mean_val) / abs(mean_val) * 100.0) if abs(mean_val) > 1e-6 else 0.0
        d_color = "#0f766e" if delta_pct > 2.0 else ("#dc2626" if delta_pct < -2.0 else "#64748b")
        elements.append(
            f'<text x="{width - 6}" y="{y + 3.5}" text-anchor="end" '
            f'font-family="{_esc(fonts["mono"])}" font-size="9.5" font-weight="700" '
            f'fill="{d_color}">{delta_pct:+.1f}%</text>'
        )

    y_footer = top_pad + (n - 1) * row_h + 20
    elements.append(
        f'<line x1="0" y1="{y_footer - 10}" x2="{width}" y2="{y_footer - 10}" stroke="#cbd5e1" stroke-width="0.8"/>'
        f'<text x="0" y="{y_footer + 2}" font-family="{_esc(fonts["ui"])}" '
        f'font-size="8.5" fill="#475569">Stephen Few Perceptual Bullet Graph · Vertical Marker (|) = Benchmark Mean ({mean_val:.2f}{_esc(unit)}) · Right Column = Variance Δ%</text>'
        f"</svg>"
    )
    return "\n".join(elements)


def swd_focus_bar(labels, values, errors=None, title="", subtitle="", unit="", width=600, height=None):
    """Cole Knaflic (Storytelling with Data) School: Decluttered grey context bars + bold focal bar + narrative callout box."""
    if not labels or not values:
        return ""
    spec = _school_spec("knaflic")
    pal = spec["palette"]
    fonts = spec["fonts"]
    n = len(labels)
    row_h = 28
    clean_vals = [float(v) for v in values]
    clean_errs = [
        float(e) if (errors and i < len(errors) and errors[i] is not None) else 0.0
        for i, e in enumerate(errors or [0.0] * n)
    ]
    clean_labels = [_clean_label(l, max_len=27) for l in labels]

    max_idx = int(max(range(n), key=lambda idx: clean_vals[idx]))
    min_idx = int(min(range(n), key=lambda idx: clean_vals[idx]))
    mean_val = sum(clean_vals) / len(clean_vals)
    top_label = clean_labels[max_idx]
    top_val = clean_vals[max_idx]
    pct_above = ((top_val - mean_val) / abs(mean_val) * 100.0) if abs(mean_val) > 1e-6 else 0.0

    # Action title in SWD style
    action_sub = f"Focal highlight: '{top_label}' leads at {top_val:.2f}{unit} ({pct_above:+.1f}% vs. mean {mean_val:.2f}{unit})"
    header_els, top_pad = _render_svg_title_block(title, action_sub, width, fonts, pal, canon="knaflic")
    bottom_pad = 28
    if height is None:
        height = max(145, top_pad + n * row_h + bottom_pad)

    highs = [v + e for v, e in zip(clean_vals, clean_errs)]
    axis_min = min(0.0, min(clean_vals))
    axis_max = max(highs) * 1.15 if max(highs) > 0 else 10.0
    rng = axis_max - axis_min if axis_max != axis_min else 1.0

    pad_left = min(190, max(120, max(len(l) for l in clean_labels) * 6 + 14))
    callout_w = 155 if n >= 2 else 90
    plot_w = max(145, width - pad_left - callout_w - 65)

    def x_pos(val):
        return pad_left + ((max(axis_min, val) - axis_min) / rng) * plot_w

    elements = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" data-school="knaflic" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{_esc(_clean_label(title))}">'
    ] + header_els

    for i, (trunc_label, val, err) in enumerate(zip(clean_labels, clean_vals, clean_errs)):
        y = top_pad + i * row_h
        is_top_focal = (i == max_idx)
        is_bottom_pain = (n >= 3 and i == min_idx and (max(clean_vals) - min(clean_vals)) > 0.12 * max(abs(mean_val), 1.0))

        if is_top_focal:
            bar_fill = "#1e40af"
            lbl_fill = "#0f172a"
            fw = "700"
        elif is_bottom_pain:
            bar_fill = "#ea580c"
            lbl_fill = "#9a3412"
            fw = "700"
        else:
            bar_fill = "#cbd5e1"
            lbl_fill = "#64748b"
            fw = "400"

        bar_w = max(4.0, x_pos(val) - pad_left)
        elements.append(
            f'<text x="{pad_left - 10}" y="{y + 4}" text-anchor="end" '
            f'font-family="{_esc(fonts["body"])}" font-size="10.2" font-weight="{fw}" fill="{lbl_fill}">'
            f"{_esc(trunc_label)}</text>"
            f'<rect x="{pad_left:.1f}" y="{y - 8}" width="{bar_w:.1f}" height="16" rx="2.5" fill="{bar_fill}"/>'
        )
        val_str = f"{val:.2f}{unit}" if abs(val) < 10 and abs(val - round(val)) > 0.01 else f"{val:.1f}{unit}"
        if is_top_focal:
            val_str += " ★"
        elements.append(
            f'<text x="{pad_left + bar_w + 6:.1f}" y="{y + 4}" '
            f'font-family="{_esc(fonts["ui"])}" font-size="9.8" font-weight="{fw}" '
            f'fill="{bar_fill if (is_top_focal or is_bottom_pain) else "#64748b"}">'
            f"{_esc(val_str)}</text>"
        )

    # Cole Knaflic signature Preattentive Narrative Callout Annotation Card on the right
    cx_box = width - callout_w - 4
    cy_box = top_pad - 10
    ch_box = max(64, min(84, n * row_h + 8))
    elements.append(
        f'<rect x="{cx_box}" y="{cy_box}" width="{callout_w}" height="{ch_box}" rx="4" '
        f'fill="#eff6ff" stroke="#bfdbfe" stroke-width="1"/>'
        f'<rect x="{cx_box}" y="{cy_box}" width="4" height="{ch_box}" rx="2" fill="#1e40af"/>'
        f'<text x="{cx_box + 10}" y="{cy_box + 15}" font-family="{_esc(fonts["ui"])}" '
        f'font-size="8.5" font-weight="800" fill="#1e40af">💡 KEY TAKEAWAY</text>'
        f'<text x="{cx_box + 10}" y="{cy_box + 29}" font-family="{_esc(fonts["body"])}" '
        f'font-size="9" font-weight="700" fill="#0f172a">{_esc(top_label[:20])}</text>'
        f'<text x="{cx_box + 10}" y="{cy_box + 42}" font-family="{_esc(fonts["body"])}" '
        f'font-size="8.5" fill="#334155">Peak: {top_val:.2f}{_esc(unit)} ({pct_above:+.1f}%)</text>'
        f'<text x="{cx_box + 10}" y="{cy_box + 54}" font-family="{_esc(fonts["body"])}" '
        f'font-size="8.2" fill="#64748b">Context muted in grey</text>'
    )

    elements.append("</svg>")
    return "\n".join(elements)


def swiss_lollipop_plot(labels, values, errors=None, title="", subtitle="", unit="", width=600, height=None):
    """Swiss Grid & Jacques Bertin School: Exposed architectural modular grid & Bertin retinal symbol encoding."""
    if not labels or not values:
        return ""
    spec = _school_spec("swiss")
    pal = spec["palette"]
    fonts = spec["fonts"]
    n = len(labels)
    row_h = 28
    header_els, top_pad = _render_svg_title_block(title, subtitle, width, fonts, pal, canon="swiss")
    bottom_pad = 28
    if height is None:
        height = max(130, top_pad + n * row_h + bottom_pad)

    clean_vals = [float(v) for v in values]
    clean_errs = [
        float(e) if (errors and i < len(errors) and errors[i] is not None) else 0.0
        for i, e in enumerate(errors or [0.0] * n)
    ]
    clean_labels = [_clean_label(l, max_len=26) for l in labels]

    lows = [v - e for v, e in zip(clean_vals, clean_errs)]
    highs = [v + e for v, e in zip(clean_vals, clean_errs)]
    mn = min(0.0, min(lows))
    mx = max(highs) * 1.12 if max(highs) != 0 else 10.0
    rng = (mx - mn) if mx != mn else 1.0

    idx_col_w = 28
    pad_left = min(205, max(135, idx_col_w + max(len(l) for l in clean_labels) * 6 + 14))
    pad_right = 92
    plot_w = max(155, width - pad_left - pad_right)

    def x_pos(val):
        return pad_left + ((val - mn) / rng) * plot_w

    mean_val = sum(clean_vals) / len(clean_vals)
    mean_x = x_pos(mean_val)

    elements = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" data-school="swiss" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{_esc(_clean_label(title))}">'
    ] + header_els

    grid_top = top_pad - 12
    grid_h = n * row_h
    # Outer architectural modular frame (exposed hairlines)
    elements.append(
        f'<rect x="0" y="{grid_top}" width="{width}" height="{grid_h}" fill="#ffffff" stroke="#0a0a0a" stroke-width="1.8"/>'
        f'<line x1="{idx_col_w}" y1="{grid_top}" x2="{idx_col_w}" y2="{grid_top + grid_h}" stroke="#0a0a0a" stroke-width="1.2"/>'
        f'<line x1="{pad_left}" y1="{grid_top}" x2="{pad_left}" y2="{grid_top + grid_h}" stroke="#0a0a0a" stroke-width="1.5"/>'
        f'<line x1="{pad_left + plot_w}" y1="{grid_top}" x2="{pad_left + plot_w}" y2="{grid_top + grid_h}" stroke="#0a0a0a" stroke-width="1.5"/>'
    )
    # Internal modular coordinate gridlines
    for frac in (0.25, 0.5, 0.75):
        gx = pad_left + plot_w * frac
        elements.append(
            f'<line x1="{gx:.1f}" y1="{grid_top}" x2="{gx:.1f}" y2="{grid_top + grid_h}" stroke="#e5e5dc" stroke-width="0.8"/>'
        )
    elements.append(
        f'<line x1="{mean_x:.1f}" y1="{grid_top}" x2="{mean_x:.1f}" y2="{grid_top + grid_h}" '
        f'stroke="#e63946" stroke-width="1.4" stroke-dasharray="3,2"/>'
    )

    for i, (trunc_label, val, err) in enumerate(zip(clean_labels, clean_vals, clean_errs)):
        row_top = grid_top + i * row_h
        y = row_top + row_h / 2
        cx = x_pos(val)
        if i > 0:
            elements.append(
                f'<line x1="0" y1="{row_top:.1f}" x2="{width}" y2="{row_top:.1f}" stroke="#0a0a0a" stroke-width="0.9"/>'
            )
        elements.append(
            f'<text x="{idx_col_w / 2:.1f}" y="{y + 3.5:.1f}" text-anchor="middle" '
            f'font-family="{_esc(fonts["mono"])}" font-size="9" font-weight="700" fill="#e63946">{i+1:02d}</text>'
            f'<text x="{idx_col_w + 6}" y="{y + 3.5:.1f}" font-family="{_esc(fonts["heading"])}" '
            f'font-size="9.8" font-weight="700" fill="#0a0a0a">{_esc(trunc_label)}</text>'
            f'<line x1="{pad_left:.1f}" y1="{y:.1f}" x2="{cx:.1f}" y2="{y:.1f}" stroke="#0a0a0a" stroke-width="2.2"/>'
        )
        if err > 0:
            x1 = max(pad_left, x_pos(val - err))
            x2 = min(pad_left + plot_w, x_pos(val + err))
            elements.append(
                f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" stroke="#0a0a0a" stroke-width="1.2"/>'
                f'<line x1="{x1:.1f}" y1="{y - 3:.1f}" x2="{x1:.1f}" y2="{y + 3:.1f}" stroke="#0a0a0a" stroke-width="1.2"/>'
                f'<line x1="{x2:.1f}" y1="{y - 3:.1f}" x2="{x2:.1f}" y2="{y + 3:.1f}" stroke="#0a0a0a" stroke-width="1.2"/>'
            )
        # Bertin retinal size + shape encoding
        rel_mag = max(0.45, min(1.0, (val - mn) / rng))
        sym_r = 3.2 + 2.4 * rel_mag
        if val >= mean_val:
            elements.append(
                f'<rect x="{cx - sym_r:.1f}" y="{y - sym_r:.1f}" width="{sym_r*2:.1f}" height="{sym_r*2:.1f}" '
                f'fill="#1d3557" stroke="#0a0a0a" stroke-width="1.1"/>'
            )
        else:
            elements.append(
                f'<circle cx="{cx:.1f}" cy="{y:.1f}" r="{sym_r:.1f}" fill="#e63946" stroke="#0a0a0a" stroke-width="1.1"/>'
            )
        val_str = f"{val:.2f}{unit}" if abs(val) < 10 and abs(val - round(val)) > 0.01 else f"{val:.1f}{unit}"
        if err > 0:
            val_str += f"±{err:.2f}" if err < 1 else f"±{err:.1f}"
        elements.append(
            f'<text x="{width - 6}" y="{y + 3.5:.1f}" text-anchor="end" '
            f'font-family="{_esc(fonts["mono"])}" font-size="9.2" font-weight="700" fill="#0a0a0a">{_esc(val_str)}</text>'
        )

    elements.append(
        f'<text x="0" y="{height - 6}" font-family="{_esc(fonts["mono"])}" font-size="8.5" fill="#40403c">'
        f"SWISS MODULAR GRID // BERTIN RETINAL ENCODING · REF MEAN = {mean_val:.2f}{_esc(unit)} [■ ≥ MEAN | ● &lt; MEAN]</text></svg>"
    )
    return "\n".join(elements)


def editorial_lollipop_plot(labels, values, errors=None, title="", subtitle="", unit="", width=600, height=None):
    """The Economist / FT Editorial School: Newsprint canvas, crimson header tag, top scale ticks & right-hand value axis."""
    if not labels or not values:
        return ""
    spec = _school_spec("editorial")
    pal = spec["palette"]
    fonts = spec["fonts"]
    n = len(labels)
    row_h = 28
    header_els, top_pad = _render_svg_title_block(title, subtitle, width, fonts, pal, canon="editorial")
    top_pad += 8  # Room for top scale axis labels (Economist signature)
    bottom_pad = 28
    if height is None:
        height = max(135, top_pad + n * row_h + bottom_pad)

    clean_vals = [float(v) for v in values]
    clean_errs = [
        float(e) if (errors and i < len(errors) and errors[i] is not None) else 0.0
        for i, e in enumerate(errors or [0.0] * n)
    ]
    clean_labels = [_clean_label(l, max_len=28) for l in labels]

    lows = [v - e for v, e in zip(clean_vals, clean_errs)]
    highs = [v + e for v, e in zip(clean_vals, clean_errs)]
    mn = min(0.0, min(lows))
    mx = max(highs) * 1.12 if max(highs) != 0 else 10.0
    rng = (mx - mn) if mx != mn else 1.0

    pad_left = min(195, max(125, max(len(l) for l in clean_labels) * 6 + 14))
    pad_right = 88
    plot_w = max(160, width - pad_left - pad_right)

    def x_pos(val):
        return pad_left + ((val - mn) / rng) * plot_w

    max_idx = int(max(range(n), key=lambda idx: clean_vals[idx]))
    mean_val = sum(clean_vals) / len(clean_vals)
    mean_x = x_pos(mean_val)

    elements = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" data-school="editorial" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{_esc(_clean_label(title))}">'
    ] + header_els

    # Vertical grid lines & top scale numbers (Economist chart grammar)
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        gx = pad_left + plot_w * frac
        gval = mn + rng * frac
        elements.append(
            f'<line x1="{gx:.1f}" y1="{top_pad - 12}" x2="{gx:.1f}" y2="{top_pad + (n - 1) * row_h + 10}" '
            f'stroke="#dfd8ce" stroke-width="0.9"/>'
            f'<text x="{gx:.1f}" y="{top_pad - 15}" text-anchor="middle" font-family="{_esc(fonts["ui"])}" '
            f'font-size="8.2" fill="#59544f">{gval:.1f}</text>'
        )
    elements.append(
        f'<line x1="{mean_x:.1f}" y1="{top_pad - 12}" x2="{mean_x:.1f}" y2="{top_pad + (n - 1) * row_h + 10}" '
        f'stroke="#e3120b" stroke-width="1.1" stroke-dasharray="3,2"/>'
    )

    for i, (trunc_label, val, err) in enumerate(zip(clean_labels, clean_vals, clean_errs)):
        y = top_pad + i * row_h
        cx = x_pos(val)
        is_lead = (i == max_idx)
        mark_color = "#e3120b" if is_lead else "#005689"

        elements.append(
            f'<line x1="0" y1="{y + row_h/2:.1f}" x2="{width}" y2="{y + row_h/2:.1f}" stroke="#eee8de" stroke-width="0.7"/>'
            f'<text x="{pad_left - 10}" y="{y + 4}" text-anchor="end" '
            f'font-family="{_esc(fonts["ui"])}" font-size="10.2" '
            f'font-weight="{"700" if is_lead else "500"}" fill="#1a1817">{_esc(trunc_label)}</text>'
            f'<line x1="{pad_left:.1f}" y1="{y}" x2="{cx:.1f}" y2="{y}" stroke="{mark_color}" stroke-width="3.4"/>'
        )
        if err > 0:
            x1 = max(pad_left, x_pos(val - err))
            x2 = min(pad_left + plot_w, x_pos(val + err))
            elements.append(
                f'<line x1="{x1:.1f}" y1="{y}" x2="{x2:.1f}" y2="{y}" stroke="#1a1817" stroke-width="1.2"/>'
            )
        elements.append(f'<circle cx="{cx:.1f}" cy="{y}" r="4.5" fill="{mark_color}" stroke="#fcf8f2" stroke-width="1"/>')
        val_str = f"{val:.2f}{unit}" if abs(val) < 10 and abs(val - round(val)) > 0.01 else f"{val:.1f}{unit}"
        if err > 0:
            val_str += f" (±{err:.2f})" if err < 1 else f" (±{err:.1f})"
        elements.append(
            f'<text x="{width - 6}" y="{y + 4}" text-anchor="end" '
            f'font-family="{_esc(fonts["ui"])}" font-size="9.8" '
            f'font-weight="{"700" if is_lead else "500"}" fill="{mark_color}">{_esc(val_str)}</text>'
        )

    elements.append(
        f'<line x1="0" y1="{height - 16}" x2="{width}" y2="{height - 16}" stroke="#1a1817" stroke-width="0.8"/>'
        f'<text x="0" y="{height - 4}" font-family="{_esc(fonts["ui"])}" font-size="8.5" fill="#59544f">'
        f"Source: Data-Pro-Skill Survey Analysis (95% CI) · Red dashed line = Mean ({mean_val:.2f}{_esc(unit)})</text></svg>"
    )
    return "\n".join(elements)


def dot_plot(labels, values, errors=None, title="", subtitle="", unit="", width=600, height=None, school="tufte"):
    """Dispatch primary metric/segment comparison chart according to the active Data Design School.

    Defaults to Edward Tufte's classic Cleveland dot plot with 95% CI whiskers & range-frame axis.
    """
    canon = _norm_school(school)
    if canon == "few":
        return bullet_plot(labels, values, errors=errors, title=title, subtitle=subtitle, unit=unit, width=width, height=height)
    if canon == "knaflic":
        return swd_focus_bar(labels, values, errors=errors, title=title, subtitle=subtitle, unit=unit, width=width, height=height)
    if canon == "swiss":
        return swiss_lollipop_plot(labels, values, errors=errors, title=title, subtitle=subtitle, unit=unit, width=width, height=height)
    if canon == "editorial":
        return editorial_lollipop_plot(labels, values, errors=errors, title=title, subtitle=subtitle, unit=unit, width=width, height=height)

    # Default: Edward Tufte Cleveland Dot Plot with Range-Frame Axis
    if not labels or not values:
        return ""
    spec = _school_spec("tufte")
    pal = spec["palette"]
    fonts = spec["fonts"]
    n = len(labels)
    row_h = 26
    header_els, top_pad = _render_svg_title_block(title, subtitle, width, fonts, pal, canon="tufte")
    bottom_pad = 30
    if height is None:
        height = max(120, top_pad + n * row_h + bottom_pad)

    clean_vals = [float(v) for v in values]
    clean_errs = [float(e) if (errors and i < len(errors) and errors[i] is not None) else 0.0 for i, e in enumerate(errors or [0.0] * n)]
    clean_labels = [_clean_label(l, max_len=28) for l in labels]

    lows = [v - e for v, e in zip(clean_vals, clean_errs)]
    highs = [v + e for v, e in zip(clean_vals, clean_errs)]
    mn = min(lows)
    mx = max(highs)
    if mn > 0 and mn / (mx if mx else 1) < 0.35:
        mn = 0.0
    rng = (mx - mn) if mx != mn else 1.0
    pad_val = rng * 0.08
    axis_min = mn - pad_val if mn < 0 else max(0.0, mn - pad_val)
    axis_max = mx + pad_val
    axis_rng = (axis_max - axis_min) if axis_max != axis_min else 1.0

    pad_left = min(195, max(125, max(len(l) for l in clean_labels) * 6 + 16))
    pad_right = 88
    plot_w = max(160, width - pad_left - pad_right)

    def x_pos(val):
        return pad_left + ((val - axis_min) / axis_rng) * plot_w

    mean_val = sum(clean_vals) / len(clean_vals)
    mean_x = x_pos(mean_val)

    elements = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" data-school="tufte" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{_esc(_clean_label(title))}">'
    ] + header_els

    elements.append(
        f'<line x1="{mean_x:.1f}" y1="{top_pad - 8}" x2="{mean_x:.1f}" y2="{top_pad + (n - 1) * row_h + 8}" '
        f'stroke="#888888" stroke-width="0.9" stroke-dasharray="3,3"/>'
    )

    for i, (trunc_label, val, err) in enumerate(zip(clean_labels, clean_vals, clean_errs)):
        y = top_pad + i * row_h
        cx = x_pos(val)
        dot_color = "#a61c1c" if (val + err) < mean_val else "#1b4f72"

        elements.append(
            f'<line x1="{pad_left}" y1="{y}" x2="{pad_left + plot_w}" y2="{y}" '
            f'stroke="#e6e6de" stroke-width="0.7" stroke-dasharray="1,3"/>'
            f'<text x="{pad_left - 8}" y="{y + 4}" text-anchor="end" '
            f'font-family="Georgia, Palatino, serif" font-size="10.5" fill="#222222">{_esc(trunc_label)}</text>'
        )
        if err > 0:
            x1 = max(pad_left, x_pos(val - err))
            x2 = min(pad_left + plot_w, x_pos(val + err))
            elements.append(
                f'<line x1="{x1:.1f}" y1="{y}" x2="{x2:.1f}" y2="{y}" stroke="#555555" stroke-width="1.2"/>'
                f'<line x1="{x1:.1f}" y1="{y - 3}" x2="{x1:.1f}" y2="{y + 3}" stroke="#555555" stroke-width="1.0"/>'
                f'<line x1="{x2:.1f}" y1="{y - 3}" x2="{x2:.1f}" y2="{y + 3}" stroke="#555555" stroke-width="1.0"/>'
            )
        elements.append(f'<circle cx="{cx:.1f}" cy="{y}" r="3.8" fill="{dot_color}"/>')
        val_str = f"{val:.2f}{unit}" if abs(val) < 10 and abs(val - round(val)) > 0.01 else f"{val:.1f}{unit}"
        if err > 0:
            val_str += f" (±{err:.2f})" if err < 1 else f" (±{err:.1f})"
        elements.append(
            f'<text x="{pad_left + plot_w + 8}" y="{y + 4}" '
            f'font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="10" fill="#222222">{_esc(val_str)}</text>'
        )

    # Tufte Range-Frame Bottom Axis (spans strictly from observed min to observed max)
    rf_y = top_pad + (n - 1) * row_h + 12
    x_min_obs = x_pos(min(lows))
    x_max_obs = x_pos(max(highs))
    elements.append(
        f'<line x1="{x_min_obs:.1f}" y1="{rf_y}" x2="{x_max_obs:.1f}" y2="{rf_y}" stroke="#111111" stroke-width="1.0"/>'
        f'<line x1="{x_min_obs:.1f}" y1="{rf_y - 3}" x2="{x_min_obs:.1f}" y2="{rf_y + 3}" stroke="#111111" stroke-width="1.0"/>'
        f'<line x1="{x_max_obs:.1f}" y1="{rf_y - 3}" x2="{x_max_obs:.1f}" y2="{rf_y + 3}" stroke="#111111" stroke-width="1.0"/>'
        f'<text x="{x_min_obs:.1f}" y="{rf_y + 11}" text-anchor="middle" font-family="Georgia, Palatino, serif" font-size="8.5" fill="#555555">{min(lows):.1f}</text>'
        f'<text x="{mean_x:.1f}" y="{rf_y + 11}" text-anchor="middle" font-family="Georgia, Palatino, serif" font-size="8.5" font-style="italic" fill="#555555">Mean: {mean_val:.2f}{_esc(unit)}</text>'
        f'<text x="{x_max_obs:.1f}" y="{rf_y + 11}" text-anchor="middle" font-family="Georgia, Palatino, serif" font-size="8.5" fill="#555555">{max(highs):.1f}</text>'
        f"</svg>"
    )
    return "\n".join(elements)


def diverging_bar(labels, neg_pcts, neu_pcts, pos_pcts, title="", subtitle="", width=600, school="tufte"):
    """Generate a horizontally centered diverging stacked bar chart for Likert / NPS sentiment."""
    if not labels:
        return ""
    spec = _school_spec(school)
    pal = spec["palette"]
    fonts = spec["fonts"]
    canon = _norm_school(school)

    n = len(labels)
    row_h = 28
    header_els, top_pad = _render_svg_title_block(title, subtitle, width, fonts, pal, canon=canon)
    height = max(120, top_pad + n * row_h + 28)
    clean_labels = [_clean_label(l, max_len=26) for l in labels]
    pad_left = min(190, max(120, max(len(l) for l in clean_labels) * 6 + 14))
    pad_right = 80
    plot_w = max(160, width - pad_left - pad_right)
    mid_x = pad_left + plot_w / 2.0
    scale = plot_w / 200.0

    elements = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" data-school="{_esc(canon)}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{_esc(_clean_label(title))}">'
    ] + header_els

    elements.append(
        f'<line x1="{mid_x:.1f}" y1="{top_pad - 10}" x2="{mid_x:.1f}" y2="{top_pad + (n - 1) * row_h + 12}" '
        f'stroke="{pal["ink"]}" stroke-width="0.9" stroke-dasharray="2,2"/>'
    )

    for i, lbl in enumerate(clean_labels):
        y = top_pad + i * row_h
        neg = float(neg_pcts[i]) if i < len(neg_pcts) else 0.0
        neu = float(neu_pcts[i]) if i < len(neu_pcts) else 0.0
        pos = float(pos_pcts[i]) if i < len(pos_pcts) else 0.0
        net = pos - neg

        det_w = neg * scale
        pas_w = neu * scale
        pro_w = pos * scale

        elements.append(
            f'<text x="{pad_left - 8}" y="{y + 4}" text-anchor="end" '
            f'font-family="{_esc(fonts["body"])}" font-size="10.2" fill="{pal["ink"]}">'
            f"{_esc(lbl)}</text>"
        )
        x_det = mid_x - (pas_w / 2.0) - det_w
        x_pas = mid_x - (pas_w / 2.0)
        x_pro = mid_x + (pas_w / 2.0)

        if det_w > 0:
            elements.append(
                f'<rect x="{x_det:.1f}" y="{y - 6}" width="{det_w:.1f}" height="12" fill="{pal["alert_neg"]}" opacity="0.88"/>'
            )
        if pas_w > 0:
            elements.append(
                f'<rect x="{x_pas:.1f}" y="{y - 6}" width="{pas_w:.1f}" height="12" fill="{pal["neutral_bar"]}"/>'
            )
        if pro_w > 0:
            elements.append(
                f'<rect x="{x_pro:.1f}" y="{y - 6}" width="{pro_w:.1f}" height="12" fill="{pal["alert_pos"]}" opacity="0.9"/>'
            )
        elements.append(
            f'<text x="{pad_left + plot_w + 6}" y="{y + 4}" '
            f'font-family="{_esc(fonts["ui"])}" font-size="9.5" '
            f'font-weight="700" fill="{pal["ink"]}">Net {net:+.0f}%</text>'
        )

    elements.append("</svg>")
    return "\n".join(elements)


def residual_heatmap_svg(row_labels, col_labels, z_matrix, title="", subtitle="", width=600, school="tufte"):
    """Generate a school-authentic SVG matrix of Chi-Square Standardized Residuals (zᵢⱼ):
      - tufte:     Minimalist Booktabs Supertable (zero vertical lines, circle cue for |z| >= 1.96)
      - few:       Perceptual Diverging Bar Matrix (inline horizontal +/- z-bars inside each cell)
      - knaflic:   SWD Preattentive Highlight Table (muted grey noise, solid focal badges for |z| >= 1.96)
      - swiss:     Jacques Bertin Permutable Retinal Matrix (scaled circles/squares inside exposed black grid)
      - editorial: Economist/FT Newsprint Heatmap Card with crimson header tag & editorial source line
    """
    if not row_labels or not col_labels or not z_matrix:
        return ""
    spec = _school_spec(school)
    pal = spec["palette"]
    fonts = spec["fonts"]
    canon = _norm_school(school)

    clean_rows = [_clean_label(r, max_len=22) for r in row_labels]
    clean_cols = [_clean_label(c, max_len=12) for c in col_labels]
    n_rows = len(clean_rows)
    n_cols = len(clean_cols)

    pad_left = min(165, max(100, max(len(r) for r in clean_rows) * 6 + 14))
    cell_w = max(44, min(88, (width - pad_left - 20) / max(1, n_cols)))
    actual_w = int(max(width, pad_left + n_cols * cell_w + 20))
    header_els, top_pad = _render_svg_title_block(title, subtitle, actual_w, fonts, pal, canon=canon)
    top_pad += 8
    row_h = 28
    height = top_pad + n_rows * row_h + 34

    elements = [
        f'<svg viewBox="0 0 {actual_w} {height}" width="100%" height="{height}" data-school="{_esc(canon)}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{_esc(_clean_label(title))}">'
    ] + header_els

    # Column Headers
    if canon == "tufte":
        elements.append(
            f'<line x1="0" y1="{top_pad - 22}" x2="{actual_w - 10}" y2="{top_pad - 22}" stroke="#111111" stroke-width="1.6"/>'
            f'<line x1="0" y1="{top_pad - 2}" x2="{actual_w - 10}" y2="{top_pad - 2}" stroke="#111111" stroke-width="0.9"/>'
        )
    elif canon == "swiss":
        elements.append(
            f'<rect x="{pad_left}" y="{top_pad - 20}" width="{n_cols * cell_w:.1f}" height="20" fill="#0a0a0a"/>'
        )

    for j, c_lbl in enumerate(clean_cols):
        cx = pad_left + j * cell_w + cell_w / 2
        hdr_fill = "#ffffff" if canon == "swiss" else ("#64748b" if canon == "knaflic" else pal["ink"])
        elements.append(
            f'<text x="{cx:.1f}" y="{top_pad - 7}" text-anchor="middle" '
            f'font-family="{_esc(fonts["mono"] if canon == "swiss" else fonts["ui"])}" font-size="9" '
            f'font-weight="700" fill="{hdr_fill}">{_esc(c_lbl)}</text>'
        )

    for i, r_lbl in enumerate(clean_rows):
        y = top_pad + i * row_h
        elements.append(
            f'<text x="{pad_left - 8}" y="{y + 17}" text-anchor="end" '
            f'font-family="{_esc(fonts["body"])}" font-size="10" '
            f'font-weight="{"700" if canon == "swiss" else "500"}" fill="{pal["ink"]}">'
            f"{_esc(r_lbl)}</text>"
        )
        if canon == "tufte" and i > 0:
            elements.append(
                f'<line x1="0" y1="{y}" x2="{actual_w - 10}" y2="{y}" stroke="#e2e2d8" stroke-width="0.6"/>'
            )

        row_vals = z_matrix[i] if i < len(z_matrix) else []
        for j in range(n_cols):
            z = float(row_vals[j]) if j < len(row_vals) else 0.0
            x = pad_left + j * cell_w
            cx = x + cell_w / 2
            cy = y + row_h / 2 - 1
            is_sig_pos = z >= 1.96
            is_sig_neg = z <= -1.96
            is_sig = is_sig_pos or is_sig_neg

            if canon == "tufte":
                # Minimalist Booktabs supertable: no vertical borders, subtle highlight on |z| >= 1.96
                if is_sig:
                    ring_col = "#1b4f72" if is_sig_pos else "#a61c1c"
                    bg_col = "#eef4f8" if is_sig_pos else "#f9ebeb"
                    elements.append(
                        f'<rect x="{x + 3:.1f}" y="{y + 3}" width="{cell_w - 6:.1f}" height="{row_h - 6}" rx="2" '
                        f'fill="{bg_col}" stroke="{ring_col}" stroke-width="0.9"/>'
                    )
                txt_col = "#111111" if is_sig else "#666666"
                fw = "700" if is_sig else "400"
                elements.append(
                    f'<text x="{cx:.1f}" y="{y + 17}" text-anchor="middle" '
                    f'font-family="Georgia, Palatino, serif" font-size="9.8" font-weight="{fw}" fill="{txt_col}">{z:+.2f}</text>'
                )

            elif canon == "few":
                # Stephen Few Perceptual Diverging Bar inside each cell
                elements.append(
                    f'<rect x="{x:.1f}" y="{y}" width="{cell_w:.1f}" height="{row_h - 2}" fill="#ffffff" stroke="#cbd5e1" stroke-width="0.6"/>'
                    f'<line x1="{cx:.1f}" y1="{y + 2}" x2="{cx:.1f}" y2="{y + row_h - 4}" stroke="#cbd5e1" stroke-width="0.7"/>'
                )
                bar_frac = min(1.0, abs(z) / 3.5) * (cell_w / 2 - 4)
                if z >= 0:
                    b_col = "#0f766e" if is_sig_pos else "#94a3b8"
                    elements.append(
                        f'<rect x="{cx:.1f}" y="{y + row_h - 8}" width="{bar_frac:.1f}" height="4" fill="{b_col}"/>'
                    )
                else:
                    b_col = "#dc2626" if is_sig_neg else "#94a3b8"
                    elements.append(
                        f'<rect x="{cx - bar_frac:.1f}" y="{y + row_h - 8}" width="{bar_frac:.1f}" height="4" fill="{b_col}"/>'
                    )
                t_col = "#0f766e" if is_sig_pos else ("#dc2626" if is_sig_neg else "#475569")
                elements.append(
                    f'<text x="{cx:.1f}" y="{y + 14}" text-anchor="middle" font-family="{_esc(fonts["mono"])}" '
                    f'font-size="9" font-weight="{"700" if is_sig else "400"}" fill="{t_col}">{z:+.2f}</text>'
                )

            elif canon == "knaflic":
                # Cole Knaflic SWD Preattentive Table: noise muted in grey, ONLY |z| >= 1.96 pops in solid focal color
                if is_sig_pos:
                    elements.append(
                        f'<rect x="{x + 2:.1f}" y="{y + 2}" width="{cell_w - 4:.1f}" height="{row_h - 5}" rx="3" fill="#1e40af"/>'
                        f'<text x="{cx:.1f}" y="{y + 17}" text-anchor="middle" font-family="{_esc(fonts["ui"])}" '
                        f'font-size="9.5" font-weight="800" fill="#ffffff">{z:+.2f}</text>'
                    )
                elif is_sig_neg:
                    elements.append(
                        f'<rect x="{x + 2:.1f}" y="{y + 2}" width="{cell_w - 4:.1f}" height="{row_h - 5}" rx="3" fill="#ea580c"/>'
                        f'<text x="{cx:.1f}" y="{y + 17}" text-anchor="middle" font-family="{_esc(fonts["ui"])}" '
                        f'font-size="9.5" font-weight="800" fill="#ffffff">{z:+.2f}</text>'
                    )
                else:
                    elements.append(
                        f'<text x="{cx:.1f}" y="{y + 17}" text-anchor="middle" font-family="{_esc(fonts["ui"])}" '
                        f'font-size="9" fill="#94a3b8">{z:+.2f}</text>'
                    )

            elif canon == "swiss":
                # Jacques Bertin Permutable Retinal Matrix: exposed black grid + proportional retinal symbols
                elements.append(
                    f'<rect x="{x:.1f}" y="{y}" width="{cell_w:.1f}" height="{row_h}" fill="#ffffff" stroke="#0a0a0a" stroke-width="1.0"/>'
                )
                sym_r = min(6.5, max(2.0, abs(z) * 2.1))
                sym_x = x + 10
                if z >= 0:
                    s_fill = "#1d3557" if is_sig_pos else "#a8b2bd"
                    elements.append(
                        f'<rect x="{sym_x - sym_r:.1f}" y="{cy - sym_r + 1:.1f}" width="{sym_r*2:.1f}" height="{sym_r*2:.1f}" '
                        f'fill="{s_fill}" stroke="#0a0a0a" stroke-width="0.8"/>'
                    )
                else:
                    s_fill = "#e63946" if is_sig_neg else "#e5c3c6"
                    elements.append(
                        f'<circle cx="{sym_x:.1f}" cy="{cy + 1:.1f}" r="{sym_r:.1f}" fill="{s_fill}" stroke="#0a0a0a" stroke-width="0.8"/>'
                    )
                elements.append(
                    f'<text x="{x + cell_w - 5:.1f}" y="{y + 17}" text-anchor="end" font-family="{_esc(fonts["mono"])}" '
                    f'font-size="8.8" font-weight="{"700" if is_sig else "400"}" fill="#0a0a0a">{z:+.2f}</text>'
                )

            else:
                # Economist / FT Editorial Heatmap
                if is_sig_pos:
                    bg, fg, fw = "#cde3ee", "#004166", "700"
                elif is_sig_neg:
                    bg, fg, fw = "#f9d2d0", "#b10e08", "700"
                else:
                    bg, fg, fw = "#f4ece1", "#59544f", "400"
                elements.append(
                    f'<rect x="{x + 1:.1f}" y="{y + 1}" width="{cell_w - 2:.1f}" height="{row_h - 3}" fill="{bg}" stroke="#dfd8ce" stroke-width="0.6"/>'
                    f'<text x="{cx:.1f}" y="{y + 17}" text-anchor="middle" font-family="{_esc(fonts["ui"])}" '
                    f'font-size="9.2" font-weight="{fw}" fill="{fg}">{z:+.2f}</text>'
                )

    if canon == "tufte":
        elements.append(
            f'<line x1="0" y1="{top_pad + n_rows * row_h}" x2="{actual_w - 10}" y2="{top_pad + n_rows * row_h}" stroke="#111111" stroke-width="1.6"/>'
        )

    note_y = height - 8
    elements.append(
        f'<text x="0" y="{note_y}" font-family="{_esc(fonts["ui"])}" font-size="8.5" fill="{pal["muted"]}">'
        f"Note: |zᵢⱼ| ≥ 1.96 indicates statistically significant cell deviation at p &lt; 0.05 ({_esc(spec.get('short_name', canon))}).</text></svg>"
    )
    return "\n".join(elements)


def priority_matrix_svg(items, title="", subtitle="", width=600, height=340, school="tufte"):
    """Generate a school-authentic 2x2 Priority Action Matrix (Derived Importance × Mean Performance)."""
    if not items:
        return ""
    spec = _school_spec(school)
    pal = spec["palette"]
    fonts = spec["fonts"]
    canon = _norm_school(school)

    imps = [float(it.get("importance", 0) or 0) for it in items]
    perfs = [float(it.get("performance", it.get("mean_performance", 0)) or 0) for it in items]
    if not imps or not perfs:
        return ""

    min_imp, max_imp = min(imps), max(imps)
    min_perf, max_perf = min(perfs), max(perfs)
    mean_imp = sum(imps) / len(imps)
    mean_perf = sum(perfs) / len(perfs)

    imp_rng = (max_imp - min_imp) if max_imp != min_imp else 0.5
    perf_rng = (max_perf - min_perf) if max_perf != min_perf else 1.0

    pad_left = 60
    pad_right = 34
    header_els, top_pad = _render_svg_title_block(title, subtitle, width, fonts, pal, canon=canon)
    pad_bottom = 42
    plot_w = width - pad_left - pad_right
    plot_h = height - top_pad - pad_bottom

    def tx(p):
        return pad_left + ((p - (min_perf - 0.15 * perf_rng)) / (1.3 * perf_rng)) * plot_w

    def ty(im):
        return top_pad + plot_h - ((im - (min_imp - 0.15 * imp_rng)) / (1.3 * imp_rng)) * plot_h

    mx_line = tx(mean_perf)
    my_line = ty(mean_imp)

    elements = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" height="{height}" data-school="{_esc(canon)}" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{_esc(_clean_label(title))}">'
    ] + header_els

    # School-specific quadrant framing
    if canon == "knaflic":
        # Highlight Critical Fix quadrant in soft preattentive orange/blue
        elements.append(
            f'<rect x="{pad_left}" y="{top_pad}" width="{max(0, mx_line - pad_left):.1f}" height="{max(0, my_line - top_pad):.1f}" '
            f'fill="#fff7ed" stroke="#fdba74" stroke-width="1"/>'
        )
    elif canon == "few":
        elements.append(
            f'<rect x="{pad_left}" y="{top_pad}" width="{max(0, mx_line - pad_left):.1f}" height="{max(0, my_line - top_pad):.1f}" '
            f'fill="#fef2f2"/>'
        )

    frame_stroke = "#0a0a0a" if canon == "swiss" else "#94a3b8"
    frame_w = "1.8" if canon == "swiss" else "0.9"
    elements.append(
        f'<rect x="{pad_left}" y="{top_pad}" width="{plot_w}" height="{plot_h}" '
        f'fill="none" stroke="{frame_stroke}" stroke-width="{frame_w}"/>'
        f'<line x1="{mx_line:.1f}" y1="{top_pad}" x2="{mx_line:.1f}" y2="{top_pad + plot_h}" '
        f'stroke="{frame_stroke}" stroke-width="1.0" stroke-dasharray="4,4"/>'
        f'<line x1="{pad_left}" y1="{my_line:.1f}" x2="{pad_left + plot_w}" y2="{my_line:.1f}" '
        f'stroke="{frame_stroke}" stroke-width="1.0" stroke-dasharray="4,4"/>'
    )

    elements.append(
        f'<text x="{pad_left + 8}" y="{top_pad + 15}" font-family="{_esc(fonts["ui"])}" '
        f'font-size="8.8" font-weight="800" fill="{pal["alert_neg"]}">CRITICAL FIX (High Imp / Low Perf)</text>'
        f'<text x="{pad_left + plot_w - 8}" y="{top_pad + 15}" text-anchor="end" '
        f'font-family="{_esc(fonts["ui"])}" font-size="8.8" font-weight="700" fill="{pal["alert_pos"]}">'
        f"PROTECT STRENGTH (High Imp / High Perf)</text>"
        f'<text x="{pad_left + 8}" y="{top_pad + plot_h - 8}" font-family="{_esc(fonts["ui"])}" '
        f'font-size="8.5" fill="#777777">LOW PRIORITY (Low Imp / Low Perf)</text>'
        f'<text x="{pad_left + plot_w - 8}" y="{top_pad + plot_h - 8}" text-anchor="end" '
        f'font-family="{_esc(fonts["ui"])}" font-size="8.5" fill="#777777">'
        f"MAINTAIN / OVERKILL (Low Imp / High Perf)</text>"
    )

    elements.append(
        f'<text x="{pad_left + plot_w / 2:.1f}" y="{height - 8}" text-anchor="middle" '
        f'font-family="{_esc(fonts["body"])}" font-size="10" fill="{pal["ink"]}">'
        f"Mean Performance Score →</text>"
        f'<text x="14" y="{top_pad + plot_h / 2:.1f}" text-anchor="middle" '
        f'transform="rotate(-90 14 {top_pad + plot_h / 2:.1f})" '
        f'font-family="{_esc(fonts["body"])}" font-size="10" fill="{pal["ink"]}">'
        f"Derived Importance (|r|) →</text>"
    )

    for it in items:
        lbl = _clean_label(it.get("label", it.get("attribute", "")), max_len=20)
        imp = float(it.get("importance", 0) or 0)
        perf = float(it.get("performance", it.get("mean_performance", 0)) or 0)
        px, py = tx(perf), ty(imp)
        is_crit = imp >= mean_imp and perf < mean_perf
        color = pal["alert_neg"] if is_crit else (pal["alert_pos"] if imp >= mean_imp else "#94a3b8")
        if canon == "swiss" and is_crit:
            elements.append(
                f'<rect x="{px - 4.5:.1f}" y="{py - 4.5:.1f}" width="9" height="9" fill="{color}" stroke="#0a0a0a" stroke-width="1"/>'
            )
        else:
            elements.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.8" fill="{color}"/>')
        elements.append(
            f'<text x="{px + 7:.1f}" y="{py + 3.5:.1f}" '
            f'font-family="{_esc(fonts["ui"])}" font-size="9.2" '
            f'font-weight="{"700" if is_crit else "400"}" fill="{pal["ink"] if is_crit or canon != "knaflic" else "#64748b"}">{_esc(lbl)}</text>'
        )

    elements.append("</svg>")
    return "\n".join(elements)


def small_multiples(grid_data, title="", subtitle="", cell_w=145, cell_h=92, school="tufte"):
    """Generate school-authentic small multiples from real (label, values) pairs:
      - tufte:     Word-sized serif sparklines with min/max/last endpoint dots
      - few:       Framed Perceptual Sparkbar Histogram mini-panels
      - knaflic:   SWD Preattentive Bar mini-cards (grey context bars + bold blue modal peak bar)
      - swiss:     Exposed Modular Grid cells ([01], [02]) with geometric step-columns
      - editorial: Economist/FT Newsprint cards with crimson top rule & shaded area sparkline
    """
    valid_grid = [(_clean_label(lbl, max_len=19), [float(v) for v in vals if v is not None]) for lbl, vals in grid_data if vals and len(vals) >= 2]
    if not valid_grid:
        return ""
    spec = _school_spec(school)
    pal = spec["palette"]
    fonts = spec["fonts"]
    canon = _norm_school(school)

    cols = min(4, len(valid_grid))
    rows = math.ceil(len(valid_grid) / cols)
    total_w = max(580, cols * cell_w)
    cell_w = int(total_w / cols)
    header_els, top_pad = _render_svg_title_block(title, subtitle, total_w, fonts, pal, canon=canon)
    total_h = top_pad + rows * cell_h + 14

    cells = []
    for idx, (label, vals) in enumerate(valid_grid):
        col = idx % cols
        row = idx // cols
        cx = col * cell_w
        cy = top_pad + row * cell_h
        mn, mx = min(vals), max(vals)
        rng = (mx - mn) if mx != mn else 1.0
        inner_w = cell_w - 18
        inner_h = cell_h - 38

        if canon == "tufte":
            sp = sparkline(vals, width=inner_w, height=inner_h, school="tufte")
            cells.append(
                f'<g transform="translate({cx},{cy})">'
                f'<text x="{inner_w/2:.1f}" y="12" text-anchor="middle" '
                f'font-family="{_esc(fonts["heading"])}" font-size="9.8" font-weight="bold" fill="{pal["ink"]}">'
                f"{_esc(label)}</text>"
                f'<g transform="translate(4, 16)">{sp}</g>'
                f'<text x="{inner_w/2:.1f}" y="{cell_h - 6}" text-anchor="middle" '
                f'font-family="{_esc(fonts["ui"])}" font-size="8.2" fill="{pal["muted"]}">'
                f"range: {mn:.0f} – {mx:.0f}</text></g>"
            )
        elif canon in ("few", "knaflic", "swiss"):
            # Mini-bar / histogram representation
            frame_fill = "#ffffff"
            frame_stroke = "#0a0a0a" if canon == "swiss" else ("#cbd5e1" if canon == "few" else "#e2e8f0")
            frame_sw = "1.4" if canon == "swiss" else "0.8"
            max_i = int(max(range(len(vals)), key=lambda k: vals[k]))
            bars_svg = []
            nb = len(vals)
            bw = max(4.0, (inner_w - 8) / max(1, nb) - 3)
            for bi, bv in enumerate(vals):
                bh = max(2.0, ((bv - min(0.0, mn)) / (mx - min(0.0, mn) if mx != min(0.0, mn) else 1.0)) * (inner_h - 8))
                bx = 8 + bi * (bw + 3)
                by = 18 + inner_h - bh
                if canon == "knaflic":
                    bfill = "#1e40af" if bi == max_i else "#cbd5e1"
                elif canon == "few":
                    bfill = "#0f766e" if bi == max_i else "#64748b"
                else:
                    bfill = "#e63946" if bi == max_i else "#0a0a0a"
                bars_svg.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{bfill}"/>')

            hdr_prefix = f"[{idx+1:02d}] " if canon == "swiss" else ""
            cells.append(
                f'<g transform="translate({cx + 3},{cy + 2})">'
                f'<rect x="0" y="0" width="{cell_w - 8}" height="{cell_h - 6}" fill="{frame_fill}" stroke="{frame_stroke}" stroke-width="{frame_sw}"/>'
                f'<text x="6" y="13" font-family="{_esc(fonts["heading"])}" font-size="9" font-weight="700" fill="{pal["ink"]}">'
                f"{_esc(hdr_prefix + label)}</text>"
                f'{"".join(bars_svg)}'
                f'<text x="6" y="{cell_h - 11}" font-family="{_esc(fonts["mono"] if canon == "swiss" else fonts["ui"])}" font-size="8" fill="{pal["muted"]}">'
                f"peak: {mx:.0f} (min {mn:.0f})</text></g>"
            )
        else:
            # Editorial shaded area card
            sp = sparkline(vals, width=inner_w, height=inner_h, school="editorial")
            cells.append(
                f'<g transform="translate({cx + 3},{cy + 2})">'
                f'<rect x="0" y="0" width="{cell_w - 8}" height="{cell_h - 6}" fill="#f4ece1" stroke="#dfd8ce" stroke-width="0.7"/>'
                f'<line x1="0" y1="0" x2="{cell_w - 8}" y2="0" stroke="#e3120b" stroke-width="2.2"/>'
                f'<text x="6" y="14" font-family="{_esc(fonts["heading"])}" font-size="9.2" font-weight="700" fill="#1a1817">'
                f"{_esc(label)}</text>"
                f'<g transform="translate(4, 18)">{sp}</g>'
                f'<text x="6" y="{cell_h - 10}" font-family="{_esc(fonts["ui"])}" font-size="8" fill="#59544f">'
                f"range: {mn:.0f}–{mx:.0f}</text></g>"
            )

    return (
        f'<svg viewBox="0 0 {total_w} {total_h}" width="100%" height="{total_h}" data-school="{_esc(canon)}" '
        f'xmlns="http://www.w3.org/2000/svg">{"".join(header_els)}{"".join(cells)}</svg>'
    )


def mermaid_to_svg(mermaid_code, width=600, school="tufte"):
    """Compile Mermaid xychart-beta or pie blocks directly into school-authentic inline SVGs."""
    code = mermaid_code.strip()
    title_match = re.search(r'title\s+"([^"]+)"', code)
    title = title_match.group(1) if title_match else ""

    if code.startswith("xychart-beta"):
        x_match = re.search(r"x-axis\s+\[(.*?)\]", code, re.DOTALL)
        bar_match = re.search(r"(?:bar|line)\s+\[(.*?)\]", code, re.DOTALL)
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
                return dot_plot(raw_labels, raw_vals, title=title, subtitle=subtitle, unit=unit, width=width, school=school)

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
                school=school,
            )

    return ""


def _emit_charts_for_single_school(input_dir, target_dir, school_id):
    """Emit the full suite of standalone SVG charts for a single school into target_dir."""
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    spec = _school_spec(school_id)
    charts = []

    # 1. Segment comparison plots from setup_segments.csv
    for seg_file in (input_dir / "setup" / "setup_segments.csv", input_dir / "setup_segments.csv"):
        if seg_file.exists():
            with open(seg_file, encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
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
                        clean_col_title = _clean_label(col.replace("_", " "))
                        svg = dot_plot(
                            labels,
                            values,
                            errors=errors,
                            title=f"{clean_col_title} by Segment",
                            subtitle=f"{spec.get('short_name', 'Tufte')} comparison with 95% confidence intervals",
                            school=school_id,
                        )
                        if svg:
                            safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", col)
                            path = target_dir / f"dotplot_{safe_name}.svg"
                            path.write_text(svg, encoding="utf-8")
                            charts.append(str(path.name))
            break

    # 2. Profile numeric metrics plot & small multiples from 00_profile.json
    for prof_file in (input_dir / "setup" / "00_profile.json", input_dir / "00_profile.json"):
        if prof_file.exists():
            try:
                profile = json.loads(prof_file.read_text(encoding="utf-8"))
                variables = profile.get("variables", {})
                likert_labels, likert_means, likert_moes, grid_items = [], [], [], []
                for vname, vinfo in variables.items():
                    if isinstance(vinfo, dict) and vinfo.get("mean") is not None:
                        m = float(vinfo["mean"])
                        if 0 <= m <= 10:
                            likert_labels.append(vinfo.get("original_name", vname))
                            likert_means.append(m)
                            likert_moes.append(float(vinfo.get("moe_95", 0.0) or 0.0))
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
                        subtitle=f"Total Sample N = {profile.get('sample_size', profile.get('n_rows', '?'))} · {spec.get('short_name', 'Tufte')} Standard",
                        school=school_id,
                    )
                    path = target_dir / "dotplot_profile_means.svg"
                    path.write_text(svg, encoding="utf-8")
                    charts.append(str(path.name))

                if len(grid_items) >= 2:
                    svg = small_multiples(
                        grid_items[:8],
                        title="Response Distribution Shapes Across Variables",
                        subtitle=f"Empirical frequency distributions ({spec.get('short_name', 'Tufte')} Small Multiples)",
                        school=school_id,
                    )
                    if svg:
                        path = target_dir / "small_multiples_distributions.svg"
                        path.write_text(svg, encoding="utf-8")
                        charts.append(str(path.name))
            except Exception:
                pass
            break

    # 3. Crosstab residual heatmaps from cross/*_stats.json
    for cdir in (input_dir / "cross", input_dir):
        if cdir.exists():
            for stats_file in sorted(cdir.glob("cross_*_stats.json"))[:4]:
                try:
                    st = json.loads(stats_file.read_text(encoding="utf-8"))
                    res_table = st.get("standardized_residuals")
                    if isinstance(res_table, dict) and res_table.get("rows") and res_table.get("cols"):
                        idx_name = _clean_label(st.get("index", ""), max_len=28)
                        col_name = _clean_label(st.get("columns", ""), max_len=28)
                        svg = residual_heatmap_svg(
                            res_table["rows"],
                            res_table["cols"],
                            res_table["z_matrix"],
                            title=f"Standardized Residuals (zᵢⱼ): {idx_name} × {col_name}",
                            subtitle=f"Chi-Square p = {st.get('p_value', 1.0):.4f} · Cramér's V = {st.get('cramers_v', 0.0):.3f}",
                            school=school_id,
                        )
                        if svg:
                            out_name = f"residuals_{stats_file.stem.replace('_stats', '')}.svg"
                            (target_dir / out_name).write_text(svg, encoding="utf-8")
                            charts.append(out_name)
                except Exception:
                    continue
            break

    # 4. Priority Matrix SVG from advanced/advanced_metrics.json
    for adv_file in (input_dir / "advanced" / "advanced_metrics.json", input_dir / "advanced_metrics.json"):
        if adv_file.exists():
            try:
                adv = json.loads(adv_file.read_text(encoding="utf-8"))
                pmatrix = adv.get("priority_matrix", [])
                if len(pmatrix) >= 2:
                    svg = priority_matrix_svg(
                        pmatrix,
                        title="Priority Action Matrix (Derived Importance × Performance)",
                        subtitle="Priority Score = Importance × (Scaleₘₐₓ − Mean Performance)",
                        school=school_id,
                    )
                    if svg:
                        path = target_dir / "priority_matrix.svg"
                        path.write_text(svg, encoding="utf-8")
                        charts.append(str(path.name))
            except Exception:
                pass
            break

    return charts


def generate_charts(input_dir, charts_dir, school=None, all_schools=True):
    """Scan .dps/outputs and emit SVG charts styled for the active Data Design School
    (and pre-generate `charts_dir/by_school/<sid>/*.svg` for all 5 schools so live switching works).
    """
    charts_dir = Path(charts_dir)
    charts_dir.mkdir(parents=True, exist_ok=True)
    input_dir = Path(input_dir)

    if design_schools is not None:
        active_school = design_schools.resolve_active_school(explicit_school=school, search_dirs=[input_dir])
        school_order = list(design_schools.SCHOOL_ORDER)
    else:
        active_school = _norm_school(school)
        school_order = ["tufte", "few", "knaflic", "swiss", "editorial"]

    charts = _emit_charts_for_single_school(input_dir, charts_dir, active_school)
    for cname in charts:
        print(f"  ✓ [{active_school}] chart: {cname}")

    if all_schools:
        for sid in school_order:
            sub_dir = charts_dir / "by_school" / sid
            _emit_charts_for_single_school(input_dir, sub_dir, sid)

    if not charts:
        print(f"  ℹ No standalone chart files emitted (inline {active_school} SVG compiler remains active)")

    return charts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-School SVG chart generator (Tufte, Few, Knaflic, Swiss, Editorial)")
    parser.add_argument("--input", default=".dps/outputs", help="Root outputs directory")
    parser.add_argument("--charts-dir", default=".dps/outputs/export/charts", help="Output SVG directory")
    parser.add_argument(
        "--school",
        "-s",
        default="auto",
        help="Data Design School: tufte (default), few, knaflic, swiss, editorial, or auto",
    )
    args = parser.parse_args()
    generate_charts(args.input, args.charts_dir, school=args.school)
