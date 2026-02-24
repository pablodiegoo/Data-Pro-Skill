# Python Programmatic Markdown Generation Rules

## Context
When writing Python scripts that generate `.md` files dynamically (e.g., EDA Reports, Analysis Summaries), a common anti-pattern causes literal `\n` characters to appear in the output document instead of actual line breaks.

## The Rule
1. **Never use deep-nested escaped backslashes in multi-line f-strings meant for Markdown.**
2. When creating multi-line strings for Markdown blocks, use explicit `""" ... """` triple quotes for the block structure, rather than string concatenation with explicit `\n`.
3. If you must inject variables containing lists or newlines inside an f-string, construct the variable completely *before* injecting it into the f-string.

### Bad Pattern (Anti-Pattern)
```python
# The \\n becomes a literal string "\n" in the markdown file
markdown_content = f"### Main Points\\n\\n1. Item 1\\n2. Item 2" 
```

### Good Pattern
```python
# Use standard triple quotes allowing natural line breaks
features = ["Item 1", "Item 2"]
features_str = "\n".join([f"{i+1}. {x}" for i, x in enumerate(features)])

markdown_content = f"""### Main Points

{features_str}
"""
```

### Impact
Enforcing this prevents malformed `.md` report outputs and eliminates iterative debugging cycles trying to fix line breaks in generated documents.
