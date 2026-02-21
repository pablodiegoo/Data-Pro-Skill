"""
Event-Driven Capital Allocation Simulator
==========================================
Generic money management simulator for backtested trade signals.

Applies realistic capital allocation rules to a raw trades CSV:
- Fixed-percentage allocation per trade
- Maximum simultaneous trades (leverage cap)
- Per-ticker exposure limit (concentration risk)
- Heartbeat equity curve for smooth visualization
- Markdown report generation

Usage:
    from capital_allocation_simulator import run_simulation

    history_df = run_simulation(
        trades_file='backtest_trades.csv',
        initial_capital=100_000.0,
        allocation_pct=0.04,          # 4% per trade
        max_leverage=2.0,             # 200% = 50 simultaneous trades at 4%
        max_per_ticker=2,             # Max 2 concurrent trades per ticker
        output_md='report.md',
        output_history_csv='equity_history.csv',
    )
"""

import pandas as pd
import numpy as np
import os


def run_simulation(
    trades_file: str,
    initial_capital: float = 100_000.0,
    allocation_pct: float = 0.04,
    max_leverage: float = 2.0,
    max_per_ticker: int = 2,
    output_md: str | None = None,
    output_history_csv: str | None = None,
) -> pd.DataFrame:
    """
    Simulate capital allocation over a sequence of trades.

    Parameters
    ----------
    trades_file : str
        Path to semicolon-delimited CSV with columns:
        Pair, Entry Date, Exit Date, PnL, Type.
    initial_capital : float
        Starting equity.
    allocation_pct : float
        Fraction of current equity allocated per trade (e.g. 0.04 = 4%).
    max_leverage : float
        Maximum total exposure as a multiple of capital
        (e.g. 2.0 = 200% → max_active = leverage / allocation_pct).
    max_per_ticker : int
        Maximum simultaneous trades involving the same ticker.
    output_md : str or None
        If provided, write a Markdown summary report to this path.
    output_history_csv : str or None
        If provided, write the equity history DataFrame to this CSV.

    Returns
    -------
    DataFrame with columns: time, equity, active_trades
    """
    if not os.path.exists(trades_file):
        raise FileNotFoundError(f"Trades file not found: {trades_file}")

    df = pd.read_csv(trades_file, sep=";")
    df["Entry Date"] = pd.to_datetime(df["Entry Date"])
    df["Exit Date"]  = pd.to_datetime(df["Exit Date"])

    # Build event list (ENTRY + EXIT per trade)
    events = []
    for idx, row in df.iterrows():
        events.append({"time": row["Entry Date"], "type": "ENTRY", "trade_id": idx,
                        "pnl_unit": row["PnL"], "pair": row["Pair"]})
        events.append({"time": row["Exit Date"],  "type": "EXIT",  "trade_id": idx,
                        "pnl_unit": row["PnL"], "pair": row["Pair"]})

    # EXIT before ENTRY on same timestamp (free up capital first)
    events.sort(key=lambda x: (x["time"], 0 if x["type"] == "EXIT" else 1))

    max_active_trades = int(max_leverage / allocation_pct)
    current_equity    = initial_capital
    active_trades: dict = {}
    history = []

    accepted_count = skipped_count = skipped_exposure_count = 0

    for event in events:
        # Heartbeat: fill gaps > 7 days for smooth equity curve
        if history:
            last_time = history[-1]["time"]
            if (event["time"] - last_time).days > 7:
                history.append({
                    "time": last_time + pd.Timedelta(days=7),
                    "equity": current_equity,
                    "active_trades": len(active_trades),
                })

        if current_equity <= 0 or np.isnan(current_equity):
            current_equity = 0
            history.append({"time": event["time"], "equity": 0.0, "active_trades": 0})
            break

        if event["type"] == "ENTRY":
            pair_tickers = event["pair"].split("-")

            # Concentration check
            exposure_blocked = False
            for ticker in pair_tickers:
                count = sum(1 for t in active_trades.values() if ticker in t["pair"].split("-"))
                if count >= max_per_ticker:
                    exposure_blocked = True
                    break

            if exposure_blocked:
                skipped_exposure_count += 1
                continue

            if len(active_trades) < max_active_trades:
                allocation = current_equity * allocation_pct
                active_trades[event["trade_id"]] = {"allocation": allocation, "pair": event["pair"]}
                accepted_count += 1
                history.append({"time": event["time"], "equity": current_equity,
                                 "active_trades": len(active_trades)})
            else:
                skipped_count += 1

        elif event["type"] == "EXIT":
            if event["trade_id"] in active_trades:
                trade_data = active_trades.pop(event["trade_id"])
                alloc = trade_data["allocation"]
                capped_pnl = max(event["pnl_unit"], -1.0)  # Max loss = 100% of allocation
                current_equity += alloc * capped_pnl
                history.append({"time": event["time"], "equity": current_equity,
                                 "active_trades": len(active_trades)})

    history_df = pd.DataFrame(history)

    # ── Markdown Report ────────────────────────────────────────────────────────
    if output_md:
        final_return_pct = (current_equity / initial_capital - 1) * 100
        md = f"""# Capital Allocation Report ({allocation_pct*100:.1f}% Risk / {max_leverage*100:.0f}% Leverage)

## Parameters
| Parameter | Value |
|-----------|-------|
| Initial Capital | R$ {initial_capital:,.2f} |
| Allocation per Trade | {allocation_pct*100:.1f}% |
| Max Leverage | {max_leverage*100:.0f}% ({max_active_trades} simultaneous trades) |
| Max per Ticker | {max_per_ticker} |

## Results
| Metric | Value |
|--------|-------|
| Final Equity | **R$ {current_equity:,.2f}** |
| Total Return | **{final_return_pct:.2f}%** |
| Net Profit | R$ {current_equity - initial_capital:,.2f} |
| Accepted Trades | {accepted_count} |
| Skipped (No Margin) | {skipped_count} |
| Skipped (Exposure) | {skipped_exposure_count} |
"""
        os.makedirs(os.path.dirname(output_md) if os.path.dirname(output_md) else ".", exist_ok=True)
        with open(output_md, "w", encoding="utf-8") as f:
            f.write(md)

    # ── History CSV ────────────────────────────────────────────────────────────
    if output_history_csv and not history_df.empty:
        os.makedirs(os.path.dirname(output_history_csv) if os.path.dirname(output_history_csv) else ".", exist_ok=True)
        history_df.to_csv(output_history_csv, index=False)

    return history_df
