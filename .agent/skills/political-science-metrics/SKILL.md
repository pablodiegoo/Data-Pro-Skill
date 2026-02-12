---
name: political-science-metrics
description: "Specialized metrics for political campaigning, including Disapproval Analysis (Pain Curves) and Successor Retention Indices."
---

# Political Science Metrics Skill

This skill provides advanced frameworks for analyzing political survey data, focusing on rejection drivers and threshold analysis.

## Core Procedures

### 1. Disapproval Analysis (Inverse Regression)
Identifies "shields"—attributes that, when high, significantly reduce the probability of rejection.
- **Goal**: Find "deal breakers" rather than "vote gatherers".

### 2. Pain Curves
Visualizes the relationship between attribute performance and rejection probability.
- **Goal**: Identify critical thresholds where failure becomes unacceptable.

## Reference Material
- **Conceptual Details & Examples**: See [political_reference.md](references/political_reference.md)

## Available Scripts

### `disapproval_analysis.py`
Runs a logistic regression targeting the absence of approval.

**Usage**:
```bash
python3 .agent/skills/political-science-metrics/scripts/disapproval_analysis.py \
    data.parquet --target "Vote" --val 1 --attributes "Q1,Q2,Q3" --output output_dir
```

### `pain_curves.py`
Generates probabilistic curves segmented by demographic variables.

**Usage**:
```bash
python3 .agent/skills/political-science-metrics/scripts/pain_curves.py \
    data.parquet --target "Rejection" --driver "Info" --segment "Income"
```
