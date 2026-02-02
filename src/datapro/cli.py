#!/usr/bin/env python3
"""
DataPro CLI - Command Line Interface for Data Analysis Intelligence.

Usage:
    datapro search "correlation analysis"
    datapro analyze data.csv --domain survey
    datapro snippet --list
"""

import argparse
import sys
from pathlib import Path

from datapro import __version__


def cmd_search(args):
    """Search the knowledge base."""
    from datapro.search import search_knowledge_base
    
    results = search_knowledge_base(
        query=args.query,
        search_type=args.type,
        domain=args.domain,
        category=args.category,
        limit=args.limit,
    )
    
    if not results:
        print("No results found.")
        return
    
    if args.json:
        import json
        print(json.dumps(results, indent=2))
    else:
        print(f"\n{'='*65}")
        print(f" DataPro - {len(results)} Results")
        print(f"{'='*65}\n")
        
        for r in results:
            rtype = r.get("_type", "unknown")
            if rtype == "analysis":
                print(f"📊 {r.get('name', 'N/A')}")
                print(f"   Category: {r.get('category', '')} | Domain: {r.get('domain', '')}")
                print(f"   Function: {r.get('python_function', '')}")
            elif rtype == "visualization":
                print(f"📈 {r.get('chart_type', 'N/A')}")
                print(f"   Best for: {r.get('best_for', '')}")
                print(f"   Matplotlib: {r.get('matplotlib_func', '')}")
            elif rtype == "palette":
                print(f"🎨 {r.get('name', 'N/A')}")
                print(f"   Domain: {r.get('domain', '')} | Mood: {r.get('mood', '')}")
            elif rtype == "rule":
                print(f"💡 [{r.get('priority', '').upper()}] {r.get('trigger', '')}")
                print(f"   {r.get('recommendation', '')}")
            else:
                print(f"• {r}")
            print()


def cmd_analyze(args):
    """Analyze a data file and generate recommendations."""
    import pandas as pd
    
    # Import locally to avoid slow startup
    from datapro.reasoning import profile_data, generate_analysis_plan, format_plan
    
    # Load data
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    
    if filepath.suffix == ".csv":
        df = pd.read_csv(filepath)
    elif filepath.suffix in [".xlsx", ".xls"]:
        df = pd.read_excel(filepath)
    else:
        print(f"Error: Unsupported format: {filepath.suffix}", file=sys.stderr)
        sys.exit(1)
    
    # Generate plan
    profile = profile_data(df, domain=args.domain, goal=args.goal)
    plan = generate_analysis_plan(profile)
    
    if args.json:
        import json
        print(json.dumps(plan.__dict__, indent=2, default=str))
    else:
        print(format_plan(plan))


def cmd_snippet(args):
    """Get Python code snippets for analyses."""
    import json as json_module
    
    data_dir = Path(__file__).parent / "data"
    snippets_file = data_dir / "code_snippets.json"
    
    if not snippets_file.exists():
        print("Error: code_snippets.json not found", file=sys.stderr)
        sys.exit(1)
    
    with open(snippets_file, encoding="utf-8") as f:
        snippets = json_module.load(f)
    
    if args.list:
        print("\n📋 Available Code Snippets\n")
        for sid, s in snippets.items():
            print(f"  {sid:20} - {s['name']} [{s['category']}]")
        print(f"\nTotal: {len(snippets)} snippets")
        print("Use: datapro snippet --id <id> to get code")
        
    elif args.id:
        if args.id not in snippets:
            print(f"Error: Snippet '{args.id}' not found", file=sys.stderr)
            sys.exit(1)
        
        s = snippets[args.id]
        if args.json:
            print(json_module.dumps(s, indent=2))
        else:
            print(f"\n# {s['name']}")
            print(f"# Category: {s['category']}")
            print(f"# {s['description']}\n")
            print(s['imports'])
            print()
            print(s['code'])
            print()
            print(f"# Example: {s['example']}")
            
    elif args.query:
        query = args.query.lower()
        matches = {k: v for k, v in snippets.items() 
                   if query in v['name'].lower() or query in v['description'].lower()}
        
        if not matches:
            print(f"No snippets matching '{args.query}'")
        else:
            print(f"\n🔍 Snippets matching '{args.query}':\n")
            for sid, s in matches.items():
                print(f"  {sid:20} - {s['name']}")
    else:
        # Default: show list
        cmd_snippet(argparse.Namespace(list=True, id=None, query=None, json=False))


def cmd_convert(args):
    """Convert PDF/DOCX/PPTX to Markdown."""
    from datapro.converter import perform_conversion
    import os
    
    input_path = args.input
    output_option = args.output
    force_ocr = args.ocr
    
    if not os.path.exists(input_path):
        print(f"Error: Input path '{input_path}' not found.", file=sys.stderr)
        return
        
    files_to_convert = []
    if os.path.isfile(input_path):
        file_path_no_ext, input_ext = os.path.splitext(input_path)
        if input_ext.lower() not in ['.docx', '.pdf', '.pptx']:
            print(f"Error: {input_ext} not supported.", file=sys.stderr)
            return
        
        if not output_option:
            output_file = file_path_no_ext + ".md"
        elif os.path.isdir(output_option):
            output_file = os.path.join(output_option, os.path.basename(file_path_no_ext) + ".md")
        else:
            output_file = output_option
        files_to_convert.append((input_path, output_file))
    elif os.path.isdir(input_path):
        for item in os.listdir(input_path):
            if item.lower().endswith(('.docx', '.pdf', '.pptx')):
                in_f = os.path.join(input_path, item)
                out_f = os.path.join(output_option if output_option else input_path, 
                                     os.path.splitext(item)[0] + ".md")
                files_to_convert.append((in_f, out_f))
    
    for in_f, out_f in files_to_convert:
        perform_conversion(in_f, out_f, force_ocr=force_ocr)


def cmd_report(args):
    """Generate professional PDF/DOCX from Markdown."""
    from datapro.reporter import compile_document
    compile_document(args)


def cmd_setup(args):
    """Setup DataPro in a new project."""
    import shutil
    import os
    from pathlib import Path

    target_project = Path(args.path).absolute()
    source_root = Path(__file__).parent.parent.parent.parent # Root of Data-Pro-Skill
    
    print(f"\n🚀 Setting up DataPro potential in: {target_project}\n")
    
    # 1. Provide Pip instructions
    print("📦 Step 1: Install Python Package")
    pkg_path = source_root
    print(f"   Run: pip install -e {pkg_path}\n")
    
    # 2. Copy Agent Skills
    if not args.no_skills:
        print("🤖 Step 2: Integrating AI Skills")
        skills_to_copy = ["data-pro-max", "survey-stats", "document-converter", "mermaid-diagrams"]
        target_skills_dir = target_project / ".agent" / "skills"
        
        try:
            os.makedirs(target_skills_dir, exist_ok=True)
            for skill in skills_to_copy:
                source_skill = source_root / ".agent" / "skills" / skill
                if source_skill.exists():
                    target_skill = target_skills_dir / skill
                    if target_skill.exists():
                        print(f"   - {skill} already exists, skipping.")
                    else:
                        shutil.copytree(source_skill, target_skill)
                        print(f"   ✅ Integrated skill: {skill}")
            print("\n✨ Done! Your AI agent now has DataPro intelligence in the new project.")
        except Exception as e:
            print(f"   ❌ Error copying skills: {e}")
            print("   You may need to manually copy the .agent/skills/ folder.")
    
    print("\n💡 Tip: After setup, try 'datapro --help' in the new project directory.")


def cmd_version(args):
    """Show version info."""
    print(f"datapro {__version__}")


def main():
    parser = argparse.ArgumentParser(
        prog="datapro",
        description="DataPro CLI - Data Analysis Intelligence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  datapro search "correlation"
  datapro analyze survey.csv --domain survey
  datapro snippet --id nps_calc
  datapro convert raw_data.pdf --ocr
  datapro report analysis.md --title "Final Report" --format pdf
        """,
    )
    parser.add_argument("--version", "-V", action="store_true", help="Show version")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # SEARCH command
    search_parser = subparsers.add_parser("search", help="Search knowledge base")
    search_parser.add_argument("query", nargs="?", help="Text to search")
    search_parser.add_argument("--type", "-t", 
                               choices=["analysis", "visualization", "palette", "rule", "style", "all"],
                               default="all", help="Type of data to search")
    search_parser.add_argument("--domain", "-d", help="Filter by domain")
    search_parser.add_argument("--category", "-c", help="Filter by category")
    search_parser.add_argument("--limit", "-l", type=int, default=10, help="Max results")
    search_parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    # ANALYZE command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze data file")
    analyze_parser.add_argument("file", help="Path to CSV/Excel file")
    analyze_parser.add_argument("--domain", "-d", default="general", help="Analysis domain")
    analyze_parser.add_argument("--goal", "-g", default="", help="Analysis goal")
    analyze_parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    # SNIPPET command
    snippet_parser = subparsers.add_parser("snippet", help="Get Python code snippets")
    snippet_parser.add_argument("--list", "-l", action="store_true", help="List all snippets")
    snippet_parser.add_argument("--id", "-i", help="Get snippet by ID")
    snippet_parser.add_argument("--query", "-q", help="Search snippets")
    snippet_parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    # CONVERT command
    convert_parser = subparsers.add_parser("convert", help="Convert PDF/DOCX/PPTX to Markdown")
    convert_parser.add_argument("input", help="Input file or directory")
    convert_parser.add_argument("-o", "--output", help="Output file or directory")
    convert_parser.add_argument("--ocr", action="store_true", help="Force OCR for PDFs")

    # REPORT command
    report_parser = subparsers.add_parser("report", help="Generate PDF/DOCX from Markdown")
    report_parser.add_argument("input_file", help="Input Markdown file")
    report_parser.add_argument("-f", "--format", choices=["pdf", "docx"], default="pdf")
    report_parser.add_argument("-o", "--output", help="Output path")
    report_parser.add_argument("--title", default="Report")
    report_parser.add_argument("--subtitle", default="")
    report_parser.add_argument("--author", default="DataPro")
    report_parser.add_argument("--date", default="auto")
    report_parser.add_argument("--color", default="1a5276", help="Primary hex color")
    
    # SETUP command
    setup_parser = subparsers.add_parser("setup", help="Integrate DataPro into a new project")
    setup_parser.add_argument("path", help="Path to the new project directory")
    setup_parser.add_argument("--no-skills", action="store_true", help="Only show installation info, don't copy skills")
    
    args = parser.parse_args()
    
    if args.version:
        cmd_version(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "snippet":
        cmd_snippet(args)
    elif args.command == "convert":
        cmd_convert(args)
    elif args.command == "report":
        cmd_report(args)
    elif args.command == "setup":
        cmd_setup(args)
    else:
        parser.print_help()



if __name__ == "__main__":
    main()
