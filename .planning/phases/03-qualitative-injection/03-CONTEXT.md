# Phase 3: Qualitative Injection - Context

**Gathered:** 2026-05-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Adicionar análise qualitativa como ramificação dos segmentos quantitativos ao SKILL.md:

1. **`/dps-inject-open [texto]`** — IA extrai temas automaticamente de respostas abertas, identifica verbatims, categoriza dentro dos segmentos do `/dps-setup`
2. **`/dps-mode:quali`** — Ativa persona Antropólogo, adiciona 4a etapa ao loop de agentes
3. **Integração quali+quanti** — Output qualitativo como subseção dentro do segmento quantitativo correspondente

**Regra fundamental:** Qualitativo NUNCA standalone — sempre anexado a um segmento quantitativo existente.

</domain>

<decisions>
## Implementation Decisions

### Categorização `/dps-inject-open`
- **D-01:** IA extrai temas automaticamente de texto bruto (não requer CSV estruturado)
- **D-02:** Agente Antropólogo lê todas as respostas, identifica temas recorrentes, extrai verbatims representativos
- **D-03:** Temas são mapeados para segmentos definidos no manifesto do `/dps-setup`
- **D-04:** Frequência de temas reportada como contagem bruta (ex: "8 de 12 participantes"), nunca porcentagens para N<30

### Modo `/dps-mode:quali`
- **D-05:** Loop de agentes se torna 4 etapas: Estatístico → Crítico → **Antropólogo** → Designer Tufte
- **D-06:** Antropólogo analisa temas, extrai verbatims, identifica padrões emergentes
- **D-07:** Crítico audita: temas com <2 verbatims, generalizações indevidas, viés de confirmação qualitativo
- **D-08:** Session-scoped — afeta todos os comandos subsequentes até `/dps-mode:quant` ou reset

### Output quali+quanti
- **D-09:** Output quali aparece como subseção `### Análise Qualitativa — {Segmento}` dentro da seção do segmento quantitativo
- **D-10:** Subseção inclui: temas identificados (com frequência), verbatims (entre aspas), nota de margem conectando quali ao padrão quantitativo
- **D-11:** Nunca criar seções standalone de qualitativo — sempre dentro do segmento quantitativo

### Herdado das Fases 1-2
- Prefixo `/dps-`, zero XML, output Tufte, DPS naming
- SKILL.md: 405 linhas, 6 comandos implementados
- Agentes: agent-anthropologist.md e agent-strategist.md já existem
- constitution.md: regras de rigor quali (N<30 sem %, verabatims diretos)

### the agent's Discretion
- Critérios exatos para identificar um "tema" (quantos verbatims mínimos, similaridade semântica)
- Ordem dos verbatims dentro de um tema
- Nível de detalhe das notas de margem quali

</decisions>

<canonical_refs>
## Canonical References

### Fundação
- `SKILL.md` — Meta-prompt principal (405 linhas, 6 comandos implementados)
- `constitution.md` — Regras de rigor estatístico e qualitativo
- `agents/agent-anthropologist.md` — Agente Antropólogo (já criado)
- `agents/agent-critic.md` — Dimensões de auditoria quali
- `agents/agent-tufte-designer.md` — Regras de output

### Planejamento
- `.planning/ROADMAP.md` — Fase 3 goal e success criteria
- `.planning/REQUIREMENTS.md` — INJECT-01, MODE-02, ARCH-02
- `.planning/phases/01-constitution-setup/01-CONTEXT.md` — Decisões Fase 1
- `.planning/phases/02-quantitative-analysis/02-CONTEXT.md` — Decisões Fase 2
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `SKILL.md` § /dps-cross — Padrão de comando com loop de agentes, replicar para /dps-inject-open
- `agents/agent-anthropologist.md` — Já define: categorização temática, extração de verbatims, frequência, arquétipos, mapeamento de jornadas
- `agents/agent-critic.md` — Já define dimensões de auditoria quali (overgeneralization, N<30, etc.)
- `SKILL.md` § /dps-mode:quant — Padrão de toggle de persona, replicar para /dps-mode:quali

### Integration Points
- `/dps-inject-open` referencia segmentos do manifesto `/dps-setup` (document-driven)
- `/dps-mode:quali` modifica o loop de agentes (adiciona 4a etapa)
- Output quali aparece como subseção dentro de cada segmento quantitativo
</code_context>

<specifics>
## Specific Ideas

- `/dps-inject-open` deve validar que um `/dps-setup` foi executado antes (manifesto precisa existir para ter segmentos)
- Se não houver manifesto, erro: "Execute /dps-setup primeiro para definir os segmentos quantitativos"
- Verbatims devem ser literais (entre aspas), não parafraseados
- Temas devem ter no mínimo 2 verbatims para serem reportados (menos que isso = "menção isolada")
</specifics>

<deferred>
## Deferred Ideas

- Análise de sentimento automatizada — fase futura
- Nuvem de palavras/visualização de temas — fase 4
- Análise de jornada do consumidor — modo especializado futuro

</deferred>

---

*Phase: 03-qualitative-injection*
*Context gathered: 2026-05-25*
