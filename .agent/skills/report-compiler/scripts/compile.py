
import subprocess
import shutil
import argparse
import sys
import os

def check_dependencies():
    """Checks if pandoc is installed."""
    if not shutil.which("pandoc"):
        print("Error: 'pandoc' is not installed. Please install it using: sudo apt install pandoc texlive-xetex")
        return False
    return True

def compile_document(input_file, output_format="pdf", output_file=None):
    """
    Compiles markdown to PDF or DOCX using Pandoc.
    """
    if not check_dependencies():
        return

    if not output_file:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}.{output_format}"

    cmd = ["pandoc", input_file, "-o", output_file]

    # Add extra args for better PDF looking
    if output_format == "pdf":
         # Use geometry to set margins
        cmd.extend(["-V", "geometry:margin=1in"])
        # Use a nice font if possible (optional, keeping it simple for now)
        cmd.extend(["--pdf-engine=xelatex"]) 
        # Add table of contents
        cmd.extend(["--toc"])
        
    print(f"Compiling '{input_file}' to '{output_file}'...")
    try:
        subprocess.run(cmd, check=True)
        print(f"Success! Document saved to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling document: {e}")
    except FileNotFoundError:
        print("Error: Pandoc or PDF engine not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile Markdown to PDF/DOCX.")
    parser.add_argument("input_file", help="Path to input Markdown file.")
    parser.add_argument("-f", "--format", choices=["pdf", "docx"], default="pdf", help="Output format.")
    parser.add_argument("-o", "--output", help="Output file path.")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' not found.")
        sys.exit(1)
        
    compile_document(args.input_file, args.format, args.output)
