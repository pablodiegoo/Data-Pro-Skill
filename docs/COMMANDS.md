# Referência de Comandos — Data-Pro-Skill v2.0

## Pipeline Analítico Principal (Passos 0 a 7)

### Passo 0: `/dps-grill` *(alias `/dps-clarify`)*
Executa o protocolo **Data Grilling**: realiza reconhecimento silencioso do dataset (*Fact Reconnaissance*) e conduz **Rodadas de Fronteira** (`❓ Q#` + `➡️ Recomendação Padrão`) nos 5 ramos da Árvore de Decisão (*Destino de Decisão*, *Hipóteses*, *Espinha Dorsal Analítica*, *Pesos & Governança*, *Metodologias Avançadas*).
- **Saídas:** `.dps/outputs/setup/clarify_notes.md`, `.dps/outputs/setup/00_data_glossary.md`, `.dps/outputs/setup/column_mapping.json`.

### Passo 1: `/dps-setup`
Gera o perfil estatístico completo da base, mapeamento `snake_case` e executa os **Portões de Qualidade do Artigo 6** (*Straight-Lining*, soma de porcentagens e taxa de dados faltantes).
- **CLI Python:** `python3 scripts/quant_analyzer.py <dataset> --profile -o .dps/outputs/setup/`
- **Saídas:** `00_profile.json`, `setup_manifest.json`, `setup_segments.csv`, `setup_report.md`, `00_project_manifest.md`.

### Passo 2: `/dps-plan`
Constrói o Plano Analítico (`plan.md`) aplicando a árvore de decisão de testes estatísticos (`references/analysis/statistical_test_selector.md`) e as 88 regras de `reasoning_rules.csv`.
- **Saída:** `.dps/outputs/setup/plan.md`.

### Passo 3: `/dps-cross [VarX] x [VarY]`
Cruza duas variáveis com validação de **Branching Overlap** (`Artigo 7c`), teste de hipótese automático ($\chi^2$, Exato de Fisher, $t$ de Welch, Mann-Whitney $U$, ANOVA $F$, Kruskal-Wallis $H$, Correlação Dupla), tamanho de efeito (`Cramér's V`, `Cohen's d`, $\eta^2$) e matriz de **Resíduos Padronizados ($z_{ij}$)**.
- **CLI Python:** `python3 scripts/crosstabs.py <dataset> --index <VarX> --columns <VarY> -o .dps/outputs/cross/`
- **Saídas:** `cross_{X}_{Y}.csv`, `cross_{X}_{Y}_residuals.csv`, `cross_{X}_{Y}_stats.json`, `cross_{X}_{Y}_report.md`.

### Passo 4: `/dps-execute`
Executa autonomamente os cruzamentos planejados e gera o **Effect-Size Leaderboard** ranqueado por significância ($p < 0.05$) e magnitude de efeito.
- **CLI Python:** `python3 scripts/crosstabs.py <dataset> --execute-all -o .dps/outputs/cross/`
- **Saídas:** `execute_summary.md`, `execute_leaderboard.json`.

### Passo 5: `/dps-advanced`
Executa os 6 módulos profundos de ciência de pesquisa (`references/analysis/`):
1. **Pure Sentiment Stack:** Centralização Ipsativa ($X_{ij} - \bar{X}_i$) + Remoção de Efeito Halo por regressão.
2. **Priority Action Matrix:** Importância Derivada $\times$ Performance + $\text{Priority Score} = \text{Imp} \times (\text{Scale}_{\max} - \text{Perf})$.
3. **Key Drivers & Expectation Residuals:** OLS Padronizado + Random Forest + segmentação *Disappointed / Aligned / Delighted*.
4. **Dual Correlation Matrix:** Pearson $r$ (linear) vs. Spearman $\rho$ (monotônico).
5. **Dual Clustering & Psychometrics:** Personas K-Means otimizadas por Silhouette + detecção de *outliers* DBSCAN (`-1`) + PCA/Fatorial + **Alfa de Cronbach ($\alpha$)**.
6. **TURF Reach Optimization:** Alcance incremental não-duplicado.
- **CLI Python:** `python3 scripts/advanced_analytics_generator.py <dataset> --target <OutcomeCol> --report-dir .dps/outputs/advanced/`
- **Saídas:** `advanced_report.md`, `advanced_metrics.json`.

### Passo 6: `/dps-inject-open`
Categoriza respostas abertas com remoção de stopwords (PT + EN), vincula temas aos segmentos quantitativos e aplica o **Artigo 4** ($N < 30$ exige contagens brutas `"4 of 19"` sem `%`; $\ge 2$ verbatims literais por tema; **Silence Notes** para segmentos com 0 respostas).
- **CLI Python:** `python3 scripts/qualitative_categorizer.py <dataset> -o .dps/outputs/quali/`
- **Saídas:** `quali_themes.csv`, `quali_verbatims.json`, `quali_report.md`.

### Passo 7: `/dps-export`
Consolida todas as análises em `final_report.md`, audita os Artigos 1–8 (`verification_report.json`), gera gráficos `<svg>` estilo Tufte e compila o relatório **HTML Estilo Edward Tufte Pronto para Impressão em PDF** (`final_report.html`).
- **CLI Python:** `python3 scripts/final_report_generator.py --input .dps/outputs/ -o .dps/outputs/export/`
- **Saídas:** `final_report.html`, `final_report.md`, `verification_report.json`, `charts/*.svg`.

---

## Modos Especializados (`/dps-mode:*`)

- `/dps-mode:quant` — Ativa a lente **Estatístico Sênior**.
- `/dps-mode:quali` — Ativa a lente **Antropólogo Corporativo**.
- `/dps-mode:strategy` — Ativa a lente **Diretor de Estratégia / BI**.
