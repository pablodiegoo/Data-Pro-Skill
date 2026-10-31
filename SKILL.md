---
name: data-pro-skill
description: "Survey and market research data analysis system. Use when analyzing quantitative surveys, qualitative verbatims, or CSV/XLSX/ODS/Parquet datasets; running Data Grilling (/dps-grill, /dps-clarify) to uncover research objectives and hypotheses; building a Quantitative Manifesto and selecting a Data Design School (/dps-setup: Edward Tufte, Stephen Few, Cole Knaflic SWD, Swiss Grid/Bertin, or Economist/FT Editorial) or Analytical Plan (/dps-plan); computing weighted crosstabs and hypothesis tests (/dps-cross, /dps-execute); running deep survey science (/dps-advanced: Key Drivers, Halo Removal, Priority Matrix, Dual Clustering, Factor Analysis/PCA, TURF); injecting open-ended verbatims into quantitative segments (/dps-inject-open); synthesizing executive strategy (/dps-mode:strategy); or exporting print-ready multi-school HTML reports (/dps-export). Modes: /dps-mode:quant, /dps-mode:quali, /dps-mode:strategy. Requires constitution.md."
harness: universal
version: 2.1.0
requires:
  - constitution.md
  - GLOSSARY.md
---

# Data-Pro-Skill v2.1

Transform raw quantitative and qualitative survey data into high-density analytical reports (`final_report.html` + `final_report.md`), engineered to render on screen and print directly to PDF with standard running headers and footers across **five selectable Data Design Schools** (`tufte` [Edward Tufte — Default], `few` [Stephen Few], `knaflic` [Cole Knaflic / Storytelling with Data], `swiss` [Swiss Grid & Jacques Bertin], and `editorial` [The Economist / FT Editorial]).

**Bold terms** carry exact definitions in [`GLOSSARY.md`](GLOSSARY.md). Constitutional rules live in [`constitution.md`](constitution.md). Design school specifications live in [`references/design-schools.md`](references/design-schools.md).

---

## 1. Execution Sequence (Steps & Completion Criteria)

Work through these steps in order. Every step ends on a checkable, exhaustive **completion criterion** — never advance to post-completion steps until the current criterion holds.

### Step 0 — Data Grilling (`/dps-grill` or `/dps-clarify`)

Interview the user relentlessly in **frontier** rounds to lock the research objective, hypotheses, and **Analytical Spine** before committing to full execution. Read [`references/dps-clarify.md`](references/dps-clarify.md).

1. **Fact Reconnaissance first (never ask the user for facts in the environment).** Before asking Round 1, inspect the dataset yourself (`python3 .dps/scripts/quant_analyzer.py <data> --profile`, or inspect headers, $N$, missingness, Likert scales, multi-response `RM` groups, weight columns, and open-ended columns).
2. **Map the 5-branch Design Tree:**
   - **Branch 1 — Decision Destination & Data Design School:** What Monday-morning decision, budget allocation, or policy action hinges on this report, who is the audience, and which **Data Design School** (`tufte` [default], `few`, `knaflic`, `swiss`, or `editorial`) fits that audience?
   - **Branch 2 — Hypotheses & Priors:** What do stakeholders believe is happening, and what quantitative finding would falsify that prior?
   - **Branch 3 — Analytical Spine:** Which column is the primary dependent outcome (e.g., NPS, CSAT, Churn, Spend, Approval), and which columns define the canonical **segments** (banners)?
   - **Branch 4 — Weights & Governance:** Does the sample require **Raking (IPF)** against universe targets or uniform weights (`weight = 1.0`), and what survey skip/branching rules apply?
   - **Branch 5 — Deep Methodologies:** Which advanced modules (**Pure Sentiment Stack**, **Priority Matrix**, **Dual Clustering**, Factor Analysis/PCA, **TURF**, Qualitative Injection) do the hypotheses require?
3. **Work the tree in Frontier Rounds.** The **frontier** is every decision whose prerequisites are already settled. Ask the entire current frontier in one round, grounded in concrete dataset facts (column names, $N$, observed distributions), with a recommended default worded so `"yes"` accepts it:
   ```markdown
   ❓ **Q1** - **<Decision Title>**: <Question grounded in concrete dataset facts: columns, N, observed range/anomalies>

   ➡️ <Recommended answer — worded so "yes" accepts it>

   ---

   ❓ **Q2** - **<Decision Title>**: <Question body>

   ➡️ <Recommended answer>
   ```
4. **Model the domain inline.** As each round resolves, immediately update `.dps/outputs/column_mapping.json` (**Schema Mapping**: `snake_case` $\rightarrow$ original question text), `.dps/outputs/00_data_glossary.md`, and `.dps/outputs/clarify_notes.md`. Recompute the frontier and ask the next round.

- **Completion Criterion:** The **frontier** is empty (all 5 branches of the **Design Tree** resolved), `column_mapping.json` and `clarify_notes.md` are written to disk, and the user confirms shared understanding.

---

### Step 1 — Quantitative Manifesto & Data Design School Selection (`/dps-setup`)

Build the **Analytical Spine** that anchors every downstream command and let the user pick their preferred **Data Design School**. Read [`references/dps-setup.md`](references/dps-setup.md) and [`references/design-schools.md`](references/design-schools.md).

0. **Select Data Design School on Setup:** If not yet locked in `clarify_notes.md`, `.dps/config.json`, or via `--school`, let the user pick one of the 5 **Data Design Schools**:
   - `tufte` — **Edward Tufte *(Default)***: Ivory `#fffff8`, Palatino serif, 58%/36% floating right **Margin Notes**, **Booktabs Tables**, and Cleveland dot plots with 95% CI whiskers.
   - `few` — **Stephen Few**: Full-width perceptual BI grid (`#f8fafc`), Inter sans, **Bullet Graphs** (qualitative bands + target line), and inline `PERCEPTUAL DIAGNOSTIC` strips.
   - `knaflic` — **Cole Nussbaumer Knaflic (*Storytelling with Data*)**: Decluttered white canvas, muted grey context (`#cbd5e1`) + single bold focal accent (`#1e40af` / `#ea580c`), Action-Title banners, and `💡 KEY TAKEAWAY` cards.
   - `swiss` — **Swiss Grid & Jacques Bertin**: Exposed `1.5px`/`4px` black modular grid, Neo-Grotesque sans + monospace indices, and Bertin retinal lollipops/matrices (`#e63946` & `#1d3557`).
   - `editorial` — **The Economist / FT Editorial**: Warm newsprint (`#fcf8f2`), signature `6px` crimson top bar (`#e3120b`), Kicker + Headline + Standfirst hierarchy, and lollipop range charts.
1. **Enforce Schema Governance (`Article 7a`):** Map raw survey headers to clean `snake_case` keys in `.dps/outputs/setup/column_mapping.json`.
2. **Enforce Explicit Weighting (`Article 7b`):** Initialize `weight = 1.0` if unweighted, or run `scripts/weighting.py` (**Raking / IPF**) if universe targets were established during **Data Grilling**.
3. **Execute Deterministic Profiler & Setup Engine:**
   ```bash
   python3 .dps/scripts/quant_analyzer.py <data_file> [config.json] --school <tufte|few|knaflic|swiss|editorial> -o .dps/outputs/setup/
   ```
   *(Pass `--pick-school` for an interactive CLI school selector on setup.)*
4. **Run Invisible Agent Loop (Statistician $\rightarrow$ Critic $\rightarrow$ Designer):** Verify **Article 1** (95% CI MoE on every `%`), **Article 6a** (**Straight-Lining** detection on Likert blocks $\ge 5$ items), **Article 6b** ($100\% \pm 0.5\%$ sum validation on `RU` questions; explicit `Total Base` disclosure on `RM` questions), and **Article 6c** (missingness flags at $>10\%$ and $>20\%$).
5. **Render Manifesto (`00_project_manifest.md` / `setup_report.md`):** Output YAML frontmatter (`project`, `framework`, `design_school`, `sample_size`, `metrics_tracked`, `segments`), the canonical **Segment Matrix** (`Segment | N | % (±MoE%, 95% CI) | Core Metric`), per-variable distribution blocks, and the Data Quality Gate **Margin Note**.

- **Completion Criterion:** `setup_manifest.json`, `00_profile.json`, `design_school.json`, `setup_segments.csv`, and `setup_report.md` exist; the user's chosen **Data Design School** is locked; every dataset variable is accounted for; all 8 **Data Constitution** articles pass with zero contradictions.

---

### Step 2 — Analytical Plan (`/dps-plan`)

Design the hypothesis-driven test matrix before running crosstabs. Read [`references/dps-plan.md`](references/dps-plan.md) and [`references/analysis/statistical_test_selector.md`](references/analysis/statistical_test_selector.md).

1. Load `setup_manifest.json`, `00_profile.json`, and `clarify_notes.md` (if present).
2. Classify each Segment $\times$ Metric pair and stakeholder hypothesis by research goal (*Find Relationships*, *Compare Groups*, *Predict Outcomes*), variable scale (*categorical*, *ordinal/Likert*, *continuous*), group sample size ($N \ge 30$ vs $N < 30$), and skewness ($|\text{skew}| > 2$).
3. Match against [`references/analysis/statistical_test_selector.md`](references/analysis/statistical_test_selector.md) and [`references/analysis/reasoning_rules.csv`](references/analysis/reasoning_rules.csv) to select the exact test and effect size metric.
4. Render the advisory checklist table (`# | Hypothesis / Cross | Variables & Base | Recommended Test & Effect Size | Business Rationale`).

- **Completion Criterion:** Every segment $\times$ metric combination and grilled hypothesis is mapped to a justified parametric or non-parametric test and effect size in a single **Booktabs Table**.

---

### Step 3 — Hypothesis Testing & Slicing (`/dps-cross` & `/dps-execute`)

Slice variables with automatic assumption checks, statistical testing, and **Standardized Residual** anomaly detection. Read [`references/dps-cross.md`](references/dps-cross.md) and [`references/dps-execute.md`](references/dps-execute.md).

1. **Validate Branching Overlap (`Article 7c`):** Verify $N_{X \cap Y} > 0$ before crossing. If $N_{X \cap Y} = 0$, halt the cross and report mutually exclusive survey skip logic (`survey_branching_validation.md`).
2. **Run Deterministic Crosstab Engine:**
   ```bash
   python3 .dps/scripts/crosstabs.py <data_file> --index <VarX> --columns <VarY> --output .dps/outputs/cross/
   ```
   *(For `/dps-execute`, run across all prioritized Segment $\times$ Metric crosses from the manifesto or plan.)*
3. **Run Invisible Agent Loop:**
   - **Statistician:** Checks $N \ge 30$ per cell/group (`Article 5`), Shapiro-Wilk normality, and expected counts $E_{ij} \ge 5$. Selects $\chi^2$ + **Cramér's $V$** + **Standardized Residuals** $z_{ij} = (O_{ij}-E_{ij})/\sqrt{E_{ij}}$ (or Fisher's Exact if $E_{ij} < 5$ in 2×2); Welch's $t$ + **Cohen's $d$** (or **Mann-Whitney $U$**); One-Way ANOVA $F$ + $\eta^2$ (or **Kruskal-Wallis $H$** + $\epsilon^2$); or **Dual Correlation** (**Pearson's $r$** + **Spearman's $\rho$**).
   - **Critic:** Enforces `±MoE% (95% CI)` on every cell (`Article 1`), exact $p$-value + effect size (`Article 2`), and blocks unsupported significance claims when $p \ge 0.05$.
   - **Tufte Designer:** Renders the **Booktabs Table** with conclusion-first heading, inline/Mermaid chart, and interpretive **Margin Note** highlighting cells with $|z_{ij}| \ge 1.96$.

- **Completion Criterion:** Every requested cross (or the full `/dps-execute` matrix + effect-size-ranked synthesis) is written to `.dps/outputs/cross/` with verified test statistics, effect sizes, `±MoE%`, and **Margin Notes**.

---

### Step 4 — Deep Survey Science (`/dps-advanced`)

Execute multivariate, causal, and bias-removal methodologies when triggered by the **Design Tree** or `/dps-advanced`. Read [`references/dps-advanced.md`](references/dps-advanced.md).

```bash
python3 .dps/scripts/advanced_analytics_generator.py <data_file> <target_col> .dps/outputs/advanced/advanced_analytics.ipynb --report-dir .dps/outputs/advanced/
```

Applies the disclosed methodologies from `references/analysis/`:
- **Pure Sentiment Stack (`halo_removal.md`, `new_methodologies.md`):** **Ipsative Centering** ($X_{ij} - \bar{X}_i$) + regression-based **Halo Residual** extraction to isolate true attribute performance free of respondent grading bias.
- **Priority Matrix & Pain Curves (`priority_matrix.md`, `science.md`):** Crosses Derived Importance against Performance, computes $\text{Priority Score} = \text{Importance} \times (\text{Scale}_{\max} - \text{Performance})$, maps attributes into the 4 strategic quadrants (*Maximum Priority*, *Maintenance*, *Indifference*, *Over-investment*), and identifies non-linear **Pain Curve** rejection thresholds.
- **Causal Drivers & Expectation Residuals (`causal.md`):** Standardized regression + Random Forest feature importance on the outcome variable, plus **Expectation Residual** segmentation (*Disappointed*, *Aligned*, *Delighted*).
- **Dual Clustering & Latent Factors (`multivariate.md`, `analytical_methodology_patterns.md`):** **K-Means** (Silhouette-optimized marketing personas) paired with **DBSCAN** (density/outlier `-1` detection) or **Gower Distance** for mixed types; **Multi-Pass PCA / Factor Analysis** (Scree + loadings $|w| > 0.30$) with **Cronbach's $\alpha$** scale reliability (`r051`).
- **Portfolio Optimization (`turf_analysis.py`):** **TURF** incremental unduplicated reach and frequency curve.

- **Completion Criterion:** `.dps/outputs/advanced/advanced_report.md`, `advanced_metrics.json`, and `advanced_analytics.ipynb` exist, with every applicable methodology interpreted via Tufte **Booktabs Tables** and **Margin Notes**.

---

### Step 5 — Qualitative Injection (`/dps-inject-open [text or file]`)

Categorize open-ended verbatims *inside* the quantitative segments established by `/dps-setup`. Read [`references/dps-inject-open.md`](references/dps-inject-open.md).

1. Verify `/dps-setup` manifesto exists (hard prerequisite: qualitative findings never stand alone).
2. Run deterministic categorizer and verbatim extractor:
   ```bash
   python3 .dps/scripts/qualitative_categorizer.py <data_file> --text-col <col> --segment-col <seg_col> --segments .dps/outputs/setup/setup_segments.csv -o .dps/outputs/quali/
   ```
3. Run the 4-stage **Invisible Agent Loop** (Statistician $\rightarrow$ Critic $\rightarrow$ **Anthropologist** $\rightarrow$ Tufte Designer):
   - Enforces **Article 4**: whenever segment $N < 30$, report raw counts (`mentioned by n of N participants` / `mencionado por n de N participantes`) — **NEVER** percentages (`%`).
   - Requires $\ge 2$ literal `"verbatim quotes"` with participant context per reported theme; singletons go to `Isolated Mentions`.
   - Explicitly records **Silence Notes** for any manifesto segment with $0$ qualitative responses.

- **Completion Criterion:** `.dps/outputs/quali/quali_report.md`, `quali_themes.csv`, and `quali_verbatims.json` exist; every manifesto segment is accounted for (either with $\ge 2$-verbatim themes or an explicit silence note); zero `%` symbols appear on segments with $N < 30$.

---

### Step 6 — Executive Strategy Post-Processor (`/dps-mode:strategy`)

Translate validated quantitative and qualitative evidence into Monday-morning decisions. Read [`references/modes.md`](references/modes.md) and [`agents/agent-strategist.md`](agents/agent-strategist.md).

Appends five mandatory decision blocks before final export:
1. **Executive Summary:** 1 paragraph, maximum 4 sentences, headline business verdict first.
2. **Key Business Findings (3–5):** Evidence metric + business implication + calibrated confidence (`High / Medium / Low` with $N$ and `±MoE%`).
3. **Prioritization Matrix:** Action $\times$ Impact $\times$ Effort $\times$ Priority Tier (`⚡ Immediate`, `◆ Short-term`, `○ Long-term`) $\times$ Evidence link.
4. **Risk Assessment:** Risks of acting vs. risks of ignoring (`Probability × Impact × Mitigation`).
5. **Monday Morning Action Plan:** Concrete owner-ready steps for Week 1 and Weeks 2–4, plus open questions requiring follow-up research.

- **Completion Criterion:** All 5 strategic blocks are generated, every recommendation cites a specific metric or verbatim from the session, and zero unsupported opinions remain.

---

### Step 7 — Print-Ready Multi-School HTML & Markdown Export (`/dps-export`)

Consolidate all outputs in the dataset's native language (`pt-BR`, `en`, or `es`) and compile the self-contained **Print-Ready HTML** report (`final_report.html`) in the project's locked **Data Design School** (`tufte` default, `few`, `knaflic`, `swiss`, or `editorial`) alongside its source Markdown (`final_report.md`). Read [`references/dps-export.md`](references/dps-export.md), [`references/design-schools.md`](references/design-schools.md), and [`references/tufte-rules.md`](references/tufte-rules.md).

```bash
python3 .dps/scripts/final_report_generator.py --input .dps/outputs/ -o .dps/outputs/export/ [--school <tufte|few|knaflic|swiss|editorial>]
python3 .dps/scripts/tufte_viz.py --input .dps/outputs/ --charts-dir .dps/outputs/export/charts/ [--school <tufte|few|knaflic|swiss|editorial>]
python3 .dps/scripts/tufte_html.py --md .dps/outputs/export/final_report.md [--school <tufte|few|knaflic|swiss|editorial>]
```

- **HTML is the Primary Publication Output (`Article 8`):** `final_report.html` embeds the selected school's stylesheet (`tufte.css`, `few.css`, `knaflic.css`, `swiss.css`, or `editorial.css` — plus an interactive `.no-print` toolbar switcher to preview all 5 schools live), school-specific inline SVG visualizations (`tufte_viz.py` + compiled Mermaid `xychart-beta` / `pie` charts), `<aside class="margin-note">` sidenotes/callouts, `tabular-nums` data tables, and the **Print Frame** (`@page` + repeating `<thead>/<tfoot>` spacers + fixed running Header and Footer) so printing to PDF from any browser produces a publication-ready document with headers, footers, and clean page breaks.

- **Completion Criterion:** Both `.dps/outputs/export/final_report.md` and `.dps/outputs/export/final_report.html` exist, render in the dataset's native language and locked **Data Design School**, pass all 8 **Data Constitution** checks in `verification_report.json`, and include print-to-PDF running headers and footers.

---

## 2. Invisible Agent Loop

Every analytical command executes this internal pipeline silently. **Never display Stage 1, 2, or 3 reports to the user — emit only Stage 4 (Tufte Designer).** Detailed handoff contracts live in [`references/agent-loop.md`](references/agent-loop.md).

```
User Command → [Orchestrator] → [1. Statistician] → [2. Critic] → [3. Anthropologist*] → [4. Tufte Designer] → User Output
                                                                   (*active on /dps-inject-open & /dps-mode:quali)
```

| Stage | Agent Definition | Core Mandate |
| :---: | :--- | :--- |
| **0** | [`agents/agent-griller.md`](agents/agent-griller.md) | Runs **Fact Reconnaissance** + **Data Grilling** frontier rounds (`/dps-grill`, `/dps-clarify`). |
| **1** | [`agents/agent-statistician.md`](agents/agent-statistician.md) | Validates **Valid Base** vs **Total Base**, weights, 95% CI MoE, assumption checks, test selection, and effect sizes. |
| **2** | [`agents/agent-critic.md`](agents/agent-critic.md) | Audits Stage 1 against all 8 articles of [`constitution.md`](constitution.md). Blocks delivery on any violation. |
| **3** | [`agents/agent-anthropologist.md`](agents/agent-anthropologist.md) | Categorizes segment-anchored themes, extracts $\ge 2$ literal verbatims per theme, notes silences. |
| **4** | [`agents/agent-tufte-designer.md`](agents/agent-tufte-designer.md) | Synthesizes validated findings into zero-fluff Tufte Markdown and **Print-Ready Tufte HTML**. |
| **Post** | [`agents/agent-strategist.md`](agents/agent-strategist.md) | Post-processes completed analysis into executive strategy when `/dps-mode:strategy` is active. |

---

## 3. Tufte Output & Positive Steering Rules

State findings directly: open every section, paragraph, and **Margin Note** with a **metric**, a **named segment**, or a **falsifiable analytical finding**. Detailed typographic rules live in [`references/tufte-rules.md`](references/tufte-rules.md).

1. **Headline Finding in Every Heading:** Write `## Age × Churn — 18–24 Segment Concentrates 45.0% of Cancellations`, never `## Crosstab of Age and Churn`.
2. **Booktabs Tables with Explicit Base & MoE:** Every table includes a dedicated `N` column, `±MoE% (95% CI)` on proportions, `tabular-nums` alignment, and a **Base / Total** footer row distinguishing **Valid Base** from **Total Base**.
3. **Margin Notes Answer "So What?":** Follow every table or chart with `> **Margin Note:**` (or `> **Nota de Margem:**`) in 1–3 sharp sentences linking the statistical pattern ($p$, effect size, $|z| \ge 1.96$) to its causal mechanism, verbatim evidence, or business decision.
4. **The Deletion Test (`Article 3`):** Delete any sentence that lacks a number, a named segment/entity, or a falsifiable finding. Never open with throat-clearing phrases (*"It's important to note that..."*, *"Based on the data provided..."*, *"Interestingly..."*, *"The data suggests that..."*).

---

## 4. Context Pointers (Disclosed Reference Map)

Load these disclosed files on demand when their **branch** condition fires:

| Branch / Trigger Condition | Context Pointer |
| :--- | :--- |
| Running `/dps-grill` or `/dps-clarify` to interview the user on objectives, hypotheses, and the 5-branch **Design Tree** | [`references/dps-clarify.md`](references/dps-clarify.md) & [`agents/agent-griller.md`](agents/agent-griller.md) |
| Running `/dps-setup` to profile data, pick a **Data Design School**, map `snake_case` schema, apply weights, and build the **Analytical Spine** | [`references/dps-setup.md`](references/dps-setup.md), [`references/design-schools.md`](references/design-schools.md), [`references/analysis/survey_governance.md`](references/analysis/survey_governance.md), [`references/analysis/explicit_weight_handling.md`](references/analysis/explicit_weight_handling.md) |
| Running `/dps-plan` or choosing between parametric and non-parametric statistical tests and 88 reasoning rules | [`references/dps-plan.md`](references/dps-plan.md), [`references/analysis/statistical_test_selector.md`](references/analysis/statistical_test_selector.md), [`references/analysis/reasoning_rules.csv`](references/analysis/reasoning_rules.csv) |
| Running `/dps-cross` or `/dps-execute` for bivariate contingency tables, group comparisons, correlations, and branching checks | [`references/dps-cross.md`](references/dps-cross.md), [`references/dps-execute.md`](references/dps-execute.md), [`references/analysis/survey_branching_validation.md`](references/analysis/survey_branching_validation.md) |
| Running `/dps-advanced` for Key Drivers, **Pure Sentiment Stack** (**Ipsative** + **Halo Removal**), **Priority Matrix**, **Pain Curves**, **Dual Clustering**, Factor Analysis/PCA, or **TURF** | [`references/dps-advanced.md`](references/dps-advanced.md), [`references/analysis/new_methodologies.md`](references/analysis/new_methodologies.md), [`references/analysis/halo_removal.md`](references/analysis/halo_removal.md), [`references/analysis/priority_matrix.md`](references/analysis/priority_matrix.md), [`references/analysis/causal.md`](references/analysis/causal.md), [`references/analysis/multivariate.md`](references/analysis/multivariate.md), [`references/analysis/analytical_methodology_patterns.md`](references/analysis/analytical_methodology_patterns.md), [`references/analysis/science.md`](references/analysis/science.md), [`references/analysis/evaluation_and_diagnostics.md`](references/analysis/evaluation_and_diagnostics.md) |
| Running `/dps-inject-open` or `/dps-mode:quali` to categorize open-ended verbatims within quantitative segments | [`references/dps-inject-open.md`](references/dps-inject-open.md) & [`agents/agent-anthropologist.md`](agents/agent-anthropologist.md) |
| Switching personas (`/dps-mode:quant`, `/dps-mode:quali`, `/dps-mode:strategy`) | [`references/modes.md`](references/modes.md) & [`agents/agent-strategist.md`](agents/agent-strategist.md) |
| Running `/dps-export` or formatting **Print-Ready Multi-School HTML** (`tufte`, `few`, `knaflic`, `swiss`, `editorial`) with inline SVGs and `@page` / **Print Frame** running headers and footers | [`references/dps-export.md`](references/dps-export.md), [`references/design-schools.md`](references/design-schools.md), [`references/tufte-rules.md`](references/tufte-rules.md), [`references/styles/tufte.css`](references/styles/tufte.css), [`references/styles/few.css`](references/styles/few.css), [`references/styles/knaflic.css`](references/styles/knaflic.css), [`references/styles/swiss.css`](references/styles/swiss.css), [`references/styles/editorial.css`](references/styles/editorial.css), [`references/styles/visualization_rules.csv`](references/styles/visualization_rules.csv), [`references/styles/palettes.csv`](references/styles/palettes.csv) |
| Generating reproducible Jupyter notebooks or programmatic Markdown | [`references/analysis/notebook_generation_pattern.md`](references/analysis/notebook_generation_pattern.md), [`references/analysis/numbered_report_generation.md`](references/analysis/numbered_report_generation.md), [`references/analysis/markdown_generation_escapes.md`](references/analysis/markdown_generation_escapes.md) |
| Auditing against the 8 constitutional articles or resolving domain vocabulary | [`constitution.md`](constitution.md) & [`GLOSSARY.md`](GLOSSARY.md) |
