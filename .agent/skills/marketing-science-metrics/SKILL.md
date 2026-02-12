---
name: marketing-science-metrics
description: "Advanced marketing science techniques to remove survey bias (Halo Effect, Response Style) and reveal true attribute importance."
---

# Marketing Science Metrics Skill

This skill provides "De-Biasing" techniques for attribute analysis in surveys, removing response style and halo effects.

## Core Procedures

### 1. Removing Respondent Bias (Ipsative)
Reduces "generosity" or "strictness" of respondents by centering scores on their personal mean.
- **Why**: Reveals *relative* priorities inside the respondent's mind.

### 2. Removing Halo Effect (Residuals)
Subtracts general sentiment (image) from individual attributes using OLS residuals.
- **Why**: Reveals "pure" attribute performance independent of brand popularity.

## Reference Material
- **Conceptual Details & Examples**: See [ipsative_reference.md](references/ipsative_reference.md)

## Available Scripts

### `ipsative_analysis.py`
Standardized script for Ipsative and/or Residual correlation analysis.

**Usage**:
```bash
python3 .agent/skills/marketing-science-metrics/scripts/ipsative_analysis.py \
    data.parquet --attributes "Q1,Q2,Q3" --output output_dir
```

### `halo_removal.py`
Standalone script specifically for Halo Effect removal using regression residuals.

**Usage**:
```bash
python3 .agent/skills/marketing-science-metrics/scripts/halo_removal.py \
    data.parquet --attributes "Q1,Q2,Q3" --output output_dir
```
