---
name: pdf-to-markdown
description: "A robust tool for converting PDF, DOCX, and PPTX files into Markdown, with support for OCR."
---

# PDF to Markdown Converter

This skill allows you to convert PDF, DOCX, and PPTX documents into Markdown format. It is particularly useful for extracting content from reports, slides, and scanned documents for further processing or analysis.

## Capabilities

- **PDF Conversion**: Uses `pdftotext` for layout preservation. Falls back to OCR (Tesseract) for scanned documents.
- **DOCX/PPTX Conversion**: extracted using `pypandoc` and `python-pptx`.
- **Batch Processing**: Can convert a single file or an entire directory.

## Dependencies

Before running, ensure the following system dependencies are installed:
- `poppler-utils` (for `pdftotext`)
- `tesseract-ocr` (for OCR)

And the following Python packages:
- `pypandoc`
- `pdfminer.six`
- `pdf2image`
- `pytesseract`
- `python-pptx`
- `Pillow`

To install Python dependencies:
```bash
pip install pypandoc pdfminer.six pdf2image pytesseract python-pptx Pillow
```

## Usage

The script is located at `.agent/skills/pdf-to-markdown/scripts/markdowner.py`.

### Basic Conversion
To convert a single file:
```bash
python3 .agent/skills/pdf-to-markdown/scripts/markdowner.py /path/to/input.pdf
```
This will create `/path/to/input.md` by default.

### Specify Output
To specify an output file or directory:
```bash
python3 .agent/skills/pdf-to-markdown/scripts/markdowner.py /path/to/input.pdf -o /path/to/output.md
```

### Force OCR
If the PDF contains images of text (scanned) and normal extraction fails:
```bash
python3 .agent/skills/pdf-to-markdown/scripts/markdowner.py /path/to/input.pdf --ocr
```

### Batch Conversion
To convert all supported files in a directory:
```bash
python3 .agent/skills/pdf-to-markdown/scripts/markdowner.py /path/to/input_directory/ -o /path/to/output_directory/
```

## Troubleshooting
- **Missing text in PDF**: Try using the `--ocr` flag.
- **Dependencies errors**: Ensure you have installed the system packages (`sudo apt install poppler-utils tesseract-ocr`) and python packages.
- **"python-pptx library not installed"**: Run `pip install python-pptx`.
