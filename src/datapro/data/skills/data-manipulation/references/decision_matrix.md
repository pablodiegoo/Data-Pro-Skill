# Data Manipulation Decision Matrix

A guide for choosing the right tool for data manipulation tasks within the DataPro ecosystem.

## 📊 Decision Tree

| Feature / Tool | Pandas | Numpy | DuckDB | Polars (Optional) |
| :--- | :--- | :--- | :--- | :--- |
| **Data Size** | Small-to-Medium (< 2GB) | Multi-dim Arrays | Large (> 2GB) | Medium-to-Large |
| **Primary Use** | Clean, Pivot, Exploration | Fast Math, Stats Formulas | SQL Joins, Aggregation | Parallel Processing |
| **Complexity** | High (Python logic) | Medium (Vectorized) | Low (Pure SQL) | High (Lazy API) |
| **I/O Support** | Standard | Raw Arrays | Direct Files (CSV/Parquet) | Very Fast I/O |

## 🛠️ Selection Logic

1.  **Use PANDAS when**:
    -   You need deep feature engineering with custom Python functions.
    -   The dataset fits comfortably in memory.
    -   You are preparing data for Matplotlib/Seaborn.
2.  **Use NUMPY when**:
    -   You are implementing a specific statistical formula from a paper.
    -   You are doing low-level array manipulation.
3.  **Use DUCKDB when**:
    -   The dataset is too large for Pandas to handle efficiently.
    -   You have complex JOINs across multiple files.
    -   You want a SQL-first approach for aggregation.
    -   The objective is "Analytical Reporting" on raw files.

## 💡 The "DataPro Strategy"

-   **Phase 1 (Clean)**: Use Pandas/DuckDB to standardize columns.
-   **Phase 2 (Pivot)**: Use Melting patterns to reach Long Format.
-   **Phase 3 (Calc)**: Use Numpy/Pandas/DuckDB for stats.
-   **Phase 4 (Ship)**: Export to Clean CSV for Visuals or PDF Engine.
