# Project Harvest Overview: Festival Verão 2026

The `/project-harvest` workflow has successfully completed a deep scan of the Festival Verão 2026 project. We have extracted high-value assets ranging from generic notebook generation scripts to advanced statistical pattern implementations. 

## Harvest Summary

### 1. Reusable Scripts (`assets/harvest/scripts/`)
We extracted and generalized 4 major Python scripts that should be ported to `Data-Pro-Max` skills:
- **`eda_notebook_generator.py`**: [High Priority] Automates exploratory data analysis notebooks (distributions, demographics, schema mapping) directly from data files.
- **`advanced_analytics_generator.py`**: [High Priority] Automates complex modeling (Random Forest drivers, Dual Clustering, Pearson/Spearman correlation matrices, Residual Halos) into an interactive notebook.
- **`duckdb_fuzzy_cleaner.py`**: [Medium Priority] Standardizes the ingestion of dirty CSVs (trailing commas, long text headers) using DuckDB and fuzzy dictionary matching.
- **`qualitative_categorizer.py`**: [Medium Priority] Simple, fast rule-engine for categorizing open-ended text based on keyword dictionaries.

### 2. Methodologies & Patterns (`assets/harvest/references/new_methodologies.md`)
We identified 4 highly effective analytical concepts used to deeply understand the survey data:
- **Dual Clustering**: Using K-Means for Personas and DBSCAN for Anomaly/Density detection.
- **Dual Correlation**: Contrasting Pearson (Linear) and Spearman (Rank-based/Likert).
- **The Pure Sentiment Stack**: Using Ipsative centering combined with Linear Regression Residuals to neutralize the Halo Effect in satisfaction scores.
- **Chi-Squared Residual Heatmapping**: Finding surprises in crosstabs using standardized visuals.

### 3. Database Updates (`assets/harvest/database/`)
Prepared additions for the `datapro` CLI:
- **New Snippets (`new_snippets.json`)**: Code templates for DuckDB fuzzy mapping and Chi-Squared Heatmaps.
- **New Analysis Types (`new_analysis_types.csv`)**: Registered notebook generators as formal system capabilities.

### 4. Governance Rules (`assets/harvest/rules/survey_governance.md`)
- **Survey Schema Mapping**: Proposed a strict rule mandating the mapping of raw survey string headers to `snake_case_ids` early in the pipeline, storing the mapping in a JSON, and automatically rendering it as a Glossary in all generated deliverables.

### 5. Workflow Architecture (`assets/harvest/workflows/notebook_generation_pattern.md`)
- **Dual-Layered Notebook Workflow**: Proposed shifting away from writing ad-hoc analysis scripts per project to using a standard, 2-layer Generator Pattern (Basic EDA Generator + Advanced Analytics Generator).

---
## Next Steps
This harvest is complete. The harvested artifacts are ready to be integrated into the core `Data-Pro-Skill` ecosystem upstream via the `/project-evolution` workflow.
