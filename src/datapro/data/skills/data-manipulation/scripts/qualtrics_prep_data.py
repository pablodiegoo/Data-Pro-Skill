import sys
print("Starting python script...", flush=True)
import pandas as pd
import numpy as np
import os

def prep_data():
    """Reads raw CSV, applies column type mapping, cleans data and exports to Parquet."""
    
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    input_file = os.path.join(project_dir, 'database', 'raw', '#1252983925 - OS18 - Sebrae SP - Marketplace - Base Integrada.xlsx - BASE.csv')
    processed_dir = os.path.join(project_dir, 'database', 'processed')
    output_file = os.path.join(processed_dir, 'OS18_Marketplace_Processed.parquet')

    print(f"Reading {input_file}...", flush=True)
    
    # Read CSV (skip line 1 and 2 if they are survey metadata headers, assuming row 0 is main header and 1/2 are subheaders or import text)
    # Qualtrics normally has 3 header rows. Let's read row 0 as header, and drop row 1, 2.
    df = pd.read_csv(input_file, header=0)
    
    # Qualtrics exports usually have two extra header rows (survey structure and import IDs)
    if 'Data de Início' in df.columns:
        if pd.isna(df.iloc[0]['Data de Início']) or 'ImportId' in str(df.iloc[1]['Data de Início']):
             df = df.iloc[2:].reset_index(drop=True)
             
    # To be safe, if we see strings like "Response Type" or "Tipo de Resposta" in row 0 for 'Status'
    if 'Tipo de Resposta' in df.columns and df['Tipo de Resposta'].iloc[0] in ['Response Type', 'Tipo de Resposta']:
        df = df.iloc[2:].reset_index(drop=True)
        
    print(f"Initial shape after removing Qualtrics metadata rows: {df.shape}", flush=True)
    
    # --- Column Renaming (Optional, can be done if names are too long, but we keep them mostly intact or map them via a dictionary later) ---
    
    # --- Basic Data Cleaning ---
    # Convert dates
    if 'Data de Início' in df.columns:
        df['Data de Início'] = pd.to_datetime(df['Data de Início'], errors='coerce')
    if 'Data de Término' in df.columns:
        df['Data de Término'] = pd.to_datetime(df['Data de Término'], errors='coerce')
        
    # Convert purely numeric columns
    cols_to_numeric = [
        'Progresso', 'Duração (em segundos)', 
    ]
    for col in cols_to_numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Remove unfinished responses if needed
    if 'Concluído' in df.columns:
        # True is 1 or 'True' in Qualtrics
        df = df[df['Concluído'].astype(str).str.lower().isin(['1', 'true', 'verdadeiro'])]
        print(f"Shape after keeping only finished responses: {df.shape}", flush=True)

    # --- Scale Mapping 1 to 5 ---
    # We will map standard Likert scales to numeric.
    # We need to look for columns with 1 to 5 values or string equivalents.
    scale_cols = [c for c in df.columns if "De 1 a 5, o quanto" in c or "RU – Estimulada 1 = nada impacta | 5 = impacta" in c]
    scale_map = {
        '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
        '1 - Nada': 1, '5 - Muito': 5,
        'Não sei': np.nan, 'NS/NR': np.nan, 'Não se aplica / Não tem suporte': np.nan
    }
    
    # Apply to generic 1-5 scale questions
    for c in scale_cols:
        df[c] = df[c].astype(str).str.strip().map(lambda x: scale_map.get(x, x))
        df[c] = pd.to_numeric(df[c], errors='coerce')
        
    # Nível de satisfação
    satis_cols = [c for c in df.columns if "Qual seu nível de satisfação" in c]
    satis_map = {
        'Muito insatisfeito': 1,
        'Insatisfeito': 2,
        'Neutro': 3,
        'Satisfeito': 4,
        'Muito satisfeito': 5,
        'Nunca precisei / Não se aplica': np.nan
    }
    for c in satis_cols:
        df[c] = df[c].astype(str).str.strip().map(satis_map)

    # Convert age to categories properly if needed, although survey seems to have pre-defined '25 a 34 anos', etc.

    os.makedirs(processed_dir, exist_ok=True)
    df.to_parquet(output_file, index=False)
    print(f"Successfully processed {df.shape[0]} rows and saved to Parquet.", flush=True)
    print(df.head(3), flush=True)

if __name__ == "__main__":
    prep_data()
