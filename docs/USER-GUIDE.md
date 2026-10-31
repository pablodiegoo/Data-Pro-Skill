# Guia do Usuário — Data-Pro-Skill v2.0

## 1. Instalação

```bash
# Instalador interativo (instala localmente em .dps/ e/ou globalmente no seu harness):
node bin/install.js
```

## 2. Fluxo de Trabalho Recomendado

### Passo 0: Alinhar Objetivos com Data Grilling (`/dps-grill`)
Antes de rodar cruzamentos às cegas, inicie com:
```text
/dps-grill dados_pesquisa.csv
```
O agente inspecionará silenciosamente o arquivo (amostra $N$, escalas Likert, colunas de texto aberto, taxas de *missing*) e fará perguntas cirúrgicas em **Rodadas de Fronteira** (`❓ Q1` + `➡️ Recomendação Padrão`) para alinhar a decisão de negócio, hipóteses e segmentos prioritários.

### Passo 1: Setup e Higiene Estatística (`/dps-setup`)
```text
/dps-setup dados_pesquisa.csv
```
Gera o mapeamento `column_mapping.json`, o perfil `00_profile.json` e audita os **Portões de Qualidade do Artigo 6** (*Straight-Lining* em baterias Likert, soma de porcentagens e dados faltantes).

### Passo 2 a 5: Plano, Cruzamentos e Ciência de Pesquisa (`/dps-plan`, `/dps-execute`, `/dps-advanced`)
- `/dps-plan` monta o plano de testes estatísticos.
- `/dps-cross Segmento x Satisfacao` ou `/dps-execute` roda os testes de hipóteses ($\chi^2$, $t$ de Welch, ANOVA, Kruskal-Wallis), calcula **Resíduos Padronizados ($z_{ij}$)** e monta o **Effect-Size Leaderboard**.
- `/dps-advanced` remove o **Efeito Halo** (via Centralização Ipsativa e Resíduos de Regressão), constrói a **Matriz de Prioridade**, segmenta **Resíduos de Expectativa** (*Disappointed / Aligned / Delighted*), extrai **Personas K-Means + Outliers DBSCAN**, calcula o **Alfa de Cronbach ($\alpha$)** e roda **TURF**.

### Passo 6: Injeção de Perguntas Abertas (`/dps-inject-open`)
```text
/dps-inject-open
```
Categoriza respostas abertas dentro dos segmentos quantitativos, citando $\ge 2$ verbatims literais por tema, registrando **Silence Notes** para segmentos silenciosos e aplicando a regra de contagens brutas (`"4 of 19"`) sempre que $N < 30$.

### Passo 7: Exportação em HTML Tufte Pronto para Impressão em PDF (`/dps-export`)
```text
/dps-export
```
Gera `.dps/outputs/export/final_report.html` (e `final_report.md` + `verification_report.json`).

## 3. Como Imprimir ou Salvar `final_report.html` como PDF

1. Abra `.dps/outputs/export/final_report.html` em qualquer navegador moderno (Chrome, Edge, Brave, Firefox ou Safari).
2. Clique no botão **`🖨️ Print / Save as PDF`** na barra superior (ou pressione `Ctrl+P` / `Cmd+P`).
3. Selecione **Salvar como PDF** (*Save as PDF*).
4. O arquivo HTML já contém regras `@page` e uma estrutura `<table class="print-frame">` que reserva margens superiores e inferiores em **todas as páginas impressas**, renderizando automaticamente o **cabeçalho corrente** (título do projeto + classificação) e o **rodapé corrente** (framework, amostra $N$, margem de erro IC 95% e data) sem cortar tabelas ou gráficos `<svg>`.
