# Comandos — Data-Pro-Skill v2

## Pipeline Principal

### `/setup`
Gera o manifesto quantitativo — a âncora de contexto para toda análise subsequente.

**Input esperado:**
- Dados brutos (CSV, sumário de frequências, tabelas)
- Ou referência a um arquivo de dados

**Output:**
```yaml
---
project: "Nome do Projeto"
sample_size: N
metrics: [metric1, metric2, ...]
segments: [seg1, seg2, ...]
---
# Manifesto Quantitativo

## Matriz de Segmentos
| Segmento | N | % | Métrica Core |
| ... |
```

**Regras:**
- Toda tabela inclui N e volumetria
- Segmentos são definidos e nomeados
- Nenhuma análise posterior pode contradizer este manifesto

### `/cross [VarX] x [VarY]`
Cruza variáveis com tabelas densas estilo Tufte.

**Uso:** `/cross Faixa_Etaria x NPS`

**Output:**
- Tabela de contingência com N, %, e insights
- Nota de margem interpretativa
- Teste estatístico apropriado (χ², t-test, ANOVA, etc.)
- Margem de erro quando aplicável

### `/inject-open [texto ou arquivo]`
Categoriza respostas abertas dentro dos segmentos quantitativos existentes.

**Uso:** `/inject-open respostas_abertas.csv`

**Regras críticas:**
- Nunca criar seções standalone de qualitativo
- Sempre anexar a um segmento definido no `/setup`
- N < 30: citar verbatims, NUNCA reportar porcentagens
- Notar ausência de temas esperados

### `/export`
Consolida toda análise em um arquivo Markdown limpo.

**Output:** `outputs/final_report.md`
- Pronto para Quarto/LaTeX/PDF
- Inclui YAML frontmatter com metadados do projeto
- Todas as tabelas, notas de margem e análises consolidadas

---

## Comandos Auxiliares

### `/clarify`
Faz 3-5 perguntas provocativas sobre objetivos de negócio antes de tocar nos dados.

**Propósito:** Evitar que a IA rode análises sem entender o contexto de negócio.

### `/plan`
Desenha o plano analítico antes da execução.

**Output:** Quais testes serão usados, quais variáveis serão cruzadas, e por quê.

---

## Modos Especializados

### `/mode:quant`
Ativa persona **Estatístico Sênior** — correlações, crosstabs, NPS, Churn, CSAT.

### `/mode:quali`
Ativa persona **Antropólogo** — dores latentes, sentimento, arquétipos, jornadas.

### `/mode:strategy`
Ativa persona **Diretor de BI** — recomendações de negócio acionáveis.

---

## Comandos GSD (Gestão do Projeto)

| Comando | Descrição |
|---------|-----------|
| `/gsd-new-project` | Inicializar projeto |
| `/gsd-plan-phase N` | Planejar fase N |
| `/gsd-execute-phase N` | Executar fase N |
| `/gsd-verify-work N` | Verificar trabalho da fase |
| `/gsd-ship N` | Criar PR da fase |
| `/gsd-quick` | Tarefas rápidas |
| `/gsd-progress` | Ver progresso |
| `/gsd-settings` | Configurações |

Ver [COMMANDS.md do GSD](COMMANDS-GSD.md) para referência completa.
