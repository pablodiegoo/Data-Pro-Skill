# Phase 2: Quantitative Analysis - Context

**Gathered:** 2026-05-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Adicionar a lógica completa dos comandos quantitativos ao SKILL.md:

1. **`/dps-clarify`** — Perguntas abertas adaptativas sobre objetivos de negócio e hipóteses antes de tocar nos dados (3-5 perguntas, adaptadas ao contexto)
2. **`/dps-plan`** — Checklist de análises sugeridas (testes, cruzamentos, variáveis) — sugestão, não requisito
3. **`/dps-cross [VarX] x [VarY]`** — Tabelas densas estilo Tufte com teste estatístico automático
4. **`/dps-execute`** — Execução autônoma de análise quantitativa, independente do `/dps-plan`
5. **`/dps-mode:quant`** — Ativa persona Estatístico Sênior para todas as operações quantitativas

</domain>

<decisions>
## Implementation Decisions

### Banco de perguntas `/dps-clarify`
- **D-01:** Perguntas abertas adaptativas — a IA gera perguntas contextualizadas com base nos dados fornecidos, não um template fixo
- **D-02:** Categorias de referência (não template rígido): (1) objetivo de negócio, (2) hipóteses do stakeholder, (3) surpresas esperadas, (4) decisões dependentes, (5) qualidade/confiabilidade dos dados
- **D-03:** Máximo 5 perguntas, mínimo 3, adaptadas ao contexto específico

### Seleção de testes no `/dps-cross`
- **D-04:** O agente Estatístico decide o teste baseado nos dados observados
- **D-05:** A Statistical Test Selector Matrix em `agents/agent-statistician.md` serve como guia de referência, não como regra rígida
- **D-06:** O agente Crítico valida a escolha do teste (assunções atendidas? poder estatístico suficiente?)

### `/dps-plan` e `/dps-execute` independentes
- **D-07:** `/dps-plan` gera um checklist de análises sugeridas (VarX × VarY, teste Z recomendado) — é uma sugestão, não requisito
- **D-08:** `/dps-execute` roda análise autônoma sem depender do `/dps-plan` — pode ser usado sozinho
- **D-09:** Se `/dps-plan` foi executado antes, `/dps-execute` referencia o plano como ponto de partida, mas se adapta aos dados reais

### Herdado da Fase 1
- Prefixo `/dps-` em todos os comandos
- Zero XML tags no SKILL.md
- Output Tufte (tabelas com N, notas de margem, zero fluff)
- DPS naming convention
- constitution.md como dependência (já existe)

### the agent's Discretion

O planner tem liberdade para:
- Ordem exata das seções no SKILL.md para os novos comandos (desde que sigam o padrão estabelecido na Fase 1)
- Estrutura detalhada do checklist do `/dps-plan` (desde que seja um checklist, não narrativa)
- Exemplos específicos no `/dps-clarify` para guiar a IA na geração de perguntas adaptativas

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Fundação (Fase 1)
- `SKILL.md` — Meta-prompt principal (222 linhas, agent loop, /dps-setup implementado)
- `constitution.md` — 6 artigos, 8 regras de rigor (160 linhas)
- `agents/agent-statistician.md` — Agente Estatístico (Statistical Test Selector Matrix)
- `agents/agent-critic.md` — Agente Crítico (6 dimensões de auditoria)
- `agents/agent-tufte-designer.md` — Regras de output Tufte

### Planejamento
- `.planning/ROADMAP.md` — Fase 2 goal e success criteria
- `.planning/REQUIREMENTS.md` — Requisitos CLAR-01, PLAN-01, CROSS-01/02, EXEC-01, MODE-01
- `.planning/phases/01-constitution-setup/01-CONTEXT.md` — Decisões da Fase 1
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `SKILL.md` § Internal Agent Loop — Estrutura de 3 estágios já implementada, fase 2 adiciona comandos sem alterar o loop
- `SKILL.md` § Command: /dps-setup — Padrão de documentação de comando (seções ## Command, ### Execution Steps, ### Output Format)
- `SKILL.md` § Command Reference — Lista de comandos já definidos com /dps- prefixo
- `agents/agent-statistician.md` — Statistical Test Selector Matrix já existe como referência para /dps-cross
- `constitution.md` — Regras de output Tufte já forçadas pelo Designer

### Established Patterns
- Cada comando no SKILL.md segue: ## Command: /dps-{name} → ### Execution Steps → ### Output Format
- Agentes referenciados por nome (Statistician, Critic, Tufte Designer) — nunca duplicados inline
- YAML frontmatter como formato de saída para dados estruturados

### Integration Points
- `/dps-cross` usa o agente Estatístico → Crítico → Tufte Designer (loop existente)
- `/dps-execute` pode usar `/dps-setup` como fonte de segmentos (document-driven)
- `/dps-mode:quant` altera o comportamento do loop de agentes (mais foco numérico)
</code_context>

<specifics>
## Specific Ideas

- O `/dps-clarify` deve ser a PRIMEIRA coisa a rodar ao detectar novos dados — antes de qualquer cálculo
- A matriz de testes estatísticos em agent-statistician.md cobre: χ², Fisher's exact, t-test, Mann-Whitney U, ANOVA, Kruskal-Wallis, Pearson's r, Spearman's ρ, regressão linear
- O `/dps-cross` deve SEMPRE incluir N, %, teste estatístico, e nota de margem no output
- O `/dps-execute` deve priorizar cruzamentos baseados nos segmentos definidos no `/dps-setup` (document-driven)
</specifics>

<deferred>
## Deferred Ideas

- Testes estatísticos avançados (regressão múltipla, MANOVA, análise fatorial) — fase futura ou modo especializado
- Visualização automática de distribuições — fase 4 (export)
- Integração com Python/R para cálculos estatísticos precisos — fora do escopo do meta-prompt puro

</deferred>

---

*Phase: 02-quantitative-analysis*
*Context gathered: 2026-05-25*
