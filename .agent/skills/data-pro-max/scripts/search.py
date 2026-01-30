#!/usr/bin/env python3
import sys
import re
from pathlib import Path

FRAMEWORK_PATH = Path(__file__).parent.parent / "data" / "framework.md"

def load_framework():
    if not FRAMEWORK_PATH.exists():
        print(f"Error: Framework file not found at {FRAMEWORK_PATH}")
        sys.exit(1)
    return FRAMEWORK_PATH.read_text(encoding='utf-8')

def search_framework(query):
    content = load_framework()
    lines = content.split('\n')
    
    matches = []
    current_section = None
    buffer = []
    recording = False
    
    # Simple semantic-ish search: find headers or lines containing query
    # and return context around them.
    
    print(f"\n🔍 Searching Framework for: '{query}'\n" + "="*50)
    
    count = 0
    for i, line in enumerate(lines):
        if line.startswith('#'):
            current_section = line.strip()
            
        if query.lower() in line.lower():
            count += 1
            print(f"\n[Match {count}] Section: {current_section or 'General'}")
            print(f"Line {i+1}: {line.strip()}")
            
            # Print context (5 lines before and 10 after)
            start = max(0, i - 2)
            end = min(len(lines), i + 15)
            
            print("-" * 20)
            for j in range(start, end):
                prefix = "> " if j == i else "  "
                print(f"{prefix}{lines[j]}")
            print("-" * 20)
            
            if count >= 3: # Limit to 3 matches to avoid spam
                print("\n... (More matches found, restrict query for precision) ...")
                break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 search.py <query>")
        sys.exit(1)
    
    search_framework(sys.argv[1])
