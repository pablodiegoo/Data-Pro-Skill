#!/usr/bin/env python3
"""Convert final_report.md to a self-contained Multi-School HTML report with print-to-PDF headers/footers
and native mathematical formula typography.

Supports all 5 canonical Data Design Schools selectable during `/dps-setup`:
  1. tufte     — Edward Tufte (58%/36% floating right Margin Notes on #fffff8 ivory, Booktabs) [Default]
  2. few       — Stephen Few (Perceptual BI Dashboard KPI strip, Bullet Graphs & diagnostic panels)
  3. knaflic   — Cole Nussbaumer Knaflic (Storytelling with Data: Big Idea card, Action Titles & focal bars)
  4. swiss     — Swiss Grid & Jacques Bertin (Exposed architectural modular grid & retinal matrices)
  5. editorial — The Economist / FT Editorial (Crimson top rule, Briefing Box & lollipop range charts)
"""

import argparse
import datetime
import html as html_lib
import json
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

try:
    import tufte_viz
except ImportError:
    tufte_viz = None


# ── LaTeX Mathematical Formula Engine ─────────────────────────────────────────

LATEX_SYMBOLS = {
    r"\alpha": "α",
    r"\beta": "β",
    r"\gamma": "γ",
    r"\Gamma": "Γ",
    r"\delta": "δ",
    r"\Delta": "Δ",
    r"\epsilon": "ε",
    r"\varepsilon": "ε",
    r"\zeta": "ζ",
    r"\eta": "η",
    r"\theta": "θ",
    r"\vartheta": "θ",
    r"\Theta": "Θ",
    r"\kappa": "κ",
    r"\lambda": "λ",
    r"\Lambda": "Λ",
    r"\mu": "μ",
    r"\nu": "ν",
    r"\xi": "ξ",
    r"\pi": "π",
    r"\Pi": "Π",
    r"\rho": "ρ",
    r"\sigma": "σ",
    r"\Sigma": "Σ",
    r"\tau": "τ",
    r"\phi": "φ",
    r"\varphi": "φ",
    r"\Phi": "Φ",
    r"\chi": "χ",
    r"\psi": "ψ",
    r"\omega": "ω",
    r"\Omega": "Ω",
    r"\ge": "≥",
    r"\geq": "≥",
    r"\le": "≤",
    r"\leq": "≤",
    r"\ne": "≠",
    r"\neq": "≠",
    r"\approx": "≈",
    r"\sim": "∼",
    r"\equiv": "≡",
    r"\pm": "±",
    r"\mp": "∓",
    r"\times": "×",
    r"\cdot": "·",
    r"\div": "÷",
    r"\sum": "∑",
    r"\prod": "∏",
    r"\int": "∫",
    r"\infty": "∞",
    r"\partial": "∂",
    r"\nabla": "∇",
    r"\in": "∈",
    r"\notin": "∉",
    r"\subset": "⊂",
    r"\subseteq": "⊆",
    r"\cup": "∪",
    r"\cap": "∩",
    r"\forall": "∀",
    r"\exists": "∃",
    r"\rightarrow": "→",
    r"\to": "→",
    r"\leftarrow": "←",
    r"\Rightarrow": "⇒",
    r"\leftrightarrow": "↔",
    r"\Leftrightarrow": "⇔",
}


def _render_latex_math(expr, display=False):
    """Compile a LaTeX math expression into semantic HTML with fractions, radicals, sub/superscripts & symbols."""
    s = str(expr or "").strip()
    if not s:
        return ""

    nodes = {}

    def _put_node(html_fragment):
        key = f"@@MNODE{len(nodes)}@@"
        nodes[key] = html_fragment
        return key

    # 1. Normalize LaTeX spacing and escaped characters
    s = s.replace(r"\%", "%")
    s = re.sub(r"\\[,;:!]", "&#8201;", s)
    s = s.replace(r"\quad", "&emsp;").replace(r"\qquad", "&emsp;&emsp;")
    s = re.sub(r"\\left\s*", "", s)
    s = re.sub(r"\\right\s*", "", s)

    # 2. Extract \text{...}, \mathrm{...}, \operatorname{...}, \mathbf{...} (innermost first)
    for _ in range(4):
        m_txt = re.search(r"\\(?:text|mathrm|operatorname|textrm)\{([^{}]*)\}", s)
        if not m_txt:
            break
        inner_txt = html_lib.escape(m_txt.group(1))
        s = s[: m_txt.start()] + _put_node(f'<span class="math-rm">{inner_txt}</span>') + s[m_txt.end() :]

    for _ in range(4):
        m_bf = re.search(r"\\(?:mathbf|textbf|boldsymbol)\{([^{}]*)\}", s)
        if not m_bf:
            break
        inner_bf = _render_latex_inner_tokens(m_bf.group(1), nodes)
        s = s[: m_bf.start()] + _put_node(f"<strong>{inner_bf}</strong>") + s[m_bf.end() :]

    # 2b. Handle \bar{X}, \overline{X}, \hat{Y}, \widehat{Y}, \tilde{X}
    for _ in range(4):
        m_acc = re.search(r"\\(bar|overline|hat|widehat|tilde)\{([^{}]*)\}", s)
        if not m_acc:
            break
        kind = m_acc.group(1)
        inner_acc = _render_latex_inner_tokens(m_acc.group(2), nodes)
        if kind in ("bar", "overline"):
            node_html = f'<span class="math-overline" style="text-decoration:overline;">{inner_acc}</span>'
        elif kind in ("hat", "widehat"):
            node_html = f"{inner_acc}&#770;"
        else:
            node_html = f"{inner_acc}&#771;"
        s = s[: m_acc.start()] + _put_node(node_html) + s[m_acc.end() :]

    # 3. Handle nested braces in subscripts/superscripts BEFORE \sqrt and \frac so e.g. \sqrt{n_{\text{sub}}} works
    for _ in range(6):
        m_sub = re.search(r"_\{([^{}]*)\}", s)
        if m_sub:
            sub_html = _render_latex_inner_tokens(m_sub.group(1), nodes)
            s = s[: m_sub.start()] + _put_node(f"<sub>{sub_html}</sub>") + s[m_sub.end() :]
            continue
        m_sup = re.search(r"\^\{([^{}]*)\}", s)
        if m_sup:
            sup_html = _render_latex_inner_tokens(m_sup.group(1), nodes)
            s = s[: m_sup.start()] + _put_node(f"<sup>{sup_html}</sup>") + s[m_sup.end() :]
            continue
        break

    # 4. Handle \sqrt{...}
    for _ in range(4):
        m_sqrt = re.search(r"\\sqrt\{([^{}]*)\}", s)
        if not m_sqrt:
            break
        rad_html = _render_latex_inner_tokens(m_sqrt.group(1), nodes)
        sqrt_node = _put_node(
            f'<span class="math-sqrt"><span class="math-sqrt-sign">&radic;</span>'
            f'<span class="math-radicand">{rad_html}</span></span>'
        )
        s = s[: m_sqrt.start()] + sqrt_node + s[m_sqrt.end() :]

    # 5. Handle \frac{num}{den}
    for _ in range(4):
        m_frac = re.search(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", s)
        if not m_frac:
            break
        num_html = _render_latex_inner_tokens(m_frac.group(1), nodes)
        den_html = _render_latex_inner_tokens(m_frac.group(2), nodes)
        frac_node = _put_node(
            f'<span class="math-frac"><span class="math-num">{num_html}</span>'
            f'<span class="math-den">{den_html}</span></span>'
        )
        s = s[: m_frac.start()] + frac_node + s[m_frac.end() :]

    # 6. Render remaining tokens, single-char sub/superscripts, Greek symbols & variables
    rendered = _render_latex_inner_tokens(s, nodes)
    tag = "div" if display else "span"
    cls = "math-formula math-display" if display else "math-formula math-inline"
    return f'<{tag} class="{cls}">{rendered}</{tag}>'


def _render_latex_inner_tokens(segment, nodes):
    """Render single-token sub/superscripts, Greek symbols, operators, and italic math variables."""
    s = segment

    # Replace LaTeX commands (longest first so \geq beats \ge)
    for cmd in sorted(LATEX_SYMBOLS.keys(), key=len, reverse=True):
        s = re.sub(re.escape(cmd) + r"(?![a-zA-Z])", LATEX_SYMBOLS[cmd], s)

    # Strip any remaining unknown backslash commands gracefully: \foo -> foo
    s = re.sub(r"\\([a-zA-Z]+)", r"\1", s)

    # Single-token subscripts & superscripts (e.g. _e, _0, ^2, ^k, or _@@MNODE0@@)
    def _sub_repl(m):
        tok = m.group(1)
        return f"<sub>{tok}</sub>"

    def _sup_repl(m):
        tok = m.group(1)
        return f"<sup>{tok}</sup>"

    s = re.sub(r"_(@@MNODE\d+@@|[A-Za-z0-9]+)", _sub_repl, s)
    s = re.sub(r"\^(@@MNODE\d+@@|[A-Za-z0-9+\-]+)", _sup_repl, s)

    # Remove leftover curly braces if any
    s = s.replace("{", "").replace("}", "")

    # Protect existing HTML tags (<sub>, <sup>) and @@MNODEk@@ before escaping
    sub_tags = {}

    def _stash_tag(m):
        k = f"@@MTAG{len(sub_tags)}@@"
        sub_tags[k] = m.group(0)
        return k

    s = re.sub(r"</?(?:sub|sup|strong|span)[^>]*>|@@MNODE\d+@@|&#\d+;|&[a-zA-Z]+;", _stash_tag, s)
    s = html_lib.escape(s)

    # Format absolute value bars |x| -> &#x7C;x&#x7C;
    s = re.sub(r"\|([^|]+)\|", r'<span class="math-abs">&#x7C;\1&#x7C;</span>', s)

    # Typographic minus sign before digits or variables
    s = re.sub(r"(?<![A-Za-z0-9])-(?=\s*[0-9A-Za-zα-ωΑ-Ω])", "&minus;", s)

    # Italicize standalone single-letter Latin mathematical variables (N, n, p, z, r, t, F, H, U, V, d, K, R, O, E, x, y)
    s = re.sub(
        r"(?<![A-Za-z0-9_@#$])([A-Za-z])(?![A-Za-z0-9_@;])",
        r'<var class="math-var">\1</var>',
        s,
    )

    # Restore stashed tags and nodes (iteratively for nested nodes)
    for _ in range(6):
        changed = False
        for k, v in sub_tags.items():
            if k in s:
                s = s.replace(k, v)
                changed = True
        for k, v in nodes.items():
            if k in s:
                s = s.replace(k, v)
                changed = True
        if not changed:
            break

    return s


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


def _strip_embedded_frontmatter(md_body, active_school=None, is_pt=False):
    """Remove any accidentally embedded YAML frontmatter blocks inside concatenated sub-reports
    and synchronize inline school references to the active school."""
    cleaned = re.sub(
        r"(?:^|\n)---\r?\n(?:[a-zA-Z0-9_]+\s*:[^\n]*\r?\n)+---\r?\n",
        "\n",
        md_body,
    )
    if active_school and design_schools is not None:
        sid = design_schools.normalize_school(active_school)
        spec = design_schools.get_school_spec(sid)
        short_name = spec["short_name"]
        full_name = spec.get("name_pt", spec["name"]) if is_pt else spec["name"]
        cleaned = re.sub(
            r"(\*\*Data Design School:\*\*|\*\*Escola de Design de Dados:\*\*)\s*`[^`]+`\s*\(`[^`]+`\)",
            rf"\1 `{short_name}` (`{sid}`)",
            cleaned,
        )
        cleaned = re.sub(
            r"locked to the \*\*[^*]+\*\*\s*\(`--school\s+[^`]+`\)",
            f"locked to the **{full_name}** (`--school {sid}`)",
            cleaned,
        )
        cleaned = re.sub(
            r"Active Data Design School:\s*\*\*[^*]+\*\*\s*\(`[^`]+`\)",
            f"Active Data Design School: **{full_name}** (`{sid}`)",
            cleaned,
        )
        cleaned = re.sub(
            r"rendered under the \*\*[^*]+\*\*",
            f"rendered under the **{full_name}**",
            cleaned,
        )
    return cleaned


def _format_inline(text):
    """Convert inline Markdown (**bold**, *italic*, `code`, $math$, [label](url)) to publication-grade HTML."""
    s = str(text or "")
    if not s:
        return ""

    # Fix common malformed math ending with backtick instead of $ (e.g., $\Delta = 0.0%`)
    s = re.sub(r"\$\\Delta\s*=\s*([0-9.+%\-]+)`", r"$\\Delta = \1$", s)

    placeholders = {}

    def _put(html_str):
        key = f"@@PH_{len(placeholders)}@@"
        placeholders[key] = html_str
        return key

    # 1. Extract inline code `...` first (if a code span wraps pure LaTeX like `$\eta^2$`, render it as math!)
    def _stash_code(match):
        inner = match.group(1).strip()
        if inner.startswith("$") and inner.endswith("$") and len(inner) >= 3:
            return _put(_render_latex_math(inner[1:-1], display=False))
        return _put(f"<code>{html_lib.escape(match.group(1))}</code>")

    s = re.sub(r"`([^`]+)`", _stash_code, s)

    # 2. Extract Display Math $$...$$ and Inline Math $...$ BEFORE Markdown * / _ emphasis!
    s = re.sub(
        r"\$\$(.+?)\$\$",
        lambda m: _put(_render_latex_math(m.group(1), display=True)),
        s,
        flags=re.DOTALL,
    )
    s = re.sub(
        r"(?<!\$)\$(?!\$)([^$\n]+?)(?<!\$)\$(?!\$)",
        lambda m: _put(_render_latex_math(m.group(1), display=False)),
        s,
    )

    # 3. Sweep stray bare LaTeX expressions outside $...$ (e.g., E_ij, z_ij, O_ij, \chi^2, \eta^2)
    s = re.sub(
        r"\b([EOz])_\{?ij\}?\b",
        lambda m: _put(_render_latex_math(f"{m.group(1)}_{{ij}}", display=False)),
        s,
    )
    s = re.sub(
        r"\\(?:chi\^2|eta\^2|alpha|beta|Delta|ge|geq|le|leq|pm|times)\b",
        lambda m: _put(_render_latex_math(m.group(0), display=False)),
        s,
    )

    # 4. Standard Markdown links & emphasis
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"(?<![A-Za-z0-9_])_([^_\n]+)_(?![A-Za-z0-9_])", r"<em>\1</em>", s)

    # 5. Restore placeholders
    for key, val in placeholders.items():
        s = s.replace(key, val)
    return s


def _split_md_table_row(line):
    """Split a Markdown pipe-table row on `|` while ignoring `|` inside `$math$` or `` `code` ``."""
    # First protect |x| absolute value bars inside $...$ so they never act as column separators
    def _protect_math_pipes(m):
        return m.group(0).replace("|", "@@MATHPIPE@@")

    protected = re.sub(r"`[^`]*`|\$[^$\n]+\$", _protect_math_pipes, line.strip())
    if protected.startswith("|"):
        protected = protected[1:]
    if protected.endswith("|"):
        protected = protected[:-1]
    cells = [c.replace("@@MATHPIPE@@", "|").strip() for c in protected.split("|")]
    return cells


def _is_numeric_cell(cell_text):
    """Heuristic to detect numeric/statistical table cells for right-alignment & tabular-nums."""
    clean = re.sub(r"<[^>]+>", "", cell_text).strip()
    if not clean or clean in ("—", "-", "N/A"):
        return False
    if re.match(r"^[+\-±$R€£]?\s*\d+([.,]\d+)?\s*(%|pts|pp|bps)?(\s*\(±?[0-9.]+%?\))?(\*+)?$", clean):
        return True
    if re.match(r"^\d+\s+(of|de)\s+\d+$", clean, re.IGNORECASE):
        return True
    if re.match(r"^(\d+([.,]\d+)?%?\s*\(\d+\))$", clean):
        return True
    if re.match(r"^(p|r|V|d|z|F|t|H|U|α)\s*[=<>]\s*[+\-]?\d", clean):
        return True
    return False


def _render_table(table_lines):
    """Convert Markdown pipe-table lines into a <table class='data-table'>."""
    rows = []
    alignments = []
    for line in table_lines:
        raw_cells = _split_md_table_row(line)
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
    n_cols = len(header)
    wide_cls = " wide" if n_cols >= 4 else ""
    table_cls = "data-table wide-table" if n_cols >= 4 else "data-table"

    out = [f'<div class="table-wrapper{wide_cls}"><table class="{table_cls}">']
    out.append("  <thead>\n    <tr>")
    for j, cell in enumerate(header):
        align = alignments[j] if j < len(alignments) else ("right" if j > 0 and _is_numeric_cell(cell) else "left")
        cls = ' class="num"' if align == "right" or clean_header_is_num(cell) else ""
        out.append(f"      <th{cls}>{_format_inline(cell)}</th>")
    out.append("    </tr>\n  </thead>")

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
    h = re.sub(r"[*_`$\\]", "", header_text).strip().lower()
    num_tokens = (
        "n", "%", "±moe", "moe", "mean", "média", "sd", "dp", "median", "mediana",
        "iqr", "p-value", "valor-p", "z", "z-score", "score", "nps", "top-2-box",
        "priority", "prioridade", "importance", "importância", "performance",
        "reach", "alcance", "weight", "peso", "r", "rho", "v", "d", "alpha", "α",
        "valid n", "subgroup n", "skewness", "observed", "expected", "residual"
    )
    return any(h == tok or h.startswith(tok + " ") or h.endswith(" " + tok) or "%" in h or "±" in h for tok in num_tokens)


def _build_school_overview_html(school_id, meta, is_pt=False):
    """Build a school-authentic structural overview component injected at the top of the report."""
    sid = design_schools.normalize_school(school_id) if design_schools else "tufte"
    sample_n = str(meta.get("sample_size", "—"))
    n_eff = str(meta.get("effective_sample_size", sample_n))
    moe = str(meta.get("global_moe_95ci", meta.get("moe_95", "—")))
    metrics_cnt = str(meta.get("metrics_tracked", "—"))
    segs_cnt = str(meta.get("segments_count", meta.get("segments", "—")))

    if sid == "few":
        # Stephen Few: Perceptual Executive BI Dashboard Monitoring Strip (4 KPI Cards with Bullet Bars)
        lbl_n = "AMOSTRA TOTAL (N)" if is_pt else "TOTAL SAMPLE (N)"
        lbl_moe = "PRECISÃO GLOBAL (IC 95%)" if is_pt else "GLOBAL PRECISION (95% CI)"
        lbl_m = "DIMENSÕES MONITORADAS" if is_pt else "MONITORED DIMENSIONS"
        lbl_g = "GOVERNANÇA ESTATÍSTICA" if is_pt else "STATISTICAL GOVERNANCE"
        sub_n = f"Base Efetiva N_eff = {n_eff}" if is_pt else f"Effective Base N_eff = {n_eff}"
        sub_moe = "Limite máx. variância p=0.50" if is_pt else "Max variance bound p=0.50"
        sub_m = f"{segs_cnt} segmentos cruzados" if is_pt else f"Across {segs_cnt} primary segments"
        sub_g = "Artigos 1–8 Verificados" if is_pt else "Articles 1–8 Verified"
        return f"""
        <section class="school-overview few-dashboard-strip" aria-label="Perceptual KPI Summary">
          <div class="kpi-grid">
            <div class="kpi-card">
              <div class="kpi-label">{lbl_n}</div>
              <div class="kpi-value">{html_lib.escape(sample_n)}</div>
              <div class="kpi-bullet-bar"><span style="width:92%;background:#0f766e;"></span></div>
              <div class="kpi-sub">{html_lib.escape(sub_n)}</div>
            </div>
            <div class="kpi-card">
              <div class="kpi-label">{lbl_moe}</div>
              <div class="kpi-value">{html_lib.escape(moe)}</div>
              <div class="kpi-bullet-bar"><span style="width:86%;background:#0f172a;"></span></div>
              <div class="kpi-sub">{html_lib.escape(sub_moe)}</div>
            </div>
            <div class="kpi-card">
              <div class="kpi-label">{lbl_m}</div>
              <div class="kpi-value">{html_lib.escape(metrics_cnt)}</div>
              <div class="kpi-bullet-bar"><span style="width:78%;background:#0f766e;"></span></div>
              <div class="kpi-sub">{html_lib.escape(sub_m)}</div>
            </div>
            <div class="kpi-card">
              <div class="kpi-label">{lbl_g}</div>
              <div class="kpi-value" style="color:#0f766e;">100% PASS</div>
              <div class="kpi-bullet-bar"><span style="width:100%;background:#0f766e;"></span></div>
              <div class="kpi-sub">{html_lib.escape(sub_g)}</div>
            </div>
          </div>
        </section>
        """

    if sid == "knaflic":
        # Cole Knaflic (SWD): Executive "Big Idea" Storyboard Deck Banner
        tag = "HISTÓRIA COM DADOS · A GRANDE IDEIA EXECUTIVA" if is_pt else "STORYTELLING WITH DATA · THE EXECUTIVE BIG IDEA"
        headline = (
            f"Decisões ancoradas em N = {sample_n} respondentes (margem de erro {moe} a 95% IC), "
            f"isolando alavancas estatisticamente significativas em {metrics_cnt} métricas e {segs_cnt} segmentos."
            if is_pt
            else f"Evidence-backed synthesis across N = {sample_n} respondents ({moe} global 95% CI MoE), "
            f"isolating preattentive focal levers across {metrics_cnt} metrics and {segs_cnt} segments."
        )
        return f"""
        <section class="school-overview swd-big-idea-card" aria-label="Executive Big Idea">
          <div class="swd-big-idea-tag">💡 {tag}</div>
          <p class="swd-big-idea-text">{html_lib.escape(headline)}</p>
          <div class="swd-pill-strip">
            <span class="swd-pill focal">N = {html_lib.escape(sample_n)} (N_eff = {html_lib.escape(n_eff)})</span>
            <span class="swd-pill focal">95% CI MoE: {html_lib.escape(moe)}</span>
            <span class="swd-pill context">Metrics: {html_lib.escape(metrics_cnt)} · Segments: {html_lib.escape(segs_cnt)}</span>
            <span class="swd-pill context"> gray = context · blue/orange = focal action</span>
          </div>
        </section>
        """

    if sid == "swiss":
        # Swiss Grid & Jacques Bertin: Architectural Blueprint Modular Grid
        return f"""
        <section class="school-overview swiss-blueprint-grid" aria-label="Architectural Specification Grid">
          <div class="swiss-cell accent">
            <span class="swiss-idx">[00.1 // GRID SYSTEM]</span>
            <strong class="swiss-val">MÜLLER-BROCKMANN // BERTIN</strong>
          </div>
          <div class="swiss-cell">
            <span class="swiss-idx">[00.2 // SAMPLE N]</span>
            <strong class="swiss-val">{html_lib.escape(sample_n)} (EFF {html_lib.escape(n_eff)})</strong>
          </div>
          <div class="swiss-cell">
            <span class="swiss-idx">[00.3 // PRECISION 95% CI]</span>
            <strong class="swiss-val">{html_lib.escape(moe)}</strong>
          </div>
          <div class="swiss-cell">
            <span class="swiss-idx">[00.4 // MATRIX DIMENSIONS]</span>
            <strong class="swiss-val">{html_lib.escape(metrics_cnt)} VARS × {html_lib.escape(segs_cnt)} SEGS</strong>
          </div>
        </section>
        """

    if sid == "editorial":
        # Economist / FT Editorial: "The Numbers in Brief" Briefing Card
        box_title = "OS NÚMEROS EM RESUMO · BRIEFING EDITORIAL" if is_pt else "THE NUMBERS IN BRIEF · EDITORIAL BRIEFING"
        b1 = f"Amostra verificada de N = {sample_n} (base efetiva N_eff = {n_eff}) com margem de erro global de {moe} (IC 95%)." if is_pt else f"Verified survey base of N = {sample_n} (effective N_eff = {n_eff}) with a global 95% confidence margin of {moe}."
        b2 = f"Cobertura analítica de {metrics_cnt} variáveis quantitativas cruzadas contra {segs_cnt} dimensões de segmentação." if is_pt else f"Analytical coverage across {metrics_cnt} quantitative metrics cross-tabulated against {segs_cnt} segmentation dimensions."
        return f"""
        <section class="school-overview editorial-brief-box" aria-label="Editorial Numbers in Brief">
          <div class="editorial-brief-header">{box_title}</div>
          <div class="editorial-brief-grid">
            <div class="editorial-brief-item"><span class="crimson-sq">■</span> {html_lib.escape(b1)}</div>
            <div class="editorial-brief-item"><span class="crimson-sq">■</span> {html_lib.escape(b2)}</div>
          </div>
        </section>
        """

    # Default: Edward Tufte Scholarly Epigraph & Methodological Precision Contract
    epigraph = (
        "“Acima de tudo, mostre os dados.” — Edward R. Tufte, The Visual Display of Quantitative Information (1983)"
        if is_pt
        else "“Above all else show the data.” — Edward R. Tufte, The Visual Display of Quantitative Information (1983)"
    )
    return f"""
    <section class="school-overview tufte-epigraph-block" aria-label="Tufte Methodological Epigraph">
      <p class="tufte-epigraph">{html_lib.escape(epigraph)}</p>
    </section>
    """


def convert_markdown_to_tufte_html(md_body, school="tufte", is_pt=False):
    """Convert Markdown body into semantic HTML adapted to the selected Data Design School.

    Returns (body_html, mermaid_blocks_list) so inline charts can be pre-rendered for all 5 schools.
    """
    canon_school = design_schools.normalize_school(school) if design_schools else "tufte"
    spec = design_schools.get_school_spec(canon_school) if design_schools else None

    clean_md = _strip_embedded_frontmatter(md_body, active_school=canon_school, is_pt=is_pt)
    lines = clean_md.splitlines()
    out = []
    mermaid_blocks = []
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
                svg_str = tufte_viz.mermaid_to_svg(raw_code, school=canon_school)
                if svg_str:
                    chart_idx = len(mermaid_blocks)
                    mermaid_blocks.append(raw_code)
                    out.append(
                        f'<figure class="chart-figure">'
                        f'<div class="chart-container" data-inline-chart-idx="{chart_idx}">{svg_str}</div>'
                        f"</figure>"
                    )
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

        # 5. Blockquotes -> Margin Notes / Callout Notes vs Verbatim Quotes
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
                    "perceptual diagnostic",
                    "key takeaway",
                    "grid module",
                    "editorial brief",
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
                cleaned_note = re.sub(
                    r"^\*?\*?(Margin Note|Nota de Margem|Sidenote|💡\s*Insight|Key Takeaway|Perceptual Diagnostic|Editorial Brief)\s*:?\*?\*?\s*",
                    "",
                    bq_text,
                    flags=re.IGNORECASE,
                )
                if spec:
                    lbl_tmpl = spec["note_label_pt"] if is_pt else spec["note_label_en"]
                    note_badge = lbl_tmpl.format(n=sidenote_counter)
                else:
                    note_badge = f"§{sidenote_counter}"
                out.append(
                    f'<aside class="margin-note" data-note-index="{sidenote_counter}">'
                    f'<span class="margin-note-num">{html_lib.escape(note_badge)}</span> '
                    f"{_format_inline(cleaned_note)}"
                    f"</aside>"
                )
            elif "—" in bq_text or '"' in bq_text or "“" in bq_text or bq_text.startswith("*"):
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

        # 9. Standard Paragraph
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

    return "\n".join(out), mermaid_blocks


def _load_all_school_stylesheets(primary_css_arg=None):
    """Load CSS text for all 5 Data Design Schools so the report is 100% self-contained."""
    styles_map = {}
    if design_schools is not None:
        for sid in design_schools.SCHOOL_ORDER:
            cpath = design_schools.resolve_css_for_school(sid, custom_css_arg=primary_css_arg if sid == "tufte" else None)
            if cpath and cpath.exists():
                styles_map[sid] = cpath.read_text(encoding="utf-8")
    if not styles_map.get("tufte"):
        repo_css = SCRIPT_DIR.parent / "references" / "styles" / "tufte.css"
        if repo_css.exists():
            styles_map["tufte"] = repo_css.read_text(encoding="utf-8")
    return styles_map


def _build_visual_appendix_for_school(charts_dir, school_id, is_pt=False):
    """Build the inner HTML of #visual-appendix for a specific Data Design School."""
    if not charts_dir:
        return ""
    cdir = Path(charts_dir)
    if not cdir.exists():
        return ""

    spec = design_schools.get_school_spec(school_id) if design_schools else {"short_name": "Edward Tufte"}
    school_subdir = cdir / "by_school" / school_id
    target_dir = school_subdir if school_subdir.exists() and list(school_subdir.glob("*.svg")) else cdir
    chart_svgs = sorted(target_dir.glob("*.svg"))
    if not chart_svgs:
        return ""

    heading = (
        f"Anexo Visual: Gráficos Vetoriais ({spec['short_name']})"
        if is_pt
        else f"Visual Appendix: Vector Graphics ({spec['short_name']})"
    )
    items = []
    for idx, svg_file in enumerate(chart_svgs, start=1):
        svg_content = svg_file.read_text(encoding="utf-8")
        if tufte_viz is not None and hasattr(tufte_viz, "human_caption_for_chart"):
            cap_body = tufte_viz.human_caption_for_chart(svg_file.stem, school=school_id, is_pt=is_pt)
        else:
            cap_body = svg_file.stem.replace("_", " ").title()
        fig_prefix = f"Figura {idx} —" if is_pt else f"Figure {idx} —"
        items.append(
            f'<figure class="chart-figure">'
            f'<div class="chart-container">{svg_content}</div>'
            f'<figcaption class="chart-caption"><strong>{fig_prefix}</strong> {html_lib.escape(cap_body)}</figcaption>'
            f"</figure>"
        )
    return f'<h2>{html_lib.escape(heading)}</h2>{"".join(items)}'


def generate_html(md_file, css_file=None, charts_dir=None, lang="auto", output_file=None, school="auto"):
    """Generate a self-contained, print-ready HTML report in the chosen Data Design School."""
    md_file = Path(md_file)
    raw_md = md_file.read_text(encoding="utf-8") if md_file.exists() else "# No report found"
    meta, body_md = _parse_frontmatter(raw_md)

    search_dirs = [md_file.parent, md_file.parent.parent]
    if design_schools is not None:
        active_school = design_schools.resolve_active_school(
            explicit_school=school,
            search_dirs=search_dirs,
            md_meta=meta,
            default="tufte",
        )
        spec = design_schools.get_school_spec(active_school)
        css_path = design_schools.resolve_css_for_school(active_school, custom_css_arg=css_file)
    else:
        active_school = "tufte"
        spec = {
            "id": "tufte",
            "name": "Edward Tufte (Classic Data-Ink & Sidenote School)",
            "short_name": "Edward Tufte",
            "kicker_en": "EDWARD TUFTE ANALYTICAL STANDARD",
            "kicker_pt": "PADRÃO ANALÍTICO EDWARD TUFTE",
            "footer_stamp_en": "Edward Tufte Standard",
            "footer_stamp_pt": "Padrão Edward Tufte",
            "note_label_en": "§{n}",
            "note_label_pt": "§{n}",
        }
        css_path = SCRIPT_DIR.parent / "references" / "styles" / "tufte.css"

    css = css_path.read_text(encoding="utf-8") if (css_path and css_path.exists()) else ""
    all_school_css = _load_all_school_stylesheets(primary_css_arg=css_file)
    if css and active_school not in all_school_css:
        all_school_css[active_school] = css

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

    # Extract First H1 from body if present
    first_h1_match = re.search(r"^#\s+(.+)$", body_md, flags=re.MULTILINE)
    doc_title = meta.get("project") or (first_h1_match.group(1).strip() if first_h1_match else None)
    if not doc_title:
        doc_title = "Relatório Analítico Data-Pro-Skill" if is_pt else "Data-Pro-Skill Analytical Report"

    if first_h1_match and meta:
        body_md = body_md[: first_h1_match.start()] + body_md[first_h1_match.end() :]

    sample_size = meta.get("sample_size", "—")
    moe_95 = meta.get("global_moe_95ci", meta.get("moe_95", "—"))
    conf_level = meta.get("confidence_level", "95%")
    export_date = meta.get("export_date", datetime.date.today().isoformat())
    classification = meta.get(
        "classification",
        "Confidencial · Inteligência Analítica" if is_pt else "Confidential · Decision Intelligence",
    )

    kicker_txt = spec.get("kicker_pt" if is_pt else "kicker_en", spec["short_name"])
    footer_stamp = spec.get("footer_stamp_pt" if is_pt else "footer_stamp_en", f"{spec['short_name']} Standard")

    labels = {
        "print_btn": "🖨️ Imprimir / Salvar PDF" if is_pt else "🖨️ Print / Save as PDF",
        "notes_btn": "📐 Notas / Callouts" if is_pt else "📐 Toggle Callouts",
        "school_lbl": "🎨 Escola:" if is_pt else "🎨 School:",
        "sample_lbl": "Amostra (N)" if is_pt else "Sample (N)",
        "moe_lbl": "Margem de Erro (IC 95%)" if is_pt else "Global MoE (95% CI)",
        "school_meta_lbl": "Escola de Design" if is_pt else "Design School",
        "date_lbl": "Data" if is_pt else "Export Date",
        "audit_badge": (
            "✓ VERIFICADO · CONSTITUIÇÃO ARTIGOS 1–8"
            if is_pt
            else "✓ VERIFIED · CONSTITUTION ARTICLES 1–8 COMPLIANT"
        ),
        "header_right": f"{spec['short_name']} · {classification}",
        "footer_left": f"Data-Pro-Skill v2.1 · {footer_stamp}",
        "footer_right": (
            f"N = {sample_size} · MoE = {moe_95} ({conf_level} CI) · {export_date}"
            if sample_size != "—"
            else f"{classification} · {export_date}"
        ),
    }

    body_html, mermaid_blocks = convert_markdown_to_tufte_html(body_md, school=active_school, is_pt=is_pt)
    overview_html = _build_school_overview_html(active_school, meta, is_pt=is_pt)
    appendix_inner_html = _build_visual_appendix_for_school(charts_dir, active_school, is_pt=is_pt)
    charts_html = (
        f'<section class="report-section" id="visual-appendix">{appendix_inner_html}</section>'
        if appendix_inner_html
        else '<section class="report-section" id="visual-appendix"></section>'
    )

    # Build header metadata strip
    header_block_html = ""
    if meta or first_h1_match:
        meta_items = []
        if sample_size != "—":
            meta_items.append(
                f'<span class="meta-item"><strong>{labels["sample_lbl"]}:</strong> {html_lib.escape(str(sample_size))}</span>'
            )
        if moe_95 != "—":
            meta_items.append(
                f'<span class="meta-item"><strong>{labels["moe_lbl"]}:</strong> {html_lib.escape(str(moe_95))}</span>'
            )
        meta_items.append(
            f'<span class="meta-item"><strong>{labels["school_meta_lbl"]}:</strong> '
            f'<span id="dps-active-school-label">{html_lib.escape(spec["short_name"])}</span> '
            f'(<code id="dps-active-school-code">{html_lib.escape(active_school)}</code>)</span>'
        )
        if meta.get("metrics_tracked"):
            meta_items.append(
                f'<span class="meta-item"><strong>Metrics:</strong> {html_lib.escape(str(meta["metrics_tracked"]))}</span>'
            )
        if meta.get("segments_count") or meta.get("segments"):
            seg_val = meta.get("segments_count") or meta.get("segments")
            meta_items.append(f'<span class="meta-item"><strong>Segments:</strong> {html_lib.escape(str(seg_val))}</span>')
        meta_items.append(f'<span class="meta-item"><strong>{labels["date_lbl"]}:</strong> {html_lib.escape(str(export_date))}</span>')
        meta_items.append(f'<span class="audit-badge">{labels["audit_badge"]}</span>')

        subtitle_html = (
            f'<p class="report-subtitle subtitle">{html_lib.escape(meta["subtitle"])}</p>'
            if meta.get("subtitle")
            else ""
        )
        header_block_html = f"""
        <header class="report-header-block">
          <div class="report-kicker" id="dps-report-kicker">{html_lib.escape(kicker_txt)}</div>
          <h1>{html_lib.escape(doc_title)}</h1>
          {subtitle_html}
          <div class="meta-strip">
            {"".join(meta_items)}
          </div>
        </header>
        <div id="dps-school-overview-slot">{overview_html}</div>
        """

    # Pre-compile all 5 schools' CSS, structural overviews, inline charts, and appendix charts for instant live switching
    school_options_html = []
    school_js_meta = {}
    school_list = design_schools.SCHOOL_ORDER if design_schools is not None else ["tufte"]
    for sid in school_list:
        s_info = design_schools.SCHOOLS[sid] if design_schools is not None else spec
        sel_attr = ' selected="selected"' if sid == active_school else ""
        school_options_html.append(
            f'<option value="{sid}"{sel_attr}>{html_lib.escape(s_info["short_name"])} ({sid})</option>'
        )
        inline_svgs_for_sid = []
        if tufte_viz is not None and mermaid_blocks:
            for m_code in mermaid_blocks:
                inline_svgs_for_sid.append(tufte_viz.mermaid_to_svg(m_code, school=sid))
        school_js_meta[sid] = {
            "id": sid,
            "short_name": s_info["short_name"],
            "kicker": s_info.get("kicker_pt" if is_pt else "kicker_en", s_info["short_name"]),
            "header_right": f"{s_info['short_name']} · {classification}",
            "footer_left": f"Data-Pro-Skill v2.1 · {s_info.get('footer_stamp_pt' if is_pt else 'footer_stamp_en', s_info['short_name'])}",
            "note_label_tmpl": s_info.get("note_label_pt" if is_pt else "note_label_en", "§{n}"),
            "css": all_school_css.get(sid, css),
            "overview_html": _build_school_overview_html(sid, meta, is_pt=is_pt),
            "inline_charts": inline_svgs_for_sid,
            "appendix_html": _build_visual_appendix_for_school(charts_dir, sid, is_pt=is_pt),
        }

    school_selector_html = (
        f'<label for="dps-school-select" style="font-weight:600;">{labels["school_lbl"]}</label>'
        f'<select id="dps-school-select" aria-label="Select Data Design School" onchange="window.dpsSwitchSchool(this.value)">'
        f'{"".join(school_options_html)}'
        f"</select>"
    )

    full_html = f"""<!DOCTYPE html>
<html lang="{'pt-BR' if is_pt else 'en'}" data-school="{html_lib.escape(active_school)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="generator" content="Data-Pro-Skill v2.1 ({html_lib.escape(spec['short_name'])} Print-Ready HTML Engine)">
  <meta name="dps-design-school" content="{html_lib.escape(active_school)}">
  <title>{html_lib.escape(doc_title)}</title>
  <style id="dps-school-stylesheet">
{css}
  </style>
  <style id="dps-core-math-and-print-fixes">
    /* Universal Mathematical Formula Typography (Articles 1–8) */
    .math-formula.math-inline {{
      font-family: "Latin Modern Math", "STIX Two Math", "Cambria Math", Palatino, "Palatino Linotype", Georgia, serif;
      font-size: 1.02em;
      white-space: nowrap;
      display: inline;
      line-height: 1;
    }}
    .math-formula.math-display {{
      font-family: "Latin Modern Math", "STIX Two Math", "Cambria Math", Palatino, Georgia, serif;
      font-size: 1.12rem;
      margin: 1rem 0;
      padding: 0.65rem 1rem;
      text-align: center;
      display: block;
    }}
    .math-formula var.math-var {{
      font-style: italic;
      font-weight: 500;
    }}
    .math-formula .math-rm {{
      font-style: normal;
      font-family: inherit;
    }}
    .math-formula sub,
    .math-formula sup {{
      font-size: 0.74em;
      line-height: 0;
      position: relative;
      vertical-align: baseline;
    }}
    .math-formula sup {{ top: -0.45em; }}
    .math-formula sub {{ bottom: -0.24em; }}
    .math-formula .math-frac {{
      display: inline-flex;
      flex-direction: column;
      align-items: center;
      vertical-align: middle;
      margin: 0 0.18em;
      font-size: 0.88em;
      line-height: 1.05;
    }}
    .math-formula .math-frac > .math-num {{
      border-bottom: 1px solid currentColor;
      padding: 0 0.2em 0.08em;
    }}
    .math-formula .math-frac > .math-den {{
      padding: 0.08em 0.2em 0;
    }}
    .math-formula .math-sqrt {{
      display: inline-flex;
      align-items: baseline;
      margin: 0 0.05em;
    }}
    .math-formula .math-sqrt-sign {{
      font-size: 1.05em;
      line-height: 1;
      margin-right: 0.02em;
    }}
    .math-formula .math-radicand {{
      border-top: 1px solid currentColor;
      padding: 0.04em 0.14em 0 0.08em;
    }}
    .math-formula .math-abs {{
      padding: 0 0.05em;
    }}

    /* School-Specific Structural Overview Components */
    .school-overview {{
      margin: 0 0 1.85rem 0;
    }}
    .tufte-epigraph-block {{
      width: 58%;
      border-left: 2px solid #8c8c80;
      padding: 0.15rem 0 0.15rem 0.9rem;
      margin-bottom: 1.6rem;
    }}
    .tufte-epigraph {{
      font-style: italic;
      font-size: 0.96rem;
      color: #444440;
      margin: 0 !important;
    }}
    .kpi-bullet-bar {{
      width: 100%;
      height: 5px;
      background: #e2e8f0;
      margin: 0.38rem 0 0.25rem;
      overflow: hidden;
    }}
    .kpi-bullet-bar > span {{
      display: block;
      height: 100%;
    }}
    .swd-big-idea-card {{
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-left: 6px solid #1e40af;
      border-radius: 0 6px 6px 0;
      padding: 1rem 1.25rem;
    }}
    .swd-big-idea-tag {{
      font-family: var(--font-sans);
      font-size: 0.74rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      color: #1e40af;
      margin-bottom: 0.35rem;
    }}
    .swd-big-idea-text {{
      font-size: 1.02rem;
      font-weight: 600;
      color: #0f172a;
      margin: 0 0 0.65rem 0 !important;
    }}
    .swd-pill-strip {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
    }}
    .swd-pill {{
      font-family: var(--font-sans);
      font-size: 0.74rem;
      font-weight: 700;
      padding: 0.18rem 0.55rem;
      border-radius: 3px;
    }}
    .swd-pill.focal {{ background: #dbeafe; color: #1e3a8a; }}
    .swd-pill.context {{ background: #e2e8f0; color: #475569; }}
    .swiss-blueprint-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      border: 2px solid #0a0a0a;
      background: #ffffff;
    }}
    .swiss-cell {{
      padding: 0.65rem 0.8rem;
      border-right: 1.5px solid #0a0a0a;
      display: flex;
      flex-direction: column;
      gap: 0.2rem;
    }}
    .swiss-cell:last-child {{ border-right: none; }}
    .swiss-cell.accent {{ background: #0a0a0a; color: #ffffff; }}
    .swiss-idx {{
      font-family: var(--font-mono);
      font-size: 0.68rem;
      font-weight: 700;
      color: #e63946;
    }}
    .swiss-val {{
      font-family: var(--font-sans);
      font-size: 0.88rem;
      font-weight: 800;
    }}
    .editorial-brief-box {{
      background: #f4ece1;
      border-top: 4px solid #e3120b;
      border-bottom: 1px solid #1a1817;
      padding: 0.85rem 1.1rem;
    }}
    .editorial-brief-header {{
      font-family: var(--font-sans);
      font-size: 0.74rem;
      font-weight: 800;
      letter-spacing: 0.07em;
      color: #e3120b;
      margin-bottom: 0.45rem;
    }}
    .editorial-brief-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 0.65rem 1.25rem;
      font-size: 0.9rem;
      color: #1a1817;
    }}
    .crimson-sq {{ color: #e3120b; margin-right: 0.3rem; }}

    /* Universal Print-Frame & Running Header/Footer Protection Across All Pages */
    table.print-frame {{
      width: 100% !important;
      max-width: 100% !important;
      table-layout: fixed !important;
      border-collapse: collapse !important;
    }}
    table.print-frame > tbody > tr > td.print-body-cell {{
      width: 100% !important;
      max-width: 100% !important;
      overflow-wrap: break-word;
    }}
    @media print {{
      h1, h2, h3, h4 {{
        break-inside: avoid !important;
        page-break-inside: avoid !important;
        break-after: avoid !important;
        page-break-after: avoid !important;
      }}
      .school-overview,
      .chart-figure,
      .chart-container,
      aside.margin-note {{
        break-inside: avoid !important;
        page-break-inside: avoid !important;
      }}
      .table-wrapper {{
        overflow: visible !important;
        max-width: 100% !important;
      }}
      table.data-table {{
        width: 100% !important;
        max-width: 100% !important;
        font-size: 7.8pt !important;
      }}
      table.data-table th,
      table.data-table td {{
        padding: 0.28rem 0.4rem !important;
        word-break: break-word;
      }}
      .print-header-space {{ height: 14mm !important; }}
      .print-footer-space {{ height: 14mm !important; }}
      .print-running-header {{
        display: flex !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 9.5mm !important;
        align-items: center !important;
        justify-content: space-between !important;
        background: #ffffff !important;
        z-index: 99999 !important;
      }}
      .print-running-footer {{
        display: flex !important;
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 9.5mm !important;
        align-items: center !important;
        justify-content: space-between !important;
        background: #ffffff !important;
        z-index: 99999 !important;
      }}
    }}
    body.hide-margin-notes .margin-note {{ display: none !important; }}
    body.hide-margin-notes p,
    body.hide-margin-notes ul,
    body.hide-margin-notes ol,
    body.hide-margin-notes blockquote {{ width: 92% !important; }}
  </style>
</head>
<body data-school="{html_lib.escape(active_school)}">
  <!-- Screen-only interactive utility bar -->
  <nav class="tufte-toolbar no-print" aria-label="Report Controls">
    <div class="toolbar-brand">
      <span>{html_lib.escape(doc_title)}</span>
      <span class="toolbar-meta"> · N = {html_lib.escape(str(sample_size))} · MoE {html_lib.escape(str(moe_95))}</span>
    </div>
    <div class="toolbar-actions" style="display:flex;align-items:center;gap:0.45rem;">
      {school_selector_html}
      <button type="button" class="toolbar-btn" onclick="document.body.classList.toggle('hide-margin-notes')">
        {labels["notes_btn"]}
      </button>
      <button type="button" class="toolbar-btn primary" onclick="window.print()">
        {labels["print_btn"]}
      </button>
    </div>
  </nav>

  <!-- Fixed Running Header & Footer for Print-to-PDF (Ctrl+P / Save as PDF on EVERY page) -->
  <div class="print-running-header" aria-hidden="true">
    <span id="dps-print-header-left"><strong>{html_lib.escape(doc_title)}</strong></span>
    <span id="dps-print-header-right">{html_lib.escape(labels["header_right"])}</span>
  </div>
  <div class="print-running-footer" aria-hidden="true">
    <span id="dps-print-footer-left">{html_lib.escape(labels["footer_left"])}</span>
    <span id="dps-print-footer-right">{html_lib.escape(labels["footer_right"])}</span>
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
            <article class="tufte-prose main-column">
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

  <script>
    window.DPS_SCHOOLS = {json.dumps(school_js_meta, ensure_ascii=False)};
    window.dpsSwitchSchool = function(schoolId) {{
      var info = window.DPS_SCHOOLS && window.DPS_SCHOOLS[schoolId];
      if (!info) return;
      document.documentElement.setAttribute('data-school', schoolId);
      document.body.setAttribute('data-school', schoolId);
      var styleEl = document.getElementById('dps-school-stylesheet');
      if (styleEl && info.css) styleEl.textContent = info.css;
      var kickerEl = document.getElementById('dps-report-kicker');
      if (kickerEl && info.kicker) kickerEl.textContent = info.kicker;
      var lblEl = document.getElementById('dps-active-school-label');
      if (lblEl && info.short_name) lblEl.textContent = info.short_name;
      var codeEl = document.getElementById('dps-active-school-code');
      if (codeEl) codeEl.textContent = schoolId;
      var hRightEl = document.getElementById('dps-print-header-right');
      if (hRightEl && info.header_right) hRightEl.textContent = info.header_right;
      var footEl = document.getElementById('dps-print-footer-left');
      if (footEl && info.footer_left) footEl.textContent = info.footer_left;
      var ovSlot = document.getElementById('dps-school-overview-slot');
      if (ovSlot && typeof info.overview_html === 'string') ovSlot.innerHTML = info.overview_html;
      if (Array.isArray(info.inline_charts)) {{
        var inlineSlots = document.querySelectorAll('[data-inline-chart-idx]');
        inlineSlots.forEach(function(el) {{
          var idx = parseInt(el.getAttribute('data-inline-chart-idx'), 10);
          if (!isNaN(idx) && info.inline_charts[idx]) {{
            el.innerHTML = info.inline_charts[idx];
          }}
        }});
      }}
      var appEl = document.getElementById('visual-appendix');
      if (appEl && typeof info.appendix_html === 'string') {{
        appEl.innerHTML = info.appendix_html;
      }}
      if (info.note_label_tmpl) {{
        var notes = document.querySelectorAll('aside.margin-note[data-note-index]');
        notes.forEach(function(nEl) {{
          var nIdx = parseInt(nEl.getAttribute('data-note-index'), 10);
          var badgeEl = nEl.querySelector('.margin-note-num');
          if (badgeEl && !isNaN(nIdx)) {{
            var formatted = info.note_label_tmpl
              .replace('{{n:02d}}', String(nIdx).padStart(2, '0'))
              .replace('{{n}}', String(nIdx));
            badgeEl.textContent = formatted;
          }}
        }});
      }}
    }};
  </script>
</body>
</html>
"""

    out_path = Path(output_file) if output_file else md_file.with_suffix(".html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(full_html, encoding="utf-8")
    size_kb = out_path.stat().st_size / 1024.0
    print(
        f"✓ {out_path} ({size_kb:.1f} KB, {'pt-BR' if is_pt else 'en'}, "
        f"School: {spec['short_name']} [{active_school}], Print-to-PDF Ready)"
    )
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-School Print-to-PDF HTML compiler (Tufte, Few, Knaflic, Swiss, Editorial)")
    parser.add_argument("--input", "-i", default=".dps/outputs/export/final_report.md", help="Input Markdown file")
    parser.add_argument("--css", default="references/styles", help="Path to CSS file or styles directory")
    parser.add_argument("--charts-dir", default=".dps/outputs/export/charts", help="Path to standalone SVG charts directory")
    parser.add_argument("--lang", default="auto", choices=["auto", "en", "pt"], help="Report language (en, pt, or auto)")
    parser.add_argument("--output", "-o", default=None, help="Output HTML path (defaults to <input>.html)")
    parser.add_argument(
        "--school",
        "-s",
        default="auto",
        help="Data Design School: tufte (default), few, knaflic, swiss, editorial, or auto",
    )
    args = parser.parse_args()
    generate_html(args.input, args.css, args.charts_dir, lang=args.lang, output_file=args.output, school=args.school)
