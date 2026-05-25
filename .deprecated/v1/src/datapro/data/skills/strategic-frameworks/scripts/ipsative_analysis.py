import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse

def plot_heatmap(corr_matrix, title, output_path):
    plt.figure(figsize=(12, 10))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    # Simple labels if not provided
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', 
                cmap='BrBG', center=0, vmin=-1, vmax=1, 
                linewidths=0.5, cbar_kws={"shrink": .8})
    
    plt.title(title, fontsize=16)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Saved heatmap to {output_path}")

def run_marketing_science(data_path, attributes, output_dir, method='both'):
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data
    df = pd.read_parquet(data_path) if data_path.endswith('.parquet') else pd.read_csv(data_path)
    data = df[attributes].dropna().copy()
    
    if method in ['ipsative', 'both']:
        print("Iniciando Análise Ipsativa...")
        data['personal_mean'] = data.mean(axis=1)
        ipsative_data = pd.DataFrame(index=data.index)
        for col in attributes:
            ipsative_data[col] = data[col] - data['personal_mean']
        
        corr_ips = ipsative_data.corr()
        corr_ips.to_csv(os.path.join(output_dir, 'ipsative_correlation.csv'))
        plot_heatmap(corr_ips, 'Matriz Ipsativa (Viés Pessoal Removido)', 
                     os.path.join(output_dir, 'viz_ipsative_correlation.png'))

    if method in ['residuals', 'both']:
        print("Iniciando Análise de Resíduos do Halo...")
        data['halo_proxy'] = data[attributes].mean(axis=1)
        X = sm.add_constant(data['halo_proxy'])
        
        residuals = pd.DataFrame(index=data.index)
        for attr in attributes:
            y = data[attr]
            model = sm.OLS(y, X).fit()
            residuals[attr] = model.resid
            
        corr_resid = residuals.corr()
        corr_resid.to_csv(os.path.join(output_dir, 'halo_removed_correlation.csv'))
        plot_heatmap(corr_resid, 'Matriz de Resíduos (Efeito Halo Removido)', 
                     os.path.join(output_dir, 'viz_halo_removed_correlation.png'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="Path to input file")
    parser.add_argument("--attributes", help="Comma-separated attribute columns", required=True)
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--method", choices=['ipsative', 'residuals', 'both'], default='both')
    args = parser.parse_args()
    
    run_marketing_science(args.data, args.attributes.split(','), args.output, args.method)
