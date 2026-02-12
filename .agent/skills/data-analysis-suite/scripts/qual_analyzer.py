import pandas as pd
import argparse
import sys
import re
from collections import Counter

# Basic Portuguese stop words
STOP_WORDS = set([
    "a", "o", "as", "os", "um", "uma", "uns", "umas", "de", "do", "da", "dos", "das",
    "em", "no", "na", "nos", "nas", "com", "por", "para", "que", "se", "como", "e", "é",
    "ou", "mas", "não", "foi", "está", "tem", "pelo", "pela", "também", "muito", "mais"
])

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # Remove special characters and lowercase
    text = re.sub(r'[^\w\s]', '', text).lower()
    # Tokenize and remove stop words
    words = [w for w in text.split() if w not in STOP_WORDS and len(w) > 2]
    return words

def main():
    parser = argparse.ArgumentParser(description="Survey Qualitative Analyzer")
    parser.add_argument("input", help="Input CSV file")
    parser.add_argument("column", help="Column name to analyze")
    parser.add_argument("-o", "--output", help="Output frequency CSV", default="word_freq.csv")
    parser.add_argument("--filter", help="Optional filter in 'Col=Value' format")
    
    args = parser.parse_args()
    
    try:
        df = pd.read_csv(args.input)
        
        # Apply filter if provided
        if args.filter:
            f_col, f_val = args.filter.split("=")
            df = df[df[f_col].astype(str).str.contains(f_val, case=False, na=False)]
            
        if args.column not in df.columns:
            print(f"❌ Column '{args.column}' not found in CSV.")
            sys.exit(1)
            
        all_words = []
        for text in df[args.column]:
            all_words.extend(clean_text(text))
            
        counts = Counter(all_words)
        freq_df = pd.DataFrame(counts.items(), columns=['Word', 'Frequency']).sort_values(by='Frequency', ascending=False)
        
        freq_df.to_csv(args.output, index=False)
        print(f"✅ Qualitative analysis complete. Word frequencies saved to {args.output}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
