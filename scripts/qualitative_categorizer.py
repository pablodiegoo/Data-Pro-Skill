#!/usr/bin/env python3
"""Data-Pro-Skill Qualitative Categorizer, Emergent Theme Extractor & Article 4 Engine.

Implements:
  - Automatic open-text column & segment column discovery
  - Bilingual stopword filtering (auto-loads references/analysis/stopwords_pt.txt + English)
  - Emergent keyword-cluster theme taxonomy (or custom category dictionary)
  - Strict Constitutional Article 4 enforcement:
      * N < 30: raw counts only ("4 of 19"), zero percentages
      * >= 2 literal participant verbatims per theme with respondent & segment tags
      * Explicit Silence Notes for segments with 0 open-ended responses

Outputs in output directory (.dps/outputs/quali/):
  - quali_themes.csv
  - quali_verbatims.json
  - quali_report.md
"""

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
STOPWORDS_PT_PATH = SCRIPT_DIR.parent / "references" / "analysis" / "stopwords_pt.txt"

DEFAULT_STOPWORDS = {
    # English
    "the", "and", "for", "that", "this", "with", "was", "were", "are", "have", "has", "had",
    "not", "but", "from", "they", "very", "more", "some", "what", "when", "where", "who",
    "will", "would", "could", "should", "about", "into", "than", "then", "them", "these",
    "those", "their", "there", "been", "being", "also", "just", "only", "like", "good",
    "great", "nice", "really", "much", "many", "all", "any", "out", "can", "our", "your",
    # Portuguese fallback
    "que", "para", "com", "não", "nao", "uma", "por", "mais", "dos", "das", "como", "mas",
    "foi", "ao", "ele", "ela", "entre", "depois", "sem", "mesmo", "aos", "ter", "seus",
    "quem", "nas", "me", "esse", "eles", "estão", "você", "tinha", "foram", "essa", "num",
    "nem", "suas", "meu", "às", "minha", "têm", "numa", "pelos", "elas", "havia", "seja",
    "qual", "será", "nós", "tenho", "lhe", "deles", "essas", "esses", "pelas", "este",
    "fosse", "dele", "muito", "muita", "bom", "boa", "tudo", "todos", "todas", "nada",
    "sobre", "está", "esta", "isso", "isto", "aqui", "onde", "quando", "porque", "pois",
}


def _load_all_stopwords():
    sw = set(DEFAULT_STOPWORDS)
    if STOPWORDS_PT_PATH.exists():
        try:
            for line in STOPWORDS_PT_PATH.read_text(encoding="utf-8").splitlines():
                w = line.strip().lower()
                if w:
                    sw.add(w)
        except Exception:
            pass
    return sw


# ==============================================================================
# LEGACY API (Preserved for backwards compatibility)
# ==============================================================================

def categorize_text(text: str, category_dict: dict, default_category: str = "Outros / Other", missing_category: str = "NS/NR") -> str:
    """Categorizes a spontaneous text string based on a dictionary of keywords."""
    if not text or pd.isna(text):
        return missing_category
    text_lower = str(text).strip().lower()
    if not text_lower or text_lower in ("nan", "none", "-", "n/a", "ns/nr", "nada", "nenhum", "none"):
        return missing_category
    for cat_name, keywords in category_dict.items():
        if any(kw.lower() in text_lower for kw in keywords):
            return cat_name
    return default_category


def apply_qualitative_categorization(df: pd.DataFrame, source_col: str, target_col: str, category_dict: dict):
    """Applies qualitative categorization to an entire DataFrame column."""
    df_copy = df.copy()
    df_copy[target_col] = df_copy[source_col].apply(lambda x: categorize_text(x, category_dict))
    counts = df_copy[target_col].value_counts(normalize=True) * 100
    print(f"Categorization Summary for '{source_col}':")
    print(counts.round(2).astype(str) + "%")
    return df_copy


# ==============================================================================
# EMERGENT THEME DISCOVERY & ARTICLE 4 SYNTHESIS ENGINE
# ==============================================================================

def _discover_emergent_categories(texts, stopwords, max_themes=5):
    """Build an emergent keyword dictionary from raw verbatims when no custom dict is supplied."""
    # Curated domain-agnostic semantic buckets + data-driven top tokens
    seed_buckets = {
        "Service, Support & Responsiveness": [
            "support", "service", "help", "staff", "team", "agent", "response", "slow", "fast",
            "atendimento", "suporte", "equipe", "demora", "rápido", "rapido", "atenção", "fila",
        ],
        "Price, Value & Billing": [
            "price", "cost", "expensive", "cheap", "billing", "fee", "value", "money", "plan",
            "preço", "preco", "caro", "barato", "valor", "custo", "cobrança", "mensalidade",
        ],
        "Product Quality, Reliability & Features": [
            "quality", "bug", "crash", "feature", "reliable", "stable", "work", "broken", "performance",
            "qualidade", "erro", "falha", "funciona", "sistema", "produto", "estrutura", "limpeza",
        ],
        "Usability, Access & Experience": [
            "easy", "hard", "interface", "ux", "design", "intuitive", "confusing", "access", "onboarding",
            "fácil", "facil", "difícil", "dificil", "acesso", "uso", "experiência", "organiz", "segurança",
        ],
    }

    # Check how many texts match seed buckets
    matched_counts = {k: 0 for k in seed_buckets}
    for t in texts:
        tl = str(t).lower()
        for k, kws in seed_buckets.items():
            if any(kw in tl for kw in kws):
                matched_counts[k] += 1
                break

    active_dict = {k: v for k, v in seed_buckets.items() if matched_counts[k] > 0}

    # Supplement with top emergent frequent tokens not covered by seed buckets
    token_counter = Counter()
    for t in texts:
        words = re.findall(r"[a-zA-ZÀ-ÿ]{4,}", str(t).lower())
        for w in set(words):
            if w not in stopwords:
                token_counter[w] += 1

    used_kws = {kw for kws in active_dict.values() for kw in kws}
    for tok, freq in token_counter.most_common(12):
        if len(active_dict) >= max_themes:
            break
        if freq >= 2 and tok not in used_kws:
            theme_title = f"Emergent Theme: {tok.capitalize()}"
            active_dict[theme_title] = [tok]
            used_kws.add(tok)

    if not active_dict:
        # Fallback if verbatims are very short/unique
        for tok, freq in token_counter.most_common(3):
            active_dict[f"Theme: {tok.capitalize()}"] = [tok]

    return active_dict


def run_qualitative_synthesis(
    df,
    text_col=None,
    segment_col=None,
    segments_filter=None,
    output_dir=".dps/outputs/quali",
    custom_categories=None,
):
    """Run full Article 4 qualitative categorization, verbatim extraction, and silence auditing."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stopwords = _load_all_stopwords()

    # Auto-detect open-text column if not provided
    if not text_col or text_col not in df.columns:
        best_col = None
        best_len = 0.0
        for c in df.columns:
            s = df[c].dropna().astype(str).str.strip()
            s = s[s != ""]
            if len(s) == 0:
                continue
            avg_l = s.str.len().mean()
            uniq_r = s.nunique() / len(s)
            if avg_l > best_len and (avg_l > 18 or uniq_r > 0.4):
                best_len = avg_l
                best_col = c
        text_col = best_col or df.columns[-1]

    # Auto-detect segment column if not provided
    if not segment_col or segment_col not in df.columns:
        for c in df.columns:
            if c == text_col:
                continue
            nunique = df[c].dropna().nunique()
            if 2 <= nunique <= 12:
                segment_col = c
                break

    work_df = df.copy()
    if segments_filter and segment_col and segment_col in work_df.columns:
        allowed = {s.strip().lower() for s in str(segments_filter).split(",") if s.strip()}
        if allowed:
            work_df = work_df[work_df[segment_col].astype(str).str.strip().str.lower().isin(allowed)]

    # Identify valid non-empty verbatims
    raw_series = work_df[text_col]
    valid_mask = (
        raw_series.notna()
        & (raw_series.astype(str).str.strip() != "")
        & (~raw_series.astype(str).str.strip().str.lower().isin({"nan", "none", "n/a", "-", "ns/nr", "nada", "nenhum"}))
    )
    valid_df = work_df[valid_mask].copy()
    n_total_rows = len(work_df)
    n_valid = len(valid_df)
    is_small_sample = n_valid < 30

    # Silence Notes detection per segment (Article 4c)
    silence_segments = []
    segment_counts = {}
    if segment_col and segment_col in work_df.columns:
        all_segs = work_df[segment_col].dropna().astype(str).str.strip().unique()
        for seg in sorted(all_segs):
            if not seg:
                continue
            seg_total = int((work_df[segment_col].astype(str).str.strip() == seg).sum())
            seg_valid = int((valid_df[segment_col].astype(str).str.strip() == seg).sum())
            segment_counts[seg] = {"total_n": seg_total, "valid_verbatims": seg_valid}
            if seg_valid == 0:
                silence_segments.append(seg)

    categories = custom_categories or _discover_emergent_categories(valid_df[text_col].tolist(), stopwords)
    valid_df["_theme"] = valid_df[text_col].apply(
        lambda x: categorize_text(x, categories, default_category="General Feedback & Other")
    )

    # Aggregate themes with Article 4 formatting and >= 2 literal verbatims
    theme_vc = valid_df["_theme"].value_counts()
    theme_rows = []
    verbatims_payload = {
        "text_column": text_col,
        "segment_column": segment_col,
        "n_total_respondents": n_total_rows,
        "n_valid_verbatims": n_valid,
        "small_sample_rule_active": is_small_sample,
        "silence_segments": silence_segments,
        "segment_coverage": segment_counts,
        "themes": [],
    }

    for theme_name, count in theme_vc.items():
        cnt = int(count)
        sub_t = valid_df[valid_df["_theme"] == theme_name]
        # Format frequency strictly per Article 4
        if is_small_sample:
            freq_display = f"{cnt} of {n_valid}"
            pct_val = None
            moe_val = None
        else:
            p = cnt / n_valid if n_valid > 0 else 0.0
            pct_val = round(p * 100.0, 1)
            moe_val = round(1.96 * math.sqrt(p * (1.0 - p) / n_valid) * 100.0, 1)
            freq_display = f"{cnt} of {n_valid} ({pct_val:.1f}% ±{moe_val:.1f}%)"

        # Dominant segment for this theme
        dom_seg = "All Segments"
        if segment_col and segment_col in sub_t.columns and len(sub_t) > 0:
            top_s = sub_t[segment_col].astype(str).value_counts()
            if len(top_s) > 0:
                dom_seg = f"{top_s.index[0]} (n={int(top_s.iloc[0])})"

        # Select up to 3 literal verbatims (minimum 2 whenever cnt >= 2)
        quotes = []
        for idx, r in sub_t.head(3).iterrows():
            q_txt = str(r[text_col]).strip()
            seg_lbl = str(r[segment_col]).strip() if (segment_col and segment_col in r and pd.notna(r[segment_col])) else "Unspecified"
            quotes.append({
                "respondent_id": str(r.get("id", r.get("ID", idx))),
                "segment": seg_lbl,
                "quote": q_txt,
            })

        theme_entry = {
            "theme": theme_name,
            "count": cnt,
            "n_valid_base": n_valid,
            "frequency_display": freq_display,
            "pct": pct_val,
            "moe_95_pct": moe_val,
            "dominant_segment": dom_seg,
            "verbatims": quotes,
        }
        verbatims_payload["themes"].append(theme_entry)
        theme_rows.append({
            "theme": theme_name,
            "count": cnt,
            "n_valid_base": n_valid,
            "frequency_display": freq_display,
            "dominant_segment": dom_seg,
            "sample_verbatim_1": quotes[0]["quote"] if len(quotes) >= 1 else "",
            "sample_verbatim_2": quotes[1]["quote"] if len(quotes) >= 2 else "",
        })

    pd.DataFrame(theme_rows).to_csv(out_dir / "quali_themes.csv", index=False)
    (out_dir / "quali_verbatims.json").write_text(
        json.dumps(verbatims_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Build Tufte Markdown Report (quali_report.md)
    md_lines = [
        f"# Qualitative Verbatim Synthesis: `{text_col}`",
        "",
        f"**Valid Open-Ended Responses ($N_{{\\text{{quali}}}}$):** `{n_valid}` (out of `{n_total_rows}` total respondents) · "
        f"**Article 4 Reporting Mode:** `{'RAW COUNTS ONLY (N < 30)' if is_small_sample else 'Parametric % ± 95% CI MoE (N ≥ 30)'}`",
        "",
        f"> **Margin Note:** **Constitutional Article 4 Compliance:** "
        + (
            f"Because valid qualitative responses $N = {n_valid} < 30$, percentages are suppressed in favor of exact raw counts (`n of {n_valid}`) to prevent false precision."
            if is_small_sample
            else f"With $N = {n_valid} \\ge 30$, theme proportions include 95% confidence margins alongside raw counts."
        ),
        "",
        "## 1. Emergent Theme Taxonomy",
        "",
        "| Qualitative Theme | Frequency | Dominant Segment | Representative Verbatim Anchor |",
        "| :--- | ---: | :--- | :--- |",
    ]

    for t in verbatims_payload["themes"]:
        anchor = t["verbatims"][0]["quote"][:90] + ("…" if len(t["verbatims"][0]["quote"]) > 90 else "") if t["verbatims"] else "—"
        md_lines.append(
            f"| **{t['theme']}** | {t['frequency_display']} | {t['dominant_segment']} | *“{anchor}”* |"
        )
    md_lines.extend(["", "## 2. Literal Participant Verbatims by Theme (Article 4 Evidence)", ""])

    for t in verbatims_payload["themes"]:
        md_lines.append(f"### {t['theme']} (`{t['frequency_display']}` — Dominant: {t['dominant_segment']})")
        md_lines.append("")
        for q in t["verbatims"]:
            md_lines.append(
                f'> *“{q["quote"]}”* — **[Respondent #{q["respondent_id"]}, Segment: {q["segment"]}]**'
            )
            md_lines.append("")

    # Silence Notes section (Article 4c)
    md_lines.extend(["## 3. Segment Coverage & Silence Notes", ""])
    if silence_segments:
        for s_seg in silence_segments:
            md_lines.append(
                f"- **Silence Note (`{s_seg}`):** Segment `{s_seg}` recorded `0` open-ended responses out of `{segment_counts[s_seg]['total_n']}` respondents — qualitative silence noted."
            )
    else:
        md_lines.append("- **Full Segment Voice Coverage:** All active demographic/behavioral segments recorded $\\ge 1$ open-ended verbatim response (zero silent segments).")
    md_lines.append("")

    (out_dir / "quali_report.md").write_text("\n".join(md_lines), encoding="utf-8")
    return verbatims_payload


def main():
    parser = argparse.ArgumentParser(description="Data-Pro-Skill Qualitative Categorizer & Article 4 Synthesis CLI")
    parser.add_argument("input", help="Input dataset file (.csv, .xlsx, .ods, .parquet)")
    parser.add_argument("--text-col", "-t", default=None, help="Open-ended text column name")
    parser.add_argument("--segment-col", "-s", default=None, help="Segment column name for cross-mapping")
    parser.add_argument("--segments", default=None, help="Optional comma-separated segment filter")
    parser.add_argument("-o", "--output", default=".dps/outputs/quali", help="Output directory")

    args = parser.parse_args()
    try:
        p = Path(args.input)
        if p.suffix.lower() in (".xlsx", ".xls"):
            df = pd.read_excel(p)
        else:
            df = pd.read_csv(p)
        res = run_qualitative_synthesis(
            df,
            text_col=args.text_col,
            segment_col=args.segment_col,
            segments_filter=args.segments,
            output_dir=args.output,
        )
        print(
            f"✅ Qualitative synthesis complete in {args.output} "
            f"(N_quali={res['n_valid_verbatims']}, Themes={len(res['themes'])}, "
            f"SmallSampleMode={res['small_sample_rule_active']})"
        )
    except Exception as e:
        print(f"❌ Error during qualitative synthesis: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
