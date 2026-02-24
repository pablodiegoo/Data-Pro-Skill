# Causal Inference & Drivers Reference

Methodologies for identifying the "Why" behind the data through regression and association modeling.

## 1. Drivers Analysis
Identifies which independent variables (X) have the strongest impact on an outcome (Y, e.g., NPS).
- **Script**: `scripts/drivers_analysis.py`
- **Technique**: Multiple Linear/Logistic Regression with standardized coefficients.

## 2. Expectation Analysis (Residuals)
Segments respondents by comparing their actual satisfaction to what was predicted by a model.
- **Script**: `scripts/residual_segmentation.py`
- **Segments**:
  - **Disappointed**: Lower than predicted.
  - **Aligned**: As predicted.
  - **Delighted**: Higher than predicted.

## 3. Association Matrices
Maps hidden correlations between categories using Chi-Square residuals.
- **Scripts**: `scripts/chi2_residuals.py`, `scripts/association_matrix.py`
- **Utility**: Finds which demographics are significantly "attached" to certain segments or behaviors.

---
> [!NOTE]
> Interaction effects between drivers should be checked if the regression R² is low.
