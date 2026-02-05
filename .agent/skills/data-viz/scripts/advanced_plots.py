
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import os

def load_data(filepath):
    return pd.read_csv(filepath)

def plot_predicted_probability(df, feature, target, output_path, title):
    """
    Plots the logistic regression curve: Probability of Approval vs Attribute Score.
    Visualizes the "Slope" of the driver.
    """
    # Clean data for this pair
    data = df[[feature, target]].dropna().copy()
    
    # Fit simple model for visualization line
    X = sm.add_constant(data[feature])
    y = data[target]
    model = sm.Logit(y, X).fit(disp=0)
    
    # Generate prediction line
    x_range = np.linspace(0, 10, 100)
    X_pred = sm.add_constant(x_range)
    y_pred = model.predict(X_pred)
    
    plt.figure(figsize=(10, 6))
    
    # Scatter plot with jitter to show density
    sns.stripplot(x=feature, y=target, data=data, 
                  jitter=0.1, alpha=0.1, color='gray', size=4)
    
    # Plot the curve
    plt.plot(x_range, y_pred, color='#e74c3c', linewidth=3, label='Probabilidade de Aprovação')
    
    plt.title(title, fontsize=14, pad=20)
    plt.xlabel(f'Nota: {feature.replace("_", " ").title()}', fontsize=12)
    plt.ylabel('Probabilidade de Aprovação (0-100%)', fontsize=12)
    plt.ylim(-0.1, 1.1)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.savefig(output_path)
    print(f"Saved probability plot to {output_path}")

def plot_correlation_matrix(df, attributes, output_path):
    """
    Plots correlation heatmap to show how attributes relate to each other.
    """
    corr = df[attributes].corr()
    
    plt.figure(figsize=(12, 10))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', 
                cmap='RdBu_r', center=0, vmin=-1, vmax=1,
                linewidths=0.5, cbar_kws={"shrink": .8})
    
    plt.title('Matriz de Correlação: Atributos de Imagem', fontsize=16)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Saved correlation map to {output_path}")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, 'db', 'processed', 'survey_cleaned.csv')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'assets', 'results')
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = load_data(DATA_PATH)
    
    # 1. Plot Probability Curve for Top Driver (Humility)
    plot_predicted_probability(
        df, 
        feature='humilde_respeitosa', 
        target='aprovacao_bin',
        output_path=os.path.join(OUTPUT_DIR, 'viz_prob_humildade.png'),
        title='Impacto da "Humildade" na Aprovação'
    )
    
    # 2. Plot Probability Curve for Weakness (Autonomy)
    plot_predicted_probability(
        df, 
        feature='autonomia', 
        target='aprovacao_bin',
        output_path=os.path.join(OUTPUT_DIR, 'viz_prob_autonomia.png'),
        title='Impacto da "Autonomia" na Aprovação'
    )
    
    # 3. Correlation Matrix
    attributes = [
        'humilde_respeitosa', 'honesta_correta', 'carismatica', 
        'competente', 'confianca', 'proxima_pessoas', 
        'preparada_tecnicamente', 'inteligente_resolve', 
        'propostas', 'autonomia', 'foco_cidade', 'realidade_populacao'
    ]
    plot_correlation_matrix(df, attributes, os.path.join(OUTPUT_DIR, 'viz_correlation_matrix.png'))
