import pandas as pd
import argparse
import sys
import re
import unicodedata

# Mapping of State Codes to Regions in Brazil
REGION_MAP = {
    'AC': 'Norte', 'AM': 'Norte', 'AP': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
    'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
    'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste',
    'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
    'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul'
}

def normalize_string(s):
    if not isinstance(s, str): return ""
    # Remove accents and lowercase
    nfkd_form = unicodedata.normalize('NFKD', s)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower().strip()

def parse_geo_string(val):
    """
    Parses strings like 'Duartina - SP' or 'Itatinga-SP' 
    returns (city_norm, state_code, region)
    """
    if not isinstance(val, str): return "", "", ""
    
    # Try to extract UF (last 2 letters after a separator or at the end)
    match = re.search(r'[-/]\s*([A-Z]{2})$|([A-Z]{2})$', val.upper())
    state_code = match.group(1) or match.group(2) if match else ""
    
    # Remove state code and separators from city name
    city_raw = re.sub(r'[-/]\s*[A-Z]{2}$|[A-Z]{2}$', '', val).strip()
    city_norm = normalize_string(city_raw)
    
    region = REGION_MAP.get(state_code, "Desconhecido")
    
    return city_norm, state_code, region

def main():
    parser = argparse.ArgumentParser(description="Geo Municipality Mapper")
    parser.add_argument("input", help="Input CSV file")
    parser.add_argument("column", help="Column name containing geo strings")
    parser.add_argument("-o", "--output", help="Output CSV", default="geo_normalized.csv")
    
    args = parser.parse_args()
    
    try:
        df = pd.read_csv(args.input)
        
        if args.column not in df.columns:
            print(f"❌ Column '{args.column}' not found.")
            sys.exit(1)
            
        results = df[args.column].apply(parse_geo_string)
        df[['City_Norm', 'State_Code', 'Region']] = pd.DataFrame(results.tolist(), index=df.index)
        
        df.to_csv(args.output, index=False)
        print(f"✅ Geographic normalization complete. Results saved to {args.output}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
