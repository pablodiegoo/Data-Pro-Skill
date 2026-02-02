"""
DataPro Dictionary Mapper Module - Variable name → label mapping.
"""

import json
import pandas as pd
from typing import Dict, Any, Optional


class DictionaryMapper:
    """Class to handle mapping between short variable names and full question labels."""
    
    def __init__(self, mapping: Optional[Dict[str, Any]] = None):
        self.mapping = mapping or {}
        
    def infer_from_file(self, input_file: str, header_row: int = 0) -> bool:
        """
        Reads a CSV/Excel and generates a mapping from index/col_name to full label.
        Useful when the first row contains the full question text.
        """
        try:
            if input_file.lower().endswith('.csv'):
                df = pd.read_csv(input_file, header=header_row, nrows=0)
            elif input_file.lower().endswith(('.xlsx', '.xls')):
                df = pd.read_excel(input_file, header=header_row, nrows=0)
            else:
                return False

            self.mapping = {}
            for i, col in enumerate(df.columns):
                key = f"col_{i}"
                label = str(col).strip()
                self.mapping[key] = {
                    "index": i,
                    "original_name": col,
                    "label": label
                }
            return True
        except Exception:
            return False

    def save_json(self, output_file: str) -> bool:
        """Save current mapping to JSON file."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.mapping, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    def load_json(self, input_file: str) -> bool:
        """Load mapping from JSON file."""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                self.mapping = json.load(f)
            return True
        except Exception:
            return False

    def get_label(self, key: str) -> str:
        """Get the full label for a key."""
        if key in self.mapping:
            return self.mapping[key].get("label", key)
        return key


def infer_mapping(input_file: str, output_file: str, header_row: int = 0) -> bool:
    """Helper function for CLI/standalone use."""
    mapper = DictionaryMapper()
    if mapper.infer_from_file(input_file, header_row):
        return mapper.save_json(output_file)
    return False
