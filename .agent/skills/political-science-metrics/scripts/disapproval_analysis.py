
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

def run_inverse_regression(df):
    """
    Runs Logistic Regression targeting DISAPPROVAL (0).
    We flip the target: y = (aprovacao_bin == 0).astype(int)
    """
    # Define Target: 1 represents Disapproval
    target_col = 'desaprovacao_bin'
    df[target_col] = (df['aprovacao_bin'] == 0).astype(int)
    
    features = [
        'humilde_respeitosa', 'honesta_correta', 'carismatica', 
        'competente', 'confianca', 'proxima_pessoas', 
        'preparada_tecnicamente', 'inteligente_resolve', 
        'propostas', 'autonomia', 'foco_cidade', 'realidade_populacao'
    ]
    
    # Drop rows with missing values
    df_model = df.dropna(subset=[target_col] + features).copy()
    
    X = df_model[features]
    y = df_model[target_col]
    X = sm.add_constant(X)
    
    model = sm.Logit(y, X).fit(disp=0)
    
    # Process Results for Visualization
    summary = model.summary2().tables[1]
    results = pd.DataFrame({
        'OR': np.exp(summary['Coef.']),
        'pvalue': summary['P>|z|'],
        'Coef': summary['Coef.']
    })
    
    # We want to know: Which low scores drive disapproval?
    # In this model (Target=Disapproval):
    # Negative Coef for Attribute X means: Higher Score in X -> Lower prob of Disapproval.
    # So, Low Score in X -> Higher prob of Disapproval.
    # The attributes with the most NEGATIVE coefficients are the ones where failure is costliest.
    
    results['Importance'] = results['Coef'].abs()
    results = results.drop('const', errors='ignore').sort_values(by='Coef', ascending=True) # Most negative first
    
    return results, df_model

def plot_disapproval_drivers(results, output_path):
    """
    Plots the attributes that most shield against disapproval (Strongest Negative Coefs).
    """
    label_map = {
        'humilde_respeitosa': 'Humilde e Respeitosa',
        'honesta_correta': 'Honesta e Correta',
        'carismatica': 'Carismática',
        'competente': 'Competente',
        'confianca': 'Inspira Confiança',
        'proxima_pessoas': 'Próxima das Pessoas',
        'preparada_tecnicamente': 'Preparada Tecnicamente',
        'inteligente_resolve': 'Inteligente e Resolve',
        'propostas': 'Boas Propostas',
        'autonomia': 'Tem Autonomia',
        'foco_cidade': 'Foco na Cidade',
        'realidade_populacao': 'Conhece a Realidade'
    }
    
    # Map index
    results.index = [label_map.get(x, x.replace('_', ' ').title()) for x in results.index]

    plt.figure(figsize=(10, 8))
    
    # improving readability: "Impacto na Redução da Rejeição"
    # Negative coef means: Increasing this attribute significantly REDUCES rejection.
    sns.barplot(x='Coef', y=results.index, data=results, palette='RdYlGn')
    
    plt.title('Quais falhas geram Desaprovação?\n(Coeficientes Negativos = Atributos que Evitam Rejeição)', fontsize=14)
    plt.xlabel('Força do Impacto (Coeficiente Logit)', fontsize=12)
    plt.axvline(0, color='gray', linestyle='--')
    plt.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Saved inverse drivers plot to {output_path}")

def plot_pain_curve(df, feature, output_path, title):
    """
    Plots the probability of DISAPPROVAL as the attribute score drops.
    """
    label_map = {
        'humilde_respeitosa': 'Humilde e Respeitosa',
        'honesta_correta': 'Honesta e Correta',
        'carismatica': 'Carismática',
        'competente': 'Competente',
        'confianca': 'Inspira Confiança',
        'proxima_pessoas': 'Próxima das Pessoas',
        'preparada_tecnicamente': 'Preparada Tecnicamente',
        'inteligente_resolve': 'Inteligente e Resolve',
        'propostas': 'Boas Propostas',
        'autonomia': 'Tem Autonomia',
        'foco_cidade': 'Foco na Cidade',
        'realidade_populacao': 'Conhece a Realidade'
    }
    
    target = 'desaprovacao_bin'
    data = df[[feature, target]].dropna().copy()
    
    X = sm.add_constant(data[feature])
    y = data[target]
    model = sm.Logit(y, X).fit(disp=0)
    
    x_range = np.linspace(0, 10, 100)
    X_pred = sm.add_constant(x_range)
    y_pred = model.predict(X_pred)
    
    clean_feature = label_map.get(feature, feature.replace("_", " ").title())
    
    plt.figure(figsize=(10, 6))
    
    # Curve
    plt.plot(x_range, y_pred, color='#c0392b', linewidth=3)
    plt.fill_between(x_range, y_pred, color='#c0392b', alpha=0.1)
    
    plt.title(title.replace(feature.title(), clean_feature), fontsize=14)
    plt.xlabel(f'Nota no Atributo: {clean_feature}', fontsize=12)
    plt.ylabel('Probabilidade de REJEIÇÃO (0-100%)', fontsize=12)
    plt.ylim(-0.05, 1.05)
    plt.grid(True, alpha=0.3)
    
    plt.savefig(output_path)
    print(f"Saved pain curve to {output_path}")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, 'db', 'processed', 'survey_cleaned.csv')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'assets', 'results')
    
    df = load_data(DATA_PATH)
    results, df_model = run_inverse_regression(df)
    
    # Save Stats
    results.to_csv(os.path.join(OUTPUT_DIR, 'disapproval_drivers.csv'))
    
    # Plot 1: The Drivers
    plot_disapproval_drivers(results, os.path.join(OUTPUT_DIR, 'viz_drivers_disapproval.png'))
    
    # Plot 2: Detailed Curve for Top Shield (likely correlated with Top Driver)
    # Get the attribute with the most negative coefficient (biggest shield)
    top_shield = results.index[0] 
    plot_pain_curve(
        df_model, 
        feature=top_shield, 
        output_path=os.path.join(OUTPUT_DIR, f'viz_pain_{top_shield}.png'),
        title=f'Anatomia da Rejeição: O Perigo da Falta de "{top_shield.title()}"'
    )
