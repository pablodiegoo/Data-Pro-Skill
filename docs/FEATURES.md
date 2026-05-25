# Funcionalidades — Data-Pro-Skill v2

## Pipeline Quantitativo (Fase 1-2)

| Funcionalidade | Comando | Status |
|---------------|---------|--------|
| Manifesto quantitativo com YAML frontmatter | `/setup` | Planejado |
| Matriz de segmentos com N, volumetria, métricas | `/setup` | Planejado |
| Tabelas densas estilo Tufte | `/cross` | Planejado |
| Testes estatísticos automáticos (χ², t-test, ANOVA) | `/cross` | Planejado |
| Margem de erro em todas as afirmações | `/setup`, `/cross` | Planejado |
| Perguntas de clarificação de negócio | `/clarify` | Planejado |
| Plano analítico antes da execução | `/plan` | Planejado |
| Execução do plano com output Tufte | `/execute` | Planejado |

## Injeção Qualitativa (Fase 3)

| Funcionalidade | Comando | Status |
|---------------|---------|--------|
| Categorização temática de respostas abertas | `/inject-open` | Planejado |
| Vinculação obrigatória a segmentos quantitativos | `/inject-open` | Planejado |
| Extração de verabatims com contexto de segmento | `/inject-open` | Planejado |
| Proteção contra generalizações (N<30) | `/inject-open` | Planejado |
| Identificação de arquétipos e jornadas | `/mode:quali` | Planejado |

## Modos Especializados

| Funcionalidade | Comando | Status |
|---------------|---------|--------|
| Persona estatístico sênior | `/mode:quant` | Planejado |
| Persona antropólogo | `/mode:quali` | Planejado |
| Persona diretor de BI | `/mode:strategy` | Planejado |

## Exportação

| Funcionalidade | Comando | Status |
|---------------|---------|--------|
| Consolidação em Markdown limpo | `/export` | Planejado |
| Pronto para Quarto/LaTeX/PDF | `/export` | Planejado |
| YAML frontmatter com metadados | `/export` | Planejado |

## Multi-Harness

| Funcionalidade | Status |
|---------------|--------|
| Compatível com OpenCode | Planejado |
| Compatível com Gemini CLI | Planejado |
| Compatível com Codex CLI | Planejado |
| Compatível com Claude Code | Planejado |
| Compatível com Hermes (open-source) | Planejado |
| Compatível com OpenClaw | Planejado |

## Rigor Estatístico (constitution.md)

| Regra | Status |
|-------|--------|
| Margem de erro obrigatória | Planejado |
| p < 0.05 para significância | Planejado |
| Proibição de % em amostras quali < 30 | Planejado |
| Detecção de viés de confirmação | Planejado |
| Proibição de prosa fluff | Planejado |

---
*Status: 100% planejado. Ver `.planning/ROADMAP.md` para cronograma de implementação.*
