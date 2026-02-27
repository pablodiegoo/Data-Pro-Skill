# Statistical Test Selector

A decision framework for choosing the right statistical test based on research goal, variable types, and data assumptions. Derived from Dr. Samira Hosseini's flowchart.

## Decision Tree

```mermaid
flowchart TD
    START(["What type of analysis?"])
    GOAL{"WHAT IS YOUR<br/>RESEARCH GOAL?"}

    START --> GOAL

    %% ── Branch 1: Find Relationships ──
    GOAL -->|Find Relationships| VAR_TYPE{"What type<br/>of variables?"}

    VAR_TYPE -->|Both Continuous| LINEAR{"Is relationship<br/>linear?"}
    LINEAR -->|Yes| PEARSON["Pearson Correlation<br/><code>correlation_pearson</code>"]
    LINEAR -->|No| SPEARMAN["Spearman Correlation<br/><code>correlation_spearman</code>"]

    VAR_TYPE -->|One Categorical| PBIS["Point-Biserial<br/><code>point_biserial</code>"]
    VAR_TYPE -->|Both Categorical| CHI["Chi-Square Test<br/><code>chi_square</code>"]

    %% ── Branch 2: Compare Groups ──
    GOAL -->|Compare Groups| N_GROUPS{"How many<br/>groups?"}

    N_GROUPS -->|Two Groups| NORM_2{"Is data<br/>normal?"}
    NORM_2 -->|Yes| TTEST["T-Test<br/><code>ttest_ind</code>"]
    NORM_2 -->|No| MANN["Mann-Whitney U<br/><code>mann_whitney</code>"]

    N_GROUPS -->|Three+ Groups| NORM_3{"Is data<br/>normal?"}
    NORM_3 -->|Yes| ANOVA["ANOVA<br/><code>anova_oneway</code>"]
    NORM_3 -->|No| KRUSKAL["Kruskal-Wallis<br/><code>kruskal_wallis</code>"]

    %% ── Branch 3: Predict Outcomes ──
    GOAL -->|Predict Outcomes| OUTCOME{"What type<br/>of outcome?"}

    OUTCOME -->|Continuous| PREDICTORS{"How many<br/>predictors?"}
    PREDICTORS -->|One| SLR["Simple Linear<br/>Regression"]
    PREDICTORS -->|Multiple| MLR["Multiple<br/>Regression"]

    OUTCOME -->|Categorical| N_CAT{"How many<br/>categories?"}
    N_CAT -->|Two| LOGISTIC["Logistic<br/>Regression"]
    N_CAT -->|Multiple| MULTINOMIAL["Multinomial<br/>Regression<br/><code>multinomial_logistic</code>"]

    %% ── Styling ──
    classDef goal fill:#0d7377,color:#fff,stroke:none,font-weight:bold
    classDef decision fill:#0d7377,color:#fff,stroke:none
    classDef test fill:#f0a500,color:#000,stroke:none,font-weight:bold
    classDef start fill:#e0e0e0,color:#333,stroke:none

    class GOAL goal
    class VAR_TYPE,LINEAR,N_GROUPS,NORM_2,NORM_3,OUTCOME,PREDICTORS,N_CAT decision
    class PEARSON,SPEARMAN,PBIS,CHI,TTEST,MANN,ANOVA,KRUSKAL,SLR,MLR,LOGISTIC,MULTINOMIAL test
    class START start
```

## Quick Reference Table

| Research Goal | Variables / Conditions | Test | Snippet ID | Parametric? |
|---|---|---|---|---|
| **Find Relationships** | Both continuous + linear | Pearson Correlation | `correlation_pearson` | Yes |
| | Both continuous + non-linear | Spearman Correlation | `correlation_spearman` | No |
| | 1 categorical + 1 continuous | Point-Biserial Correlation | `point_biserial` | Yes |
| | Both categorical | Chi-Square Test | `chi_square` | No |
| **Compare Groups** | 2 groups + normal data | Independent T-Test | `ttest_ind` | Yes |
| | 2 groups + non-normal data | Mann-Whitney U Test | `mann_whitney` | No |
| | 3+ groups + normal data | One-Way ANOVA | `anova_oneway` | Yes |
| | 3+ groups + non-normal data | Kruskal-Wallis H Test | `kruskal_wallis` | No |
| **Predict Outcomes** | 1 predictor → continuous outcome | Simple Linear Regression | — | Yes |
| | Multiple predictors → continuous outcome | Multiple Regression | — | Yes |
| | Predictors → binary outcome | Logistic Regression | — | Yes |
| | Predictors → multi-class outcome | Multinomial Regression | `multinomial_logistic` | Yes |

## Pre-Test Assumptions Checklist

Before selecting a test, verify these assumptions:

| Check | How to Test | Snippet ID |
|---|---|---|
| **Normality** | Shapiro-Wilk (n ≤ 5000) | `normality_test` |
| **Linearity** | Scatter plot or partial residual plot | `partial_residual_plot` |
| **Homoscedasticity** | Levene's test or residual plot | — |
| **Sample size** | n ≥ 30 per group (CLT) for parametric | — |
| **Independence** | Study design (no repeated measures) | — |

> [!TIP]
> When in doubt between parametric and non-parametric: if n < 30 per group or Shapiro-Wilk p < 0.05, prefer the non-parametric alternative. Non-parametric tests sacrifice only a small amount of power when assumptions are met, but are far more robust when they are not.

## Decision Heuristics

1. **Goal first**: Always start by classifying your research question into one of the three branches.
2. **Variable types second**: Count how many variables and what types (continuous, ordinal, nominal).
3. **Assumptions third**: Only after selecting a candidate test, verify its assumptions.
4. **Effect size always**: Statistical significance alone is insufficient. Always report effect sizes (Cohen's d, Cramér's V, η², R²).

> [!IMPORTANT]
> **Ordinal data** (Likert scales, rankings): Treat as non-parametric unless the scale has ≥ 7 points and the distribution is approximately symmetric. Use Spearman over Pearson, and Mann-Whitney/Kruskal-Wallis over T-Test/ANOVA.

## Source Attribution

- **Original flowchart**: Dr. Samira Hosseini — "Statistical Analysis Methods"
- **Adapted for**: Data-Pro-Skill `survey-analytics` reference library
- **Adaptation date**: 2026-02-27

---

> [!NOTE]
> Last updated: 2026-02-27
