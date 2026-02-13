#!/usr/bin/env python3
import pandas as pd
import argparse
import json
import os

def infer_mapping(input_file, output_file, header_row=0):
    """
    Reads a CSV and generates a mapping from index/col_name to full label.
    Useful when the first row contains the full question text.
    """
    try:
        # Read only the header
        if input_file.lower().endswith('.csv'):
            df = pd.read_csv(input_file, header=header_row, nrows=0)
        elif input_file.lower().endswith('.xlsx'):
            df = pd.read_excel(input_file, header=header_row, nrows=0)
        else:
            print(f"❌ Error: Unsupported file format {input_file}")
            return False

        mapping = {}
        for i, col in enumerate(df.columns):
            # Create a simplified key (e.g., "col_0", "col_1") or use the column name if short
            key = f"col_{i}"
            # The value is the column header itself (which is often the question)
            label = str(col).strip()
            mapping[key] = {
                "index": i,
                "original_name": col,
                "label": label
            }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=4, ensure_ascii=False)
            
        print(f"✅ Mapping saved to {output_file}")
        return True

    except Exception as e:
        print(f"❌ Error extracting mapping: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Infer Dictionary Mapping from Raw Data File")
    parser.add_argument("input_file", help="Path to raw CSV/Excel file")
    parser.add_argument("-o", "--output", default="mapping.json", help="Output JSON map")
    parser.add_argument("--header", type=int, default=0, help="Row number containing the questions (0-indexed)")
    
    args = parser.parse_args()
    infer_mapping(args.input_file, args.output, args.header)
