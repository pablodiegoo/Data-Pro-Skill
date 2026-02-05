
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

def plot_heatmap(corr_matrix, title, output_path):
    plt.figure(figsize=(12, 10))
    # Mask upper triangle
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    # Rename index/columns for display - Force rename via list assertion
    new_index = [label_map.get(x, x.replace('_', ' ').title()) for x in corr_matrix.index]
    new_columns = [label_map.get(x, x.replace('_', ' ').title()) for x in corr_matrix.columns]
    
    display_matrix = corr_matrix.copy()
    display_matrix.index = new_index
    display_matrix.columns = new_columns
    
    print("Labels being used for heatmap:", display_matrix.columns.tolist())
    
    sns.heatmap(display_matrix, mask=mask, annot=True, fmt='.2f', 
                cmap='BrBG', center=0, vmin=-1, vmax=1, # BrBG palette
                linewidths=0.5, cbar_kws={"shrink": .8})
    
    plt.title(title, fontsize=16)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Saved heatmap to {output_path}")

def analysis_ipsative(df, attributes):
    """
    1. Calcula a média pessoal de cada respondente.
    2. Subtrai a média pessoal de cada atributo.
    3. Gera matriz de correlação.
    """
    print("Iniciando Análise Ipsativa...")
    
    # Select subset
    data = df[attributes].dropna().copy()
    
    # 1. Calculate Personal Mean
    data['personal_mean'] = data.mean(axis=1)
    
    # 2. Subtract Mean (Ipsative Transformation)
    ipsative_data = pd.DataFrame()
    for col in attributes:
        ipsative_data[f'{col}_ips'] = data[col] - data['personal_mean']
    
    # 3. Correlation
    corr = ipsative_data.corr()
    
    # Rename columns for display (remove _ips)
    corr.columns = [c.replace('_ips', '') for c in corr.columns]
    corr.index = [c.replace('_ips', '') for c in corr.index]
    
    return corr

def analysis_residuals(df, attributes):
    """
    1. Identifica a Imagem Geral (Categorica -> Numérica).
    2. Regressão: Atributo ~ Imagem Geral.
    3. Pega os Resíduos (O que sobra do atributo tirando o Halo da Imagem).
    4. Matriz de Correlação dos Resíduos.
    """
    print("Iniciando Análise de Resíduos do Halo...")
    
    # Identify General Image column
    # Based on column inspection, likely candidates start with '26.' or similar.
    # In prep script, we didn't explicitly rename a '26' column to 'imagem_geral'.
    # We will look for it dynamically using startswith logic similar to prep script.
    
    img_col = None
    for col in df.columns:
        if col.startswith('26.') or 'imagem' in col.lower():
             img_col = col
             break
    
    # Use Personal Mean as the Halo Proxy. Drop NaNs to ensure OLS works.
    data = df[attributes].dropna().copy()
    data['personal_mean'] = data[attributes].mean(axis=1)
    X = sm.add_constant(data['personal_mean'])
    
    residuals = pd.DataFrame()
    for attr in attributes:
        y = data[attr]
        model = sm.OLS(y, X).fit()
        residuals[f'{attr}_resid'] = model.resid
            
    # Correlation of Residuals
    corr = residuals.corr()
    # Rename columns
    corr.columns = [c.replace('_resid', '') for c in corr.columns]
    corr.index = [c.replace('_resid', '') for c in corr.index]
    
    return corr
        


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, 'db', 'processed', 'survey_cleaned.csv')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'assets', 'results')
    
    df = load_data(DATA_PATH)
    

    attributes = [
        'humilde_respeitosa', 'honesta_correta', 'carismatica', 
        'competente', 'confianca', 'proxima_pessoas', 
        'preparada_tecnicamente', 'inteligente_resolve', 
        'propostas', 'autonomia', 'foco_cidade', 'realidade_populacao'
    ]
    
    # 1. Ipsative Analysis
    corr_ips = analysis_ipsative(df, attributes)
    corr_ips.to_csv(os.path.join(OUTPUT_DIR, 'my_ipsative_matrix.csv')) # SAVE CSV
    plot_heatmap(corr_ips, 
                 'Matriz Ipsativa (Viés Pessoal Removido)\nComo os atributos negociam prioridade na mente do eleitor', 
                 os.path.join(OUTPUT_DIR, 'viz_corr_ipsative.png'))
    
    # 2. Residual Analysis (Halo Removed)
    corr_resid = analysis_residuals(df, attributes)
    if corr_resid is not None:
        corr_resid.to_csv(os.path.join(OUTPUT_DIR, 'my_residuals_matrix.csv')) # SAVE CSV
        plot_heatmap(corr_resid, 
                     'Matriz de Resíduos (Efeito Halo Removido)\nConexões "puras" entre atributos', 
                     os.path.join(OUTPUT_DIR, 'viz_corr_residuals.png'))
