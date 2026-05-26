# Data-Pro-Skill v2 — Contexto do Projeto

## Origem

O **Data-Pro-Skill v1** foi criado como um meta-prompt para análise de dados de pesquisa de mercado (quantitativa e qualitativa). O código Python organizava skills, scripts de análise estatística (crosstabs, PCA, clustering, causal inference), templates Quarto e um engine de geração de relatórios.

**Problema detectado:** O v1 era confuso e mal estruturado. A IA gerava análises genéricas e incompletas — mesmo em datasets simples. O excesso de arquivos Python, skills fragmentadas e falta de uma arquitetura rígida causavam "context rot": a IA se perdia, esquecia as regras e entregava resultados superficiais.

O código v1 completo está preservado em `.deprecated/v1/`.

## Decisão de Refatoração (Maio 2026)

Discussão com Gemini (documentada em `.deprecated/v1/coonversa.md`) convergiu em três decisões fundamentais:

### 1. Arquitetura Document-Driven

Em vez de scripts Python soltos, o meta-prompt agora é um **sistema document-driven**: cada comando ancora contexto para o próximo. O output do `/setup` é a "verdade única" — nenhuma análise posterior pode contradizer métricas já estabelecidas.

Isso resolve o problema de "context rot": a IA sempre tem um documento de referência para se ancorar.

### 2. Quantitativo Primeiro, Qualitativo Como Extensão

O pipeline quantitativo é a espinha dorsal. As perguntas abertas (quali) são injetadas **dentro** dos segmentos quantitativos existentes — nunca como análise standalone. Isso elimina os "loops de comandos semelhantes" entre quanti e quali.

### 3. Agentes Invisíveis (Estilo GSD)

O usuário interage apenas com o output final. Três agentes internos rodam em silêncio: Estatístico (valida números), Crítico (detecta vieses), Designer Tufte (formata o output). A saída do Designer é o que o usuário vê.

## Inspiração Híbrida

| Fonte | O que trouxe |
|-------|-------------|
| **Edward Tufte** | Alta densidade de dados, notas de margem, zero prosa fluff, tabelas autoexplicativas |
| **GSD (Get Shit Done)** | Agentes invisíveis, loop Discutir→Planejar→Executar→Verificar, contextos isolados |
| **Spec-Kit (GitHub)** | Comando `/clarify` — entrevista o usuário sobre hipóteses antes de tocar nos dados |
| **BMAD Method** | Separação de personas (`/mode:quant` vs `/mode:quali` vs `/mode:strategy`) |

## Blueprint Arquitetural (definida pelo Gemini)

```
1. Comando /setup → Gera o manifesto quantitativo (YAML + matriz de segmentos)
2. /cross [VarX] x [VarY] → Tabelas densas estilo Tufte com notas de margem
3. /inject-open [texto] → Categoriza respostas abertas dentro dos segmentos do /setup
4. /export → Consolida em Markdown limpo, pronto para Quarto/LaTeX/PDF
```

### Loop de Agentes

```
Usuário → [Orquestrador] → [Estatístico] → [Crítico] → [Designer Tufte] → Output
```

### Modos de Operação

- `/mode:quant` — Persona Estatístico Sênior
- `/mode:quali` — Persona Antropólogo
- `/mode:strategy` — Persona Diretor de BI

## Regras de Output (Estilo Tufte)

1. **Proibição de prosa fluff:** Nunca começar com "É importante notar que..." ou "Com base nos dados fornecidos..."
2. **Notas de margem:** Blockquotes (`>`) após tabelas e dados para insights interpretativos
3. **Tabelas autoexplicativas:** Toda tabela inclui N (amostra) e conclusão no cabeçalho
4. **Zero emoji em output analítico** (notas de margem podem usar indicadores sutis)

## Multi-Harness

Projetado para funcionar em qualquer harness de IA — sem depender de features exclusivas:
- OpenCode (público-alvo principal por ser gratuito)
- Gemini CLI
- Codex CLI
- Claude Code
- Hermes (modelos open-source)
- OpenClaw

**Regra:** Nada de tags XML. Apenas YAML frontmatter e Markdown puro.

## Estrutura do Projeto (Base: get-shit-done-redux)

O projeto usa o template `open-gsd/get-shit-done-redux` como base estrutural:
- `dps-engine/` — Engine GSD (workflows, templates, referências)
- `agents/` — Definições dos agentes (adaptados para análise de dados)
- `commands/` — Comandos GSD + comandos específicos de análise
- `docs/` — Documentação do projeto
- `.planning/` — Planejamento GSD (ROADMAP, STATE, REQUIREMENTS, PROJECT)

Partes removidas do template original: `tests/`, `scripts/` (JS/TS), `package.json`, CI/CD, changelogs técnicos.

## Próximos Passos (Roadmap)

Ver `.planning/ROADMAP.md` para o plano completo. Resumo:

1. **Fase 1:** Constitution & Setup — `constitution.md`, `/setup`, manifesto Tufte
2. **Fase 2:** Análise Quantitativa — `/clarify`, `/plan`, `/cross`, `/execute`
3. **Fase 3:** Injeção Qualitativa — `/inject-open`, `/mode:quali`
4. **Fase 4:** Estratégia & Export — `/mode:strategy`, `/export`, multi-harness

---
*Contexto definido: 2026-05-25*
*Baseado na conversa com Gemini em coonversa.md e nas decisões do GSD new-project*
