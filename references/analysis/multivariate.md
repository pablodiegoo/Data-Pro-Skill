# Multivariate Analysis Reference

Advanced techniques for sample weighting and pattern discovery in multi-attribute datasets.

## 1. Sample Weighting (Raking)
Corrects disproportionate samples to match universe targets.
- **Script**: `scripts/weighting.py`
- **Pattern**: Iterative Proportional Fitting (IPF).

## 2. Dimensionality Reduction (PCA & Factor Analysis)
Simplifies dozens of attributes into a few core themes.
- **Scripts**: `scripts/factor_analysis.py`, `scripts/survey_pca.py`
- **PCA**: Best for variance-based reduction.
- **Factor Analysis**: Best for identifying latent psychological constructs (e.g., "Brand trust", "Product value").

## 3. Segmentation (Clustering)
Finds natural groupings of respondents based on behaviors or attitudes.
- **Script**: `scripts/clustering.py`
- **Algorithm**: K-Means clustering with optimal cluster detection (Elbow/Silhouette).

## 4. Optimization (TURF)
Total Unduplicated Reach and Frequency.
- **Script**: `scripts/turf_analysis.py`
- **Goal**: Find the minimum set of items (products, channels) that reaches the maximum number of unique people.

---
> [!IMPORTANT]
> Scale standardization is mandatory before running Factor Analysis or Clustering.
