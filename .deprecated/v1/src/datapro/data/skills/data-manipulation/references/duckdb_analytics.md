# DuckDB Analytical SQL

Strategic use of DuckDB for large-scale data analysis and high-performance querying without significant RAM overhead.

## 🦆 Why DuckDB?

1.  **Analytical Engine**: Optimized for columnar storage and SQL JOINs.
2.  **Zero-ETL Ingestion**: Direct query on CSV, Parquet, and JSON files.
3.  **Low Memory**: Handles datasets larger than physical RAM.

## 🛠️ Typical Workflow

```python
import duckdb

# Connect to in-memory database
con = duckdb.connect()

# Query directly from CSV
result = con.execute("""
    SELECT 
        segment, 
        avg(satisfaction) as avg_sat,
        count(*) as total
    FROM read_csv_auto('data.csv')
    GROUP BY segment
    HAVING count(*) > 50
    ORDER BY avg_sat DESC
""").df()  # Convert result to Pandas for visualization
```

## 🔗 Joins & Transformations

DuckDB is significantly faster than Pandas for large table JOINs.

```sql
SELECT 
    t1.*, 
    t2.demographics
FROM read_parquet('results.parquet') t1
JOIN read_csv('demographics.csv') t2 ON t1.user_id = t2.id
```

## 📉 Aggregation Features

-   **APPROX_COUNT_DISTINCT**: Faster for massive datasets.
-   **WINDOW FUNCTIONS**: Full support for `RANK()`, `LEAD()`, `LAG()`.
-   **MEDIAN**: Built-in specialized aggregate.
