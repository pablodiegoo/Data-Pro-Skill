# Data-Pro-Skill v2.0 — Contexto Arquitetural e Modelo de Domínio

## 1. Visão Geral e Evolução

O **Data-Pro-Skill v2.0** é um sistema de inteligência analítica e pesquisa de mercado (quantitativa, psicométrica e qualitativa) projetado para agentes de IA. Ele transforma bases de dados brutas (`.csv`, `.xlsx`, `.ods`, `.parquet`) em relatórios analíticos **Edward Tufte em HTML prontos para impressão em PDF** (`final_report.html`), governados por uma Constituição Estatística de 8 Artigos (`constitution.md`).

### Problemas Resolvidos na Versão 2.0

1. **Alinhamento de Objetivo antes da Execução (`Data Grilling`):** Inspirado nas skills `grilling`, `domain-modeling` e `writing-for-agents` de Matt Pocock, o comando `/dps-grill` (`/dps-clarify`) realiza uma **Reconhecimento Silencioso de Fatos** nos dados antes de conduzir **Rodadas de Fronteira** (`❓ Q#` + `➡️ Recomendação Padrão`) com o usuário.
2. **Ciência de Pesquisa Profunda (`references/analysis/`):** Integração completa entre prompts e scripts Python (`scripts/*.py`) para remoção de **Efeito Halo** e **Centralização Ipsativa** (`Pure Sentiment Stack`), **Matriz de Prioridade** (Importância Derivada $\times$ Performance), **Resíduos de Expectativa** (*Disappointed / Aligned / Delighted*), **Correlação Dupla** (Pearson $r$ + Spearman $\rho$), **Resíduos Padronizados de Qui-Quadrado ($z_{ij}$)**, **Clusterização Dupla** (K-Means via Silhouette + DBSCAN para *outliers* `-1`), **Análise Fatorial / PCA + Alfa de Cronbach ($\alpha$)**, **TURF** e **Raking (IPF)**.
3. **HTML Pronto para Impressão em PDF com 5 Escolas de Design de Dados (`references/design-schools.md`):** Substituição de pipelines frágeis de LaTeX/Quarto por um compilador HTML autônomo (`scripts/design_schools.py` + `scripts/tufte_html.py` + `scripts/tufte_viz.py` + `references/styles/*.css`) que permite ao usuário escolher, durante o `/dps-setup` (ou `/dps-grill` / `node bin/install.js`), entre **5 Escolas Canônicas de Design de Dados**:
   - **`tufte` — Edward Tufte *(Padrão)***: Papel marfim (`#fffff8`), serifa Palatino, coluna 58%/36% com notas de margem flutuantes, tabelas `booktabs` e *Cleveland dot plots* (IC 95%).
   - **`few` — Stephen Few**: Grid perceptual de largura total (`#f8fafc`), *Bullet Graphs* com faixas qualitativas e linhas de meta, e alertas de limiar inline.
   - **`knaflic` — Cole Nussbaumer Knaflic (*Storytelling with Data*)**: Fundo branco limpo (`#ffffff`), contexto em cinza suave (`#cbd5e1`) + cor focal pré-atentiva única (`#1e40af` / `#ea580c`) e títulos de ação executivos.
   - **`swiss` — Swiss Grid & Jacques Bertin**: Grid modular arquitetônico exposto (`1.5px`/`4px` `#0a0a0a`), tipografia Neo-Grotesca e matrizes/lollipops retinianos de Bertin (`#e63946` e `#1d3557`).
   - **`editorial` — The Economist / Financial Times**: Papel editorial aquecido (`#fcf8f2`), barra superior carmesim (`#e3120b`), hierarquia *Kicker + Manchete + Standfirst* e gráficos lollipop jornalísticos.
   Todas as 5 escolas incluem cabeçalhos/rodapés correntes padronizados (`@page` + `<table class="print-frame">`) em todas as páginas ao imprimir como PDF (`Ctrl+P`) e um seletor interativo ao vivo na barra de ferramentas da tela.

---

## 2. Vocabulário Canônico (`GLOSSARY.md`)

Consulte [GLOSSARY.md](GLOSSARY.md) para as definições completas das **Leading Words** (*Leitworte*) do repositório:
- **Entregáveis de Dados:** `Setup Manifest`, `Column Mapping`, `Analysis Plan`, `Effect-Size Leaderboard`, `Verification Report`, `Tufte HTML Report`.
- **Protocolo de Entrevista:** `Data Grilling`, `Fact Reconnaissance`, `Design Tree`, `Frontier Round`, `Silence Note`.
- **Rigor Estatístico:** `Margin of Error (MoE)`, `Effective Sample Size (N_eff)`, `Pure Sentiment Stack`, `Ipsative Centering`, `Halo Residual`, `Priority Matrix`, `Expectation Residuals`, `Standardized Residuals (z_ij)`, `Dual Correlation`, `Dual Clustering`, `Cronbach's Alpha`, `TURF Analysis`, `Branching Overlap`.
- **Arquitetura Visual e Impressão:** `Answer-First Prose`, `Margin Note`, `Booktabs Table`, `Print Frame`.

---

## 3. Loop Invisível de 4 Agentes

```
Usuário → [Griller] → [Statistician] → [Methodological Critic] → [Tufte Designer] → Output Final
```

1. **Griller (`agents/agent-griller.md`):** Inspeciona o dataset silenciosamente, mapeia variáveis (`column_mapping.json` e `00_data_glossary.md`) e resolve a Árvore de Decisão de 5 ramos.
2. **Statistician (`agents/agent-statistician.md`):** Executa os scripts Python (`quant_analyzer.py`, `crosstabs.py`, `advanced_analytics_generator.py`), pareando estimadores paramétricos (`Média/DP`) e não-paramétricos (`Mediana/IIQ`), $p$-valores e tamanhos de efeito.
3. **Methodological Critic (`agents/agent-critic.md`):** Audita os Artigos 1–8 da Constituição (`constitution.md`), bloqueando porcentagens em amostras $N < 30$, exigindo nota de margem sobre *Straight-Lining* e garantindo divulgação de *Null Findings* ($p \ge 0.05$).
4. **Tufte Designer (`agents/agent-tufte-designer.md`):** Compila prosa *Answer-First*, tabelas *booktabs*, notas de margem `<aside class="margin-note">`, gráficos `<svg>` e o pacote HTML pronto para impressão em PDF (`final_report.html`).
