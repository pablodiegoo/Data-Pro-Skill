import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse

def association_matrix(data_path, target_col, attributes, output_dir, top_level='Alta'):
    """
    Creates an Association Matrix of Chi-Square Residuals.
    Shows which attributes (at high performance) are most associated 
    with positive/negative target segments.
    """
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_parquet(data_path) if data_path.endswith('.parquet') else pd.read_csv(data_path)
    
    # 1. Segment Target (if 0-10)
    def bin_val(val):
        if val <= 6: return 'Low'
        if val <= 8: return 'Mid'
        return 'High'
        
    df['Target_Seg'] = df[target_col].apply(bin_val)
    results = []
    
    for attr in attributes:
        temp = df[[attr, 'Target_Seg']].dropna()
        temp['Attr_Level'] = temp[attr].apply(bin_val) # Or custom binning
        
        ct = pd.crosstab(temp['Attr_Level'], temp['Target_Seg'])
        chi2, p, dof, expected = chi2_contingency(ct)
        resid = (ct - expected) / np.sqrt(expected)
        
        if top_level in resid.index:
            row = resid.loc[top_level].to_dict()
            row['Attribute'] = attr
            results.append(row)
            
    res_df = pd.DataFrame(results).set_index('Attribute')
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(res_df, annot=True, cmap='RdBu_r', center=0)
    plt.title('Top-Box Association Matrix (Standardized Residuals)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'association_matrix.png'), dpi=300)
    
    res_df.to_csv(os.path.join(output_dir, 'association_matrix.csv'))
    return res_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="Path to input file")
    parser.add_argument("--target", help="Target column name", required=True)
    parser.add_argument("--attributes", help="Comma-separated attributes", required=True)
    parser.add_argument("--output", default="output", help="Output directory")
    args = parser.parse_args()
    
    association_matrix(args.data, args.target, args.attributes.split(','), args.output)
