"""
PCA + DBSCAN Walk-Forward Pair Election
=========================================
Generic implementation of the Sohail (2020) pair election methodology.

Combines PCA loadings (price co-movement) with sector one-hot dummies
(domain constraint) to form a hybrid feature space, then clusters with
DBSCAN to identify statistically similar asset pairs.

Runs in a rolling walk-forward fashion: for each period, use the last
N months as the formation window, then advance by M months.

Usage:
    from pca_dbscan_pair_election import run_walk_forward

    pairs_df = run_walk_forward(
        prices_df=my_prices_df,         # Wide DataFrame: date index, ticker columns
        sector_map=my_sector_map,       # Series: ticker -> sector string
        formation_months=24,
        trading_months=6,
        pca_components=2,
        eps=0.03,
        min_samples=3,
        sector_weight=1.0,
        data_start='2005-01-01',
        data_end='2025-01-01',
        output_file='pairs_history.csv',  # None = in-memory only
    )
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


def calculate_log_returns(prices_df: pd.DataFrame) -> pd.DataFrame:
    """Compute log returns from a wide price DataFrame."""
    return np.log(prices_df / prices_df.shift(1))


def build_hybrid_features(
    returns: pd.DataFrame,
    sector_map: pd.Series,
    n_components: int = 10,
    sector_weight: float = 1.0,
) -> pd.DataFrame | None:
    """
    Build hybrid feature matrix: PCA loadings + weighted sector dummies.

    Parameters
    ----------
    returns : DataFrame
        Log returns, tickers as columns.
    sector_map : Series
        Index = ticker, values = sector label string.
    n_components : int
        Number of PCA components to extract.
    sector_weight : float
        Multiplier for sector dummy columns (0 = pure PCA, 1 = equal weight).

    Returns
    -------
    DataFrame of shape (n_tickers, n_components + n_sectors) or None if
    insufficient data.
    """
    valid_returns = returns.dropna(axis=1, how="any")

    if valid_returns.shape[1] < n_components + 1:
        return None

    scaler = StandardScaler()
    standardized = scaler.fit_transform(valid_returns)

    pca = PCA(n_components=n_components)
    pca.fit(standardized)

    loadings = pd.DataFrame(
        pca.components_.T,
        index=valid_returns.columns,
        columns=[f"PC{i+1}" for i in range(n_components)],
    )

    window_sectors = sector_map.reindex(valid_returns.columns).fillna("OUTROS")
    sector_dummies = pd.get_dummies(window_sectors, prefix="SEC").astype(float) * sector_weight

    return pd.concat([loadings, sector_dummies], axis=1)


def find_pairs_in_clusters(
    features: pd.DataFrame,
    eps: float = 0.03,
    min_samples: int = 3,
) -> tuple[pd.DataFrame, int]:
    """
    Run DBSCAN and enumerate all intra-cluster pairs with their Euclidean distance.

    Returns
    -------
    (pairs_df, n_clusters)
        pairs_df columns: ticker1, ticker2, cluster, distance_hybrid, cluster_size
    """
    clf = DBSCAN(eps=eps, min_samples=min_samples, metric="euclidean")
    labels = clf.fit_predict(features)

    pairs = []
    n_clusters = 0

    for lbl in set(labels):
        if lbl == -1:
            continue
        n_clusters += 1
        indices = [i for i, x in enumerate(labels) if x == lbl]
        cluster_tickers = features.index[indices].tolist()
        cluster_data = features.iloc[indices]

        for i in range(len(cluster_tickers)):
            for j in range(i + 1, len(cluster_tickers)):
                s1, s2 = cluster_tickers[i], cluster_tickers[j]
                dist = np.linalg.norm(cluster_data.loc[s1] - cluster_data.loc[s2])
                pairs.append({
                    "ticker1": s1, "ticker2": s2,
                    "cluster": lbl, "distance_hybrid": dist,
                    "cluster_size": len(cluster_tickers),
                })

    return pd.DataFrame(pairs), n_clusters


def run_walk_forward(
    prices_df: pd.DataFrame,
    sector_map: pd.Series,
    formation_months: int = 24,
    trading_months: int = 6,
    pca_components: int = 2,
    eps: float = 0.03,
    min_samples: int = 3,
    sector_weight: float = 1.0,
    data_start: str | None = None,
    data_end: str | None = None,
    output_file: str | None = "pairs_history.csv",
    silent: bool = False,
) -> pd.DataFrame:
    """
    Run the full walk-forward pair election pipeline.

    Parameters
    ----------
    prices_df : DataFrame
        Wide format: DatetimeIndex, ticker columns, close prices.
    sector_map : Series
        Index = ticker, values = sector label.
    formation_months : int
        Length of the formation (training) window in months.
    trading_months : int
        Length of the trading (out-of-sample) window in months.
    pca_components : int
        Max PCA components (capped at n_assets/3).
    eps : float
        DBSCAN epsilon (neighbourhood radius).
    min_samples : int
        DBSCAN minimum cluster size.
    sector_weight : float
        Weight of sector dummies vs PCA loadings.
    data_start, data_end : str or None
        Date range filter (ISO format).
    output_file : str or None
        If provided, save pairs to this CSV path.
    silent : bool
        Suppress progress output.

    Returns
    -------
    DataFrame with all elected pairs across all walk-forward windows.
    """
    returns = calculate_log_returns(prices_df)

    start = pd.Timestamp(data_start) if data_start else returns.index.min()
    end   = pd.Timestamp(data_end)   if data_end   else returns.index.max()
    start = max(start, returns.index.min())
    end   = min(end,   returns.index.max())

    current = start
    all_pairs = []

    if not silent:
        print(f"Walk-Forward: {start.date()} → {end.date()} | EPS={eps}, Min={min_samples}, SecWt={sector_weight}")

    while current + pd.DateOffset(months=formation_months) < end:
        form_start  = current
        form_end    = current + pd.DateOffset(months=formation_months)
        trade_start = form_end
        trade_end   = trade_start + pd.DateOffset(months=trading_months)

        slice_ret = returns.loc[form_start:form_end].dropna(axis=1, how="all").fillna(0)
        n_assets  = slice_ret.shape[1]

        n_clusters = pairs_count = 0

        if n_assets > 10:
            n_comps  = min(pca_components, int(n_assets / 3))
            features = build_hybrid_features(slice_ret, sector_map, n_components=n_comps, sector_weight=sector_weight)

            if features is not None:
                pairs_df, n_clusters = find_pairs_in_clusters(features, eps=eps, min_samples=min_samples)

                if not pairs_df.empty:
                    pairs_df["formation_start"] = form_start
                    pairs_df["formation_end"]   = form_end
                    pairs_df["trading_start"]   = trade_start
                    pairs_df["trading_end"]     = trade_end
                    pairs_df["n_universe"]      = n_assets
                    all_pairs.append(pairs_df)
                    pairs_count = len(pairs_df)

        if not silent:
            print(f"  [{form_end.date()}] Universe={n_assets}, Clusters={n_clusters}, Pairs={pairs_count}")

        current += pd.DateOffset(months=trading_months)

    final_df = pd.DataFrame()
    if all_pairs:
        final_df = pd.concat(all_pairs, ignore_index=True)
        if output_file:
            final_df.to_csv(output_file, index=False, sep=";")
            if not silent:
                print(f"Saved {len(final_df)} pairs to {output_file}")
    elif not silent:
        print("No pairs found.")

    return final_df
