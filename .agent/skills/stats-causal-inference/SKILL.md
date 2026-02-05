---
name: stats-causal-inference
description: "Advanced statistical modeling to look for drivers and causality. Uses logistic regression and coefficients to determine what impacts an outcome."
---

# Stats Causal Inference Skill

This skill allows the agent to go beyond "Correlation" and look for "Causality" (or at least strong directional drivers).

## Scripts

### `drivers_analysis.py`
Runs a logistic regression (or linear) to identify which independent variables (X) drive the dependent variable (Y).

**Usage**:
```bash
python3 .agent/skills/stats-causal-inference/scripts/drivers_analysis.py data.csv --target "NPS_Class" --predictors "sat_price,sat_quality,sat_service"
```

**Output**:
- Coefficient Table (Impact)
- Odds Ratios (for Logistic)
- Model Fit (R-squared / Pseudo-R2)
