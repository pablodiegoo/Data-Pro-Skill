---
description: Estudo profundo de documentos externos para extrair insights, validar aplicabilidade e propor melhorias para o projeto
---

# 📚 Document Study Workflow

Este workflow combina as melhores skills do agente para fazer análise profunda de documentos, extrair insights acionáveis e propor melhorias para o Aporia.

## Quando Usar

- Analisando papers acadêmicos, artigos técnicos ou documentação externa
- Estudando features de concorrentes
- Revisando RFCs, especificações ou standards
- Avaliando bibliotecas ou frameworks novos
- Extraindo conhecimento de PDFs, posts ou tutoriais

## Fases do Workflow

---

### Fase 1: Preparação e Leitura

**Objetivo**: Compreender o documento completamente antes de qualquer análise.

1. **Carregar o documento**
   - Se for URL, usar `read_url_content`
   - Se for arquivo local, usar `view_file`
   - Se for PDF, converter para texto primeiro

2. **Leitura exploratória**
   - Ler títulos e subtítulos
   - Identificar estrutura geral
   - Notar seções mais relevantes para o projeto

3. **Criar sumário de leitura**
   - Documentar em `docs/studies/YYYY-MM-DD-<nome-do-doc>.md`
   - Incluir: título, fonte, data, resumo de 3-5 linhas

---

### Fase 2: Extração de Conhecimento

**Objetivo**: Mapear todo conhecimento útil do documento.

// turbo
4. **Extrair conceitos-chave**
   - Listar termos técnicos novos
   - Identificar patterns ou frameworks mencionados
   - Mapear arquiteturas ou fluxos descritos

5. **Identificar claims e evidências**
   - Quais afirmações o documento faz?
   - Que dados ou testes suportam essas afirmações?
   - Há referências que vale a pena seguir?

6. **Mapear tecnologias e ferramentas**
   - Quais tecnologias são mencionadas?
   - Há bibliotecas específicas recomendadas?
   - Quais versões ou configurações?

---

### Fase 3: Análise de Aplicabilidade

**Objetivo**: Validar o que é aplicável ao contexto do Aporia.

7. **Comparar com stack atual**
   - Consultar `.agent/memory` para context
   - Verificar compatibilidade com a stack do projeto
   - Identificar conflitos ou incompatibilidades

8. **Avaliar esforço vs benefício**
   Usar framework RICE da skill `product-manager-toolkit`:
   - **Reach**: Quantos usuários/features seriam impactados?
   - **Impact**: massive/high/medium/low/minimal
   - **Confidence**: Quão seguros estamos da avaliação?
   - **Effort**: Estimativa de implementação

9. **Classificar insights por tipo**
   ```markdown
   ## ✅ Direto Aplicável (Quick Wins)
   - [insight que pode ser implementado facilmente]
   
   ## 🔄 Requer Adaptação
   - [insight que precisa ser modificado pro contexto]
   
   ## 🔮 Inspiração Futura
   - [ideias para versões futuras]
   
   ## ❌ Não Aplicável
   - [por que não se aplica ao Aporia]
   ```

---

### Fase 4: Geração de Insights

**Objetivo**: Transformar conhecimento em ações concretas.

10. **Brainstorming de features**
    Usando metodologia da skill `brainstorming`:
    - Para cada insight aplicável, propor 2-3 abordagens
    - Incluir trade-offs de cada abordagem
    - Recomendar uma opção com justificativa

11. **Propor melhorias técnicas**
    - Otimizações de performance
    - Padrões de código melhores
    - Arquiteturas mais escaláveis
    - Práticas de segurança

12. **Mapear para roadmap**
    Categorizar por horizonte temporal:
    ```markdown
    ## 🎯 Curto Prazo (Próximo Sprint)
    - [ ] [melhoria específica]
    
    ## 📅 Médio Prazo (1-2 meses)
    - [ ] [feature inspirada]
    
    ## 🚀 Longo Prazo (3+ meses)
    - [ ] [mudança arquitetural]
    ```

---

### Fase 5: Documentação e Integração

**Objetivo**: Preservar conhecimento e integrar com o projeto.

13. **Criar artefato de estudo**
    Formato do arquivo `docs/studies/YYYY-MM-DD-<nome>.md`:
    ```markdown
    # Estudo: [Nome do Documento]
    
    **Fonte**: [URL ou referência]
    **Data**: [data do estudo]
    **Relevância**: ⭐⭐⭐⭐☆
    
    ## Resumo Executivo
    [3-5 linhas sobre o documento]
    
    ## Insights Principais
    [lista dos insights mais importantes]
    
    ## Aplicabilidade ao Aporia
    [análise de como se aplica]
    
    ## Ações Propostas
    [checkboxes com tarefas concretas]
    
    ## Referências Adicionais
    [links para aprofundamento]
    ```

// turbo
14. **Atualizar documentação do projeto**
    Conforme o tipo de insight:
    - **Novos padrões**: Atualizar skills ou memory
    - **Novas features**: Adicionar em `.agent/tasks/backlog.md`
    - **Referências úteis**: Adicionar em `.agent/references/`

15. **Notificar usuário**
    Apresentar resumo com:
    - Top 3 insights mais valiosos
    - Ações recomendadas com prioridade
    - Perguntas para validação

---

## Template de Output

```markdown
# 📊 Análise: [Nome do Documento]

## 🎯 TL;DR (3 bullets)
- [Principal descoberta]
- [Maior oportunidade]
- [Ação mais urgente]

## 📈 Insights por Categoria

### Performance & Otimização
- [insights técnicos]

### UX & Design
- [insights de experiência]

### Arquitetura
- [insights de estrutura]

### Segurança
- [insights de segurança]

## ✅ Plano de Ação

### Implementar Agora
1. [ ] [tarefa específica] - **Impacto**: Alto, **Esforço**: Baixo

### Avaliar com Equipe
1. [ ] [item que precisa discussão]

### Backlog Futuro
1. [ ] [item para versões futuras]

## 🔗 Próximos Passos
- [ ] Validar insights com stakeholders
- [ ] Criar issues para tarefas aprovadas
- [ ] Agendar POC se necessário
```

---

## Skills Utilizadas

| Skill | Uso no Workflow |
|-------|-----------------|
| `brainstorming` | Fase 4 - Exploração de abordagens |
| `product-manager-toolkit` | Fase 3 - Framework RICE |
| `context-optimizer` | Fase 5 - Organização em .agent |
| `documentation-mastery` | Fase 5 - Formatação do artefato |
| `clean-code` | Fase 4 - Avaliar melhorias técnicas |

---

## Dicas de Uso

> [!TIP]
> Para documentos muito longos, peça ao agente para fazer a análise em chunks, focando em uma seção por vez.

> [!IMPORTANT]
> Sempre valide os insights extraídos antes de implementar - o documento pode ter contexto diferente do Aporia.

> [!NOTE]
> Use `/document-study` seguido do path ou URL do documento para iniciar o workflow.