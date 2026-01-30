import pandas as pd
import numpy as np

def weighted_crosstab(df, index_col, columns_col, weight_col='weight', normalize=True):
    """
    Generates a weighted crosstab.
    
    Args:
        df: DataFrame
        index_col: Column for rows (e.g., 'Gender')
        columns_col: Column for columns (e.g., 'Satisfaction')
        weight_col: Column containing weights
        normalize: 'index' (row %), 'columns' (col %), 'all', or False.
        
    Returns:
        DataFrame with weighted counts or percenages.
    """
    # Defensive check
    if weight_col not in df.columns:
        print(f"Warning: {weight_col} not found. Using unweighted counts.")
        weights = np.ones(len(df))
    else:
        weights = df[weight_col]

    ct = pd.crosstab(
        index=df[index_col],
        columns=df[columns_col],
        values=weights,
        aggfunc='sum',
        normalize=normalize
    )
    
    if normalize:
        ct = ct * 100
        
    return ct

def run_automated_crosstabs(df, target_cols, banner_cols, weight_col='weight', output_dir='output'):
    """
    Runs a banner (demographic splits) against a list of target questions.
    
    Args:
        df: DataFrame
        target_cols: List of question columns (e.g., Q1, Q2...)
        banner_cols: List of banner columns (e.g., Region, Gender)
    """
    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for var in target_cols:
        for banner in banner_cols:
            try:
                msg = f"Processing {var} x {banner}..."
                print(msg)
                ct = weighted_crosstab(df, var, banner, weight_col)
                
                # Save
                safe_var = var.replace('/', '_').replace(' ', '_')[:20]
                safe_banner = banner.replace('/', '_').replace(' ', '_')[:20]
                filename = f"{output_dir}/Example_{safe_var}_by_{safe_banner}.csv"
                ct.to_csv(filename)
            except Exception as e:
                print(f"Skipping {var} x {banner}: {e}")
