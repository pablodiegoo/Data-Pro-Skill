---
name: stats-causal-inference
description: "Advanced statistical modeling to look for drivers and causality. Uses logistic regression and coefficients to determine what impacts an outcome."
---

# Stats Causal Inference Skill

This skill allows the agent to go beyond "Correlation" and look for "Causality" (or at least strong directional drivers).

## Scripts

### 1. `drivers_analysis.py`
Runs a logistic regression (or linear) to identify which independent variables (X) drive the dependent variable (Y).

```bash
python3 .agent/skills/stats-causal-inference/scripts/drivers_analysis.py \
    data.csv --target "NPS_Class" --predictors "sat_price,sat_quality,sat_service"
```

**Output**: Coefficient Table, Odds Ratios (Logistic), Model Fit (R²/Pseudo-R²).

---

### 2. `chi2_residuals.py`
Chi-Square test of independence + Standardized Residuals heatmap. Identifies statistically significant over/under-representation in cross-tabs.

```bash
python3 .agent/skills/stats-causal-inference/scripts/chi2_residuals.py \
    data.parquet --rows "Cluster_Label" --cols "P5_Gender" --output output/chi2
```

**Python API**:
```python
from chi2_residuals import chi2_residuals
result = chi2_residuals(df, 'Cluster', 'Gender', 'output/chi2', label_map={'Cluster': 'Segmento'})
# Returns dict with chi2, p_value, dof, residuals DataFrame, plot_path, csv_path
# Returns None if p >= 0.05
```

**Output**: Residuals heatmap (PNG), residuals table (CSV).

---

### 3. `residual_segmentation.py`
Deep Dive pattern: Fit Y ~ X → Residual → Segment into Disappointed/Aligned/Delighted → Cross with qualitative data.

> **Prerequisite**: Input data must be **numeric-encoded** (apply SCALE_MAP in `01_prep_data.py` per the "Encode Once" rule).

```bash
python3 .agent/skills/stats-causal-inference/scripts/residual_segmentation.py \
    data.parquet --target "P33_Eval_General" \
    --predictors "P14_Eval_Attractions,P15_Eval_Beaches,P16_Eval_Lagoons" \
    --output output/deep_dive --threshold 0.7
```

**Python API**:
```python
from residual_segmentation import residual_segmentation
result_df = residual_segmentation(df, 'Overall_Score', predictors, 'output/', threshold=0.7)
# Returns DataFrame with Predicted, Residual, Sentiment_Group columns
```

**Output**: Coefficient table (CSV), residual distribution (PNG), segment bar chart (PNG), segmented data (CSV).
