---
description: Standard workflow for end-to-end Survey Analysis (Discovery -> Reporting)
---

# Survey Analysis Pipeline

This workflow outlines the standard operating procedure for analyzing survey data (e.g., Sebrae projects) using the Agent's specialized consolidated skills.

## 1. Discovery & Context
**Goal**: Understand the project scope and set up the environment.

1.  **Context Optimization**:
    - Use the `context-optimizer` skill to decompose large docs (Work Order, Questionnaire).
    - Populate `.agent/memory/project_facts.md` with Universe targets and Sample info.

## 2. Data Preparation
**Goal**: Clean raw data and map variable names using DuckDB for high-performance processing.

1.  **Dictionary Mapping**:
    - Use **`data-analysis-suite`**:
      ```bash
      python3 .agent/skills/data-analysis-suite/scripts/dict_mapper.py dict.xlsx
      ```
2.  **Cleaning Script (DuckDB Pipeline)**:
    - Create `01_data_prep.py` leveraging `duckdb-sql-master`.

## 3. Data Validation
**Goal**: Ensure data quality before analysis.

1.  **Pre-Flight Checks**: Verify data types, missing values, and outliers.
2.  **Schema Compliance**: Validate against the data dictionary.

## 4. Weighting (Raking)
**Goal**: Adjust sample to match population targets.

1.  **Run Weighting**:
    - Create `02_weighting.py` using **`data-analysis-suite`**.
    ```python
    from scripts.weighting import rake_weights
    df['weight'] = rake_weights(df, targets)
    ```

## 5. Analysis & Visuals
**Goal**: Generate insights and charts.

1.  **Charts**:
    - Generate breakdown charts using **`data-viz`**.
    - Save outputs to the results folder defined in `structure.json` (`assets/images/`).

## 6. Advanced Analysis (Specialized Metrics)
**Goal**: Reveal hidden patterns and remove biases.

1.  **Methodology**:
    - Use **`data-analysis-suite`** for specialized calculations.
    - Consult `references/causal.md` for Drivers.
    - Consult `references/science.md` for Halo removal and Pain Curves.

## 7. Reporting
**Goal**: Compile the final deliverable.

1.  **Draft Report**: Write `report.md` following **`document-mastery`** standards (Mermaid diagrams, alerts, structure).
2.  **Compile**:
    - Use **`document-converter`** for final PDF/DOCX export.
