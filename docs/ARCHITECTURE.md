# Data-Pro-Skill v2 — Arquitetura

> Para usuários, veja o [Guia do Usuário](USER-GUIDE.md). Para contribuidores, veja [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## Visão Geral

Data-Pro-Skill v2 é um **meta-prompt document-driven** para análise de dados de pesquisa de mercado. O usuário fornece dados brutos (quantitativos e qualitativos) através de comandos estruturados, e o sistema produz documentos analíticos densos no estilo Tufte.

## Princípios de Design

1. **Document-driven context:** Cada comando ancora contexto para o próximo. O manifesto do `/setup` é a fonte única da verdade.
2. **Agentes invisíveis:** O usuário nunca interage com agentes internos — vê apenas o output final.
3. **Quant-first:** Pipeline quantitativo como espinha dorsal; qualitativo como extensão.
4. **Multi-harness:** Zero dependências de plataforma — apenas YAML + Markdown.
5. **Tufte output:** Máxima densidade de dados, zero prosa fluff.

## Arquitetura de Agentes

### Loop de Agentes Invisíveis

```
Usuário → [Orquestrador] → [Estatístico] → [Crítico] → [Designer Tufte] → Output
```

Três agentes rodam em silêncio a cada comando:

| Agente | Arquivo | Função |
|--------|---------|--------|
| **Estatístico** | `agents/agent-statistician.md` | Valida números, calcula distribuições, escolhe testes |
| **Crítico** | `agents/agent-critic.md` | Detecta vieses, correlações espúrias, generalizações |
| **Designer Tufte** | `agents/agent-tufte-designer.md` | Formata output — zero fluff, tabelas densas, notas de margem |

### Agentes Especializados (por modo)

| Agente | Ativado por | Função |
|--------|-------------|--------|
| **Antropólogo** | `/mode:quali` ou `/inject-open` | Análise temática, verabatims, arquétipos |
| **Estrategista** | `/mode:strategy` | Recomendações de negócio, matriz de priorização |

## Pipeline de Comandos

### Fluxo Principal

```
/setup  →  outputs/00_project_manifest.md        (manifesto quantitativo)
  ↓
/cross  →  outputs/01_crosstab_X_x_Y.md          (tabelas Tufte)
  ↓
/cross  →  outputs/02_crosstab_A_x_B.md          (mais tabelas)
  ↓
/inject-open → enriquece segmentos existentes     (dados qualitativos)
  ↓
/export →  outputs/final_report.md                (consolidado)
```

### Document-Driven Context

O manifesto do `/setup` é a âncora. Toda análise subsequente:
1. Lê o manifesto para contexto
2. Produz output que referencia segmentos do manifesto
3. Não pode contradizer métricas estabelecidas

Isso resolve o "context rot" — a IA sempre tem um documento de referência estável.

## Estrutura do Projeto

```
/
├── SKILL.md                   # Meta-prompt principal (a ser criado)
├── constitution.md            # Regras de rigor estatístico
├── AGENTS.md                  # Instruções para a IA
├── README.md                  # Documentação principal
├── CONTEXT.md                 # Contexto e decisões do projeto
│
├── agents/                    # Definições dos agentes
│   ├── agent-statistician.md
│   ├── agent-critic.md
│   ├── agent-tufte-designer.md
│   ├── agent-anthropologist.md
│   └── agent-strategist.md
│
├── commands/gsd/              # Comandos de workflow GSD
├── get-shit-done/             # Engine GSD (workflows, templates)
├── docs/                      # Documentação
├── hooks/                     # Hooks de validação
├── assets/                    # Imagens e ícones
│
├── .planning/                 # Planejamento do projeto
│   ├── PROJECT.md
│   ├── REQUIREMENTS.md
│   ├── ROADMAP.md
│   └── STATE.md
│
└── .deprecated/v1/            # Código antigo preservado
```

## Formato de Output (Tufte)

Todo output analítico segue regras estritas:

### Tabelas
- Incluem coluna N (tamanho da amostra)
- Conclusão/insight no cabeçalho
- Autoexplicativas sem texto ao redor

### Notas de Margem
- Blockquotes (`>`) após dados
- Interpretação, não repetição
- 1-3 frases no máximo

### Prosa Fluff — PROIBIDO
- "É importante notar que..."
- "Com base nos dados fornecidos..."
- "Interessantemente..."
- Qualquer frase que possa ser deletada sem perder informação

## Compatibilidade Multi-Harness

O formato YAML frontmatter + Markdown puro funciona em todos os harnesses alvo:

| Harness | Compatibilidade |
|---------|:--------------:|
| OpenCode | ✓ |
| Gemini CLI | ✓ |
| Codex CLI | ✓ |
| Claude Code | ✓ |
| Hermes (open-source) | ✓ |
| OpenClaw | ✓ |

Nunca usar: tags XML, sintaxe específica de plataforma, emojis em output analítico.

---

*Baseado no engine GSD (`get-shit-done-redux`). Ver [get-shit-done/](../get-shit-done/) para detalhes do sistema de workflows.*
