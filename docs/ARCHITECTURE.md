# Data-Pro-Skill v2.0 — Arquitetura do Sistema

> Para instruções passo a passo de uso, veja o [Guia do Usuário](USER-GUIDE.md) e a referência de [Comandos](COMMANDS.md).

---

## 1. Princípios de Design (Inspiração Matt Pocock + Edward Tufte)

1. **Pit of Success (Fluxo Ordenado):** Os comandos `/dps-grill` → `/dps-setup` → `/dps-plan` → `/dps-cross` / `/dps-execute` → `/dps-advanced` → `/dps-inject-open` → `/dps-export` possuem critérios de conclusão explícitos e ancoram artefatos persistentes em `.dps/outputs/`.
2. **Progressive Disclosure (Divulgação Progressiva em 3 Camadas):**
   - **Camada 1 (`SKILL.md`):** Roteamento de comandos e critérios de conclusão.
   - **Camada 2 (`GLOSSARY.md` & `constitution.md`):** Vocabulário canônico (*Leading Words*) e os 8 Artigos inegociáveis de rigor estatístico, qualitativo e visual.
   - **Camada 3 (`references/*.md` & `references/analysis/*.md`):** Protocolos profundos carregados sob demanda (Data Grilling, Seleção de Testes Estatísticos, Remoção de Efeito Halo, Matriz de Prioridade, Resíduos de Expectativa, Clusterização Dupla, PCA/Alfa de Cronbach, TURF, Raking).
3. **Deep Modules (`scripts/*.py`):** Scripts Python autossuficientes que expõem interfaces CLI simples e encapsulam toda a matemática estatística, testes de hipóteses, cálculo de tamanhos de efeito e compilação SVG/HTML.
4. **HTML Estilo Edward Tufte Pronto para Impressão em PDF:** `final_report.html` é o entregável primário, combinando tipografia clássica, notas de margem flutuantes (`<aside class="margin-note">`), tabelas *booktabs* sem grades verticais, gráficos vetoriais `<svg>` inline e cabeçalhos/rodapés correntes em todas as páginas impressas (`@page` + `<table class="print-frame">`).

---

## 2. Loop Invisível de 4 Agentes

```
Usuário → [Griller] → [Statistician] → [Methodological Critic] → [Tufte Designer] → Output Final
```

| Agente | Arquivo | Responsabilidade Central |
| :--- | :--- | :--- |
| **Griller** | `agents/agent-griller.md` | Reconhecimento silencioso de fatos no dataset, entrevista em Rodadas de Fronteira (`❓ Q#` + `➡️`) e modelagem de domínio (`column_mapping.json`, `00_data_glossary.md`). |
| **Statistician** | `agents/agent-statistician.md` | Executa scripts Python, pareia estimadores paramétricos (`Média/DP`) e não-paramétricos (`Mediana/IIQ`), calcula IC 95% (`±MoE%`), $p$-valores e tamanhos de efeito. |
| **Methodological Critic** | `agents/agent-critic.md` | Audita os Artigos 1–8 da `constitution.md` (Straight-Lining, proibição de `%` quando $N < 30$, sobreposição de pulo `0x0`, divulgação de *Null Findings* $p \ge 0.05$). |
| **Tufte Designer** | `agents/agent-tufte-designer.md` | Formata prosa *Answer-First*, tabelas *booktabs*, notas de margem numeradas (`§1`), gráficos `<svg>` e compila `final_report.html`. |

### Agentes de Lente Especializada (`/dps-mode:*`)

| Agente | Arquivo | Ativado por | Foco |
| :--- | :--- | :--- | :--- |
| **Anthropologist** | `agents/agent-anthropologist.md` | `/dps-mode:quali`, `/dps-inject-open` | Taxonomia emergente, tensões culturais, verbatims literais e *Silence Notes*. |
| **Strategist** | `agents/agent-strategist.md` | `/dps-mode:strategy`, `/dps-advanced` | Quadrantes da Matriz de Prioridade, TURF e recomendações quantificadas (`Alvo + Ação + Impacto`). |

---

## 3. Fluxo de Artefatos Document-Driven (`.dps/outputs/`)

```
/dps-grill        → .dps/outputs/setup/clarify_notes.md + 00_data_glossary.md
  ↓
/dps-setup        → .dps/outputs/setup/00_profile.json + column_mapping.json + setup_report.md
  ↓
/dps-plan         → .dps/outputs/setup/plan.md
  ↓
/dps-cross /      → .dps/outputs/cross/cross_{X}_{Y}_report.md + execute_leaderboard.json
/dps-execute
  ↓
/dps-advanced     → .dps/outputs/advanced/advanced_report.md + advanced_metrics.json
  ↓
/dps-inject-open  → .dps/outputs/quali/quali_report.md + quali_verbatims.json
  ↓
/dps-export       → .dps/outputs/export/final_report.html + final_report.md + verification_report.json
```
