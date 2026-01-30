---
description: Workflow orquestrador para construção completa do contexto do projeto
---

# Project Context Orchestrator

Workflow principal que orquestra a criação de todo o contexto do projeto, delegando para workflows especializados.

## Quando Usar
- Setup inicial de projeto ("Day 1").
- Rebuild completo do contexto.

---

## Passo 1: Detectar e Preparar Entrada

### Se existe documento extenso (PRD/Blueprint):
Use a skill `context-optimizer` para quebrar o documento inicial em partes menores:
```bash
python3 .agent/skills/context-optimizer/scripts/decompose.py documento.md -o .agent/temp_split -l 2
```

### Se não existe documento:
Prossiga, os workflows individuais irão solicitar inputs via `brainstorming`.

---

## Passo 2: Contexto Básico

// turbo
Execute o workflow de fundamentos:
- Leia/Execute `.agent/workflows/build-context-basics.md`
- **Saída**: `PROJECT.md`, `ROADMAP.md`

---

## Passo 3: Arquitetura Técnica

// turbo
Execute o workflow de arquitetura:
- Leia/Execute `.agent/workflows/build-context-architecture.md`
- **Saída**: `ARCHITECTURE.md`

---

## Passo 4: Banco de Dados

// turbo
Execute o workflow de dados:
- Leia/Execute `.agent/workflows/build-context-database.md`
- **Saída**: `DATABASE.md`

---

## Passo 5: Design System

// turbo
Execute o workflow de design:
- Leia/Execute `.agent/workflows/build-context-design.md`
- **Saída**: `DESIGN_SYSTEM.md`

---

## Passo 6: Regras e Governança

// turbo
Execute o workflow de regras:
- Leia/Execute `.agent/workflows/build-project-rules.md`
- **Saída**: Diretório `.agent/rules/` populado

---

## Passo 7: Instalação de Skills e Recursos

// turbo
Execute o setup de recursos:
- Leia/Execute `.agent/workflows/setup-agent-resources.md`
- **Saída**: Pasta `.agent/skills` e `.agent/workflows` populadas com ferramentas operacionais.

---

## Passo 8: Otimização Final e Limpeza

Use `context-optimizer` para garantir que o contexto gerado esteja otimizado para a janela de contexto da IA.

- [ ] Arquivos em `.agent/context/` < 500 linhas (quebre se necessário).
- [ ] Remover diretórios temporários (`.agent/temp_split`).
- [ ] Verificar integridade dos links entre arquivos.

## Estrutura Final Esperada

```
.agent/
├── context/       (Gerado pelos passos 2-5)
├── rules/         (Gerado pelo passo 6)
├── skills/        (Populada pelo passo 7)
├── workflows/     (Populada pelo passo 7+Originais)
└── tasks/
```
