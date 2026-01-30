#!/usr/bin/env python3
"""
Report Writer - Unified Compilation Script
Merges capabilities of markdown-to-pdf and report-compiler.
"""

import subprocess
import shutil
import os
import sys
import tempfile
import re
import argparse
from datetime import datetime

def check_dependencies():
    """Checks if pandoc and xelatex are installed."""
    missing = []
    if not shutil.which("pandoc"):
        missing.append("pandoc")
    if not shutil.which("xelatex"):
        missing.append("texlive-xetex")
    
    if missing:
        print(f"❌ Error: Missing dependencies: {', '.join(missing)}")
        print("   Install with: sudo apt install pandoc texlive-xetex texlive-fonts-extra")
        return False
    return True

# --- Pre-processing Logic (From markdown-to-pdf) ---

def preprocess_markdown(content):
    """
    Pre-processes markdown to ensure nice formatting in PDF.
    - Handles image centering and sizing.
    - Adds page breaks.
    - Handles Mermaid blocks (strips them as they break PDF generation).
    """
    # 1. Handle Mermaid blocks (Pandoc typically fails on these without a filter)
    mermaid_pattern = r'```mermaid\n(.*?)```'
    mermaid_note = r'> *[Diagram available in digital version]*'
    content = re.sub(mermaid_pattern, mermaid_note, content, flags=re.DOTALL)
    
    # 2. Image Handling
    # Force images into their own paragraphs and add width attribute for Pandoc
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'\n\n![\1](\2){width=80%}\n\n', content)
    
    # 3. Smart Page Breaks (For PDF only ideally, but harmless in DOCX usually)
    # Add \newpage before main sections (H1, H2)
    content = re.sub(r'\n(## \d+\.|# )', r'\n\\newpage\n\1', content)
    
    # Remove the first newpage if inserted at the start
    content = content.replace('\\newpage\n## 1.', '## 1.', 1)
    content = content.replace('\\newpage\n# ', '# ', 1)
    
    return content

def create_latex_header(title, subtitle, author, date, primary_color):
    """Generates the LaTeX header with configuration (For PDF)."""
    if date.lower() == 'auto':
        date = datetime.now().strftime("%B %Y")
        
    return r"""
---
title: "{title}"
subtitle: "{subtitle}"
author: "{author}"
date: "{date}"
titlepage: true
titlepage-color: "{color}"
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "FFFFFF"
titlepage-rule-height: 2
toc: true
toc-title: "Table of Contents"
toc-own-page: true
numbersections: true
geometry: "margin=2.5cm"
fontsize: 11pt
documentclass: report
colorlinks: true
linkcolor: "{color}"
urlcolor: "{color}"
header-includes:
  - \usepackage{{graphicx}}
  - \usepackage{{float}}
  - \floatplacement{{figure}}{{H}}
  - \setlength{{\parindent}}{{0pt}}
  - \setlength{{\parskip}}{{6pt}}
  - \usepackage{{caption}}
  - \captionsetup{{justification=centering}}
  - \usepackage{{etoolbox}}
  - \AtBeginEnvironment{{figure}}{{\centering}}
  - \usepackage{{fancyhdr}}
  - \pagestyle{{fancy}}
  - \fancyhead[L]{{\small {subtitle}}}
  - \fancyhead[R]{{\small \thepage}}
  - \fancyfoot[C]{{}}
  - \renewcommand{{\headrulewidth}}{{0.4pt}}
  - \usepackage{{booktabs}}
  - \usepackage{{longtable}}
---

""".format(title=title, subtitle=subtitle, author=author, date=date, color=primary_color)

# --- Main Logic ---

def compile_document(args):
    if not check_dependencies():
        return False
        
    input_path = os.path.abspath(args.input_file)
    output_ext = "pdf" if args.format == "pdf" else "docx"
    output_path = os.path.abspath(args.output) if args.output else os.path.splitext(input_path)[0] + "." + output_ext
    
    if not os.path.exists(input_path):
        print(f"❌ Error: Input file '{input_path}' not found.")
        return False
        
    print(f"📄 Reading '{args.input_file}'...")
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pre-process is mostly beneficial for PDF, but cleaning attributes helps DOCX too.
    print("🔧 Pre-processing markdown...")
    processed_content = preprocess_markdown(content)

    # Temporary file handling
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if args.format == "pdf":
        # PDF Mode: Inject LaTeX Header
        header = create_latex_header(args.title, args.subtitle, args.author, args.date, args.color)
        final_content = header + processed_content
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, dir=script_dir, encoding='utf-8') as tmp:
            tmp.write(final_content)
            tmp_path = tmp.name
            
        print("📑 Compiling PDF (Advanced Mode)...")
        resource_path = os.path.dirname(input_path)
        cmd = [
            "pandoc", tmp_path, "-o", output_path,
            "--pdf-engine=xelatex",
            f"--resource-path={resource_path}",
            "--standalone"
        ]
        
    else:
        # DOCX Mode: Simple conversion
        # We still use the pre-processed content (images centered etc), but NO LaTeX header.
        # Although \newpage, titlepage vars are ignored by DOCX writer usually or handled gracefully.
        
        # We assume for DOCX we don't use the Title Page metadata YAML block because Pandoc handles DOCX covers differently (Reference doc).
        # We just pass the content.
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, dir=script_dir, encoding='utf-8') as tmp:
            tmp.write(processed_content)
            tmp_path = tmp.name
            
        print("📑 Compiling DOCX...")
        resource_path = os.path.dirname(input_path)
        cmd = [
            "pandoc", tmp_path, "-o", output_path,
            f"--resource-path={resource_path}",
            "--toc" # Simple TOC for DOCX
        ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Compilation failed:")
            print(result.stderr)
            return False
            
        print(f"✅ Success! Document generated: {output_path}")
        return True
    finally:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Report Writer - Convert Markdown to Professional PDF/DOCX")
    parser.add_argument("input_file", help="Path to input Markdown file")
    parser.add_argument("-f", "--format", choices=["pdf", "docx"], default="pdf", help="Output format")
    parser.add_argument("-o", "--output", help="Output path (default: same as input)")
    
    # Metadata args (Used primarily for PDF)
    parser.add_argument("--title", default="Report", help="Document Title")
    parser.add_argument("--subtitle", default="", help="Document Subtitle")
    parser.add_argument("--author", default="Antigravity", help="Document Author")
    parser.add_argument("--date", default="auto", help="Document Date")
    parser.add_argument("--color", default="1a5276", help="Primary hex color (for PDF themes)")
    
    args = parser.parse_args()
    success = compile_document(args)
    sys.exit(0 if success else 1)
