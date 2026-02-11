"""
Residual Segmentation Analysis (Deep Dive)
===========================================
Pattern: Fit Y ~ X1...Xn → Calculate Residual → Segment → Cross with qualitative data.

Segments:
- Disappointed (Residual < -threshold): Actual satisfaction LOWER than predicted.
  Unmeasured factors are dragging them down.
- Aligned (|Residual| <= threshold): Satisfaction matches expectations.
- Delighted (Residual > +threshold): Actual satisfaction HIGHER than predicted.
  Unmeasured positive factors at play.

Origin: Harvested from Saquarema Turística project (02_analysis_deep_dive.py).
Promoted via /process-contribution workflow.
"""

import pandas as pd
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression


def residual_segmentation(df, target, predictors, output_dir,
                          threshold=0.7, label_map=None):
    """
    Fit a linear regression, calculate residuals, and segment respondents.

    IMPORTANT: Input DataFrame must contain **pre-encoded numeric** columns.
    Do NOT pass raw string columns — apply SCALE_MAP in your prep script first
    (per the "Encode Once" rule).

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe with numeric target and predictor columns.
    target : str
        Name of the dependent variable column (e.g., 'P33_Eval_General').
    predictors : list[str]
        List of independent variable column names.
    output_dir : str
        Directory to save output tables and plots.
    threshold : float, default 0.7
        Residual threshold for segmentation. |residual| > threshold
        classifies as Disappointed/Delighted.
    label_map : dict, optional
        Mapping of column names to short human-readable labels for charts.

    Returns
    -------
    pd.DataFrame
        Copy of input dataframe with added columns:
        - 'Predicted': model predictions
        - 'Residual': actual - predicted
        - 'Sentiment_Group': 'Disappointed' | 'Aligned' | 'Delighted'
    """
    print(f"Residual Segmentation: {target} ~ {predictors}")

    os.makedirs(output_dir, exist_ok=True)

    # Filter to valid rows
    cols_needed = [target] + predictors
    model_df = df[cols_needed].dropna().copy()
    print(f"  Valid rows: {len(model_df)} / {len(df)}")

    # Fit Model
    X = model_df[predictors]
    y = model_df[target]

    model = LinearRegression()
    model.fit(X, y)

    r2 = model.score(X, y)
    print(f"  R² = {r2:.4f}")

    # Calculate Residuals
    model_df['Predicted'] = model.predict(X)
    model_df['Residual'] = model_df[target] - model_df['Predicted']

    # Segment
    model_df['Sentiment_Group'] = 'Aligned'
    model_df.loc[model_df['Residual'] < -threshold, 'Sentiment_Group'] = 'Disappointed'
    model_df.loc[model_df['Residual'] > threshold, 'Sentiment_Group'] = 'Delighted'

    print(f"\n  Segment Distribution:")
    dist = model_df['Sentiment_Group'].value_counts()
    for group, count in dist.items():
        pct = count / len(model_df) * 100
        print(f"    {group}: {count} ({pct:.1f}%)")

    # --- Outputs ---

    # 1. Coefficients table
    lm = label_map or {}
    coef_df = pd.DataFrame({
        'Predictor': [lm.get(p, p) for p in predictors],
        'Coefficient': model.coef_,
    }).sort_values('Coefficient', ascending=False)
    coef_df.to_csv(os.path.join(output_dir, 'coefficients.csv'), index=False)

    # 2. Residual distribution plot
    plt.figure(figsize=(10, 6))
    sns.histplot(model_df['Residual'], kde=True, color='steelblue', bins=30)
    plt.axvline(-threshold, color='red', linestyle='--', label=f'Disappointed (<{-threshold})')
    plt.axvline(threshold, color='green', linestyle='--', label=f'Delighted (>{threshold})')
    plt.title('Residual Distribution with Segmentation Thresholds')
    plt.xlabel('Residual (Actual - Predicted)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'residual_distribution.png'), dpi=150)
    plt.close()

    # 3. Segment distribution bar chart
    plt.figure(figsize=(8, 5))
    colors = {'Disappointed': '#e74c3c', 'Aligned': '#95a5a6', 'Delighted': '#2ecc71'}
    order = ['Disappointed', 'Aligned', 'Delighted']
    existing_order = [g for g in order if g in dist.index]
    counts = [dist.get(g, 0) for g in existing_order]
    bar_colors = [colors[g] for g in existing_order]
    plt.bar(existing_order, counts, color=bar_colors)
    plt.title('Sentiment Group Distribution')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'segment_distribution.png'), dpi=150)
    plt.close()

    # 4. Save segment data
    model_df.to_csv(os.path.join(output_dir, 'segmented_data.csv'), index=True)

    print(f"\n  Outputs saved to {output_dir}/")

    return model_df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Residual Segmentation Analysis")
    parser.add_argument("input", help="Path to parquet or CSV (numeric-encoded)")
    parser.add_argument("--target", required=True, help="Dependent variable column")
    parser.add_argument("--predictors", required=True, help="Comma-separated predictor columns")
    parser.add_argument("--output", default="output/deep_dive", help="Output directory")
    parser.add_argument("--threshold", type=float, default=0.7, help="Segmentation threshold")
    args = parser.parse_args()

    ext = os.path.splitext(args.input)[1].lower()
    if ext == '.parquet':
        data = pd.read_parquet(args.input)
    else:
        data = pd.read_csv(args.input)

    preds = [p.strip() for p in args.predictors.split(',')]
    residual_segmentation(data, args.target, preds, args.output, args.threshold)
