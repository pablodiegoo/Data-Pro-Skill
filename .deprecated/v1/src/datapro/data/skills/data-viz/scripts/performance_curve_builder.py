"""
Multi-Strategy Equity Curve Builder
=====================================
Builds daily equity curves from raw trade CSVs without a full
money management simulator. Useful for quick visualization and
comparison of multiple strategies.

Usage:
    from equity_curve_builder import build_equity_curve, calculate_drawdown

    df_eq = build_equity_curve('trades.csv', initial_capital=100_000, allocation_pct=0.05)
    df_eq['drawdown'] = calculate_drawdown(df_eq['equity'])
"""

import pandas as pd
import numpy as np


def build_equity_curve(
    trades_file: str,
    initial_capital: float = 100_000.0,
    allocation_pct: float = 0.05,
    sep: str = ";",
) -> pd.DataFrame:
    """
    Build a daily equity curve from a trades CSV.

    Parameters
    ----------
    trades_file : str
        CSV with columns: Entry Date, Exit Date, PnL (semicolon-delimited by default).
    initial_capital : float
        Starting equity.
    allocation_pct : float
        Fixed fraction of initial capital allocated per trade.
    sep : str
        CSV delimiter.

    Returns
    -------
    DataFrame with columns: time (daily), equity
    """
    df = pd.read_csv(trades_file, sep=sep)
    df["Entry Date"] = pd.to_datetime(df["Entry Date"])
    df["Exit Date"]  = pd.to_datetime(df["Exit Date"])

    events = []
    for idx, row in df.iterrows():
        events.append({"time": row["Entry Date"], "type": "ENTRY", "pnl": row["PnL"], "id": idx})
        events.append({"time": row["Exit Date"],  "type": "EXIT",  "pnl": row["PnL"], "id": idx})

    events.sort(key=lambda x: (x["time"], 0 if x["type"] == "EXIT" else 1))

    curr_equity = initial_capital
    active_allocs: dict = {}
    curve = [{"time": events[0]["time"] - pd.Timedelta(days=1), "equity": curr_equity}]

    for e in events:
        if e["type"] == "ENTRY":
            active_allocs[e["id"]] = curr_equity * allocation_pct
        else:
            if e["id"] in active_allocs:
                alloc = active_allocs.pop(e["id"])
                curr_equity += alloc * e["pnl"]
        curve.append({"time": e["time"], "equity": curr_equity})

    df_curve = pd.DataFrame(curve).set_index("time")
    return df_curve.resample("D").last().ffill().reset_index()


def calculate_drawdown(equity_series: pd.Series) -> pd.Series:
    """
    Compute rolling drawdown from peak.

    Returns
    -------
    Series of drawdown values (negative, e.g. -0.15 = -15% from peak).
    """
    rolling_max = equity_series.cummax()
    return (equity_series - rolling_max) / rolling_max


def extend_series_to_date(df: pd.DataFrame, target_date, time_col: str = "time", equity_col: str = "equity") -> pd.DataFrame:
    """
    Extend a strategy's equity curve to a target end date by repeating the last value.
    Useful for aligning multiple strategies on the same x-axis.
    """
    last_date   = df[time_col].max()
    last_equity = df[equity_col].iloc[-1]
    if last_equity < 0:
        last_equity = 0

    if last_date < pd.Timestamp(target_date):
        missing = pd.date_range(start=last_date + pd.Timedelta(days=1), end=target_date, freq="D")
        ext = pd.DataFrame({time_col: missing, equity_col: last_equity})
        df = pd.concat([df, ext], ignore_index=True)

    return df
