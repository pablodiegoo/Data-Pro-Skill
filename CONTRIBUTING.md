# Contribuindo — Data-Pro-Skill v2

Data-Pro-Skill v2 é um meta-prompt open-source para análise de dados de pesquisa de mercado. Contribuições são bem-vindas.

## Como Contribuir

1. **Fork** o repositório
2. **Crie uma branch** para sua feature: `git checkout -b feature/minha-ideia`
3. **Faça as alterações** seguindo as convenções do projeto
4. **Commit** com mensagens claras
5. **Abra um Pull Request**

## Convenções

### Formato de Documento
- YAML frontmatter + Markdown puro
- Sem tags XML
- Sem sintaxe específica de plataforma

### Estilo de Código
- Sem comentários desnecessários
- Sem emoji em output analítico
- Zero prosa fluff

### Regras Quantitativas
- Sempre incluir margem de erro
- p < 0.05 para significância
- Nunca generalizar de amostras qualitativas pequenas (N < 30)

### Regras Qualitativas
- Categorizar dentro de segmentos quantitativos existentes
- Sem seções standalone de qualitativo
- Citar verbatims diretamente

## Áreas para Contribuir

| Área | Descrição |
|------|-----------|
| **Agentes** | Melhorar ou adicionar agentes de análise |
| **Comandos** | Novos comandos de análise de dados |
| **Documentação** | Tutoriais, exemplos, traduções |
| **Testes** | Testar em diferentes harnesses |
| **constitution.md** | Refinar regras de rigor estatístico |

## Testando

Teste o meta-prompt nos harnesses alvo:
- OpenCode
- Gemini CLI
- Codex CLI
- Claude Code
- Hermes
- OpenClaw

Reporte problemas abrindo uma issue.

---

*Baseado no template de contribuição do GSD. Ver `.deprecated/v1/CONTRIBUTING.md` para o guia original.*
