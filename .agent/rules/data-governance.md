---
description: Data governance rules for derived columns and data persistence
---

# Data Governance

## Save Derived Columns
> If an analysis script creates a new column (e.g., `Sentiment_Group`, `Cluster_Label`), it MUST save the updated DataFrame back to parquet so downstream scripts can use it.

**Why**: The Deep Dive script calculated `Sentiment_Group` but never persisted it. The Chi² script couldn't use it, causing duplicated logic.

**How**:
```python
# After adding derived column
df['Sentiment_Group'] = ...
df.to_parquet(output_path, index=False)  # ← REQUIRED
print(f"Saved updated data with Sentiment_Group to {output_path}")
```
