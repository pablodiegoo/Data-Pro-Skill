import pandas as pd
import argparse
import sys
import re
from collections import Counter
from pathlib import Path

# Default English stop words (minimal)
DEFAULT_STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"
}

def load_stopwords(filepath):
    """Load stop words from a file (one per line)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return set(line.strip().lower() for line in f if line.strip())
    except Exception as e:
        print(f"⚠️ Warning: Could not load stopwords from {filepath}: {e}")
        return set()

def clean_text(text, stop_words):
    if not isinstance(text, str):
        return []
    # Remove special characters and lowercase
    text = re.sub(r'[^\w\s]', '', text).lower()
    # Tokenize and remove stop words
    words = [w for w in text.split() if w not in stop_words and len(w) > 2]
    return words

def main():
    parser = argparse.ArgumentParser(description="Survey Qualitative Analyzer")
    parser.add_argument("input", help="Input CSV file")
    parser.add_argument("column", help="Column name to analyze")
    parser.add_argument("-o", "--output", help="Output frequency CSV", default="word_freq.csv")
    parser.add_argument("--filter", help="Optional filter in 'Col=Value' format")
    parser.add_argument("--stopwords", help="Path to stopwords file (txt, one per line)", default=None)
    
    args = parser.parse_args()
    
    try:
        # Load stopwords
        if args.stopwords:
            stop_words = load_stopwords(args.stopwords)
            print(f"ℹ️ Loaded {len(stop_words)} stop words from {args.stopwords}")
        else:
            stop_words = DEFAULT_STOP_WORDS
            print("ℹ️ Using default English stop words")

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
            all_words.extend(clean_text(text, stop_words))
            
        counts = Counter(all_words)
        freq_df = pd.DataFrame(counts.items(), columns=['Word', 'Frequency']).sort_values(by='Frequency', ascending=False)
        
        freq_df.to_csv(args.output, index=False)
        print(f"✅ Qualitative analysis complete. Word frequencies saved to {args.output}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
