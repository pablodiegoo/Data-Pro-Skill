---
name: document-converter
description: "Unified document conversion tool. Import: PDF/DOCX/PPTX → Markdown (with OCR). Export: Markdown → PDF/DOCX (with cover page). Combines pdf-to-markdown and report-writer skills."
---

# Document Converter

All-in-one document conversion skill for both **importing** external documents and **exporting** analysis reports.

## Overview

```
┌─────────────────┐              ┌─────────────────┐
│   INPUT FILES   │              │  OUTPUT FILES   │
│  PDF, DOCX,     │ ──import──▶  │   Markdown      │
│  PPTX (OCR)     │              │   (.md)         │
└─────────────────┘              └─────────────────┘
                                        │
                                        │ export
                                        ▼
                                 ┌─────────────────┐
                                 │  FINAL REPORTS  │
                                 │  PDF (styled),  │
                                 │  DOCX           │
                                 └─────────────────┘
```

## Capabilities

### 1. IMPORT: PDF/DOCX/PPTX → Markdown

Uses `markdowner.py` to convert documents to Markdown.

```bash
# Basic conversion
python3 .agent/skills/document-converter/scripts/markdowner.py input.pdf

# Force OCR for scanned documents
python3 .agent/skills/document-converter/scripts/markdowner.py input.pdf --ocr

# Specify output path
python3 .agent/skills/document-converter/scripts/markdowner.py input.pdf -o output.md

# Batch convert directory
python3 .agent/skills/document-converter/scripts/markdowner.py /input_dir/ -o /output_dir/
```

**Supported formats**: `.pdf`, `.docx`, `.pptx`

**Features**:
- Layout preservation with `pdftotext`
- OCR fallback with Tesseract for scanned documents
- DOCX/PPTX extraction with pypandoc

### 2. EXPORT: Markdown → PDF/DOCX

Uses `compile_report.py` to generate professional reports.

```bash
# Professional PDF with cover page
python3 .agent/skills/document-converter/scripts/compile_report.py \
    report.md \
    --format pdf \
    --title "Analysis Report" \
    --subtitle "Q1 2026" \
    --color "2980b9"

# Simple DOCX for editing
python3 .agent/skills/document-converter/scripts/compile_report.py \
    report.md --format docx
```

**PDF Features**:
- Professional cover page with custom title, subtitle, author
- Auto-centered and scaled images
- LaTeX styling with eisvogel-like headers
- Page breaks handled automatically

**DOCX Features**:
- Standard conversion for further editing

## Dependencies

### System Packages
```bash
sudo apt install poppler-utils tesseract-ocr pandoc texlive-xetex texlive-fonts-extra
```

### Python Packages
```bash
pip install pypandoc pdfminer.six pdf2image pytesseract python-pptx Pillow
```

## Workflow Examples

### Import → Process → Export

```bash
# 1. Import external PDF to markdown
python3 markdowner.py survey_report.pdf -o source.md

# 2. Process/analyze in Python or manually

# 3. Export final report
python3 compile_report.py analysis.md \
    --format pdf \
    --title "Survey Analysis"
```

### Batch Processing

```bash
# Import all PDFs in folder
python3 markdowner.py /reports/ -o /markdown/

# Export all markdown to PDFs
for f in /markdown/*.md; do
    python3 compile_report.py "$f" --format pdf
done
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Missing text in PDF | Use `--ocr` flag |
| OCR not working | Install `tesseract-ocr` |
| PDF styling broken | Install `texlive-xetex texlive-fonts-extra` |
| PPTX error | Install `python-pptx` |
| Pandoc not found | Install `pandoc` |

## File Structure

```
.agent/skills/document-converter/
├── SKILL.md              # This file
└── scripts/
    ├── markdowner.py     # PDF/DOCX/PPTX → Markdown
    └── compile_report.py # Markdown → PDF/DOCX
```

## Migration Note

This skill replaces and unifies:
- `pdf-to-markdown` (import functionality)
- `report-writer` (export functionality)

The original skills are deprecated but kept for backward compatibility.
