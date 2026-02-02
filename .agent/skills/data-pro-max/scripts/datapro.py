#!/usr/bin/env python3
"""
DataPro CLI - Unified Data Analysis Command Line Interface

Combines search, reasoning, and report generation in one tool.

Usage:
    datapro search "correlation analysis"
    datapro analyze data.csv --domain survey
    datapro report data.csv -o report.pdf --title "Survey Results"
    datapro style --list
    datapro pipeline data.csv -o report.pdf --domain survey
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
SKILLS_DIR = SCRIPT_DIR.parent.parent  # .agent/skills
REPORT_WRITER = SKILLS_DIR / "report-writer" / "scripts" / "compile_report.py"

# Import local modules
sys.path.insert(0, str(SCRIPT_DIR))


def cmd_search(args):
    """Search the knowledge base."""
    from search import load_csv, search_data, FORMATTERS, FILES
    
    filters = {}
    if args.domain:
        filters["domain"] = args.domain
    if args.category:
        filters["category"] = args.category
    
    search_types = list(FILES.keys()) if args.type == "all" else [args.type]
    
    all_results = []
    for search_type in search_types:
        data = load_csv(FILES[search_type])
        results = search_data(data, args.query, filters, args.limit)
        for r in results:
            r["_type"] = search_type
        all_results.extend(results)
    
    if not all_results:
        print("No results found.")
        return
    
    if args.json:
        import json
        print(json.dumps(all_results, indent=2))
    else:
        print(f"\n{'='*65}")
        print(f" DATAPRO SEARCH - {len(all_results)} Results")
        print(f"{'='*65}")
        
        for row in all_results[:args.limit]:
            formatter = FORMATTERS.get(row["_type"], str)
            print(formatter(row))


def cmd_analyze(args):
    """Analyze a dataset and generate recommendations."""
    import pandas as pd
    from reasoning_engine import generate_analysis_plan, format_plan_markdown
    import json as json_module
    
    try:
        df = pd.read_csv(args.datafile, nrows=args.rows)
    except Exception as e:
        print(f"Error loading {args.datafile}: {e}", file=sys.stderr)
        sys.exit(1)
    
    plan = generate_analysis_plan(df, args.domain, args.goal)
    
    if args.json:
        output = json_module.dumps({
            "profile": {
                "n_rows": plan.data_profile.n_rows,
                "n_cols": plan.data_profile.n_cols,
                "numeric_cols": plan.data_profile.numeric_cols,
                "categorical_cols": plan.data_profile.categorical_cols,
                "text_cols": plan.data_profile.text_cols,
                "missing_pct": plan.data_profile.missing_pct,
                "domain": plan.data_profile.domain,
            },
            "recommended_analyses": [a["name"] for a in plan.recommended_analyses],
            "recommended_visualizations": [v["chart_type"] for v in plan.recommended_visualizations],
            "palette": plan.recommended_palette.get("name", ""),
            "warnings": plan.warnings,
        }, indent=2)
    else:
        output = format_plan_markdown(plan)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✓ Analysis plan saved to: {args.output}")
    else:
        print(output)


def cmd_report(args):
    """Generate PDF/DOCX report from Markdown."""
    if not REPORT_WRITER.exists():
        print(f"Error: report-writer not found at {REPORT_WRITER}", file=sys.stderr)
        sys.exit(1)
    
    cmd = [
        "python3", str(REPORT_WRITER),
        args.input,
        "--format", args.format,
    ]
    
    if args.title:
        cmd.extend(["--title", args.title])
    if args.subtitle:
        cmd.extend(["--subtitle", args.subtitle])
    if args.color:
        cmd.extend(["--color", args.color])
    if args.output:
        cmd.extend(["--output", args.output])
    
    print(f"🔄 Generating {args.format.upper()} report...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ Report generated successfully")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"✗ Error generating report:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)


def cmd_style(args):
    """List or apply visualization styles."""
    from style_presets import list_styles, apply_style, get_style_config
    import json as json_module
    
    if args.list:
        list_styles()
    elif args.apply:
        if args.json:
            config = get_style_config(args.apply)
            print(json_module.dumps(config, indent=2))
        else:
            apply_style(args.apply)
    else:
        list_styles()


def cmd_snippet(args):
    """Get Python code snippets for analyses."""
    import json as json_module
    
    snippets_file = SCRIPT_DIR.parent / "data" / "code_snippets.json"
    
    if not snippets_file.exists():
        print("Error: code_snippets.json not found", file=sys.stderr)
        sys.exit(1)
    
    with open(snippets_file, encoding="utf-8") as f:
        snippets = json_module.load(f)
    
    if args.list:
        print("\n📝 Available Code Snippets:\n")
        print(f"{'ID':<20} {'Name':<30} {'Category'}")
        print("-" * 70)
        for sid, s in snippets.items():
            print(f"{sid:<20} {s['name']:<30} {s['category']}")
        return
    
    if args.id:
        if args.id not in snippets:
            print(f"Error: Snippet '{args.id}' not found", file=sys.stderr)
            print(f"Available: {', '.join(snippets.keys())}")
            sys.exit(1)
        
        snippet = snippets[args.id]
        
        if args.json:
            print(json_module.dumps(snippet, indent=2))
        else:
            print(f"\n{'='*65}")
            print(f" {snippet['name']} ({snippet['category']})")
            print(f"{'='*65}")
            print(f"\n📝 Description: {snippet['description']}")
            print(f"\n📦 Imports:")
            print(f"```python\n{snippet['imports']}\n```")
            print(f"\n🔧 Code:")
            print(f"```python\n{snippet['code']}\n```")
            print(f"\n📊 Example: {snippet['example']}")
            print(f"📤 Returns: {snippet['output_type']}")
    
    elif args.query:
        query = args.query.lower()
        matches = [s for s in snippets.values() 
                   if query in s['name'].lower() or query in s['description'].lower()]
        
        if not matches:
            print(f"No snippets matching '{args.query}'")
            return
        
        print(f"\n📝 Snippets matching '{args.query}':\n")
        for s in matches[:5]:
            print(f"  • {s['id']}: {s['name']} ({s['category']})")
        print(f"\nUse: datapro snippet --id <snippet_id>")
    else:
        cmd_snippet(argparse.Namespace(list=True, id=None, query=None, json=False))


def cmd_pipeline(args):
    """Full pipeline: analyze -> report."""
    import pandas as pd
    from reasoning_engine import generate_analysis_plan, format_plan_markdown
    from style_presets import get_style_config
    
    print(f"📊 DataPro Pipeline: {args.datafile}")
    print("=" * 50)
    
    # Step 1: Load and analyze
    print("\n1️⃣ Analyzing data...")
    try:
        df = pd.read_csv(args.datafile, nrows=args.rows)
    except Exception as e:
        print(f"Error loading {args.datafile}: {e}", file=sys.stderr)
        sys.exit(1)
    
    plan = generate_analysis_plan(df, args.domain, args.goal)
    print(f"   ✓ {plan.data_profile.n_rows:,} rows, {plan.data_profile.n_cols} columns")
    print(f"   ✓ {len(plan.recommended_analyses)} analyses recommended")
    print(f"   ✓ {len(plan.recommended_visualizations)} visualizations suggested")
    print(f"   ✓ Palette: {plan.recommended_palette.get('name', 'N/A')}")
    
    if plan.warnings:
        print("\n   ⚠️ Warnings:")
        for w in plan.warnings[:3]:
            print(f"      {w}")
    
    # Step 2: Generate markdown
    print("\n2️⃣ Generating analysis plan...")
    md_output = format_plan_markdown(plan)
    md_file = args.output.replace(".pdf", ".md").replace(".docx", ".md") if args.output else "analysis_plan.md"
    
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_output)
    print(f"   ✓ Saved to: {md_file}")
    
    # Step 3: Generate report (if output specified and report-writer available)
    if args.output and REPORT_WRITER.exists():
        fmt = "pdf" if args.output.endswith(".pdf") else "docx"
        print(f"\n3️⃣ Generating {fmt.upper()} report...")
        
        cmd = [
            "python3", str(REPORT_WRITER),
            md_file,
            "--format", fmt,
            "--title", args.title or "Data Analysis Report",
        ]
        
        if args.color:
            cmd.extend(["--color", args.color])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   ✓ Report generated: {args.output}")
        else:
            print(f"   ✗ Report generation failed")
            print(f"   📝 Markdown saved at: {md_file}")
    
    print("\n✅ Pipeline complete!")


def main():
    parser = argparse.ArgumentParser(
        prog="datapro",
        description="DataPro CLI - Unified Data Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  datapro search "correlation"
  datapro search --type visualization "bar"
  datapro analyze survey.csv --domain survey --goal "customer segmentation"
  datapro report analysis.md -o report.pdf --title "Q1 Results"
  datapro style --list
  datapro pipeline data.csv -o report.pdf --domain survey
        """,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # SEARCH command
    search_parser = subparsers.add_parser("search", help="Search the knowledge base")
    search_parser.add_argument("query", nargs="?", help="Text to search")
    search_parser.add_argument("--type", "-t", 
                               choices=["analysis", "visualization", "palette", "rule", "style", "all"],
                               default="all", help="Type to search")
    search_parser.add_argument("--domain", "-d", help="Filter by domain")
    search_parser.add_argument("--category", "-c", help="Filter by category")
    search_parser.add_argument("--limit", "-l", type=int, default=10, help="Max results")
    search_parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    # ANALYZE command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a dataset")
    analyze_parser.add_argument("datafile", help="CSV file to analyze")
    analyze_parser.add_argument("--domain", "-d", default="general",
                                choices=["general", "survey", "research", "marketing", "healthcare", "financial"],
                                help="Domain context")
    analyze_parser.add_argument("--goal", "-g", default="", help="Analysis goal")
    analyze_parser.add_argument("--output", "-o", help="Output file")
    analyze_parser.add_argument("--rows", "-n", type=int, default=1000, help="Max rows to profile")
    analyze_parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    # REPORT command
    report_parser = subparsers.add_parser("report", help="Generate PDF/DOCX report")
    report_parser.add_argument("input", help="Markdown input file")
    report_parser.add_argument("--format", "-f", choices=["pdf", "docx"], default="pdf", help="Output format")
    report_parser.add_argument("--output", "-o", help="Output file path")
    report_parser.add_argument("--title", "-t", help="Report title")
    report_parser.add_argument("--subtitle", "-s", help="Report subtitle")
    report_parser.add_argument("--color", "-c", help="Accent color (hex without #)")
    
    # STYLE command
    style_parser = subparsers.add_parser("style", help="Visualization styles")
    style_parser.add_argument("--list", "-l", action="store_true", help="List available styles")
    style_parser.add_argument("--apply", "-a", help="Apply a style by ID")
    style_parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    # SNIPPET command
    snippet_parser = subparsers.add_parser("snippet", help="Get Python code snippets")
    snippet_parser.add_argument("--list", "-l", action="store_true", help="List all snippets")
    snippet_parser.add_argument("--id", "-i", help="Get snippet by ID")
    snippet_parser.add_argument("--query", "-q", help="Search snippets")
    snippet_parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    # PIPELINE command
    pipeline_parser = subparsers.add_parser("pipeline", help="Full analysis pipeline")
    pipeline_parser.add_argument("datafile", help="CSV file to analyze")
    pipeline_parser.add_argument("--output", "-o", help="Output report file (pdf/docx)")
    pipeline_parser.add_argument("--domain", "-d", default="general",
                                 choices=["general", "survey", "research", "marketing", "healthcare", "financial"],
                                 help="Domain context")
    pipeline_parser.add_argument("--goal", "-g", default="", help="Analysis goal")
    pipeline_parser.add_argument("--title", "-t", help="Report title")
    pipeline_parser.add_argument("--color", "-c", help="Accent color")
    pipeline_parser.add_argument("--rows", "-n", type=int, default=1000, help="Max rows")
    
    args = parser.parse_args()
    
    if args.command == "search":
        cmd_search(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "report":
        cmd_report(args)
    elif args.command == "style":
        cmd_style(args)
    elif args.command == "snippet":
        cmd_snippet(args)
    elif args.command == "pipeline":
        cmd_pipeline(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
