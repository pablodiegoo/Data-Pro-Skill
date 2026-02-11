
# DuckDB SQL Cheat Sheet

## CLI Commands

- `.help`: Show help
- `.quit`: Exit DuckDB CLI
- `.tables`: List tables
- `.schema <table_name>`: Show schema of a table
- `.read path/to/file.sql`: Execute SQL from file
- `.output path/to/file.csv`: Export query result to CSV

## Data Loading

```sql
-- Load CSV with auto-detection
SELECT * FROM read_csv_auto('data.csv');

-- Load JSON (New-Line Delimited)
SELECT * FROM read_json_auto('logs.json');

-- Load Parquet
SELECT * FROM read_parquet('data.parquet');

-- Create TABLE from CSV
CREATE TABLE my_table AS SELECT * FROM read_csv_auto('data.csv');
```

## Data Export

```sql
-- Export to Parquet (Snappy compressed by default)
COPY (SELECT * FROM my_table) TO 'output.parquet' (FORMAT 'PARQUET');

-- Export to CSV
COPY (SELECT * FROM my_table) TO 'output.csv' (HEADER, DELIMITER ',');
```

## Transformations

```sql
-- CTE Example
WITH filtered_users AS (
    SELECT user_id FROM users WHERE status = 'active'
)
SELECT u.city, COUNT(*)
FROM users u
JOIN filtered_users fu ON u.user_id = fu.user_id
GROUP BY u.city;

-- Window Functions
SELECT 
    product_id, 
    sales, 
    RANK() OVER (PARTITION BY category_id ORDER BY sales DESC) as rank
FROM sales_data;
```

## JSON Manipulation

```sql
-- Extracting fields from JSON column
SELECT json_extract(metadata, '$.user.id') as user_id
FROM events;

-- Expanding a JSON array into rows
SELECT unnest(json_transform(tags, '["apple", "banana"]')) as tag;
```

## Optimization

- **Prefer `read_parquet` over `read_csv` when possible.**
- **Use `approx_count_distinct(col)`** for massive datasets if 100% accuracy isn't critical.
- **Use `PRAGMA threads=4;`** to limit parallelism if memory constrained.
