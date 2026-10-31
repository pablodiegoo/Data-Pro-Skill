# Funcionalidades Implementadas — Data-Pro-Skill v2.0

## 1. Data Grilling & Governança de Domínio (Fase 0–1)

| Funcionalidade | Comando / Script | Status |
| :--- | :--- | :---: |
| Reconhecimento Silencioso de Fatos (*Fact Reconnaissance*) | `/dps-grill`, `quant_analyzer.py` | ✅ Implementado |
| Entrevista em Rodadas de Fronteira (`❓ Q#` + `➡️ Default`) | `/dps-grill` (`references/dps-clarify.md`) | ✅ Implementado |
| Mapeamento Programático `snake_case` (`column_mapping.json`) | `/dps-setup`, `quant_analyzer.py` | ✅ Implementado |
| Ponderação Amostral Raking / IPF + $N_{\text{eff}}$ de Kish | `/dps-setup`, `weighting.py` | ✅ Implementado |
| Portões de Qualidade Artigo 6 (*Straight-Lining*, soma 100%, *Missingness*) | `/dps-setup`, `quant_analyzer.py` | ✅ Implementado |

## 2. Cruzamentos, Testes de Hipóteses e Ciência de Pesquisa (Fase 2–5)

| Funcionalidade | Comando / Script | Status |
| :--- | :--- | :---: |
| Seletor de Testes Estatísticos + 88 Regras (`reasoning_rules.csv`) | `/dps-plan`, `crosstabs.py` | ✅ Implementado |
| Validação de Sobreposição de Pulo (`0x0 Branching Overlap`) | `/dps-cross`, `crosstabs.py` | ✅ Implementado |
| Testes Paramétricos e Não-Paramétricos + Tamanhos de Efeito | `/dps-cross`, `/dps-execute`, `crosstabs.py` | ✅ Implementado |
| Matriz de Resíduos Padronizados de Qui-Quadrado ($z_{ij}$) | `/dps-cross`, `crosstabs.py`, `tufte_viz.py` | ✅ Implementado |
| *Pure Sentiment Stack* (Centralização Ipsativa + Remoção de Efeito Halo) | `/dps-advanced`, `advanced_analytics_generator.py` | ✅ Implementado |
| Matriz de Prioridade (Importância Derivada $\times$ Performance) | `/dps-advanced`, `advanced_analytics_generator.py` | ✅ Implementado |
| Resíduos de Expectativa (*Disappointed / Aligned / Delighted*) | `/dps-advanced`, `advanced_analytics_generator.py` | ✅ Implementado |
| Correlação Dupla (Pearson $r$ vs. Spearman $\rho$) | `/dps-advanced`, `crosstabs.py` | ✅ Implementado |
| Clusterização Dupla (K-Means Silhouette + DBSCAN Outliers `-1`) | `/dps-advanced`, `advanced_analytics_generator.py` | ✅ Implementado |
| Análise Fatorial / PCA Multi-Pass + Alfa de Cronbach ($\alpha$) | `/dps-advanced`, `survey_pca.py` | ✅ Implementado |
| Otimização de Alcance TURF | `/dps-advanced`, `turf_analysis.py` | ✅ Implementado |

## 3. Injeção Qualitativa & Exportação HTML Tufte Pronta para Impressão (Fase 6–7)

| Funcionalidade | Comando / Script | Status |
| :--- | :--- | :---: |
| Categorização Temática com Stopwords Bilíngues (PT + EN) | `/dps-inject-open`, `qualitative_categorizer.py` | ✅ Implementado |
| Proteção Artigo 4 ($N < 30$ apenas contagens brutas `"4 of 19"`) | `/dps-inject-open`, `qualitative_categorizer.py` | ✅ Implementado |
| Auditoria de Silêncio por Segmento (*Silence Notes*) | `/dps-inject-open`, `qualitative_categorizer.py` | ✅ Implementado |
| Gráficos Vetoriais `<svg>` Estilo Tufte (Dot Plot, Heatmap $z_{ij}$, Priority Matrix) | `/dps-export`, `tufte_viz.py` | ✅ Implementado |
| Relatório Primário em HTML Estilo Edward Tufte (`final_report.html`) | `/dps-export`, `tufte_html.py` | ✅ Implementado |
| Impressão Nativa para PDF com Cabeçalho e Rodapé Correntes (`@page` + `.print-frame`) | `/dps-export`, `references/styles/tufte.css` | ✅ Implementado |
