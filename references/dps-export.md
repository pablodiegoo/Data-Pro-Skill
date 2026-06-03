# /dps-export — Consolidate & Export

Generates the final publication-ready document from all intermediate outputs.

## Pipeline

```
All intermediate files → Python script → final_report.md [+ final_report.html]
```

## Execution Steps

1. **Collect** all outputs from `.dps/outputs/setup/`, `cross/`, `quali/`
2. **Run script**:
   ```bash
   python3 .dps/scripts/final_report_generator.py --input .dps/outputs/ -o .dps/outputs/export/
   ```
3. **Render** — consolidated Markdown with chronological sections

## Flags

| Flag | Result |
|------|--------|
| `--full` (default) | All sections: manifesto + crosstabs + quali + strategy |
| `--manifest` | Setup section only |
| `--crosstabs` | All crosstab sections only |
| `--html` | Generate Tufte HTML (requires Quarto) |

## Output Format

Single self-contained Markdown file with YAML frontmatter, ready for Pandoc/Quarto/LaTeX.
