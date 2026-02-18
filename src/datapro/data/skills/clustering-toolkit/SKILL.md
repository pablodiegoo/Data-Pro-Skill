---
name: clustering-toolkit
description: "Advanced clustering and grouping toolkit using PCA and DBSCAN. Provides a complete pipeline for identifying homogeneous groups in high-dimensional data with built-in quality diagnostics and stability metrics. Use for: (1) Grouping similar entities (assets, products, clients) based on multi-dimensional features, (2) Principal Component Analysis for dimensionality reduction, (3) DBSCAN clustering with noise filtering, (4) Diagnosing clustering pathologies like giant cluster ratio or configuration instability."
---

# Clustering Toolkit Skill

This skill provides a specialized pipeline for identifying homogeneous groups within high-dimensional datasets. It combines dimensionality reduction (PCA) with density-based clustering (DBSCAN) to find natural patterns while filtering noise.

## Capabilities

### 1. PCA+DBSCAN Grouping (`pca_dbscan_grouping`)
A hybrid pipeline that uses Principal Component Analysis to extract features and DBSCAN to group entities.
- Supports hybrid features (numerical + categorical weights).
- Configurable walk-forward clustering for dynamic datasets.
- Automatic noise detection (outliers).

### 2. Basic Segmentation (`basic_clustering`)
Standard K-Means clustering pipeline for rapid entity grouping.
- Automated feature scaling.
- Configurable cluster count (`k`).
- Centroid analysis for segment profiling.

### 3. Residual Segmentation (`residual_segmentation`)
Advanced behavioral segmentation using regression residuals (Actual vs. Predicted).
- Identifies "Delighted" vs "Disappointed" segments based on unmeasured variables.
- Automated distribution plotting and coefficient analysis.

### 4. Gower Distance Matrix (`gower_distance`)
Similarity metric for mixed data types (numerical + categorical).
- Handles NaNs gracefully.
- Core component for distance-based clustering when one-hot encoding is undesirable.

### 2. Cluster Quality Diagnostics (`dbscan_cluster_quality`)
Utilities to detect common clustering pathologies.
- **Giant Cluster Ratio**: Detects if a single group dominates the universe (>50%).
- **Stability Metrics**: Measures how often entities change groups over time.
- **Configuration Scoring**: Scalar metric to rank different hyperparameter (EPS, MinSamples) setups.

## Usage

```python
from scripts.pca_dbscan_grouping import PCA_DBSCAN_Pipeline
from scripts.dbscan_cluster_quality import calculate_cluster_metrics

# 1. Run clustering pipeline
pipeline = PCA_DBSCAN_Pipeline(n_components=5, eps=0.015)
clusters = pipeline.fit_predict(df)

# 2. Diagnose quality
metrics = calculate_cluster_metrics(clusters)
if metrics['Giant_Ratio'] > 0.5:
    print("Warning: Pathological giant cluster detected. Reduce EPS.")
```

## Best Practices
- **Feature Scaling**: Always normalize features before PCA.
- **Categorical Weights**: Use `sector_weight` (or equivalent) to balance statistical similarity with domain knowledge.
- **EPS Tuning**: Small changes in `eps` can have drastic effects. Use `grid_search_checkpoint` for tuning.

## Detailed References
- **Methodology**: See [pca_dbscan_methodology.md](references/pca_dbscan_methodology.md) for pipeline, parameters, and diagnostics.

## Dependencies
`scikit-learn`, `pandas`, `numpy`.
