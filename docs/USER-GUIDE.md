# Guia do Usuário — Data-Pro-Skill v2

## Instalação

Data-Pro-Skill v2 é um meta-prompt — não requer instalação de software.

1. Copie `SKILL.md` para o diretório de skills do seu harness:
   - **OpenCode:** `~/.config/opencode/skills/data-pro-skill/SKILL.md`
   - **Gemini CLI:** `~/.gemini/skills/data-pro-skill/SKILL.md`
   - **Codex CLI:** `~/.codex/skills/data-pro-skill/SKILL.md`
   - **Claude Code:** `~/.claude/skills/data-pro-skill/SKILL.md`

2. Copie `constitution.md` para o mesmo diretório.

3. Reinicie o harness.

## Uso Básico

### 1. Iniciar um Projeto de Análise

```
/setup

Aqui estão meus dados de pesquisa:
[cole sumário de frequências, CSV, ou descreva a estrutura]
```

O sistema gera um manifesto quantitativo que serve como âncora para toda análise posterior.

### 2. Cruzar Variáveis

```
/cross Faixa_Etaria x Satisfacao
```

Gera tabelas densas com N, %, insights e notas de margem.

### 3. Adicionar Dados Qualitativos

```
/inject-open respostas_abertas.csv
```

As respostas são automaticamente categorizadas dentro dos segmentos do manifesto.

### 4. Exportar

```
/export
```

Consolida tudo em `outputs/final_report.md`, pronto para converter em PDF.

## Exemplo Completo

```
> /setup
> Tenho uma pesquisa de satisfação com 500 respondentes.
> Variáveis: idade, região, satisfação (1-5), NPS, e 3 perguntas abertas.

[Manifesto gerado com segmentos]

> /cross Idade x Satisfacao

[Tabela Tufte com distribuição por faixa etária]

> /cross Regiao x NPS

[Tabela Tufte com NPS por região]

> /inject-open perguntas_abertas.csv

[Verbatims categorizados por segmento]

> /export

[Relatório final consolidado]
```

## Modos

- `/mode:quant` — Para análise puramente quantitativa
- `/mode:quali` — Para análise qualitativa aprofundada
- `/mode:strategy` — Para recomendações de negócio

## Recomendações

1. **Sempre comece com `/setup`** — sem o manifesto, a IA não tem âncora de contexto
2. **Não cole todos os dados de uma vez** — divida em etapas lógicas
3. **Use `/clarify` antes de análises complexas** — ajuda a IA a entender seus objetivos
4. **Verifique as notas de margem** — elas contêm os insights interpretativos

## Troubleshooting

**A IA está gerando análises genéricas?**
- Verifique se o `/setup` foi executado primeiro
- Os dados foram fornecidos em formato estruturado?

**As tabelas não incluem N?**
- O `constitution.md` exige N em todas as tabelas
- Verifique se o arquivo está presente no diretório de skills

**A análise qualitativa está separada da quantitativa?**
- Isso viola as regras do sistema
- Execute `/inject-open` novamente especificando o segmento alvo

---
*Para referência completa de comandos, veja [COMMANDS.md](COMMANDS.md).*
