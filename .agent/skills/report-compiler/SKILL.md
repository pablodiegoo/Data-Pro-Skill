---
name: report-compiler
description: "Compiles Markdown analysis reports into formal PDF or DOCX documents using Pandoc. Use this to create the final deliverable for the user."
---

# Report Compiler

This skill handles the final step of the reporting pipeline: transforming the Markdown analysis (with text and images) into a polished PDF or DOCX file.

## Capabilities

### 1. File Compilation (`compile.py`)
Wraps `pandoc` to convert files with proper settings (margins, TOC).

**Usage:**
```bash
python3 .agent/skills/report-compiler/scripts/compile.py final_report.md -f pdf
```

## Prerequisites

This skill depends on `pandoc` and `texlive-xetex` (for PDF generation).
```bash
sudo apt install pandoc texlive-xetex
```

## Best Practices for Reports

When writing the markdown source for the report:
1.  **Images**: Use relative paths. `![Title](images/chart.png)`.
2.  **Page Breaks**: Use `\newpage` (LaTeX command) to force page breaks between sections.
3.  **Headers**: Use `#` for Title, `##` for Sections. These will auto-generate the Table of Contents.
