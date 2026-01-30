---
description: Workflow para definir e gerar regras de projeto (coding standards, arquitetura, workflow) adaptáveis a diferentes stacks
---

# Build Project Rules

Este workflow guia a criação de um conjunto robusto de regras para governar o desenvolvimento do projeto. O objetivo é popular o diretório `.agent/rules/` com diretrizes claras que a IA e os desenvolvedores devem seguir.

## Quando Usar
- Início de novos projetos.
- Refatoração de governança em projetos existentes.
- Definição de contexto para Agentes de IA.

## Pré-requisitos
- Acesso às skills: `coding-standards`, `architecture`, `testing`, `security`.
- Entendimento do Stack Tecnológico (definido em `PROJECT.md` ou detectado).

---

## Passo 1: Análise do Stack Tecnológico

Identifique as tecnologias principais do projeto para adaptar as regras.

1. **Linguagem Principal**: (ex: PHP, Python, Node.js)
2. **Frameworks**: (ex: Laravel, Django, Next.js)
3. **Estilo Arquitetural**: (ex: Monolito, Microservices, Event-Driven)

*Ação:* Se não estiver claro, analise o `composer.json`, `package.json` ou `requirements.txt`.

---

## Passo 2: Coding Standards (Padrões de Código)

Gere o arquivo `.agent/rules/coding-standards.md`.
Utilize a skill `coding-standards` como base.

**O que incluir:**
- **Nomenclatura**: Convenções para variáveis, classes, métodos, tabelas (ex: PascalCase vs snake_case).
- **Estrutura**: Organização de métodos (públicos antes de privados), tamanho máximo de classes/funções.
- **Boas Práticas**: Tipagem forte, Early Returns, tratamento de exceções.
- **Exemplos**: Blocos de código "✅ Do" e "❌ Don't".

---

## Passo 3: Padrões de Arquitetura

Gere o arquivo `.agent/rules/architecture.md`.
Utilize a skill `architecture` e `software-architecture`.

**O que incluir:**
- **Design Patterns**: Quais padrões são encorajados (ex: Repository, Service, Facade) e quais evitar.
- **Camadas**: Definição clara de responsabilidades (ex: Controllers só validam e chamam Services).
- **Fluxo de Dados**: Como os dados transitam entre Frontend e Backend ou entre módulos.
- **Decisões Estruturais**: Uso de DTOs, Value Objects, ou Models diretamento.

---

## Passo 4: Git e Workflow de Desenvolvimento

Gere o arquivo `.agent/rules/git-workflow.md`.
Utilize a skill `git-pushing` e `task-planning`.

**O que incluir:**
- **Commits**: Padrão Conventional Commits (`feat:`, `fix:`, `chore:`).
- **Branches**: Estratégia de branching (Main/Develop, Feature Branches).
- **Pull Requests**: Checklist para Code Review (link para skill `code-review`).

---

## Passo 5: Qualidade e Testes

Gere o arquivo `.agent/rules/quality-assurance.md`.
Utilize a skill `testing` e `security`.

**O que incluir:**
- **Testing**: Stack de testes (Pest, PHPUnit, Jest).
- **Cobertura**: Expectativas de cobertura de código.
- **Segurança**: Validação de inputs, sanitização, práticas de auth (OWASP).
- **Linting**: Ferramentas de análise estática obrigatórias (Pint, ESLint).

---

## Passo 6: Criação dos Arquivos

Execute a criação dos arquivos na pasta `.agent/rules/`.

```bash
mkdir -p .agent/rules
touch .agent/rules/coding-standards.md
touch .agent/rules/architecture.md
touch .agent/rules/git-workflow.md
touch .agent/rules/quality-assurance.md
```

Preencha cada arquivo com o conteúdo gerado nos passos anteriores.

---

## Passo 7: Validação

Verifique se as regras geradas não conflitam entre si e se cobrem os aspectos críticos do projeto.
Adicione uma referência a essas regras no `PROJECT.md` ou no prompt de sistema do Agente, se possível.

**Resultado Esperado:**
Uma pasta `.agent/rules/` populada servindo como "Tribunal" para decisões de código futuras.
