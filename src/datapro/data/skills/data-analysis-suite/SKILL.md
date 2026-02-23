---
name: data-analysis-suite
description: "Unified suite for end-to-end data analysis (Quantitative, Qualitative, Multivariate, Causal, and Science). Use for: (1) Sample weighting (Raking), (2) Driver analysis and Causality, (3) Marketing & Political science metrics (Halo/Pain Curves), and (4) Survey pipeline automation."
---

# Data Analysis Suite

This super-skill unifies all quantitative and statistical capabilities into a single entry point. It follows a modular structure to maintain context efficiency.

## 1. Domain Entry Points

To avoid context overflow, specific instructions and scripts are organized into these reference modules:

| Domain | Focus Area | Reference File |
| :--- | :--- | :--- |
| **Pipeline** | Preparation & T-Layer | Use `@data-manipulation` |
| **Multivariate** | Weights, PCA & Clusters | [multivariate.md](./references/multivariate.md) |
| **Causal** | Drivers & Associations | [causal.md](./references/causal.md) |
| **Science** | Bias & Specialty Metrics | [science.md](./references/science.md) |
| **Methodologies** | Advanced Harvested Patterns | [new_methodologies.md](./references/new_methodologies.md) |
| **Machine Learning** | Classification & Feature Importance | [imbalanced_data_strategies.md](./references/imbalanced_data_strategies.md) |
| **Strategic** | Priority Matrix & Halo | [priority_matrix.md](./references/priority_matrix.md), [halo_removal.md](./references/halo_removal.md) |

## 2. Integrated Scripts Overview

The following core scripts are available in the `scripts/` directory:

- **Pipeline**: `quant_analyzer.py`, `qual_analyzer.py`, `crosstabs.py`
- **Generators**: `eda_notebook_generator.py`, `advanced_analytics_generator.py`
- **Stats**: `factor_analysis.py`, `survey_pca.py`, `turf_analysis.py`, `permutation_test_utilities.py`
- **Qualitative**: `qualitative_categorizer.py`
- **Diagnostics**: `partial_residual_plot.py`, `glm_partial_residual_plot.py`
- **Causal**: `drivers_analysis.py`, `chi2_residuals.py`, `association_matrix.py`
- **Science**: `halo_removal.py`, `ipsative_analysis.py`, `pain_curves.py`, `disapproval_analysis.py`
- **Strategy**: `priority_matrix.py`, `conversion_funnel.py`
- **ML**: `permutation_feature_importance.py`

> [!NOTE]
> **Segmentation & Clustering**: All clustering-related tasks (K-Means, DBSCAN, Residual Segmentation, Gower Distance) have been migrated to the specialized `@clustering-toolkit`. Use that skill for grouping logic.

## 3. General Best Practices

1. **Standard Input**: Use Parquet for performance and data types persistence (Category/DateTime).
2. **Sequential Flow**: Map -> Clean -> Weight -> Analyze -> Visualize.
3. **Weighting**: Always check if the sample (n) vs. universe targets requires weighting before running multivariate tests.

---
> [!IMPORTANT]
> All analytical output, code comments, and documentation produced by this suite MUST be in **English**.
