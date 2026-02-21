# Data Pipeline & Qualitative Reference

This module handles the initial stages of data processing, from raw file mapping to qualitative text extraction.

## 1. Dictionary Mapping
Standardizes raw variables (e.g., `P1`, `Q10`) into semantic labels.
- **Script**: `scripts/dict_mapper.py`
- **Key Functionality**: Reads an external map (JSON/Excel) and renames DataFrame columns.

## 2. Quantitative Processing
Core calculations for survey automation.
- **Script**: `scripts/quant_analyzer.py`
- **Normalization**: Scales point systems (e.g., 1-13) to unified ranges (0-10).
- **Domain Scoring**: Aggregates batteries of questions into higher-level domains.

## 3. Cross Tabulation
Frequency analysis between categorical variables.
- **Script**: `scripts/crosstabs.py`
- **Key Functionality**: Generates cross-tabs with margins and normalization options.

## 4. Qualitative Analysis
Processing open-ended text fields.
- **Script**: `scripts/qual_analyzer.py`
- **Word Frequency**: Identifies dominant themes.
- **Sentiment Segments**: Filters comments based on demographic or rating segments.

---
> [!TIP]
> Always run `quant_analyzer.py` with a consistent `config.json` to ensure reproducible results across different survey waves.
