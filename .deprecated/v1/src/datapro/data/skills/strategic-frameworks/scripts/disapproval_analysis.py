import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse

def plot_disapproval_drivers(results, output_path):
    plt.figure(figsize=(10, 8))
    sns.barplot(x='Coef', y=results.index, data=results, palette='RdYlGn')
    plt.title('Drivers of Disapproval\n(Negative Coef = Shields against Rejection)', fontsize=14)
    plt.xlabel('Impact (Logit Coefficient)', fontsize=12)
    plt.axvline(0, color='gray', linestyle='--')
    plt.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Saved inverse drivers plot to {output_path}")

def plot_pain_curve(df, feature, target, output_path, title):
    data = df[[feature, target]].dropna().copy()
    X = sm.add_constant(data[feature])
    y = data[target]
    model = sm.Logit(y, X).fit(disp=0)
    
    x_range = np.linspace(0, 10, 100)
    X_pred = sm.add_constant(x_range)
    y_pred = model.predict(X_pred)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_range, y_pred, color='#c0392b', linewidth=3)
    plt.fill_between(x_range, y_pred, color='#c0392b', alpha=0.1)
    plt.title(title, fontsize=14)
    plt.xlabel(f'Score: {feature}', fontsize=12)
    plt.ylabel('Rejection Probability', fontsize=12)
    plt.ylim(-0.05, 1.05)
    plt.grid(True, alpha=0.3)
    plt.savefig(output_path)
    print(f"Saved pain curve for {feature} to {output_path}")

def run_political_science(data_path, target_col, approval_val, attributes, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_parquet(data_path) if data_path.endswith('.parquet') else pd.read_csv(data_path)
    
    # 1. Inverse Target: 1 is DISAPPROVAL
    disapproval_target = 'disapproval_bin'
    df[disapproval_target] = (df[target_col] != approval_val).astype(int)
    
    df_model = df.dropna(subset=[disapproval_target] + attributes).copy()
    X = df_model[attributes]
    y = df_model[disapproval_target]
    X_const = sm.add_constant(X)
    
    model = sm.Logit(y, X_const).fit(disp=0)
    summary = model.summary2().tables[1]
    
    results = pd.DataFrame({
        'OR': np.exp(summary['Coef.']),
        'Coef': summary['Coef.'],
        'P-Value': summary['P>|z|']
    }).drop('const', errors='ignore').sort_values(by='Coef')
    
    results.to_csv(os.path.join(output_dir, 'disapproval_drivers.csv'))
    plot_disapproval_drivers(results, os.path.join(output_dir, 'viz_drivers_disapproval.png'))
    
    # Pain Curve for top driver
    top_shield = results.index[0]
    plot_pain_curve(df_model, top_shield, disapproval_target, 
                   os.path.join(output_dir, f'viz_pain_{top_shield}.png'),
                   f'Pain Curve: Importance of {top_shield}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="Path to input file")
    parser.add_argument("--target", help="Raw approval column", required=True)
    parser.add_argument("--val", help="Value that means APPROVAL", type=int, default=1)
    parser.add_argument("--attributes", help="Comma-separated attribute columns", required=True)
    parser.add_argument("--output", default="output", help="Output directory")
    args = parser.parse_args()
    
    run_political_science(args.data, args.target, args.val, args.attributes.split(','), args.output)
