#!/usr/bin/env python3
"""Data-Pro-Skill Cross-Tabulation, Hypothesis Testing & Effect-Size Engine.

Implements:
  - Article 7c: Branching Overlap validation (detects 0x0 skip-logic conflicts)
  - Article 2 & 3: Automatic parametric & non-parametric hypothesis testing with effect sizes:
      * Chi-Square (χ²) + Cramér's V + Standardized Residuals (z_ij = (O - E)/sqrt(E))
      * Fisher's Exact test (2x2 tables with expected cell < 5)
      * Welch's t-test + Cohen's d + Mann-Whitney U (2-group metric comparison)
      * One-Way ANOVA F + Eta-Squared (η²) + Kruskal-Wallis H + Epsilon-Squared (ε²) (k-group comparison)
      * Dual Correlation: Pearson r + Spearman ρ + non-linearity divergence flag (|r - ρ| > 0.10)
  - Article 1 & 4: 95% CI (±MoE%) on every cell and N < 30 small-sample enforcement
  - Autonomous Multi-Cross Execution (--execute-all) with an Effect-Size Leaderboard
"""

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


# ==============================================================================
# LEGACY FUNCTIONS (Preserved for backwards compatibility)
# ==============================================================================

def weighted_crosstab(df, index_col, columns_col, weight_col="weight", normalize=True):
    """Generates a weighted crosstab."""
    if not weight_col or weight_col not in df.columns:
        weights = np.ones(len(df))
    else:
        weights = pd.to_numeric(df[weight_col], errors="coerce").fillna(1.0)

    ct = pd.crosstab(
        index=df[index_col],
        columns=df[columns_col],
        values=weights,
        aggfunc="sum",
        normalize=normalize,
    )
    if normalize:
        ct = ct * 100
    return ct


def run_automated_crosstabs(df, target_cols, banner_cols, weight_col="weight", output_dir="output"):
    """Runs a banner (demographic splits) against a list of target questions."""
    os.makedirs(output_dir, exist_ok=True)
    for var in target_cols:
        for banner in banner_cols:
            try:
                ct = weighted_crosstab(df, var, banner, weight_col)
                safe_var = re.sub(r"[^a-zA-Z0-9_-]", "_", str(var))[:25]
                safe_banner = re.sub(r"[^a-zA-Z0-9_-]", "_", str(banner))[:25]
                filename = f"{output_dir}/Example_{safe_var}_by_{safe_banner}.csv"
                ct.to_csv(filename)
            except Exception as e:
                print(f"Skipping {var} x {banner}: {e}")


# ==============================================================================
# HELPERS & COLUMN RESOLUTION
# ==============================================================================

def _load_df(path):
    p = Path(path)
    ext = p.suffix.lower()
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(p)
    if ext == ".ods":
        return pd.read_excel(p, engine="odf")
    if ext == ".parquet":
        return pd.read_parquet(p)
    for enc in ("utf-8", "utf-8-sig", "latin1", "cp1252"):
        try:
            return pd.read_csv(p, encoding=enc)
        except Exception:
            continue
    return pd.read_csv(p)


def _resolve_col(df, col_query, mapping_dir=None):
    """Resolve column name by exact match, case-insensitive match, or snake_case mapping."""
    if col_query in df.columns:
        return col_query
    q_low = str(col_query).strip().lower()
    for c in df.columns:
        if str(c).strip().lower() == q_low:
            return c
    # Try snake_case match
    for c in df.columns:
        snake = re.sub(r"[^a-zA-Z0-9]+", "_", str(c).lower()).strip("_")
        if snake == q_low or snake.startswith(q_low):
            return c
    # Check column_mapping.json if present
    if mapping_dir:
        map_file = Path(mapping_dir) / "column_mapping.json"
        if map_file.exists():
            try:
                cmap = json.loads(map_file.read_text(encoding="utf-8"))
                if col_query in cmap:
                    orig = cmap[col_query].get("original_name")
                    if orig in df.columns:
                        return orig
            except Exception:
                pass
    raise KeyError(f"Column '{col_query}' not found in dataset columns: {list(df.columns)}")


def _safe_slug(text, max_len=28):
    s = re.sub(r"[^a-zA-Z0-9]+", "_", str(text)).strip("_")
    return s[:max_len] if s else "var"


def _interpret_cramers_v(v):
    if v < 0.10:
        return "negligible"
    if v < 0.30:
        return "small-to-moderate"
    if v < 0.50:
        return "moderate-to-strong"
    return "strong"


def _interpret_cohens_d(d):
    ad = abs(d)
    if ad < 0.20:
        return "negligible"
    if ad < 0.50:
        return "small"
    if ad < 0.80:
        return "medium"
    return "large"


def _interpret_eta_sq(eta):
    if eta < 0.01:
        return "negligible"
    if eta < 0.06:
        return "small"
    if eta < 0.14:
        return "medium"
    return "large"


# ==============================================================================
# CORE CROSSTAB & HYPOTHESIS TESTING ENGINE
# ==============================================================================

def run_crosstab_analysis(
    df,
    index_col,
    columns_col,
    output_dir=".dps/outputs/cross",
    weight_col=None,
    test="auto",
    normalize="index",
):
    """Execute a rigorous cross-tabulation with Article 1-7 statistical guarantees."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    x_col = _resolve_col(df, index_col, out_dir.parent / "setup")
    y_col = _resolve_col(df, columns_col, out_dir.parent / "setup")
    slug_x = _safe_slug(x_col)
    slug_y = _safe_slug(y_col)
    base_name = f"cross_{slug_x}_{slug_y}"

    # Article 7c: Branching Overlap Validation
    sub = df[[x_col, y_col]].copy()
    if weight_col and weight_col in df.columns:
        sub["_w"] = pd.to_numeric(df[weight_col], errors="coerce").fillna(1.0)
    else:
        sub["_w"] = 1.0

    # Filter out blanks / NaNs
    mask_x = sub[x_col].notna() & (sub[x_col].astype(str).str.strip() != "") & (sub[x_col].astype(str).str.lower() != "nan")
    mask_y = sub[y_col].notna() & (sub[y_col].astype(str).str.strip() != "") & (sub[y_col].astype(str).str.lower() != "nan")
    valid = sub[mask_x & mask_y].copy()

    n_total = len(df)
    n_valid = len(valid)

    if n_valid == 0:
        err_payload = {
            "index": x_col,
            "columns": y_col,
            "n_total": n_total,
            "n_valid": 0,
            "skip_logic_conflict": True,
            "error": "0x0 Structural Branching Overlap: Variables belong to mutually exclusive skip-logic branches.",
        }
        (out_dir / f"{base_name}_stats.json").write_text(json.dumps(err_payload, indent=2, ensure_ascii=False), encoding="utf-8")
        (out_dir / f"{base_name}_report.md").write_text(
            f"# Cross-Tabulation Skipped: {x_col} × {y_col}\n\n"
            f"> **Margin Note:** **Article 7c (Branching Overlap Gate):** Joint valid sample is $N = 0$ out of $N_{{\\text{{total}}}} = {n_total}$. "
            f"`{x_col}` and `{y_col}` belong to mutually exclusive questionnaire skip-logic branches.\n",
            encoding="utf-8",
        )
        return err_payload

    # Contingency table (raw counts & weighted percentages)
    ct_counts = pd.crosstab(valid[x_col], valid[y_col])
    ct_pct = pd.crosstab(
        valid[x_col],
        valid[y_col],
        values=valid["_w"],
        aggfunc="sum",
        normalize=normalize if normalize in ("index", "columns", "all") else "index",
    ) * 100.0

    row_totals = ct_counts.sum(axis=1)
    col_totals = ct_counts.sum(axis=0)
    grand_total = int(ct_counts.values.sum())

    # Chi-Square test, Cramér's V, and Standardized Residuals z_ij = (O - E) / sqrt(E)
    obs = ct_counts.values.astype(float)
    r_num, c_num = obs.shape
    if r_num >= 2 and c_num >= 2 and grand_total > 0:
        chi2_val, p_chi2, dof, expected = stats.chi2_contingency(obs, correction=False)
        with np.errstate(divide="ignore", invalid="ignore"):
            z_resid = np.where(expected > 0, (obs - expected) / np.sqrt(expected), 0.0)
        min_dim = min(r_num - 1, c_num - 1)
        cramers_v = float(math.sqrt(chi2_val / (grand_total * min_dim))) if (grand_total * min_dim) > 0 else 0.0
        low_expected_cells = int((expected < 5.0).sum())
        low_expected_pct = round(low_expected_cells / expected.size * 100.0, 1)
        fisher_p = None
        if r_num == 2 and c_num == 2 and low_expected_cells > 0:
            _, fisher_p = stats.fisher_exact(obs)
    else:
        chi2_val, p_chi2, dof = 0.0, 1.0, 0
        expected = obs.copy()
        z_resid = np.zeros_like(obs)
        cramers_v = 0.0
        low_expected_cells = 0
        low_expected_pct = 0.0
        fisher_p = None

    residuals_df = pd.DataFrame(
        np.round(z_resid, 3),
        index=[str(i) for i in ct_counts.index],
        columns=[str(c) for c in ct_counts.columns],
    )

    # Identify significant residual cells (|z| >= 1.96)
    sig_cells = []
    for i, r_lbl in enumerate(ct_counts.index):
        for j, c_lbl in enumerate(ct_counts.columns):
            z_val = float(z_resid[i, j])
            if abs(z_val) >= 1.96:
                sig_cells.append({
                    "row": str(r_lbl),
                    "col": str(c_lbl),
                    "observed": int(obs[i, j]),
                    "expected": round(float(expected[i, j]), 1),
                    "row_pct": round(float(ct_pct.iloc[i, j]), 1),
                    "z_residual": round(z_val, 2),
                    "direction": "over-indexed" if z_val > 0 else "under-indexed",
                })
    sig_cells.sort(key=lambda item: abs(item["z_residual"]), reverse=True)

    # Group comparison tests if Y (or X) is numeric/Likert
    y_num = pd.to_numeric(valid[y_col], errors="coerce")
    x_num = pd.to_numeric(valid[x_col], errors="coerce")
    group_test_info = {}
    segment_metric_rows = []
    dual_corr_info = {}

    # Check if both are numeric -> Dual Correlation (Pearson r + Spearman rho)
    if y_num.notna().mean() >= 0.85 and x_num.notna().mean() >= 0.85 and x_num.nunique() >= 3 and y_num.nunique() >= 3:
        pair_df = pd.DataFrame({"x": x_num, "y": y_num}).dropna()
        if len(pair_df) >= 5:
            r_val, p_r = stats.pearsonr(pair_df["x"], pair_df["y"])
            rho_val, p_rho = stats.spearmanr(pair_df["x"], pair_df["y"])
            diff = abs(float(r_val) - float(rho_val))
            dual_corr_info = {
                "pearson_r": round(float(r_val), 4),
                "pearson_p": float(p_r),
                "spearman_rho": round(float(rho_val), 4),
                "spearman_p": float(p_rho),
                "divergence_abs": round(diff, 4),
                "non_linear_monotonic_flag": diff > 0.10,
            }

    # Check if X is categorical segment and Y is numeric/Likert metric
    if y_num.notna().mean() >= 0.85 and 2 <= valid[x_col].nunique() <= 15:
        valid_num = valid.assign(_y_num=y_num).dropna(subset=["_y_num"])
        groups = []
        for seg_val, grp in valid_num.groupby(x_col):
            vals = grp["_y_num"].values
            n_g = len(vals)
            if n_g == 0:
                continue
            groups.append((str(seg_val), vals))
            m_g = float(np.mean(vals))
            sd_g = float(np.std(vals, ddof=1)) if n_g > 1 else 0.0
            moe_g = 1.96 * sd_g / math.sqrt(n_g) if n_g > 1 else 0.0
            q25, med_g, q75 = [float(v) for v in np.percentile(vals, [25, 50, 75])]
            segment_metric_rows.append({
                "segment": str(seg_val),
                "n": int(n_g),
                "small_sample_flag": n_g < 30,
                "mean": round(m_g, 2),
                "sd": round(sd_g, 2),
                "moe_95": round(moe_g, 2),
                "median": round(med_g, 2),
                "iqr": round(q75 - q25, 2),
            })

        if len(groups) == 2 and len(groups[0][1]) >= 2 and len(groups[1][1]) >= 2:
            g1, g2 = groups[0][1], groups[1][1]
            t_stat, p_t = stats.ttest_ind(g1, g2, equal_var=False)
            u_stat, p_u = stats.mannwhitneyu(g1, g2, alternative="two-sided")
            # Pooled SD for Cohen's d
            n1, n2 = len(g1), len(g2)
            s1, s2 = np.var(g1, ddof=1), np.var(g2, ddof=1)
            pooled_sd = math.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / max(1, n1 + n2 - 2))
            cohens_d = float((np.mean(g1) - np.mean(g2)) / pooled_sd) if pooled_sd > 0 else 0.0
            group_test_info = {
                "parametric_test": "Welch's t-test",
                "t_stat": round(float(t_stat), 3),
                "p_value_parametric": float(p_t),
                "effect_size_name": "Cohen's d",
                "effect_size": round(cohens_d, 3),
                "effect_magnitude": _interpret_cohens_d(cohens_d),
                "non_parametric_test": "Mann-Whitney U",
                "u_stat": round(float(u_stat), 1),
                "p_value_non_parametric": float(p_u),
            }
        elif len(groups) >= 3 and all(len(g[1]) >= 2 for g in groups):
            arrays = [g[1] for g in groups]
            f_stat, p_f = stats.f_oneway(*arrays)
            h_stat, p_h = stats.kruskal(*arrays)
            all_vals = np.concatenate(arrays)
            grand_mean = np.mean(all_vals)
            ss_total = float(np.sum((all_vals - grand_mean) ** 2))
            ss_between = float(sum(len(a) * ((np.mean(a) - grand_mean) ** 2) for a in arrays))
            eta_sq = ss_between / ss_total if ss_total > 0 else 0.0
            n_tot_g = len(all_vals)
            eps_sq = float(h_stat / ((n_tot_g ** 2 - 1) / (n_tot_g + 1))) if n_tot_g > 1 else 0.0
            group_test_info = {
                "parametric_test": "One-Way ANOVA (F)",
                "f_stat": round(float(f_stat), 3),
                "p_value_parametric": float(p_f),
                "effect_size_name": "Eta-Squared (η²)",
                "effect_size": round(eta_sq, 4),
                "effect_magnitude": _interpret_eta_sq(eta_sq),
                "non_parametric_test": "Kruskal-Wallis (H)",
                "h_stat": round(float(h_stat), 3),
                "p_value_non_parametric": float(p_h),
                "epsilon_squared": round(eps_sq, 4),
            }

    # Save CSVs
    ct_combined = ct_pct.round(1).copy()
    ct_combined["Row_N"] = row_totals
    ct_combined.to_csv(out_dir / f"{base_name}.csv")
    residuals_df.to_csv(out_dir / f"{base_name}_residuals.csv")

    primary_p = fisher_p if fisher_p is not None else float(p_chi2)
    if group_test_info and group_test_info.get("p_value_parametric") is not None:
        primary_p = min(primary_p, float(group_test_info["p_value_parametric"]))

    stats_payload = {
        "index": x_col,
        "columns": y_col,
        "n_total": n_total,
        "n_valid": grand_total,
        "skip_logic_conflict": False,
        "chi2": round(float(chi2_val), 3),
        "dof": int(dof),
        "p_value": round(float(primary_p), 6),
        "p_value_chi2": round(float(p_chi2), 6),
        "fisher_exact_p": round(float(fisher_p), 6) if fisher_p is not None else None,
        "cramers_v": round(cramers_v, 4),
        "cramers_v_magnitude": _interpret_cramers_v(cramers_v),
        "low_expected_cells_count": low_expected_cells,
        "low_expected_cells_pct": low_expected_pct,
        "significant_residual_cells": sig_cells[:10],
        "group_comparison": group_test_info,
        "segment_metric_summary": segment_metric_rows,
        "dual_correlation": dual_corr_info,
        "standardized_residuals": {
            "rows": [str(i) for i in ct_counts.index],
            "cols": [str(c) for c in ct_counts.columns],
            "z_matrix": residuals_df.values.tolist(),
        },
    }
    (out_dir / f"{base_name}_stats.json").write_text(
        json.dumps(stats_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Build Tufte Markdown Report (cross_{X}_{Y}_report.md)
    sig_badge = "STATISTICALLY SIGNIFICANT ($p < 0.05$)" if primary_p < 0.05 else "NO SIGNIFICANT DIFFERENCE ($p \\ge 0.05$ — Null Finding)"
    md_lines = [
        f"# Cross-Tabulation: {x_col} × {y_col}",
        "",
        f"**Verdict:** **{sig_badge}** — $\\chi^2({dof}, N={grand_total}) = {chi2_val:.2f}, p = {p_chi2:.4f}$, **Cramér's $V = {cramers_v:.3f}$** ({_interpret_cramers_v(cramers_v)} effect).",
        "",
    ]

    if group_test_info:
        md_lines.append(
            f"**Parametric / Non-Parametric Metric Test:** {group_test_info['parametric_test']} = `{group_test_info.get('t_stat', group_test_info.get('f_stat'))}`, "
            f"$p = {group_test_info['p_value_parametric']:.4f}$, **{group_test_info['effect_size_name']} = `{group_test_info['effect_size']}`** ({group_test_info['effect_magnitude']}) · "
            f"{group_test_info['non_parametric_test']} $p = {group_test_info['p_value_non_parametric']:.4f}$."
        )
        md_lines.append("")

    if dual_corr_info:
        md_lines.append(
            f"**Dual Correlation:** Pearson $r = {dual_corr_info['pearson_r']:+.3f}$ ($p = {dual_corr_info['pearson_p']:.4f}$) · "
            f"Spearman $\\rho = {dual_corr_info['spearman_rho']:+.3f}$ ($p = {dual_corr_info['spearman_p']:.4f}$) · "
            f"Divergence $|\\Delta| = {dual_corr_info['divergence_abs']:.3f}$ "
            f"({'⚠ Non-linear/outlier sensitivity detected' if dual_corr_info['non_linear_monotonic_flag'] else 'Linear alignment confirmed'})."
        )
        md_lines.append("")

    # Margin note with diagnostics
    caveat_txt = (
        f"Warning: {low_expected_cells} cells ({low_expected_pct}%) have expected count E_ij < 5."
        if low_expected_pct > 20.0
        else "All expected cell frequencies satisfy Cochran's rule."
    )
    md_lines.extend([
        f"> **Margin Note:** Joint valid sample $N = {grand_total}$ (out of $N_{{\\text{{total}}}} = {n_total}$). "
        f"$\\chi^2 = {chi2_val:.2f}, p = {p_chi2:.4f}$, Cramér's $V = {cramers_v:.3f}$. {caveat_txt}",
        "",
        "## 1. Contingency Table (Row % ± 95% CI MoE & Subgroup $N$)",
        "",
    ])

    # Build Booktabs Contingency Table (Article 4 compliant: if row_N < 30, show raw count "n of N")
    col_headers = [str(c) for c in ct_counts.columns]
    header_row = "| " + str(x_col) + " | Subgroup $N$ | ±MoE (95% CI) | " + " | ".join(col_headers) + " |"
    align_row = "| :--- | ---: | ---: | " + " | ".join(["---:" for _ in col_headers]) + " |"
    md_lines.extend([header_row, align_row])

    for i, r_lbl in enumerate(ct_counts.index):
        r_n = int(row_totals.iloc[i])
        r_moe = 1.96 * math.sqrt(0.25 / r_n) * 100.0 if r_n > 0 else 0.0
        n_cell = f"{r_n} *(SMALL SAMPLE)*" if r_n < 30 else f"{r_n}"
        moe_cell = "—" if r_n < 30 else f"±{r_moe:.1f}%"
        row_cells = []
        for j, c_lbl in enumerate(ct_counts.columns):
            cnt = int(obs[i, j])
            pct = float(ct_pct.iloc[i, j])
            z_v = float(z_resid[i, j])
            star = "**" if abs(z_v) >= 1.96 else ""
            if r_n < 30:
                # Article 4: raw counts only for N < 30
                row_cells.append(f"{star}{cnt} of {r_n}{star}")
            else:
                row_cells.append(f"{star}{pct:.1f}% ({cnt}){star}")
        md_lines.append(f"| **{r_lbl}** | {n_cell} | {moe_cell} | " + " | ".join(row_cells) + " |")

    # Total row
    tot_moe = 1.96 * math.sqrt(0.25 / grand_total) * 100.0 if grand_total > 0 else 0.0
    tot_cells = [f"{(col_totals.iloc[j] / grand_total * 100.0):.1f}% ({int(col_totals.iloc[j])})" for j in range(len(col_headers))]
    md_lines.append(f"| **Total / Base** | {grand_total} | ±{tot_moe:.1f}% | " + " | ".join(tot_cells) + " |")
    md_lines.append("")

    # Segment metric summary table + Mermaid chart if available
    if segment_metric_rows:
        md_lines.extend([
            f"## 2. Segment Performance on `{y_col}` (Parametric & Non-Parametric)",
            "",
            f"| {x_col} Segment | $N$ | Mean ± 95% MoE | SD | Median (IQR) | Sample Status |",
            "| :--- | ---: | ---: | ---: | ---: | :--- |",
        ])
        for sr in segment_metric_rows:
            status = "SMALL SAMPLE (<30)" if sr["small_sample_flag"] else "Adequate (≥30)"
            md_lines.append(
                f"| **{sr['segment']}** | {sr['n']} | {sr['mean']:.2f} (±{sr['moe_95']:.2f}) | "
                f"{sr['sd']:.2f} | {sr['median']:.2f} ({sr['iqr']:.2f}) | {status} |"
            )
        md_lines.append("")

        # Add Mermaid xychart-beta block (automatically compiled to Tufte SVG by tufte_html.py)
        chart_labels = ", ".join(f'"{sr["segment"][:20]}"' for sr in segment_metric_rows)
        chart_vals = ", ".join(f'{sr["mean"]:.2f}' for sr in segment_metric_rows)
        md_lines.extend([
            "```mermaid",
            "xychart-beta",
            f'  title "Mean {y_col} by {x_col}"',
            f"  x-axis [{chart_labels}]",
            f'  y-axis "Mean {y_col}"',
            f"  bar [{chart_vals}]",
            "```",
            "",
        ])

    # Standardized Residuals Table (z_ij)
    if sig_cells:
        md_lines.extend([
            "## 3. Significant Cell Deviations — Standardized Residuals ($|z_{ij}| \\ge 1.96$)",
            "",
            "| Segment Row | Outcome Column | Observed ($O_{ij}$) | Expected ($E_{ij}$) | Row % | Residual ($z_{ij}$) | Direction |",
            "| :--- | :--- | ---: | ---: | ---: | ---: | :--- |",
        ])
        for sc in sig_cells[:8]:
            md_lines.append(
                f"| **{sc['row']}** | {sc['col']} | {sc['observed']} | {sc['expected']:.1f} | "
                f"{sc['row_pct']:.1f}% | **{sc['z_residual']:+.2f}** | {sc['direction']} |"
            )
        md_lines.append("")

    (out_dir / f"{base_name}_report.md").write_text("\n".join(md_lines), encoding="utf-8")
    return stats_payload


def execute_all_crosstabs(df, output_dir=".dps/outputs/cross", weight_col=None, max_pairs=12):
    """Autonomously discover and execute the highest-value Segment x Metric crosstabs (/dps-execute)."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Identify segment columns (2 to 10 unique values) and metric/outcome columns
    segment_cols = []
    metric_cols = []
    for col in df.columns:
        s = df[col].dropna()
        if len(s) == 0:
            continue
        num_s = pd.to_numeric(s, errors="coerce").dropna()
        uniq = s.nunique()
        if len(num_s) / len(s) >= 0.85 and 2 <= num_s.nunique() <= 11:
            metric_cols.append(col)
        elif 2 <= uniq <= 10 and str(col).lower() not in ("id", "respondent_id"):
            segment_cols.append(col)

    if not segment_cols and len(metric_cols) >= 2:
        segment_cols = [metric_cols[0]]
        metric_cols = metric_cols[1:]

    results = []
    pairs_run = 0
    for seg in segment_cols[:4]:
        for met in metric_cols[:5]:
            if seg == met or pairs_run >= max_pairs:
                continue
            res = run_crosstab_analysis(df, seg, met, output_dir=out_dir, weight_col=weight_col)
            if not res.get("skip_logic_conflict"):
                results.append(res)
                pairs_run += 1

    # Rank by Cramér's V / effect size for the Effect-Size Leaderboard
    results.sort(key=lambda r: (r.get("p_value", 1.0) < 0.05, r.get("cramers_v", 0.0)), reverse=True)

    summary_lines = [
        "# Autonomous Cross-Tabulation Synthesis & Effect-Size Leaderboard",
        "",
        f"**Executed Cross-Tabulations:** `{len(results)}` · **Statistically Significant ($p < 0.05$):** `{sum(1 for r in results if r['p_value'] < 0.05)}`",
        "",
        "> **Margin Note:** Findings are ranked by statistical significance ($p < 0.05$) and effect magnitude (Cramér's $V$ and group effect size) in accordance with Articles 2, 3, and 5 of the Data-Pro-Skill Constitution.",
        "",
        "## Effect-Size Leaderboard",
        "",
        "| Rank | Segment ($X$) | Outcome Metric ($Y$) | Valid $N$ | $\\chi^2$ $p$-value | Cramér's $V$ | Parametric Effect Size | Verdict |",
        "| ---: | :--- | :--- | ---: | ---: | ---: | :--- | :--- |",
    ]
    for idx, r in enumerate(results, 1):
        gc = r.get("group_comparison") or {}
        eff_str = f"{gc.get('effect_size_name', '—')}: {gc.get('effect_size', '—')}" if gc else "—"
        verdict = "**Significant**" if r["p_value"] < 0.05 else "Null ($p \\ge 0.05$)"
        summary_lines.append(
            f"| {idx} | **{r['index']}** | **{r['columns']}** | {r['n_valid']} | "
            f"`{r['p_value']:.4f}` | `{r['cramers_v']:.3f}` ({r['cramers_v_magnitude']}) | {eff_str} | {verdict} |"
        )
    summary_lines.append("")

    (out_dir / "execute_summary.md").write_text("\n".join(summary_lines), encoding="utf-8")
    (out_dir / "execute_leaderboard.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    return results


def main():
    parser = argparse.ArgumentParser(description="Data-Pro-Skill Cross-Tabulation & Hypothesis Testing CLI")
    parser.add_argument("input", help="Input dataset file (.csv, .xlsx, .ods, .parquet)")
    parser.add_argument("--index", "-x", default=None, help="Row/Segment variable name")
    parser.add_argument("--columns", "-y", default=None, help="Column/Outcome variable name")
    parser.add_argument("--weight", "-w", default=None, help="Optional weight column name")
    parser.add_argument("--test", default="auto", help="Statistical test (auto, chi2, fisher, t_test, anova, kruskal)")
    parser.add_argument("--normalize", default="index", choices=["index", "columns", "all"], help="Normalization axis")
    parser.add_argument("--execute-all", action="store_true", help="Autonomously run top Segment x Metric crosstabs")
    parser.add_argument("-o", "--output", default=".dps/outputs/cross", help="Output directory")

    args = parser.parse_args()

    try:
        df = _load_df(args.input)
        if args.execute_all or (not args.index and not args.columns):
            res = execute_all_crosstabs(df, output_dir=args.output, weight_col=args.weight)
            print(f"✅ Executed {len(res)} cross-tabulations in {args.output} (Effect-Size Leaderboard written)")
        else:
            if not args.index or not args.columns:
                raise ValueError("Please specify both --index <X> and --columns <Y>, or use --execute-all.")
            res = run_crosstab_analysis(
                df,
                args.index,
                args.columns,
                output_dir=args.output,
                weight_col=args.weight,
                test=args.test,
                normalize=args.normalize,
            )
            if res.get("skip_logic_conflict"):
                print(f"⚠ Skip-logic conflict (0x0 overlap) between {args.index} and {args.columns}")
            else:
                print(
                    f"✅ Crosstab {res['index']} × {res['columns']} complete "
                    f"(N={res['n_valid']}, p={res['p_value']:.4f}, Cramér's V={res['cramers_v']:.3f})"
                )
    except Exception as e:
        print(f"❌ Error during crosstab analysis: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
