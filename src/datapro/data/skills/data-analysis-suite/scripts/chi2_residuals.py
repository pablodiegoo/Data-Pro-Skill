"""
Chi-Square Residuals Analysis
==============================
Calculates Chi-Square test of independence and Standardized Residuals
for any pair of categorical variables. Generates a heatmap of residuals.

Std Residual Rule of Thumb:
- Residual > 1.96: Observed is SIGNIFICANTLY HIGHER than expected (p < .05)
- Residual < -1.96: Observed is SIGNIFICANTLY LOWER than expected

Origin: Harvested from Saquarema Turística project (02_analysis_chi2.py).
Promoted via /process-contribution workflow.
"""

import pandas as pd
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency


def chi2_residuals(df, col_rows, col_cols, output_dir, label_map=None):
    """
    Calculates Chi-Square and Standardized Residuals for two categorical columns.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe with the two categorical columns.
    col_rows : str
        Column name for the rows of the contingency table.
    col_cols : str
        Column name for the columns of the contingency table.
    output_dir : str
        Directory to save the heatmap PNG and residuals CSV.
    label_map : dict, optional
        Mapping of column names to human-readable labels for chart titles.
        If None, raw column names are used.

    Returns
    -------
    dict or None
        If significant (p < 0.05), returns a dict with:
        - 'chi2': float, the chi-square statistic
        - 'p_value': float
        - 'dof': int, degrees of freedom
        - 'residuals': pd.DataFrame, standardized residuals
        - 'plot_path': str, path to saved heatmap
        - 'csv_path': str, path to saved residuals CSV
        If not significant, returns None.
    """
    print(f"Chi-Squared: {col_rows} x {col_cols}")

    os.makedirs(output_dir, exist_ok=True)

    # Create Contingency Table
    contingency = pd.crosstab(df[col_rows], df[col_cols])

    # Chi-Square Test
    chi2, p, dof, expected = chi2_contingency(contingency)

    print(f"  χ² = {chi2:.2f}, p-value = {p:.4f}, dof = {dof}")

    if p >= 0.05:
        print("  >> No significant association (p >= 0.05)")
        return None

    print("  >> Significant Association Found!")

    # Standardized Residuals: (Observed - Expected) / sqrt(Expected)
    residuals = (contingency - expected) / np.sqrt(expected)

    # Plot Heatmap
    plt.figure(figsize=(10, 8))
    limit = max(abs(residuals.min().min()), abs(residuals.max().max()), 2.5)

    sns.heatmap(
        residuals, annot=True, fmt='.1f',
        cmap='RdBu_r', center=0, vmin=-limit, vmax=limit
    )

    row_label = (label_map or {}).get(col_rows, col_rows)
    col_label = (label_map or {}).get(col_cols, col_cols)

    plt.title(
        f'Residual Analysis: {row_label} x {col_label}\n'
        f'(>1.96 = Significant Positive Association)',
        fontsize=10
    )
    plt.tight_layout()

    safe_name = f"{col_rows}_x_{col_cols}".replace(' ', '_').replace('/', '_')
    plot_path = os.path.join(output_dir, f'chi2_{safe_name}.png')
    csv_path = os.path.join(output_dir, f'residuals_{safe_name}.csv')

    plt.savefig(plot_path, dpi=150)
    plt.close()

    residuals.to_csv(csv_path)

    print(f"  Saved: {plot_path}")
    print(f"  Saved: {csv_path}")

    return {
        'chi2': chi2,
        'p_value': p,
        'dof': dof,
        'residuals': residuals,
        'plot_path': plot_path,
        'csv_path': csv_path,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Chi-Square Residuals Analysis")
    parser.add_argument("input", help="Path to parquet or CSV file")
    parser.add_argument("--rows", required=True, help="Column for rows")
    parser.add_argument("--cols", required=True, help="Column for columns")
    parser.add_argument("--output", default="output/chi2", help="Output directory")
    args = parser.parse_args()

    ext = os.path.splitext(args.input)[1].lower()
    if ext == '.parquet':
        data = pd.read_parquet(args.input)
    else:
        data = pd.read_csv(args.input)

    chi2_residuals(data, args.rows, args.cols, args.output)
