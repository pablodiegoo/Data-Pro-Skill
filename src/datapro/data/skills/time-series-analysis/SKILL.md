---
name: time-series-analysis
description: "Comprehensive time-series validation and analysis suite. Handles backtesting of trading and non-trading strategies with support for walk-forward validation (training vs testing windows), performance metric calculation (Sharpe, Drawdown, Win Rate), and event-driven resource allocation simulation. Use for: (1) Validating sequential logic on time-series data, (2) Calculating risk-adjusted performance, (3) Simulating constraints in resource distribution, (4) Detecting look-ahead bias through walk-forward testing."
---

# Time-Series Analysis Skill

This skill provides a robust framework for validating any logic applied to time-series data (financial, operational, or behavioral). It focuses on avoiding look-ahead bias and ensuring statistical robustness through walk-forward validation.

## Capabilities

### 1. Strategy Validation Engine (`time_series_backtest_engine`)
Vectorized engine to simulate decisions over time.
- Supports custom entry/exit logic.
- Implements time-based and threshold-based stops.
- Handles massive datasets via streaming output.

### 2. Resource Allocation Simulator (`resource_allocation_simulator`)
Event-driven simulator to test how resources (capital, inventory, etc.) are distributed across multiple signals.
- Fixed-percentage or dynamic allocation.
- Concentration limits per signal.
- Realistic constraint modeling (leverage caps, minimum allocations).

### 3. Performance Metrics
Calculates standard risk-adjusted return metrics:
- Sharpe Ratio / Sortino Ratio.
- Maximum Drawdown (MDD).
- Win Rate and Expectancy.

## Usage

```python
from scripts.time_series_backtest_engine import run_backtest
from scripts.resource_allocation_simulator import simulate_allocation

# 1. Validate a strategy over historical data
results = run_backtest(
    data=df, 
    entry_threshold=2.0, 
    exit_threshold=0.0,
    stop_loss=3.0
)

# 2. Simulate resource distribution based on signals
sim_report = simulate_allocation(
    trades=results,
    initial_resource=100000,
    max_per_signal=0.1
)
```

## Best Practices
- **Walk-Forward**: Always separate the formation (training) window from the trading (test) window.
- **Look-ahead Bias**: Ensure signals at time `t` only use data available at `t-1`.
- **DPI**: Use `performance_curve_builder` for high-resolution result visualization.

## Detailed References
- **Methodology**: See [time_series_validation_methodology.md](references/time_series_validation_methodology.md) for backtest logic and spread calculation.
- **Metrics**: See [financial_metrics_pairs_trading.md](references/financial_metrics_pairs_trading.md) for financial-specific indicators (Half-Life, Sharpe).
- **Validation**: See [walk_forward_validation.md](references/walk_forward_validation.md) for gold-standard validation patterns.

## Dependencies
`pandas`, `numpy`, `scipy`.
