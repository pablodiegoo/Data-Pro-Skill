---
name: survey-analytics
description: "Core statistical analysis and pipeline automation for survey datasets. Use for: (1) Running standard Crosstabs, NPS, Top-Box calculations, (2) Generating complete EDA or Analytics notebooks, (3) Quantitative and qualitative processing of questionnaire data."
---

# Survey Analytics

This skill provides fundamental data operations exclusively tailored for Survey and Quantitative research.

## Core Capabilities

### 1. Survey Processing & Automation
- **`quant_analyzer.py`**: Standard statistical aggregations.
- **`qual_analyzer.py`**: Basic qualitative text processing.
- **`eda_notebook_generator.py`**: Generates automated Exploratory Data Analysis notebooks.
- **`advanced_analytics_generator.py`**: Scaffolds advanced statistical notebooks.

### 2. Market Research Standards
- **`crosstabs.py`**: Cross-tabulation matrices with significance testing.
- **`turf_analysis.py`**: Total Unduplicated Reach and Frequency analysis.
- **`survey_pca.py`**: Principal Component Analysis for dimension reduction in block questions.
- **`qualitative_categorizer.py`**: NLP/LLM-aided categorizer for open-ended survey text.

## Governance & Rules
Refer to the `references/` folder for specific guidelines on:
- **Explicit Weight Handling** (`explicit_weight_handling.md`)
- **Survey Governance** (`survey_governance.md`)
