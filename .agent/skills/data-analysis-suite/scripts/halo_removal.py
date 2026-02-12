import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse

def remove_halo_effect(data_path, attributes, output_dir, images_dir):
    """
    Removes the Halo Effect (general sentiment bias) by regressing 
    each attribute against the respondent's mean score.
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    df = pd.read_parquet(data_path) if data_path.endswith('.parquet') else pd.read_csv(data_path)
    data = df[attributes].dropna().copy()
    
    # Calculate Halo Proxy (Personal Mean)
    data['Halo_Proxy'] = data[attributes].mean(axis=1)
    X = sm.add_constant(data['Halo_Proxy'])
    
    residuals = pd.DataFrame(index=data.index)
    for attr in attributes:
        y = data[attr]
        model = sm.OLS(y, X).fit()
        residuals[attr] = model.resid
        
    pure_corr = residuals.corr()
    
    # Plotting
    plt.figure(figsize=(12, 10))
    sns.heatmap(pure_corr, annot=True, fmt='.2f', cmap='BrBG', center=0, vmin=-1, vmax=1)
    plt.title('Pure Correlation Matrix (Halo Removed)')
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'correlation_halo_removed.png'), dpi=300)
    
    pure_corr.to_csv(os.path.join(output_dir, 'halo_removed_correlation.csv'))
    return pure_corr

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="Path to input file")
    parser.add_argument("--attributes", help="Comma-separated column names", required=True)
    parser.add_argument("--output", default="output", help="Output directory")
    args = parser.parse_args()
    
    remove_halo_effect(
        args.data, 
        args.attributes.split(','), 
        args.output, 
        args.output
    )
