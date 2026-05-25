# Workflow: Standard Data Asset Tiering

For data-intensive survey projects, we propose a 3-tier structure for `assets/database/`.

## Proposed Structure
1.  **`assets/database/raw/`**: Permanent, immutable raw files (CSV, Excel).
2.  **`assets/database/intermediate/`**: High-performance binary formats (Parquet) for cleaned, weighted, and indexed datasets used in exploration.
3.  **`assets/database/results/`**: Final, lightweight analysis tables (CSV, JSON) used directly in reports and dashboards.

## Benefits
-   **Performance**:
    - **raw/**: Direct from source (CSV/XLSX).
    - **intermediate/**: Prepared by **`@data-manipulation`** (Parquet).
    - **results/**: Analyzed by **`@survey-analytics`** or **`@causal-inference`** (Tables/JSON).
    Reading Parquet from `intermediate/` is 10x-50x faster than raw CSV during iterative analysis.
-   **Auditability**: Keeping raw files immutable ensures reproducibility.
-   **Reporting**: Separating final results prevents cluttering the code with data-processing logic during visualization.
