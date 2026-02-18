# Workflow: Resilient Grid Search with Checkpoints

## Problem

Long-running grid searches (40+ combinations) are prone to interruptions due to power failures, memory leaks, timeouts, or manual stops. Without a checkpoint mechanism, all progress is lost and the process must restart from the beginning.

## Proposal

> **Every long-running grid search MUST implement an incremental checkpoint mechanism.**
> Save each result immediately after calculation and check the existing results file before executing a new combination.

## Implementation Pattern

```python
import pandas as pd
import os

results_file = 'db/processed/grid_results.csv'

# 1. Load existing results to identify completed combinations
if os.path.exists(results_file):
    existing = pd.read_csv(results_file)
    # Map parameters to a set of tuples for fast lookup
    processed = set(zip(existing['ParamA'], existing['ParamB'], existing['ParamC']))
else:
    processed = set()
    # Initialize file with header
    pd.DataFrame(columns=['ParamA', 'ParamB', 'ParamC', 'Score', 'Metric1']).to_csv(results_file, index=False)

# 2. Grid search with resume capability
for pa in [1, 2, 3]:
    for pb in [10, 20]:
        for pc in ['low', 'high']:
            if (pa, pb, pc) in processed:
                print(f"Skipping ({pa}, {pb}, {pc}): Already processed.")
                continue
            
            # Execute logic
            result = run_heavy_logic(pa, pb, pc)
            
            # Save immediately (append mode)
            row = {'ParamA': pa, 'ParamB': pb, 'ParamC': pc, **result}
            pd.DataFrame([row]).to_csv(results_file, mode='a', header=False, index=False)
            
            processed.add((pa, pb, pc))
            print(f"Completed ({pa}, {pb}, {pc}) → Score: {result['Score']:.4f}")
```

## Benefits

- **Automatic Resume**: Pick up exactly where it left off after an interruption.
- **Real-time Monitoring**: The results file is always valid and reflects current progress.
- **Resource Efficiency**: No wasted compute on already-calculated combinations.

## When to Use

- Any grid search with more than 10-15 combinations.
- Any process that takes more than 30 minutes to complete.
- When working in unstable environments (cloud preemptible instances, spots, etc.).

## Tags

`workflow`, `resilience`, `grid-search`, `automation`, `best-practices`
