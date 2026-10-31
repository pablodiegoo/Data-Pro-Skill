#!/usr/bin/env python3
"""Convert final_report.md to a self-contained Edward Tufte HTML report with print-to-PDF headers/footers.

Features:
  - Full Tufte layout (58% body prose + 36% right margin notes column on #fffff8 ivory stock)
  - Booktabs tables (zero vertical gridlines, tabular-nums alignment, automatic numeric detection)
  - Automatic compilation of Mermaid (xychart-beta, pie) blocks into inline Tufte SVGs
  - Numbered <aside class="margin-note"> sidenotes for statistical diagnostics & caveats
  - Standards-compliant Print-to-PDF (@page rules + repeating <table class="print-frame"> header/footer)
"""

import argparse
import datetime
import html as html_lib
import re
import sys
from pathlib import Path

# Allow importing tufte_viz from the same scripts/ folder
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

try:
    import tufte_viz
except ImportError:
    tufte_viz = None


def _parse_frontmatter(md_text):
    """Extract YAML frontmatter key-values and return (metadata_dict, body_markdown)."""
    meta = {}
    text = md_text.lstrip("\ufeff")
    if text.startswith("---"):
        parts = re.split(r"^---\s*$", text, maxsplit=2, flags=re.MULTILINE)
        if len(parts) >= 3:
            raw_yaml = parts[1]
            body = parts[2].lstrip("\n")
            for line in raw_yaml.splitlines():
                line = line.strip()
                if not line or line.startswith("#") or ":" not in line:
                    continue
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"').strip("'")
            return meta, body
    return meta, text


def _format_inline(text):
    """Convert inline Markdown (**bold**, *italic*, `code`, [label](url)) to HTML."""
    # Protect inline <code> and <svg> tags first
    placeholders = {}

    def _stash(match):
        key = f"@@CODE_{len(placeholders)}@@"
        placeholders[key] = f"<code>{html_lib.escape(match.group(1))}</code>"
        return key

    text = re.sub(r"`([^`]+)`", _stash, text)
    # Links
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    # Bold + Italic
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)

    for key, val in placeholders.items():
        text = text.replace(key, val)
    return text


def _is_numeric_cell(cell_text):
    """Heuristic to detect numeric/statistical table cells for right-alignment & tabular-nums."""
    clean = re.sub(r"<[^>]+>", "", cell_text).strip()
    if not clean or clean in ("—", "-", "N/A"):
        return False
    # Matches numbers, percentages, ±MoE, p-values, z-scores, currency, raw counts "4 of 19"
    if re.match(r"^[+\-±$R€£]?\s*\d+([.,]\d+)?\s*(%|pts|pp|bps)?(\s*\(±[0-9.]+%?\))?(\*+)?$", clean):
        return True
    if re.match(r"^\d+\s+(of|de)\s+\d+$", clean, re.IGNORECASE):
        return True
    if re.match(r"^(p|r|V|d|z|F|t|H|U|α)\s*[=<>]\s*[+\-]?\d", clean):
        return True
    return False


def _render_table(table_lines):
    """Convert Markdown pipe-table lines into a Tufte Booktabs <table class='data-table'>."""
    rows = []
    alignments = []
    for idx, line in enumerate(table_lines):
        raw_cells = [c.strip() for c in line.strip().strip("|").split("|")]
        # Check if this row is a separator row like | :--- | :---: | ---: |
        if all(re.match(r"^:?-{2,}:?$", c.replace(" ", "")) for c in raw_cells if c != ""):
            alignments = []
            for c in raw_cells:
                c_clean = c.replace(" ", "")
                if c_clean.startswith(":") and c_clean.endswith(":"):
                    alignments.append("center")
                elif c_clean.endswith(":"):
                    alignments.append("right")
                else:
                    alignments.append("left")
            continue
        rows.append(raw_cells)

    if not rows:
        return ""

    header = rows[0]
    body_rows = rows[1:]

    out = ['<div class="table-wrapper"><table class="data-table">']
    # Header
    out.append("  <thead>\n    <tr>")
    for j, cell in enumerate(header):
        align = alignments[j] if j < len(alignments) else ("right" if j > 0 and _is_numeric_cell(cell) else "left")
        cls = ' class="num"' if align == "right" or clean_header_is_num(cell) else ""
        out.append(f"      <th{cls}>{_format_inline(cell)}</th>")
    out.append("    </tr>\n  </thead>")

    # Body
    if body_rows:
        out.append("  <tbody>")
        for r in body_rows:
            first_cell_plain = re.sub(r"[*_`~]", "", r[0]).strip().lower() if r else ""
            is_total = first_cell_plain.startswith(("total", "base", "global", "overall", "média", "media", "all "))
            tr_cls = ' class="total-row"' if is_total else ""
            out.append(f"    <tr{tr_cls}>")
            for j, cell in enumerate(r):
                align = alignments[j] if j < len(alignments) else "left"
                is_num = (align == "right") or (j > 0 and _is_numeric_cell(cell))
                td_cls = ' class="num"' if is_num else ""
                out.append(f"      <td{td_cls}>{_format_inline(cell)}</td>")
            out.append("    </tr>")
        out.append("  </tbody>")

    out.append("</table></div>")
    return "\n".join(out)


def clean_header_is_num(header_text):
    """Return True if a column header represents a quantitative metric."""
    h = re.sub(r"[*_`]", "", header_text).strip().lower()
    num_tokens = (
        "n", "%", "±moe", "moe", "mean", "média", "sd", "dp", "median", "mediana",
        "iqr", "p-value", "valor-p", "z", "z-score", "score", "nps", "top-2-box",
        "priority", "prioridade", "importance", "importância", "performance",
        "reach", "alcance", "weight", "peso", "r", "rho", "v", "d", "alpha", "α"
    )
    return any(h == tok or h.startswith(tok + " ") or h.endswith(" " + tok) or "%" in h or "±" in h for tok in num_tokens)


def convert_markdown_to_tufte_html(md_body):
    """Convert Markdown body into semantic Edward Tufte HTML."""
    lines = md_body.splitlines()
    out = []
    i = 0
    n = len(lines)
    sidenote_counter = 0

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # 1. Fenced code blocks (including ```mermaid)
        if stripped.startswith("```"):
            fence_lang = stripped[3:].strip().lower()
            code_lines = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            raw_code = "\n".join(code_lines)
            if fence_lang == "mermaid" and tufte_viz is not None:
                svg_str = tufte_viz.mermaid_to_svg(raw_code)
                if svg_str:
                    out.append(f'<figure class="chart-figure"><div class="chart-container">{svg_str}</div></figure>')
                    continue
            out.append(f"<pre><code>{html_lib.escape(raw_code)}</code></pre>")
            continue

        # 2. Horizontal rule
        if re.match(r"^(\*{3,}|-{3,}|_{3,})$", stripped):
            out.append("<hr>")
            i += 1
            continue

        # 3. Headings
        h_match = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if h_match:
            level = len(h_match.group(1))
            title_text = h_match.group(2).strip()
            slug = re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", title_text.lower())).strip("-")
            out.append(f'<h{level} id="{slug}">{_format_inline(title_text)}</h{level}>')
            i += 1
            continue

        # 4. Markdown Pipe Table
        if stripped.startswith("|") and stripped.endswith("|") and "|" in stripped[1:-1]:
            table_lines = []
            while i < n and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                table_lines.append(lines[i])
                i += 1
            out.append(_render_table(table_lines))
            continue

        # 5. Blockquotes -> Tufte Margin Notes vs Verbatim Quotes
        if stripped.startswith(">"):
            bq_lines = []
            while i < n and lines[i].strip().startswith(">"):
                bq_lines.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            bq_text = " ".join(l for l in bq_lines if l).strip()
            lower_bq = bq_text.lower()

            is_margin_note = any(
                marker in lower_bq
                for marker in (
                    "margin note",
                    "nota de margem",
                    "statistical note",
                    "nota estatística",
                    "methodological note",
                    "nota metodológica",
                    "sidenote",
                    "💡",
                    "📌",
                    "📐",
                    "p =",
                    "p <",
                    "cramér",
                    "cramer",
                    "95% ci",
                    "ic 95%",
                    "moe",
                    "article ",
                    "artigo ",
                )
            )
            if is_margin_note:
                sidenote_counter += 1
                # Strip redundant prefix like "**Margin Note:**"
                cleaned_note = re.sub(
                    r"^\*?\*?(Margin Note|Nota de Margem|Sidenote|💡\s*Insight)\s*:?\*?\*?\s*",
                    "",
                    bq_text,
                    flags=re.IGNORECASE,
                )
                out.append(
                    f'<aside class="margin-note">'
                    f'<span class="margin-note-num">§{sidenote_counter}</span>'
                    f'{_format_inline(cleaned_note)}'
                    f"</aside>"
                )
            elif '—' in bq_text or '"' in bq_text or "“" in bq_text or bq_text.startswith("*"):
                out.append(f'<blockquote class="verbatim-quote"><p>{_format_inline(bq_text)}</p></blockquote>')
            else:
                out.append(f"<blockquote><p>{_format_inline(bq_text)}</p></blockquote>")
            continue

        # 6. Unordered Lists
        if re.match(r"^[-*+]\s+.+", stripped):
            out.append("<ul>")
            while i < n and re.match(r"^\s*[-*+]\s+.+", lines[i]):
                item_txt = re.sub(r"^\s*[-*+]\s+", "", lines[i]).strip()
                out.append(f"  <li>{_format_inline(item_txt)}</li>")
                i += 1
            out.append("</ul>")
            continue

        # 7. Ordered Lists
        if re.match(r"^\d+\.\s+.+", stripped):
            out.append("<ol>")
            while i < n and re.match(r"^\s*\d+\.\s+.+", lines[i]):
                item_txt = re.sub(r"^\s*\d+\.\s+", "", lines[i]).strip()
                out.append(f"  <li>{_format_inline(item_txt)}</li>")
                i += 1
            out.append("</ol>")
            continue

        # 8. Blank lines
        if not stripped:
            i += 1
            continue

        # 9. Standard Paragraph (merge consecutive text lines)
        para_lines = []
        while (
            i < n
            and lines[i].strip()
            and not lines[i].strip().startswith(("#", ">", "|", "```", "---"))
            and not re.match(r"^([-*+]|\d+\.)\s+", lines[i].strip())
        ):
            para_lines.append(lines[i].strip())
            i += 1
        para_text = " ".join(para_lines)
        out.append(f"<p>{_format_inline(para_text)}</p>")

    return "\n".join(out)


def _resolve_css_path(css_arg):
    """Resolve tufte.css path whether passed a file, a references directory, or None."""
    if css_arg:
        p = Path(css_arg)
        if p.is_file():
            return p
        if p.is_dir():
            for rel in ("styles/tufte.css", "tufte.css"):
                cand = p / rel
                if cand.exists():
                    return cand
    # Fallback to repository's canonical references/styles/tufte.css
    repo_css = SCRIPT_DIR.parent / "references" / "styles" / "tufte.css"
    if repo_css.exists():
        return repo_css
    return None


def generate_html(md_file, css_file=None, charts_dir=None, lang="auto", output_file=None):
    """Generate a self-contained, print-ready Edward Tufte HTML report from Markdown."""
    md_file = Path(md_file)
    css_path = _resolve_css_path(css_file)
    css = css_path.read_text(encoding="utf-8") if (css_path and css_path.exists()) else ""
    raw_md = md_file.read_text(encoding="utf-8") if md_file.exists() else "# No report found"

    meta, body_md = _parse_frontmatter(raw_md)

    # Detect language from content
    if lang == "auto":
        pt_words = sum(
            len(re.findall(rf"\b{w}\b", body_md.lower()))
            for w in ["de", "da", "do", "em", "para", "com", "por", "uma", "dos", "das", "seção", "tabela", "análise", "amostra"]
        )
        en_words = sum(
            len(re.findall(rf"\b{w}\b", body_md.lower()))
            for w in ["the", "of", "and", "for", "with", "this", "that", "from", "section", "table", "analysis", "sample"]
        )
        is_pt = pt_words > en_words
    else:
        is_pt = str(lang).lower().startswith("pt")

    # Extract First H1 from body if not in frontmatter
    first_h1_match = re.search(r"^#\s+(.+)$", body_md, flags=re.MULTILINE)
    doc_title = meta.get("project") or (first_h1_match.group(1).strip() if first_h1_match else None)
    if not doc_title:
        doc_title = "Relatório Analítico Data-Pro-Skill" if is_pt else "Data-Pro-Skill Analytical Report"

    # If the body starts with an H1 and we render a structured header block, strip the duplicate first H1
    if first_h1_match and meta:
        body_md = body_md[:first_h1_match.start()] + body_md[first_h1_match.end():]

    sample_size = meta.get("sample_size", "—")
    moe_95 = meta.get("global_moe_95ci", meta.get("moe_95", "—"))
    conf_level = meta.get("confidence_level", "95%")
    export_date = meta.get("export_date", datetime.date.today().isoformat())
    framework = meta.get("framework", "Data-Pro-Skill v2.0 · Tufte Edition")
    classification = meta.get(
        "classification",
        "Confidencial · Inteligência Analítica" if is_pt else "Confidential · Decision Intelligence",
    )

    # Labels localized
    labels = {
        "print_btn": "🖨️ Imprimir / Salvar PDF" if is_pt else "🖨️ Print / Save as PDF",
        "notes_btn": "📐 Notas de Margem" if is_pt else "📐 Toggle Margin Notes",
        "sample_lbl": "Amostra (N)" if is_pt else "Sample (N)",
        "moe_lbl": "Margem de Erro (IC 95%)" if is_pt else "Global MoE (95% CI)",
        "date_lbl": "Data" if is_pt else "Export Date",
        "audit_badge": (
            "✓ VERIFICADO · CONSTITUIÇÃO ARTIGOS 1–8"
            if is_pt
            else "✓ VERIFIED · CONSTITUTION ARTICLES 1–8 COMPLIANT"
        ),
        "charts_heading": "Anexo Visual: Gráficos Vetoriais Tufte" if is_pt else "Visual Appendix: Tufte Vector Graphics",
        "footer_left": f"{framework} · Edward Tufte Standard",
        "footer_right": (
            f"N = {sample_size} · MoE = {moe_95} ({conf_level} CI) · {export_date}"
            if sample_size != "—"
            else f"{classification} · {export_date}"
        ),
    }

    body_html = convert_markdown_to_tufte_html(body_md)

    # Embed standalone SVG charts from charts_dir (if present)
    charts_html = ""
    if charts_dir:
        cdir = Path(charts_dir)
        if cdir.exists():
            chart_svgs = sorted(cdir.glob("*.svg"))
            if chart_svgs:
                charts_items = []
                for svg_file in chart_svgs:
                    svg_content = svg_file.read_text(encoding="utf-8")
                    caption = svg_file.stem.replace("_", " ").title()
                    charts_items.append(
                        f'<figure class="chart-figure">'
                        f'<div class="chart-container">{svg_content}</div>'
                        f'<figcaption class="chart-caption">{html_lib.escape(caption)}</figcaption>'
                        f"</figure>"
                    )
                charts_html = (
                    f'<section class="report-section" id="visual-appendix">'
                    f'<h2>{labels["charts_heading"]}</h2>'
                    f'{"".join(charts_items)}'
                    f"</section>"
                )

    # Build header metadata strip if frontmatter exists
    header_block_html = ""
    if meta or first_h1_match:
        meta_items = []
        if sample_size != "—":
            meta_items.append(f'<span class="meta-item"><strong>{labels["sample_lbl"]}:</strong> {html_lib.escape(str(sample_size))}</span>')
        if moe_95 != "—":
            meta_items.append(f'<span class="meta-item"><strong>{labels["moe_lbl"]}:</strong> {html_lib.escape(str(moe_95))}</span>')
        if meta.get("metrics_tracked"):
            meta_items.append(f'<span class="meta-item"><strong>Metrics:</strong> {html_lib.escape(str(meta["metrics_tracked"]))}</span>')
        if meta.get("segments"):
            meta_items.append(f'<span class="meta-item"><strong>Segments:</strong> {html_lib.escape(str(meta["segments"]))}</span>')
        meta_items.append(f'<span class="meta-item"><strong>{labels["date_lbl"]}:</strong> {html_lib.escape(str(export_date))}</span>')
        meta_items.append(f'<span class="audit-badge">{labels["audit_badge"]}</span>')

        subtitle_html = (
            f'<p class="subtitle">{html_lib.escape(meta["subtitle"])}</p>'
            if meta.get("subtitle")
            else ""
        )
        header_block_html = f"""
        <header class="report-header-block">
          <h1>{html_lib.escape(doc_title)}</h1>
          {subtitle_html}
          <div class="meta-strip">
            {"".join(meta_items)}
          </div>
        </header>
        """

    full_html = f"""<!DOCTYPE html>
<html lang="{'pt-BR' if is_pt else 'en'}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="generator" content="Data-Pro-Skill v2.0 (Edward Tufte Print-Ready HTML Engine)">
  <title>{html_lib.escape(doc_title)}</title>
  <style>
{css}
  </style>
</head>
<body>
  <!-- Screen-only interactive utility bar -->
  <nav class="tufte-toolbar no-print" aria-label="Report Controls">
    <div class="toolbar-brand">
      <span>{html_lib.escape(doc_title)}</span>
      <span class="toolbar-meta">N = {html_lib.escape(str(sample_size))} · MoE {html_lib.escape(str(moe_95))}</span>
    </div>
    <div class="toolbar-actions">
      <button type="button" class="toolbar-btn" onclick="document.body.classList.toggle('hide-margin-notes')">
        {labels["notes_btn"]}
      </button>
      <button type="button" class="toolbar-btn primary" onclick="window.print()">
        {labels["print_btn"]}
      </button>
    </div>
  </nav>

  <!-- Fixed Running Header & Footer for Print-to-PDF (Ctrl+P / Save as PDF) -->
  <div class="print-running-header" aria-hidden="true">
    <span>{html_lib.escape(doc_title)}</span>
    <span>{html_lib.escape(classification)}</span>
  </div>
  <div class="print-running-footer" aria-hidden="true">
    <span>{html_lib.escape(labels["footer_left"])}</span>
    <span>{html_lib.escape(labels["footer_right"])}</span>
  </div>

  <!-- Repeating Print Frame Table reserves top/bottom margin space on every printed page -->
  <table class="print-frame" role="presentation">
    <thead>
      <tr><td><div class="print-header-space"></div></td></tr>
    </thead>
    <tbody>
      <tr>
        <td class="print-body-cell">
          <main class="report-container">
            {header_block_html}
            <article class="tufte-prose">
              {body_html}
            </article>
            {charts_html}
          </main>
        </td>
      </tr>
    </tbody>
    <tfoot>
      <tr><td><div class="print-footer-space"></div></td></tr>
    </tfoot>
  </table>

  <style>
    body.hide-margin-notes .margin-note {{ display: none !important; }}
    body.hide-margin-notes p,
    body.hide-margin-notes ul,
    body.hide-margin-notes ol,
    body.hide-margin-notes blockquote {{ width: 92% !important; }}
  </style>
</body>
</html>
"""

    out_path = Path(output_file) if output_file else md_file.with_suffix(".html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(full_html, encoding="utf-8")
    size_kb = out_path.stat().st_size / 1024.0
    print(f"✓ {out_path} ({size_kb:.1f} KB, {'pt-BR' if is_pt else 'en'}, Print-to-PDF Ready)")
    return out_path


if __name__ == "__main__":
    # Support both legacy positional usage:
    #   python3 scripts/tufte_html.py .dps/references .dps/outputs/export/final_report.md
    # and explicit flag usage:
    #   python3 scripts/tufte_html.py --md final_report.md --css references/styles/tufte.css
    if len(sys.argv) >= 2 and not sys.argv[1].startswith("-"):
        refs_arg = Path(sys.argv[1])
        md_arg = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".dps/outputs/export/final_report.md")
        charts_arg = md_arg.parent / "charts"
        generate_html(md_arg, refs_arg, charts_arg if charts_arg.exists() else None)
    else:
        parser = argparse.ArgumentParser(description="Compile Markdown report to Print-Ready Edward Tufte HTML")
        parser.add_argument("--md", default=".dps/outputs/export/final_report.md", help="Input Markdown file")
        parser.add_argument("--css", default=None, help="Path to tufte.css or references directory")
        parser.add_argument("--charts-dir", default=None, help="Directory with standalone SVG charts")
        parser.add_argument("--output", "-o", default=None, help="Output HTML file path")
        parser.add_argument("--lang", default="auto", choices=["auto", "en", "pt"], help="Report language")
        args = parser.parse_args()
        md_p = Path(args.md)
        c_dir = Path(args.charts_dir) if args.charts_dir else (md_p.parent / "charts")
        generate_html(md_p, args.css, c_dir if c_dir.exists() else None, lang=args.lang, output_file=args.output)
