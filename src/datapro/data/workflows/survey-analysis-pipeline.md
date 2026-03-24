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
    - Use **`data-manipulation`**:
      ```bash
      python3 .agent/skills/data-manipulation/scripts/dict_mapper.py dict.xlsx
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
    - Create `02_weighting.py` using **`data-manipulation`**.
    ```python
    from scripts.weighting import rake_weights
    # Note: script is now in data-manipulation/scripts/
    ```

## 5. Analysis & Visuals
**Goal**: Generate insights and charts.

1.  **Charts**:
    - Use `survey_report_generator.py` for automated EDA.
    - Standardize the use of Mermaid.js (`xychart-beta` and `pie`) for frequencies to maintain 100% Markdown output.

## 6. Advanced Analysis (Specialized Metrics)
**Goal**: Reveal hidden patterns and remove biases.

1.  **Methodology**:
    - Use **`@causal-inference`** or **`@strategic-frameworks`** for specialized calculations (Drivers, Halo Removal, Priority Matrices).
    - Consult `references/causal.md` for Drivers.
    - Consult `references/science.md` for Halo removal and Pain Curves.

## 7. Reporting
**Goal**: Compile the final deliverable.

1.  **Draft Report**: Generate the final analytical report via a hypothesis-driven script like `final_report_generator.py`. This script must natively output cross-tabs, NPS, and statistical significance tests in Markdown.
2.  **Compile**:
    - Use **`document-converter`** for final PDF/DOCX export.
