#!/usr/bin/env python3
"""
Data Pro Max - Search Engine
Search the knowledge base for analysis recommendations.

Usage:
    python3 search.py "correlation analysis"
    python3 search.py --domain survey --category inferential
    python3 search.py --type visualization "bar chart"
    python3 search.py --type palette --domain healthcare
    python3 search.py --type rule "missing data"
"""

import argparse
import csv
import os
import sys
from pathlib import Path
from typing import Optional

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"

# Data files
FILES = {
    "analysis": DATA_DIR / "analysis_types.csv",
    "visualization": DATA_DIR / "visualization_rules.csv",
    "palette": DATA_DIR / "palettes.csv",
    "rule": DATA_DIR / "reasoning_rules.csv",
    "style": DATA_DIR / "visualization_styles.csv",
}


def load_csv(filepath: Path) -> list[dict]:
    """Load CSV file into list of dicts."""
    if not filepath.exists():
        print(f"Warning: {filepath} not found", file=sys.stderr)
        return []
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def search_data(
    data: list[dict],
    query: Optional[str] = None,
    filters: Optional[dict] = None,
    limit: int = 10,
) -> list[dict]:
    """
    Search data with optional text query and filters.
    
    Args:
        data: List of row dicts
        query: Text to search in all fields
        filters: Dict of {field: value} exact matches
        limit: Max results
    
    Returns:
        Matching rows
    """
    results = []
    query_lower = query.lower() if query else None
    
    for row in data:
        # Apply text search
        if query_lower:
            row_text = " ".join(str(v).lower() for v in row.values())
            if query_lower not in row_text:
                continue
        
        # Apply filters
        if filters:
            match = True
            for field, value in filters.items():
                if field in row and value.lower() not in row[field].lower():
                    match = False
                    break
            if not match:
                continue
        
        results.append(row)
        if len(results) >= limit:
            break
    
    return results


def format_analysis(row: dict) -> str:
    """Format analysis type result."""
    return f"""
┌─────────────────────────────────────────────────────────────┐
│ {row['name']:<59} │
├─────────────────────────────────────────────────────────────┤
│ Category:    {row['category']:<46} │
│ Use Case:    {row['use_case'][:46]:<46} │
│ When to Use: {row['when_to_use'][:46]:<46} │
│ Avoid When:  {row['avoid_when'][:46]:<46} │
│ Function:    {row['python_function'][:46]:<46} │
│ Domain:      {row['domain']:<46} │
└─────────────────────────────────────────────────────────────┘"""


def format_visualization(row: dict) -> str:
    """Format visualization rule result."""
    return f"""
┌─────────────────────────────────────────────────────────────┐
│ {row['chart_type']:<59} │
├─────────────────────────────────────────────────────────────┤
│ Data Type:   {row['data_type']:<46} │
│ Variables:   {row['n_variables']:<46} │
│ Best For:    {row['best_for'][:46]:<46} │
│ Avoid When:  {row['avoid_when'][:46]:<46} │
│ Matplotlib:  {row['matplotlib_func'][:46]:<46} │
│ Plotly:      {row['plotly_type'][:46]:<46} │
└─────────────────────────────────────────────────────────────┘"""


def format_palette(row: dict) -> str:
    """Format palette result."""
    colors = f"{row['color_primary']} | {row['color_secondary']} | {row['color_accent']}"
    return f"""
┌─────────────────────────────────────────────────────────────┐
│ {row['name']:<59} │
├─────────────────────────────────────────────────────────────┤
│ Domain:      {row['domain']:<46} │
│ Mood:        {row['mood']:<46} │
│ Colors:      {colors[:46]:<46} │
│ Best For:    {row['best_for'][:46]:<46} │
│ Seaborn:     {row['seaborn_palette']:<46} │
└─────────────────────────────────────────────────────────────┘"""


def format_rule(row: dict) -> str:
    """Format reasoning rule result."""
    return f"""
┌─────────────────────────────────────────────────────────────┐
│ [{row['priority'].upper()}] {row['trigger']:<52} │
├─────────────────────────────────────────────────────────────┤
│ Condition:      {row['condition'][:42]:<42} │
│ Recommendation: {row['recommendation'][:42]:<42} │
│ Action:         {row['action'][:42]:<42} │
│ Rationale:      {row['rationale'][:42]:<42} │
│ Domain:         {row['domain']:<42} │
└─────────────────────────────────────────────────────────────┘"""


def format_style(row: dict) -> str:
    """Format visualization style result."""
    return f"""
┌─────────────────────────────────────────────────────────────┐
│ {row['name']:<59} │
├─────────────────────────────────────────────────────────────┤
│ Category:    {row['category']:<46} │
│ Fonts:       {row['font_title'][:20] + ' / ' + row['font_body'][:20]:<46} │
│ Figure Size: {row['figsize_default']:<46} │
│ DPI:         {row['dpi']:<46} │
│ Best For:    {row['best_for'][:46]:<46} │
│ Matplotlib:  {row['matplotlib_style']:<46} │
│ Seaborn:     {row['seaborn_context']:<46} │
└─────────────────────────────────────────────────────────────┘"""


FORMATTERS = {
    "analysis": format_analysis,
    "visualization": format_visualization,
    "palette": format_palette,
    "rule": format_rule,
    "style": format_style,
}


def main():
    parser = argparse.ArgumentParser(
        description="Search Data Pro Max knowledge base",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 search.py "correlation"
  python3 search.py --type analysis "t-test"
  python3 search.py --type visualization "distribution"
  python3 search.py --type palette --domain healthcare
  python3 search.py --type rule "missing"
  python3 search.py --domain survey --category inferential
        """,
    )
    parser.add_argument("query", nargs="?", help="Text to search")
    parser.add_argument(
        "--type",
        "-t",
        choices=["analysis", "visualization", "palette", "rule", "style", "all"],
        default="all",
        help="Type of data to search",
    )
    parser.add_argument("--domain", "-d", help="Filter by domain")
    parser.add_argument("--category", "-c", help="Filter by category")
    parser.add_argument("--limit", "-l", type=int, default=10, help="Max results")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if not args.query and not args.domain and not args.category:
        parser.print_help()
        return

    # Build filters
    filters = {}
    if args.domain:
        filters["domain"] = args.domain
    if args.category:
        filters["category"] = args.category

    # Determine which files to search
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
        print(f" DATA PRO MAX - {len(all_results)} Results")
        print(f"{'='*65}")
        
        for row in all_results[: args.limit]:
            formatter = FORMATTERS.get(row["_type"], str)
            print(formatter(row))
        
        if len(all_results) > args.limit:
            print(f"\n... and {len(all_results) - args.limit} more results")


if __name__ == "__main__":
    main()
