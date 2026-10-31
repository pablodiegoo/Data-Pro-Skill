
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


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Raking (Iterative Proportional Fitting) Weighting CLI")
    parser.add_argument("input", help="Input CSV dataset")
    parser.add_argument("--targets", required=True, help="JSON file or inline JSON string of target distributions")
    parser.add_argument("-o", "--output", default=".dps/outputs/setup/weighted_data.csv", help="Output weighted CSV path")
    args = parser.parse_args()

    df_in = pd.read_csv(args.input)
    t_path = Path(args.targets)
    targets_dict = json.loads(t_path.read_text(encoding="utf-8")) if t_path.is_file() else json.loads(args.targets)
    w_series = rake_weights(df_in, targets_dict)
    df_in["weight"] = w_series
    n_eff = float((w_series.sum() ** 2) / ((w_series ** 2).sum())) if (w_series ** 2).sum() > 0 else len(df_in)
    deff = len(df_in) / n_eff if n_eff > 0 else 1.0
    out_p = Path(args.output)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    df_in.to_csv(out_p, index=False)
    print(f"✅ Raking complete -> {out_p} (N={len(df_in)}, Kish N_eff={n_eff:.1f}, DEFF={deff:.3f})")
