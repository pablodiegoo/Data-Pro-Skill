# `/dps-setup` — Quantitative Manifesto & Analytical Spine

Generates the **Analytical Spine** (`00_project_manifest.md` / `setup_report.md`, `setup_manifest.json`, `00_profile.json`, `setup_segments.csv`, and `column_mapping.json`) that anchors all subsequent analysis. No downstream command may contradict metrics or segments established here.

---

## 1. Pipeline

```
Raw Data (.csv/.xlsx/.ods/.parquet) + [config.json / clarify_notes.md]
    → scripts/quant_analyzer.py
    → setup_manifest.json + 00_profile.json + column_mapping.json + setup_segments.csv + setup_report.md
```

---

## 2. Execution Steps

1. **Ingest & Map Schema (`Article 7a`, `survey_governance.md`):**
   - Read the dataset (`.csv`, `.xlsx`, `.ods`, `.parquet`, or pasted table).
   - Map every raw question header to a semantic `snake_case` identifier and persist to `.dps/outputs/setup/column_mapping.json` (`{"snake_case_id": "Original Question Text"}`).
2. **Initialize or Rake Weights (`Article 7b`, `explicit_weight_handling.md`):**
   - If population universe targets were provided during **Data Grilling**, execute `scripts/weighting.py` (**Raking / IPF**) and verify $\sum w_i = N_{\text{target}}$.
   - Otherwise, initialize an explicit `weight = 1.0` column so all downstream operators remain weight-aware.
3. **Run Deterministic Setup & Quality Gate Engine:**
   ```bash
   python3 .dps/scripts/quant_analyzer.py <data_file> [config.json] -o .dps/outputs/setup/
   ```
4. **Execute Invisible Agent Loop (Statistician $\rightarrow$ Critic $\rightarrow$ Tufte Designer):**
   - **Statistician:** Computes total sample size $N_{\text{total}}$, global 95% CI Margin of Error, **Valid Base** ($n_{\text{valid}}$) per variable, segment distributions with `±MoE% (95% CI)` (`Article 1`), parametric (Mean, SD) and robust non-parametric metrics (Median, IQR, **MAD** when $|\text{skew}| > 2$ per `r002`), Top-2-Box / Bottom-2-Box (`r016`), and NPS (`Promoters [9–10] - Detractors [0–6]`, `r015`).
   - **Critic:** Enforces **Article 6 Data Quality Gates**:
     - **6a (Straight-Lining):** Flags respondents with $\ge 80\%$ identical consecutive responses on Likert batteries ($\ge 5$ items) and reports sensitivity delta ($>2.0\text{pp}$ impact requires reporting both with and without straight-liners).
     - **6b (Percentage Sum Validation):** Verifies mutually exclusive `RU` categories sum to $100.0\% \pm 0.5\%$ over **Valid Base**, and verifies `RM` multiple-response groups disclose **Total Base**.
     - **6c (Missingness Gate):** Flags any variable with $>10.0\%$ missingness (with MCAR/MAR/MNAR bias direction assessment) and marks variables with $>20.0\%$ missingness as provisional.
   - **Tufte Designer:** Renders `setup_report.md` and `00_project_manifest.md` in zero-fluff Tufte style.

---

## 3. Output Format (`setup_report.md` / `00_project_manifest.md`)

```markdown
---
project: "{Project Name}"
framework: "Data-Pro-Skill v2.1"
sample_size: {N}
global_moe_95ci: "±{moe}%"
has_weight_column: {true|false}
metrics_tracked: [{metric_1}, {metric_2}]
segments: [{segment_1}, {segment_2}]
---

# {Project Name} — Quantitative Manifesto

> **Margin Note:** This document anchors the numerical context (**Analytical Spine**). Total sample $N = {N}$ (global 95% CI MoE = $\pm{moe}\%$). No subsequent analysis may contradict metrics established here.

## 1. Canonical Segment Matrix

| Segment | N | % (±MoE, 95% CI) | Core Metric | Diagnostic Finding |
| :--- | :---: | :---: | :---: | :--- |
| {Segment A} | {n_a} | {pct_a}% (±{moe_a}%, 95% CI) | {metric_a} | {sharp finding} |
| {Segment B} | {n_b} | {pct_b}% (±{moe_b}%, 95% CI) | {metric_b} | {sharp finding} |
| **Total Base** | **{N}** | **100.0%** | **{metric_total}** | **Baseline anchor** |

> **Margin Note:** {1–3 sentences explaining the business implication of the segment split — never repeating table cells.}

## 2. Variable Profile & Distribution Blocks

### Variable: {Original Question Label} (`{snake_case_id}`)

| Option / Scale | n | % (±MoE, 95% CI) | Summary Statistics |
| :--- | :---: | :---: | :--- |
| {Category 1} | {n_1} | {pct_1}% (±{moe_1}%) | Mean = {mean}, SD = {sd}, Median = {med}, IQR = {iqr} |
| **Valid Base** | **{n_valid}** | **100.0%** | **Missing: {n_miss} ({pct_miss}% of N={N})** |

> **Margin Note:** {Variable-specific insight, skewness/outlier note, or Top-2-Box / NPS benchmark.}

## 3. Data Quality & Constitution Audit (Article 6)

| Quality Gate | Status | Metric / Affected Variables | Constitutional Action |
| :--- | :---: | :--- | :--- |
| **6a. Straight-Lining** | {PASS/FLAG} | {count} respondents ({pct}%) across {k} Likert items | Max headline delta = {delta}pp ({action}) |
| **6b. Percentage Sums** | {PASS} | All {m} single-choice tables sum within 99.5%–100.5% | Validated |
| **6c. Missing Data (>10%)** | {PASS/FLAG} | {flagged_vars_summary} | {MCAR/MAR/MNAR bias note} |
```

---

## 4. Flags & Completion Criterion

- `--profile`: Run **Fact Reconnaissance** only (outputs `00_profile.json` and `column_mapping.json` for `/dps-grill`).
- `--json-only`: Output only `setup_manifest.json` and `00_profile.json`.
- **Completion Criterion:** `setup_manifest.json`, `00_profile.json`, `column_mapping.json`, `setup_segments.csv`, and `setup_report.md` exist in `.dps/outputs/setup/`, every variable has its own distribution block, and all **Article 1** and **Article 6** checks pass.
