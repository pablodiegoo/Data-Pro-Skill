# Phase 1: Constitution & Setup - Context

**Gathered:** 2026-05-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Estabelecer os fundamentos do Data-Pro-Skill v2:

1. **constitution.md** — Regras inegociáveis de rigor estatístico, rigor qualitativo, qualidade de dados e tratamento de viés
2. **SKILL.md** — Meta-prompt principal orquestrando o loop de agentes e comandos
3. **Comando `/dps-setup`** — Gera o manifesto quantitativo (YAML frontmatter + tabela de segmentos) que ancora toda análise subsequente
4. **Loop de agentes invisíveis** — Estatístico → Crítico → Designer Tufte, orquestrado pelo SKILL.md
5. **Regras de output Tufte** — Zero prosa fluff, tabelas autoexplicativas com N, notas de margem interpretativas
6. **Nomenclatura DPS** — Todos os comandos usam prefixo `/dps-`; textos internos referenciam "DPS" (não "GSD")

</domain>

<decisions>
## Implementation Decisions

### Formato do Manifesto `/dps-setup`
- **D-01:** YAML frontmatter com: `project`, `framework` ("Data-Pro-Skill v2"), `sample_size`, `metrics_tracked` (array), `segments` (array)
- **D-02:** Tabela Markdown simples com colunas: Segmento | N | % | Métrica Core
- **D-03:** Sem mapa de cruzamento sugerido no manifesto — manter simples e focado

### Regras do `constitution.md`
- **D-04:** 5 regras core: (1) margem de erro obrigatória em claims amostrais, (2) p < 0.05 para significância, (3) proibição de prosa fluff, (4) proibição de % em amostras quali N<30, (5) N mínimo para testes paramétricos
- **D-05:** Regras de qualidade de dados: detecção de straight-lining em Likert, validação de soma de % = 100%, flag de missing data >10%
- **D-06:** Estrutura sugerida: 6 artigos, cada um com regra + justificativa + consequência da violação

### Loop de Agentes Invisíveis
- **D-07:** Arquivos separados em `agents/` (agent-statistician.md, agent-critic.md, agent-tufte-designer.md) — já criados
- **D-08:** SKILL.md referencia e orquestra os agentes: "Antes de responder, execute internamente: 1. Valide números (Estatístico), 2. Audite vieses (Crítico), 3. Formate output Tufte (Designer). Apenas o output do Designer é exibido."
- **D-09:** Agentes especializados (agent-anthropologist.md, agent-strategist.md) são ativados pelos comandos `/dps-mode:quali` e `/dps-mode:strategy`

### Nomenclatura GSD → DPS
- **D-10:** Todos os comandos do meta-prompt usam prefixo `/dps-`: `/dps-setup`, `/dps-cross`, `/dps-inject-open`, `/dps-export`, `/dps-clarify`, `/dps-plan`, `/dps-mode:quant`, `/dps-mode:quali`, `/dps-mode:strategy`
- **D-11:** Nos textos internos do meta-prompt, substituir "GSD" por "DPS". O engine `get-shit-done/` mantém o nome original como dependência de infraestrutura

### the agent's Discretion

O planner tem liberdade para:
- Estrutura exata de parágrafos no constitution.md (desde que cubra as 8 regras decididas)
- Organização das seções do SKILL.md (desde que cubra agent loop, comandos, output rules)
- Nomes de variáveis no YAML frontmatter do manifesto (desde que incluam os campos decididos)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Projeto
- `.planning/PROJECT.md` — Visão, core value, constraints, key decisions
- `.planning/REQUIREMENTS.md` — 21 requisitos v1, traceability matrix
- `.planning/ROADMAP.md` — 4 fases, Phase 1 goal e success criteria
- `.planning/STATE.md` — Estado atual do projeto
- `AGENTS.md` — Stack, conventions, architecture, project skills
- `CONTEXT.md` — Histórico do projeto e decisões arquiteturais (raiz)
- `.deprecated/v1/coonversa.md` — Conversa original de design com Gemini

### Agentes (já criados)
- `agents/agent-statistician.md` — Validação numérica, distribuições, testes
- `agents/agent-critic.md` — Detecção de vieses, correlações espúrias
- `agents/agent-tufte-designer.md` — Formatação de output Tufte
- `agents/agent-anthropologist.md` — Análise qualitativa (fase 3)
- `agents/agent-strategist.md` — Recomendações de negócio (fase 4)

### Documentação
- `docs/ARCHITECTURE.md` — Arquitetura do meta-prompt
- `docs/COMMANDS.md` — Referência de comandos
- `docs/FEATURES.md` — Funcionalidades planejadas
- `docs/USER-GUIDE.md` — Guia do usuário

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `agents/agent-statistician.md` — Já define o formato de output (Statistician Report) com sample profile, distributions, recommended tests, quality flags
- `agents/agent-critic.md` — Já define 6 dimensões de auditoria (bias, spurious correlations, overgeneralization, missing data, analysis quality, prose fluff)
- `agents/agent-tufte-designer.md` — Já define regras de output (tabelas com N, margin notes, forbidden phrases, output structure)

### Established Patterns
- YAML frontmatter + Markdown puro — usado em todos os documentos do projeto
- Agentes como arquivos .md com frontmatter (name, description, color, tools) — padrão do engine GSD
- Comandos como arquivos .md em `commands/gsd/` — estrutura existente

### Integration Points
- `SKILL.md` será o arquivo principal que o usuário copia para o diretório de skills do harness
- `constitution.md` deve ser copiado junto com `SKILL.md` (dependência)
- Os agentes em `agents/` são referenciados mas não precisam ser copiados (o SKILL.md contém as instruções orquestradoras inline)
</code_context>

<specifics>
## Specific Ideas

- O manifesto `/dps-setup` deve incluir uma nota de margem inicial: "Este documento ancora o contexto numérico. Nenhuma análise posterior pode contradizer as métricas estabelecidas aqui."
- O `constitution.md` deve seguir o estilo dos 6 artigos, similar a uma constituição legal: cada artigo tem regra + justificativa + consequência
- O SKILL.md deve começar com o loop de agentes (é a primeira coisa que a IA precisa internalizar)
- Exemplo de output Tufte no README.md pode ser reutilizado como referência
</specifics>

<deferred>
## Deferred Ideas

- Tradução do meta-prompt para outros idiomas (inglês, espanhol) — fase futura
- Script de instalação automatizada para cada harness — fase 4 (export)
- Templates Quarto/LaTeX para o `/dps-export` — fase 4
- Logo e identidade visual DPS — fora do escopo do meta-prompt

</deferred>

---

*Phase: 01-constitution-setup*
*Context gathered: 2026-05-25*
