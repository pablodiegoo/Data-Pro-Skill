#!/usr/bin/env python3
"""Data-Pro-Skill Quantitative Setup, Profiling & Quality Gate Engine.

Supports:
  1. Full dataset profiling & quality gates (/dps-setup):
     python3 scripts/quant_analyzer.py <dataset.csv> -o .dps/outputs/setup/
     python3 scripts/quant_analyzer.py <dataset.csv> --profile -o .dps/outputs/setup/
  2. Legacy domain score normalization:
     python3 scripts/quant_analyzer.py <dataset.csv> <config.json> -o processed_output.csv

Outputs in output directory:
  - column_mapping.json      (Article 7a snake_case schema mapping)
  - 00_profile.json          (Complete parametric & non-parametric variable profiles)
  - setup_manifest.json      (Project manifest for downstream /dps-plan and /dps-export)
  - setup_segments.csv       (Segment x Metric summary table for Tufte dot plots)
  - setup_report.md          (Tufte-formatted setup & Article 6 Quality Gate report)
  - 00_project_manifest.md   (Executive dataset manifest)
"""

import argparse
import datetime
import json
import math
import os
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd


# ==============================================================================
# LEGACY DOMAIN NORMALIZATION API (Preserved for backwards compatibility)
# ==============================================================================

def normalize_points(row, columns, max_points, scale_to):
    """Sums points from specific columns and normalizes to a new scale."""
    points_sum = 0
    if isinstance(columns, dict):
        for col, weight in columns.items():
            val = str(row.get(col, "")).strip()
            if val and val.lower() not in ["nan", "none", "0", "false", "no", "não"]:
                points_sum += weight
    elif isinstance(columns, list):
        for col in columns:
            val = str(row.get(col, "0")).lower()
            if val in ["1", "true", "yes", "x", "sim", "checked"]:
                points_sum += 1
            elif val.isdigit():
                points_sum += int(val)
    return (points_sum / max_points) * scale_to if max_points > 0 else 0


def calculate_scores(df, config):
    """Applies normalizations and calculates domain averages."""
    if "normalizations" in config:
        for norm_col, settings in config["normalizations"].items():
            df[norm_col] = df.apply(
                lambda r: normalize_points(r, settings["columns"], settings["max_points"], settings["scale_to"]),
                axis=1,
            )
    domain_columns = []
    if "domains" in config:
        for domain_name, cols in config["domains"].items():
            for col in cols:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
            df[domain_name] = df[cols].mean(axis=1)
            domain_columns.append(domain_name)
    if domain_columns:
        df["Escore Final"] = df[domain_columns].mean(axis=1)
    return df


# ==============================================================================
# DATASET LOADER & SNAKE_CASE SCHEMA MAPPER (Article 7a)
# ==============================================================================

def load_dataset(path):
    """Load CSV, TSV, Excel (.xlsx/.xls), ODS, or Parquet into a pandas DataFrame."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {p}")
    ext = p.suffix.lower()
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(p)
    if ext == ".ods":
        return pd.read_excel(p, engine="odf")
    if ext == ".parquet":
        return pd.read_parquet(p)
    if ext == ".tsv":
        return pd.read_csv(p, sep="\t")
    # Default CSV with automatic encoding & delimiter fallback
    for enc in ("utf-8", "utf-8-sig", "latin1", "cp1252"):
        try:
            return pd.read_csv(p, encoding=enc)
        except Exception:
            continue
    return pd.read_csv(p)


def to_snake_case(text, max_len=42):
    """Convert an arbitrary survey column header into a clean snake_case identifier."""
    norm = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode("ascii")
    norm = re.sub(r"[^a-zA-Z0-9]+", "_", norm.lower()).strip("_")
    if not norm:
        norm = "col"
    if norm[0].isdigit():
        norm = "q_" + norm
    if len(norm) > max_len:
        norm = norm[:max_len].rstrip("_")
    return norm


def classify_column(series, col_name):
    """Classify a column into: id, weight, likert, numeric, categorical, binary, open_text, datetime."""
    name_low = str(col_name).lower()
    non_null = series.dropna()
    n_valid = len(non_null)
    if n_valid == 0:
        return "empty"

    # Weight column detection
    if any(w in name_low for w in ("weight", "peso", "pond", "fator_exp", "wgt")):
        num_s = pd.to_numeric(non_null, errors="coerce").dropna()
        if len(num_s) / n_valid > 0.9:
            return "weight"

    # ID column detection
    if re.match(r"^(id|respondent_id|uuid|record_id|id_pesquisa|codigo|cpf|email)$", name_low):
        return "id"

    # Try numeric conversion
    num_s = pd.to_numeric(non_null, errors="coerce").dropna()
    if len(num_s) / n_valid >= 0.85:
        uniq = num_s.nunique()
        mn, mx = float(num_s.min()), float(num_s.max())
        # Check if ID-like (monotonically unique integers at column 0)
        if uniq == n_valid and n_valid > 30 and ("id" in name_low or "cod" in name_low):
            return "id"
        if uniq == 2 and set(num_s.unique()).issubset({0, 1, 0.0, 1.0}):
            return "binary"
        # Likert / Rating scale: integer-like values in [1..5], [1..7], [0..10], [1..10]
        is_int_like = np.all(np.isclose(num_s, np.round(num_s)))
        if is_int_like and 2 <= uniq <= 11 and 0 <= mn and mx <= 10:
            return "likert"
        return "numeric"

    # String / Object column
    str_s = non_null.astype(str).str.strip()
    str_s = str_s[str_s != ""]
    if len(str_s) == 0:
        return "empty"
    uniq = str_s.nunique()
    avg_len = str_s.str.len().mean()
    max_len = str_s.str.len().max()

    # Open-ended text detection
    if avg_len > 32 or (max_len > 75 and uniq / len(str_s) > 0.35):
        return "open_text"
    if any(k in name_low for k in ("comment", "comentario", "sugest", "open", "aberto", "verbatim", "motivo", "por_que", "observa")):
        if uniq > 8 or avg_len > 18:
            return "open_text"

    if uniq == 2:
        return "binary"
    if uniq <= max(25, int(len(str_s) * 0.25)):
        return "categorical"
    if uniq == len(str_s) and avg_len < 25:
        return "id"
    return "open_text" if avg_len > 22 else "categorical"


# ==============================================================================
# STATISTICAL PROFILING & QUALITY GATES (Articles 1, 6, 7)
# ==============================================================================

def _compute_moe_proportion(p, n):
    if n <= 0:
        return 0.0
    p_clamped = min(max(float(p), 0.0), 1.0)
    return 1.96 * math.sqrt((p_clamped * (1.0 - p_clamped)) / n) * 100.0


def profile_dataset(df, output_dir, weight_col=None, config=None, dataset_name="Survey Dataset"):
    """Run comprehensive /dps-setup profiling and Article 6 Quality Gates."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if config:
        df = calculate_scores(df.copy(), config)

    n_rows, n_cols = df.shape

    # 1. Build snake_case column_mapping.json (Article 7a)
    col_mapping = {}
    used_snakes = set()
    for col in df.columns:
        base_snake = to_snake_case(col)
        snake = base_snake
        counter = 2
        while snake in used_snakes:
            snake = f"{base_snake}_{counter}"
            counter += 1
        used_snakes.add(snake)
        role = classify_column(df[col], col)
        col_mapping[snake] = {
            "original_name": str(col),
            "snake_name": snake,
            "role": role,
            "dtype": str(df[col].dtype),
        }

    # Detect weight column if not explicitly passed
    if not weight_col:
        for info in col_mapping.values():
            if info["role"] == "weight":
                weight_col = info["original_name"]
                break

    # Compute effective sample size (Kish's N_eff)
    if weight_col and weight_col in df.columns:
        w = pd.to_numeric(df[weight_col], errors="coerce").fillna(0.0)
        w_pos = w[w > 0]
        if len(w_pos) > 0 and (w_pos ** 2).sum() > 0:
            n_eff = float((w_pos.sum() ** 2) / ((w_pos ** 2).sum()))
            deff = float(len(w_pos) / n_eff) if n_eff > 0 else 1.0
        else:
            n_eff = float(n_rows)
            deff = 1.0
    else:
        n_eff = float(n_rows)
        deff = 1.0

    global_moe_pct = round(_compute_moe_proportion(0.5, n_eff), 2)

    # 2. Variable-by-variable statistical profiling
    variables_profile = {}
    likert_cols = []
    numeric_cols = []
    categorical_cols = []
    open_text_cols = []
    moderate_missing_cols = []
    high_missing_cols = []
    pct_sum_violations = []

    for snake, meta in col_mapping.items():
        col = meta["original_name"]
        role = meta["role"]
        s = df[col]
        n_missing = int(s.isna().sum() + (s.astype(str).str.strip() == "").sum() - s.isna().sum())
        # Accurate missing count including empty strings
        non_empty_mask = s.notna() & (s.astype(str).str.strip() != "") & (s.astype(str).str.strip().str.lower() != "nan")
        n_valid = int(non_empty_mask.sum())
        n_missing = int(n_rows - n_valid)
        missing_pct = round((n_missing / n_rows * 100.0) if n_rows > 0 else 0.0, 2)

        if missing_pct > 20.0:
            high_missing_cols.append({"column": col, "snake": snake, "missing_pct": missing_pct})
        elif missing_pct > 10.0:
            moderate_missing_cols.append({"column": col, "snake": snake, "missing_pct": missing_pct})

        v_prof = {
            "original_name": col,
            "snake_name": snake,
            "role": role,
            "n_valid": n_valid,
            "n_missing": n_missing,
            "missing_pct": missing_pct,
        }

        if role in ("likert", "numeric", "binary"):
            num_s = pd.to_numeric(s[non_empty_mask], errors="coerce").dropna()
            if len(num_s) > 0:
                mean_val = float(num_s.mean())
                sd_val = float(num_s.std(ddof=1)) if len(num_s) > 1 else 0.0
                se_val = sd_val / math.sqrt(len(num_s)) if len(num_s) > 1 else 0.0
                moe_95 = 1.96 * se_val
                q25, med_val, q75 = [float(x) for x in np.percentile(num_s, [25, 50, 75])]
                iqr_val = q75 - q25
                mad_val = float(np.median(np.abs(num_s - med_val)))
                skew_val = float(num_s.skew()) if len(num_s) > 2 else 0.0
                mn_val, mx_val = float(num_s.min()), float(num_s.max())

                v_prof.update({
                    "mean": round(mean_val, 3),
                    "sd": round(sd_val, 3),
                    "se": round(se_val, 4),
                    "moe_95": round(moe_95, 3),
                    "median": round(med_val, 3),
                    "iqr": round(iqr_val, 3),
                    "mad": round(mad_val, 3),
                    "skewness": round(skew_val, 3),
                    "min": round(mn_val, 3),
                    "max": round(mx_val, 3),
                    "recommended_estimator": "Non-Parametric (Median/IQR)" if abs(skew_val) > 1.0 else "Parametric (Mean/SD)",
                })

                if role == "likert":
                    likert_cols.append(col)
                    val_counts = num_s.value_counts().sort_index()
                    v_prof["distribution"] = {str(k): int(v) for k, v in val_counts.items()}
                    # Top-2-Box and Bottom-2-Box
                    if mx_val <= 5:
                        t2b = float((num_s >= 4).mean() * 100.0)
                        b2b = float((num_s <= 2).mean() * 100.0)
                    elif mx_val <= 7:
                        t2b = float((num_s >= 6).mean() * 100.0)
                        b2b = float((num_s <= 2).mean() * 100.0)
                    else:
                        t2b = float((num_s >= 9).mean() * 100.0)
                        b2b = float((num_s <= 6).mean() * 100.0)
                    v_prof["top2box_pct"] = round(t2b, 1)
                    v_prof["bottom2box_pct"] = round(b2b, 1)
                    v_prof["net_score"] = round(t2b - b2b, 1)
                else:
                    numeric_cols.append(col)

        if role in ("categorical", "binary"):
            categorical_cols.append(col)
            clean_cats = s[non_empty_mask].astype(str).str.strip()
            vc = clean_cats.value_counts()
            cat_table = {}
            pct_sum = 0.0
            for k, cnt in vc.head(20).items():
                p_val = (cnt / n_valid) if n_valid > 0 else 0.0
                pct_val = round(p_val * 100.0, 1)
                pct_sum += (cnt / n_valid * 100.0) if n_valid > 0 else 0.0
                cat_table[str(k)] = {
                    "count": int(cnt),
                    "pct": pct_val,
                    "moe_95_pct": round(_compute_moe_proportion(p_val, n_valid), 1),
                }
            v_prof["categories"] = cat_table
            v_prof["n_unique"] = int(clean_cats.nunique())
            v_prof["distribution"] = {str(k): int(cnt) for k, cnt in vc.head(12).items()}
            if vc.shape[0] <= 20 and n_valid > 0 and abs(pct_sum - 100.0) > 0.5:
                pct_sum_violations.append({"column": col, "sum_pct": round(pct_sum, 2)})

        if role == "open_text":
            open_text_cols.append(col)
            clean_txt = s[non_empty_mask].astype(str).str.strip()
            v_prof["n_verbatims"] = int(len(clean_txt))
            v_prof["avg_char_length"] = round(float(clean_txt.str.len().mean()), 1) if len(clean_txt) > 0 else 0.0
            v_prof["sample_verbatims"] = clean_txt.head(3).tolist()

        variables_profile[snake] = v_prof

    # 3. Article 6a: Straight-Lining Quality Gate (Row SD == 0 across >= 5 Likert items)
    straight_lining_info = {
        "evaluated": False,
        "n_likert_items": len(likert_cols),
        "straight_liners_count": 0,
        "straight_lining_pct": 0.0,
        "sensitivity_max_delta_pct": 0.0,
        "flagged_row_indices": [],
    }
    if len(likert_cols) >= 5:
        likert_df = df[likert_cols].apply(pd.to_numeric, errors="coerce")
        valid_counts = likert_df.notna().sum(axis=1)
        row_stds = likert_df.std(axis=1, ddof=0)
        is_straight = (valid_counts >= 5) & (row_stds == 0.0)
        sl_count = int(is_straight.sum())
        sl_pct = round((sl_count / n_rows * 100.0) if n_rows > 0 else 0.0, 2)

        # Compute sensitivity delta if straight-liners are removed
        max_delta_pct = 0.0
        if 0 < sl_count < n_rows:
            clean_likert_df = likert_df.loc[~is_straight]
            for lcol in likert_cols:
                m_all = likert_df[lcol].mean()
                m_clean = clean_likert_df[lcol].mean()
                if pd.notna(m_all) and pd.notna(m_clean) and m_all != 0:
                    delta_pct = abs(m_clean - m_all) / abs(m_all) * 100.0
                    max_delta_pct = max(max_delta_pct, float(delta_pct))

        straight_lining_info = {
            "evaluated": True,
            "n_likert_items": len(likert_cols),
            "straight_liners_count": sl_count,
            "straight_lining_pct": sl_pct,
            "sensitivity_max_delta_pct": round(max_delta_pct, 2),
            "flagged_row_indices": [int(idx) for idx in df.index[is_straight][:50]],
        }

    # 4. Build setup_segments.csv for primary segment column x top numeric/Likert columns
    primary_segment_col = None
    for c in categorical_cols:
        nunique = df[c].dropna().nunique()
        if 2 <= nunique <= 12:
            primary_segment_col = c
            break

    metric_cols = (likert_cols + numeric_cols)[:6]
    segment_rows = []
    segments_list = []

    if primary_segment_col and metric_cols:
        for seg_val, grp in df.groupby(primary_segment_col, dropna=True):
            seg_name = str(seg_val).strip()
            if not seg_name:
                continue
            segments_list.append(seg_name)
            row_dict = {"segment": seg_name, "n": int(len(grp))}
            # Compute 95% MoE on the first metric for dot plot whiskers
            first_m = pd.to_numeric(grp[metric_cols[0]], errors="coerce").dropna()
            row_dict["moe_95"] = (
                round(1.96 * float(first_m.std(ddof=1)) / math.sqrt(len(first_m)), 3)
                if len(first_m) > 1
                else 0.0
            )
            for mcol in metric_cols:
                ms = pd.to_numeric(grp[mcol], errors="coerce").dropna()
                row_dict[mcol] = round(float(ms.mean()), 2) if len(ms) > 0 else ""
            segment_rows.append(row_dict)

    seg_csv_path = out_dir / "setup_segments.csv"
    if segment_rows:
        pd.DataFrame(segment_rows).to_csv(seg_csv_path, index=False)

    # 5. Write column_mapping.json, 00_profile.json, setup_manifest.json
    col_map_path = out_dir / "column_mapping.json"
    col_map_path.write_text(json.dumps(col_mapping, indent=2, ensure_ascii=False), encoding="utf-8")

    quality_gates = {
        "article_6a_straight_lining": straight_lining_info,
        "article_6b_percentage_sum_check": {
            "passed": len(pct_sum_violations) == 0,
            "violations": pct_sum_violations,
        },
        "article_6c_missingness": {
            "moderate_10_to_20_pct": moderate_missing_cols,
            "high_over_20_pct": high_missing_cols,
        },
    }

    profile_payload = {
        "project": dataset_name,
        "generated_at": datetime.datetime.now().isoformat(),
        "sample_size": n_rows,
        "effective_sample_size": round(n_eff, 1),
        "design_effect_deff": round(deff, 3),
        "weight_column": weight_col,
        "n_columns": n_cols,
        "global_moe_95ci": f"±{global_moe_pct:.2f}%",
        "global_moe_95ci_num": global_moe_pct,
        "primary_segment_column": primary_segment_col,
        "likert_columns": likert_cols,
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "open_text_columns": open_text_cols,
        "quality_gates": quality_gates,
        "variables": variables_profile,
    }
    profile_path = out_dir / "00_profile.json"
    profile_path.write_text(json.dumps(profile_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    manifest_payload = {
        "project": dataset_name,
        "sample_size": n_rows,
        "effective_sample_size": round(n_eff, 1),
        "global_moe_95ci": f"±{global_moe_pct:.2f}%",
        "confidence_level": "95%",
        "metrics_tracked": len(likert_cols) + len(numeric_cols),
        "segments_count": len(segments_list),
        "segments": segments_list,
        "primary_segment_column": primary_segment_col,
        "likert_columns": likert_cols,
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "open_text_columns": open_text_cols,
        "quality_gates_passed": len(pct_sum_violations) == 0,
        "export_date": datetime.date.today().isoformat(),
    }
    manifest_path = out_dir / "setup_manifest.json"
    manifest_path.write_text(json.dumps(manifest_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # 6. Generate Tufte-styled setup_report.md and 00_project_manifest.md
    report_lines = [
        f"# Dataset Setup & Statistical Hygiene Report — {dataset_name}",
        "",
        f"**Total Sample ($N$):** `{n_rows:,}` · **Effective Sample ($N_{{\\text{{eff}}}}$):** `{n_eff:,.1f}` (DEFF = `{deff:.2f}`) · **Global 95% CI MoE:** `±{global_moe_pct:.2f}%`",
        "",
        "> **Margin Note:** Global Margin of Error is computed at the 95% confidence level ($z = 1.96$) under maximum binomial variance ($p = 0.50$). Subgroup margins widen proportionally to $1/\\sqrt{n_{\\text{sub}}}$.",
        "",
        "## 1. Article 6 Data Quality Gates Audit",
        "",
        "| Quality Gate | Constitutional Rule | Result | Audit Diagnostic |",
        "| :--- | :--- | :--- | :--- |",
        f"| **Gate 6a: Straight-Lining** | Row SD $= 0$ across $\\ge 5$ Likert items | `{'EVALUATED' if straight_lining_info['evaluated'] else 'N/A (<5 items)'}` | `{straight_lining_info['straight_liners_count']}` respondents (`{straight_lining_info['straight_lining_pct']}%`) · Sensitivity $\\Delta = {straight_lining_info['sensitivity_max_delta_pct']}%` |",
        f"| **Gate 6b: Percentage Sums** | Category distributions sum to $100\\% \\pm 0.5\\%$ | `{'PASS' if not pct_sum_violations else 'FLAG'}` | `{len(pct_sum_violations)}` violations across `{len(categorical_cols)}` categorical variables |",
        f"| **Gate 6c: Missingness Rate** | Flag variables $>10\\%$ and $>20\\%$ missing | `{'PASS' if not high_missing_cols else 'CAVEAT'}` | `{len(moderate_missing_cols)}` moderate ($>10\\%$), `{len(high_missing_cols)}` high ($>20\\%$) missingness columns |",
        "",
    ]

    if likert_cols or numeric_cols:
        report_lines.extend([
            "## 2. Quantitative & Likert Scale Variable Profile",
            "",
            "| Variable | Role | Valid $N$ | Mean ± 95% MoE | SD | Median (IQR) | Skewness | Top-2-Box % | Estimator |",
            "| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | :--- |",
        ])
        for snake, v in variables_profile.items():
            if v["role"] in ("likert", "numeric", "binary") and "mean" in v:
                t2b_str = f"{v['top2box_pct']:.1f}%" if "top2box_pct" in v else "—"
                report_lines.append(
                    f"| **{v['original_name']}** (`{snake}`) | {v['role']} | {v['n_valid']} | "
                    f"{v['mean']:.2f} (±{v['moe_95']:.2f}) | {v['sd']:.2f} | "
                    f"{v['median']:.2f} ({v['iqr']:.2f}) | {v['skewness']:+.2f} | "
                    f"{t2b_str} | {v['recommended_estimator']} |"
                )
        report_lines.append("")

    if categorical_cols:
        report_lines.extend([
            "## 3. Categorical & Segment Distributions",
            "",
            "| Variable | Valid $N$ | Missing % | Unique Categories | Top Modal Category (Count, % ± 95% MoE) |",
            "| :--- | ---: | ---: | ---: | :--- |",
        ])
        for snake, v in variables_profile.items():
            if v["role"] in ("categorical", "binary") and v.get("categories"):
                top_cat, top_info = next(iter(v["categories"].items()))
                report_lines.append(
                    f"| **{v['original_name']}** (`{snake}`) | {v['n_valid']} | {v['missing_pct']:.1f}% | "
                    f"{v.get('n_unique', len(v['categories']))} | "
                    f"{top_cat} (`n={top_info['count']}`, `{top_info['pct']:.1f}% ±{top_info['moe_95_pct']:.1f}%`) |"
                )
        report_lines.append("")

    if open_text_cols:
        report_lines.extend([
            "## 4. Open-Ended Qualitative Verbatim Channels",
            "",
            "| Open-Text Column | Valid Verbatims ($N$) | Missing % | Mean Length (chars) |",
            "| :--- | ---: | ---: | ---: |",
        ])
        for snake, v in variables_profile.items():
            if v["role"] == "open_text":
                report_lines.append(
                    f"| **{v['original_name']}** (`{snake}`) | {v['n_verbatims']} | {v['missing_pct']:.1f}% | {v['avg_char_length']:.1f} |"
                )
        report_lines.append("")

    report_md = "\n".join(report_lines)
    (out_dir / "setup_report.md").write_text(report_md, encoding="utf-8")
    (out_dir / "00_project_manifest.md").write_text(report_md, encoding="utf-8")

    return profile_payload


def main():
    parser = argparse.ArgumentParser(description="Data-Pro-Skill Quantitative Setup & Profiling Engine")
    parser.add_argument("input", help="Input dataset file (.csv, .xlsx, .ods, .parquet)")
    parser.add_argument("config", nargs="?", default=None, help="Optional domain configuration JSON file")
    parser.add_argument("-o", "--output", default=".dps/outputs/setup", help="Output directory or CSV file path")
    parser.add_argument("--profile", action="store_true", help="Force full /dps-setup profiling mode")
    parser.add_argument("--weight", default=None, help="Optional survey weight column name")
    parser.add_argument("--name", default=None, help="Project / dataset display title")
    parser.add_argument("--json-only", action="store_true", help="Emit JSON profile summary to stdout")
    parser.add_argument("--csv", action="store_true", help="Also export processed dataset CSV")

    args = parser.parse_args()

    try:
        df = load_dataset(args.input)
        config = None
        if args.config and Path(args.config).is_file():
            with open(args.config, "r", encoding="utf-8") as f:
                config = json.load(f)

        out_path = Path(args.output)
        dataset_title = args.name or Path(args.input).stem.replace("_", " ").title()

        # Legacy mode: config provided and output ends with .csv and not --profile
        if config and out_path.suffix.lower() == ".csv" and not args.profile:
            df_processed = calculate_scores(df, config)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            df_processed.to_csv(out_path, index=False)
            print(f"✅ Domain score normalization complete. Saved to {out_path}")
            return

        # Full /dps-setup profiling mode
        target_dir = out_path.parent if out_path.suffix else out_path
        profile = profile_dataset(
            df,
            target_dir,
            weight_col=args.weight,
            config=config,
            dataset_name=dataset_title,
        )
        if args.csv:
            df.to_csv(target_dir / "processed_dataset.csv", index=False)

        if args.json_only:
            print(json.dumps({
                "sample_size": profile["sample_size"],
                "global_moe_95ci": profile["global_moe_95ci"],
                "likert_columns": profile["likert_columns"],
                "categorical_columns": profile["categorical_columns"],
                "open_text_columns": profile["open_text_columns"],
            }, indent=2, ensure_ascii=False))
        else:
            print(
                f"✅ Setup profiling complete in {target_dir} "
                f"(N={profile['sample_size']}, MoE={profile['global_moe_95ci']}, "
                f"{len(profile['likert_columns'])} Likert, {len(profile['categorical_columns'])} Categorical, "
                f"{len(profile['open_text_columns'])} Open-Text)"
            )

    except Exception as e:
        print(f"❌ Error during quantitative setup: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
