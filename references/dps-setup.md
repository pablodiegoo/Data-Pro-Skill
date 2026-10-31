# `/dps-setup` — Quantitative Manifesto, Data Design School Selection & Analytical Spine

Generates the **Analytical Spine** (`00_project_manifest.md` / `setup_report.md`, `setup_manifest.json`, `00_profile.json`, `design_school.json`, `setup_segments.csv`, and `column_mapping.json`) that anchors all subsequent analysis and locks the user's chosen **Data Design School**. No downstream command may contradict metrics, segments, or design school established here.

---

## 1. Pipeline

```
Raw Data (.csv/.xlsx/.ods/.parquet) + [config.json / clarify_notes.md / --school]
    → scripts/quant_analyzer.py (and scripts/design_schools.py)
    → setup_manifest.json + 00_profile.json + design_school.json + column_mapping.json + setup_segments.csv + setup_report.md
```

---

## 2. Execution Steps

0. **Select Data Design School (`design-schools.md`):**
   - If the user has not already locked a **Data Design School** during `/dps-grill` (`clarify_notes.md`), in `.dps/config.json`, or via `--school <id>`, **present the 5 canonical Data Design Schools and let the user pick one on setup** (defaulting to `tufte` if accepted or run in non-interactive batch mode):
     1. **`tufte` — Edward Tufte *(Default)***: Ivory `#fffff8`, Palatino serif, 58%/36% floating right **Margin Notes**, **Booktabs Tables**, and Cleveland dot plots with 95% CI whiskers. Best for academic, scientific, and public-policy reports.
     2. **`few` — Stephen Few**: Full-width perceptual BI grid (`#f8fafc`), Inter/Source Sans, **Bullet Graphs** (qualitative performance bands + target markers + 95% CI), high-density tables, and inline `PERCEPTUAL DIAGNOSTIC` callouts. Best for operational BI and KPI reviews.
     3. **`knaflic` — Cole Nussbaumer Knaflic (*Storytelling with Data*)**: Decluttered white canvas (`#ffffff`), context pushed to muted grey (`#cbd5e1`) with **one bold preattentive focal color** (`#1e40af` / `#ea580c`), **Action-Title Banners**, and `💡 KEY TAKEAWAY` cards. Best for C-level executive decks and Monday-morning action plans.
     4. **`swiss` — Swiss Grid & Jacques Bertin**: Exposed architectural modular grid (`1.5px`/`4px` `#0a0a0a`), Neo-Grotesque typography + monospace indices, and **Bertin Retinal Lollipops & Matrices** (Vermilion `#e63946` & Cobalt `#1d3557`). Best for design-forward manifestos and urban/multivariate studies.
     5. **`editorial` — The Economist / FT Editorial**: Warm newsprint (`#fcf8f2`), signature **`6px` crimson top bar (`#e3120b`)**, **Kicker + Headline + Standfirst** hierarchy, editorial lollipop range charts, and `EDITORIAL BRIEF` sidebars. Best for market research publications and public polling.
1. **Ingest & Map Schema (`Article 7a`, `survey_governance.md`):**
   - Read the dataset (`.csv`, `.xlsx`, `.ods`, `.parquet`, or pasted table).
   - Map every raw question header to a semantic `snake_case` identifier and persist to `.dps/outputs/setup/column_mapping.json` (`{"snake_case_id": "Original Question Text"}`).
2. **Initialize or Rake Weights (`Article 7b`, `explicit_weight_handling.md`):**
   - If population universe targets were provided during **Data Grilling**, execute `scripts/weighting.py` (**Raking / IPF**) and verify $\sum w_i = N_{\text{target}}$.
   - Otherwise, initialize an explicit `weight = 1.0` column so all downstream operators remain weight-aware.
3. **Run Deterministic Setup & Quality Gate Engine (Locking the Chosen School):**
   ```bash
   python3 .dps/scripts/quant_analyzer.py <data_file> [config.json] --school <tufte|few|knaflic|swiss|editorial> -o .dps/outputs/setup/
   ```
   *(Or pass `--pick-school` to launch the interactive terminal selector during setup.)*
4. **Execute Invisible Agent Loop (Statistician $\rightarrow$ Critic $\rightarrow$ Designer):**
   - **Statistician:** Computes total sample size $N_{\text{total}}$, global 95% CI Margin of Error, **Valid Base** ($n_{\text{valid}}$) per variable, segment distributions with `±MoE% (95% CI)` (`Article 1`), parametric (Mean, SD) and robust non-parametric metrics (Median, IQR, **MAD** when $|\text{skew}| > 2$ per `r002`), Top-2-Box / Bottom-2-Box (`r016`), and NPS (`Promoters [9–10] - Detractors [0–6]`, `r015`).
   - **Critic:** Enforces **Article 6 Data Quality Gates**:
     - **6a (Straight-Lining):** Flags respondents with $\ge 80\%$ identical consecutive responses on Likert batteries ($\ge 5$ items) and reports sensitivity delta ($>2.0\text{pp}$ impact requires reporting both with and without straight-liners).
     - **6b (Percentage Sum Validation):** Verifies mutually exclusive `RU` categories sum to $100.0\% \pm 0.5\%$ over **Valid Base**, and verifies `RM` multiple-response groups disclose **Total Base**.
     - **6c (Missingness Gate):** Flags any variable with $>10.0\%$ missingness (with MCAR/MAR/MNAR bias direction assessment) and marks variables with $>20.0\%$ missingness as provisional.
   - **Designer:** Renders `setup_report.md` and `00_project_manifest.md` in the chosen **Data Design School** (`tufte` default, `few`, `knaflic`, `swiss`, or `editorial`).

---

## 3. Output Format (`setup_report.md` / `00_project_manifest.md`)

```markdown
---
project: "{Project Name}"
framework: "Data-Pro-Skill v2.1 ({School Short Name} Edition)"
design_school: "{tufte|few|knaflic|swiss|editorial}"
design_school_name: "{Full School Name}"
sample_size: {N}
global_moe_95ci: "±{moe}%"
has_weight_column: {true|false}
metrics_tracked: [{metric_1}, {metric_2}]
segments: [{segment_1}, {segment_2}]
---

# {Project Name} — Quantitative Manifesto

> **Margin Note:** This document anchors the numerical context (**Analytical Spine**). Total sample $N = {N}$ (global 95% CI MoE = $\pm{moe}\%$). Visual and typographic deliverables are locked to the **{Full School Name}** (`--school {school}`). No subsequent analysis may contradict metrics established here.

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

- `--school <tufte|few|knaflic|swiss|editorial>`: Lock the project's **Data Design School** (`tufte` default).
- `--pick-school`: Interactively prompt the user to choose one of the 5 **Data Design Schools** during setup.
- `--list-schools`: Print the 5 **Data Design Schools** comparison table and exit.
- `--profile`: Run **Fact Reconnaissance** only (outputs `00_profile.json` and `column_mapping.json` for `/dps-grill`).
- `--json-only`: Output only `setup_manifest.json` and `00_profile.json`.
- **Completion Criterion:** `setup_manifest.json`, `00_profile.json`, `design_school.json`, `column_mapping.json`, `setup_segments.csv`, and `setup_report.md` exist in `.dps/outputs/setup/`, the user's chosen **Data Design School** is locked, every variable has its own distribution block, and all **Article 1** and **Article 6** checks pass.
