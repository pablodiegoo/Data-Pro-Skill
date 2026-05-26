# Phase 4: Strategy, Export & Polish - Context

**Gathered:** 2026-05-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Fase final do Data-Pro-Skill v2 — adiciona camada estratégica, exportação e polish multi-harness ao SKILL.md (516 linhas, 8 comandos):

1. **`/dps-export`** — Consolida toda análise em MD único + opção de seções individuais
2. **`/dps-mode:strategy`** — Pós-processamento estratégico: recomendações de negócio
3. **HARN-03** — Validação multi-harness final

</domain>

<decisions>
## Implementation Decisions

### `/dps-export`
- **D-01:** Gera arquivo MD único consolidado: outputs/final_report.md
- **D-02:** YAML frontmatter com metadados do projeto + todas as seções em ordem cronológica
- **D-03:** Flags: `--manifest` (só /dps-setup), `--crosstabs` (só tabelas), `--full` (tudo incluso quali+estratégia)
- **D-04:** Sem flag = `--full` (comportamento padrão)
- **D-05:** Output pronto para Quarto/LaTeX/PDF

### `/dps-mode:strategy`
- **D-06:** Pós-processamento — após toda análise (quanti + quali), adiciona seção de recomendações
- **D-07:** Output estratégico inclui: key findings (3-5), matriz de priorização (impacto × esforço), plano de ação "segunda de manhã"
- **D-08:** NÃO adiciona 5a etapa ao loop — age como pós-processador, não durante a análise
- **D-09:** Agent-strategist.md já existe como referência

### Herdado
- Prefixo /dps-, zero XML, DPS naming, output Tufte
- SKILL.md: 516 linhas, 8 comandos, loop 4 etapas

</decisions>
