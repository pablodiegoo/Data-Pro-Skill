---
name: survey-quant-analyzer
description: "Programmatic tool for analyzing quantitative survey data. Calculates weighted scores, domain-based means, and normalizes complex point systems (e.g., 13-to-10 point conversions). Use when you have raw CSV survey results and need to: (1) Calculate domain scores, (2) Apply normalization rules, (3) Generate a weighted/processed dataset, or (4) Analyze evolution between survey cycles (Pre vs Post)."
---

# Survey Quantitative Analyzer

This skill provides a structured way to process and score quantitative survey data using a parameter-driven approach.

## Capabilities

- **Normalized Scoring**: Automatically converts non-standard point sums (like 0-13) to unified scales (0-10).
- **Domain Aggregation**: Groups questions into semantic domains and calculates their respective means.
- **Weighted Datasets**: Generates a processed CSV with calculated scores appended for each respondent.
- **Cycle Comparison**: Compares "Pre" and "Post" survey results to measure evolution.

## Usage

### 1. Preparation
Define a configuration JSON file that maps your CSV columns to domains and specifies normalization rules.

### 2. Run Analysis
Use the bundled script:
```bash
python3 .agent/skills/survey-quant-analyzer/scripts/analyzer.py input.csv config.json -o output_weighted.csv
```

## References
- [CALCULATION_LOGIC.md](../../workflows/calculation_logic.md): For details on how the scores are calculated.
- [METHODOLOGY.md](../../memory/methodology.md): For the semantic meaning of the score ranges.

## Example Config
```json
{
  "domains": {
    "Domain 1": ["Q1", "Q2", "Q3"],
    "Domain 2": ["Q4_norm", "Q5", "Q6"]
  },
  "normalizations": {
    "Q4_norm": {
      "columns": ["Q4_a", "Q4_b", "Q4_c", "Q4_d", "Q4_e", "Q4_f", "Q4_g", "Q4_h", "Q4_i", "Q4_j"],
      "max_points": 13,
      "scale_to": 10
    }
  }
}
```
