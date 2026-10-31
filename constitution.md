# Data-Pro-Skill v2 — Analytical Constitution

> **Purpose:** This document defines the non-negotiable statistical, methodological, and typographic rigor rules of Data-Pro-Skill. It is read and enforced by the **Critic agent** during Stage 2 of the DPS **Invisible Agent Loop**. Every analysis command (`/dps-setup`, `/dps-cross`, `/dps-execute`, `/dps-advanced`, `/dps-inject-open`, `/dps-export`) triggers the Critic to audit output against all 8 articles below. Any violation blocks delivery to the Tufte Designer.

> **Enforcement:** All 8 articles are enforced by the Critic agent during Stage 2 of the DPS invisible agent loop. Violations block output delivery to the Tufte Designer. The Critic answers "is this violated?" with a mechanical yes/no decision on each article, per output, per command. Vocabulary follows [`GLOSSARY.md`](GLOSSARY.md).

---

## Article 1 — Margin of Error Mandatory on All Sample-Based Claims

### Rule
Every percentage or proportion derived from a sample MUST be accompanied by its margin of error at the 95% confidence level. No sample-based claim may be presented as a bare percentage without its confidence interval.

**Formula:** $\text{MoE} = z_{\text{crit}} \times \sqrt{p(1-p)/n}$, where $z_{\text{crit}} = 1.96$ for 95% confidence, $p = \text{proportion } (0 \text{ to } 1)$, $n = \text{valid sample size}$.

Every reported percentage must appear as: `X% (±Y%, 95% CI)` (or `X% ±Y%` inside dense multi-column crosstab cells where `95% CI` is declared in the table header/footer), where `Y` is the computed margin of error rounded to 1 decimal place.

### Justification
Point estimates without confidence intervals imply false precision. A reported "45% prefer Brand A" without MoE misleads the reader into believing certainty where none exists. The margin of error communicates the precision of the estimate given the sample size — without it, the reader cannot judge whether a difference between two percentages is real or noise.

### Violation Consequence
The Critic refuses to pass output to the Tufte Designer until margin of error is computed and displayed on every sample-based percentage claim. A bare percentage without `±Y%, 95% CI` is a hard block.

### Detection Method / Computation
- **Detection:** Scan output for any percentage not followed by `±` / `95% CI` notation. Also scan for "margin of error" in prose that is not accompanied by a numeric value.
- **Computation:** For each percentage $p\%$ with valid sample size $n$, compute $\text{MoE} = 1.96 \times \sqrt{p(1-p)/n}$. If $\text{MoE} > 10.0\%$, append flag: `"wide confidence interval (±Y%) — treat finding as provisional"`.
- **Testable:** Every percentage in output either has MoE notation or the output is blocked. Yes/no.

---

## Article 2 — Statistical Significance Threshold ($p < 0.05$) & Effect Size

### Rule
All claims of difference, correlation, anomaly, or effect between variables MUST report:
1. The exact test statistic and degrees of freedom (`χ²(df, N=n) = value`, `t(df) = value`, `U = value`, `F(df1, df2) = value`, `H(df) = value`, `r = value`, `ρ = value`).
2. The exact $p$-value (e.g., `p = 0.014`, or `p < 0.001` when below $0.001$).
3. The corresponding **effect size** (`Cramér's V`, `Cohen's d`, `η²`, `ε²`, or `r²`) with magnitude interpretation (*negligible*, *small*, *moderate*, *large*).
4. For contingency tables ($\chi^2$), cell-level claims of local attraction or rejection must be backed by **Standardized Residuals** $z_{ij} = (O_{ij} - E_{ij}) / \sqrt{E_{ij}}$ exceeding $|z_{ij}| \ge 1.96$.
5. When $>5$ simultaneous hypothesis tests are run in a battery (`r031`), apply Bonferroni or Benjamini-Hochberg FDR correction.

A $p$-value $\ge 0.05$ disallows language asserting "significant", "meaningful difference", "clear relationship", or any equivalent claim of reliable effect. When $p \ge 0.05$, the output must state: `"no statistically significant difference found (p = {value})"`. Never claim causation from observational correlation (`r075`).

### Justification
Without a significance threshold, any observed difference can be claimed as real, even when attributable to random chance. Conversely, in large samples ($N > 1000$), trivial differences can achieve $p < 0.05$; pairing $p$-values with effect sizes separates statistical significance from practical business importance (`r030`, `r076`).

### Violation Consequence
The Critic downgrades unsupported significance claims and blocks any output that asserts a relationship without reporting a test statistic, exact $p$-value, and effect size.

### Detection Method / Computation
- **Detection:** Scan output for the words "significant", "significant difference", "meaningful", "clear relationship", "correlated", "associated", "anomaly". Each instance MUST be accompanied by a test statistic, $p$-value, and effect size.
- **Verification:** For each significance claim, verify that the reported $p < 0.05$. If $p \ge 0.05$ is reported but language still claims significance, flag as contradiction.
- **Testable:** Count all significance-language assertions. Verify each has a test statistic, $p$-value $< 0.05$, and effect size. Reject if any assertion violates this rule. Yes/no.

---

## Article 3 — Prohibition of Prose Fluff & The Deletion Test

### Rule
Output must go straight to the data. The first sentence after any heading must be a finding, a number, or a named entity — never throat-clearing. The following phrases and all their close variants (in English, Portuguese, or Spanish) are FORBIDDEN as paragraph openers or content fillers:

1. "It's important to note that..." / "É importante notar que..."
2. "Based on the data provided..." / "Com base nos dados fornecidos..."
3. "Interestingly..." / "Interessantemente..."
4. "It is worth mentioning..." / "Vale mencionar que..."
5. "One can observe that..." / "Pode-se observar que..."
6. "The data suggests that..." / "Os dados sugerem que..."
7. "In conclusion..." / "Em conclusão..."
8. "As we can see..." / "Como podemos ver..."

**Deletion Test:** If a sentence can be removed without losing a number, named entity, or falsifiable finding, it is fluff. Delete it. A sentence qualifies as fluff if: (a) it contains no numeric value, (b) it contains no proper noun or named segment/entity, and (c) it contains no analytical finding that changes understanding of the data.

### Justification
Prose fluff adds words without adding information. It reduces data density — the ratio of meaningful content to total text. Edward Tufte's principle: *"Maximize data-ink ratio"* translates directly to prose: maximize information per word. Phrases like "It's important to note that..." occupy 6 words conveying zero information — the reader must scan past them to reach the actual finding.

### Violation Consequence
The Critic scans every output for these phrases before delivery. Any match returns the output to the Tufte Designer with fluff phrases highlighted. The Designer must remove or rewrite the offending sentences before the output can be delivered to the user.

### Detection Method / Computation
- **Detection:** Grep output for the 8 forbidden phrase patterns (case-insensitive, across EN/PT/ES). Apply the Deletion Test to the first sentence of every paragraph: if it contains no numeric digit, no proper noun/segment, and no finding-dependent clause, flag as fluff.
- **Testable:** Count matches of forbidden phrases in output. If count $> 0$, output is blocked. Yes/no.

---

## Article 4 — Prohibition of Percentages in Qualitative Samples ($N < 30$)

### Rule
When $N < 30$ for qualitative data (open-ended responses, interviews, focus groups, verbatim coding within a segment), NEVER report percentages. Quote literal verbatims directly. Note frequency strictly as raw counts: `"mentioned by n of N participants"` (`"mencionado por n de N participantes"`) without false precision. The output must not contain percentage symbols (`%`) applied to any qualitative sample where the denominator $N < 30$. Every reported qualitative theme requires a minimum of **2 literal verbatims**; single mentions must be relegated to `Isolated Mentions` (`Menções Isoladas`).

### Justification
A percentage computed from $N < 30$ creates an illusion of quantitative rigor where none exists. Reporting that "67% mentioned pricing" when $N = 12$ creates false precision — one respondent changes the percentage by 8.3 percentage points. Small samples cannot support percentage generalization; they support thematic identification and verbatim representation.

### Violation Consequence
The Critic flags any quantitative generalization or `%` symbol from small qualitative samples ($N < 30$) or any theme with $<2$ verbatims as a hard block. Output cannot be delivered to the Tufte Designer until corrected.

### Detection Method / Computation
- **Detection:** Scan output for any statement of the form "X% of respondents mentioned Y" or percentage symbols in qualitative sections where segment $N < 30$. Verify every `#### Theme` / `#### Tema` block contains at least 2 blockquote verbatims.
- **Testable:** Count percentages in output derived from qualitative $N < 30$, and count themes with $<2$ verbatims. If either count $> 0$, block. Yes/no.

---

## Article 5 — Minimum Sample Size & Assumption Gate for Parametric Tests

### Rule
Parametric tests require $N \ge 30$ per group/cell AND satisfaction of distributional assumptions (Shapiro-Wilk normality $p \ge 0.05$ for $n \le 5000$, skewness within $[-2, +2]$, Levene homoscedasticity). Specifically:
- **Independent or paired t-test**: $N \ge 30$ per group and normal/symmetric distribution
- **ANOVA** (one-way, factorial): $N \ge 30$ per cell and homogeneous variance
- **Pearson's $r$** (linear correlation): $N \ge 30$ total, interval/ratio scale, linear relationship
- **Linear regression**: $N \ge 30$ total, with $\ge 10$ observations per predictor and VIF $< 5$ (`r008`)

When group sizes fall below $N = 30$, skewness exceeds $\pm 2$ (`r002`), or variables are ordinal/Likert scales ($<7$ points, `r007`), the Statistician MUST use non-parametric equivalents and report Median + IQR / MAD alongside Mean + SD:
- **Mann-Whitney U test** (instead of independent t-test)
- **Wilcoxon signed-rank test** (instead of paired t-test)
- **Kruskal-Wallis H test** (instead of one-way ANOVA)
- **Spearman's $\rho$** (instead of or paired with Pearson's $r$ via **Dual Correlation**)
- **Fisher's Exact Test** (instead of $\chi^2$ when any expected cell count $E_{ij} < 5$, `r014`)

### Justification
Parametric tests assume normality of the sampling distribution — an assumption that the Central Limit Theorem only guarantees at $N \ge 30$ for reasonably symmetric data. Below this threshold or on skewed/ordinal scales, $p$-values and means from parametric tests are distorted by outliers. Non-parametric tests and robust estimators (Median, IQR, MAD) maintain valid Type I error rates regardless of distribution shape.

### Violation Consequence
If a parametric test result is reported alone on a sample where $N < 30$ per group, or $\chi^2$ is used where $E_{ij} < 5$ in a 2×2 table without Fisher's exact correction, the Critic blocks delivery and forces the non-parametric alternative.

### Detection Method / Computation
- **Detection:** For every reported parametric test statistic ($t$, $F$, Pearson's $r$), verify the associated $N$ per group is $\ge 30$ and skewness is within $[-2, +2]$.
- **Testable:** Count parametric-only test results with $N < 30$ per group. If count $> 0$, block. Yes/no.

---

## Article 6 — Data Quality Gates

### 6a. Straight-Lining Detection
- **Rule:** $\ge 80\%$ identical consecutive responses on a Likert-scale block (minimum 5 items) from a single respondent $\rightarrow$ flag as potentially inattentive. The Statistician computes the straight-lining rate and reports it in the Data Quality section.
- **Violation Consequence:** The Critic reports: number and percentage of straight-lining respondents detected, variables affected, and whether excluding them changes any headline metric by $> 2.0$ percentage points (or $> 0.20$ scale points). If the impact exceeds $2.0\text{pp}$, the output must include both with/without figures.

### 6b. Percentage Sum & Base Validation
- **Rule:** All percentage columns across mutually exclusive single-choice (`RU`) categories MUST sum to $100.0\%$ ($\pm 0.5\%$ rounding tolerance) over the **Valid Base** ($n_{\text{valid}}$). Mutually exclusive categories include: NPS segments ($\text{Promoters} + \text{Passives} + \text{Detractors} = 100\%$), single-select survey responses, and exhaustive segment partitions. For Multiple-Response (`RM`) questions, percentages are computed over **Total Base** ($N_{\text{total}}$) and the table footer MUST explicitly state: `"Multiple Response — column sum exceeds 100% (Base = N respondents)"`.
- **Violation Consequence:** Any single-select percentage sum outside $99.5\%$–$100.5\%$ or any unlabelled `RM` base is blocked by the Critic until reconciled.

### 6c. Missing Data Threshold
- **Rule:** Any variable with $>10.0\%$ missing responses ($1 - n_{\text{valid}}/N_{\text{total}}$) must be flagged with: variable name, exact missingness rate ($\%$ to 1 decimal), and an assessment of potential bias direction (MCAR, MAR, or MNAR — comparing demographics of responders vs. non-responders when available). For variables with $>20.0\%$ missing, append mandatory caveat: `"findings involving this variable should be treated as provisional"` and exclude from claims of population representativeness (`>30%` missing triggers exclusion evaluation per `r010`).
- **Violation Consequence:** The Critic blocks delivery of any output containing claims derived from a variable with $>10\%$ missing data that lacks the mandatory missingness disclosure.

---

## Article 7 — Survey Governance: Schema Mapping, Explicit Weights & Branching Overlap

### 7a. Clean Schema Governance (`survey_governance.md`)
- **Rule:** Never use raw, multi-word survey question strings as analytical column identifiers in scripts or models. Map raw headers to semantic `snake_case` keys in `column_mapping.json` (`{"snake_case_id": "Original Question Text"}`), and render both or the human-readable question label in user-facing tables and charts.

### 7b. Explicit Weight Handling (`explicit_weight_handling.md`)
- **Rule:** Scripts must never silently assume unweighted data. If a dataset lacks a weighting column, initialize `weight = 1.0` explicitly; if population universe targets are provided, compute sample weights via **Raking (IPF)** (`scripts/weighting.py`) and verify that $\sum w_i$ matches target $N$. All aggregations (frequencies, means, correlations, crosstabs) must operate through weighted estimators.

### 7c. Survey Branching Overlap Validation (`survey_branching_validation.md`)
- **Rule:** Before computing any bivariate crosstab, correlation, or co-occurrence matrix between Variable A and Variable B, validate the **Branching Overlap** $N_{A \cap B}$. If $N_{A \cap B} = 0$ (a `0x0` intersection), halt the cross immediately and report: `"Zero sample overlap (N=0): Variables A and B sit on mutually exclusive survey branching/skip logic."`

---

## Article 8 — Print-Ready Multi-School HTML Deliverable Standard (Default: Edward Tufte)

### Rule
The primary publication deliverable of Data-Pro-Skill (`/dps-export`) is a self-contained **Print-Ready HTML** report (`final_report.html`) styled in the project's locked **Data Design School** (`tufte` [Edward Tufte — Default], `few` [Stephen Few], `knaflic` [Cole Knaflic / Storytelling with Data], `swiss` [Swiss Grid / Jacques Bertin], or `editorial` [The Economist / FT Editorial] — see [`references/design-schools.md`](references/design-schools.md)) alongside its clean source Markdown (`final_report.md`). External PDF compilation toolchains (LaTeX, Quarto, Pandoc PDF) are NOT required or targeted; instead, `final_report.html` MUST be engineered to print directly to PDF (`Ctrl+P` / `Save as PDF` / Chromium print) with publication-grade fidelity:
1. **Multi-School Screen & Print Typography (`references/styles/{tufte,few,knaflic,swiss,editorial}.css`)**:
   - **`tufte` (Default)**: Palatino/Georgia serif body prose, Gill/Helvetica sans-serif tables, `#fffff8` ivory background on screen and `#ffffff` in `@media print`, 58%/36% asymmetric grid with floating `<aside class="margin-note">` sidenotes, and **Booktabs tables** (zero vertical gridlines, `tabular-nums` alignment).
   - **`few` (Stephen Few)**: Humanist sans-serif (`Inter`), `#f8fafc` 100% full-width perceptual BI grid, compact perceptual tables, and inline diagnostic callout strips.
   - **`knaflic` (Storytelling with Data)**: Decluttered `#ffffff` executive narrative, muted grey context (`#cbd5e1`) + single bold focal accent (`#1e40af` / `#ea580c`), Action-Title banners, and `💡 KEY TAKEAWAY` callout cards.
   - **`swiss` (Swiss Grid / Bertin)**: Exposed `1.5px`/`4px` solid `#0a0a0a` architectural modular grid on `#f5f5f0`, Neo-Grotesque sans-serif + monospace indices, and high-contrast retinal tables.
   - **`editorial` (The Economist / FT)**: Warm `#fcf8f2` newsprint, signature `6px solid #e3120b` crimson top bar & section tags, Kicker + Headline + Standfirst hierarchy, and editorial sidebar briefs.
2. **Self-Contained School-Authentic Vector Visualizations (`scripts/tufte_viz.py` & `scripts/tufte_html.py`)**: All charts (Tufte Cleveland dot plots with 95% CI whiskers, Few Bullet Graphs with qualitative bands & target markers, Knaflic preattentive grey/focal horizontal bars, Swiss/Bertin retinal lollipops, Economist/FT editorial lollipop range charts, diverging Likert/NPS bars, $\chi^2$ residual heatmaps, Priority Matrices, sparklines, and compiled Mermaid `xychart-beta` / `pie` charts) must be embedded directly as inline `<svg>` elements — zero broken external image links, zero external JS runtime required to print.
3. **Standard Print-to-PDF Running Headers, Footers & Pagination (`Print Frame`)**:
   - Must include W3C `@page` rules (`size: A4 portrait`, page margins, `@top-left`, `@top-right`, `@bottom-left`, `@bottom-right`) AND a repeating HTML `<table class="print-frame">` (`<thead>` header-space + `<tfoot>` footer-space) paired with `position: fixed` `<header class="print-running-header">` and `<footer class="print-running-footer">` in `@media print`.
   - Every printed PDF page displays the **Running Header** (Project Name, Framework, Sample Size $N$, 95% CI, Date) and **Running Footer** (Data-Pro-Skill Constitution Audit Stamp, Active Data Design School Standard, Print Date).
   - Must enforce `break-inside: avoid; page-break-inside: avoid` on `table`, `figure`, `.chart-container`, `.margin-note`, and `break-after: avoid` on `h1, h2, h3, h4` so tables, charts, and headings never split awkwardly across page boundaries.

### Violation Consequence
Any exported HTML report that uses boxed vertical-grid tables, leaves raw YAML frontmatter or unrendered Mermaid code blocks in the visual body, relies on external image files that can break, or lacks `@media print` / `@page` running header and footer structures is blocked by the Critic.

---

*All 8 articles are enforced by the Critic agent during Stage 2 of the DPS invisible agent loop. Violations block output delivery to the Tufte Designer. Each article defines a mechanically testable yes/no check.*
