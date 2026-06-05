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

## Execution — Automatic (all formats)

No flags needed. Running `/dps-export` generates ALL formats automatically.

1. **Read** — all outputs from `.dps/outputs/setup/`, `cross/`, `quali/`
2. **Consolidate**:
   ```bash
   python3 .dps/scripts/final_report_generator.py --input .dps/outputs/ -o .dps/outputs/export/
   ```
3. **Add Mermaid charts** — for each crosstab, append a Mermaid bar chart.
   Language matches the project data (detected automatically).
4. **Generate HTML**:
   ```bash
   python3 .dps/scripts/tufte_viz.py --input .dps/outputs/ --charts-dir .dps/outputs/export/charts/
   python3 .dps/scripts/tufte_html.py .dps/references/ .dps/outputs/export/final_report.md
   ```

## Outputs Generated

| File | Format | Content |
|------|--------|---------|
| `final_report.md` | Markdown + Mermaid | Full report, embeddable in GitHub/GitLab |
| `final_report.html` | HTML + Tufte CSS + SVG charts | Publication-ready, print-friendly |

Both are always generated. No flags needed.

## Language

All intermediate files are in English. The final report language is detected automatically from the data (column/segment names).
