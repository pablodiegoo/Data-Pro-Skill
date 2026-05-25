<div align="center">

# Data-Pro-Skill v2

**Português** · [English](README.en.md) (em breve)

**Meta-prompt para análise de dados de pesquisa de mercado. Transforma dados brutos quantitativos e qualitativos em documentos analíticos densos, estilo Tufte — zero prosa fluff, densidade máxima de dados.**

**Funciona em qualquer harness: OpenCode, Gemini, Codex, Hermes, OpenClaw, Claude.**

<br>

```bash
# Copie o SKILL.md para o diretório de skills do seu harness
cp SKILL.md ~/.config/opencode/skills/data-pro-skill/
```

<br>

*"Análises que antes tomavam horas de ajuste manual agora saem prontas para publicar."*

*"Finalmente um prompt que não se perde no meio do caminho."*

</div>

---

## Pipeline de Comandos

Quatro comandos. Cada um ancora o próximo. Nenhuma análise pode contradizer métricas já estabelecidas.

| Comando | O que faz |
|---------|-----------|
| `/setup` | Gera o manifesto quantitativo (YAML frontmatter + matriz de segmentos) |
| `/cross [VarX] x [VarY]` | Cruza variáveis com tabelas densas estilo Tufte |
| `/inject-open [texto]` | Categoriza respostas abertas dentro dos segmentos existentes |
| `/export` | Consolida tudo em Markdown limpo, pronto para Quarto/LaTeX/PDF |

### Modos especializados

| Comando | Persona ativada |
|---------|----------------|
| `/mode:quant` | Estatístico Sênior — correlações, tabelas cruzadas, NPS, Churn, CSAT |
| `/mode:quali` | Antropólogo — dores latentes, sentimento, arquétipos, jornadas |
| `/mode:strategy` | Diretor de BI — recomendações de negócio acionáveis |

---

## Exemplo de Output (Estilo Tufte)

```markdown
---
project: "Pesquisa de Churn — Q2 2026"
sample_size: 1450
metrics: [NPS, Frequência, Idade, Motivo]
---

## Distribuição de Churn por Faixa Etária

O pico de cancelamentos está em 18-24 anos (45% do Churn total, apenas 20% da base).

| Faixa Etária | N  | Churn (%) | Alvo Qualitativo |
| :---         |:--:| :--:      | :---             |
| 18-24        | 290 | 45%       | Barreira de Preço / Valor Percebido |
| 25-34        | 580 | 12%       | Falta de Tempo / Mudança de Rotina  |
| 35+          | 580 | 5%        | Problemas Técnicos de Usabilidade   |

> **Nota de Margem:** Análise quali do Segmento A revela correlação entre rejeição e preço
> pós-trial. Termos recorrentes: "caro", "estudante", "reajuste".
```

---

## Arquitetura

### Loop de Agentes Invisíveis

O usuário interage apenas com o output final. Três agentes internos rodam em silêncio:

```
Usuário → [Orquestrador] → [Estatístico] → [Crítico] → [Designer Tufte]
                                                              ↓
                                                       Output ao usuário
```

| Agente | Responsabilidade |
|--------|-----------------|
| **Estatístico** | Valida consistência numérica, calcula distribuições, escolhe testes |
| **Crítico** | Detecta vieses, correlações espúrias, generalizações indevidas |
| **Designer Tufte** | Sintetiza eliminando adjetivos, foco em densidade de dados e notas de margem |

### Document-Driven Context

Cada comando escreve em um documento compartilhado. O manifesto do `/setup` é a verdade única — nenhuma análise posterior pode contradizer métricas já estabelecidas. Isso elimina o "context rot" (degradação de qualidade conforme a IA preenche a janela de contexto).

---

## Constituição dos Dados

Regras inegociáveis definidas em `constitution.md`:

- **Rigor Estatístico:** Margem de erro, tamanho amostral mínimo, nível de confiança (p < 0.05)
- **Rigor Qualitativo:** Proibição de generalizações com amostras pequenas (ex: "70% dos entrevistados" com N=10)
- **Tratamento de Viés:** Identificação de viés de confirmação, correlações espúrias
- **Prosa Fluff:** Proibição de frases como "É importante notar que..." ou "Com base nos dados..."

---

## Compatibilidade Multi-Harness

Projetado para funcionar em qualquer runtime de IA — sem depender de features exclusivas de um plataforma:

| Harness | Status | Notas |
|---------|--------|-------|
| **OpenCode** | ✓ | Público-alvo principal |
| **Gemini CLI** | ✓ | YAML frontmatter + Markdown |
| **Codex CLI** | ✓ | Testado |
| **Claude Code** | ✓ | Sem tags XML |
| **Hermes** | ✓ | Modelos open-source |
| **OpenClaw** | ✓ | Compatível |

Nada de XML, nada de sintaxe proprietária. Apenas YAML frontmatter e Markdown.

---

## Estrutura do Projeto

```
├── SKILL.md              # Meta-prompt principal
├── constitution.md        # Regras de rigor estatístico/qualitativo
├── agents/                # Definições dos agentes GSD
├── commands/              # Comandos (setup, cross, inject-open, export)
├── docs/                  # Documentação expandida
├── get-shit-done/         # Engine GSD (workflows, templates, referências)
├── hooks/                 # Hooks de validação
├── assets/                # Ícones e imagens
└── .planning/             # Planejamento do projeto (ROADMAP, STATE, etc.)
```

---

## Inspiração

Construído combinando o melhor de três mundos:

| Framework | Contribuição para Data-Pro-Skill |
|-----------|----------------------------------|
| **Tufte** (Edward Tufte) | Output com alta densidade de dados, notas de margem, zero fluff |
| **GSD** (Get Shit Done) | Agentes invisíveis, loop Discutir→Planejar→Executar→Verificar |
| **Spec-Kit** (GitHub) | Comando `/clarify` — questionar hipóteses antes de tocar nos dados |
| **BMAD** | Separação de personas (`/mode:quant`, `/mode:quali`) |

---

## Licença

MIT License. Veja [LICENSE](LICENSE).

---

<div align="center">

**Dados brutos entram. Documentos analíticos publicáveis saem. Sem enrolação.**

</div>
