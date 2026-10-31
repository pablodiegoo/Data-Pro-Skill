# `/dps-advanced` — Deep Survey Science & Multivariate Analytics

Executes the advanced statistical, psychometric, causal, and segmentation methodologies housed in [`references/analysis/`](analysis/). Triggered when **Data Grilling** (Branch 5) or the analyst calls for drivers, bias removal, priority matrices, latent constructs, clustering, or reach optimization.

---

## 1. Pipeline

```
Data + Target Outcome + [column_mapping.json]
    → scripts/advanced_analytics_generator.py + scripts/survey_pca.py + scripts/turf_analysis.py + scripts/weighting.py
    → .dps/outputs/advanced/advanced_report.md + advanced_metrics.json + advanced_analytics.ipynb
```

```bash
python3 .dps/scripts/advanced_analytics_generator.py <data_file> <target_col> .dps/outputs/advanced/advanced_analytics.ipynb --report-dir .dps/outputs/advanced/
```

---

## 2. The Six Deep Survey Science Modules

### Module A — The Pure Sentiment Stack: Ipsative Centering & Halo Removal
**Disclosed References:** [`references/analysis/halo_removal.md`](analysis/halo_removal.md), [`references/analysis/new_methodologies.md`](analysis/new_methodologies.md), [`references/analysis/science.md`](analysis/science.md)

Survey batteries suffer from **Halo Effect** (overall brand/event affection inflating all item scores) and respondent baseline bias ("harsh critics" vs. "easy graders").
1. **Ipsative Centering:** Subtract each respondent's personal mean across all $K$ rated items ($\bar{X}_i = \frac{1}{K}\sum_{k=1}^K X_{ik}$) from each item score: $I_{ij} = X_{ij} - \bar{X}_i$. Reveals within-person relative strengths ($>0$) and weaknesses ($<0$).
2. **Regression Halo Residual:** Regress each attribute $X_j$ on the respondent's personal mean $\bar{X}_i$ (or overall satisfaction score): $X_{ij} = \beta_0 + \beta_1 \bar{X}_i + \varepsilon_{ij}$. The mean residual $\bar{\varepsilon}_j$ isolates true operational performance stripped of the general halo filter.

### Module B — Priority Matrix & Pain Curves (Investment Allocation)
**Disclosed References:** [`references/analysis/priority_matrix.md`](analysis/priority_matrix.md), [`references/analysis/science.md`](analysis/science.md)

Crosses **Derived Importance** ($I_j$: standardized regression weight, Random Forest importance, or Spearman correlation $\rho_j$ with the target outcome) against **Performance** ($P_j$: mean score on scale $0..\text{Scale}_{\max}$).
1. **Priority Score Formula:**
   $$\text{Priority Score}_j = I_j \times (\text{Scale}_{\max} - P_j)$$
2. **Strategic Quadrants (split at median/mean Importance and Performance):**
   - **Q1 — Maximum Priority (Opportunity):** High Importance, Low Performance $\rightarrow$ immediate capital/operational fix.
   - **Q2 — Maintenance (Core Pillar):** High Importance, High Performance $\rightarrow$ protect standard.
   - **Q3 — Indifference (Low Priority):** Low Importance, Low Performance $\rightarrow$ monitor only.
   - **Q4 — Over-investment (Surplus):** Low Importance, High Performance $\rightarrow$ reallocate budget.
3. **Pain Curves (Crisis & Rejection Thresholds):** Plot each attribute score ($0..10$) against the probability of overall rejection/detraction ($\text{NPS} \le 6$ or churn) to locate the exact non-linear cliff where dissatisfaction triggers defection.

### Module C — Causal Drivers & Expectation Residual Segmentation
**Disclosed References:** [`references/analysis/causal.md`](analysis/causal.md), [`references/analysis/evaluation_and_diagnostics.md`](analysis/evaluation_and_diagnostics.md)

1. **Key Drivers Analysis:** Fit both Standardized Multiple Regression (checking VIF $< 5$ per `r008` and partial residuals per `evaluation_and_diagnostics.md`) and Random Forest Regressor to rank independent predictors of the target outcome.
2. **Expectation Residuals ($Y_i - \hat{Y}_i$):** Compare each respondent's actual outcome $Y_i$ against model-predicted $\hat{Y}_i$:
   - **Disappointed ($z_{\text{res}} < -1.0$):** Scoring significantly lower than their attribute ratings predict — exposes unmeasured friction.
   - **Aligned ($-1.0 \le z_{\text{res}} \le +1.0$):** Outcome explained by measured attributes.
   - **Delighted ($z_{\text{res}} > +1.0$):** Scoring higher than predicted — captures organic brand equity.

### Module D — Dual Correlation & Chi-Squared Residual Heatmapping
**Disclosed References:** [`references/analysis/new_methodologies.md`](analysis/new_methodologies.md)

1. **Dual Correlation Matrix:** Compute **Pearson's $r$** (linear) and **Spearman's $\rho$** (monotonic rank) side-by-side across all scale variables. Highlight pairs where $|\rho - r| > 0.10$ as non-linear saturation/threshold relationships.
2. **Chi-Squared Standardized Residuals:** For categorical crosses, compute $z_{ij} = (O_{ij} - E_{ij})/\sqrt{E_{ij}}$ and flag all cells with $|z_{ij}| \ge 1.96$ ($p < 0.05$) or $|z_{ij}| \ge 2.58$ ($p < 0.01$).

### Module E — Dual Clustering & Multi-Pass Factor Analysis / PCA
**Disclosed References:** [`references/analysis/multivariate.md`](analysis/multivariate.md), [`references/analysis/analytical_methodology_patterns.md`](analysis/analytical_methodology_patterns.md)

1. **Scale Reliability Gate (`r051`):** Compute **Cronbach's $\alpha$** on multi-item batteries before reduction ($\alpha \ge 0.70$ acceptable; $\alpha \ge 0.80$ strong).
2. **Multi-Pass PCA / Factor Analysis (`scripts/survey_pca.py`):** Standardize scales (`StandardScaler`), identify optimal components via Scree elbow / Kaiser criterion, and report factor loadings highlighting $|w| > 0.30$.
3. **Dual Clustering:**
   - **K-Means** (choosing $K \in [2..6]$ via maximum **Silhouette Score**) to partition respondents into actionable marketing personas.
   - **DBSCAN** (`eps`, `min_samples`) to isolate density-based natural clusters and flag noise/outlier respondents (`cluster = -1`).
   - **Gower Distance Agglomerative Clustering** when clustering mixed numeric + categorical variables (`Pattern 1` in `analytical_methodology_patterns.md`).

### Module F — TURF Optimization & Sample Raking
**Disclosed References:** [`references/analysis/multivariate.md`](analysis/multivariate.md), [`references/analysis/explicit_weight_handling.md`](analysis/explicit_weight_handling.md)

1. **TURF (`scripts/turf_analysis.py`):** On binary/multi-response (`RM`) sets, compute the incremental unduplicated reach curve for $k = 1..K_{\max}$ items to identify the minimum portfolio that maximizes unique audience reach.
2. **Sample Weighting / Raking (`scripts/weighting.py`):** Run Iterative Proportional Fitting (IPF) when sample marginals must be calibrated to census/universe proportions.

---

## 3. Output Format (`advanced_report.md`)

Render each active module as a self-explanatory **Booktabs Table** with an accompanying Tufte SVG visualization (`priority_matrix.svg`, `halo_residuals.svg`, `cluster_profiles.svg`) and a 1–3 sentence **Margin Note** translating the mathematical output into a concrete business decision.

---

## 4. Completion Criterion

`.dps/outputs/advanced/advanced_report.md`, `advanced_metrics.json`, and `advanced_analytics.ipynb` are generated; scale standardization and assumption checks (Cronbach's $\alpha$, VIF, Silhouette score) are explicitly reported; and all outputs pass the **Critic** audit.
