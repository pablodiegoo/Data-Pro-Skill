# `/dps-execute` — Autonomous Multi-Cross Execution & Synthesis

Runs autonomous multi-cross quantitative analysis across the **Analytical Spine**, executing every candidate Segment $\times$ Metric cross through the **Invisible Agent Loop** and synthesizing findings ranked by **effect size**.

---

## 1. Execution Steps

1. **Verify Analytical Spine:**
   - Load `.dps/outputs/setup/setup_manifest.json` and `setup_segments.csv`.
   - If no manifesto exists, halt and output: `"Execute /dps-setup first to define segments and metrics."`
2. **Build Candidate Cross Matrix:**
   - If `/dps-plan` or `clarify_notes.md` exists, seed the queue with its prioritized crosses.
   - Combine with all Segment $\times$ Metric pairs from `setup_manifest.json`.
   - If candidate crosses exceed 15, prioritize by: (a) grilled stakeholder hypotheses, (b) largest valid intersection $N_{X \cap Y}$, and (c) highest between-segment variance. Log deferred crosses explicitly.
3. **Execute Batch Crosstab Pipeline:**
   - For each cross, run `scripts/crosstabs.py` and the full **Invisible Agent Loop** (Statistician $\rightarrow$ Critic $\rightarrow$ [Anthropologist if `/dps-mode:quali`] $\rightarrow$ Tufte Designer).
   - If a pair has zero **Branching Overlap** ($N_{X \cap Y} = 0$, `Article 7c`), record the structural skip-logic note rather than silently dropping it.
   - When $>5$ hypothesis tests run simultaneously (`Article 2`, `r031`), apply Benjamini-Hochberg FDR or Bonferroni adjustment alongside exact $p$-values.
4. **Synthesize by Effect Size (Convergent vs. Divergent Evidence):**
   - Rank all completed crosses by **effect size** magnitude (Cramér's $V$, Cohen's $d$, $\eta^2$, $\epsilon^2$, $|r|$) rather than raw $p$-value (`r030`, `r076`).
   - Identify **Convergent Evidence** (patterns reinforced across multiple independent segments/metrics) and surface **Divergent Tension** (where two crosses point in opposite directions — never hide contradictions).

---

## 2. Output Format

```markdown
---
project: "{Project Name}"
framework: "Data-Pro-Skill v2.1"
sample_size: {N}
crosses_executed: {K}
---

# {Project Name} — Autonomous Multi-Cross Synthesis

> **Margin Note:** Executed {K} hypothesis crosses across $N = {N}$ respondents (Benjamini-Hochberg FDR applied across {K} tests). Findings are ranked by practical **effect size**, separating structural business drivers from statistical noise.

## 1. Effect-Size Leaderboard (All Executed Crosses)

| Rank | Cross (`VarX × VarY`) | Valid $n$ | Test Statistic | Exact $p$ ($p_{\text{adj}}$) | Effect Size | Peak Anomaly / Direction |
| :---: | :--- | :---: | :--- | :---: | :---: | :--- |
| 1 | `{Seg1} × {Metric1}` | {n1} | $\chi^2(3) = 48.20$ | $p < 0.001$ | $V = 0.42$ (moderate) | `{Group A}` $z = +3.85^*$ |
| 2 | `{Seg2} × {Metric2}` | {n2} | $H(2) = 19.40$ | $p < 0.001$ | $\epsilon^2 = 0.18$ (moderate) | `{Group C}` Median = 6.0 vs 9.0 |
| 3 | `{Seg1} × {Metric3}` | {n3} | $U = 14210$ | $p = 0.214$ | $r_{rb} = 0.05$ (negligible) | No significant difference |

## 2. Detailed Crosstab Sections

### 2.1 {VarX} × {VarY} — {Headline Finding}
{Full Booktabs Table + Mermaid Chart + Margin Note per /dps-cross specification}

...

## 3. Synthesis of Convergent & Divergent Evidence

- **Primary Structural Driver ({Effect Size}):** {Finding backed by test statistic, N, and ±MoE%}.
- **Convergent Pattern:** {How Cross A and Cross B reinforce the same operational bottleneck}.
- **Divergent Tension / Null Falsifier:** {Where a stakeholder prior was falsified ($p \ge 0.05$) or where two segments diverge unexpectedly}.
```

---

## 3. Completion Criterion

All prioritized crosses are executed and saved under `.dps/outputs/cross/`, the Effect-Size Leaderboard ranks every test with exact $p$ and effect size, and both convergent and divergent findings are synthesized without violating any article of `constitution.md`.
