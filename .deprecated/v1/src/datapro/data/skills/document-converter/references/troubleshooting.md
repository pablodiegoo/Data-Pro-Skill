# Document Conversion Troubleshooting

| Issue | Solution |
|-------|----------|
| Missing text in PDF | Use `--ocr` flag in `markdowner.py` |
| OCR not working | Ensure `tesseract-ocr` system package is installed |
| PDF styling broken | Ensure `texlive-xetex` and `texlive-fonts-extra` are installed |
| PPTX error | Install `python-pptx` |
| Pandoc not found | Install `pandoc` system package |
| Quarto not found | Download and install from quarto.org |
| LaTeX compilation error | Check if all fonts used in the template are installed locally |
