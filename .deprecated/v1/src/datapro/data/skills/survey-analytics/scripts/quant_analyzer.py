import pandas as pd
import json
import argparse
import sys
import os

def normalize_points(row, columns, max_points, scale_to):
    """Sums points from specific columns and normalizes to a new scale."""
    points_sum = 0
    
    # If columns is a dict, it implies weighting {col_name: weight}
    if isinstance(columns, dict):
        for col, weight in columns.items():
            val = str(row.get(col, "")).strip()
            # If cell is not empty/null/0, add the weight
            if val and val.lower() not in ["nan", "none", "0", "false", "no", "não"]:
                points_sum += weight
    
    # Legacy list support (weight=1)
    elif isinstance(columns, list):
        for col in columns:
            val = str(row.get(col, "0")).lower()
            if val in ["1", "true", "yes", "x", "sim", "checked"]:
                points_sum += 1
            elif val.isdigit():
                points_sum += int(val)
            
    return (points_sum / max_points) * scale_to if max_points > 0 else 0

def calculate_scores(df, config):
    """Applies normalizations and calculates domain averages."""
    # 1. Apply Normalizations
    if "normalizations" in config:
        for norm_col, settings in config["normalizations"].items():
            df[norm_col] = df.apply(
                lambda r: normalize_points(r, settings["columns"], settings["max_points"], settings["scale_to"]),
                axis=1
            )
    
    # 2. Calculate Domain Scores
    domain_columns = []
    if "domains" in config:
        for domain_name, cols in config["domains"].items():
            # Ensure columns exist and are numeric
            for col in cols:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            df[domain_name] = df[cols].mean(axis=1)
            domain_columns.append(domain_name)
    
    # 3. Calculate Final Escore
    if domain_columns:
        df["Escore Final"] = df[domain_columns].mean(axis=1)
    
    return df

def main():
    parser = argparse.ArgumentParser(description="Survey Quantitative Analyzer")
    parser.add_argument("input", help="Input CSV file")
    parser.add_argument("config", help="Configuration JSON file")
    parser.add_argument("-o", "--output", help="Output CSV file", default="processed_output.csv")
    
    args = parser.parse_args()
    
    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
            
        df = pd.read_csv(args.input)
        df_processed = calculate_scores(df, config)
        df_processed.to_csv(args.output, index=False)
        print(f"✅ Analysis complete. Processed data saved to {args.output}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
