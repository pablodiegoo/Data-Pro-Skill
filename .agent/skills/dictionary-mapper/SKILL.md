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

## Template Structures

When generating a `dictionary.py`, always include these three structures alongside `QUESTION_MAP` and `LABEL_MAP`:

### `SHORT_LABEL_MAP`
Concise labels (≤15 chars) for chart axes. Auto-derive from `LABEL_MAP` by extracting the key noun.

```python
SHORT_LABEL_MAP = {
    'P14_Eval_Attractions': 'Atrativos',
    'P15_Eval_Beaches': 'Praias',
    'P33_Eval_General': 'Geral',
}
```

### `FEATURE_GROUPS`
Logical groupings of columns by analytical purpose. Used by prep scripts and downstream analysis.

```python
FEATURE_GROUPS = {
    'satisfaction': ['P14_Eval_Attractions', 'P15_Eval_Beaches', ...],
    'demographics': ['P1_Relation', 'P4_Age', 'P5_Gender', ...],
    'behavior': ['P8_Reason', 'P9_Duration', ...],
}
```

### `SCALE_COLUMNS`
Ordinal columns that `01_prep_data.py` should auto-encode using `SCALE_MAP`. Enables the "Encode Once" rule.

```python
SCALE_COLUMNS = FEATURE_GROUPS['satisfaction'] + ['P33_Eval_General']
```

## Dependencies
```bash
pip install pandas openpyxl
```
