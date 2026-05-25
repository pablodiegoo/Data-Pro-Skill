"""
DBSCAN Cluster Quality Metrics
================================
Evaluates the quality of DBSCAN clustering results for pairs trading,
specifically detecting "giant cluster" pathology where one cluster
absorbs most of the universe.

Also provides a grid search scorer for DBSCAN hyperparameter optimization.

Usage:
    from dbscan_cluster_quality import calculate_cluster_metrics, score_configuration

    metrics = calculate_cluster_metrics(pairs_df)
    score   = score_configuration(metrics)
"""

import pandas as pd
import numpy as np


def calculate_cluster_metrics(pairs_df: pd.DataFrame, total_periods: int = 41) -> dict:
    """
    Compute quality metrics for a walk-forward pairs DataFrame.

    Parameters
    ----------
    pairs_df : DataFrame
        Output of run_walk_forward(); must have columns:
        formation_end, cluster, ticker1, ticker2, n_universe.
    total_periods : int
        Expected total number of walk-forward periods (for zero-pair period count).

    Returns
    -------
    dict with keys:
        Avg_Pairs, Total_Pairs, Avg_Clusters, Avg_Giant_Ratio,
        Max_Giant_Ratio, Periods_Giant, Total_Periods, Zero_Pair_Periods
    """
    if pairs_df.empty:
        return {
            "Avg_Pairs": 0, "Total_Pairs": 0, "Avg_Clusters": 0,
            "Avg_Giant_Ratio": 0, "Max_Giant_Ratio": 0,
            "Periods_Giant": 0, "Total_Periods": 0,
            "Zero_Pair_Periods": total_periods,
        }

    giant_threshold = 0.50
    period_metrics  = []

    for period in pairs_df["formation_end"].unique():
        pdf = pairs_df[pairs_df["formation_end"] == period]
        clusters = pdf["cluster"].unique()

        sizes = []
        for c in clusters:
            cdf = pdf[pdf["cluster"] == c]
            tickers = set(cdf["ticker1"]).union(set(cdf["ticker2"]))
            sizes.append(len(tickers))

        max_size = max(sizes) if sizes else 0
        universe = pdf["n_universe"].iloc[0] if "n_universe" in pdf.columns else sum(sizes)
        giant_ratio = max_size / universe if universe > 0 else 0

        period_metrics.append({
            "period": period,
            "n_pairs": len(pdf),
            "n_clusters": len(clusters),
            "giant_ratio": giant_ratio,
            "is_giant": giant_ratio > giant_threshold,
        })

    df_m = pd.DataFrame(period_metrics)

    return {
        "Avg_Pairs":        df_m["n_pairs"].mean(),
        "Total_Pairs":      len(pairs_df),
        "Avg_Clusters":     df_m["n_clusters"].mean(),
        "Avg_Giant_Ratio":  df_m["giant_ratio"].mean(),
        "Max_Giant_Ratio":  df_m["giant_ratio"].max(),
        "Periods_Giant":    int(df_m["is_giant"].sum()),
        "Total_Periods":    len(df_m),
        "Zero_Pair_Periods": total_periods - len(df_m),
    }


def score_configuration(metrics: dict) -> float:
    """
    Compute a scalar score for a DBSCAN configuration.

    Higher is better. Penalizes giant clusters and frequent failures.

    Score = Total_Pairs × (1 - Avg_Giant_Ratio)
          × 0.5  if Max_Giant_Ratio > 0.8
          × 0.1  if Periods_Giant > 10
    """
    score = metrics["Total_Pairs"] * (1 - metrics["Avg_Giant_Ratio"])
    if metrics["Max_Giant_Ratio"] > 0.8:
        score *= 0.5
    if metrics["Periods_Giant"] > 10:
        score *= 0.1
    return score


def run_grid_search(
    run_walk_forward_fn,
    grid_eps: list,
    grid_min_samples: list,
    grid_sector_weight: list,
    total_periods: int = 41,
    log_file: str | None = None,
) -> pd.DataFrame:
    """
    Run a grid search over DBSCAN hyperparameters.

    Parameters
    ----------
    run_walk_forward_fn : callable
        Function with signature (eps, min_samples, sector_weight, output_file=None, silent=True)
        that returns a pairs DataFrame.
    grid_eps, grid_min_samples, grid_sector_weight : list
        Parameter grids.
    total_periods : int
        Expected total walk-forward periods.
    log_file : str or None
        If provided, append results to this CSV incrementally.

    Returns
    -------
    DataFrame of results sorted by Score descending.
    """
    import time

    results = []

    for eps in grid_eps:
        for min_s in grid_min_samples:
            for sec_wt in grid_sector_weight:
                print(f"Testing EPS={eps}, Min={min_s}, SecWt={sec_wt} ...", flush=True)
                t0 = time.time()
                try:
                    df_pairs = run_walk_forward_fn(eps=eps, min_samples=min_s, sector_weight=sec_wt,
                                                   output_file=None, silent=True)
                    m = calculate_cluster_metrics(df_pairs, total_periods=total_periods)
                    score = score_configuration(m)
                    row = {"EPS": eps, "MinSamples": min_s, "SectorWeight": sec_wt, **m, "Score": score}
                    results.append(row)
                    if log_file:
                        pd.DataFrame([row]).to_csv(log_file, mode="a", header=not pd.io.common.file_exists(log_file), index=False)
                    print(f"  → Pairs={m['Total_Pairs']}, GiantPeriods={m['Periods_Giant']}, Score={score:.1f} ({time.time()-t0:.1f}s)")
                except Exception as e:
                    print(f"  [ERROR] {e}")

    df_res = pd.DataFrame(results)
    if not df_res.empty:
        df_res = df_res.sort_values("Score", ascending=False)
    return df_res
