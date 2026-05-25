# Phase 1: Constitution & Setup — Discussion Log

**Date:** 2026-05-25

## Gray Areas Discussed

### 1. Formato do Manifesto `/dps-setup`
- **Question:** Quão detalhado deve ser o output do /setup?
- **Options:** YAML+tabela simples | +mapa de cruzamento | +hipóteses
- **Selected:** YAML + tabela (simples)
- **Note:** Manter foco — manifesto é âncora, não relatório completo

### 2. Regras do `constitution.md`
- **Question:** As regras planejadas são suficientes?
- **Options:** 5 core rules | +qualidade de dados | +inferência causal
- **Selected:** Adicionar regras de qualidade de dados
- **Note:** Total de 8 regras: 5 core + 3 qualidade de dados (straight-lining, % sum validation, missing data >10%)

### 3. Loop de Agentes Invisíveis
- **Question:** Como estruturar o loop de agentes?
- **Options:** Inline no SKILL.md | Arquivos separados + orquestrador
- **Selected:** Arquivos separados + orquestrador SKILL.md
- **Note:** Agentes já criados em agents/. SKILL.md referencia e orquestra

### 4. Nomenclatura GSD → DPS
- **Question:** Prefixo /dps nos comandos ou manter sem prefixo?
- **Options:** Sem prefixo | Com prefixo /dps
- **Selected:** Com prefixo /dps em tudo
- **Note:** Todos os comandos: /dps-setup, /dps-cross, /dps-inject-open, /dps-export, /dps-clarify, /dps-plan, /dps-mode:quant, /dps-mode:quali, /dps-mode:strategy

## Deferred Ideas
- Tradução do meta-prompt — fase futura
- Script de instalação automatizada — fase 4
- Templates Quarto/LaTeX — fase 4
- Logo e identidade visual DPS — fora do escopo

## the agent's Discretion
- Estrutura exata de parágrafos no constitution.md
- Organização das seções do SKILL.md
- Nomes de variáveis no YAML frontmatter do manifesto
