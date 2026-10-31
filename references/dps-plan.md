# `/dps-plan` — Hypothesis-Driven Analytical Plan

Maps every canonical segment, tracked outcome metric, and grilled stakeholder hypothesis to its optimal statistical test and effect size before execution. Consults [`references/analysis/statistical_test_selector.md`](analysis/statistical_test_selector.md) and [`references/analysis/reasoning_rules.csv`](analysis/reasoning_rules.csv).

---

## 1. Execution Steps

1. **Load Spine & Discovery Context:**
   - Read `.dps/outputs/setup/setup_manifest.json`, `00_profile.json`, and `setup_segments.csv`.
   - Read `.dps/outputs/clarify_notes.md` (if **Data Grilling** was executed).
   - If no manifesto exists, halt and output: `"Execute /dps-setup first to establish the Analytical Spine."`
2. **Evaluate Variable Pairs & Assumptions (`Statistician`):**
   - For each hypothesis and Segment $\times$ Metric combination, inspect:
     - **Research Goal:** *Compare Groups*, *Find Relationships*, or *Predict Outcomes*.
     - **Measurement Scales:** Nominal/categorical (`RU`/`RM`), ordinal/Likert ($<7$ pts vs $\ge 7$ pts), or continuous ratio/interval.
     - **Distributional & Sample Diagnostics:** Group sizes ($n \ge 30$ vs $n < 30$ per `Article 5`), skewness ($|\text{skew}| > 2$ per `r002`), expected cell counts ($E_{ij} \ge 5$ vs $< 5$ per `r014`), and **Branching Overlap** ($N_{X \cap Y} > 0$ per `Article 7c`).
3. **Select Statistical Test & Effect Size:**

| Comparison / Goal | Parametric Path ($n \ge 30$/group, normal) | Non-Parametric / Robust Path ($n < 30$, skewed, ordinal) | Mandatory Effect Size |
| :--- | :--- | :--- | :--- |
| **2 Categorical (`RU` $\times$ `RU`)** | Chi-Square ($\chi^2$) + **Standardized Residuals** ($z_{ij}$) | **Fisher's Exact Test** (when any $E_{ij} < 5$) | **Cramér's $V$** (or Odds Ratio) |
| **2 Groups $\times$ Continuous/Scale** | Independent Welch's $t$-test (or Paired $t$-test) | **Mann-Whitney $U$** (or Wilcoxon signed-rank) | **Cohen's $d$** / Rank-Biserial $r_{rb}$ |
| **3+ Groups $\times$ Continuous/Scale** | One-Way **ANOVA ($F$)** + Tukey HSD post-hoc | **Kruskal-Wallis $H$** + Dunn post-hoc | **$\eta^2$ (Eta-squared)** / $\epsilon^2$ |
| **2 Continuous / Likert Scales** | **Pearson's $r$** (linear) | **Spearman's $\rho$** (monotonic rank) — run **Dual Correlation** | **$r^2$** (shared variance) |
| **Multi-Attribute Battery ($\ge 4$ items)** | Linear Regression / Random Forest Key Drivers | **Pure Sentiment Stack** (**Ipsative** + **Halo Residual**) + **Priority Matrix** | Standardized $\beta$ / **Priority Score** |
| **Audience Segmentation** | **K-Means** (Silhouette $K$) + Factor Analysis / PCA | **DBSCAN** (outlier `-1` detection) / **Gower Distance** (mixed types) | Silhouette Score / Explained Variance % |
| **Multi-Response (`RM`) Reach** | — | **TURF** (Total Unduplicated Reach & Frequency) | Incremental Unduplicated Reach % |

4. **Render Advisory Checklist:** Output only the structured **Booktabs Table** and next-step pointer — zero introductory or closing fluff.

---

## 2. Output Format

```markdown
## Suggested Analytical Plan — {Project Name}

> **Margin Note:** Advisory test matrix anchored on `setup_manifest.json` ($N = {N}$). When $n < 30$ per cell or skewness exceeds $\pm 2.0$, non-parametric equivalents are locked per **Constitution Article 5**.

| # | Cross / Hypothesis | Var X (Base) | Var Y (Scale) | Selected Test | Effect Size & Diagnostics | Business Rationale |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | {Seg A} × {Outcome} | `{var_x}` ($k={k}, n_{\min}={n}$) | `{var_y}` (0–10 scale) | Kruskal-Wallis $H$ | $\epsilon^2$ + Median/IQR | {Why this decision matters} |
| 2 | {Seg B} × {Churn} | `{var_x}` ($2\times 2$) | `{var_y}` (Binary) | $\chi^2$ + Residuals $z_{ij}$ | Cramér's $V$ | {Why this decision matters} |
| 3 | Infra Battery → NPS | 12 rating items | `{nps_col}` | Priority Matrix + Halo Removal | Priority Score + $R^2$ | Isolate true operational drags |

**Next Step:** Run `/dps-cross [VarX] x [VarY]` for individual slices, `/dps-execute` to run all bivariate crosses autonomously, or `/dps-advanced` for multivariate drivers, Halo Removal, Priority Matrix, and clustering.
```

---

## 3. Completion Criterion

Every segment $\times$ metric pair from the manifesto and every hypothesis from **Data Grilling** is accounted for in the table with an explicit test, assumption justification, and effect size metric.
