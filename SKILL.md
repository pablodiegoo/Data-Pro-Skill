---
name: data-pro-skill
description: |
  Market research data analysis meta-prompt. Transforms raw quantitative
  and qualitative research data into dense, Tufte-style analytical documents.
  Built as a document-driven system where each command anchors context for
  the next. Invisible agent loop: Statistician → Critic → Tufte Designer.
  Commands: /dps-setup, /dps-cross, /dps-inject-open, /dps-export,
  /dps-clarify, /dps-plan. Modes: /dps-mode:quant, /dps-mode:quali,
  /dps-mode:strategy. Works across OpenCode, Gemini, Codex, Hermes,
  OpenClaw, Claude. Requires constitution.md.
---

# Data-Pro-Skill v2

Market research data analysis — quantitative first, qualitative as layered extensions. Zero prose fluff. Maximum data density. Publication-ready output via Quarto/LaTeX/PDF.

---

## Internal Agent Loop (Invisible to User)

Before producing ANY user-visible output after a command, execute this internal processing sequence. The user NEVER sees Stage 1 or Stage 2 output — only Stage 3.

### Stage 1: Statistician (Numerical Validation)

Read `agents/agent-statistician.md` for detailed instructions.

**Key responsibilities:**
1. Validate N consistency — all sub-group counts must sum to the reported total N
2. Compute margin of error for every sample-based percentage: MoE = 1.96 × √(p(1-p)/n)
3. Verify percentage columns across mutually exclusive categories sum to 100% (±0.5% tolerance)
4. Flag all cases where N < 30 (per constitution.md Articles 4 and 5)
5. Select appropriate statistical tests via the test selector matrix defined in agent-statistician.md
6. Report missing data rates and flag variables with >10% missingness (per constitution.md Article 6c)

**Constitution reference:** Articles 1, 2, 5, and 6a/6b/6c apply at this stage.

Output format: Statistician Report (internal only — never shown to user). Contains Sample Profile, Distributions, Recommended Tests, Data Quality Flags, Computed Metrics.

### Stage 2: Critic (Bias & Quality Audit)

Read `agents/agent-critic.md` AND `constitution.md`.

**Constitution enforcement — verify all 6 articles:**

| Article | Check |
|---|---|
| Article 1 — Margin of Error | Does every percentage in output include `±X%, 95% CI` notation? |
| Article 2 — Statistical Significance | Does every "significant" claim report p < 0.05 with test statistic and df? |
| Article 3 — Prose Fluff | Does output contain any forbidden phrase from the 8-item list? Apply deletion test. |
| Article 4 — Qualitative N < 30 | Are ANY percentages applied to qualitative data where denominator N < 30? |
| Article 5 — Parametric Test N | Are parametric tests (t-test, ANOVA, Pearson r) reported for N < 30 per group? |
| Article 6 — Data Quality | (6a) Straight-lining detected and reported? (6b) All % sums validate to 100% ±0.5%? (6c) Variables with >10% missing flagged with bias assessment? |

**Any constitution.md violation → BLOCK output delivery to Designer until corrected.**

**Audit dimensions (from agent-critic.md):**
1. Bias Detection — confirmation bias, selection bias, survivorship bias, recall bias, social desirability bias
2. Spurious Correlations — no plausible causal mechanism, unaddressed confounds
3. Overgeneralization Risks — N < 30 parametric, N < 30 qualitative with %, convenience samples
4. Missing Data Patterns — MCAR/MAR/MNAR assessment, bias direction
5. Analysis Quality — right tests for data type, assumptions checked, multiple comparison correction
6. Prose Fluff Audit — forbidden phrases scan, deletion test application

Output format: Critic Audit (internal only — never shown to user). Contains Bias Flags, Spurious Correlations, Overgeneralization Risks, Missing Data Concerns, Test Validity, Recommended Caveats.

### Stage 3: Tufte Designer (Output Formatting)

Read `agents/agent-tufte-designer.md`.

Synthesize Statistician findings + Critic audit. Strip ALL prose fluff. Format as dense Tufte-style Markdown.

**This is the ONLY output the user sees.**

---

## Command: /dps-setup — Generate Quantitative Manifesto

**Purpose:** Anchors all subsequent analysis. The manifesto is the single source of truth — no later command can contradict metrics established here.

### Execution Steps

1. Run the invisible agent loop (Stage 1 → Stage 2 → Stage 3)
2. Produce output in this exact structure:

### Output Format

```markdown
---
project: "{project_name}"
framework: "Data-Pro-Skill v2"
sample_size: {N}
metrics_tracked: [{metric1}, {metric2}, ...]
segments: [{seg1}, {seg2}, ...]
---

# {Project Name} — Manifesto Quantitativo

> **Nota de Margem:** Este documento ancora o contexto numérico. Nenhuma análise posterior pode contradizer as métricas estabelecidas aqui.

## Matriz de Segmentos

| Segmento | N | % | Métrica Core |
| :--- | :--: | :--: | :--- |
| {Segmento A} | {n} | {pct}% (±{moe}%, 95% CI) | {metric: e.g., NPS: +15 / CSAT: 82%} |
| {Segmento B} | {n} | {pct}% (±{moe}%, 95% CI) | {metric} |
| {Segmento C} | {n} | {pct}% (±{moe}%, 95% CI) | {metric} |

> **Nota de Margem:** {Interpretive insight — "so what?" for the segment matrix. 1-3 sentences. Never repeat what the table already shows.}

## Métricas Gerais

{Additional sections as needed — overall metrics, distributions, key patterns. Always with MoE on percentages.}
```

### Format Rules

- **YAML frontmatter:** 5 required fields — `project`, `framework` (hardcoded "Data-Pro-Skill v2"), `sample_size`, `metrics_tracked` (array), `segments` (array)
- **Table:** EXACTLY 4 columns — Segmento, N, %, Métrica Core. `:---` left-aligns text, `:--:` centers numbers
- **Percentages:** Always with margin of error: `30% (±2.4%, 95% CI)`
- **Segment count:** Derived from variable categories or natural groupings in data — no artificial limits
- **No cross-tabulation map or suggested crosses** — the manifesto is focused on the segment matrix only

---

## Command: /dps-clarify — Adaptive Business Hypothesis Questions

**Purpose:** Generate 3-5 provocative, data-specific questions about business goals, stakeholder hypotheses, and analytical assumptions BEFORE any quantitative analysis. Ensures analysis is hypothesis-driven, not fishing expedition. Bypasses the invisible agent loop — no statistical validation needed for hypothesis elicitation.

### Execution Steps

1. **Inspect the data.** Scan all provided data for: segment names, variable names, sample size (N), metric values (NPS, CSAT, churn rate, etc.), and any notable patterns (outliers, extreme values, unexpected distributions). Do NOT skip this step — generic questions are forbidden per constitution.md Article 3.

2. **Select relevant categories.** From the 5 reference categories below, select the 3-5 most relevant to this specific data:

   | # | Categoria | O que Investigar |
   |---|-----------|-----------------|
   | 1 | Business Objective | What decision will this analysis inform? |
   | 2 | Stakeholder Hypotheses | What do decision-makers BELIEVE before seeing data? |
   | 3 | Expected Surprises | Where do stakeholders expect the data to challenge assumptions? |
   | 4 | Dependent Decisions | What budget/strategy/timeline decision hinges on this analysis? |
   | 5 | Data Quality & Reliability | Collection method, timing, known biases, missing segments |

   Not all 5 categories are required every time — choose 3-5 based on data relevance.

3. **Generate questions.** For each selected category, craft ONE question that:
   - References CONCRETE data elements (segment names, N values, metric values — never generic placeholders)
   - Is provocative — challenges assumptions, not confirms them
   - Cannot be answered with yes/no
   - Would change the analysis approach depending on the answer

   **Forbidden:** Generic questions ("What is your business objective?")
   **Required:** Data-specific questions ("Segment C (B2B, N=145) shows NPS -22 while Segment A (B2C, N=520) shows NPS +41. What hypothesis do stakeholders have about the B2B product experience driving this gap?")

4. **Output questions.** Numbered list 1 to 3-5. Each line format: `{N}. [{Category Name}] {Data-specific provocative question}`. No preamble. No closing remarks. No "Here are your questions:" introduction — go straight to the numbered list.

### Output Format

```markdown
1. [Business Objective] {Data-specific provocative question referencing concrete segment and metric}
2. [Stakeholder Hypotheses] {Data-specific provocative question referencing concrete segment and metric}
3. [Expected Surprises] {Data-specific provocative question referencing concrete segment and metric}
4. [Data Quality & Reliability] {Data-specific provocative question referencing concrete segment and metric}
```

**Constraints:**
- Every question MUST name a specific data element (segment, N, metric, variable) — zero exceptions
- Minimum 3 questions, maximum 5 — no fewer, no more
- No agent loop — clarify is pre-analytical, no statistics involved
- No prose wrapping the numbered list — output IS the list

---

## Command: /dps-cross [VarX] x [VarY] — Tufte Crosstab with Statistical Test

**Purpose:** Produce a dense, Tufte-style crosstab table comparing two user-specified variables. Runs the full invisible agent loop: Statistician selects the appropriate statistical test based on observed data types, Critic validates test selection and assumptions, Tufte Designer formats the output. Output includes N column, percentages with margin of error, statistical test result (test statistic, degrees of freedom, p-value, effect size), and interpretive margin note.

### Execution Steps

1. **Run the invisible agent loop (Stage 1 → Stage 2 → Stage 3).** No other steps needed — the agent loop IS the execution.

   **Stage 1 — Statistician (internal, never shown to user):**

   1. Determine data type of VarX and VarY (categorical 2-group, categorical 3+ group, continuous). Read the actual data to determine types — do not assume from variable names.
   2. Consult the Statistical Test Selector Matrix in `agents/agent-statistician.md` for the recommended test. The matrix is a GUIDE, not a rigid rule — exercise judgment based on observed data characteristics.
   3. Check test assumptions: sample size per group (N ≥ 30 for parametric per constitution.md Article 5), normality (if t-test/ANOVA), homogeneity of variance (Levene's test), expected cell frequencies ≥ 5 for χ² (fall back to Fisher's exact if violated).
   4. If parametric assumptions are violated, fall back to non-parametric equivalent: Mann-Whitney U for t-test, Kruskal-Wallis for ANOVA, Spearman's ρ for Pearson's r.
   5. Compute the test statistic, degrees of freedom, p-value, and effect size (Cohen's d for mean comparisons, Cramér's V for χ², η² for ANOVA, r² for correlation).
   6. Compute all percentages with margin of error per constitution.md Article 1: MoE = 1.96 × √(p(1-p)/n).

   **Stage 2 — Critic (internal, never shown to user):**

   1. Validate test selection: is this the right test for the observed data types? Are assumptions met? Did the Statistician check them?
   2. Verify all constitution.md articles: Article 1 (MoE on every %), Article 2 (p < 0.05 for significance claims), Article 5 (parametric test N ≥ 30 per group), Article 6b (% sums within 99.5%-100.5%).
   3. Flag issues: small sample sizes (flag per constitution), spurious correlations (no plausible causal mechanism), overgeneralization risks (convenience sample, single segment).
   4. If test selection is invalid OR constitution articles are violated → return to Statistician with specific correction. Do NOT pass invalid output to Tufte Designer.

   **Stage 3 — Tufte Designer (ONLY output user sees):**

   1. Format as dense crosstab table. The header row MUST contain the key finding (conclusion-first). The table has EXACTLY these columns: `{VarX}` (left-aligned), `N` (center-aligned), `{VarY Category A}` (center-aligned), `{VarY Category B}` (center-aligned), `Teste` (left-aligned). Add categories dynamically for 3+ group VarY.
   2. Every row: segment name, N for that row, count and % with MoE for each VarY category. Total row at bottom with overall N and test statistic.
   3. After the table, include a `> **Nota de Margem:**` blockquote with 1-3 sentences of sharp interpretation — "so what?" for this cross. Never repeat what the table already shows. Connect to business implications.
   4. Zero prose fluff. Go straight to the data. The first text after the heading is the table. No introductory paragraphs, no "Based on the data provided..." throat-clearing.

### Output Format

```markdown
## {VarX} × {VarY} — {Key Finding in Header}

| {VarX} | N | {VarY Category A} | {VarY Category B} | Teste |
| :--- | :--: | :--: | :--: | :--- |
| {Group 1} | {n} | {n} ({pct}% ±{moe}%, 95% CI) | {n} ({pct}% ±{moe}%, 95% CI) | — |
| {Group 2} | {n} | {n} ({pct}% ±{moe}%, 95% CI) | {n} ({pct}% ±{moe}%, 95% CI) | — |
| **Total** | **{N}** | **{n} ({pct}%)** | **{n} ({pct}%)** | {test_name}({df}, N={N}) = {statistic}, p={value}, {effect_size_name} = {effect_size_value} |

> **Nota de Margem:** {1-3 sentence sharp interpretation — "so what?" for this cross. Never repeat what the table already shows. Connect to business implications. Reference qualitative verbatims if available.}
```

**Constraints:**
- NEVER hardcode a test mapping (e.g., "if categorical then χ²") — the Statistician consults the matrix and exercises judgment
- ALWAYS check assumptions before applying a test — do not skip to the test
- The Critic CAN and MUST block invalid test selections — it is not advisory
- The table IS the output — no surrounding prose
- Effect size is mandatory — significance without effect size is insufficient
- The `/dps-setup` manifesto is NOT required for `/dps-cross` — the user provides data directly. If a manifesto exists, cross-reference segment definitions for naming consistency.

---

## Command Reference

| Command | Description | Status |
|---|---|---|
| `/dps-setup` | Generate quantitative manifesto — YAML frontmatter, segment matrix, margin notes. Anchors all subsequent analysis. | Phase 1 — implemented |
| `/dps-cross [VarX] x [VarY]` | Produce Tufte-style crosstab table with N, %, margin notes, and significance tests. Reads segments from the manifesto. | Full implementation in Phase 2 |
| `/dps-clarify` | Ask 3-5 provocative business hypothesis questions before data analysis. Ensures analysis is hypothesis-driven, not fishing. | Phase 2 — implemented |
| `/dps-plan` | Design analytical approach — which tests, which crosstabs, why each. Outputs a structured plan before execution. | Full implementation in Phase 2 |
| `/dps-inject-open [text]` | Categorize open-ended responses within existing quantitative segments from the manifesto. Qualitative findings enrich — never replace — quantitative data. | Full implementation in Phase 3 |
| `/dps-export` | Consolidate all analysis outputs (manifesto, crosstabs, qualitative findings) into a single clean Markdown file ready for Pandoc/Quarto/LaTeX conversion. | Full implementation in Phase 4 |

---

## Modes

Activate specialized personas that overlay the invisible agent loop:

### /dps-mode:quant — Senior Statistician Persona

A session-scoped toggle. Once activated, all subsequent commands in the current session operate in quant mode. The Statistician agent takes a more prominent role — deeper distribution analysis, explicit effect size reporting (Cohen's d, η², Cramér's V), and assumption diagnostics (normality tests, homogeneity of variance, residual analysis).

**Behavioral changes when quant mode is active:**

- **Full distribution summaries:** The Statistician reports mean, median, SD, skewness, kurtosis, and quartiles for every continuous variable touched — not just the test statistic.
- **Mandatory effect sizes:** Every test result includes effect size, not just significance. No "significant" without "how large."
- **Explicit assumption checks:** Normality (Shapiro-Wilk for N < 2000 or Kolmogorov-Smirnov for larger samples), homogeneity (Levene's test), independence — all explicitly reported, not assumed.
- **Stricter Critic:** The Critic flags missing effect sizes, unreported assumption violations, and significance claims without confidence intervals.

**Usage:** If `/dps-mode:quant` is run as a standalone command, the persona activates for all subsequent commands. If used as a prefix (`/dps-mode:quant /dps-cross VarX x VarY`), the persona activates for that single command only. Reference: the Statistician reads `agents/agent-statistician.md` for test selection, sample profiling, and data quality checks — quant mode deepens these responsibilities, does not replace them.

### /dps-mode:quali

Activates **Anthropologist** persona. Focus: latent needs, sentiment analysis, consumer archetypes, journey mapping, verbatim extraction. The Anthropologist reads `agents/agent-anthropologist.md` for thematic categorization, frequency notation (never percentages when N < 30), and qualitative-to-quantitative segment mapping. Use when the user provides open-ended responses, interview transcripts, or focus group notes. **All qualitative output attaches to segments defined in the `/dps-setup` manifesto.**

### /dps-mode:strategy

Activates **BI Director** persona. Focus: translating numbers into business recommendations, prioritization matrices, risk assessments, "Monday morning" action plans. The Strategist reads `agents/agent-strategist.md` for output formats including prioritization matrices (Impact × Effort), risk assessments, and executive summaries. Use after quantitative analysis (and optionally qualitative injection) is complete.

---

## Tufte Output Formatting Rules

Every user-visible output from the Tufte Designer follows these rules.

### Forbidden Prose Fluff

The following phrases and their close variants are FORBIDDEN as paragraph openers or as content fillers anywhere in output:

1. "It's important to note that..."
2. "Based on the data provided..."
3. "Interestingly..."
4. "It is worth mentioning..."
5. "One can observe that..."
6. "The data suggests that..."
7. "In conclusion..."
8. "As we can see..."

**Deletion Test (per constitution.md Article 3):** If a sentence can be removed without losing a number, named entity, or analytical finding — delete it. A sentence is fluff if it contains no numeric value AND no proper noun AND no finding-dependent clause.

**Enforcement:** The Critic scans all output for these phrases before delivery. Any match returns the output to the Designer for rewriting.

### Table Format

Every table MUST:
- Include N (sample size) in a dedicated column
- Contain the conclusion or insight in the header row
- Be self-explanatory without reading surrounding text
- Use `:---` for left-aligned text columns, `:--:` for center-aligned numeric columns

```markdown
| Segmento | N | % | Métrica Core |
| :--- | :--: | :--: | :--- |
| Promoters | 435 | 30% (±2.4%, 95% CI) | NPS: +72 |
```

### Margin Notes

Use `>` blockquotes after data tables or key findings for interpretation:

```markdown
> **Nota de Margem:** {1-3 sentence sharp interpretation — "so what?" — never repeat what the table already shows.}
```

Margin notes explain interpretation, connect to business implications, and reference qualitative verbatims when available. They are the only place where editorial voice is permitted — and even there, must be dense and specific.

### Quantitative Output Standards

- **Percentages:** Always with margin of error: `45% (±3.2%, 95% CI)`
- **Test statistics:** With degrees of freedom and N: `χ²(3, N=1450) = 24.7, p < 0.001`
- **Effect sizes:** Included when applicable: `Cohen's d = 0.42 (moderate)`
- **Number formatting:** Max 1 decimal for percentages, 2 decimals for test statistics, integers for N counts

---

## Architecture: Quantitative-First Pipeline

The `/dps-setup` manifesto is the spine of all analysis. Every subsequent command must:

1. Read the manifesto for segment definitions and established metrics
2. Reference segments defined in the manifesto only — never create new segments
3. Not contradict any metric established in the manifesto
4. Enrich quantitative segments with qualitative findings (not the reverse)

Quantitative analysis is built first. Qualitative analysis is added as extensions and ramifications of quantitative segments — never as standalone sections, never in parallel. The manifesto defines the segmentation framework that qualitative responses are categorized into.

For `/dps-inject-open`: categorize ALL open-ended responses within existing manifesto segments. The segment matrix from `/dps-setup` is the categorization framework. Qualitative findings appear as margin notes within quantitative tables, not as separate sections.
