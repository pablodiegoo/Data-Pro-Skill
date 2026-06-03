"""
survey_report_generator.py
==========================
Generic Python script to process CSV/XLSX market/opinion survey files.
Detects question types (Single Choice / Multiple Choice / Open-Ended),
generates Markdown reports with Mermaid.js charts and frequency tables.

USAGE:
    1. Edit the CONFIGURATION block below.
    2. Run: python3 survey_report_generator.py

FIXES (v2):
    - Frequency is always calculated as (n / valid_n) × 100 — consistent between chart and table.
    - All question types now produce a chart (including open-ended).
    - Charts are limited to TOP_N_CHART options for readability.
    - Numeric scales (e.g. 1–10, 1–5) are sorted descending; non-numeric options follow last.
    - Pie chart used whenever distinct options ≤ PIE_CHART_MAX_OPTIONS.
"""

import pandas as pd
import re
import os
from collections import defaultdict

# ──────────────────────────────────────────────────────────────
# ⚙️  CONFIGURATION — Edit values here only
# ──────────────────────────────────────────────────────────────
INPUT_FILE   = '/media/pablo-diego/Storage1/AGP/Reports/Saquarema/Beerfest/202603/database/raw/1316610817-SGPSaquarema-BeerFest-Maro2026.csv'
OUTPUT_FILE  = '/media/pablo-diego/Storage1/AGP/Reports/Saquarema/Beerfest/202603/docs/reports/frequencies_report.md'
REPORT_TITLE = 'Relatório de Frequências: Beerfest Saquarema 2026'

# Metadata column exclusion (case-insensitive substrings)
METADATA_KEYWORDS = [
    'index', 'latitude', 'longitude', 'nro', 'data início', 'data fim',
    'pesquisador', 'contato', 'nome', 'identificação', 'nro.', 'lat', 'lon'
]

# Open-ended question keywords — kept, but show top N with chart
OPEN_ENDED_KEYWORDS = ['espontânea', 'o que', 'qual', 'por que', 'melhor', 'pior']

# Cardinality threshold: distinct values > this fraction → skip (likely free-text ID)
CARDINALITY_THRESHOLD = 0.80

# Use Pie chart when distinct options ≤ this number; otherwise Bar
PIE_CHART_MAX_OPTIONS = 6

# Maximum options to show in a chart (top N by frequency)
TOP_N_CHART = 10

# Top N for open-ended qualitative responses
OPEN_ENDED_TOP_N = 10

# Scale detection: if this fraction of non-null values are pure integers → it's a scale
SCALE_DETECTION_THRESHOLD = 0.60
# ──────────────────────────────────────────────────────────────


# ── Utilities ─────────────────────────────────────────────────

def safe_label(text: str) -> str:
    """Sanitize text for Mermaid.js labels."""
    text = str(text).strip()
    text = re.sub(r'["{}[\]()%#]', '', text)
    text = text.replace(':', '-').replace('\n', ' ')
    return text[:50]


def is_metadata(col_name: str) -> bool:
    col_lower = col_name.lower()
    return any(kw in col_lower for kw in METADATA_KEYWORDS)


def is_open_ended(col_name: str) -> bool:
    col_lower = col_name.lower()
    return any(kw in col_lower for kw in OPEN_ENDED_KEYWORDS)


def detect_question_type(col_name: str) -> str:
    if '[rm' in col_name.lower():
        return 'RM'
    if '[ru' in col_name.lower():
        return 'RU'
    if is_open_ended(col_name):
        return 'OPEN'
    return 'RU'


def group_rm_columns(columns: list) -> dict:
    """Groups Multiple Choice columns that share a base name + _N suffix."""
    groups = defaultdict(list)
    for col in columns:
        match = re.match(r'^(.+?)(_\d+)?$', col)
        if match:
            base = match.group(1)
            groups[base].append(col)
    return {k: v for k, v in groups.items() if len(v) > 1}


def clean_column_name(col: str) -> str:
    """Remove leading Q-numbers and trailing _N suffixes from column name."""
    cleaned = re.sub(r'^\d+(\.\d+)*\.\s*', '', col)
    cleaned = re.sub(r'_\d+$', '', cleaned)
    return cleaned.strip()


# ── Scale Detection & Sorting ─────────────────────────────────

def is_numeric_scale(series: pd.Series) -> bool:
    """
    Returns True if the column is a numeric scale (e.g. 0-10, 1-5).
    Robust to: int64/float64 dtypes, '5', '5.0', ' 5 ', mixed with 'NS/NR'.

    Strategy:
    - Convert to numeric (coerce → NaN for non-numeric like 'NS/NR', text labels).
    - Check that the numeric values are integer-like (no decimals beyond .0).
    - If ≥ SCALE_DETECTION_THRESHOLD of non-null values are integer-like → it's a scale.
    """
    if len(series.dropna()) == 0:
        return False

    numeric = pd.to_numeric(series, errors='coerce')
    non_null_num = numeric.dropna()

    if len(non_null_num) == 0:
        return False

    # Check what fraction of the original non-null values became valid numbers
    original_non_null = len(series.dropna())
    numeric_fraction = len(non_null_num) / original_non_null

    if numeric_fraction < SCALE_DETECTION_THRESHOLD:
        return False

    # Among those numeric values, check they are integer-like (e.g. 5.0, not 5.7)
    integer_like = (non_null_num == non_null_num.round()).all()
    return integer_like


def sort_scale_counts(counts: pd.Series) -> pd.Series:
    """
    Sort counts for a numeric scale:
    - Numeric values: descending order (10, 9, 8, ...)
    - Non-numeric (NS/NR, text options): appended after, sorted by frequency desc.
    """
    numeric_idx = []
    text_idx = []
    for val in counts.index:
        try:
            int(str(val).strip())
            numeric_idx.append(val)
        except ValueError:
            text_idx.append(val)

    # Sort numerics descending by value, text by frequency descending
    sorted_numeric = sorted(numeric_idx, key=lambda x: int(str(x).strip()), reverse=True)
    sorted_text = sorted(text_idx, key=lambda x: counts[x], reverse=True)

    ordered_index = sorted_numeric + sorted_text
    return counts[ordered_index]


# ── Chart Generators ──────────────────────────────────────────

def mermaid_pie(title: str, counts: pd.Series, valid_n: int) -> str:
    """Mermaid.js Pie Chart — uses valid_n for % calculation. Caller controls slice."""
    lines = ['```mermaid', f'pie title {safe_label(title)}']
    for val, cnt in counts.items():
        pct = round((cnt / valid_n) * 100, 1)
        lines.append(f'    "{safe_label(str(val))}" : {pct}')
    lines.append('```')
    return "\n".join(lines)


def mermaid_bar(title: str, counts: pd.Series, valid_n: int) -> str:
    """Mermaid.js XY Bar Chart — uses valid_n for % calculation. Caller controls slice."""
    labels = [f'"{safe_label(str(v))}"' for v in counts.index]
    values = [round((cnt / valid_n) * 100, 1) for cnt in counts.values]

    lines = [
        '```mermaid',
        'xychart-beta',
        f'    title "{safe_label(title)}"',
        f'    x-axis [{", ".join(labels)}]',
        f'    y-axis "% Respondentes" 0 --> 100',
        f'    bar [{", ".join(str(v) for v in values)}]',
        '```'
    ]
    return "\n".join(lines)


def make_chart(title: str, counts: pd.Series, valid_n: int, is_scale: bool = False,
               max_options: int = TOP_N_CHART) -> str:
    """
    Selects and generates the appropriate chart. Caller passes max_options to control
    how many items are shown (use TOP_N_CHART for RU, OPEN_ENDED_TOP_N for open).
    """
    if is_scale:
        sorted_counts = sort_scale_counts(counts)  # Scale: no extra slice, sorted by value desc
        return mermaid_bar(title, sorted_counts, valid_n)

    sliced = counts.head(max_options)

    if len(sliced) <= PIE_CHART_MAX_OPTIONS:
        return mermaid_pie(title, sliced, valid_n)

    return mermaid_bar(title, sliced, valid_n)


# ── Frequency Table Generator ─────────────────────────────────

def frequency_table(counts: pd.Series, valid_n: int, total_n: int,
                    base_label: str = 'Respondentes com Resposta',
                    note: str = '') -> str:
    """
    Markdown frequency table.

    IMPORTANT — base rules:
    - Freq. Relativa (%) is ALWAYS (n / valid_n) × 100 where valid_n = non-null respondents.
    - The table footer shows valid_n (actual base) AND total_n (sample) for audit transparency.
    """
    rows = [
        "| Opção | Freq. Absoluta (n) | Freq. Relativa (%) |",
        "| :--- | :---: | :---: |"
    ]
    for val, cnt in counts.items():
        pct = (cnt / valid_n) * 100
        rows.append(f"| {str(val)[:80]} | {cnt} | {pct:.1f}% |")

    rows.append(f"| **Base ({base_label})** | **{valid_n}** | 100.0% |")
    if valid_n != total_n:
        rows.append(f"| _Base Total da Amostra_ | _{total_n}_ | _{valid_n/total_n*100:.1f}% responderam_ |")
    if note:
        rows.append(f"| _{note}_ | | |")

    return "\n".join(rows)


# ── Render Functions ──────────────────────────────────────────

def render_single_choice(col: str, series: pd.Series, total_n: int) -> str:
    """Renders any non-RM question: chart + frequency table."""
    title = clean_column_name(col)
    clean_series = series.dropna().astype(str).str.strip()
    clean_series = clean_series[~clean_series.str.upper().isin(['NAN', ''])]

    valid_n = len(clean_series)
    counts = clean_series.value_counts()

    out = [f"### {title}\n"]

    if valid_n == 0:
        out.append("_Sem respostas válidas._\n")
        return "\n".join(out)

    scale = is_numeric_scale(series)

    if scale:
        sorted_counts = sort_scale_counts(counts)
        # Scale: bar ordered by value desc; no top-N slice (all values matter for scale context)
        out.append(mermaid_bar(title, sorted_counts, valid_n))
        out.append("")
        out.append(frequency_table(sorted_counts, valid_n=valid_n, total_n=total_n))
    else:
        # Non-scale: limit chart to TOP_N_CHART; table still shows all values
        out.append(make_chart(title, counts, valid_n, is_scale=False, max_options=TOP_N_CHART))
        out.append("")
        out.append(frequency_table(counts, valid_n=valid_n, total_n=total_n))

    out.append("")
    return "\n".join(out)


def render_multiple_choice(base_name: str, cols: list, df: pd.DataFrame, total_n: int) -> str:
    """
    Renders a Multiple Choice (RM) question.
    % base = total_n (total respondents), since each respondent could pick multiple options.
    """
    title = clean_column_name(base_name)
    out = [f"### {title} _(Múltipla Escolha — base = {total_n} respondentes)_\n"]

    # Aggregate all non-null, non-placeholder responses
    agg: dict = {}
    for col in cols:
        for val in df[col].dropna():
            val_str = str(val).strip()
            if val_str and val_str.upper() not in ('NAN', 'NS/NR', '999', 'NADA', 'NENHUM', ''):
                agg[val_str] = agg.get(val_str, 0) + 1

    if not agg:
        out.append("_Sem respostas válidas._\n")
        return "\n".join(out)

    counts = pd.Series(agg).sort_values(ascending=False)
    # RM: always bar chart
    out.append(mermaid_bar(title, counts, total_n))
    out.append("")

    # Table — note: base is total_n, total CAN exceed 100%
    rows = [
        "| Opção | Freq. Absoluta (n) | Freq. Relativa (%) |",
        "| :--- | :---: | :---: |"
    ]
    for val, cnt in counts.items():
        pct = (cnt / total_n) * 100
        rows.append(f"| {str(val)[:80]} | {cnt} | {pct:.1f}% |")
    rows.append(f"| **Base Total de Respondentes** | **{total_n}** | _(soma pode ultrapassar 100%)_ |")

    out.append("\n".join(rows))
    out.append("")
    return "\n".join(out)


def render_open_ended(col: str, series: pd.Series, total_n: int) -> str:
    """
    Renders an open-ended question.
    Shows a bar chart (top N) + frequency table.
    """
    title = clean_column_name(col)
    clean_series = series.dropna().astype(str).str.strip()
    clean_series = clean_series[~clean_series.str.upper().isin(['NAN', 'NS/NR', '999', 'NADA', 'NENHUM', ''])]

    valid_n = len(clean_series)
    out = [f"### {title} _(Pergunta Aberta — Top {OPEN_ENDED_TOP_N})_\n"]

    if valid_n == 0:
        out.append("_Sem respostas qualitativas._\n")
        return "\n".join(out)

    counts = clean_series.value_counts()
    # Slice here with OPEN_ENDED_TOP_N — chart and table share this same top set
    top_counts = counts.head(OPEN_ENDED_TOP_N)

    # Chart: always bar for open-ended; limit already applied above via OPEN_ENDED_TOP_N
    out.append(mermaid_bar(title, top_counts, valid_n))
    out.append("")

    # Table with correct % (based on valid_n)
    rows = [
        "| Resposta | Freq. Absoluta (n) | Freq. Relativa (%) |",
        "| :--- | :---: | :---: |"
    ]
    for val, cnt in top_counts.items():
        pct = (cnt / valid_n) * 100
        rows.append(f"| {str(val)[:100]} | {cnt} | {pct:.1f}% |")
    rows.append(f"| **Base (Respondentes com Resposta)** | **{valid_n}** | |")
    if valid_n != total_n:
        rows.append(f"| _Base Total da Amostra_ | _{total_n}_ | _{valid_n/total_n*100:.1f}% responderam_ |")

    out.append("\n".join(rows))
    out.append("")
    return "\n".join(out)


# ── Correlation Matrix ────────────────────────────────────────

def corr_emoji(r: float) -> str:
    """
    Returns a colored block emoji representing Pearson r strength.
    Positive: 🟥 (strong) → 🟧 → 🟨 → ⬜ (negligible)
    Negative: 🟦 (weak) → 🟪 → 🔵 (strong)
    """
    if r >= 0.70:  return '🟥'
    if r >= 0.50:  return '🟧'
    if r >= 0.30:  return '🟨'
    if r >= -0.30: return '⬜'
    if r >= -0.50: return '🟦'
    if r >= -0.70: return '🟪'
    return '🔵'


def render_correlation_matrix(df: pd.DataFrame, scale_cols: list) -> str:
    """
    Computes Pearson correlation between all numeric scale columns and renders
    the result as a native Markdown table with emoji color coding.
    No images — pure Markdown, compatible with VS Code, GitHub and Obsidian.

    Legend:
        🟥 ≥ 0.70  Strong positive
        🟧 ≥ 0.50  Moderate positive
        🟨 ≥ 0.30  Weak positive
        ⬜  near 0  Negligible
        🟦 ≤ -0.30 Weak negative
        🟪 ≤ -0.50 Moderate negative
        🔵 ≤ -0.70 Strong negative
    """
    if len(scale_cols) < 2:
        return ""

    # Convert to numeric, force errors to NaN
    num_df = df[scale_cols].apply(pd.to_numeric, errors='coerce')

    # Drop columns with all-NaN after conversion
    num_df = num_df.dropna(axis=1, how='all')
    if num_df.shape[1] < 2:
        return ""

    corr = num_df.corr(method='pearson')
    cols = corr.columns.tolist()

    # Short labels for table headers (truncated clean names)
    short_labels = [clean_column_name(c)[:25] for c in cols]

    lines = [
        "---\n",
        "## 📊 Matriz de Correlação (Escalas Numéricas)\n",
        "> Correlação de Pearson entre todas as perguntas identificadas como escala numérica.  ",
        "> **Legenda:** 🟥 forte positiva ≥0.70 · 🟧 ≥0.50 · 🟨 ≥0.30 · ⬜ negligenciável · 🟦 ≤−0.30 · 🟪 ≤−0.50 · 🔵 forte negativa ≤−0.70\n",
    ]

    # Header row
    header = "| Pergunta | " + " | ".join(f"`{lbl}`" for lbl in short_labels) + " |"
    separator = "| :--- | " + " | ".join(":---:" for _ in cols) + " |"
    lines.append(header)
    lines.append(separator)

    # One row per variable
    for i, col_i in enumerate(cols):
        row_label = f"`{short_labels[i]}`"
        cells = []
        for j, col_j in enumerate(cols):
            r = corr.loc[col_i, col_j]
            if i == j:
                cells.append("—")  # diagonal
            elif pd.isna(r):
                cells.append("N/A")
            else:
                cells.append(f"{corr_emoji(r)} `{r:+.2f}`")
        lines.append(f"| {row_label} | " + " | ".join(cells) + " |")

    lines.append("")
    lines.append(f"_n = {len(num_df)} respondentes · {len(cols)} variáveis em escala detectadas_\n")
    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────

def main():
    # 1. Load
    ext = os.path.splitext(INPUT_FILE)[1].lower()
    if ext == '.xlsx':
        df = pd.read_excel(INPUT_FILE)
    elif ext == '.csv':
        df = pd.read_csv(INPUT_FILE, encoding='utf-8-sig')
    else:
        raise ValueError(f"Unsupported format: {ext}. Use .csv or .xlsx")

    total_n = len(df)
    print(f"✅ Loaded: {total_n} rows × {len(df.columns)} columns.")

    # 2. Filter metadata and high-cardinality columns
    valid_cols = []
    for col in df.columns:
        if is_metadata(col):
            print(f"   [SKIP Metadata] {col}")
            continue
        n_distinct = df[col].nunique()
        if n_distinct > CARDINALITY_THRESHOLD * total_n and not is_open_ended(col):
            print(f"   [SKIP High-Cardinality {n_distinct}/{total_n}] {col}")
            continue
        valid_cols.append(col)

    print(f"✅ {len(valid_cols)} columns selected for analysis.")

    # 3. Group RM columns
    rm_groups = group_rm_columns(valid_cols)
    rm_cols_flat = {c for cols in rm_groups.values() for c in cols}

    # 4. Build report
    report = [
        f"# {REPORT_TITLE}",
        f"\n> **Base Total da Amostra:** {total_n} respondentes  ",
        f"> **Arquivo:** `{os.path.basename(INPUT_FILE)}`  ",
        f"> **Nota:** _Freq. Relativa (%) calculada sobre respondentes válidos de cada pergunta (excluindo NaN)._\n",
        "---\n"
    ]

    processed_rm = set()
    for col in valid_cols:

        # RM group: process the full group once
        if col in rm_cols_flat:
            for base, cols in rm_groups.items():
                if col in cols and base not in processed_rm:
                    report.append(render_multiple_choice(base, cols, df, total_n))
                    processed_rm.add(base)
            continue

        q_type = detect_question_type(col)

        if q_type == 'OPEN':
            report.append(render_open_ended(col, df[col], total_n))
        else:
            # RU or default — includes scale detection inside render_single_choice
            report.append(render_single_choice(col, df[col], total_n))

    # 5. Correlation matrix — collect all scale columns detected
    scale_cols = [
        col for col in valid_cols
        if col not in rm_cols_flat and detect_question_type(col) not in ('OPEN', 'RM')
        and is_numeric_scale(df[col])
    ]
    print(f"✅ {len(scale_cols)} colunas de escala detectadas para matriz de correlação.")
    corr_block = render_correlation_matrix(df, scale_cols)
    if corr_block:
        report.append(corr_block)

    # 6. Save
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))

    print(f"\n✅ Report saved → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
