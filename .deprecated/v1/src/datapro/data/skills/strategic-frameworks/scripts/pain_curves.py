import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse

def generate_pain_curves(data_path, target_binary, driver_col, segment_col, output_dir):
    """
    Generates Pain Curves identifying the probability of rejection 
    based on a specific driver's performance, segmented by a demographic variable.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.read_parquet(data_path) if data_path.endswith('.parquet') else pd.read_csv(data_path)
    data = df[[target_binary, driver_col, segment_col]].dropna().copy()
    
    # Probabilistic Curve
    curve_data = data.groupby([driver_col, segment_col])[target_binary].mean().unstack()
    
    plt.figure(figsize=(12, 6))
    for col in curve_data.columns:
        plt.plot(curve_data.index, curve_data[col], marker='o', label=col, linewidth=2)
    
    plt.title(f'Pain Curve: Probability of {target_binary}')
    plt.xlabel(f'Performance: {driver_col}')
    plt.ylabel('Probability')
    plt.legend(title=segment_col)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'pain_curve.png'), dpi=300)
    
    curve_data.to_csv(os.path.join(output_dir, 'pain_curve_data.csv'))
    return curve_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="Path to input file")
    parser.add_argument("--target", help="Binary target column (0/1)", required=True)
    parser.add_argument("--driver", help="Driver column (numeric)", required=True)
    parser.add_argument("--segment", help="Segmentation column", required=True)
    parser.add_argument("--output", default="output", help="Output directory")
    args = parser.parse_args()
    
    generate_pain_curves(args.data, args.target, args.driver, args.segment, args.output)
