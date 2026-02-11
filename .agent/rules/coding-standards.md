---
description: Python code quality standards for Data Pro projects
---

# Coding Standards

## Encode Once
> Categorical-to-numeric encoding (e.g., `SCALE_MAP`) MUST be applied in `01_prep_data.py` and persisted to parquet.
> Downstream analysis scripts MUST NOT re-encode from strings.

**Why**: Prevents DRY violations where every script independently maps strings like `"Excelente "` → 5 with inconsistent `.strip()` calls.

**How**: Use `SCALE_COLUMNS` from `dictionary.py` in your prep script:
```python
for col in SCALE_COLUMNS:
    df[col] = df[col].astype(str).str.strip().map(SCALE_MAP)
```

## Close Figures
> Always call `plt.close()` after `plt.savefig()` in headless scripts.

**Why**: Prevents memory accumulation when running scripts in batch pipelines.

```python
plt.savefig(output_path, dpi=150)
plt.close()  # ← REQUIRED

## Pre-Flight Skill Sync Check
> Before creating any new analysis script, MUST verify that the target functionality doesn't already exist in an upstream skill by checking `Data-Pro-Skill/.agent/skills/*/scripts/`.

**Why**: This prevents duplicate work and ensures the project benefits from the latest generic implementations.
```
