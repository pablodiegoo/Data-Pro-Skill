---
name: data-pro-max
description: "Data Analysis Intelligence. Statistics, Visualization, Reporting, and Data Engineering. Actions: analyze, visualize, report, clean, transform, test, model. Topics: descriptive stats, inferential tests, machine learning, qualitative analysis, plotting (static/interactive), mermaid diagrams. Integrations: Pandas, Polars, Scikit-learn, Plotly, Seaborn, Matplotlib."
---

# Data Pro Max - Data Analysis Intelligence

Comprehensive guide for quantitative and qualitative data analysis. Contains framework-aligned patterns for data loading, cleaning, statistical testing, and professional reporting.

## When to Apply

Reference these guidelines when:
- Designing analysis pipelines
- Choosing statistical tests
- Creating professional visualizations
- Generating automated reports
- Cleaning complex datasets

## Rule Categories by Priority

| Priority | Category | Impact | Domain |
|----------|----------|--------|--------|
| 1 | Data Integrity | CRITICAL | `cleaning` |
| 2 | Statistical Validity | CRITICAL | `analysis` |
| 3 | Visualization Clarity | HIGH | `visualization` |
| 4 | Reproducibility | HIGH | `engineering` |
| 5 | Performance | MEDIUM | `engineering` |
| 6 | Reporting Aesthetics | MEDIUM | `reporting` |

## Quick Reference

### 1. Data Integrity (CRITICAL)
- `missing-values` - Explicit strategy (mean, median, drop) required
- `outliers` - Detect and document outliers before analysis
- `schema-validation` - Enforce types at ingestion
- `deduplication` - Check for duplicates on primary keys

### 2. Statistical Validity (CRITICAL)
- `normality-check` - Shapiro-Wilk (< 5k samples) or Anderson-Darling
- `sample-size` - Verify power of test before concluding
- `p-values` - Use 0.05 default alpha, interpret contextually
- `correlation` - Check for multicollinearity

## How to Use This Skill

When user requests Data Analysis work, follow this workflow:

### Step 1: Analyze User Requirements
Extract key information:
- **Data Type**: Survey, Financial, Time-series, Text
- **Goal**: Exploration, Prediction, Reporting, Dashboarding
- **Volume**: Small (<1GB), Medium, Large (>10GB)

### Step 2: Query the Framework (REQUIRED)
Use the search tool to find the approved pattern for the task.

```bash
python3 .agent/skills/data-pro-max/scripts/search.py "<topic>"
```

**Example:**
```bash
python3 .agent/skills/data-pro-max/scripts/search.py "normality test"
python3 .agent/skills/data-pro-max/scripts/search.py "heatmap visualization"
```

### Step 3: Implementation
Implement the code following the patterns retrieved from the framework.

## Search Reference

### Available Domains/Keywords
- `ingestion`: Loading CSV, Parquet, SQL, Excel
- `cleaning`: Missing values, outliers, normalization
- `analysis`: Descriptive, correlation, hypothesis tests
- `visualization`: Static plots, interactive (plotly), diagrams
- `reporting`: Markdown, PDF, templates, tables
