---
description: Standard workflow for end-to-end Survey Analysis (Discovery -> Reporting)
---

# Survey Analysis Pipeline

This workflow outlines the standard operating procedure for analyzing survey data (e.g., Sebrae projects) using the Agent's specialized skills.

## 1. Discovery & Context
**Goal**: Understand the project scope and set up the environment.

1.  **Context Optimization**:
    - Run `/context-optimizer` to decompose large docs (OS, Questionnaire).
    - Populate `.agent/memory/project_facts.md` with Universe targets and Sample info.

## 2. Data Preparation
**Goal**: Clean raw data and map variable names using DuckDB for high-performance processing.

1.  **Dictionary Mapping**:
    - If you have an Excel dictionary:
      ```bash
      # Use dictionary-mapper skill
      python3 .agent/skills/dictionary-mapper/scripts/parse_excel.py dict.xlsx ...
      ```
    - If raw CSV has questions in header (SurveyMonkey/Forms):
      ```bash
      python3 .agent/skills/dictionary-mapper/scripts/infer_from_csv.py raw.csv
      ```
2.  **Cleaning Script (DuckDB Pipeline)**:
    - Create `01_data_prep.py` leveraging `duckdb-sql-master`.
    - Import raw data (CSV/Excel) efficiently:
      ```python
      import duckdb
      con = duckdb.connect('data_pipeline.duckdb')
      con.sql("CREATE TABLE raw AS SELECT * FROM read_csv_auto('raw_data.csv')")
      ```
    - Apply data cleaning and mapping using optimized SQL transformations.
    - Export processed data to Parquet for performance:
      ```python
      con.sql("COPY (SELECT * FROM clean_data) TO 'db_cleaned.parquet' (FORMAT 'PARQUET')")
      ```

## 3. Data Validation (Gatekeeper)
**Goal**: Ensure data is chemically pure before analysis using SQL checks.

1.  **Run Validation (SQL)**:
    - Use DuckDB to query for anomalies directly on the Parquet file:
    - Check for missing values in critical columns (e.g., `SELECT count(*) FROM db_cleaned.parquet WHERE Weight IS NULL`).
    - Verify logic consistency (e.g., `SELECT * FROM db_cleaned.parquet WHERE Age < 18`).
    - Check for duplicates.
    - **Stop** if critical errors found.

## 4. Weighting (Raking)
**Goal**: Adjust sample to match population targets.

1.  **Define Targets**: Extract targets from `project_facts.md` (e.g., Size, Sector, Region).
2.  **Run Weighting**:
    - Create `02_weighting.py` importing `survey-stats`.
    - Load data via DuckDB: `df = duckdb.sql("SELECT * FROM 'db_cleaned.parquet'").df()`
    ```python
    from scripts.weighting import rake_weights
    df['weight'] = rake_weights(df, targets)
    ```

## 5. Analysis & Visuals
**Goal**: Generate insights and charts using DuckDB for heavy lifting.

1.  **Crosstabs (DuckDB Aggregation)**:
    - Use SQL for weighted aggregations and crosstabs (faster than Pandas for large datasets).
    - Example:
      ```sql
      SELECT Sector, SUM(Weight) as WeightedCount 
      FROM 'db_weighted.parquet' 
      GROUP BY Sector
      ```
2.  **Charts**:
    - Generate breakdown charts (Sector, Size) using `matplotlib`/`seaborn` from the aggregated results.
    - Save to `Assets/Results/`.

## 5.1 Advanced Analysis (Optional but Recommended)
**Goal**: Go beyond descriptive. Identify causality and hidden patterns.

1.  **Key Driver Analysis** (Residual Regression):
    - Create `02_analysis_residuals.py` using `stats-causal-inference` skill (`drivers_analysis.py`).
    - Output: Importance vs Performance matrix (`assets/images/residuals/`).

2.  **Ipsative Analysis** (Halo Effect Removal):
    - Create `02_analysis_ipsative.py` using `marketing-science-metrics` skill.
    - Output: True relative importance after bias removal.

3.  **Deep Dive** (Residual Segmentation):
    - Create `02_analysis_deep_dive.py` using `stats-causal-inference` skill (`residual_segmentation.py`).
    - Output: Disappointed/Delighted segment profiles.

4.  **Chi-Square Profiling**:
    - Create `02_analysis_chi2.py` using `stats-causal-inference` skill (`chi2_residuals.py`).
    - Output: Significant demographic associations with segments.

5.  **Clustering** (Optional):
    - Create `02_analysis_clustering.py` using `data-pro-max` skill.
    - Output: Visitor segments with radar profiles.

## 6. Reporting
**Goal**: Compile the final deliverable.

1.  **Draft Report**: Write `report.md` referencing the generated charts.
2.  **Compile**:
    ```bash
    # For Final PDF
    python3 .agent/skills/report-writer/scripts/compile_report.py report.md --format pdf --color "005c9e"
    ```
