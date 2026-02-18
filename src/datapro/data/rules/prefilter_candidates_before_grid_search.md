# Rule: Pre-filter Candidates Before Grid Search

## Problem

When performing a grid search over model parameters (e.g., hyperparameters, business rules), it is often inefficient to execute heavy validation tests (e.g., stationarity tests, correlation checks, stability tests) at every single iteration of the grid.

Executing these tests inside the inner loop results in a complexity of **O(n_params × n_candidates × T)**, which can take hours or days for large grids.

## Rule

> **Always pre-filter candidates once before entering the grid search loop.**
> Save the valid candidates to an intermediate file or set and reuse them throughout the grid.

## Correct Implementation

```python
# STEP 1: Validate candidates once (using base parameters)
valid_candidates_file = 'db/metadata/validated_candidates.csv'
if not os.path.exists(valid_candidates_file):
    valid_list = run_validation(all_candidates, use_heavy_test=True)
    pd.Series(valid_list).to_csv(valid_candidates_file, index=False)

valid_keys = set(pd.read_csv(valid_candidates_file).iloc[:, 0])

# STEP 2: Filter the universe
candidates_filtered = all_candidates[all_candidates['ID'].isin(valid_keys)]

# STEP 3: Grid search WITH filtered universe and WITHOUT heavy tests (already validated)
for p1 in [0.5, 1.0, 1.5]:
    for p2 in [10, 20, 30]:
        run_model(candidates_filtered, param1=p1, param2=p2, 
                  skip_heavy_test=True)  # ← Critical optimization
```

## Measured Impact

| Approach | Execution Time (45 combinations) |
|---|---|
| Test in every iteration | ~45 hours |
| Pre-filtered universe | ~2 hours |
| **Speedup** | **~22×** |

## When Not to Apply

- When the valid universe changes based on the grid parameters (e.g., grid search over a parameter that affects the validation test itself).
- When the data period varies throughout the grid.

## Tags

`performance`, `optimization`, `grid-search`, `best-practices`
