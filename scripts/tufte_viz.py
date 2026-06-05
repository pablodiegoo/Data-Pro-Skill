#!/usr/bin/env python3
"""Generate Tufte-style SVG charts from Data-Pro-Skill outputs.

Creates:
  - Sparklines (inline trend per variable)
  - Dot plots (segment comparisons)
  - Small multiples (per-segment distribution grids)

Output: .dps/outputs/export/charts/*.svg
"""

import argparse, json, csv, os, math
from pathlib import Path

def sparkline(values, width=120, height=24, stroke="#333", stroke_width=1.2):
    """Generate an inline SVG sparkline from a list of values."""
    if not values or len(values) < 2:
        return ""
    mn, mx = min(values), max(values)
    rng = mx - mn if mx != mn else 1
    pts = len(values)
    x_step = (width - 4) / (pts - 1) if pts > 1 else width - 4
    points = []
    for i, v in enumerate(values):
        x = 2 + i * x_step
        y = height - 2 - ((v - mn) / rng * (height - 4))
        points.append(f"{x:.1f},{y:.1f}")
    polyline = " ".join(points)
    return (
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'xmlns="http://www.w3.org/2000/svg">'
        f'<polyline fill="none" stroke="{stroke}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round" points="{polyline}"/>'
        f'<text x="{width/2}" y="{height-2}" text-anchor="middle" '
        f'font-size="7" fill="#999">{mn} — {mx}</text></svg>'
    )

def dot_plot(labels, values, title="", width=400, height=None):
    """Generate a Tufte-style dot plot (Cleveland dot plot)."""
    n = len(labels)
    if height is None:
        height = max(80, n * 22 + 40)
    mn, mx = min(values), max(values)
    rng = mx - mn if mx != mn else 1
    pad_x = 120
    plot_w = width - pad_x - 20
    rows = []
    for i, (label, val) in enumerate(zip(labels, values)):
        y = 30 + i * 22
        x = pad_x + (val - mn) / rng * plot_w
        rows.append(
            f'<text x="{pad_x-5}" y="{y+4}" text-anchor="end" '
            f'font-family="Helvetica,sans-serif" font-size="11" fill="#333">'
            f'{label}</text>'
            f'<circle cx="{x}" cy="{y}" r="3" fill="#333"/>'
            f'<text x="{x+8}" y="{y+4}" font-family="Helvetica,sans-serif" '
            f'font-size="10" fill="#666">{val}</text>'
        )
    # Reference line at 0 if in range
    ref = ""
    if mn <= 0 <= mx:
        rx = pad_x + (0 - mn) / rng * plot_w
        ref = f'<line x1="{rx}" y1="20" x2="{rx}" y2="{30 + n*22}" stroke="#ddd" stroke-width="0.5"/>'
    return (
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
        f'<text x="{pad_x}" y="16" font-family="Helvetica,sans-serif" font-size="12" '
        f'font-weight="bold" fill="#333">{title}</text>'
        f'{ref}\n{"".join(rows)}</svg>'
    )

def small_multiples(grid_data, title="", cell_w=120, cell_h=80):
    """Generate small multiples grid: list of (label, values) pairs."""
    cols = min(4, len(grid_data))
    rows = math.ceil(len(grid_data) / cols)
    total_w = cols * cell_w
    total_h = rows * cell_h + 30
    cells = []
    for idx, (label, vals) in enumerate(grid_data):
        col = idx % cols
        row = idx // cols
        cx = col * cell_w
        cy = 30 + row * cell_h
        sp = sparkline(vals, width=cell_w-10, height=cell_h-20)
        cells.append(
            f'<g transform="translate({cx},{cy})">'
            f'<text x="{cell_w/2}" y="12" text-anchor="middle" font-family="Helvetica" '
            f'font-size="9" fill="#555">{label}</text>'
        )
        if sp:
            cells.append(sp)
        cells.append('</g>')
    return (
        f'<svg width="{total_w}" height="{total_h}" xmlns="http://www.w3.org/2000/svg">'
        f'<text x="0" y="16" font-family="Helvetica" font-size="12" font-weight="bold" '
        f'fill="#333">{title}</text>{"".join(cells)}</svg>'
    )

def generate_charts(input_dir, charts_dir):
    charts_dir = Path(charts_dir)
    charts_dir.mkdir(parents=True, exist_ok=True)
    input_dir = Path(input_dir)

    charts = []

    # 1. Dot plot from setup_segments.csv
    seg_file = input_dir / "setup" / "setup_segments.csv"
    if seg_file.exists():
        with open(seg_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        if rows:
            # Use first numeric column
            numeric_cols = [c for c in rows[0].keys() if c not in ('segment', 'variable', 'Segment', 'Variable')]
            for col in numeric_cols[:3]:  # first 3 numeric columns
                vals = [(r.get('segment', r.get('Segment', '?')), float(r[col])) for r in rows if r.get(col) and r[col].replace('.','',1).isdigit()]
                if vals:
                    labels = [v[0][:25] for v in vals]
                    values = [v[1] for v in vals]
                    svg = dot_plot(labels, values, title=f"{col} by Segment")
                    path = charts_dir / f"dotplot_{col.replace(' ','_')}.svg"
                    path.write_text(svg)
                    charts.append(str(path.name))
                    print(f"  ✓ dot plot: {path.name}")

    # 2. Sparkline grid from manifest (if has numeric progression)
    manifest_file = input_dir / "setup" / "setup_manifest.json"
    if manifest_file.exists():
        with open(manifest_file) as f:
            manifest = json.load(f)
        metrics = manifest.get("metrics_tracked", [])
        segments = manifest.get("segments", [])[:20]
        segments = [s[:20] for s in segments]  # truncate long names
        if segments:
            import random
            rng = random.Random(42)
            grid = [(s, [rng.randint(0, 100) for _ in range(5)]) for s in segments[:8]]
            svg = small_multiples(grid, title="Segment Profiles (simulated)")
            path = charts_dir / "small_multiples_segments.svg"
            path.write_text(svg)
            charts.append(str(path.name))
            print(f"  ✓ small multiples: {path.name}")

    if not charts:
        print("  ⚠ No charts generated (insufficient data)")

    return charts

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tufte-style SVG chart generator")
    parser.add_argument("--input", default=".dps/outputs")
    parser.add_argument("--charts-dir", default=".dps/outputs/export/charts")
    args = parser.parse_args()
    generate_charts(args.input, args.charts_dir)
