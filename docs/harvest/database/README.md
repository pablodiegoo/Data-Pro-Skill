# Database Harvest - Festival Verão 2026

This directory contains additions for the Data-Pro-Max internal database (`datapro` CLI):

1. **`new_snippets.json`**:
   - **DuckDB Fuzzy CSV Header Mapping**: A crucial snippet for handling messy SurveyMonkey/Qualtrics exports without pandas chunking errors.
   - **Chi-Squared Residual Heatmap**: A visualization snippet for identifying statistical anomalies in crosstabs.

2. **`new_analysis_types.csv`**:
   - Registers new advanced capabilities like `"adv_analytics_gen"` (Advanced Analytics Generator) and `"eda_notebook_gen"` to the system so the AI knows these scripts exist and can trigger them.
