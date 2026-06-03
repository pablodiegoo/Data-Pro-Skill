# /dps-plan — Analytical Plan

Generates a suggested checklist of analyses to run.

## Behavior

Produces a lightweight advisory table — suggestions, not requirements.

## Output Format

| # | Cruzamento | Recommended Test | Rationale |
|---|-------------|-----------------|-----------|
| 1 | Segment x NPS | ANOVA | Compare NPS across 3+ segments |
| 2 | Age Group x Churn | χ² | Test independence of categorical vars |

This is a **suggestion only**. The user can pick specific items and run them with `/dps-cross`.
