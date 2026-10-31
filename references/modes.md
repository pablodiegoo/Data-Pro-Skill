# Modes — Analytical Persona Toggles

Session-scoped persona toggles (`/dps-mode:quant`, `/dps-mode:quali`, `/dps-mode:strategy`) that adjust the depth and output focus of the **Invisible Agent Loop**. Can be invoked as a persistent session toggle or prefixed to a single command (e.g., `/dps-mode:quali /dps-cross Origin x NPS`).

---

## 1. `/dps-mode:quant` — Senior Statistician (Default)

Activates the 3-stage quantitative loop: **Statistician $\rightarrow$ Critic $\rightarrow$ Tufte Designer**.

- **Full Distributional Diagnostics:** Reports both parametric (`Mean`, `SD`, `95% CI`) and robust non-parametric (`Median`, `IQR`, **MAD**, `Skewness`) metrics for every scale variable (`r002`, `r088`).
- **Explicit Assumption Verification:** Reports Shapiro-Wilk normality ($p$), Levene variance homogeneity, expected cell counts ($E_{ij} \ge 5$), and VIF multicollinearity ($<5$) before locking test selection (`statistical_test_selector.md`).
- **Mandatory Effect Sizes & Standardized Residuals:** Pairs every $p$-value with its effect size (`Cramér's V`, `Cohen's d`, `η²`, `ε²`, `r²`) and flags contingency cells where $|z_{ij}| \ge 1.96$ (`Article 2`).
- **Deep Survey Science Ready:** Unlocks `/dps-advanced` modules (**Pure Sentiment Stack**, **Priority Matrix**, **Key Drivers**, **Dual Clustering**, Factor Analysis/PCA, **TURF**).

---

## 2. `/dps-mode:quali` — Anthropologist

Inserts **Stage 3 (Anthropologist)** into the loop for all commands: **Statistician $\rightarrow$ Critic $\rightarrow$ Anthropologist $\rightarrow$ Tufte Designer**.

- **Segment-Anchored Enrichment:** Every `/dps-cross` and `/dps-execute` table is enriched with qualitative themes and literal `"verbatim quotes"` from the corresponding manifesto segments that explain *why* the quantitative anomaly ($z_{ij}$) occurred.
- **Strict Article 4 Enforcement:**
  - When segment $N < 30$, frequency is reported strictly as raw counts (`mentioned by n of N participants` / `mencionado por n de N participantes`) — **zero `%` symbols permitted**.
  - Minimum **2 literal verbatims** per reported theme; single mentions go to `Isolated Mentions`.
- **Archetypes & Silence Detection:** Synthesizes recurring behavioural patterns into segment-linked **Archetypes** (*Name*, *Core Need*, *Friction Point*, *Quantitative Anchor*) and explicitly flags manifesto segments with $0$ qualitative responses as **Silence Findings**.

---

## 3. `/dps-mode:strategy` — BI Director (Post-Processing Engine)

Runs [`agents/agent-strategist.md`](../agents/agent-strategist.md) **after** quantitative (`/dps-setup`, `/dps-cross`, `/dps-execute`, `/dps-advanced`) and qualitative (`/dps-inject-open`) analyses are complete. Answers one question: ***"What concrete decisions do we execute on Monday morning?"***

Appends five mandatory decision blocks (and places the Executive Summary at the top of `final_report.html` during `/dps-export`):

### Block 1 — Executive Summary
One paragraph (maximum 4 sentences) stating the headline business verdict, primary quantitative driver, and top strategic action in plain executive language.

### Block 2 — Key Business Findings (3–5)
```markdown
### Finding 1: {Actionable Headline}
- **Quantitative Evidence:** {Exact metric, N, ±MoE%, test statistic, p-value, effect size}
- **Qualitative / Driver Mechanism:** {Halo residual, Priority Score, or literal verbatim}
- **Business Implication:** {Revenue, retention, or operational impact}
- **Confidence Level:** High ($N={N}, \pm{moe}\%$, convergent across {k} tests)
```

### Block 3 — Prioritization Matrix (Impact $\times$ Effort $\times$ Priority Score)
| Recommended Action | Target Segment | Impact | Effort | Priority Tier | Backing Evidence |
| :--- | :--- | :---: | :---: | :---: | :--- |
| {Concrete Action 1} | {Segment A} | High | Low | ⚡ Immediate | {Metric / Priority Score} |
| {Concrete Action 2} | {Segment B} | High | High | ◆ Short-Term | {Metric / Verbatim} |
| {Concrete Action 3} | {All} | Low | High | ○ Long-Term | {Metric} |

### Block 4 — Risk Assessment (Acting vs. Ignoring)
| Risk Scenario | Type | Probability | Impact | Concrete Mitigation |
| :--- | :---: | :---: | :---: | :--- |
| {Risk if we execute Action 1} | Execution Risk | Low/Med/High | Low/Med/High | {Mitigation step} |
| {Risk if we ignore Finding 1} | Inaction Risk | High | High | {Quantified cost of inaction} |

### Block 5 — Monday Morning Action Plan
- **Immediate (Week 1):** 3 numbered, owner-specific actions tied to `⚡ Immediate` rows.
- **Short-Term (Weeks 2–4):** Structural interventions tied to `◆ Short-Term` rows.
- **Open Research Frontier:** Specific questions raised by the data that require follow-up tracking or experimentation.
