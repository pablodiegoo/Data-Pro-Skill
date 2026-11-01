# Data-Pro-Skill v2.0 — Arquitetura do Sistema

> Para instruções passo a passo de uso, veja o [Guia do Usuário](USER-GUIDE.md) e a referência de [Comandos](COMMANDS.md).

---

## 1. Princípios de Design (Inspiração Matt Pocock + 5 Escolas de Design de Dados)

1. **Pit of Success (Fluxo Ordenado):** Os comandos `/dps-grill` → `/dps-setup` → `/dps-plan` → `/dps-cross` / `/dps-execute` → `/dps-advanced` → `/dps-inject-open` → `/dps-export` possuem critérios de conclusão explícitos e ancoram artefatos persistentes em `.dps/outputs/`.
2. **Progressive Disclosure (Divulgação Progressiva em 3 Camadas):**
   - **Camada 1 (`SKILL.md`):** Roteamento de comandos e critérios de conclusão.
   - **Camada 2 (`GLOSSARY.md` & `constitution.md`):** Vocabulário canônico (*Leading Words*) e os 8 Artigos inegociáveis de rigor estatístico, qualitativo e visual.
   - **Camada 3 (`references/*.md` & `references/analysis/*.md`):** Protocolos profundos carregados sob demanda (Data Grilling, Seleção de Testes Estatísticos, Remoção de Efeito Halo, Matriz de Prioridade, Resíduos de Expectativa, Clusterização Dupla, PCA/Alfa de Cronbach, TURF, Raking e as 5 Escolas de Design).
3. **Deep Modules (`scripts/*.py`):** Scripts Python autossuficientes que expõem interfaces CLI simples e encapsulam toda a matemática estatística, testes de hipóteses, cálculo de tamanhos de efeito, geração de gráficos `<svg>` *school-aware* e compilação HTML/LaTeX.
4. **Arquitetura Multi-Escola de Design de Dados (`scripts/design_schools.py`, `references/design-schools.md`):** Suporte nativo a 5 paradigmas visuais e gráficos selecionáveis (`tufte`, `few`, `knaflic`, `swiss`, `editorial`), adaptando tanto as folhas de estilo CSS (`references/styles/*.css`) quanto a gramática geométrica dos gráficos vetoriais `<svg>` (`scripts/tufte_viz.py`), com seletor interativo em tempo real dentro de `final_report.html`.
5. **Motor Nativo de Tipografia Matemática LaTeX & Impressão para PDF (`scripts/tufte_html.py`):** `final_report.html` é o entregável primário autossuficiente (zero dependências externas/CDN), convertendo equações LaTeX inline (`$...$`) e de bloco (`$$...$$`) em tipografia matemática semântica harmonizada com a escola ativa e garantindo cabeçalhos e rodapés correntes em todas as páginas impressas (`@page` + `<table class="print-frame">`).

---

## 2. As 5 Escolas de Design de Dados (`Data Design Schools`)

| ID | Escola de Design | Paleta & Tipografia | Gramática Nativa `<svg>` (`tufte_viz.py`) | Arquitetura de Layout |
| :--- | :--- | :--- | :--- | :--- |
| **`tufte`** *(Padrão)* | **Edward Tufte** | Marfim (`#fffff8`), serifada `Palatino` | *Cleveland Dot Plots* com bigodes de IC 95% e zero linhas de grade | Coluna principal 58% + notas de margem flutuantes 36% (`<aside class="margin-note">`) e tabelas *booktabs* |
| **`few`** | **Stephen Few** | Alabastro frio (`#f8fafc`), `Inter` sans-serif | *Bullet Graphs* (faixas qualitativas de fundo + barra de medida + marcador de meta) | Grid perceptual de largura total, tabelas compactas de alta densidade e alertas diagnósticos inline |
| **`knaflic`** | **Cole Nussbaumer Knaflic** | Branco puro (`#ffffff`), `Plus Jakarta Sans` | Barras horizontais com contexto em cinza (`#cbd5e1`) e destaque pré-atentivo único (`#1e40af` / `#ea580c`) | Títulos de ação (*Action Titles*) e cartões executivos `💡 KEY TAKEAWAY` |
| **`swiss`** | **Swiss Grid & Jacques Bertin** | Pedra arquitetônica (`#f5f5f0`), `Helvetica Neue` + `JetBrains Mono` | *Bertin Retinal Lollipops* e matrizes reordenáveis em Vermelhão (`#e63946`) e Cobalto (`#1d3557`) | Grade modular preta exposta (`1.5px`/`4px`) e blocos numerados `INDEX // NOTE` |
| **`editorial`** | **The Economist / FT** | Papel jornal quente (`#fcf8f2`), `Georgia` + `Franklin Gothic` | *Editorial Lollipop Range Charts* com barra superior carmim (`#e3120b`) e rodapé `Source:` | Barra superior carmim de `6px`, hierarquia *Kicker + Headline + Standfirst* e sidebars `EDITORIAL BRIEF` |

---

## 3. Loop Invisível de 4 Agentes

```
Usuário → [Griller] → [Statistician] → [Methodological Critic] → [Tufte Designer] → Output Final
```

| Agente | Arquivo | Responsabilidade Central |
| :--- | :--- | :--- |
| **Griller** | `agents/agent-griller.md` | Reconhecimento silencioso de fatos no dataset, entrevista em Rodadas de Fronteira (`❓ Q#` + `➡️`), escolha da Escola de Design e modelagem de domínio (`column_mapping.json`, `00_data_glossary.md`). |
| **Statistician** | `agents/agent-statistician.md` | Executa scripts Python, pareia estimadores paramétricos (`Média/DP`) e não-paramétricos (`Mediana/IIQ`), calcula IC 95% (`±MoE%`), $p$-valores e tamanhos de efeito. |
| **Methodological Critic** | `agents/agent-critic.md` | Audita os Artigos 1–8 da `constitution.md` (Straight-Lining, proibição de `%` quando $N < 30$, sobreposição de pulo `0x0`, divulgação de *Null Findings* $p \ge 0.05$). |
| **Tufte Designer** | `agents/agent-tufte-designer.md` | Formata prosa *Answer-First*, tabelas *booktabs*, notas de margem numeradas (`§1`), gráficos `<svg>` na gramática da escola ativa, fórmulas matemáticas LaTeX nativas e compila `final_report.html`. |

### Agentes de Lente Especializada (`/dps-mode:*`)

| Agente | Arquivo | Ativado por | Foco |
| :--- | :--- | :--- | :--- |
| **Anthropologist** | `agents/agent-anthropologist.md` | `/dps-mode:quali`, `/dps-inject-open` | Taxonomia emergente, tensões culturais, verbatims literais e *Silence Notes*. |
| **Strategist** | `agents/agent-strategist.md` | `/dps-mode:strategy`, `/dps-advanced` | Quadrantes da Matriz de Prioridade, TURF e recomendações quantificadas (`Alvo + Ação + Impacto`). |

---

## 4. Fluxo de Artefatos Document-Driven (`.dps/outputs/`)

```
/dps-grill        → .dps/outputs/setup/clarify_notes.md + 00_data_glossary.md
  ↓
/dps-setup        → .dps/outputs/setup/00_profile.json + design_school.json + column_mapping.json + setup_report.md
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
