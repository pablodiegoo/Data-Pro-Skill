
import pandas as pd
import numpy as np
from itertools import combinations

def run_turf_analysis(df, items, n_max_size=4):
    """
    Performs TURF Analysis (Total Unduplicated Reach and Frequency).
    
    Args:
        df: DataFrame containing the data (binary 0/1 or boolean).
        items: List of column names to include in the analysis.
        n_max_size: Maximum size of combination to check (default 4).
        
    Returns:
        DataFrame with columns ['Size', 'Combination', 'Reach', 'Reach_Percent']
    """
    # Filter valid items
    valid_items = [col for col in items if col in df.columns]
    
    # Create binary matrix (force 0/1)
    # Assumes NaNs are 0 (not reached) if data is sparse
    data = df[valid_items].fillna(0).astype(bool).astype(int)
    n_respondents = len(df)
    
    results = []
    
    for size in range(1, n_max_size + 1):
        best_reach = -1
        best_combo = None
        
        # Check all combinations
        for combo in combinations(valid_items, size):
            # Calculate reach: user is reached if sum across combo columns > 0
            # Faster numpy implementation
            sub_matrix = data[list(combo)].values
            # Check if ANY item in row is 1
            reached_count = np.any(sub_matrix, axis=1).sum()
            reach_pct = reached_count / n_respondents
            
            if reach_pct > best_reach:
                best_reach = reach_pct
                best_combo = combo
        
        results.append({
            'Size': size,
            'Combination': ", ".join(best_combo),
            'Reach_Count': int(best_reach * n_respondents),
            'Reach_Percent': round(best_reach * 100, 2)
        })
        
    return pd.DataFrame(results)


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description="TURF (Total Unduplicated Reach and Frequency) CLI")
    parser.add_argument("input", help="Input CSV/XLSX dataset")
    parser.add_argument("--items", "-i", default=None, help="Comma-separated item columns (default: auto numeric/binary)")
    parser.add_argument("--max-k", "-k", type=int, default=4, help="Maximum bundle size K")
    parser.add_argument("--threshold", type=float, default=None, help="Optional rating threshold for top-box binary conversion (e.g. 4 on 1-5 scale)")
    parser.add_argument("-o", "--output", default=".dps/outputs/advanced", help="Output directory")
    args = parser.parse_args()

    df_in = pd.read_excel(args.input) if args.input.endswith((".xlsx", ".xls")) else pd.read_csv(args.input)
    if args.items:
        item_cols = [c.strip() for c in args.items.split(",") if c.strip() in df_in.columns]
    else:
        item_cols = [
            c for c in df_in.select_dtypes(include=[np.number]).columns
            if c.lower() not in ("id", "respondent_id", "weight", "peso")
        ][:10]

    work = df_in[item_cols].apply(pd.to_numeric, errors="coerce").fillna(0)
    if args.threshold is not None:
        work = (work >= args.threshold).astype(int)
    elif work.max().max() > 1:
        mx = work.max().max()
        thr = 4.0 if mx <= 5.0 else (6.0 if mx <= 7.0 else 8.0)
        work = (work >= thr).astype(int)

    res_df = run_turf_analysis(work, item_cols, n_max_size=min(args.max_k, len(item_cols)))
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    res_df.to_csv(out_dir / "turf_results.csv", index=False)
    print(f"✅ TURF analysis complete in {out_dir / 'turf_results.csv'}:")
    print(res_df.to_string(index=False))
