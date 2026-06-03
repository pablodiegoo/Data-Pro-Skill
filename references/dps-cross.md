# /dps-cross [VarX] x [VarY] — Tufte Crosstab

Produces dense contingency tables with automatic statistical test selection.

## Pipeline

```
Raw data + variable pair → Python script → cross_{X}_{Y}.csv + cross_stats.json + cross_report.md
```

## Execution Steps

1. **Parse arguments** — extract X and Y variable names from command
2. **Validate** — both variables exist in data, sufficient N per cell
3. **Select test** via Statistical Test Selector Matrix (see `agents/agent-statistician.md`):
   - 2 categorical: χ² (or Fisher's exact if N<5 per cell)
   - 1 categorical + 1 continuous: t-test (or Mann-Whitney U if non-normal)
   - 2 continuous: Pearson's r (or Spearman's ρ)
4. **Run script**:
   ```bash
   python3 .dps/scripts/crosstabs.py data.csv --index X --columns Y --output .dps/outputs/cross/
   ```
5. **Read output** — load cross table CSV + stats JSON
6. **Render** — Tufte table with N, %, margin of error, test statistic, margin note

## Output Format

| VarX \ VarY | Cat 1 | Cat 2 | Total | N |
|-------------|-------|-------|-------|---|
| Group A | % | % | 100% | N |
| Group B | % | % | 100% | N |

> **Margin Note:** χ²(df, N=X) = value, p < 0.05. Effect size: Cramér's V = 0.XX.

## Flags

- `--test chi2|ttest|anova|pearson`: override automatic test selection
- `--no-test`: skip statistical test, table only
