# Data-Pro-Skill v2 — Analytical Constitution

> **Purpose:** This document defines the inegotiable statistical rigor rules of Data-Pro-Skill v2. It is read and enforced by the **Critic agent** during Stage 2 of the DPS invisible agent loop. Every analysis command (`/dps-setup`, `/dps-cross`, `/dps-inject-open`, `/dps-export`) triggers the Critic to audit output against all 6 articles below. Any violation blocks delivery to the Tufte Designer.

> **Enforcement:** All 6 articles are enforced by the Critic agent during Stage 2 of the DPS invisible agent loop. Violations block output delivery to the Tufte Designer. The Critic answers "is this violated?" with a yes/no decision on each article, per output, per command.

---

## Article 1 — Margin of Error Mandatory on All Sample-Based Claims

### Rule
Every percentage or proportion derived from a sample MUST be accompanied by its margin of error at the 95% confidence level. No sample-based claim may be presented as a bare percentage without its confidence interval.

**Formula:** MoE = z_crit × √(p(1−p)/n), where z_crit = 1.96 for 95% confidence, p = proportion (0 to 1), n = sample size.

Every reported percentage must appear as: `X% (±Y%, 95% CI)`, where Y is the computed margin of error.

### Justification
Point estimates without confidence intervals imply false precision. A reported "45% prefer Brand A" without MoE misleads the reader into believing certainty where none exists. The margin of error communicates the precision of the estimate given the sample size — without it, the reader cannot judge whether a difference between two percentages is real or noise.

### Violation Consequence
The Critic refuses to pass output to the Tufte Designer until margin of error is computed and displayed on every sample-based percentage claim. A bare percentage without `±Y%, 95% CI` is a hard block.

### Detection Method / Computation
- **Detection:** Scan output for any percentage not followed by `(±`, 95% CI notation. Also scan for "margin of error" in prose that is not accompanied by a numeric value.
- **Computation:** For each percentage p% with sample size n, compute MoE = 1.96 × √(p × (1-p) / n). Reject if MoE > 10% (flag as "wide confidence interval — treat finding as provisional").
- **Testable:** Every percentage in output either has MoE notation or the output is blocked. Yes/no.

---

## Article 2 — Statistical Significance Threshold (p < 0.05)

### Rule
All claims of difference, correlation, or effect between variables MUST report the p-value from the appropriate statistical test. A p-value ≥ 0.05 disallows language asserting "significant", "meaningful difference", "clear relationship", or any equivalent claim of reliable effect. When p ≥ 0.05, the output must state: "no statistically significant difference found (p = {value})".

Test statistics must be reported with degrees of freedom and sample size: `χ²(df, N=n) = {value}, p = {value}`.

### Justification
Without a significance threshold, any observed difference can be claimed as real, even when attributable to random chance. The p < 0.05 convention, while imperfect, is the most widely recognized guard against false positives in social science and market research. It forces the analysis to quantify uncertainty before making claims.

### Violation Consequence
The Critic downgrades unsupported significance claims and appends a mandatory caveat to any output that uses "significant" language without meeting p < 0.05. If the output asserts a relationship without reporting a test statistic and p-value, the Critic blocks delivery.

### Detection Method / Computation
- **Detection:** Scan output for the words "significant", "significant difference", "meaningful", "clear relationship", "correlated", "associated". Each instance MUST be accompanied by a test statistic and p-value.
- **Verification:** For each significance claim, verify that the reported p < 0.05. If p ≥ 0.05 is reported but language still claims significance, flag as contradiction.
- **Testable:** Count all significance-language assertions. Verify each has a test statistic and p-value. Reject if any assertion violates p < 0.05 threshold. Yes/no.

---

## Article 3 — Prohibition of Prose Fluff

### Rule
Output must go straight to the data. The first sentence after any heading must be a finding, a number, or a named entity — never throat-clearing. The following phrases and all their close variants are FORBIDDEN as paragraph openers or content fillers:

1. "It's important to note that..."
2. "Based on the data provided..."
3. "Interestingly..."
4. "It is worth mentioning..."
5. "One can observe that..."
6. "The data suggests that..."
7. "In conclusion..."
8. "As we can see..."

**Deletion Test:** If a sentence can be removed without losing a number, named entity, or finding, it is fluff. Delete it. A sentence qualifies as fluff if: (a) it contains no numeric value, (b) it contains no proper noun or named entity, (c) it contains no analytical finding that would change understanding of the data.

### Justification
Prose fluff adds words without adding information. It reduces data density — the ratio of meaningful content to total text. Edward Tufte's principle: "Maximize data-ink ratio" translates directly to prose: maximize information per word. Phrases like "It's important to note that..." occupy 6 words conveying zero information — the reader must scan past them to reach the actual finding.

### Violation Consequence
The Critic scans every output for these phrases before delivery. Any match returns the output to the Tufte Designer with fluff phrases highlighted. The Designer must remove or rewrite the offending sentences before the output can be delivered to the user.

### Detection Method / Computation
- **Detection:** Grep output for the 8 forbidden phrase patterns (case-insensitive). Also apply the Deletion Test to the first sentence of every paragraph: if it contains no numeric digit, no proper noun, and no finding-dependent clause, flag as potential fluff.
- **Testable:** Count matches of forbidden phrases in output. If count > 0, output is blocked. Yes/no.

---

## Article 4 — Prohibition of Percentages in Qualitative Samples (N < 30)

### Rule
When N < 30 for qualitative data (open-ended responses, interviews, focus groups, verbatim coding), NEVER report percentages. Quote verbatims directly. Note frequency as "mencionado por n de N participantes" without false precision. The output must not contain percentage symbols (%) applied to any qualitative sample where the denominator N < 30.

### Justification
A percentage computed from N < 30 creates an illusion of quantitative rigor where none exists. Reporting that "67% mentioned pricing" when N = 12 creates false precision — one respondent changes the percentage by 8.3 percentage points. Small samples cannot support percentage generalization; they support thematic identification and verbatim representation.

### Violation Consequence
The Critic flags any quantitative generalization from small qualitative samples as a hard block. Output containing a percentage applied to a qualitative sample with N < 30 cannot be delivered to the Tufte Designer until corrected.

### Detection Method / Computation
- **Detection:** Scan output for any statement of the form "X% of respondents mentioned Y" or "X% reported Z" where the associated N < 30. Also scan for percentage symbols in proximity to qualitative segment names or verbatim lists.
- **Verification:** For every percentage in output, trace its denominator N. If N < 30 and the data is qualitative (open-ended, interview, focus group), flag immediately.
- **Testable:** Count percentages in output derived from qualitative N < 30. If count > 0, block. Yes/no.

---

## Article 5 — Minimum Sample Size for Parametric Tests

### Rule
Parametric tests require N ≥ 30 per group. The following tests are restricted:
- **t-test** (independent or paired): N ≥ 30 per group
- **ANOVA** (one-way, factorial): N ≥ 30 per cell
- **Pearson's r** (correlation): N ≥ 30 total
- **Linear regression**: N ≥ 30 total, with ≥ 10 observations per predictor

When group sizes fall below these thresholds, the Statistician MUST use non-parametric equivalents:
- Mann-Whitney U test (instead of t-test)
- Kruskal-Wallis test (instead of one-way ANOVA)
- Spearman's ρ (instead of Pearson's r)

### Justification
Parametric tests assume normality of the sampling distribution — an assumption that the Central Limit Theorem only guarantees at N ≥ 30. Below this threshold, p-values from parametric tests are unreliable. Non-parametric tests make no distributional assumptions and maintain correct Type I error rates regardless of sample size.

### Violation Consequence
The Statistician must flag when parametric assumptions are violated in its internal report. The Critic enforces: if a parametric test result is reported on a sample where N < 30 per group, the Critic blocks delivery and recommends the appropriate non-parametric alternative with its test statistic.

### Detection Method / Computation
- **Detection:** For every reported test statistic (t-value, F-value, Pearson's r), verify the associated N per group is ≥ 30. For regression, verify total N ≥ 30.
- **Verification:** If N < 30 for a parametric test, validate that a non-parametric equivalent was used instead. If neither was used, flag.
- **Testable:** Count parametric test results with N < 30 per group. If count > 0, block. Yes/no.

---

## Article 6 — Data Quality Gates

### 6a. Straight-Lining Detection

**Rule:** ≥80% identical consecutive responses on a Likert-scale block (minimum 5 items) from a single respondent → flag as potentially inattentive. The Statistician computes the straight-lining rate per variable and reports it in the Data Quality section.

**Justification:** Straight-lining (selecting the same response for every item) indicates the respondent is not reading the questions. Including these responses inflates central tendency and deflates variance, biasing means toward the midpoint.

**Violation Consequence:** The Critic must report: number of straight-lining respondents detected, variables affected, and whether excluding them changes any substantive conclusion by more than 2 percentage points. If the impact exceeds 2pp, the output must include both with/without figures.

**Detection Method:** For each respondent's Likert block (≥5 items), count runs of identical consecutive values. If ≥80% of items share the same value, flag. Compute impact: recalculate key metrics excluding flagged respondents; report the difference.

### 6b. Percentage Sum Validation

**Rule:** All percentage columns across mutually exclusive categories MUST sum to 100% (±0.5% rounding tolerance). Any deviation beyond ±0.5% must be flagged. Mutually exclusive categories include: NPS segments (Promoters + Passives + Detractors = 100%), single-select survey responses (all options must sum to 100%), and any partition of a sample into non-overlapping groups.

**Justification:** A percentage sum deviating from 100% by more than rounding error indicates a counting error, a missing category, or respondents selecting multiple options where only one was allowed. The reader cannot trust proportions that don't sum correctly.

**Violation Consequence:** The Critic flags any percentage sum outside 99.5%–100.5%. The flagged variable must be reported with: the expected sum, the actual sum, and the discrepancy. The output must note which categories may be missing or double-counted.

**Detection Method:** For every set of mutually exclusive categories in a table or prose, sum the percentages. If sum < 99.5% or > 100.5%, flag. Report the difference and likely cause (missing category, rounding accumulation, double-counting).

### 6c. Missing Data Threshold

**Rule:** Any variable with >10% missing responses must be flagged. The Critic must report: the variable name, the missingness rate (%, to 1 decimal), and an assessment of potential bias direction — does the missingness likely skew the results upward, downward, or is the direction unknown?

For variables with >20% missing: the output must include a caveat that "findings involving this variable should be treated as provisional" and the variable must be excluded from any claim of representativeness.

**Justification:** Missing data >10% risks non-response bias — the respondents who skipped the question may differ systematically from those who answered. Without reporting missingness rates, the reader cannot assess whether conclusions apply to the full sample or only to those who chose to answer.

**Violation Consequence:** The Critic blocks delivery of any output containing claims derived from a variable with >10% missing data without the required missingness report. The missingness rate and bias assessment are mandatory for every flagged variable.

**Detection Method:** For each variable in the dataset, compute: missing_rate = (missing_count / total_N) × 100. If missing_rate > 10%, flag. Assess bias direction: compare demographics of respondents who answered vs. those who didn't (if available); otherwise report "direction unknown."

---

*All 6 articles are enforced by the Critic agent during Stage 2 of the DPS invisible agent loop. Violations block output delivery to the Tufte Designer. Each article defines a mechanically testable yes/no check — no subjective judgment required for enforcement.*
