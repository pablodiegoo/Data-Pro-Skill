import pandas as pd
import argparse
import os

def process_multi_select_conversion(df, weight_col, q_aware_cols, q_visited_cols, exclude_list=[]):
    """
    Calculates conversion rates between 'Awareness' and 'Visitation' for 
    multi-selection survey questions.
    
    Parameters:
    df (pd.DataFrame): Dataframe containing the columns.
    weight_col (str): Column name for weights.
    q_aware_cols (list): List of columns corresponding to Knowledge/Awareness choices.
    q_visited_cols (list): List of columns corresponding to Visitation choices.
    exclude_list (list): Values to ignore (e.g., 'None', 'Other').
    
    Returns:
    pd.DataFrame: Table with Awareness (%), Visitation (%), Conversion (%), and Gap.
    """
    def extract_set(row, cols):
        return set([str(v).strip() for v in row[cols].dropna() if str(v).strip() != ""])

    # Avoid modifying original df if possible, but for performance with apply we use new columns
    df_proc = df.copy()
    df_proc['_know_set'] = df_proc.apply(lambda r: extract_set(r, q_aware_cols), axis=1)
    df_proc['_visit_set'] = df_proc.apply(lambda r: extract_set(r, q_visited_cols), axis=1)

    all_items = set()
    for s in df_proc['_know_set']: all_items.update(s)
    active_items = sorted([i for i in all_items if i not in exclude_list])

    stats = []
    total_w = df_proc[weight_col].sum()

    for item in active_items:
        k_w = df_proc[df_proc['_know_set'].apply(lambda x: item in x)][weight_col].sum()
        v_w = df_proc[df_proc['_visit_set'].apply(lambda x: item in x)][weight_col].sum()
        
        stats.append({
            'Item': item,
            'Awareness (%)': (k_w / total_w) * 100,
            'Visitation (%)': (v_w / total_w) * 100
        })

    results = pd.DataFrame(stats)
    if not results.empty:
        results['Conversion (%)'] = (results['Visitation (%)'] / results['Awareness (%)']) * 100
        results['Gap'] = results['Awareness (%)'] - results['Visitation (%)']
        results = results.sort_values('Awareness (%)', ascending=False)
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="Path to input survey file")
    parser.add_argument("--weight", default="weight", help="Weight column")
    parser.add_argument("--aware_cols", required=True, help="Comma-separated awareness columns")
    parser.add_argument("--visit_cols", required=True, help="Comma-separated visitation columns")
    parser.add_argument("--exclude", default="", help="Comma-separated values to exclude")
    parser.add_argument("--output", default="conversion_funnel.csv", help="Output file")
    args = parser.parse_args()
    
    df = pd.read_parquet(args.data) if args.data.endswith('.parquet') else pd.read_csv(args.data)
    results = process_multi_select_conversion(
        df, 
        args.weight, 
        args.aware_cols.split(','), 
        args.visit_cols.split(','),
        args.exclude.split(',') if args.exclude else []
    )
    results.to_csv(args.output, index=False)
    print(f"Results saved to {args.output}")
