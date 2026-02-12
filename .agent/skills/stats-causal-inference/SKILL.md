---
name: stats-causal-inference
description: "Advanced statistical modeling to look for drivers and causality. Uses logistic regression and coefficients to determine what impacts an outcome."
---

# Stats Causal Inference Skill

This skill provides advanced statistical modeling to identify drivers and hidden associations in survey data.

## Core Procedures
1.  **Drivers Analysis**: Identifying what impacts an outcome using regression.
2.  **Association Mapping**: Using Chi-Square residuals to find significant segments.
3.  **Expectation Analysis**: Using OLS residuals to find "Disappointed" or "Delighted" segments.

## Reference Material
- **Methodology & Interpretation**: See [causal_reference.md](references/causal_reference.md)

## Available Scripts

### `drivers_analysis.py`
Runs regression to identify key drivers.
```bash
python3 .agent/skills/stats-causal-inference/scripts/drivers_analysis.py \
    data.csv --target "Y" --predictors "X1,X2,X3"
```

### `chi2_residuals.py`
Standardized Residuals heatmap for cross-tabulations.
```bash
python3 .agent/skills/stats-causal-inference/scripts/chi2_residuals.py \
    data.parquet --rows "Segment" --cols "Question" --output output_dir
```

### `residual_segmentation.py`
Categorizes respondents by comparing actual vs. predicted satisfaction.
```bash
python3 .agent/skills/stats-causal-inference/scripts/residual_segmentation.py \
    data.parquet --target "Satisfaction" --predictors "A1,A2" --output output_dir
```

### `association_matrix.py`
Maps "High" performance attributes to target segments.
```bash
python3 .agent/skills/stats-causal-inference/scripts/association_matrix.py \
    data.parquet --target "Target" --attributes "A1,A2" --output output_dir
```
