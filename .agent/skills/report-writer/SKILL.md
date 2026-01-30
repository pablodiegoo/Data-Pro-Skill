---
name: report-writer
description: "All-in-one report generation tool. Compiles Markdown into professional PDF (with cover page, auto-formatting) or DOCX. Replaces both `markdown-to-pdf` and `report-compiler`."
---

# Report Writer

This skill is the definitive tool for converting Markdown analysis into final deliverables. It combines the professional PDF styling of `markdown-to-pdf` with the format flexibility of `report-compiler`.

## Capabilities

### 1. Unified Compilation (`compile_report.py`)
Converts Markdown to PDF or DOCX.

#### Features for PDF:
- **Professional Cover Page**: Custom title, subtitle, author, color.
- **Smart Pre-processing**: Auto-centers images, scales them to fit, handles page breaks.
- **LaTeX Styling**: Uses `eisvogel`-like custom headers (via inline template).

#### Features for DOCX:
- Standard conversion (suitable for further editing).

**Usage:**

```bash
# Generate Professional PDF (Recommended for Final Delivery)
python3 .agent/skills/report-writer/scripts/compile_report.py \
    input.md \
    --format pdf \
    --title "Project X Report" \
    --subtitle "Q1 Analysis" \
    --color "2980b9"

# Generate simple DOCX (For editing)
python3 .agent/skills/report-writer/scripts/compile_report.py \
    input.md \
    --format docx
```

## Prerequisites

```bash
sudo apt install pandoc texlive-xetex texlive-fonts-extra
```
