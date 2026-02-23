---
name: duckdb-sql-master
description: "High-performance SQL on local files. Use for: (1) Ingestion of dirty or massive CSV/Parquet files, (2) Fuzzy matching messy headers to a canonical dictionary, (3) Rapid aggregation and cleaning."
---

# DuckDB SQL Master

This skill provides capabilities for extremely fast data ingestion, querying, and cleaning of messy local files using DuckDB.

## Capabilities

### 1. Dirty Ingestion & Fuzzy Cleaning
Handles common export issues from survey platforms (trailing commas, long text headers, variable column counts).
- **Script**: `duckdb_fuzzy_cleaner.py` (located in `scripts/`)
- **Usage**: Uses `read_csv_auto` combined with a Python fuzzy-matching dictionary to standardize headers on the fly before loading into memory.

## Best Practices
1. **Prefer DuckDB for Ingestion**: When reading files larger than 1GB or with very messy formats, use DuckDB's CSV reader over pandas.
2. **Schema Mapping**: Always map raw question headers to `snake_case` ids immediately upon ingestion.

---
> [!IMPORTANT]
> All code comments, logs, and outputs from this skill MUST be in **English**.
