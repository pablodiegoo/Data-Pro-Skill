import pandas as pd
import argparse
import os

def calculate_priority_scores(df, importance_col, performance_col, scale=10):
    """
    Calculates Priority Scores for a list of attributes based on their 
    Importance (e.g., correlation) and Performance (e.g., mean score).
    
    Formula: Priority_Score = Importance * (Scale - Performance)
    
    Parameters:
    df (pd.DataFrame): DataFrame containing 'importance' and 'performance' columns.
    importance_col (str): Column name for importance values.
    performance_col (str): Column name for performance values.
    scale (float): The maximum value of the performance scale (default: 10).
    
    Returns:
    pd.DataFrame: Original DataFrame sorted by Priority_Score descending.
    """
    df['Priority_Score'] = df[importance_col] * (scale - df[performance_col])
    return df.sort_values('Priority_Score', ascending=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="Path to input CSV/Parquet results file")
    parser.add_argument("--importance", required=True, help="Column name for importance")
    parser.add_argument("--performance", required=True, help="Column name for performance")
    parser.add_argument("--scale", type=float, default=10.0, help="Performance scale max")
    parser.add_argument("--output", default="priority_results.csv", help="Output file path")
    args = parser.parse_args()
    
    df = pd.read_parquet(args.data) if args.data.endswith('.parquet') else pd.read_csv(args.data)
    results = calculate_priority_scores(df, args.importance, args.performance, args.scale)
    results.to_csv(args.output, index=True)
    print(f"Results saved to {args.output}")
