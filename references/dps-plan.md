# /dps-plan — Analytical Plan

Generates a suggested checklist of analyses based on available columns and segments.

## Behavior

Reads the manifest from `/dps-setup` outputs and produces an advisory table.

## Execution Steps

1. **Read** `.dps/outputs/setup/setup_manifest.json` (segments + metrics)
2. **Read** `.dps/outputs/setup/setup_segments.csv` (available categories)
3. **Suggest crosses** — for each metric × segment combination, recommend a test
4. **Render** — table with justification

## Output Format

```markdown
| # | Cruzamento | Recommended Test | Rationale |
|---|-------------|-----------------|-----------|
| 1 | Segment x NPS | ANOVA | 3+ groups, continuous outcome |
| 2 | Age x Churn | χ² | 2 categorical vars |
| 3 | Income x Satisfaction | Pearson's r | 2 continuous vars |

> **Note:** Suggestions only. Run specific crosses with `/dps-cross`.
```
