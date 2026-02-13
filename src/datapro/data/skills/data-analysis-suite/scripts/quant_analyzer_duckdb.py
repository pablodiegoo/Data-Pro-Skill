
import json
import argparse
import sys
import os
from datapro.engine import DataEngine

def main():
    parser = argparse.ArgumentParser(description="Survey Quantitative Analyzer (Powered by DuckDB)")
    parser.add_argument("input", help="Input CSV file")
    parser.add_argument("config", help="Configuration JSON file")
    parser.add_argument("-o", "--output", help="Output Parquet file", default="processed_output.parquet")
    
    args = parser.parse_args()
    
    try:
        # Load config
        with open(args.config, 'r') as f:
            config = json.load(f)
            
        # Initialize DuckDB Engine
        engine = DataEngine()
        table_name = "survey_data"
        
        # Load CSV into DuckDB
        engine.load_csv(args.input, table_name)
        
        # Process Logic (SQL-powered)
        print("🧠 Processing survey logic using SQL...")
        engine.process_survey_logic(table_name, config)
        
        # Export to Parquet (Compressed)
        engine.export_to_parquet(table_name, args.output)
        
        print(f"✅ Analysis complete. Processed data saved as Parquet to {args.output}")
        engine.close()
        
    except Exception as e:
        print(f"❌ Error during DuckDB analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
