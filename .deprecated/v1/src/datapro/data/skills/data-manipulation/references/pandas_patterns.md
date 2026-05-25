# Pandas High-Performance Patterns

Guidelines for efficient data manipulation in Pandas, focusing on memory efficiency and readability.

## 🚀 Performance Essentials

1.  **Vectorized Operations**: Avoid `apply()`, `iterrows()`, and `itertuples()` for mathematical operations. Use built-in Series methods.
2.  **Chaining**: Use parentheses to chain operations for better readability and to avoid "SettingWithCopy" warnings.
3.  **Dtypes**: Cast objects to `category` for low-cardinality strings and use `int32`/`float32` where possible.

## 🧹 Tidy Data & Melting

Consistent with DataPro's strategy, use the **Long Format** for visualization.

```python
# The "Jeito DataPro" to melt survey data
df_long = df.melt(
    id_vars=['respondent_id', 'segment'],
    value_vars=['q1', 'q2', 'q3'],
    var_name='question',
    value_name='score'
)
```

## 📊 Grouping & Aggregation

Use `groupby().agg()` with a dictionary for multi-metric summaries.

```python
summary = df.groupby('segment').agg({
    'satisfaction': ['mean', 'median', 'std'],
    'nps': 'mean'
}).round(2)
```

## 🔍 Large-ish Data Tricks

- **Chunking**: Use `pd.read_csv(..., chunksize=100000)` for local files that exceed RAM.
- **Query**: Use `df.query('score > 4')` for cleaner filtering logic.
