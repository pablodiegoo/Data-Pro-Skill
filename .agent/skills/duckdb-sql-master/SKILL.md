---
name: duckdb-sql-master
description: Master-level skill for efficient local OLAP data analysis using DuckDB. Use for high-performance querying of CSV/Parquet/JSON files, complex SQL transformations, data cleaning pipelines, and format conversion without a database server.
---

# DuckDB SQL Master

## Overview

This skill provides expert-level guidance and utilities for using DuckDB, a high-performance in-process SQL OLAP database management system. It is designed for fast analytical queries on local files (CSV, Parquet, JSON) and seamless integration with Python/Pandas.

## When to Use

- **Analyzing Large Files**: querying multi-GB CSV/Parquet files that don't fit in RAM.
- **Data Transformation**: Complex SQL (CTEs, Window Functions) on raw files.
- **Format Conversion**: Converting CSV to Parquet/JSON efficiently.
- **Local OLAP**: Analytical workloads without setting up Postgres/MySQL.
- **Data Cleaning**: SQL-based cleaning pipelines.

## Core Capabilities

### 1. Direct File Querying
DuckDB can query files directly without importing them first.

```sql
-- Query CSV directly
SELECT * FROM 'data/*.csv' WHERE id > 100;

-- Query Parquet directly
SELECT count(*) FROM 'large_data.parquet';

-- Query JSON directly
SELECT * FROM read_json_auto('logs.json');
```

### 2. High-Performance Export
Efficiently convert data between formats.

```sql
-- Convert CSV to Parquet (Compressed)
COPY (SELECT * FROM 'raw.csv') TO 'optimized.parquet' (FORMAT 'PARQUET', CODEC 'SNAPPY');

-- Export to CSV
COPY table_name TO 'output.csv' (HEADER, DELIMITER ',');
```

### 3. Python Integration
Seamlessly query Pandas dataframes and return results as dataframes.

```python
import duckdb
import pandas as pd

df = pd.DataFrame({'a': [1, 2, 3]})
result = duckdb.sql("SELECT sum(a) FROM df").df()
```

## Best Practices

1.  **Prefer Parquet**: Always convert large CSVs to Parquet for 10-100x faster queries on subsequent runs.
2.  **Use CTEs**: Break down complex logic using Common Table Expressions.
3.  **Memory Management**: For distinct counts on huge data, use `approx_count_distinct()`.
4.  **Extensions**: Use `httpfs` for querying S3/URLs directly, `spatial` for Geo data.

## Resources

### Scripts (`scripts/`)
- `setup_duckdb.py`: Verifies installation and installs core extensions.

### References (`references/`)
- `cheat_sheet.md`: Common patterns, CLI commands, and optimized queries.
