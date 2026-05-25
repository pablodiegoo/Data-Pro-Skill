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


def simple_markdown_to_html(md_content: str) -> str:
    """
    A lightweight, regex-based Markdown to HTML converter.
    Handles headings, tables, blockquotes, bold/italic, links, and paragraphs.
    """
    import re
    lines = md_content.split("\n")
    html_lines = []
    in_table = False
    table_headers = []
    table_rows = []
    in_list = False
    in_quote = False
    quote_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Code block
        if line.startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            code_text = "\n".join(code_lines)
            code_text = code_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            html_lines.append(f"<pre><code>{code_text}</code></pre>")
            i += 1
            continue
            
        # Table parsing
        if line.strip().startswith("|") and "|" in line:
            if re.match(r'^[\s|:-]+$', line.strip()):
                i += 1
                continue
                
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if not in_table:
                in_table = True
                table_headers = cells
            else:
                table_rows.append(cells)
            i += 1
            continue
        elif in_table:
            table_html = "<table>\n<thead>\n<tr>"
            for h in table_headers:
                table_html += f"<th>{h}</th>"
            table_html += "</tr>\n</thead>\n<tbody>\n"
            for r in table_rows:
                table_html += "<tr>"
                for cell in r:
                    table_html += f"<td>{cell}</td>"
                table_html += "</tr>\n"
            table_html += "</tbody>\n</table>"
            html_lines.append(table_html)
            in_table = False
            table_headers = []
            table_rows = []
            
        # List parsing
        if line.strip().startswith("- ") or line.strip().startswith("* "):
            content = line.strip()[2:]
            if not in_list:
                in_list = True
                html_lines.append("<ul>")
            html_lines.append(f"<li>{content}</li>")
            i += 1
            continue
        elif in_list:
            html_lines.append("</ul>")
            in_list = False
            
        # Blockquote parsing
        if line.strip().startswith(">"):
            content = line.strip()[1:].strip()
            if not in_quote:
                in_quote = True
            quote_lines.append(content)
            i += 1
            continue
        elif in_quote:
            quote_text = " ".join(quote_lines)
            html_lines.append(f"<blockquote>{quote_text}</blockquote>")
            in_quote = False
            quote_lines = []
            
        # Heading parsing
        if line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("#### "):
            html_lines.append(f"<h4>{line[5:]}</h4>")
        elif not line.strip():
            html_lines.append("")
        else:
            html_lines.append(f"<p>{line}</p>")
            
        i += 1
        
    if in_table:
        table_html = "<table>\n<thead>\n<tr>"
        for h in table_headers:
            table_html += f"<th>{h}</th>"
        table_html += "</tr>\n</thead>\n<tbody>\n"
        for r in table_rows:
            table_html += "<tr>"
            for cell in r:
                table_html += f"<td>{cell}</td>"
            table_html += "</tr>\n"
        table_html += "</tbody>\n</table>"
        html_lines.append(table_html)
    if in_list:
        html_lines.append("</ul>")
    if in_quote:
        quote_text = " ".join(quote_lines)
        html_lines.append(f"<blockquote>{quote_text}</blockquote>")
        
    full_html = "\n".join(html_lines)
    full_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', full_html)
    full_html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', full_html)
    full_html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', full_html)
    full_html = full_html.replace("<p></p>", "")
    
    return full_html


def export_tufte_report(outputs_dir: str, output_path: str) -> bool:
    """
    Finds all Markdown files in outputs_dir, sorts them alphabetically,
    concatenates their content, and compiles them to a self-contained Tufte HTML report.
    """
    from pathlib import Path
    
    outputs_path = Path(outputs_dir)
    if not outputs_path.exists() or not outputs_path.is_dir():
        print(f"❌ Error: Outputs directory '{outputs_dir}' not found.")
        return False

    # Find all .md files, sorted alphabetically
    md_files = sorted(list(outputs_path.glob("*.md")))
    if not md_files:
        print(f"❌ Error: No Markdown files found in '{outputs_dir}'.")
        return False

    print(f"📄 Found {len(md_files)} Markdown files in '{outputs_dir}'. Merging...")
    
    # Merge contents
    merged_content = ""
    for md_file in md_files:
        print(f"   - Merging: {md_file.name}")
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
            # Strip yaml frontmatter from individual files if present
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    content = parts[2].strip()
            merged_content += content + "\n\n"
            
    # Load tufte.css
    css_path = Path(__file__).parent / "data" / "tufte.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
    else:
        css_content = "/* Tufte CSS fallback */"
        
    # Attempt compilation with Pandoc
    script_dir = os.path.dirname(os.path.abspath(__file__))
    header_content = f"<style>\n{css_content}\n</style>"
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, dir=script_dir, encoding='utf-8') as tmp_header:
            tmp_header.write(header_content)
            tmp_header_path = tmp_header.name
            
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, dir=script_dir, encoding='utf-8') as tmp_merged:
            tmp_merged.write(merged_content)
            tmp_merged_path = tmp_merged.name
            
        cmd = [
            "pandoc",
            "-s",
            "-H", tmp_header_path,
            "-o", output_path,
            "--metadata", 'title=Data Pro Max Analysis Report',
            tmp_merged_path
        ]
        
        print("📑 Attempting self-contained Tufte HTML report via Pandoc...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success! Tufte HTML report generated via Pandoc: {output_path}")
            return True
        else:
            print("⚠️ Pandoc compilation failed. Falling back to native Python compiler...")
    except FileNotFoundError:
        print("⚠️ Pandoc not found. Falling back to native Python compiler...")
    except Exception as e:
        print(f"⚠️ Error with Pandoc: {e}. Falling back to native Python compiler...")
    finally:
        if 'tmp_header_path' in locals() and os.path.exists(tmp_header_path):
            os.remove(tmp_header_path)
        if 'tmp_merged_path' in locals() and os.path.exists(tmp_merged_path):
            os.remove(tmp_merged_path)

    # Native Python Compiler Fallback (highly portable)
    try:
        print("🐍 Compiling using native Python Markdown-to-HTML engine...")
        body_html = simple_markdown_to_html(merged_content)
        
        full_html = f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Data Pro Max Analysis Report</title>
  <style>
{css_content}
  </style>
</head>
<body>
  <div class="report-container">
    <div class="main-column">
{body_html}
    </div>
  </div>
</body>
</html>
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"✅ Success! Self-contained Tufte HTML report generated: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error during native compilation: {e}")
        return False


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
