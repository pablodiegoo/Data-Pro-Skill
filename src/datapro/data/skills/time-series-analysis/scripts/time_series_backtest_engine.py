"""
Pairs Trading Backtest Engine
==============================
Generic, parameterized backtest engine for statistical arbitrage (pairs trading).

Implements the Sohail (2020) methodology:
- Normalized price spread (no OLS regression needed)
- Z-score based entry/exit signals
- ADF cointegration filter (optional)
- Multiple stop-loss modes: Z-score, percentile tail, time stop
- Volatility-tier filter (optional)
- CSV streaming output for large datasets

Usage:
    from pairs_trading_backtest_engine import run_backtest

    results = run_backtest(
        pairs_df=my_pairs_df,          # DataFrame with ticker1, ticker2, formation/trading dates
        prices_df=my_prices_df,        # Wide DataFrame: index=date, columns=tickers
        entry_z=2.0,
        exit_z_override=0.5,
        stop_z=4.0,
        stop_time=63,                  # Max holding period in trading days
        output_file='trades.csv',
    )
"""

import pandas as pd
import numpy as np
import os
import csv
from statsmodels.tsa.stattools import adfuller


# ─── Default Configuration ────────────────────────────────────────────────────
ENTRY_Z = 2.0
EXIT_Z = 0.0
STOP_Z = 999.0
COST_PER_TRADE = 0.0
# ──────────────────────────────────────────────────────────────────────────────


def run_backtest(
    pairs_df: pd.DataFrame,
    prices_df: pd.DataFrame,
    entry_z: float = ENTRY_Z,
    exit_z_override: float | None = None,
    stop_z: float = STOP_Z,
    stop_p: float | None = None,          # Percentile stop (e.g. 0.99 = 99th pct)
    stop_time: int | None = None,         # Max holding period in trading days
    cost_per_trade: float = COST_PER_TRADE,
    use_coint_filter: bool = True,
    adf_threshold: float = 0.05,
    use_vol_filter: bool = False,
    output_file: str = "backtest_trades.csv",
) -> dict:
    """
    Run a vectorized pairs trading backtest.

    Parameters
    ----------
    pairs_df : DataFrame
        Must contain columns: ticker1, ticker2, formation_start, formation_end,
        trading_start, trading_end.
    prices_df : DataFrame
        Wide format: DatetimeIndex rows, ticker columns, close prices.
    entry_z : float
        Z-score threshold to enter a trade.
    exit_z_override : float or None
        Override the default exit Z (0.0 = full mean reversion).
    stop_z : float
        Z-score stop-loss level (e.g. 4.0).
    stop_p : float or None
        Percentile-based stop on the formation spread (e.g. 0.99).
    stop_time : int or None
        Maximum holding period in trading days.
    cost_per_trade : float
        Round-trip cost per leg (applied 4x per trade).
    use_coint_filter : bool
        Run ADF test on formation spread; skip non-stationary pairs.
    adf_threshold : float
        P-value threshold for ADF test.
    use_vol_filter : bool
        Apply Sohail volatility filter (only trade low-vol long legs).
    output_file : str
        Path to write trade records (CSV, semicolon-delimited).

    Returns
    -------
    dict with keys: PnL, WinRate, Trades
    """
    target_exit_z = exit_z_override if exit_z_override is not None else EXIT_Z

    # Ensure datetime index
    if not isinstance(prices_df.index, pd.DatetimeIndex):
        prices_df.index = pd.to_datetime(prices_df.index)

    # Date → integer index map for fast lookups
    dates_array = prices_df.index.values
    price_cache = {col: prices_df[col].values for col in prices_df.columns}

    # Volatility tiers (optional)
    vol_map: dict = {}
    if use_vol_filter:
        log_rets = np.log(prices_df / prices_df.shift(1))
        volatilities = log_rets.std() * np.sqrt(252)
        try:
            vol_tiers = pd.qcut(volatilities, 4, labels=["Q1", "Q2", "Q3", "Q4"])
        except ValueError:
            vol_tiers = pd.qcut(
                volatilities.rank(method="first"), 4, labels=["Q1", "Q2", "Q3", "Q4"]
            )
        vol_map = vol_tiers.to_dict()

    # Coerce date columns
    date_cols = ["formation_start", "formation_end", "trading_start", "trading_end"]
    for col in date_cols:
        pairs_df[col] = pd.to_datetime(pairs_df[col])

    total_pnl = 0.0
    win_count = 0
    trade_count = 0

    fieldnames = ["Pair", "Type", "Entry Date", "Exit Date", "Entry Z", "Exit Z", "PnL", "Result"]
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()

        for i, (_, row) in enumerate(pairs_df.iterrows()):
            if i % 200 == 0:
                print(f"  [Backtest] Processing pair {i}/{len(pairs_df)}...", flush=True)

            t1, t2 = row["ticker1"], row["ticker2"]

            # Index slicing via searchsorted
            f_start_idx = min(prices_df.index.searchsorted(row["formation_start"]), len(prices_df) - 1)
            f_end_idx   = min(prices_df.index.searchsorted(row["formation_end"]),   len(prices_df) - 1)
            t_start_idx = min(prices_df.index.searchsorted(row["trading_start"]),   len(prices_df) - 1)
            t_end_idx   = min(prices_df.index.searchsorted(row["trading_end"]),     len(prices_df) - 1)

            if f_start_idx >= f_end_idx or t_start_idx >= t_end_idx:
                continue

            try:
                p1_form = price_cache[t1][f_start_idx : f_end_idx + 1]
                p2_form = price_cache[t2][f_start_idx : f_end_idx + 1]
                p1      = price_cache[t1][t_start_idx : t_end_idx + 1]
                p2      = price_cache[t2][t_start_idx : t_end_idx + 1]
                dates   = dates_array[t_start_idx : t_end_idx + 1]
            except KeyError:
                continue

            if len(p1_form) == 0 or len(p1) == 0:
                continue

            p1_aaa, p2_aaa = p1_form[0], p2_form[0]
            if p1_aaa == 0 or p2_aaa == 0:
                continue

            # Formation spread statistics
            spread_form = (p1_form / p1_aaa) - (p2_form / p2_aaa)
            mu    = np.mean(spread_form)
            sigma = np.std(spread_form)
            if sigma == 0:
                continue

            # Percentile stop limits
            upper_stop = lower_stop = None
            if stop_p is not None:
                upper_stop = np.percentile(spread_form, stop_p * 100)
                lower_stop = np.percentile(spread_form, (1 - stop_p) * 100)

            # ADF cointegration filter
            if use_coint_filter:
                try:
                    p_value = adfuller(spread_form, autolag="AIC")[1]
                    if p_value > adf_threshold:
                        continue
                except Exception:
                    continue

            # Trading period
            spread_values = (p1 / p1_aaa) - (p2 / p2_aaa)
            z_values = (spread_values - mu) / sigma

            position = 0
            entry_idx = 0
            entry_price_spread = 0.0

            for k in range(len(z_values)):
                z = z_values[k]

                if position == 0:
                    # Entry Long
                    if z < -entry_z:
                        allowed = True
                        if use_vol_filter:
                            tier = vol_map.get(t1, vol_map.get(t1.replace(".SA", "").strip(), "Unknown"))
                            if tier != "Q1":
                                allowed = False
                        if allowed:
                            position, entry_idx, entry_price_spread = 1, k, spread_values[k]
                    # Entry Short
                    elif z > entry_z:
                        allowed = True
                        if use_vol_filter:
                            tier = vol_map.get(t2, vol_map.get(t2.replace(".SA", "").strip(), "Unknown"))
                            if tier != "Q1":
                                allowed = False
                        if allowed:
                            position, entry_idx, entry_price_spread = -1, k, spread_values[k]

                elif position == 1:
                    is_stop_p    = upper_stop is not None and (spread_values[k] - entry_price_spread) < -0.05
                    is_stop_z    = z < -stop_z
                    is_time_stop = stop_time is not None and (k - entry_idx) >= stop_time

                    if z > -target_exit_z or is_stop_z or is_stop_p or is_time_stop:
                        pnl_net = (spread_values[k] - entry_price_spread) - (4 * cost_per_trade)
                        result  = "TimeStop" if is_time_stop else ("StopOut" if (is_stop_p or is_stop_z) else ("Profit" if pnl_net > 0 else "Loss"))
                        writer.writerow({"Pair": f"{t1}-{t2}", "Type": "Long Spread",
                                         "Entry Date": dates[entry_idx], "Exit Date": dates[k],
                                         "Entry Z": -entry_z, "Exit Z": z, "PnL": pnl_net, "Result": result})
                        total_pnl += pnl_net; trade_count += 1
                        if pnl_net > 0: win_count += 1
                        position = 0

                elif position == -1:
                    is_stop_p    = upper_stop is not None and (entry_price_spread - spread_values[k]) < -0.05
                    is_stop_z    = z > stop_z
                    is_time_stop = stop_time is not None and (k - entry_idx) >= stop_time

                    if z < target_exit_z or is_stop_z or is_stop_p or is_time_stop:
                        pnl_net = (entry_price_spread - spread_values[k]) - (4 * cost_per_trade)
                        result  = "TimeStop" if is_time_stop else ("StopOut" if (is_stop_p or is_stop_z) else ("Profit" if pnl_net > 0 else "Loss"))
                        writer.writerow({"Pair": f"{t1}-{t2}", "Type": "Short Spread",
                                         "Entry Date": dates[entry_idx], "Exit Date": dates[k],
                                         "Entry Z": entry_z, "Exit Z": z, "PnL": pnl_net, "Result": result})
                        total_pnl += pnl_net; trade_count += 1
                        if pnl_net > 0: win_count += 1
                        position = 0

    win_rate = (win_count / trade_count) if trade_count > 0 else 0
    return {"PnL": total_pnl, "WinRate": win_rate, "Trades": trade_count}
