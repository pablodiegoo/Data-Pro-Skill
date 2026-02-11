---
description: Architecture rules for Data Pro project structure
---

# Architecture Rules

## Central Feature Definitions
> Feature lists (predictors, targets, demographics) used in multiple scripts MUST be defined in `dictionary.py` using `FEATURE_GROUPS` and imported — never hardcoded in each script.

**Why**: Hardcoded predictor lists like `predictors = ['P14_...', 'P15_...']` appearing in 3+ scripts create maintenance risk and divergence.

**How**:
```python
# dictionary.py
FEATURE_GROUPS = {
    'satisfaction': ['P14_Eval_Attractions', 'P15_Eval_Beaches', ...],
    'demographics': ['P1_Relation', 'P4_Age', 'P5_Gender', ...],
}

# analysis script
from scripts.utils.dictionary import FEATURE_GROUPS
predictors = FEATURE_GROUPS['satisfaction']
```
