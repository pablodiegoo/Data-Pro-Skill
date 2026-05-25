import nbformat as nbf
import os

def create_relevancia_notebook():
    nb = nbf.v4.new_notebook()
    cells = []
    
    # Title
    cells.append(nbf.v4.new_markdown_cell("""# 📊 Reprodução da Tabela de Relevância e Gráficos de Churn

Este notebook demonstra passo a passo matematicamente como recriar a tabela de **Relevância** e **Conjunto (Acima/Abaixo da Média)** usando Python e `pandas`, e em seguida, como gerar gráficos visuais atraentes para apresentar esses resultados.

### A Matemática por trás (Análise de Resíduos do Qui-Quadrado):
1. **Frequência Observada (O):** Quantas pessoas *realmente* disseram que abandonaram a Plataforma X pelo Motivo Y.
2. **Frequência Esperada (E):** Quantas pessoas *matematicamente se esperaria* que dessem essa resposta, baseando-se na média geral (se todas as plataformas fossem iguais).
3. **Conjunto:** Se `O > E`, então está **Acima da Média**. Se `O < E`, está **Abaixo da média**.
4. **Relevância:** Calculada a partir da diferença entre o Observado e o Esperado (geralmente através do Resíduo Padronizado: `|O - E| / sqrt(E)`)."""))

    # Imports & Setup
    cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

# Configurações de estilo para gráficos mais bonitos
plt.style.use('default')
sns.set_theme(style="whitegrid", palette="muted")
import warnings
warnings.filterwarnings('ignore')"""))

    # Load and Prepare Data
    cells.append(nbf.v4.new_markdown_cell("""## 1. Carregando e Preparando os Dados
Primeiro, vamos carregar a base em Parquet e explodir a pergunta de múltipla escolha para cruzar "Plataforma" x "Motivo"."""))

    cells.append(nbf.v4.new_code_cell("""# Carregar os dados processados
df = pd.read_parquet('../database/processed/OS18_Marketplace_Processed.parquet')

# Isolar colunas Q12 (Plataformas) e Q13 (Motivos)
q12_cols = [c for c in df.columns if 'hoje não vende mais' in c]
q13_col = 'Q13'

# Transformar de Largo para Longo (Unpivot)
df_long = pd.melt(df, id_vars=['ID de resposta', q13_col], value_vars=q12_cols, 
                  var_name='Pergunta', value_name='Plataforma')

# Remover vazios e limpar strings
df_long = df_long.dropna(subset=['Plataforma'])
df_long['Plataforma'] = df_long['Plataforma'].astype(str).str.strip()
df_long['Motivo'] = df_long[q13_col].astype(str).str.strip()
df_long = df_long[df_long['Motivo'] != 'nan']

# Criar a Tabela de Contingência (Frequências Observadas)
crosstab = pd.crosstab(df_long['Motivo'], df_long['Plataforma'])
print("Frequências Observadas (Contagem Absoluta):")
display(crosstab)"""))

    # Calculating Statistics
    cells.append(nbf.v4.new_markdown_cell("""## 2. Calculando as Métricas (Esperado, Conjunto e Relevância)
Vamos usar a função `chi2_contingency` do SciPy para nos dar a matriz "Esperada". Depois, calculamos a Relevância usando os Resíduos Padronizados:
$$Relevância = \\frac{|Observado - Esperado|}{\\sqrt{Esperado}}$$"""))

    cells.append(nbf.v4.new_code_cell("""# Obter a matriz esperada
chi2, p, dof, expected = chi2_contingency(crosstab)
expected_df = pd.DataFrame(expected, index=crosstab.index, columns=crosstab.columns)

# Lista para armazenar os resultados linha a linha
resultados = []

# Iterar sobre cada Motivo e Plataforma
for motivo in crosstab.index:
    for plataforma in crosstab.columns:
        O = crosstab.loc[motivo, plataforma]
        E = expected_df.loc[motivo, plataforma]
        
        # Só analisar se a frequência esperada for maior que 0
        if E > 0:
            # Conjunto (Acima ou Abaixo da Média Esperada)
            conjunto = 'Acima da Média' if O > E else 'Abaixo da média'
            
            # Relevância (Resíduo Padronizado Absoluto)
            # Obs: Multiplicamos por 100 ou ajustamos a escala dependendo de como a sua plataforma exibiu.
            # Vemos na sua tabela original números como 1.73205 (que é exatamente a raiz quadrada de 3).
            relevancia = abs(O - E) / np.sqrt(E)
            
            resultados.append({
                'Motivo': motivo,
                'Plataforma': plataforma,
                'Relevancia_Score': relevancia,
                'Conjunto': conjunto,
                'Observado': O,
                'Esperado': round(E, 2)
            })

# Transformar numa tabela bonita igual a sua
df_resultados = pd.DataFrame(resultados)

# Formatando a coluna relevância como texto com %
df_resultados['Relevancia'] = df_resultados['Relevancia_Score'].apply(lambda x: f"{x:,.5f}%".replace('.', ','))

# Exibir a Tabela Final semelhante à do usuário
df_resultados = df_resultados.sort_values(by=['Plataforma', 'Conjunto', 'Relevancia_Score'], ascending=[True, False, False])
tabela_final = df_resultados[['Motivo', 'Plataforma', 'Relevancia', 'Conjunto', 'Observado', 'Esperado']]

display(tabela_final.head(20))"""))

    # Visualizations
    cells.append(nbf.v4.new_markdown_cell("""## 3. Gerando Gráficos Visuais dos Gargalos Específicos
Para apresentar isso num relatório para o cliente final (Sebrae), uma tabela de números é difícil de ler. O ideal é gerar **Gráficos de Barras de Divergência**, mostrando os pontos "Acima da Média" (Gargalos Específicos da Plataforma) e "Abaixo da Média" (Onde a plataforma vai bem)."""))

    cells.append(nbf.v4.new_code_cell("""# Filtrando apenas as principais plataformas para não poluir os gráficos
principais_plataformas = ['Mercado Livre', 'Shopee', 'Magalu', 'Americanas']

for plat in principais_plataformas:
    # Pegar os dados só daquela plataforma
    plat_data = df_resultados[df_resultados['Plataforma'] == plat].copy()
    
    # Para o gráfico de divergência, vamos deixar "Abaixo da Média" negativo
    plat_data['Score_Plot'] = plat_data.apply(
        lambda row: row['Relevancia_Score'] if row['Conjunto'] == 'Acima da Média' else -row['Relevancia_Score'], 
        axis=1
    )
    
    # Filtrar apenas os itens com relevância forte (maior que 0.5 para o exemplo ser legível)
    plat_data = plat_data[plat_data['Relevancia_Score'] > 0.5].sort_values('Score_Plot')
    
    if len(plat_data) == 0:
        continue
        
    # Plot
    plt.figure(figsize=(10, 6))
    colors = ['#e74c3c' if x > 0 else '#2ecc71' for x in plat_data['Score_Plot']]
    
    bars = plt.barh(plat_data['Motivo'], plat_data['Score_Plot'], color=colors)
    
    # Customização
    plt.axvline(0, color='black', linewidth=1)
    plt.title(f'Pain Points vs Diferenciais Específicos: {plat}', fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Relevância (← Vai melhor que a concorrência | Gargalo crítico desta plataforma →)')
    
    # Esconder as bordas extras
    sns.despine(left=True, bottom=True)
    plt.show()"""))

    nb['cells'] = cells
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    os.makedirs(os.path.join(project_dir, 'notebooks'), exist_ok=True)
    out_path = os.path.join(project_dir, 'notebooks', 'Relevancia_Graficos_Churn.ipynb')
    
    with open(out_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
        
    print(f"Notebook successfully created at: {out_path}")

if __name__ == "__main__":
    create_relevancia_notebook()
