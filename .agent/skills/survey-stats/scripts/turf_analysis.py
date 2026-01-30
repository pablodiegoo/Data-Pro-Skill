
import pandas as pd
import numpy as np
from itertools import combinations

def run_turf_analysis(df, items, n_max_size=4):
    """
    Performs TURF Analysis (Total Unduplicated Reach and Frequency).
    
    Args:
        df: DataFrame containing the data (binary 0/1 or boolean).
        items: List of column names to include in the analysis.
        n_max_size: Maximum size of combination to check (default 4).
        
    Returns:
        DataFrame with columns ['Size', 'Combination', 'Reach', 'Reach_Percent']
    """
    # Filter valid items
    valid_items = [col for col in items if col in df.columns]
    
    # Create binary matrix (force 0/1)
    # Assumes NaNs are 0 (not reached) if data is sparse
    data = df[valid_items].fillna(0).astype(bool).astype(int)
    n_respondents = len(df)
    
    results = []
    
    for size in range(1, n_max_size + 1):
        best_reach = -1
        best_combo = None
        
        # Check all combinations
        for combo in combinations(valid_items, size):
            # Calculate reach: user is reached if sum across combo columns > 0
            # Faster numpy implementation
            sub_matrix = data[list(combo)].values
            # Check if ANY item in row is 1
            reached_count = np.any(sub_matrix, axis=1).sum()
            reach_pct = reached_count / n_respondents
            
            if reach_pct > best_reach:
                best_reach = reach_pct
                best_combo = combo
        
        results.append({
            'Size': size,
            'Combination': ", ".join(best_combo),
            'Reach_Count': int(best_reach * n_respondents),
            'Reach_Percent': round(best_reach * 100, 2)
        })
        
    return pd.DataFrame(results)
