<div align="center">

# Data-Pro-Skill v2.0

**An autonomous Survey Science, Data Grilling & Edward Tufte Print-Ready HTML Reporting Skill for AI Agents.**

Transforms raw survey and behavioral datasets (`.csv`, `.xlsx`, `.ods`, `.parquet`) into statistically verified, Answer-First **Edward Tufte HTML reports** (`final_report.html`) engineered to print directly to PDF with standard running headers and footers — zero prose fluff, maximum data-ink ratio.

**Multi-Harness Compatible:** OpenCode · Gemini CLI · Antigravity CLI · Claude Code · Codex CLI · GitHub Copilot

</div>

---

## Why Data-Pro-Skill?

Most AI data analysis fails in three ways:
1. **Blind execution without business context:** Running generic descriptive charts without knowing what decision the stakeholder needs to make.
2. **Statistical theater:** Reporting raw averages masked by respondent **Halo Effect** (`yea-saying`), ignoring sample sizes ($N$), omitting 95% confidence Margins of Error (`±MoE%`), or hallucinating percentages on tiny open-ended samples ($N < 30$).
3. **Chartjunk & broken PDF exports:** Bloated dashboards or fragile LaTeX/Quarto toolchains instead of clean, self-contained HTML that prints cleanly to PDF from any browser.

**Data-Pro-Skill v2.0** solves all three by combining:
- **Matt Pocock Agent Architecture:** *Pit of Success* ordered workflow, *Progressive Disclosure* (`SKILL.md` → `GLOSSARY.md` → `constitution.md` → `references/analysis/*.md`), *Deep Module* Python scripts, and relentless **Data Grilling** (`/dps-grill`).
- **Deep Survey Science (`references/analysis/`):** Ipsative Centering & Regression Halo Removal, Derived Importance × Performance Priority Matrices, Expectation Residuals (*Disappointed / Aligned / Delighted*), Dual Correlation (Pearson $r$ vs. Spearman $\rho$), $\chi^2$ Standardized Residuals ($z_{ij}$), Silhouette-optimized K-Means Personas + DBSCAN Outlier isolation, Multi-Pass PCA/Factor Analysis + Cronbach's $\alpha$, TURF Reach Optimization, and Raking (IPF) sample weighting.
- **Edward Tufte Print-Ready HTML Standard:** Every analysis compiles into a single self-contained `final_report.html` styled with `references/styles/tufte.css` (`#fffff8` ivory screen background, 58%/36% body + floating right-margin sidenotes, `booktabs` tables with `tabular-nums`, inline vector `<svg>` graphics, and `@page` + `<table class="print-frame">` running headers and footers on every printed PDF page).

---

## Command Pipeline

Each command writes durable artifacts to `.dps/outputs/` that anchor the next stage, eliminating context rot:

| Step | Command | Purpose & Primary Output |
| :--- | :--- | :--- |
| **Step 0** | `/dps-grill` *(alias `/dps-clarify`)* | **Silent Fact Reconnaissance** on the dataset followed by **Frontier Rounds** (`❓ Q#` + `➡️ Recommended Default`) across a 5-branch Design Tree + live domain glossary (`00_data_glossary.md`). |
| **Step 1** | `/dps-setup` | Generates `column_mapping.json` (`snake_case` schema), `00_profile.json`, `setup_manifest.json`, and runs **Article 6 Quality Gates** (Straight-Lining detection, `%` sum check, missingness audit). |
| **Step 2** | `/dps-plan` | Applies Dr. Samira Hosseini's **Statistical Test Selector** and the 88 `reasoning_rules.csv` triggers to lock the `Analysis Plan` (`plan.md`). |
| **Step 3** | `/dps-cross [VarX] x [VarY]` | Runs targeted cross-tabulations with **Branching Overlap** validation (`0x0` skip-logic guard), $\chi^2$ / Fisher's Exact / Welch's $t$ / ANOVA / Kruskal-Wallis, **Standardized Residuals ($z_{ij}$)**, and 95% CI `±MoE%`. |
| **Step 4** | `/dps-execute` | Autonomously executes all planned cross-tabulations and synthesizes an **Effect-Size Leaderboard** (`Cramér's V`, `Cohen's d`, $\eta^2$, $|r|$). |
| **Step 5** | `/dps-advanced` | Executes the 6 deep survey science modules: **Pure Sentiment Stack** (Ipsative + Halo Removal), **Priority Matrix**, **Expectation Residuals**, **Dual Correlation**, **K-Means + DBSCAN Clustering**, **PCA/FA + Cronbach's $\alpha$**, and **TURF**. |
| **Step 6** | `/dps-inject-open` | Categorizes open-ended verbatims into emergent themes mapped to quantitative segments under **Article 4** ($N < 30$ raw counts `"4 of 19"` only, $\ge 2$ literal quotes per theme, and **Silence Notes**). |
| **Step 7** | `/dps-export` | Consolidates all findings into `final_report.md`, runs the 8-Article Constitutional Audit (`verification_report.json`), generates Tufte `<svg>` charts, and compiles the self-contained **Print-Ready Tufte HTML** (`final_report.html`). |

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
| **Griller** | `agents/agent-griller.md` | Silent data reconnaissance, 5-branch Design Tree interrogation, inline domain modeling (`GLOSSARY.md`) |
| **Statistician** | `agents/agent-statistician.md` | Executes Python scripts, pairs parametric (`Mean/SD`) + non-parametric (`Median/IQR`) metrics, computes 95% CI `±MoE%`, $p$-values, and effect sizes |
| **Critic** | `agents/agent-critic.md` | Enforces Articles 1–8 of `constitution.md` (Straight-Lining, $N < 30$ raw counts, Simpson's paradox, Branching Overlap, Null Findings disclosure) |
| **Tufte Designer** | `agents/agent-tufte-designer.md` | Formats Answer-First prose, Booktabs tables, numbered `<aside class="margin-note">` sidenotes, inline `<svg>` charts, and print-ready HTML |

---

## The 8-Article Data Constitution (`constitution.md`)

1. **Article 1 — Precision & Uncertainty:** Mandatory sample size ($N$), effective sample size ($N_{\text{eff}}$), and 95% CI Margin of Error (`±MoE%`) on every metric and subgroup.
2. **Article 2 — Effect Size Mandate:** A $p$-value ($p < 0.05$) never stands alone; every test requires its paired effect size (`Cramér's V`, `Cohen's d`, $\eta^2$, $\epsilon^2$, Pearson $r$ / Spearman $\rho$).
3. **Article 3 — Parametric & Non-Parametric Pairing:** Ordinal Likert scales and skewed variables ($|\text{skewness}| > 1.0$) pair `Mean ± SD` with `Median (IQR)` and non-parametric tests.
4. **Article 4 — Small Sample & Verbatim Discipline:** Whenever $N < 30$, percentages are strictly forbidden (`"4 of 19"` raw counts only). Every qualitative theme requires $\ge 2$ literal quotes and explicit **Silence Notes** for zero-response segments.
5. **Article 5 — Answer-First Honesty & Null Findings:** Headlines lead with the quantified conclusion (`n=..., p=..., Effect Size=...`). Non-significant tests ($p \ge 0.05$) are reported transparently in a **Null Findings** table. Every recommendation specifies `Target + Concrete Action + Quantified Expected Impact Range`.
6. **Article 6 — Automated Data Quality Gates:** Pre-analysis audit for **Straight-Lining** (row $\text{SD} = 0$ across $\ge 5$ Likert items + sensitivity $\Delta$), percentage sum verification ($100\% \pm 0.5\%$), and missingness thresholds ($>10\%$ and $>20\%$).
7. **Article 7 — Survey Governance, Weighting & Branching Overlap:** Programmatic `snake_case` schema mapping (`column_mapping.json`), explicit Raking/IPF weight handling with Kish's $N_{\text{eff}}$, and `0x0` skip-logic **Branching Overlap** validation.
8. **Article 8 — Tufte Print-Ready HTML Deliverable Standard:** `final_report.html` is the primary deliverable, using Edward Tufte CSS (`references/styles/tufte.css`) and dual `@page` + `<table class="print-frame">` running headers and footers for one-click browser Print-to-PDF (`Ctrl+P` / `Cmd+P`).

---

## Quick Start & CLI Usage

### 1. Install into Your AI Harness or Project

```bash
# Interactive installer (supports Local .dps/, Global harness skills, or Both):
node bin/install.js
```

### 2. Run the Full Python Pipeline Directly from CLI

```bash
# One-shot end-to-end execution (Setup -> Cross -> Advanced -> Quali -> Print-Ready Tufte HTML):
python3 scripts/final_report_generator.py --data your_survey.csv -o .dps/outputs/export/ --title "Customer Intelligence Study"

# Or run individual Deep Module scripts step-by-step:
python3 scripts/quant_analyzer.py your_survey.csv --profile -o .dps/outputs/setup/
python3 scripts/crosstabs.py your_survey.csv --execute-all -o .dps/outputs/cross/
python3 scripts/advanced_analytics_generator.py your_survey.csv --report-dir .dps/outputs/advanced/
python3 scripts/qualitative_categorizer.py your_survey.csv -o .dps/outputs/quali/
python3 scripts/final_report_generator.py --input .dps/outputs/ -o .dps/outputs/export/
```

---

## Repository Structure

```
Data-Pro-Skill/
├── SKILL.md                      # Master skill definition (Tier 1 Workflow, Tier 2 Loop, Tier 3 Context Pointers)
├── GLOSSARY.md                   # Canonical Leading Words (Leitworte) domain & statistical glossary
├── constitution.md               # Non-negotiable 8-Article statistical & visual constitution
├── agents/                       # Specialized agent definitions (Griller, Statistician, Critic, Anthropologist, Strategist, Tufte Designer)
├── references/
│   ├── dps-clarify.md            # Step 0: Data Grilling & Frontier Rounds protocol
│   ├── dps-setup.md              # Step 1: Schema mapping, weighting & Article 6 Quality Gates
│   ├── dps-plan.md               # Step 2: Test selection & 88 reasoning rules
│   ├── dps-cross.md              # Step 3: Crosstabs, Standardized Residuals (z_ij) & Branching Overlap
│   ├── dps-execute.md            # Step 4: Autonomous batch execution & Effect-Size Leaderboard
│   ├── dps-advanced.md           # Step 5: Master router for the 6 deep survey science modules
│   ├── dps-inject-open.md        # Step 6: Qualitative synthesis, verbatims & Silence Notes
│   ├── dps-export.md             # Step 7: Tufte HTML compilation & Print-to-PDF running header/footer standard
│   ├── analysis/                 # 16 deep survey science methodology specs, stopwords_pt.txt & reasoning_rules.csv
│   ├── styles/                   # tufte.css (screen + @media print PDF engine) & visualization rules
│   └── outputs/                  # Reference golden outputs (final_report.html, 00_profile.json, verification_report.json)
└── scripts/                      # Self-contained Python analytical & Tufte SVG/HTML compilation scripts
```

---

## License

MIT License. See [LICENSE](LICENSE).
