import pandas as pd
import duckdb

def clean_and_rename_with_duckdb(csv_path: str, canonical_mapping: dict, output_parquet: str):
    """
    Reads a messy CSV using DuckDB, extracts headers, and fuzzy-matches them
    against a canonical mapping dictionary. It then renames the columns and exports to Parquet.
    
    Args:
        csv_path (str): Path to the raw CSV file.
        canonical_mapping (dict): Dictionary mapping expected raw column names to clean snake_case names.
                                  Example: {"1. What is your age?": "age"}
        output_parquet (str): Path to save the processed Parquet file.
        
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    con = duckdb.connect()
    
    # 1. Fetch actual headers from DuckDB automatically
    # This avoids Pandas' issues with trailing commas and empty headers
    headers_query = con.execute(f"SELECT * FROM read_csv_auto('{csv_path}') LIMIT 0").description
    actual_headers = [col[0] for col in headers_query]
    
    # 2. Adaptive Fuzzy Mapping
    adaptive_mapping = {}
    for h in actual_headers:
        # Exact match
        if h in canonical_mapping:
            adaptive_mapping[h] = canonical_mapping[h]
        # Trimmed match (handles leading/trailing spaces in messy CSVs)
        elif h.strip() in [k.strip() for k in canonical_mapping.keys()]:
            original_key = next((k for k in canonical_mapping.keys() if k.strip() == h.strip()), None)
            if original_key:
                adaptive_mapping[h] = canonical_mapping[original_key]

    # 3. Construct SQL for renaming
    cols_sql = []
    for orig, clean in adaptive_mapping.items():
        # E.g., "1. What is your age?" AS age
        cols_sql.append(f"\"{orig}\" AS {clean}")

    # Fallback if somehow no columns matched (unlikely in practice, but good for safety)
    if not cols_sql:
        raise ValueError("No columns matched the canonical mapping.")

    select_clause = ", ".join(cols_sql)
    
    # 4. Run the query to select only mapped and renamed columns
    query = f"SELECT {select_clause} FROM read_csv_auto('{csv_path}')"
    df = con.execute(query).df()
    
    # 5. Export
    df.to_parquet(output_parquet, index=False)
    print(f"Data cleaned and saved to {output_parquet} ({len(df)} rows, {len(df.columns)} columns).")
    return df

# Example Usage:
# if __name__ == "__main__":
#     mapping = {"How old are you? ": "age", "What is your gender?": "gender"}
#     clean_and_rename_with_duckdb("raw.csv", mapping, "clean.parquet")
