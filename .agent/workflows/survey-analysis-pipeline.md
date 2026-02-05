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
**Goal**: Clean raw data and map variable names.

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
2.  **Cleaning Script**:
    - Create `01_data_prep.py`.
    - Apply the mapping generated above.
    - Export to Parquet (e.g., `db_cleaned.parquet`).

## 3. Data Validation (Gatekeeper)
**Goal**: Ensure data is chemically pure before analysis.

1.  **Run Validation**:
    - Check for missing values in critical columns (e.g., Weights, Regions).
    - Verify logic consistency (e.g., Age > 18).
    - Check for duplicates.
    - **Stop** if critical errors found.

## 4. Weighting (Raking)
**Goal**: Adjust sample to match population targets.

1.  **Define Targets**: Extract targets from `project_facts.md` (e.g., Size, Sector, Region).
2.  **Run Weighting**:
    - Create `02_weighting.py` importing `survey-stats`.
    ```python
    from scripts.weighting import rake_weights
    df['weight'] = rake_weights(df, targets)
    ```

## 5. Analysis & Visuals
**Goal**: Generate insights and charts.

1.  **Crosstabs**:
    - Use `survey-stats/scripts/crosstabs.py` to generate weighted tables.
2.  **Charts**:
    - Generate breakdown charts (Sector, Size) using `matplotlib`/`seaborn`.
    - Save to `Assets/Results/`.

## 6. Reporting
**Goal**: Compile the final deliverable.

1.  **Draft Report**: Write `report.md` referencing the generated charts.
2.  **Compile**:
    ```bash
    # For Final PDF
    python3 .agent/skills/report-writer/scripts/compile_report.py report.md --format pdf --color "005c9e"
    ```
