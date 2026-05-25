#!/usr/bin/env python3
import os
import re
import argparse
from pathlib import Path

# Mapping of keywords to .agent directories
CATEGORY_MAP = {
    'memory': [
        r'rule', r'fact', r'convention', r'standard', r'immutable', r'preference', 
        r'pattern', r'memory', r'context', r'global', r'persona'
    ],
    'workflows': [
        r'workflow', r'process', r'step', r'procedure', r'how-to', r'guide', 
        r'pipeline', r'deploy', r'setup', r'instruction', r'sequence'
    ],
    'tasks': [
        r'task', r'plan', r'todo', r'backlog', r'sprint', r'milestone', 
        r'requirement', r'objective', r'goal', r'phase', r'implementation'
    ],
    'references': [
        r'reference', r'api', r'doc', r'schema', r'manual', r'external', 
        r'library', r'specification', r'table', r'matrix', r'list'
    ]
}

def analyze_section(content):
    """Suggests a category based on keyword density and patterns."""
    content_lower = content.lower()
    scores = {cat: 0 for cat in CATEGORY_MAP}
    
    for cat, keywords in CATEGORY_MAP.items():
        for kw in keywords:
            # Count occurrences of keywords
            scores[cat] += len(re.findall(kw, content_lower))
            
    # Check for specific structural markers
    if '[' in content and ']' in content and ('x' in content or '/' in content):
        scores['tasks'] += 5 # High probability of being a task list
        
    if '// turbo' in content:
        scores['workflows'] += 10 # Strong workflow marker
        
    if '|' in content and '-' in content:
        scores['references'] += 2 # Tables are often references
        
    # Return the category with highest score
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if sorted_scores[0][1] > 0:
        return sorted_scores[0][0]
    return 'references' # Default

def group_sections(input_dir, move=False):
    """Analyzes and optionally moves files into category subdirectories."""
    path = Path(input_dir)
    if not path.is_dir():
        print(f"Error: {input_dir} is not a directory.")
        return

    report = []
    
    for file_path in sorted(path.glob("*.md")):
        if file_path.name.startswith("00_"): # Skip index and preamble
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        category = analyze_section(content)
        report.append(f"{file_path.name} → {category}")
        
        if move:
            dest_dir = path / category
            dest_dir.mkdir(exist_ok=True)
            file_path.rename(dest_dir / file_path.name)
            
    print("\n".join(report))
    if move:
        print(f"\nFiles moved into subdirectories in {input_dir}")
    else:
        print("\nReview suggestions above. Run with --move to execute reorganization.")

def main():
    parser = argparse.ArgumentParser(description="Semantic grouping for decomposed documentation.")
    parser.add_argument("directory", help="Directory containing .md chunks")
    parser.add_argument("--move", action="store_true", help="Actually move files into subdirectories")
    
    args = parser.parse_args()
    group_sections(args.directory, args.move)

if __name__ == "__main__":
    main()
