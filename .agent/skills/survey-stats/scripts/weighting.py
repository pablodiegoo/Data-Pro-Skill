
import pandas as pd
import numpy as np

def rake_weights(df, target_distributions, max_iter=100, tolerance=0.001):
    """
    Calculates weights using the Raking (Iterative Proportional Fitting) method.
    
    Args:
        df: Pandas DataFrame containing the sample data.
        target_distributions: Dictionary where keys are column names and values are 
                              dictionaries of {category: target_proportion}.
                              Example: {'gender': {'Male': 0.49, 'Female': 0.51}}
        max_iter: Max iterations.
        tolerance: Convergence threshold.
        
    Returns:
        Series of weights.
    """
    # Initialize weights to 1.0
    df = df.copy() # Don't modify original
    df['weight'] = 1.0
    
    # Check that targets sum to 1 (approx)
    for col, targets in target_distributions.items():
        total = sum(targets.values())
        if abs(total - 1.0) > 0.01:
            print(f"Warning: Target proportions for '{col}' sum to {total}, not 1.0. Normalizing.")
            # Normalize
            target_distributions[col] = {k: v/total for k,v in targets.items()}
            
    for i in range(max_iter):
        old_weights = df['weight'].copy()
        
        # Iterate through each weighting variable
        for col, targets in target_distributions.items():
            # Calculate current weighted proportions
            current_counts = df.groupby(col)['weight'].sum()
            total_weight = current_counts.sum()
            
            # Update weights
            # New Weight = Old Weight * (Target Prop / Current Prop)
            for category, target_prop in targets.items():
                if category in current_counts.index:
                    current_prop = current_counts[category] / total_weight
                    if current_prop > 0:
                        factor = target_prop / current_prop
                        # Apply factor only to rows with this category
                        df.loc[df[col] == category, 'weight'] *= factor
                else:
                    print(f"Warning: Category '{category}' in targets missing from sample column '{col}'.")
                    
        # Check convergence
        weight_diff = (df['weight'] - old_weights).abs().sum()
        if weight_diff < tolerance:
            print(f"Raking converged after {i+1} iterations.")
            break
            
    return df['weight']
