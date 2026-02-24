# Governance: Explicit Weight Handling in Survey Analysis

In any project involving sample-to-population inference (weighted data), scripts must not assume uniform weights.

## Rule
1.  **Always Define Weights**: If the dataset doesn't have a `weight` column, one must be initialized with `1.0`.
2.  **Weighted Operators**: All aggregations (Mean, Frequency, Correlation) MUST use the `weight` column.
    -   *Bad*: `df['Column'].mean()`
    -   *Good*: `(df['Column'] * df['weight']).sum() / df['weight'].sum()`
3.  **Verification**: The sum of weights must always be compared against the target population (for Raking) or raw N (for weighted samples).

## Rationale
Implicitly assuming uniform weights in a skewed sample leads to significant estimation biases that invalidate project conclusions.
