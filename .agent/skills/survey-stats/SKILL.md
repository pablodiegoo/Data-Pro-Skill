---
name: survey-stats
description: "Advanced statistical toolset for analyzing survey data. Includes capabilities for Sample Weighting (Raking), Factor Analysis, PCA, and Clustering (K-Means). Use this when you need to perform quantitative analysis on survey datasets."
---

# Survey Stats

This skill provides a suite of statistical tools optimized for market research and survey analysis. It covers the end-to-end workflow from weighting sample data to extracting deep insights via multivariate analysis.

## Core Capabilities

### 1. Sample Weighting (`weighting.py`)
Adjusts your sample to match population targets using Iterative Proportional Fitting (Raking).

**Usage:**
```python
from scripts.weighting import rake_weights

targets = {
    'gender': {'Male': 0.49, 'Female': 0.51},
    'region': {'North': 0.2, 'South': 0.8}
}
df['final_weight'] = rake_weights(df, targets)
```

### 2. Factor Analysis (`factor_analysis.py`)
Reduces large sets of variables (e.g., Likert scales) into latent factors. Useful for identifying underlying themes in "Importance" or "Satisfaction" batteries.

**Usage:**
```python
from scripts.factor_analysis import run_factor_analysis

# Select numerical columns (Likert scale 1-5)
cols = ['q1_sat', 'q2_sat', 'q3_sat', ...]
loadings, variance = run_factor_analysis(df, cols)
```

### 3. Clustering / Segmentation (`clustering.py`)
Groups respondents into homogeneous segments based on behavior or attitudes using K-Means.

**Usage:**
```python
from scripts.clustering import run_segmentation

cols_to_segment = ['factor1_score', 'factor2_score']
df_segmented = run_segmentation(df, cols_to_segment, n_clusters=4)
```

### 4. TURF Analysis (`turf_analysis.py`)
Calculates the Total Unduplicated Reach and Frequency. Perfect for optimizing product lines or communication channels.

**Usage:**
```python
from scripts.turf_analysis import run_turf_analysis

items = ['Channel_A', 'Channel_B', 'Channel_C']
turf_res = run_turf_analysis(df, items, n_max_size=3)
print(turf_res)
```

### 5. Survey PCA (`survey_pca.py`)
Principal Component Analysis tailored for survey data, including support for standard Likert scales AND multi-response (string-split) data.

**Usage:**
```python
from scripts.survey_pca import run_survey_pca

# For multi-response columns like "ItemA;ItemB"
cols = ['multi_resp_q1', 'multi_resp_q2']
loadings, scores, var = run_survey_pca(df, cols, sep=';')
```

### 6. Weighted Visuals (`visuals.py`)
Helper functions to generate correct weighted bar charts rapidly.

**Usage:**
```python
from scripts.visuals import plot_weighted_bars

cols = ['Brand_A', 'Brand_B']
plot_weighted_bars(df, cols, "Brand Usage", "chart_brand.png", weight_col='Weight')
```

## Dependencies
Ensure the data analysis stack is installed:
```bash
pip install pandas numpy scikit-learn factor_analyzer matplotlib seaborn
```

## Workflow Example (Phase 2 Analysis)

1. **Load Data**: Load the `csv` or `sav` file.
2. **Weighting**: Define universe targets (from project specs) and calculate weights.
3. **Factor Analysis/PCA**: Reduce 20+ "Benefit" attributes to 3-4 distinct dimensions.
4. **Segmentation**: Cluster users based on these 3-4 dimensions to find "Personas".
5. **TURF**: Optimize the feature set for the new product.
6. **Visuals**: Export weighted charts for the final PDF report.
