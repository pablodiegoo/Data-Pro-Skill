# Database Enhancement Proposals

## Overview
This document proposes enhancements to the `datapro` CLI intelligence based on patterns observed in the Practical Statistics for Data Scientists repository.

---

## 1. New Code Snippets

### Snippet: Weighted Statistics
**Category**: Exploratory Data Analysis  
**Use Case**: Computing weighted means and medians when observations have different importance

```json
{
  "id": "weighted_statistics",
  "title": "Weighted Mean and Median",
  "description": "Calculate weighted statistics when observations have different importance or sample sizes",
  "tags": ["statistics", "weighted", "eda", "descriptive"],
  "code": "import numpy as np\nimport wquantiles\n\n# Weighted mean\nweighted_mean = np.average(df['value'], weights=df['weight'])\n\n# Weighted median (requires wquantiles package)\nweighted_median = wquantiles.median(df['value'], weights=df['weight'])\n\nprint(f'Weighted Mean: {weighted_mean:.2f}')\nprint(f'Weighted Median: {weighted_median:.2f}')",
  "dependencies": ["numpy", "wquantiles"]
}
```

### Snippet: Trimmed Mean
**Category**: Robust Statistics  
**Use Case**: Computing mean while removing outliers from both tails

```json
{
  "id": "trimmed_mean",
  "title": "Trimmed Mean (Robust Central Tendency)",
  "description": "Calculate mean after removing a percentage of extreme values from both tails",
  "tags": ["statistics", "robust", "outliers", "eda"],
  "code": "from scipy.stats import trim_mean\n\n# Remove 10% from each tail (20% total)\ntrimmed_avg = trim_mean(df['value'], proportiontocut=0.1)\n\nprint(f'Trimmed Mean (10% each tail): {trimmed_avg:.2f}')\nprint(f'Regular Mean: {df[\"value\"].mean():.2f}')\nprint(f'Difference: {abs(trimmed_avg - df[\"value\"].mean()):.2f}')",
  "dependencies": ["scipy"]
}
```

### Snippet: Median Absolute Deviation (MAD)
**Category**: Robust Statistics  
**Use Case**: Robust measure of variability, alternative to standard deviation

```json
{
  "id": "mad_statistic",
  "title": "Median Absolute Deviation (MAD)",
  "description": "Robust measure of variability that is resistant to outliers",
  "tags": ["statistics", "robust", "variability", "outliers"],
  "code": "from statsmodels import robust\n\n# Using statsmodels\nmad_value = robust.scale.mad(df['value'])\n\n# Manual calculation\nmedian_val = df['value'].median()\nmad_manual = abs(df['value'] - median_val).median() / 0.6744897501960817\n\nprint(f'MAD: {mad_value:.2f}')\nprint(f'Standard Deviation: {df[\"value\"].std():.2f}')\nprint(f'MAD is more robust to outliers')",
  "dependencies": ["statsmodels"]
}
```

### Snippet: Permutation Test
**Category**: Hypothesis Testing  
**Use Case**: Non-parametric hypothesis test without distributional assumptions

```json
{
  "id": "permutation_test",
  "title": "Permutation Test (Two Groups)",
  "description": "Non-parametric hypothesis test comparing two groups without assuming normality",
  "tags": ["statistics", "hypothesis-testing", "non-parametric", "permutation"],
  "code": "import numpy as np\nimport random\n\ndef permutation_test(group_a, group_b, n_permutations=10000):\n    # Observed difference\n    observed_diff = np.mean(group_b) - np.mean(group_a)\n    \n    # Combine groups\n    combined = np.concatenate([group_a, group_b])\n    n_a, n_b = len(group_a), len(group_b)\n    \n    # Permutation distribution\n    perm_diffs = []\n    for _ in range(n_permutations):\n        shuffled = np.random.permutation(combined)\n        perm_a = shuffled[:n_a]\n        perm_b = shuffled[n_a:]\n        perm_diffs.append(np.mean(perm_b) - np.mean(perm_a))\n    \n    # P-value\n    p_value = np.mean(np.abs(perm_diffs) >= np.abs(observed_diff))\n    \n    return {'observed_diff': observed_diff, 'p_value': p_value}\n\nresult = permutation_test(df[df['group']=='A']['value'].values, \n                          df[df['group']=='B']['value'].values)\nprint(f\"Observed difference: {result['observed_diff']:.2f}\")\nprint(f\"P-value: {result['p_value']:.4f}\")",
  "dependencies": ["numpy"]
}
```

### Snippet: Correlation Ellipse Plot
**Category**: Visualization  
**Use Case**: Grayscale-friendly correlation matrix visualization

```json
{
  "id": "correlation_ellipse",
  "title": "Correlation Matrix with Ellipses",
  "description": "Visualize correlation matrix using ellipses (grayscale-friendly)",
  "tags": ["visualization", "correlation", "grayscale", "publication"],
  "code": "# See assets/harvest/scripts/correlation_ellipse_plot.py\nfrom correlation_ellipse_plot import plot_corr_ellipses\nimport matplotlib.pyplot as plt\n\ncorr_matrix = df.corr()\nm, ax = plot_corr_ellipses(corr_matrix, figsize=(8, 8), cmap='bwr_r')\ncb = plt.colorbar(m, ax=ax)\ncb.set_label('Correlation coefficient')\nplt.title('Correlation Matrix')\nplt.tight_layout()\nplt.show()",
  "dependencies": ["matplotlib", "numpy", "pandas"]
}
```

### Snippet: Partial Residual Plot
**Category**: Regression Diagnostics  
**Use Case**: Diagnose nonlinearity in regression models

```json
{
  "id": "partial_residual_plot",
  "title": "Partial Residual Plot",
  "description": "Diagnostic plot for detecting nonlinearity in individual predictors",
  "tags": ["regression", "diagnostics", "nonlinearity", "visualization"],
  "code": "# See assets/harvest/scripts/partial_residual_plot.py\nfrom partial_residual_plot import partial_residual_plot\nimport statsmodels.formula.api as smf\nimport matplotlib.pyplot as plt\n\n# Fit model\nmodel = smf.ols('y ~ x + np.power(x, 2)', data=df).fit()\n\n# Create partial residual plot\nfig, ax = plt.subplots(figsize=(8, 6))\npartial_residual_plot(model, df, 'y', 'x', ax)\nplt.title('Partial Residual Plot: Checking for Nonlinearity')\nplt.show()",
  "dependencies": ["statsmodels", "matplotlib", "pandas"]
}
```

---

## 2. New Analysis Types

### Analysis Type: Robust Exploratory Analysis
**Description**: Exploratory data analysis using robust statistics resistant to outliers

```csv
analysis_type,description,typical_methods,when_to_use
robust_eda,"Exploratory analysis using robust statistics","Trimmed mean, MAD, median, IQR","Data with outliers, skewed distributions, small samples"
```

### Analysis Type: Permutation-Based Inference
**Description**: Hypothesis testing using resampling methods without distributional assumptions

```csv
analysis_type,description,typical_methods,when_to_use
permutation_inference,"Non-parametric hypothesis testing via resampling","Permutation tests, bootstrap, randomization tests","Small samples, non-normal data, exact p-values needed"
```

### Analysis Type: Weighted Regression
**Description**: Regression analysis with observation-specific weights

```csv
analysis_type,description,typical_methods,when_to_use
weighted_regression,"Regression with heterogeneous observation importance","WLS, weighted OLS, robust regression","Varying data quality, heteroskedasticity, time-varying precision"
```

---

## 3. New Reasoning Rules

### Rule: Suggest Robust Statistics for Outliers
```csv
rule_id,condition,suggestion,priority
robust_stats_outliers,"Outliers detected (>5% beyond 3 IQR)","Consider using robust statistics: trimmed mean, MAD, median instead of mean/std",high
```

### Rule: Suggest Permutation Test for Small Samples
```csv
rule_id,condition,suggestion,priority
permutation_small_sample,"Sample size < 30 and normality questionable","Consider permutation test instead of t-test for exact p-values",medium
```

### Rule: Suggest Weighted Regression for Time Series
```csv
rule_id,condition,suggestion,priority
weighted_time_series,"Time series data with varying quality over time","Consider weighted regression with higher weights for recent data",medium
```

### Rule: Suggest Partial Residual Plot for Polynomial Terms
```csv
rule_id,condition,suggestion,priority
partial_resid_polynomial,"Polynomial terms in regression model","Use partial residual plots to validate polynomial necessity",high
```

---

## 4. Integration Priority

### High Priority
1. **Weighted statistics snippet** - Common need, simple implementation
2. **Trimmed mean snippet** - Robust alternative to mean
3. **Robust statistics rule** - Helps users handle outliers better

### Medium Priority
4. **Permutation test snippet** - Educational value, fills gap
5. **MAD statistic snippet** - Robust variability measure
6. **Weighted regression analysis type** - Specialized but useful

### Low Priority
7. **Correlation ellipse snippet** - Niche use case (grayscale publications)
8. **Partial residual plot snippet** - Advanced diagnostic

---

## 5. Implementation Notes

### Dependencies to Add
- `wquantiles`: For weighted median calculations
- Already have: `scipy`, `statsmodels`, `numpy`, `pandas`

### Documentation Updates
- Add "Robust Statistics" section to analysis guide
- Add "Permutation Tests" to hypothesis testing guide
- Add "Weighted Regression" to regression guide

### Testing
- Create unit tests for new snippets
- Validate snippet code runs without errors
- Test with sample datasets

---

## 6. Example User Queries

These snippets should trigger on queries like:

- "How do I calculate a weighted average?"
- "What's a robust alternative to mean?"
- "How to handle outliers in my data?"
- "Non-parametric test for comparing groups"
- "Test without assuming normality"
- "Weighted regression in Python"
- "Check for nonlinearity in regression"

---

## References

- Practical Statistics for Data Scientists (2nd ed.), O'Reilly 2020
- Robust Statistics: The Approach Based on Influence Functions, Wiley 1986
- Good, P. (2005). Permutation, Parametric and Bootstrap Tests of Hypotheses
