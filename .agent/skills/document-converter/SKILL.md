---
name: document-converter
description: "Unified document conversion tool. Import: PDF/DOCX/PPTX → Markdown (with OCR). Export: Markdown → PDF/DOCX (with cover page). Combines pdf-to-markdown and report-writer skills."
---

# Document Converter

All-in-one skill for **importing** external documents (PDF/DOCX/PPTX) to Markdown and **exporting** analysis results to professional reports (PDF/DOCX).

## Core Procedures

### 1. IMPORT: External Docs → Markdown
Uses `markdowner.py` with optional OCR fallback.
```bash
python3 .agent/skills/document-converter/scripts/markdowner.py input.pdf [--ocr]
```

### 2. EXPORT: Markdown → Final Report
Uses `compile_report.py` for standard reports or **Quarto** for premium reports.
```bash
# Standard PDF
python3 .agent/skills/document-converter/scripts/compile_report.py report.md --format pdf
```

## Detailed Guides & Reference
- **Premium Quarto Reports**: See [quarto_reports.md](references/quarto_reports.md)
- **Troubleshooting & Setup**: See [troubleshooting.md](references/troubleshooting.md)

## Assets
- **Quarto Templates**: See `assets/quarto-templates/` for base structure.

## Dependencies

### System Packages
`sudo apt install poppler-utils tesseract-ocr pandoc texlive-xetex texlive-fonts-extra`

### Python Packages
`pip install pypandoc pdfminer.six pdf2image pytesseract python-pptx Pillow`

## File Structure
```
.agent/skills/document-converter/
├── SKILL.md
├── assets/        # Templates and branding
├── references/    # Detailed manuals
└── scripts/
    ├── markdowner.py     # Import engine
    └── compile_report.py # Export engine
```
