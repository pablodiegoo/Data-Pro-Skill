---
name: dictionary-mapper
description: "Automates the mapping of variable names (e.g., 'P1', 'Q3') to semantic labels ('Gender', 'Satisfaction') by reading Data Dictionaries (Excel/PDF)."
---

# Dictionary Mapper

This skill automates the tedious process of mapping raw survey column names (like `VAR001`, `P5_A`) to human-readable questions suitable for analysis. It reads standard Data Dictionaries (often provided as Excel or inside PDF reports) and generates a Python dictionary or JSON mapping.

## Capabilities

### 1. Excel Dictionary Parser (`parse_excel.py`)
Reads an Excel file where one column is the Variable Name and another is the Label/Question.

**Usage:**
```bash
python3 .agent/skills/dictionary-mapper/scripts/parse_excel.py \
    dictionary.xlsx \
    --col-var "Variable" \
    --col-label "Label" \
    --output mapping.json
```

### 2. Auto-Infer from Raw Data (`infer_from_csv.py`)
If the first row of your CSV contains the full question text (common in SurveyMonkey/Google Forms), this script extracts it and creates a clean mapping.

**Usage:**
```bash
python3 .agent/skills/dictionary-mapper/scripts/infer_from_csv.py \
    raw_data.csv \
    --output mapping.json
```

## Dependencies
```bash
pip install pandas openpyxl
```
