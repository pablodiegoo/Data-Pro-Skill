
import os
import re
import argparse
from pathlib import Path

def sanitize_filename(name):
    """
    Sanitizes a string to be used as a filename.
    Limit length and remove illegal chars.
    """
    # Remove invalid characters and replace spaces with underscores
    # Keep only alphanumerics
    s = re.sub(r'[^\w\s-]', '', name).strip().lower()
    s = re.sub(r'[-\s]+', '_', s)
    return s[:50] # Limit length

def split_markdown(input_file, output_dir, pattern=None, level=2, min_lines=3):
    """
    Splits a file into smaller files based on a regex pattern or markdown header level.
    
    Args:
        input_file (str): Path to the file to split.
        output_dir (str): Directory to save the split files.
        pattern (str): Custom regex pattern for splitting headers. If None, uses Markdown headers.
        level (int): The header level to split by if using default markdown splitting.
        min_lines (int): Minimum lines of content to justify a separate file.
    """
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"Error: Could not read '{input_file}'. Ensure it is a valid text file.")
        return

    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Determine splitting regex
    if pattern:
        # User provided regex. We assume it captures the Title group.
        # If the user regex doesn't have a capturing group for the title, it might fail to extract title.
        # We'll wrap it in () if simple, but for complex regex rely on user to provide group 1.
        regex = re.compile(f"({pattern})", re.MULTILINE) if "(" not in pattern else re.compile(pattern, re.MULTILINE)
        print(f"Using custom split pattern: {pattern}")
    else:
        # Default Markdown split: matches ## Title
        # Regex explanation:
        # ^           : Start of line
        # (#){level}  : Matches exactly 'level' number of hashes
        # \s+         : One or more spaces
        # (.+)$       : Captures the rest of the line as Group 2 (Title)
        regex = re.compile(r'^' + '#' * level + r'\s+(.+)$', re.MULTILINE)
        print(f"Using Markdown split level {level}")
    
    # Split content.
    parts = regex.split(content)
    
    # parts[0] is everything before the first match
    preamble = parts[0].strip()
    if preamble:
        preamble_path = os.path.join(output_dir, "00_preamble.md")
        with open(preamble_path, 'w', encoding='utf-8') as f:
            f.write(preamble)
        # print(f"Created: {preamble_path}")

    # parts structure depends on capturing groups.
    # If regex has 1 capturing group (the title), split returns: [pre, title1, body1, title2, body2...]
    # If regex captures the whole delimiter but also subgroups, it might be more complex.
    # Our default markdown regex `^## (.+)$` has TWO groups technically? No, `^##\s+(.+)$`.
    # Actually wait. `re.split` returns capturing groups.
    # Pattern `^## (.+)$` has ONE capturing group: the title.
    # So `parts` = [pre, title1, body1, title2, body2...]
    
    # If custom pattern is used, we need to be careful.
    
    count = 0
    toc = []
    
    # Iterate in steps of 2 (title, body)
    # Note: If the split pattern matched but captured multiple groups, this loop logic breaks.
    # We assume 1 capturing group for the 'Title'.
    
    if len(parts) < 2:
        print("No sections found. Try checking your regex pattern or header level.")
        return

    for i in range(1, len(parts), 2):
        if i+1 >= len(parts):
            break
            
        title_raw = parts[i].strip()
        body = parts[i+1].strip()
        
        # Clean title for filename
        # If title is very long (e.g. if regex matched a whole paragraph), truncate it.
        # Ideally regex matches a short header.
        safe_title = sanitize_filename(title_raw)
        if not safe_title:
            safe_title = f"section_{count}"
            
        # Check explicit length constraint
        if len(body.splitlines()) < min_lines:
             pass # Write anyway for now

        # Add index prefix to keep order
        filename = f"{count+1:02d}_{safe_title}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Reconstruct the header? 
            # If using regex, we don't know the header format. Just write the title as an H1.
            f.write(f"# {title_raw}\n\n{body}\n")
        
        print(f"Created: {filepath}")
        toc.append(f"- [{title_raw}]({filename})")
        count += 1

    # Create an index file
    if toc:
        index_path = os.path.join(output_dir, "00_INDEX.md")
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(f"# Index for {os.path.basename(input_file)}\n\n")
            f.write("\n".join(toc))
        print(f"Created: {index_path}")
    
    print(f"\nSuccessfully split '{input_file}' into {count} files in '{output_dir}'.")

def main():
    parser = argparse.ArgumentParser(description="Split a text/markdown file into smaller files based on headers/patterns.")
    parser.add_argument("input_file", help="Path to the input file.")
    parser.add_argument("-o", "--output", help="Output directory.")
    parser.add_argument("-l", "--level", type=int, default=2, help="Markdown header level to split by (default: 2 for ##).")
    parser.add_argument("-r", "--regex", help="Custom regex pattern to split by. Surround title in parenthesis (group 1). matches MULTILINE.")
    parser.add_argument("--min", type=int, default=3, help="Min lines")
    
    args = parser.parse_args()
    
    input_path = args.input_file
    if args.output:
        output_dir = args.output
    else:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_dir = os.path.join(os.path.dirname(input_path), f"{base_name}_split")
    
    split_markdown(input_path, output_dir, pattern=args.regex, level=args.level, min_lines=args.min)

if __name__ == "__main__":
    main()
