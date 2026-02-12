
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_data(filepath):
    return pd.read_csv(filepath)

def run_logistic_regression(df):
    """
    Runs logistic regression to identify drivers of approval.
    Target: aprovacao_bin
    Features: Competence attributes (0-10)
    """
    target = 'aprovacao_bin'
    
    # Select feature columns (numeric Likert scales)
    features = [
        'competente', 'preparada_tecnicamente', 'inteligente_resolve', 
        'propostas', 'carismatica', 'proxima_pessoas', 'confianca', 
        'humilde_respeitosa', 'realidade_populacao', 'autonomia', 
        'honesta_correta', 'foco_cidade'
    ]
    
    # Drop rows with missing values in target or features
    df_model = df.dropna(subset=[target] + features).copy()
    
    X = df_model[features]
    y = df_model[target]
    
    # Add constant for intercept
    X = sm.add_constant(X)
    
    model = sm.Logit(y, X).fit(disp=0)
    print(model.summary())
    
    # Extract Odds Ratios
    params = model.params
    conf = model.conf_int()
    conf['OR'] = params
    conf.columns = ['2.5%', '97.5%', 'OR']
    
    # Calculate standardized importance (roughly) or mapped OR
    # For interpretation: OR > 1 means positive driver
    results = np.exp(conf)
    results['pvalue'] = model.pvalues
    results = results.drop(['const'], errors='ignore')
    results = results.sort_values('OR', ascending=False)
    
    return results

def plot_drivers(results, output_path):
    """Plots the Odds Ratios."""
    plt.figure(figsize=(10, 8))
    sns.set_style("whitegrid")
    
    # Filter for significant drivers (p < 0.1 for behavioral data often acceptable, but let's show all with color coding)
    results['Color'] = ['green' if p < 0.05 else 'gray' for p in results['pvalue']]
    
    sns.barplot(x='OR', y=results.index, data=results, palette=results['Color'].tolist())
    
    plt.axvline(x=1.0, color='red', linestyle='--')
    plt.title('Key Drivers of Approval (Odds Ratio)\nGreen = Statistically Significant (p<0.05)', fontsize=14)
    plt.xlabel('Odds Ratio (Impact on Approval Probability)')
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Saved drivers plot to {output_path}")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, 'db', 'processed', 'survey_cleaned.csv')
    OUTPUT_IMG = os.path.join(BASE_DIR, 'assets', 'results', 'drivers_approval.png')
    OUTPUT_CSV = os.path.join(BASE_DIR, 'assets', 'results', 'drivers_stats.csv')
    
    os.makedirs(os.path.dirname(OUTPUT_IMG), exist_ok=True)
    
    df = load_data(DATA_PATH)
    results = run_logistic_regression(df)
    results.to_csv(OUTPUT_CSV)
    plot_drivers(results, OUTPUT_IMG)
