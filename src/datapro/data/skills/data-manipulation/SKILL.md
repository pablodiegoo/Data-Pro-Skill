---
name: data-manipulation
description: "High-performance data manipulation and transformation using Pandas, Numpy, and DuckDB. Use when Claude needs to: (1) Clean or transform structured data (CSV, Parquet, JSON), (2) Perform large-scale aggregations or analytics, (3) Optimize analysis for performance and memory, (4) Implement the 'Tidy Data' (Wide-to-Long) strategy for reporting."
---

# Data Manipulation

High-performance data manipulation and transformation suite using Pandas, Numpy, and DuckDB. This skill handles the "T-Layer" (Transformation) of the data pipeline, preparing raw data for statistical analysis or reporting.

## 1. Core Capabilities

### A. Dictionary Mapping & Cleaning
Standardizes raw, cryptic variables into semantic labels using external mapping dictionaries.
- **Script**: `scripts/dict_mapper.py`
- **Reference**: [pipeline.md](./references/pipeline.md)

### B. High-Performance Ingestion & Aggregation (DuckDB Track)
Provides extremely fast ingestion and fuzzy cleaning for messy local files or files > 1GB.
- **Scripts**: `scripts/duckdb_fuzzy_cleaner.py`, `scripts/quant_analyzer_duckdb.py`
- **Reference**: [duckdb_analytics.md](./references/duckdb_analytics.md)

### C. Sample Weighting
Calculates and applies expansion weights for representative survey analysis.
- **Script**: `scripts/weighting.py`

### D. Data Organization
Utilities for managing project directory structures and data discovery.
- **Script**: `scripts/data_directory_finder.py`

## 2. Technical Guidelines

1. **Efficiency**: Use [Pandas Patterns](./references/pandas_patterns.md) (vectorization, categorical dtypes) for datasets under 1GB.
2. **Robustness**: Use [NumPy Stats](./references/numpy_stats.md) for low-level numerical transformations.
3. **Hierarchy**: Always prefer Parquet for intermediate data storage to preserve data types.

## 3. Reference Decision Matrix

| Task | Recommended Tool | Pattern Reference |
| :--- | :--- | :--- |
| **Join > 5M rows** | DuckDB | [Analysis Pattern](./references/duckdb_analytics.md) |
| **Wide-to-Long** | Pandas `melt` | [Tidy Pattern](./references/pandas_patterns.md) |
| **Clean Outliers** | NumPy/SciPy | [Stats Pattern](./references/numpy_stats.md) |

---
> [!IMPORTANT]
> This skill focusing on **preparation**. For statistical inference, multivariate modeling, or causal analysis, defer to the `@data-analysis-suite`.
