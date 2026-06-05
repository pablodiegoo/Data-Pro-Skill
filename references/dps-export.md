# /dps-export — Consolidate & Export

Generates the final publication-ready document in the project's original language.

## Pipeline

```
All intermediate files → Python scripts → final_report.md (with Mermaid charts) + final_report.html (Tufte styled)
```

## Language

All intermediate files (setup, cross, quali) are in **English**.
The final report must be in the **project's original language** — detect from data (column names, segment names, verbatims).

| Data language | Final report |
|---------------|-------------|
| Portuguese columns ("bairro", "renda", "domicílio") | pt-BR |
| English columns ("income", "age", "satisfaction") | en |
| Spanish columns | es |

## Execution Steps

1. **Collect** — read all outputs from `.dps/outputs/setup/`, `cross/`, `quali/`
2. **Render Markdown** — consolidate with `final_report_generator.py`:
   ```bash
   python3 .dps/scripts/final_report_generator.py --input .dps/outputs/ -o .dps/outputs/export/
   ```
3. **Add Mermaid charts** — for each crosstab in the report, append:
   ```markdown
   ```mermaid
   xychart-beta
     title "Cross: X by Y"
     x-axis "Category" ["A","B","C"]
     y-axis "Percent" 0 --> 100
     bar [val1, val2, val3]
   ```
   ```
4. **Generate Tufte HTML**:
   ```bash
   python3 .dps/scripts/tufte_viz.py --input .dps/outputs/ --charts-dir .dps/outputs/export/charts/
   python3 .dps/scripts/tufte_html.py .dps/references/ .dps/outputs/export/final_report.md
   ```
5. **Result** — two files:
   - `final_report.md` — Markdown with Mermaid charts, human-readable
   - `final_report.html` — Tufte-styled HTML with SVG charts embedded

## Flags

| Flag | Result |
|------|--------|
| `--full` (default) | All sections: manifesto + crosstabs + quali + strategy |
| `--manifest` | Setup section only |
| `--crosstabs` | All crosstab sections only |
| `--lang <code>` | Override language detection: `pt`, `en`, `es` |

## Charts

The HTML output includes Tufte-style SVG charts embedded inline:
- **Sparklines** — small inline trend charts per variable
- **Dot plots** — segmented comparisons
- **Small multiples** — per-segment distribution grids
