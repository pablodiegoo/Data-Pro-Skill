<div align="center">

# Data-Pro-Skill v2.0

**An Autonomous Survey Science, Data Grilling & Multi-School Print-Ready HTML Reporting Skill for AI Agents.**

[![Version](https://img.shields.io/badge/version-2.0.0-0f172a.svg)](package.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-3776AB.svg)](scripts/)
[![Node.js >= 18](https://img.shields.io/badge/Node.js-%3E%3D18.0-339933.svg)](bin/install.js)
[![Design Schools](https://img.shields.io/badge/Design_Schools-Tufte_%7C_Few_%7C_Knaflic_%7C_Swiss_%7C_Editorial-800000.svg)](references/design-schools.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

Transforms raw survey and behavioral datasets (`.csv`, `.xlsx`, `.ods`, `.parquet`) into statistically verified, Answer-First **Print-Ready HTML reports** (`final_report.html`) across **5 selectable Data Design Schools**, featuring **school-aware `<svg>` chart grammars** and a **native zero-CDN LaTeX mathematical formula typography engine** — engineered to print directly to PDF with running headers and footers.

**Multi-Harness Compatible:** OpenCode · Gemini CLI · Antigravity CLI · Claude Code · Codex CLI · GitHub Copilot

[Quick Start](#quick-start--cli-usage) · [5 Data Design Schools](#5-selectable-data-design-schools--native-svg-grammars) · [Command Pipeline](#command-pipeline) · [8-Article Constitution](#the-8-article-data-constitution-constitutionmd) · [Documentation](docs/README.md) · [Contributing](CONTRIBUTING.md)

</div>

---

## Why Data-Pro-Skill?

Most AI data analysis fails in three ways:
1. **Blind execution without business context:** Running generic descriptive charts without knowing what decision the stakeholder needs to make.
2. **Statistical theater:** Reporting raw averages masked by respondent **Halo Effect** (`yea-saying`), ignoring sample sizes ($N$), omitting 95% confidence Margins of Error (`±MoE%`), or hallucinating percentages on tiny open-ended samples ($N < 30$).
3. **Chartjunk & broken PDF exports:** Bloated dashboards, unparsed `$...$` LaTeX strings, or fragile external LaTeX/Quarto/CDN toolchains instead of clean, self-contained HTML that prints cleanly to PDF from any browser.

**Data-Pro-Skill v2.0** solves all three by combining:
- **Matt Pocock Agent Architecture:** *Pit of Success* ordered workflow, *Progressive Disclosure* (`SKILL.md` → `GLOSSARY.md` → `constitution.md` → `references/analysis/*.md`), *Deep Module* Python scripts, and relentless **Data Grilling** (`/dps-grill`).
- **Deep Survey Science (`references/analysis/`):** Ipsative Centering & Regression Halo Removal, Derived Importance × Performance Priority Matrices, Expectation Residuals (*Disappointed / Aligned / Delighted*), Dual Correlation (Pearson $r$ vs. Spearman $\rho$), $\chi^2$ Standardized Residuals ($z_{ij}$), Silhouette-optimized K-Means Personas + DBSCAN Outlier isolation, Multi-Pass PCA/Factor Analysis + Cronbach's $\alpha$, TURF Reach Optimization, and Raking (IPF) sample weighting.
- **5 Selectable Data Design Schools with School-Aware `<svg>` Grammars (`scripts/design_schools.py`, `scripts/tufte_viz.py`):** Every school adapts not only CSS typography and layout, but also the underlying `<svg>` chart geometry and live theme switcher inside `final_report.html`.
- **Native LaTeX Mathematical Formula Engine (`scripts/tufte_html.py`):** Zero-dependency parser converting inline (`$...$`) and display (`$$...$$`) LaTeX equations ($\chi^2$, $\eta^2$, $\epsilon^2$, $\alpha$, $\rho$, $\bar{X}_i$, $\hat{Y}_i$, `\frac{a}{b}`, `\sqrt{x}`, Greek symbols, subscripts/superscripts) into semantic HTML/CSS math typography tailored to the active school — 100% offline and print-safe.
- **Print-Ready HTML Standard (`Article 8`):** Every report compiles into a single self-contained `final_report.html` with inline vector `<svg>` graphics and `@page` + `<table class="print-frame">` running headers and footers on every printed PDF page.

---

## 5 Selectable Data Design Schools & Native SVG Grammars

Pick your preferred school during `/dps-setup`, `/dps-grill`, `node bin/install.js`, or via `--school <id>` (and switch schools live in the browser inside `final_report.html`):

| ID | Data Design School | Canvas & Typography | Native `<svg>` Chart Grammar (`tufte_viz.py`) | Callout & Layout Architecture |
| :--- | :--- | :--- | :--- | :--- |
| **`tufte`** *(Default)* | **Edward Tufte** (*The Visual Display of Quantitative Information*) | Warm Ivory (`#fffff8`), `Palatino` serif + math italic numerals | **Cleveland Dot Plots** with thin 95% CI whiskers, direct data labels, zero gridlines | 58% body / 36% floating right `<aside class="margin-note">` sidenotes & `booktabs` tables |
| **`few`** | **Stephen Few** (*Information Dashboard Design*) | Cool Alabaster (`#f8fafc`), `Inter` humanist sans-serif | **Stephen Few Bullet Graphs** (3 qualitative background bands + bold measure bar + vertical target marker) | Full-width perceptual BI grid, compact dense tables, left-bordered diagnostic callouts |
| **`knaflic`** | **Cole Nussbaumer Knaflic** (*Storytelling with Data*) | Pure White (`#ffffff`), `Plus Jakarta Sans` / `Inter` | **Preattentive Highlight Bars** (context pushed to `#cbd5e1` grey; top driver/anomaly highlighted in focal `#1e40af` blue or `#ea580c` orange) | Action-Title `h2` banners & structured `💡 KEY TAKEAWAY` executive cards |
| **`swiss`** | **Swiss International Style & Jacques Bertin** (*Semiology of Graphics*) | Architectural Stone (`#f5f5f0`), `Helvetica Neue` + `JetBrains Mono` | **Bertin Retinal Lollipops & Reorderable Matrices** with crisp `1.5px` structural rules in Vermilion (`#e63946`) & Cobalt (`#1d3557`) | Exposed `1.5px`/`4px` black modular grid (`#0a0a0a`) & numbered `INDEX // NOTE` blocks |
| **`editorial`** | **The Economist / FT Editorial** (*Financial Journalism*) | Warm Newsprint (`#fcf8f2` / FT Salmon tint), `Georgia` + `Franklin Gothic` | **Editorial Lollipop Range Charts** with top-left crimson accent bar (`#e3120b`), light horizontal reference ticks, and bottom `Source:` footlines | Signature `6px` crimson top bar, **Kicker + Headline + Standfirst** hierarchy & `EDITORIAL BRIEF` sidebars |

### Native LaTeX Mathematical Formula Typography (`scripts/tufte_html.py`)

No external MathJax or KaTeX CDN scripts are required. `scripts/tufte_html.py` includes a built-in LaTeX mathematical formula lexer and renderer:
- **Display Equations (`$$...$$`):** Rendered as `.math-block` containers styled to match the active **Data Design School** (e.g., indented serif block in `tufte`, slate callout bar in `few`, exposed brutalist border box in `swiss`, crimson-accented editorial block in `editorial`).
- **Inline Formulas (`$...$`):** Rendered as `.math-inline` with proper italic math variables (`<var class="math-var">`), upright functions (`\min`, `\max`, `\log`), stacked vertical fractions (`.math-frac`), radicals (`\sqrt{...}`), nested subscripts/superscripts, and full Greek/statistical operator support ($\chi^2$, $\eta^2$, $\epsilon^2$, $\alpha$, $\rho$, $\bar{X}_i$, $\hat{Y}_i$, $\pm\text{MoE}\%$).
- **Currency Guard:** Automatically distinguishes currency ranges (`$50–$100`) from mathematical expressions so financial figures are never misparsed as equations.

---

## Command Pipeline

Each command writes durable artifacts to `.dps/outputs/` that anchor the next stage, eliminating context rot:

| Step | Command | Purpose & Primary Output |
| :--- | :--- | :--- |
| **Step 0** | `/dps-grill` *(alias `/dps-clarify`)* | **Silent Fact Reconnaissance** on the dataset followed by **Frontier Rounds** (`❓ Q#` + `➡️ Recommended Default`) across a 5-branch Design Tree + live domain glossary (`00_data_glossary.md`). |
| **Step 1** | `/dps-setup` | Locks the **Data Design School** (`design_school.json`), generates `column_mapping.json` (`snake_case` schema), `00_profile.json`, `setup_manifest.json`, and runs **Article 6 Quality Gates** (Straight-Lining detection, `%` sum check, missingness audit). |
| **Step 2** | `/dps-plan` | Applies Dr. Samira Hosseini's **Statistical Test Selector** and the 88 `reasoning_rules.csv` triggers to lock the `Analysis Plan` (`plan.md`). |
| **Step 3** | `/dps-cross [VarX] x [VarY]` | Runs targeted cross-tabulations with **Branching Overlap** validation (`0x0` skip-logic guard), $\chi^2$ / Fisher's Exact / Welch's $t$ / ANOVA / Kruskal-Wallis, **Standardized Residuals ($z_{ij}$)**, and 95% CI `±MoE%`. |
| **Step 4** | `/dps-execute` | Autonomously executes all planned cross-tabulations and synthesizes an **Effect-Size Leaderboard** (`Cramér's V`, `Cohen's d`, $\eta^2$, $|r|$). |
| **Step 5** | `/dps-advanced` | Executes the 6 deep survey science modules: **Pure Sentiment Stack** (Ipsative + Halo Removal), **Priority Matrix**, **Expectation Residuals**, **Dual Correlation**, **K-Means + DBSCAN Clustering**, **PCA/FA + Cronbach's $\alpha$**, and **TURF**. |
| **Step 6** | `/dps-inject-open` | Categorizes open-ended verbatims into emergent themes mapped to quantitative segments under **Article 4** ($N < 30$ raw counts `"4 of 19"` only, $\ge 2$ literal quotes per theme, and **Silence Notes**). |
| **Step 7** | `/dps-export` | Consolidates all findings into `final_report.md`, runs the 8-Article Constitutional Audit (`verification_report.json`), generates school-aware `<svg>` charts (`tufte_viz.py`), and compiles the self-contained **Print-Ready HTML** (`final_report.html`) with native LaTeX math typography (`tufte_html.py`). |

### Specialized Analytical Lenses

| Mode Command | Active Persona | Primary Focus |
| :--- | :--- | :--- |
| `/dps-mode:quant` | **Senior Statistician** | Hypothesis testing, effect sizes, psychometrics, Halo removal, and residual diagnostics |
| `/dps-mode:quali` | **Corporate Anthropologist** | Cultural tensions, cognitive friction, literal verbatims, and segment Silence Notes |
| `/dps-mode:strategy` | **BI Strategy Director** | Priority Matrix quadrants, TURF bundles, and quantified `Target + Action + Impact Range` decisions |

---

## Invisible 4-Agent Verification Loop

Every command runs silently through an internal verification pipeline before emitting output to the user:

```
User Request → [Griller] → [Statistician] → [Methodological Critic] → [Tufte Designer] → Output
```

| Agent | Definition File | Core Responsibility |
| :--- | :--- | :--- |
| **Griller** | [`agents/agent-griller.md`](agents/agent-griller.md) | Silent data reconnaissance, 5-branch Design Tree interrogation, inline domain modeling ([`GLOSSARY.md`](GLOSSARY.md)) |
| **Statistician** | [`agents/agent-statistician.md`](agents/agent-statistician.md) | Executes Python scripts, pairs parametric (`Mean/SD`) + non-parametric (`Median/IQR`) metrics, computes 95% CI `±MoE%`, $p$-values, and effect sizes |
| **Critic** | [`agents/agent-critic.md`](agents/agent-critic.md) | Enforces Articles 1–8 of [`constitution.md`](constitution.md) (Straight-Lining, $N < 30$ raw counts, Simpson's paradox, Branching Overlap, Null Findings disclosure) |
| **Tufte Designer** | [`agents/agent-tufte-designer.md`](agents/agent-tufte-designer.md) | Formats Answer-First prose, Booktabs tables, `<aside class="margin-note">` callouts, school-aware `<svg>` charts, native LaTeX formulas, and print-ready HTML |

---

## The 8-Article Data Constitution ([`constitution.md`](constitution.md))

1. **Article 1 — Precision & Uncertainty:** Mandatory sample size ($N$), effective sample size ($N_{\text{eff}}$), and 95% CI Margin of Error (`±MoE%`) on every metric and subgroup.
2. **Article 2 — Effect Size Mandate:** A $p$-value ($p < 0.05$) never stands alone; every test requires its paired effect size (`Cramér's V`, `Cohen's d`, $\eta^2$, $\epsilon^2$, Pearson $r$ / Spearman $\rho$).
3. **Article 3 — Parametric & Non-Parametric Pairing:** Ordinal Likert scales and skewed variables ($|\text{skewness}| > 1.0$) pair `Mean ± SD` with `Median (IQR)` and non-parametric tests.
4. **Article 4 — Small Sample & Verbatim Discipline:** Whenever $N < 30$, percentages are strictly forbidden (`"4 of 19"` raw counts only). Every qualitative theme requires $\ge 2$ literal quotes and explicit **Silence Notes** for zero-response segments.
5. **Article 5 — Answer-First Honesty & Null Findings:** Headlines lead with the quantified conclusion (`n=..., p=..., Effect Size=...`). Non-significant tests ($p \ge 0.05$) are reported transparently in a **Null Findings** table. Every recommendation specifies `Target + Concrete Action + Quantified Expected Impact Range`.
6. **Article 6 — Automated Data Quality Gates:** Pre-analysis audit for **Straight-Lining** (row $\text{SD} = 0$ across $\ge 5$ Likert items + sensitivity $\Delta$), percentage sum verification ($100\% \pm 0.5\%$), and missingness thresholds ($>10\%$ and $>20\%$).
7. **Article 7 — Survey Governance, Weighting & Branching Overlap:** Programmatic `snake_case` schema mapping (`column_mapping.json`), explicit Raking/IPF weight handling with Kish's $N_{\text{eff}}$, and `0x0` skip-logic **Branching Overlap** validation.
8. **Article 8 — Multi-School Print-Ready HTML Deliverable Standard:** `final_report.html` is the primary deliverable, combining selectable **Data Design School** stylesheets (`references/styles/*.css`), school-aware `<svg>` graphics, native LaTeX math typography, and dual `@page` + `<table class="print-frame">` running headers and footers for one-click browser Print-to-PDF (`Ctrl+P` / `Cmd+P`).

---

## Quick Start & CLI Usage

### 1. Install into Your AI Harness or Project

```bash
# Interactive installer (supports Local .dps/, Global harness skills, or Both, plus default Design School selection):
node bin/install.js
```

### 2. Run the Full Python Pipeline Directly from CLI

```bash
# One-shot end-to-end execution (Setup -> Cross -> Advanced -> Quali -> Print-Ready HTML in chosen school):
python3 scripts/final_report_generator.py --data your_survey.csv -o .dps/outputs/export/ --title "Customer Intelligence Study" --school knaflic

# Or run individual Deep Module scripts step-by-step (picking a Data Design School on setup):
python3 scripts/quant_analyzer.py your_survey.csv --profile --school few -o .dps/outputs/setup/
# (Or run interactively: python3 scripts/quant_analyzer.py your_survey.csv --pick-school -o .dps/outputs/setup/)
python3 scripts/crosstabs.py your_survey.csv --execute-all -o .dps/outputs/cross/
python3 scripts/advanced_analytics_generator.py your_survey.csv --report-dir .dps/outputs/advanced/
python3 scripts/qualitative_categorizer.py your_survey.csv -o .dps/outputs/quali/
python3 scripts/final_report_generator.py --input .dps/outputs/ -o .dps/outputs/export/

# Compile any analytical Markdown report directly into multi-school Print-Ready HTML with native LaTeX math:
python3 scripts/tufte_html.py report.md -o final_report.html --school editorial --title "Executive Dossier"
```

---

## Repository Structure

```
Data-Pro-Skill/
├── SKILL.md                      # Master skill definition (Tier 1 Workflow, Tier 2 Loop, Tier 3 Context Pointers)
├── GLOSSARY.md                   # Canonical Leading Words (Leitworte) domain & statistical glossary
├── constitution.md               # Non-negotiable 8-Article statistical & visual constitution
├── CONTEXT.md                    # Architectural history, design philosophy & multi-agent engineering context
├── agents/                       # Specialized agent personas (Griller, Statistician, Critic, Anthropologist, Strategist, Tufte Designer)
├── bin/
│   └── install.js                # Interactive multi-harness CLI installer & school selector
├── references/
│   ├── dps-clarify.md            # Step 0: Data Grilling & Frontier Rounds protocol
│   ├── dps-setup.md              # Step 1: Schema mapping, Design School lock, weighting & Article 6 Quality Gates
│   ├── dps-plan.md               # Step 2: Test selection & 88 reasoning rules
│   ├── dps-cross.md              # Step 3: Crosstabs, Standardized Residuals (z_ij) & Branching Overlap
│   ├── dps-execute.md            # Step 4: Autonomous batch execution & Effect-Size Leaderboard
│   ├── dps-advanced.md           # Step 5: Master router for the 6 deep survey science modules
│   ├── dps-inject-open.md        # Step 6: Qualitative synthesis, verbatims & Silence Notes
│   ├── dps-export.md             # Step 7: Multi-school HTML compilation, LaTeX math engine & Print-to-PDF standard
│   ├── design-schools.md         # Specification for the 5 Data Design Schools (tufte, few, knaflic, swiss, editorial)
│   ├── tufte-rules.md            # Visual & typographic rules for high data-ink ratio reporting
│   ├── analysis/                 # 16 deep survey science methodology specs, stopwords_pt.txt & reasoning_rules.csv
│   ├── styles/                   # 5 school stylesheets (tufte.css, few.css, knaflic.css, swiss.css, editorial.css) & palettes
│   └── outputs/                  # Reference golden outputs (final_report.html, 00_profile.json, verification_report.json)
├── scripts/
│   ├── design_schools.py         # Registry & metadata manager for the 5 Data Design Schools
│   ├── quant_analyzer.py         # Dataset profiler, Quality Gates auditor & snake_case schema mapper
│   ├── crosstabs.py              # Hypothesis test engine, effect sizes, z_ij residuals & Branching Overlap guard
│   ├── advanced_analytics_generator.py # Pure Sentiment Stack, Priority Matrix, Expectation Residuals & Dual Clustering
│   ├── survey_pca.py             # Multi-Pass PCA/Factor Analysis & Cronbach's alpha
│   ├── turf_analysis.py          # Combinatorial TURF reach optimization
│   ├── weighting.py              # Iterative Proportional Fitting (Raking) & Kish's N_eff calculator
│   ├── qualitative_categorizer.py# Bilingual theme extraction, Article 4 small-N guard & Silence Notes
│   ├── tufte_viz.py              # School-aware vector <svg> chart compiler (Dot plots, Bullets, Knaflic bars, Bertin lollipops)
│   ├── tufte_html.py             # Self-contained HTML compiler, native LaTeX math engine & @page print-frame wrapper
│   └── final_report_generator.py # End-to-end orchestrator & 8-Article constitutional verifier
└── docs/                         # Detailed user guide, architecture, command reference & feature matrix (PT-BR)
```

---

## Community & Governance

- **Contributing Guide:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **Code of Conduct:** [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- **Security Policy:** [SECURITY.md](SECURITY.md)
- **Support & Questions:** [SUPPORT.md](SUPPORT.md)
- **Versioning Policy:** [VERSIONING.md](VERSIONING.md)

---

## License

MIT License. See [LICENSE](LICENSE).
