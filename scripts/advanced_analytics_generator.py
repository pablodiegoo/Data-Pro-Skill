#!/usr/bin/env python3
"""Data-Pro-Skill Advanced Survey Science & Psychometrics Engine (/dps-advanced).

Executes the 6 advanced analytical methodologies from references/analysis/:
  1. Pure Sentiment Stack: Ipsative Centering (X_ij - X_bar_i) & Regression Halo Removal Residuals
  2. Priority Action Matrix: Derived Importance x Performance & Priority Score = Imp * (Scale_max - Perf)
  3. Key Driver Analysis & Expectation Residuals: Standardized OLS + Non-Linear Driver Importance + Disappointed/Aligned/Delighted
  4. Dual Correlation Matrix: Side-by-side Pearson r (linear) vs. Spearman rho (monotonic rank)
  5. Dual Clustering & Psychometrics: Silhouette-optimized K-Means Personas + DBSCAN Outlier (-1) detection
     + Multi-Pass PCA/Factor Analysis + Cronbach's Alpha (α) internal consistency
  6. TURF (Total Unduplicated Reach & Frequency): Greedy incremental reach optimization

Zero fragile dependencies: Automatically uses scikit-learn when available, or falls back seamlessly
to exact NumPy/SciPy linear algebra (SVD PCA, lstsq OLS, Lloyd's K-Means, Silhouette, and Euclidean DBSCAN).
"""

import argparse
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

COLUMN_MAPPING_PATH = ".agent/references/column_mapping.json"


# ==============================================================================
# PURE NUMPY / SCIPY FALLBACK ALGORITHMS (Zero-dependency resilience)
# ==============================================================================

def _standardize(X):
    """Z-score standardize a 2D numpy array along axis 0."""
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0, ddof=0)
    std = np.where(std > 1e-9, std, 1.0)
    return (X - mean) / std


def _ols_fit_predict(X, y):
    """Fit ordinary least squares y = a + X*b via np.linalg.lstsq; return (coef, intercept, y_pred, r2)."""
    X_mat = np.column_stack([np.ones(len(X)), X])
    theta, _, _, _ = np.linalg.lstsq(X_mat, y, rcond=None)
    intercept = float(theta[0])
    coef = theta[1:]
    y_pred = X_mat @ theta
    ss_res = float(np.sum((y - y_pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = max(0.0, 1.0 - (ss_res / ss_tot)) if ss_tot > 1e-9 else 0.0
    return coef, intercept, y_pred, r2


def _compute_silhouette_np(X, labels):
    """Compute mean Silhouette Score in pure NumPy."""
    unique_labels = np.unique(labels)
    if len(unique_labels) < 2 or len(X) < 3:
        return 0.0
    # Pairwise Euclidean distance matrix
    diff = X[:, np.newaxis, :] - X[np.newaxis, :, :]
    dist_mat = np.sqrt(np.sum(diff ** 2, axis=-1))
    n = len(X)
    sil_scores = np.zeros(n)
    for i in range(n):
        own_cluster = labels[i]
        own_mask = (labels == own_cluster)
        own_Mask_excl = own_mask.copy()
        own_Mask_excl[i] = False
        if np.any(own_Mask_excl):
            a_i = float(np.mean(dist_mat[i, own_Mask_excl]))
        else:
            a_i = 0.0
        b_i = float("inf")
        for c in unique_labels:
            if c == own_cluster:
                continue
            other_mask = (labels == c)
            if np.any(other_mask):
                b_i = min(b_i, float(np.mean(dist_mat[i, other_mask])))
        denom = max(a_i, b_i)
        sil_scores[i] = (b_i - a_i) / denom if denom > 1e-9 else 0.0
    return float(np.mean(sil_scores))


def _kmeans_np(X, k=3, random_state=42, n_init=10, max_iter=60):
    """Lloyd's K-Means with k-means++ initialization in pure NumPy."""
    rng = np.random.default_rng(random_state)
    n_samples, n_features = X.shape
    best_labels = np.zeros(n_samples, dtype=int)
    best_inertia = float("inf")

    for _ in range(n_init):
        # k-means++ initialization
        centers = np.empty((k, n_features), dtype=float)
        first_idx = int(rng.integers(0, n_samples))
        centers[0] = X[first_idx]
        for c_id in range(1, k):
            dists_sq = np.min(np.sum((X[:, None, :] - centers[None, :c_id, :]) ** 2, axis=-1), axis=1)
            probs = dists_sq / (np.sum(dists_sq) if np.sum(dists_sq) > 0 else 1.0)
            next_idx = int(rng.choice(n_samples, p=probs))
            centers[c_id] = X[next_idx]

        labels = np.zeros(n_samples, dtype=int)
        for _ in range(max_iter):
            dists = np.sum((X[:, None, :] - centers[None, :, :]) ** 2, axis=-1)
            new_labels = np.argmin(dists, axis=1)
            if np.array_equal(new_labels, labels):
                break
            labels = new_labels
            for c_id in range(k):
                mask = labels == c_id
                if np.any(mask):
                    centers[c_id] = np.mean(X[mask], axis=0)

        inertia = float(np.sum((X - centers[labels]) ** 2))
        if inertia < best_inertia:
            best_inertia = inertia
            best_labels = labels.copy()

    return best_labels


def _dbscan_np(X, eps=1.2, min_samples=5):
    """Density-Based Spatial Clustering of Applications with Noise (DBSCAN) in pure NumPy."""
    n = len(X)
    diff = X[:, np.newaxis, :] - X[np.newaxis, :, :]
    dist_mat = np.sqrt(np.sum(diff ** 2, axis=-1))
    neighbors = [np.where(dist_mat[i] <= eps)[0] for i in range(n)]
    labels = np.full(n, -1, dtype=int)
    visited = np.zeros(n, dtype=bool)
    cluster_id = 0

    for i in range(n):
        if visited[i]:
            continue
        visited[i] = True
        nbs = neighbors[i]
        if len(nbs) < min_samples:
            labels[i] = -1
        else:
            labels[i] = cluster_id
            queue = list(nbs)
            idx = 0
            while idx < len(queue):
                q = queue[idx]
                idx += 1
                if not visited[q]:
                    visited[q] = True
                    q_nbs = neighbors[q]
                    if len(q_nbs) >= min_samples:
                        for nb in q_nbs:
                            if nb not in queue:
                                queue.append(nb)
                if labels[q] == -1:
                    labels[q] = cluster_id
            cluster_id += 1

    return labels


def _pca_np(X_std, n_components=3):
    """Principal Component Analysis via Singular Value Decomposition (SVD) in pure NumPy."""
    X_centered = X_std - np.mean(X_std, axis=0)
    u, s, vt = np.linalg.svd(X_centered, full_matrices=False)
    eigvals = (s ** 2) / max(1, len(X_std) - 1)
    total_var = float(np.sum(eigvals))
    explained_ratio = (eigvals / total_var) if total_var > 0 else np.zeros_like(eigvals)
    return vt[:n_components], explained_ratio[:n_components]


def _load_df(df_path):
    p = Path(df_path)
    ext = p.suffix.lower()
    if ext == ".parquet":
        return pd.read_parquet(p)
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(p)
    if ext == ".ods":
        return pd.read_excel(p, engine="odf")
    for enc in ("utf-8", "utf-8-sig", "latin1", "cp1252"):
        try:
            return pd.read_csv(p, encoding=enc)
        except Exception:
            continue
    return pd.read_csv(p)


def compute_cronbach_alpha(df_items):
    """Compute Cronbach's Alpha (α) internal consistency reliability across scale items."""
    clean = df_items.apply(pd.to_numeric, errors="coerce").dropna()
    k = clean.shape[1]
    if k < 2 or len(clean) < 3:
        return 0.0
    item_vars = clean.var(axis=0, ddof=1).sum()
    total_scores = clean.sum(axis=1)
    total_var = total_scores.var(ddof=1)
    if total_var <= 0:
        return 0.0
    alpha = (k / (k - 1.0)) * (1.0 - (item_vars / total_var))
    return float(max(-1.0, min(1.0, alpha)))


def interpret_cronbach_alpha(alpha):
    if alpha >= 0.90:
        return "Excellent (≥ 0.90 — check redundancy)"
    if alpha >= 0.80:
        return "Good (0.80–0.89)"
    if alpha >= 0.70:
        return "Acceptable (0.70–0.79)"
    if alpha >= 0.60:
        return "Questionable (0.60–0.69)"
    return "Low / Heterogeneous (< 0.60)"


def run_advanced_survey_analytics(
    df_path,
    target_col=None,
    report_dir=".dps/outputs/advanced",
    notebook_path=None,
):
    """Execute all 6 deep survey science modules and write advanced_report.md + advanced_metrics.json."""
    try:
        from sklearn.ensemble import RandomForestRegressor
        has_sklearn = True
    except ImportError:
        has_sklearn = False

    df = _load_df(df_path)
    out_dir = Path(report_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    metadata_terms = ("id", "uuid", "time", "date", "lat", "lon", "researcher", "consent", "ref", "pii", "weight", "peso", "respondent")
    numeric_cols = []
    likert_cols = []

    for col in df.columns:
        if any(m == str(col).lower() or str(col).lower().startswith(m + "_") or str(col).lower().endswith("_" + m) for m in metadata_terms):
            continue
        s = pd.to_numeric(df[col], errors="coerce").dropna()
        if len(s) >= max(5, int(len(df) * 0.5)) and s.nunique() >= 2:
            numeric_cols.append(col)
            if 0 <= s.min() and s.max() <= 10 and s.nunique() <= 11:
                likert_cols.append(col)

    analysis_cols = likert_cols if len(likert_cols) >= 3 else numeric_cols
    if len(analysis_cols) < 2:
        raise ValueError(f"Insufficient numeric/Likert columns for advanced analytics (found {len(analysis_cols)}).")

    if not target_col or target_col not in df.columns:
        preferred = [
            c for c in analysis_cols
            if any(k in str(c).lower() for k in ("recommend", "recomend", "nps", "overall", "geral", "satisf", "score", "nota"))
        ]
        target_col = preferred[-1] if preferred else analysis_cols[-1]

    feature_cols = [c for c in analysis_cols if c != target_col]
    if not feature_cols:
        feature_cols = analysis_cols[:-1]
        target_col = analysis_cols[-1]

    num_df = df[analysis_cols].apply(pd.to_numeric, errors="coerce")
    clean_df = num_df.fillna(num_df.median())
    n_rows = len(clean_df)

    # ==========================================================================
    # MODULE 1: Pure Sentiment Stack (Ipsative Centering & Halo Removal)
    # ==========================================================================
    rating_cols = feature_cols if len(feature_cols) >= 2 else analysis_cols
    ratings_mat = clean_df[rating_cols]
    personal_mean = ratings_mat.mean(axis=1)
    ipsative_df = ratings_mat.sub(personal_mean, axis=0)

    pure_sentiment_rows = []
    X_halo = personal_mean.values.reshape(-1, 1)
    for col in rating_cols:
        y_col_vals = ratings_mat[col].values
        raw_mean = float(np.mean(y_col_vals))
        raw_sd = float(np.std(y_col_vals, ddof=1)) if n_rows > 1 else 0.0
        ips_mean = float(ipsative_df[col].mean())
        ips_sd = float(ipsative_df[col].std(ddof=1)) if n_rows > 1 else 0.0
        coef_h, _, _, _ = _ols_fit_predict(X_halo, y_col_vals)
        beta_halo = float(coef_h[0])
        grand_mean = float(personal_mean.mean())
        halo_adj_score = float(raw_mean + ips_mean * (1.0 / max(0.5, abs(beta_halo))))
        pure_delta = ips_mean
        pure_sentiment_rows.append({
            "attribute": col,
            "raw_mean": round(raw_mean, 3),
            "raw_sd": round(raw_sd, 3),
            "ipsative_mean": round(ips_mean, 3),
            "ipsative_sd": round(ips_sd, 3),
            "halo_beta": round(beta_halo, 3),
            "halo_adjusted_mean": round(halo_adj_score, 3),
            "net_sentiment_role": (
                "True Strength (+)" if pure_delta > 0.08 else ("True Pain Point (−)" if pure_delta < -0.08 else "Neutral Baseline")
            ),
        })
    pure_sentiment_rows.sort(key=lambda r: r["ipsative_mean"], reverse=True)

    # ==========================================================================
    # MODULE 2, 3 & 4: Dual Correlation, Key Drivers & Priority Action Matrix
    # ==========================================================================
    y_target = clean_df[target_col].values
    scale_max = float(max(5.0, clean_df[feature_cols].max().max()))
    if scale_max <= 5.0:
        scale_max = 5.0
    elif scale_max <= 7.0:
        scale_max = 7.0
    elif scale_max <= 10.0:
        scale_max = 10.0

    X_feat = clean_df[feature_cols].values
    X_feat_std = _standardize(X_feat)
    y_std = _standardize(y_target.reshape(-1, 1)).ravel()

    std_betas, _, _, r2_ols = _ols_fit_predict(X_feat_std, y_std)

    if has_sklearn:
        rf_model = RandomForestRegressor(n_estimators=120, random_state=42)
        rf_model.fit(X_feat, y_target)
        rf_importances = rf_model.feature_importances_
    else:
        # Non-linear rank + quadratic importance proxy (Shapley/Pratt-style relative weight)
        raw_weights = np.abs(std_betas) * np.array([
            abs(stats.spearmanr(X_feat[:, j], y_target)[0]) if np.std(X_feat[:, j]) > 0 else 0.0
            for j in range(len(feature_cols))
        ])
        rf_importances = raw_weights / (np.sum(raw_weights) if np.sum(raw_weights) > 0 else 1.0)

    dual_correlations = []
    priority_matrix = []
    temp_perfs = [float(clean_df[c].mean()) for c in feature_cols]
    temp_imps = []

    for idx, col in enumerate(feature_cols):
        x_vals = clean_df[col].values
        if np.std(x_vals) > 0 and np.std(y_target) > 0:
            r_p, p_p = stats.pearsonr(x_vals, y_target)
            r_s, p_s = stats.spearmanr(x_vals, y_target)
        else:
            r_p, p_p, r_s, p_s = 0.0, 1.0, 0.0, 1.0
        temp_imps.append(abs(float(r_p)))
        diff_rs = abs(float(r_p) - float(r_s))
        dual_correlations.append({
            "attribute": col,
            "pearson_r": round(float(r_p), 3),
            "pearson_p": round(float(p_p), 5),
            "spearman_rho": round(float(r_s), 3),
            "spearman_p": round(float(p_s), 5),
            "divergence": round(diff_rs, 3),
            "non_linear_flag": diff_rs > 0.10,
        })

    mean_imp_all = float(np.mean(temp_imps)) if temp_imps else 0.0
    mean_perf_all = float(np.mean(temp_perfs)) if temp_perfs else 0.0

    for idx, col in enumerate(feature_cols):
        imp = temp_imps[idx]
        perf = temp_perfs[idx]
        gap = max(0.0, scale_max - perf)
        prio_score = imp * gap
        if imp >= mean_imp_all and perf < mean_perf_all:
            quadrant = "Critical Fix (Immediate Action)"
        elif imp >= mean_imp_all and perf >= mean_perf_all:
            quadrant = "Protect Core Strength"
        elif imp < mean_imp_all and perf < mean_perf_all:
            quadrant = "Low Priority Monitor"
        else:
            quadrant = "Maintain / Possible Overkill"

        priority_matrix.append({
            "label": col,
            "attribute": col,
            "importance": round(imp, 3),
            "rf_importance": round(float(rf_importances[idx]), 3),
            "std_beta": round(float(std_betas[idx]), 3),
            "performance": round(perf, 3),
            "scale_max": scale_max,
            "performance_gap": round(gap, 3),
            "priority_score": round(prio_score, 3),
            "quadrant": quadrant,
        })

    priority_matrix.sort(key=lambda item: item["priority_score"], reverse=True)
    dual_correlations.sort(key=lambda item: abs(item["pearson_r"]), reverse=True)

    # ==========================================================================
    # MODULE 3B: Expectation Residuals (Disappointed / Aligned / Delighted)
    # ==========================================================================
    _, _, y_pred, _ = _ols_fit_predict(X_feat, y_target)
    exp_residuals = y_target - y_pred
    res_sd = float(np.std(exp_residuals, ddof=1)) if n_rows > 1 else 1.0
    res_sd = res_sd if res_sd > 1e-6 else 1.0

    n_disappointed = int((exp_residuals < -1.0 * res_sd).sum())
    n_delighted = int((exp_residuals > 1.0 * res_sd).sum())
    n_aligned = int(n_rows - n_disappointed - n_delighted)

    expectation_segments = {
        "model_r2": round(r2_ols, 3),
        "residual_sd": round(res_sd, 3),
        "disappointed_count": n_disappointed,
        "disappointed_pct": round(n_disappointed / n_rows * 100.0, 1),
        "aligned_count": n_aligned,
        "aligned_pct": round(n_aligned / n_rows * 100.0, 1),
        "delighted_count": n_delighted,
        "delighted_pct": round(n_delighted / n_rows * 100.0, 1),
    }

    # ==========================================================================
    # MODULE 5: Dual Clustering (K-Means + DBSCAN) & Psychometrics (PCA/FA + α)
    # ==========================================================================
    X_all_std = _standardize(clean_df[analysis_cols].values)
    best_k = 3
    best_sil = -1.0
    best_km_labels = None
    if n_rows >= 10:
        for k_cand in range(2, min(6, n_rows // 3 + 1)):
            lbls = _kmeans_np(X_all_std, k=k_cand, random_state=42, n_init=8)
            if len(set(lbls)) > 1:
                sil = _compute_silhouette_np(X_all_std, lbls)
                if sil > best_sil:
                    best_sil = sil
                    best_k = k_cand
                    best_km_labels = lbls

    km_labels = best_km_labels if best_km_labels is not None else _kmeans_np(X_all_std, k=best_k)

    # DBSCAN outlier detection
    eps_val = max(0.85, math.sqrt(len(analysis_cols)) * 0.65)
    min_pts = max(3, min(8, n_rows // 25))
    db_labels = _dbscan_np(X_all_std, eps=eps_val, min_samples=min_pts)
    n_outliers = int((db_labels == -1).sum())
    n_dense_groups = len(set(db_labels) - {-1})

    personas = []
    for cid in range(best_k):
        mask_c = km_labels == cid
        cnt_c = int(mask_c.sum())
        if cnt_c == 0:
            continue
        sub_means = clean_df.loc[mask_c, analysis_cols].mean()
        overall_means = clean_df[analysis_cols].mean()
        diffs = (sub_means - overall_means).sort_values(ascending=False)
        top_pos = f"{diffs.index[0]} ({diffs.iloc[0]:+.2f})" if len(diffs) > 0 else "—"
        top_neg = f"{diffs.index[-1]} ({diffs.iloc[-1]:+.2f})" if len(diffs) > 1 else "—"
        target_mean_c = float(clean_df.loc[mask_c, target_col].mean())
        personas.append({
            "persona_id": f"Persona {cid + 1}",
            "n": cnt_c,
            "pct": round(cnt_c / n_rows * 100.0, 1),
            "target_mean": round(target_mean_c, 2),
            "signature_strength": top_pos,
            "signature_pain_point": top_neg,
        })

    # Psychometrics: Cronbach's Alpha & PCA / Factor Analysis
    cronbach_alpha = compute_cronbach_alpha(clean_df[rating_cols])
    n_factors = min(3, len(analysis_cols) - 1) if len(analysis_cols) >= 3 else 1
    components, exp_ratio = _pca_np(X_all_std, n_components=n_factors)
    explained_var = [round(float(v * 100.0), 1) for v in exp_ratio]

    factor_summary = []
    for f_idx in range(n_factors):
        comp = components[f_idx]
        top_indices = np.argsort(np.abs(comp))[::-1][:3]
        top_vars = [f"{analysis_cols[i]} ({comp[i]:+.2f})" for i in top_indices]
        factor_summary.append({
            "factor": f"Component {f_idx + 1}",
            "variance_explained_pct": explained_var[f_idx],
            "top_loadings": ", ".join(top_vars),
        })

    # ==========================================================================
    # MODULE 6: TURF (Total Unduplicated Reach and Frequency)
    # ==========================================================================
    threshold_turf = 4.0 if scale_max <= 5.0 else (6.0 if scale_max <= 7.0 else 8.0)
    binary_reach_df = (clean_df[rating_cols] >= threshold_turf).astype(int)
    remaining_cols = list(rating_cols)
    reached_mask = np.zeros(n_rows, dtype=bool)
    turf_steps = []

    for step in range(1, min(6, len(remaining_cols) + 1)):
        best_col = None
        best_added = -1
        for col in remaining_cols:
            col_mask = binary_reach_df[col].values == 1
            added = int((col_mask & (~reached_mask)).sum())
            if added > best_added:
                best_added = added
                best_col = col
        if best_col is None or best_added == 0:
            break
        reached_mask = reached_mask | (binary_reach_df[best_col].values == 1)
        remaining_cols.remove(best_col)
        cum_reach = int(reached_mask.sum())
        turf_steps.append({
            "step": step,
            "added_attribute": best_col,
            "incremental_reach_n": best_added,
            "incremental_reach_pct": round(best_added / n_rows * 100.0, 1),
            "cumulative_reach_n": cum_reach,
            "cumulative_reach_pct": round(cum_reach / n_rows * 100.0, 1),
        })

    # Save JSON payload
    metrics_payload = {
        "target_column": target_col,
        "sample_size": n_rows,
        "scale_max": scale_max,
        "cronbach_alpha": round(cronbach_alpha, 4),
        "cronbach_alpha_interpretation": interpret_cronbach_alpha(cronbach_alpha),
        "pure_sentiment_stack": pure_sentiment_rows,
        "priority_matrix": priority_matrix,
        "dual_correlations": dual_correlations,
        "expectation_segments": expectation_segments,
        "clustering": {
            "optimal_k": best_k,
            "silhouette_score": round(best_sil, 3),
            "dbscan_dense_groups": n_dense_groups,
            "dbscan_outliers_count": n_outliers,
            "dbscan_outliers_pct": round(n_outliers / n_rows * 100.0, 1),
            "personas": personas,
        },
        "psychometrics_pca": {
            "total_variance_explained_pct": round(sum(explained_var), 1),
            "factors": factor_summary,
        },
        "turf_optimization": {
            "top_box_threshold": threshold_turf,
            "steps": turf_steps,
        },
    }
    (out_dir / "advanced_metrics.json").write_text(
        json.dumps(metrics_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Build Tufte Markdown Report (advanced_report.md)
    md = [
        f"# Advanced Survey Science & Psychometric Synthesis (Target: `{target_col}`)",
        "",
        f"**Sample Base ($N$):** `{n_rows:,}` · **Scale Reliability (Cronbach's $\\alpha$):** `{cronbach_alpha:.3f}` ({interpret_cronbach_alpha(cronbach_alpha)}) · "
        f"**Driver Model $R^2$:** `{r2_ols:.3f}` · **Optimal K-Means Silhouette:** `{best_sil:.3f}` ($K={best_k}$)",
        "",
        "> **Margin Note:** This section synthesizes six advanced methodologies from `references/analysis/`: Ipsative & Halo-Residual Pure Sentiment, Derived Importance × Performance Priority Matrix, Expectation Residual Segmentation, Dual Correlation (Pearson $r$ vs. Spearman $\\rho$), Silhouette-Optimized Persona Clustering with DBSCAN Outlier isolation, and TURF Reach Optimization.",
        "",
        "## 1. Priority Action Matrix & Key Driver Analysis",
        "",
        "Attributes are ranked by **Priority Score** $= \\text{Derived Importance } (|r|) \\times (\\text{Scale}_{\\max} - \\text{Mean Performance})$, combining linear standardized $\\beta$ and non-linear relative importance:",
        "",
        "| Rank | Attribute | Mean Perf | Gap to Max | Derived Imp ($|r|$) | Std $\\beta$ | Relative Weight | Priority Score | Strategic Quadrant |",
        "| ---: | :--- | ---: | ---: | ---: | ---: | ---: | ---: | :--- |",
    ]
    for idx, pm in enumerate(priority_matrix, 1):
        md.append(
            f"| {idx} | **{pm['attribute']}** | {pm['performance']:.2f} | {pm['performance_gap']:.2f} | "
            f"{pm['importance']:.3f} | {pm['std_beta']:+.3f} | {pm['rf_importance']:.3f} | "
            f"**{pm['priority_score']:.3f}** | {pm['quadrant']} |"
        )
    md.extend([
        "",
        "## 2. Pure Sentiment Stack (Ipsative Centering & Halo Effect Removal)",
        "",
        "To eliminate respondent-level **Halo Bias** (yea-saying / nay-saying scale inflation), each rating is centered against the respondent's own personal mean ($X_{ij} - \\bar{X}_i$) and regressed against general impression:",
        "",
        "| Attribute | Raw Mean ± SD | Ipsative Mean ($X_{ij} - \\bar{X}_i$) | Halo $\\beta$ Sensitivity | Halo-Adjusted Mean | Pure Sentiment Role |",
        "| :--- | ---: | ---: | ---: | ---: | :--- |",
    ])
    for ps in pure_sentiment_rows:
        md.append(
            f"| **{ps['attribute']}** | {ps['raw_mean']:.2f} (±{ps['raw_sd']:.2f}) | "
            f"**{ps['ipsative_mean']:+.3f}** | {ps['halo_beta']:.2f} | {ps['halo_adjusted_mean']:.2f} | {ps['net_sentiment_role']} |"
        )

    md.extend([
        "",
        "## 3. Expectation Residuals (Disappointed / Aligned / Delighted Segmentation)",
        "",
        f"Comparing each respondent's observed `{target_col}` against their driver-predicted expectation ($\\hat{{Y}}_i$, OLS $R^2 = {r2_ols:.3f}$, $\\text{{SD}}_e = {res_sd:.2f}$):",
        "",
        "| Expectation Segment | Residual Rule ($e_i = Y_i - \\hat{Y}_i$) | Respondent Count ($N$) | Share of Sample (%) | Strategic Diagnostic |",
        "| :--- | :--- | ---: | ---: | :--- |",
        f"| **Disappointed (Churn Risk)** | $e_i < -1.0\\,\\text{{SD}}_e$ | {n_disappointed} | {expectation_segments['disappointed_pct']:.1f}% | Harsh graders / uncaptured friction |",
        f"| **Aligned (Expected)** | $|e_i| \\le 1.0\\,\\text{{SD}}_e$ | {n_aligned} | {expectation_segments['aligned_pct']:.1f}% | Outcome matches attribute ratings |",
        f"| **Delighted (Brand Advocates)** | $e_i > +1.0\\,\\text{{SD}}_e$ | {n_delighted} | {expectation_segments['delighted_pct']:.1f}% | Strong goodwill / organic promoters |",
        "",
        "## 4. Dual Correlation Matrix (Pearson $r$ Linear vs. Spearman $\\rho$ Monotonic)",
        "",
        "| Attribute | Pearson $r$ | Pearson $p$-value | Spearman $\\rho$ | Spearman $p$-value | $|r - \\rho|$ Divergence | Linearity Diagnostic |",
        "| :--- | ---: | ---: | ---: | ---: | ---: | :--- |",
    ])
    for dc in dual_correlations:
        diag = "⚠ Non-linear / Threshold effect" if dc["non_linear_flag"] else "Linear alignment"
        md.append(
            f"| **{dc['attribute']}** | `{dc['pearson_r']:+.3f}` | `{dc['pearson_p']:.4f}` | "
            f"`{dc['spearman_rho']:+.3f}` | `{dc['spearman_p']:.4f}` | `{dc['divergence']:.3f}` | {diag} |"
        )

    md.extend([
        "",
        "## 5. Dual Audience Clustering (K-Means Personas + DBSCAN Anomaly Detection) & PCA Factors",
        "",
        f"- **K-Means Optimal Personas:** $K = {best_k}$ (Silhouette Score $= {best_sil:.3f}$)\n"
        f"- **DBSCAN Density Scan:** `{n_dense_groups}` dense core groups and **`{n_outliers}` noise/outlier respondents (`{metrics_payload['clustering']['dbscan_outliers_pct']:.1f}%`)** isolated (`cluster = -1`).\n"
        f"- **Latent PCA Variance Explained:** `{sum(explained_var):.1f}%` across `{n_factors}` orthogonal components.",
        "",
        "| Persona Cluster | Segment Size ($N$) | Share (%) | Mean Target Score | Signature Relative Strength | Signature Relative Pain Point |",
        "| :--- | ---: | ---: | ---: | :--- | :--- |",
    ])
    for p in personas:
        md.append(
            f"| **{p['persona_id']}** | {p['n']} | {p['pct']:.1f}% | {p['target_mean']:.2f} | "
            f"{p['signature_strength']} | {p['signature_pain_point']} |"
        )

    if turf_steps:
        md.extend([
            "",
            f"## 6. TURF Reach Optimization (Top-Box Threshold $\\ge {threshold_turf:.0f}$)",
            "",
            "| Bundle Step | Added Attribute | Incremental Reach ($N$) | Incremental Reach (%) | Cumulative Unduplicated Reach ($N$) | Cumulative Reach (%) |",
            "| ---: | :--- | ---: | ---: | ---: | ---: |",
        ])
        for ts in turf_steps:
            md.append(
                f"| Step {ts['step']} | **{ts['added_attribute']}** | +{ts['incremental_reach_n']} | "
                f"+{ts['incremental_reach_pct']:.1f}% | {ts['cumulative_reach_n']} | **{ts['cumulative_reach_pct']:.1f}%** |"
            )
        md.append("")

    (out_dir / "advanced_report.md").write_text("\n".join(md), encoding="utf-8")

    if notebook_path:
        create_advanced_notebook(str(df_path), target_col=target_col, output_path=notebook_path)

    return metrics_payload


def create_advanced_notebook(df_path, target_col=None, output_path="advanced_analytics.ipynb"):
    """Generate an interactive Jupyter Notebook for advanced multivariate exploration."""
    df = _load_df(df_path)
    metadata_terms = ["id", "time", "lat", "lon", "researcher", "consent", "ref", "pii"]
    mapping = {}
    if os.path.exists(COLUMN_MAPPING_PATH):
        with open(COLUMN_MAPPING_PATH, "r", encoding="utf-8") as f:
            mapping = json.load(f)

    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"# Advanced Analytics Report: {os.path.basename(df_path)}\n",
                "This notebook focuses on multivariate relationships, predictive importance, Halo removal, and audience segmentation.",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import numpy as np\n",
                f"df = pd.read_parquet('{os.path.abspath(df_path)}') if '{df_path}'.endswith('.parquet') else pd.read_csv('{os.path.abspath(df_path)}')\n",
                f"target_col = '{target_col}'\n",
                "numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()\n",
                f"metadata = {metadata_terms}\n",
                "analysis_cols = [c for c in numeric_cols if not any(m in c.lower() for m in metadata)]\n",
                "print(f'Ready for analysis with {len(analysis_cols)} numeric attributes.')",
            ],
        },
    ]

    notebook = {
        "cells": cells,
        "metadata": {"kernelspec": {"display_name": "Python 3", "name": "python3"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    print(f"✓ Advanced notebook saved: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data-Pro-Skill Advanced Survey Science Engine")
    parser.add_argument("input", help="Input dataset file (.csv, .xlsx, .parquet)")
    parser.add_argument("target", nargs="?", default=None, help="Optional target outcome column")
    parser.add_argument("notebook_out", nargs="?", default=None, help="Optional output .ipynb path")
    parser.add_argument("--target", "-t", dest="target_flag", default=None, help="Target outcome column name")
    parser.add_argument("--report-dir", "-o", default=".dps/outputs/advanced", help="Output directory for advanced_report.md")
    parser.add_argument("--notebook", default=None, help="Optional path to also emit a Jupyter notebook")

    args = parser.parse_args()
    tgt = args.target_flag or args.target
    nb = args.notebook or (args.notebook_out if (args.notebook_out and str(args.notebook_out).endswith(".ipynb")) else None)
    rep_dir = args.report_dir
    if args.notebook_out and not str(args.notebook_out).endswith(".ipynb"):
        rep_dir = args.notebook_out

    try:
        res = run_advanced_survey_analytics(args.input, target_col=tgt, report_dir=rep_dir, notebook_path=nb)
        print(
            f"✅ Advanced survey analytics complete in {rep_dir} "
            f"(Target={res['target_column']}, Cronbach α={res['cronbach_alpha']:.3f}, "
            f"Personas K={res['clustering']['optimal_k']}, Priority Items={len(res['priority_matrix'])})"
        )
    except Exception as e:
        print(f"❌ Error during advanced analytics: {e}", file=sys.stderr)
        sys.exit(1)
