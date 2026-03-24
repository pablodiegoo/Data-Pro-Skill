# Proposed Improvement: Survey Analysis Pipeline

## Context
The Beerfest 2026 project achieved a highly polished deliverable purely through Markdown. The current `survey-analysis-pipeline.md` relies on `data-viz` to dump images into `assets/images/`.

## Proposal
- **Phase 5 (Analysis & Visuals)**: Replace image generation with `survey_report_generator.py`. Standardize the use of Mermaid.js `xychart-beta` and `pie` for frequencies.
- **Phase 7 (Reporting)**: Define that the final report must be generated via a hypothesis-driven script like `final_report_generator.py`, which natively outputs cross-tabs, NPS, and statistical tests.
