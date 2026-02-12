# Causal Inference & Driver Analysis Reference

## 1. Drivers Analysis (Regression)
Identifies relative importance of independent variables (X) on a dependent variable (Y).

### Methodology
- **Logistic Regression**: Used when Y is binary (e.g., NPS Detractor vs non-Detractor).
- **Linear Regression**: Used when Y is continuous (e.g., Satisfaction Score).
- **Interpretation**: Coefficients indicate the "Power" of each driver. Higher coefficients = stronger impact.

## 2. Chi-Square Residuals
Identifies statistically significant patterns in cross-tabulations.

### Interpretation
- **Standardized Residual > 1.96**: Significant over-representation (positive association).
- **Standardized Residual < -1.96**: Significant under-representation (negative association).
- **Usage**: Mapping segments to specific behaviors or demographics.

## 3. Residual Segmentation (Deep Dive)
A technique to find outlier groups based on expectations.

### Workflow
1.  **Fit Model**: `Overall_Satisfaction ~ [Perception_Attributes]`.
2.  **Calculate Residuals**: `Actual - Predicted`.
3.  **Categorize**:
    - **Positive Residual > Threshold**: "Delighted" (Happier than their attribute scores would suggest).
    - **Negative Residual < -Threshold**: "Disappointed" (Angrier than their attribute scores suggest).
    - **Near Zero**: "Aligned".

## 4. Association Matrix
A strategic visualization combining multiple Chi-Square tests between a set of attributes (at a specific performance level, usually "Top-Box") and the target variable segments.
