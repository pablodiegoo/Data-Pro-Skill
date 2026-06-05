# /dps-export — Consolidate & Export

Generates the final publication-ready document in the project's original language.

## Pipeline

```
All intermediate files → Python script + tufte_viz.py → final_report.md + final_report.html
```

## Language

The final report must be in the **project's original language**. E.g.:
- Portuguese survey data → final report in Portuguese
- English survey data → final report in English
- Spanish survey data → final report in Spanish

The AI must detect the language from the data (column names, segment names, verbatims) and render the export in that language.

## Execution Steps

1. **Collect** all outputs from `.dps/outputs/setup/`, `cross/`, `quali/`
2. **Generate Tufte charts**:
   ```bash
   python3 .dps/scripts/tufte_viz.py --input .dps/outputs/ --charts-dir .dps/outputs/export/charts/
   ```
3. **Run report consolidation**:
   ```bash
   python3 .dps/scripts/final_report_generator.py --input .dps/outputs/ -o .dps/outputs/export/
   ```
4. **Generate HTML**:
   ```bash
   python3 .dps/scripts/tufte_html.py .dps/references/ .dps/outputs/export/final_report.md
   ```

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
