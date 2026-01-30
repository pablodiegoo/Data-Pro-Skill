
import pandas as pd
import numpy as np
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo

def run_factor_analysis(df, cols, n_factors=None, rotation='varimax'):
    """
    Performs Exploratory Factor Analysis.
    
    Args:
        df: DataFrame
        cols: List of column names (Likert scale items, etc.)
        n_factors: Number of factors (if None, determines based on Eigenvalues > 1)
        rotation: 'varimax', 'promax', or None
        
    Returns:
        loadings: Factor loadings DataFrame
        variance: Variance explained
    """
    data = df[cols].dropna()
    
    # 1. Adequacy Tests
    chi_square_value, p_value = calculate_bartlett_sphericity(data)
    kmo_all, kmo_model = calculate_kmo(data)
    
    print(f"KMO Test: {kmo_model:.3f} (Should be > 0.6)")
    print(f"Bartlett Sphericity p-value: {p_value:.4f} (Should be < 0.05)")
    
    if kmo_model < 0.5:
        print("Warning: Data might not be suitable for Factor Analysis (KMO < 0.5)")

    # 2. Determine number of factors if not specified (Kaiser Criterion)
    fa_check = FactorAnalyzer(rotation=None)
    fa_check.fit(data)
    ev, v = fa_check.get_eigenvalues()
    
    if n_factors is None:
        n_factors = sum(ev > 1)
        print(f"Optimal number of factors determined by Kaiser Criterion (Eigenvalue > 1): {n_factors}")
    
    # 3. Fit Model
    fa = FactorAnalyzer(n_factors=n_factors, rotation=rotation)
    fa.fit(data)
    
    # 4. Results
    loadings = pd.DataFrame(fa.loadings_, index=cols, columns=[f'Factor_{i+1}' for i in range(n_factors)])
    
    # Variance Info
    variance_info = pd.DataFrame(fa.get_factor_variance(), 
                               index=['SS Loadings', 'Proportion Var', 'Cumulative Var'],
                               columns=[f'Factor_{i+1}' for i in range(n_factors)])
                               
    return loadings, variance_info

if __name__ == "__main__":
    print("Import this module to use Factor Analysis.")
