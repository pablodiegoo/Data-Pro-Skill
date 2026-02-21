# Reference: CRISP-DM for Academic Research (Thesis/Dissertation)

> Generic reference for any academic Data Science project.
> Adapted from the standard industry framework to meet academic rigor requirements.

---

## Philosophy

CRISP-DM is not a linear checklist — it is an **iterative cycle**. In academic research, 
it is common (and expected) to backtrack from *Evaluation* to *Data Preparation* when results fail. 
This iteration **is part of the scientific method**, not a failure.

---

## The 6 Phases & Checklists

### 1. Business/Research Understanding — "The Why"
**Deliverable:** Research Proposal / Introduction

- [ ] **Problem Definition:** What is the core issue? (e.g., "Sector selection fails in emerging markets")
- [ ] **Success Criteria:** Quantitative metric (e.g., "Sharpe > 1.0" or "Accuracy > Benchmark")
- [ ] **Situation Assessment:** Identify risks (Data availability), resources, and constraints (Timeline)
- [ ] **Project Plan:** Select tools (Python, SQL) and overarching methodology

### 2. Data Understanding — "The What"
**Deliverable:** Data Section / EDA Chapter

- [ ] **Data Collection:** APIs, scraping, or proprietary databases.
- [ ] **Data Description:** Volume, granularity, and observation window (Timeframe).
- [ ] **Exploratory Data Analysis (EDA):** Distributions, correlations, and initial patterns.
- [ ] **Quality Control:** Check for gaps (NaN), outliers, and stationarity (e.g., Unit root tests).

### 3. Data Preparation — "The How"
**Deliverable:** Methodology Section (80% of the actual effort)

- [ ] **Cleaning:** Handling NaNs, adjusting for corporate actions or splits.
- [ ] **Feature Engineering:** Returns, rolling volatility, Z-scores.
- [ ] **Transformation:** Normalization/Scaling — critical for distance-based algorithms (PCA/DBSCAN).
- [ ] **Reduction:** PCA to reduce noise and identify latent factors.

### 4. Modeling — "The Logic"
**Deliverable:** Preliminary Results (e.g., Clustering)

- [ ] **Technique Selection:** Justify the choice of algorithm (e.g., DBSCAN vs. K-Means).
- [ ] **Test Design:** Train/Test split or Walk-forward validation design.
- [ ] **Model Construction:** Execute logic and extract labels/groups.
- [ ] **Model Evaluation:** Are groups cohesive? (Silhouette Score). Do they make fundamental sense?
- [ ] **Iteration:** Tune hyperparameters until results are statistically robust.

### 5. Evaluation — "The Proof"
**Deliverable:** Final Results Chapter

- [ ] **Validation:** Run logic on out-of-sample data.
- [ ] **Robustness:** Include constraints (costs, slippage, lags).
- [ ] **Comparison:** Model vs. Benchmark (Baseline strategy).
- [ ] **Failure Analysis:** IF it failed, WHY? (e.g., "Correlation ≠ Cointegration") — this is a valid academic finding!

### 6. Deployment — "The Verdict"
**Deliverable:** Conclusion Chapter

- [ ] **Final Report:** Synthesize the complete narrative.
- [ ] **Recommendations:** Practical implications of the findings.
- [ ] **Limitations:** Liquidity issues, execution lag, or historical data bias.
- [ ] **Future Work:** Potential areas for further exploration.

---

## Mapping CRISP-DM → Thesis Chapters

| CRISP-DM Phase | Thesis Chapter | Content Focus |
| :--- | :--- | :--- |
| Business Understanding | 1. Introduction | Problem, Objectives, Justification |
| Data Understanding | 3. Data & Methods | Sources, EDA, Software Stack |
| Data Preparation | 3. Data & Methods | Pre-processing, PCA, Scaling |
| Modeling | 4. Results (Part I) | Initial findings, cluster/group composition |
| Evaluation | 4. Results (Part II) | Performance curves, Drawdown, Metrics table |
| Deployment | 5. Conclusion | Final verdict, practical implications |

---

## Common Pitfalls in Academic DS

1. **Data Leakage:** Scaling the entire dataset before splitting.
   - **Fix:** Fit the scaler on the Train set only; apply to Test.

2. **Parameter Overfitting:** Optimizing hyperparameters to maximize PnL.
   - **Fix:** Optimize for cluster quality (e.g., Giant Ratio, Silhouette) or statistical stability.

3. **Ignoring Null Results:** Believing a "failed" model is a failed thesis.
   - **Fix:** Explain the failure through known theories (e.g., Market Efficiency) — this is a contribution.

4. **Favorable Windows:** Choosing a timeframe that favors the hypothesis.
   - **Fix:** Use the longest period possible, including crisis events.
