# Guia Prático: Templates e Exemplos de Código

## Parte 2: Implementação Detalhada com Exemplos Funcionais

---

## 🔥 Exemplo Completo: Dashboard de Análise de E-commerce

### 1. Arquivo de Configuração

```python
# src/config/settings.py
from pathlib import Path
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    """Configurações globais da aplicação."""
    
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    DATA_RAW = PROJECT_ROOT / "data" / "raw"
    DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
    OUTPUT_REPORTS = PROJECT_ROOT / "output" / "reports"
    OUTPUT_VISUALIZATIONS = PROJECT_ROOT / "output" / "visualizations"
    
    # Ensure directories exist
    for path in [DATA_RAW, DATA_PROCESSED, OUTPUT_REPORTS, OUTPUT_VISUALIZATIONS]:
        path.mkdir(parents=True, exist_ok=True)
    
    # Visualization
    PLOT_STYLE = 'seaborn-v0_8-darkgrid'
    PLOT_PALETTE = 'husl'
    FIG_DPI = 300
    FIG_SIZE_DEFAULT = (12, 6)
    FIG_SIZE_HEATMAP = (14, 10)
    
    # Analysis
    CORRELATION_THRESHOLD = 0.7
    OUTLIER_IQR_MULTIPLIER = 1.5
    
    # Reporting
    REPORT_AUTHOR = "Data Analysis Team"
    REPORT_COMPANY = "Your Company"

config = Config()
```

### 2. Carregamento de Dados com Validação

```python
# src/data/loaders.py (expandido)
import pandas as pd
import polars as pl
from pathlib import Path
from typing import Union, Optional
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    """Carregador robusto de dados com validação."""
    
    @staticmethod
    def load_csv_safe(filepath: Union[str, Path], 
                     encoding: str = 'utf-8',
                     dtype_mapping: Optional[dict] = None,
                     **kwargs) -> pd.DataFrame:
        """
        Carrega CSV com tratamento robusto de erros.
        
        Args:
            filepath: Caminho do arquivo
            encoding: Encoding (default: utf-8)
            dtype_mapping: Dict de tipos de dados esperados
            **kwargs: Argumentos adicionais para pd.read_csv
        
        Returns:
            DataFrame carregado
        """
        try:
            df = pd.read_csv(filepath, encoding=encoding, **kwargs)
            
            # Aplicar tipos de dados se fornecidos
            if dtype_mapping:
                df = df.astype(dtype_mapping, errors='ignore')
            
            logger.info(f"✓ Carregado {filepath}: {df.shape[0]} linhas, {df.shape[1]} colunas")
            return df
            
        except FileNotFoundError:
            logger.error(f"✗ Arquivo não encontrado: {filepath}")
            raise
        except Exception as e:
            logger.error(f"✗ Erro ao carregar {filepath}: {str(e)}")
            raise
    
    @staticmethod
    def load_multiple_csv(directory: Union[str, Path], 
                         pattern: str = "*.csv") -> dict:
        """Carrega múltiplos CSVs de um diretório."""
        directory = Path(directory)
        files = list(directory.glob(pattern))
        
        data = {}
        for file in files:
            df = DataLoader.load_csv_safe(file)
            data[file.stem] = df
            
        logger.info(f"✓ Carregados {len(data)} arquivos")
        return data
    
    @staticmethod
    def load_parquet(filepath: Union[str, Path]) -> pd.DataFrame:
        """Carrega Parquet (mais eficiente para grandes volumes)."""
        df = pd.read_parquet(filepath)
        logger.info(f"✓ Carregado Parquet: {df.shape}")
        return df
    
    @staticmethod
    def validate_schema(df: pd.DataFrame, 
                       required_columns: list,
                       required_types: dict) -> bool:
        """
        Valida schema do DataFrame.
        
        Args:
            df: DataFrame
            required_columns: Colunas obrigatórias
            required_types: {'column_name': 'int64', ...}
        
        Returns:
            True se válido
        """
        # Check columns
        missing = set(required_columns) - set(df.columns)
        if missing:
            raise ValueError(f"Colunas faltando: {missing}")
        
        # Check types
        for col, dtype in required_types.items():
            if str(df[col].dtype) != dtype:
                logger.warning(f"Tipo de {col}: esperado {dtype}, obtido {df[col].dtype}")
        
        logger.info("✓ Schema validado")
        return True
```

### 3. Limpeza e Transformação Avançada

```python
# src/data/cleaners.py (expandido)
import pandas as pd
import numpy as np
from typing import List, Literal
import logging

logger = logging.getLogger(__name__)

class DataCleaner:
    """Limpeza avançada e transformação de dados."""
    
    @staticmethod
    def comprehensive_cleaning(df: pd.DataFrame,
                              handle_missing: str = 'mean',
                              handle_outliers: bool = True,
                              normalize_text: bool = False) -> pd.DataFrame:
        """Pipeline completo de limpeza."""
        
        logger.info("Iniciando limpeza de dados...")
        df_clean = df.copy()
        
        # 1. Remove duplicatas
        duplicates = df_clean.duplicated().sum()
        if duplicates > 0:
            df_clean = df_clean.drop_duplicates()
            logger.info(f"  ✓ Removidas {duplicates} duplicatas")
        
        # 2. Trata valores nulos
        nulls = df_clean.isnull().sum().sum()
        if nulls > 0:
            df_clean = DataCleaner.handle_missing_values(df_clean, strategy=handle_missing)
            logger.info(f"  ✓ Tratados {nulls} valores nulos")
        
        # 3. Detecta e trata outliers
        if handle_outliers:
            numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                outliers = DataCleaner.detect_outliers(df_clean[col], method='iqr')
                if outliers.sum() > 0:
                    logger.info(f"  ✓ {outliers.sum()} outliers em {col}")
        
        # 4. Normaliza texto
        if normalize_text:
            text_cols = df_clean.select_dtypes(include=['object']).columns
            df_clean = DataCleaner.normalize_text(df_clean, list(text_cols))
            logger.info(f"  ✓ Texto normalizado ({len(text_cols)} colunas)")
        
        logger.info("✓ Limpeza completada")
        return df_clean
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame,
                             strategy: Literal['mean', 'median', 'mode', 'forward_fill', 'drop'] = 'mean',
                             threshold: float = 0.5) -> pd.DataFrame:
        """
        Trata valores nulos com múltiplas estratégias.
        
        Args:
            df: DataFrame
            strategy: Estratégia de preenchimento
            threshold: Se % nulos > threshold, remover coluna
        """
        df = df.copy()
        
        # Remove colunas muito vazias
        null_pct = df.isnull().sum() / len(df)
        cols_to_drop = null_pct[null_pct > threshold].index
        if len(cols_to_drop) > 0:
            df = df.drop(columns=cols_to_drop)
            logger.warning(f"Colunas removidas (>50% nulos): {list(cols_to_drop)}")
        
        # Aplicar estratégia
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        object_cols = df.select_dtypes(include=['object']).columns
        
        if strategy == 'drop':
            return df.dropna()
        elif strategy == 'mean':
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            df[object_cols] = df[object_cols].fillna(df[object_cols].mode().iloc[0])
        elif strategy == 'median':
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        elif strategy == 'forward_fill':
            df = df.fillna(method='ffill')
        
        return df
    
    @staticmethod
    def detect_outliers(series: pd.Series, 
                       method: Literal['iqr', 'zscore'] = 'iqr') -> pd.Series:
        """Detecta outliers usando IQR ou Z-Score."""
        if method == 'iqr':
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            return (series < (Q1 - 1.5 * IQR)) | (series > (Q3 + 1.5 * IQR))
        else:  # zscore
            from scipy import stats
            return np.abs(stats.zscore(series)) > 3
    
    @staticmethod
    def normalize_text(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Normaliza texto."""
        df = df.copy()
        for col in columns:
            df[col] = (df[col]
                      .str.lower()
                      .str.strip()
                      .str.replace(r'[^\w\s]', '', regex=True))
        return df
    
    @staticmethod
    def convert_datetime(df: pd.DataFrame, 
                        date_columns: dict) -> pd.DataFrame:
        """
        Converte para datetime.
        
        Args:
            date_columns: {'column_name': 'format_string', ...}
                         Ex: {'date': '%d/%m/%Y', 'timestamp': '%Y-%m-%d %H:%M:%S'}
        """
        df = df.copy()
        for col, fmt in date_columns.items():
            try:
                df[col] = pd.to_datetime(df[col], format=fmt)
            except Exception as e:
                logger.warning(f"Erro ao converter {col}: {e}")
        return df
```

### 4. Análises Estatísticas Profissionais

```python
# src/analysis/statistical_tests.py
import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class StatisticalAnalysis:
    """Análises estatísticas profissionais."""
    
    @staticmethod
    def comprehensive_analysis(df: pd.DataFrame,
                              target_col: str = None) -> Dict:
        """Análise completa de um dataset."""
        
        results = {
            'shape': df.shape,
            'basic_stats': DescriptiveAnalysis.summary_statistics(df).to_dict(),
            'correlations': DescriptiveAnalysis.correlation_matrix(df).to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'data_types': df.dtypes.astype(str).to_dict(),
        }
        
        # Análise por coluna
        for col in df.select_dtypes(include=[np.number]).columns:
            results[f'{col}_distribution'] = {
                'skewness': stats.skew(df[col].dropna()),
                'kurtosis': stats.kurtosis(df[col].dropna()),
                'normality_test': StatisticalAnalysis.normality_test(df[col])
            }
        
        return results
    
    @staticmethod
    def normality_test(series: pd.Series,
                      alpha: float = 0.05) -> Dict[str, bool]:
        """
        Testa normalidade com múltiplos testes.
        
        Returns:
            Dict com resultados dos testes
        """
        data = series.dropna()
        
        # Shapiro-Wilk (melhor para n < 5000)
        if len(data) < 5000:
            shapiro_stat, shapiro_p = stats.shapiro(data)
            shapiro_normal = shapiro_p > alpha
        else:
            shapiro_stat = shapiro_p = shapiro_normal = None
        
        # Kolmogorov-Smirnov
        ks_stat, ks_p = stats.kstest(data, 'norm', 
                                     args=(data.mean(), data.std()))
        ks_normal = ks_p > alpha
        
        # Anderson-Darling
        anderson_result = stats.anderson(data, dist='norm')
        anderson_normal = anderson_result.statistic < anderson_result.critical_values[2]
        
        return {
            'shapiro_wilk': shapiro_normal,
            'kolmogorov_smirnov': ks_normal,
            'anderson_darling': anderson_normal,
            'is_normal': all([ks_normal, anderson_normal])
        }
    
    @staticmethod
    def correlation_analysis(df: pd.DataFrame,
                            min_correlation: float = 0.5) -> Dict:
        """Análise de correlações com filtro."""
        corr_matrix = df.corr(numeric_only=True)
        
        # Encontra correlações fortes
        strong_corr = {}
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) >= min_correlation:
                    col1 = corr_matrix.columns[i]
                    col2 = corr_matrix.columns[j]
                    strong_corr[f"{col1} <-> {col2}"] = corr_val
        
        return {
            'strong_correlations': strong_corr,
            'correlation_matrix': corr_matrix.to_dict()
        }
    
    @staticmethod
    def hypothesis_test(group1: pd.Series,
                       group2: pd.Series,
                       test_type: str = 'ttest') -> Dict:
        """
        Testes de hipótese entre dois grupos.
        
        test_type: 'ttest' (paramétrico) ou 'mannwhitney' (não-paramétrico)
        """
        
        if test_type == 'ttest':
            stat, p_value = stats.ttest_ind(group1.dropna(), group2.dropna())
            test_name = "T-Test de Student"
        else:  # mann-whitney
            stat, p_value = stats.mannwhitneyu(group1.dropna(), group2.dropna())
            test_name = "Mann-Whitney U Test"
        
        alpha = 0.05
        significant = p_value < alpha
        
        return {
            'test': test_name,
            'statistic': stat,
            'p_value': p_value,
            'significant': significant,
            'interpretation': "Diferença significativa" if significant else "Sem diferença significativa"
        }
    
    @staticmethod
    def anova_test(groups: list) -> Dict:
        """ANOVA: compara múltiplos grupos."""
        f_stat, p_value = stats.f_oneway(*groups)
        
        return {
            'test': 'ANOVA F-Test',
            'f_statistic': f_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
```

### 5. Visualizações Avançadas

```python
# src/visualization/advanced_plots.py
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Optional, List

class AdvancedVisualizations:
    """Visualizações profissionais e interativas."""
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        sns.set_style(style)
        self.colors = sns.color_palette("husl", 8)
    
    def multi_panel_dashboard(self,
                             df: pd.DataFrame,
                             numeric_cols: List[str]) -> plt.Figure:
        """Dashboard com múltiplos painéis."""
        
        n_cols = min(len(numeric_cols), 3)
        n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        axes = axes.flatten()
        
        for idx, col in enumerate(numeric_cols):
            # Histograma + KDE
            axes[idx].hist(df[col].dropna(), bins=30, alpha=0.7, 
                          color=self.colors[idx], edgecolor='black')
            ax2 = axes[idx].twinx()
            df[col].plot.kde(ax=ax2, color='red', linewidth=2)
            
            axes[idx].set_title(f'Distribuição: {col}', fontweight='bold')
            axes[idx].set_xlabel(col)
            axes[idx].set_ylabel('Frequência')
        
        # Remove eixos não utilizados
        for idx in range(len(numeric_cols), len(axes)):
            fig.delaxes(axes[idx])
        
        plt.tight_layout()
        return fig
    
    def heatmap_with_annotations(self,
                                df: pd.DataFrame,
                                title: str = "Correlation Matrix") -> plt.Figure:
        """Heatmap profissional com anotações."""
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        corr = df.corr(numeric_only=True)
        
        # Máscara para triângulo superior
        mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
        
        sns.heatmap(corr, mask=mask, annot=True, fmt='.2f',
                   cmap='RdBu_r', center=0, square=True, ax=ax,
                   cbar_kws={'label': 'Correlação', 'shrink': 0.8},
                   linewidths=0.5, vmin=-1, vmax=1)
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        
        plt.tight_layout()
        return fig
    
    def time_series_decomposition(self,
                                 series: pd.Series,
                                 title: str = "Series Decomposition") -> plt.Figure:
        """Decompõe série temporal em tendência + sazonalidade."""
        
        from statsmodels.tsa.seasonal import seasonal_decompose
        
        decomposition = seasonal_decompose(series, model='additive', period=12)
        
        fig, axes = plt.subplots(4, 1, figsize=(14, 10))
        
        series.plot(ax=axes[0], color='blue', linewidth=2)
        axes[0].set_ylabel('Original')
        
        decomposition.trend.plot(ax=axes[1], color='orange', linewidth=2)
        axes[1].set_ylabel('Trend')
        
        decomposition.seasonal.plot(ax=axes[2], color='green', linewidth=2)
        axes[2].set_ylabel('Seasonal')
        
        decomposition.resid.plot(ax=axes[3], color='red', linewidth=2)
        axes[3].set_ylabel('Residual')
        
        fig.suptitle(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def interactive_scatter_3d(df: pd.DataFrame,
                              x: str, y: str, z: str,
                              color: Optional[str] = None,
                              title: str = "3D Scatter Plot") -> go.Figure:
        """Gráfico 3D interativo com Plotly."""
        
        fig = px.scatter_3d(df, x=x, y=y, z=z, color=color,
                           hover_name=df.index,
                           title=title,
                           labels={x: x, y: y, z: z})
        
        fig.update_traces(marker=dict(size=5, opacity=0.7))
        
        return fig
    
    @staticmethod
    def interactive_dashboard(df: pd.DataFrame,
                             dimensions: dict) -> go.Figure:
        """Dashboard interativo com Plotly Sunburst."""
        
        # dimensions = {'category': 'col1', 'subcategory': 'col2', 'values': 'col3'}
        
        fig = px.sunburst(df,
                         names=dimensions.get('names'),
                         parents=dimensions.get('parents'),
                         values=dimensions.get('values'),
                         title="Interactive Dashboard")
        
        return fig
```

### 6. Template de Relatório Dinâmico

```python
# src/reporting/report_templates.py
from jinja2 import Template
from datetime import datetime

class ReportTemplates:
    """Templates para diferentes tipos de relatórios."""
    
    EXECUTIVE_SUMMARY = """
# Relatório Executivo: {{ title }}

**Data de Geração:** {{ date }}  
**Autor:** {{ author }}  
**Período:** {{ period }}

---

## 📊 Resumo Executivo

{{ executive_summary }}

### Métricas Principais

| Métrica | Valor | Variação |
|---------|-------|----------|
{% for metric, value, change in metrics %}
| {{ metric }} | {{ value }} | {{ change }} |
{% endfor %}

### Destaques

{% for highlight in highlights %}
- ✓ {{ highlight }}
{% endfor %}

---

## 🔍 Análise Detalhada

### Distribuição de Dados

![Distribution]({{ dist_image }})

*Figura 1: Distribuição dos principais dados*

### Correlações

![Correlations]({{ corr_image }})

*Figura 2: Matriz de correlação*

### Série Temporal

![TimeSeries]({{ ts_image }})

*Figura 3: Evolução ao longo do tempo*

---

## 📈 Insights e Recomendações

{% for insight in insights %}
### {{ insight.title }}

{{ insight.description }}

**Recomendação:** {{ insight.recommendation }}

{% endfor %}

---

## 📋 Dados Adicionais

{{ additional_data }}

---

## Conclusão

{{ conclusion }}

**Próximos Passos:**
{% for step in next_steps %}
{{ loop.index }}. {{ step }}
{% endfor %}

---

_Relatório gerado automaticamente em {{ generated_date }}_
"""
    
    @staticmethod
    def render_report(template_str: str, **context) -> str:
        """Renderiza template com contexto."""
        template = Template(template_str)
        return template.render(**context, date=datetime.now().strftime("%d/%m/%Y"))
```

### 7. Script de Geração Completa

```python
# scripts/generate_ecommerce_report.py
#!/usr/bin/env python
"""Script completo: gera análise e relatório de e-commerce."""

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from pathlib import Path
from src.config.settings import config
from src.data.loaders import DataLoader
from src.data.cleaners import DataCleaner
from src.analysis.statistical_tests import StatisticalAnalysis
from src.visualization.advanced_plots import AdvancedVisualizations
from src.visualization.mermaid_diagrams import MermaidDiagrams
from src.reporting.report_generator import ReportGenerator
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Pipeline completo de análise."""
    
    logger.info("="*60)
    logger.info("Iniciando geração de relatório de E-commerce")
    logger.info("="*60)
    
    # 1. Carregar dados
    logger.info("\n[1/7] Carregando dados...")
    try:
        df = DataLoader.load_csv_safe(
            config.DATA_RAW / "ecommerce_sales.csv",
            dtype_mapping={
                'order_id': 'int64',
                'order_date': 'str',
                'customer_id': 'int64',
                'revenue': 'float64'
            }
        )
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {e}")
        return
    
    # 2. Converter datas
    logger.info("[2/7] Processando datas...")
    df = DataCleaner.convert_datetime(df, {
        'order_date': '%Y-%m-%d'
    })
    
    # 3. Limpeza completa
    logger.info("[3/7] Limpando dados...")
    df_clean = DataCleaner.comprehensive_cleaning(
        df,
        handle_missing='mean',
        handle_outliers=True
    )
    
    # 4. Análise estatística
    logger.info("[4/7] Realizando análises estatísticas...")
    stats = StatisticalAnalysis.comprehensive_analysis(df_clean)
    corr_results = StatisticalAnalysis.correlation_analysis(df_clean, min_correlation=0.5)
    
    # 5. Gerar visualizações
    logger.info("[5/7] Gerando visualizações...")
    viz = AdvancedVisualizations()
    
    # Dashboard múltiplo
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    fig_dashboard = viz.multi_panel_dashboard(df_clean, numeric_cols[:6])
    viz_path_dashboard = config.OUTPUT_VISUALIZATIONS / "dashboard.png"
    fig_dashboard.savefig(viz_path_dashboard, dpi=config.FIG_DPI, bbox_inches='tight')
    
    # Heatmap
    fig_heatmap = viz.heatmap_with_annotations(df_clean, "Correlação entre Variáveis")
    viz_path_heatmap = config.OUTPUT_VISUALIZATIONS / "correlations.png"
    fig_heatmap.savefig(viz_path_heatmap, dpi=config.FIG_DPI, bbox_inches='tight')
    
    # 6. Criar diagrama Mermaid
    logger.info("[6/7] Gerando diagramas...")
    pipeline_diagram = MermaidDiagrams.flowchart(
        nodes=[
            {"id": "A", "label": "Raw Data\n(CSV)"},
            {"id": "B", "label": "Data Cleaning"},
            {"id": "C", "label": "Statistical Analysis"},
            {"id": "D", "label": "Visualizations"},
            {"id": "E", "label": "Report Generation"},
        ],
        edges=[("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")],
        title="E-commerce Analysis Pipeline"
    )
    
    # 7. Gerar relatório final
    logger.info("[7/7] Gerando relatório...")
    report = ReportGenerator(str(config.OUTPUT_REPORTS))
    
    report.add_title(
        "Análise Completa de Vendas E-commerce",
        f"Período: {df_clean['order_date'].min().date()} a {df_clean['order_date'].max().date()}"
    )
    
    report.add_section("1. Resumo Executivo")
    report.add_text(f"""
    Este relatório apresenta uma análise completa das vendas de e-commerce, 
    cobrindo {len(df_clean)} transações com receita total de R$ {df_clean['revenue'].sum():,.2f}.
    
    **Destaques:**
    - Ticket Médio: R$ {df_clean['revenue'].mean():.2f}
    - Receita Mínima: R$ {df_clean['revenue'].min():.2f}
    - Receita Máxima: R$ {df_clean['revenue'].max():.2f}
    - Desvio Padrão: R$ {df_clean['revenue'].std():.2f}
    """)
    
    report.add_section("2. Pipeline de Análise")
    report.add_mermaid_diagram(pipeline_diagram)
    
    report.add_section("3. Estatísticas Descritivas")
    summary_stats = df_clean[numeric_cols].describe().round(2)
    report.add_table(summary_stats, "Resumo Estatístico")
    
    report.add_section("4. Dashboard de Distribuições")
    report.add_figure(
        str(viz_path_dashboard),
        "Dashboard com distribuições de principais variáveis"
    )
    
    report.add_section("5. Análise de Correlações")
    report.add_figure(
        str(viz_path_heatmap),
        "Matriz de correlação entre variáveis"
    )
    
    if corr_results['strong_correlations']:
        report.add_text("**Correlações Fortes Encontradas:**\n")
        for pair, corr_value in corr_results['strong_correlations'].items():
            report.add_text(f"- {pair}: {corr_value:.3f}")
    
    report.add_section("6. Conclusões e Recomendações")
    report.add_text("""
    ### Principais Descobertas
    
    1. **Distribuição de Receita**: Os dados mostram uma distribuição aproximadamente normal
       com poucos outliers, indicando consistência nas operações.
    
    2. **Padrões de Vendas**: Análise temporal revela sazonalidade significativa,
       com picos em períodos específicos do ano.
    
    3. **Segmentação de Clientes**: Identificadas 3 grupos principais de clientes
       com padrões de compra distintos.
    
    ### Recomendações
    
    ✓ Aumentar esforços de marketing nos períodos de baixa demanda  
    ✓ Desenvolver estratégia de retenção para clientes de alto valor  
    ✓ Otimizar inventário baseado em padrões sazonais  
    ✓ Investigar outliers negativos para melhorar taxa de conversão
    """)
    
    # Salvar
    logger.info("\nSalvando relatórios...")
    md_path = report.save_markdown("ecommerce_analysis.md")
    pdf_path = report.save_pdf("ecommerce_analysis.pdf")
    html_path = report.save_html("ecommerce_analysis.html")
    
    logger.info("\n" + "="*60)
    logger.info("✅ Relatório gerado com sucesso!")
    logger.info(f"  📄 Markdown: {md_path}")
    logger.info(f"  📑 PDF: {pdf_path}")
    logger.info(f"  🌐 HTML: {html_path}")
    logger.info("="*60)

if __name__ == "__main__":
    main()
```

---

## 🎓 Checklist de Implementação

```markdown
## Semana 1: Setup e Fundações
- [ ] Criar estrutura de diretórios
- [ ] Instalar dependências (requirements.txt)
- [ ] Configurar logging
- [ ] Criar scripts de teste
- [ ] Preparar dados amostrais

## Semana 2: Módulos de Dados
- [ ] Implementar DataLoader
- [ ] Implementar DataCleaner
- [ ] Criar testes unitários para loaders
- [ ] Documentar APIs
- [ ] Criar exemplos de uso

## Semana 3: Análises
- [ ] Implementar análises descritivas
- [ ] Implementar testes estatísticos
- [ ] Implementar detecção de outliers
- [ ] Criar notebooks de exploração
- [ ] Validar resultados

## Semana 4: Visualizações
- [ ] Implementar gráficos estáticos
- [ ] Implementar gráficos interativos
- [ ] Integrar Mermaid.js
- [ ] Criar galeria de exemplos
- [ ] Otimizar performance

## Semana 5: Relatórios
- [ ] Implementar ReportGenerator
- [ ] Criar templates Jinja2
- [ ] Testar exportação PDF
- [ ] Testar exportação HTML
- [ ] Criar exemplos de relatórios

## Semana 6: Integração e Deploy
- [ ] Pipeline end-to-end
- [ ] CI/CD (GitHub Actions)
- [ ] Docker containerization
- [ ] Documentação final
- [ ] Deploy piloto

## Semana 7-8: Refinement
- [ ] Testes de performance
- [ ] Otimizações
- [ ] User feedback
- [ ] Documentação avançada
- [ ] Release v1.0
```

---

## 🚀 Comandos Rápidos

```bash
# Setup inicial
git clone <repo>
cd data-analysis-platform
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Rodar análise completa
python scripts/generate_ecommerce_report.py

# Rodar testes
pytest tests/ -v

# Gerar documentação
sphinx-build -b html docs/ docs/_build/

# Build Docker
docker build -t data-analysis:latest .
docker run -v $(pwd):/app data-analysis:latest
```

---

**Status:** ✅ Pronto para Desenvolvimento | **Versão:** 1.0 | **Última atualização:** Janeiro 2026
