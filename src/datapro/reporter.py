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
from pathlib import Path

from datapro.styles import PDF_THEMES


def check_dependencies():
    """Checks if pandoc, xelatex are installed. Optional: mermaid-cli (mmdc)."""
    missing = []
    if not shutil.which("pandoc"):
        missing.append("pandoc")
    if not shutil.which("xelatex"):
        missing.append("texlive-xetex")
    
    if missing:
        print(f"❌ Error: Missing core dependencies: {', '.join(missing)}")
        print("   Install with: sudo apt install pandoc texlive-xetex texlive-fonts-extra")
        return False
    
    if not shutil.which("mmdc"):
        print("⚠️ Warning: 'mmdc' (mermaid-cli) not found. Mermaid diagrams will be skipped.")
    
    return True

# --- Pre-processing Logic ---

def render_mermaid_diagrams(content, resource_path):
    """
    Finds mermaid blocks, renders them as PNG using mmdc, 
    and replaces the blocks with image references.
    """
    if not shutil.which("mmdc"):
        # Placeholder if mmdc is missing
        placeholder = "\n\n> *[Diagram: MermaidJS (mmdc required for PDF rendering)]*\n\n"
        return re.sub(r'```mermaid\n(.*?)```', placeholder, content, flags=re.DOTALL)

    def replace_mermaid(match):
        mermaid_code = match.group(1).strip()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as tmp_mmd:
            tmp_mmd.write(mermaid_code)
            mmd_path = tmp_mmd.name
        
        img_name = f"mermaid_{hash(mermaid_code) % 1000000}.png"
        img_path = os.path.join(resource_path, img_name)
        
        # Use puppeteer config if available (important for Linux environments)
        script_dir = Path(__file__).parent.parent.parent # Root of datapro pkg
        config_path = os.path.join(os.getcwd(), "puppeteer-config.json")
        cmd = ["mmdc", "-i", mmd_path, "-o", img_path, "-b", "transparent"]
        if os.path.exists(config_path):
            cmd.extend(["-p", config_path])
            
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            if os.path.exists(mmd_path):
                os.remove(mmd_path)
            return f"\n\n![Diagram]({img_name})\n\n"
        except Exception as e:
            print(f"⚠️ Failed to render Mermaid diagram: {e}")
            return "\n\n> *[Failed to render Mermaid diagram]*\n\n"

    return re.sub(r'```mermaid\n(.*?)```', replace_mermaid, content, flags=re.DOTALL)


def preprocess_markdown(content, args):
    """
    Pre-processes markdown to ensure nice formatting in PDF.
    """
    # 1. Handle Mermaid
    resource_path = os.path.dirname(os.path.abspath(args.input_file))
    content = render_mermaid_diagrams(content, resource_path)
    
    # 2. Image Handling
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'\n\n![\1](\2){width=80%}\n\n', content)
    
    # 3. Handle Columns (LaTeX multicol)
    if args.format == "pdf" and args.columns > 1:
        # Wrap the whole content in multicols using Pandoc raw blocks 
        # to ensure it doesn't break header parsing
        content = f"\n\n```{{=latex}}\n\\begin{{multicols}}{{{args.columns}}}\n```\n\n{content}\n\n```{{=latex}}\n\\end{{multicols}}\n```\n\n"
    
    # 4. Smart Page Breaks
    content = re.sub(r'\n(## \d+\.|# )', r'\n\\newpage\n\1', content)
    content = content.replace('\\newpage\n## 1.', '## 1.', 1)
    content = content.replace('\\newpage\n# ', '# ', 1)
    
    return content


def create_latex_header(args):
    """Generates the LaTeX header with configuration (For PDF)."""
    # Select theme
    theme_id = getattr(args, 'theme', 'executive')
    theme = PDF_THEMES.get(theme_id, PDF_THEMES['executive'])
    
    # Override theme color if user provided one
    primary_color = getattr(args, 'color', None) or theme.primary_color
    
    date = getattr(args, 'date', 'auto')
    if date.lower() == 'auto':
        date = datetime.now().strftime("%B %Y")
        
    header_includes = [
        r"\usepackage{graphicx}",
        r"\usepackage{float}",
        r"\floatplacement{figure}{H}",
        r"\setlength{\parindent}{0pt}",
        r"\setlength{\parskip}{6pt}",
        r"\usepackage{caption}",
        r"\captionsetup{justification=centering}",
        r"\usepackage{etoolbox}",
        r"\AtBeginEnvironment{figure}{\centering}",
        r"\usepackage{fancyhdr}",
        r"\pagestyle{fancy}",
        f"\\fancyhead[L]{{\\small {getattr(args, 'subtitle', '')}}}",
        r"\fancyhead[R]{\small \thepage}",
        r"\fancyfoot[C]{" + f"{getattr(args, 'footer', '')}" + "}",
        r"\renewcommand{\headrulewidth}{0.4pt}",
        r"\usepackage{booktabs}",
        r"\usepackage{longtable}",
        r"\usepackage{multicol}", # For N-columns
    ]
    
    # Fix for longtable in multicol mode
    if getattr(args, 'columns', 1) > 1:
        header_includes.append(r"\makeatletter")
        header_includes.append(r"\let\oldlt\longtable")
        header_includes.append(r"\let\endoldlt\endlongtable")
        header_includes.append(r"\renewenvironment{longtable}[1]{\begin{tabular}{#1}}{\end{tabular}}")
        header_includes.append(r"\makeatother")
    
    # Watermark support
    if getattr(args, 'watermark', None):
        # Escape special LaTeX characters in watermark
        safe_watermark = args.watermark.replace("_", "\\_").replace("#", "\\#").replace("%", "\\%")
        header_includes.append(r"\usepackage[printwatermark]{xwatermark}")
        header_includes.append(f"\\newwatermark[allpages,color=gray!20,angle=45,scale=3,xpos=0,ypos=0]{{{safe_watermark}}}")

    # Logo support
    if getattr(args, 'logo', None):
        header_includes.append(r"\usepackage{titling}")
        logo_path = os.path.abspath(args.logo)
        header_includes.append(f"\\pretitle{{\\begin{{center}}\\includegraphics[width=2cm]{{{logo_path}}}\\\\[2cm]}}")
        header_includes.append(r"\posttitle{\end{center}}")

    header = f"""---
title: "{args.title}"
subtitle: "{args.subtitle}"
author: "{args.author}"
date: "{date}"
titlepage: true
titlepage-color: "{theme.titlepage_color}"
titlepage-text-color: "{theme.titlepage_text_color}"
titlepage-rule-color: "{theme.titlepage_text_color}"
titlepage-rule-height: 2
toc: {str(not getattr(args, 'no_toc', False)).lower()}
toc-title: "Table of Contents"
toc-own-page: true
numbersections: true
geometry: "margin={getattr(args, 'margins', '2.5cm')}{', landscape' if getattr(args, 'landscape', False) else ''}"
fontsize: 11pt
mainfont: "{theme.font_main}"
sansfont: "{theme.font_main}"
documentclass: report
colorlinks: true
linkcolor: "{primary_color}"
urlcolor: "{primary_color}"
header-includes:
"""
    for line in header_includes:
        header += f"  - {line}\n"
    
    header += "---\n\n"
    return header

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

    print("🔧 Pre-processing markdown (Mermaid, Columns, Images)...")
    processed_content = preprocess_markdown(content, args)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if args.format == "pdf":
        print(f"🎨 Applying Theme: {getattr(args, 'theme', 'executive')}")
        header = create_latex_header(args)
        final_content = header + processed_content
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, dir=script_dir, encoding='utf-8') as tmp:
            tmp.write(final_content)
            tmp_path = tmp.name
            
        print("📑 Compiling PDF (Advanced Xelatex Engine)...")
        resource_path = os.path.dirname(input_path)
        cmd = [
            "pandoc", tmp_path, "-o", output_path,
            "--pdf-engine=xelatex",
            f"--resource-path={resource_path}",
            "--standalone"
        ]
        
    else:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, dir=script_dir, encoding='utf-8') as tmp:
            tmp.write(processed_content)
            tmp_path = tmp.name
            
        print("📑 Compiling DOCX...")
        resource_path = os.path.dirname(input_path)
        cmd = [
            "pandoc", tmp_path, "-o", output_path,
            f"--resource-path={resource_path}",
            "--toc"
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
    parser = argparse.ArgumentParser(description="Report Writer - Advanced PDF/DOCX Engine")
    parser.add_argument("input_file", help="Path to input Markdown file")
    parser.add_argument("-f", "--format", choices=["pdf", "docx"], default="pdf")
    parser.add_argument("-o", "--output")
    parser.add_argument("--theme", choices=["executive", "minimalist", "academic", "dark"], default="executive")
    parser.add_argument("--columns", type=int, default=1)
    parser.add_argument("--landscape", action="store_true")
    parser.add_argument("--watermark")
    parser.add_argument("--logo")
    parser.add_argument("--footer", default="")
    parser.add_argument("--title", default="Report")
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--author", default="DataPro")
    parser.add_argument("--date", default="auto")
    parser.add_argument("--color")
    parser.add_argument("--margins", default="2.5cm")
    parser.add_argument("--no-toc", action="store_true")
    
    args = parser.parse_args()
    success = compile_document(args)
    sys.exit(0 if success else 1)
