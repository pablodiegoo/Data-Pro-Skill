# Project Evolution - v0.4.0

**Date**: 2026-02-24  
**Source Project(s)**: OS18 (Sebrae Churn)  
**Harvest Cycles**: 1  
**Total Items Absorbed**: 5 (plus a major architectural refactoring)

## Summary
Version 0.4.0 introduces a massive architectural overhaul of the Data-Pro-Skill engine. The monolithic `data-analysis-suite` has been split into four highly-specialized skills (`survey-analytics`, `strategic-frameworks`, `causal-inference`, and `machine-learning-lite`) to significantly reduce Agent context bloat. Furthermore, `duckdb-sql-master` was merged into `data-manipulation` for a unified ingestion T-layer. 

Global rules were drastically pruned and distributed horizontally into their relevant skill references, ensuring the LLM's system prompt stays lean. Following this optimization, the OS18 Harvest was successfully absorbed, injecting client-facing explanation architectures into the newly organized `causal-inference` and `survey-analytics` tracks.

## Changes by Category

### ✅ Architectural Overhaul (The Monolith Split)

#### Skills
- **[survey-analytics]**: Created to handle standardized Crosstabs, Factor Analysis, and Survey NLP.
- **[strategic-frameworks]**: Created to handle executive matrices (Pain Curves, Priorities, Halo Removal).
- **[causal-inference]**: Created to handle statistical key drivers and Chi-Square residuals.
- **[machine-learning-lite]**: Created to handle simple, tactical predictive analysis like Feature Importance (Strictly avoiding black-box Deep Learning).
- **[data-manipulation]**: Absorbed the extreme-speed capabilities of DuckDB to offer an ingestion dual-track.

#### Rules Context Optimization
- **Pruning**: Removed `survey_governance`, `explicit_weight_handling`, `monitor_giant_cluster_ratio`, and `prefilter_candidates` from the global `rules/` directory. They are now loaded "on-demand" as References inside their specific analytical skills.

### ✅ Absorbed Items (OS18 Harvest)

#### Scripts
- **`qualtrics_prep_data.py`**: Robust stripping of Qualtrics system metadata rows. 
  - Location: `data-manipulation/scripts/`
- **`relevancia_explanation_generator.py`**: Generates Notebooks structurally explaining Chi-Square Residual scores to clients.
  - Location: `causal-inference/scripts/`

#### References
- **`diverging_bar_charts.md`**: Best practices for plotting Association Matrices.
  - Location: `data-viz/references/`
- **`survey_branching_validation.md`**: Validating mutually exclusive paths via shape matrices.
  - Location: `survey-analytics/references/`

#### Workflows & Rules
- **`numbered_report_generation.md`**: A foundational project workflow enforcing serialized script generation for reproducibility.
  - Location: `workflows/numbered_report_generation.md`
- **`markdown_generation_escapes.md`**: Enforces strict syntactical escapes when programmatically generating Markdown.
  - Location: `survey-analytics/references/markdown_generation_escapes.md`

## Impact Assessment
- **Cognitive Load**: [Low] -> The context split radically drops token consumption per operation.
- **Reuse Potential**: [High] -> Highly segregated tools are easier for agents to deploy safely.
- **Production Readiness**: [Ready] -> The `datapro setup` structure manifest is successfully mapped to the new architecture.

## Testing Performed
- [x] Integrity check (`diff` & `ls`) confirms all 23 scripts and 10 references from the suite monolith migrated without data loss.
- [x] Manifest array parsed manually to ensure OS18 components dropped into correct directories.
- [x] Setup CLI block-guard confirmed operational in the root repo.

## Source Attribution
- **Source**: OS18 / Marketplace Sebrae
- **Harvest Date**: 2026-02-24
