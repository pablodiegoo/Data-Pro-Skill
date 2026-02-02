"""
DataPro Search Module - Query the knowledge base.
"""

import csv
from pathlib import Path
from typing import Optional

# Package data directory
DATA_DIR = Path(__file__).parent / "data"

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
        return []
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def search_knowledge_base(
    query: Optional[str] = None,
    search_type: str = "all",
    domain: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 10,
) -> list[dict]:
    """
    Search the DataPro knowledge base.
    
    Args:
        query: Text to search in all fields
        search_type: One of 'analysis', 'visualization', 'palette', 'rule', 'style', 'all'
        domain: Filter by domain (survey, healthcare, financial, etc.)
        category: Filter by category (descriptive, inferential, etc.)
        limit: Maximum number of results
    
    Returns:
        List of matching records as dictionaries
    
    Example:
        >>> from datapro import search_knowledge_base
        >>> results = search_knowledge_base("correlation", search_type="analysis")
        >>> for r in results:
        ...     print(r['name'], r['python_function'])
    """
    # Build filters
    filters = {}
    if domain:
        filters["domain"] = domain
    if category:
        filters["category"] = category
    
    query_lower = query.lower() if query else None
    
    # Determine which files to search
    search_types = list(FILES.keys()) if search_type == "all" else [search_type]
    
    all_results = []
    for stype in search_types:
        if stype not in FILES:
            continue
        data = load_csv(FILES[stype])
        
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
            
            row["_type"] = stype
            all_results.append(row)
            
            if len(all_results) >= limit:
                break
        
        if len(all_results) >= limit:
            break
    
    return all_results


def get_analysis_types(domain: Optional[str] = None) -> list[dict]:
    """Get all available analysis types, optionally filtered by domain."""
    return search_knowledge_base(search_type="analysis", domain=domain, limit=100)


def get_visualizations(data_type: Optional[str] = None) -> list[dict]:
    """Get visualization recommendations."""
    return search_knowledge_base(query=data_type, search_type="visualization", limit=100)


def get_palettes(domain: str = "general") -> list[dict]:
    """Get color palettes for a specific domain."""
    return search_knowledge_base(search_type="palette", domain=domain, limit=50)


def get_rules(trigger: Optional[str] = None) -> list[dict]:
    """Get reasoning rules, optionally filtered by trigger."""
    return search_knowledge_base(query=trigger, search_type="rule", limit=100)
