"""
Permutation-Based Feature Importance Calculator

Calculates feature importance by measuring the decrease in model accuracy
when each feature is randomly permuted. This is a model-agnostic approach
that works with any classifier.

Unlike tree-based feature importance (Gini/Entropy), permutation importance:
- Works with any model type
- Measures actual predictive power
- Accounts for feature interactions
- Is less biased toward high-cardinality features

Source: Practical Statistics for Data Scientists, Chapter 6
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
from collections import defaultdict


def calculate_permutation_importance(model, X, y, n_repeats=3, test_size=0.3, 
                                     random_state=None, metric='accuracy'):
    """
    Calculate feature importance using permutation method.
    
    Parameters
    ----------
    model : sklearn estimator
        Fitted or unfitted sklearn model (will be refitted if needed)
    X : pd.DataFrame
        Feature matrix
    y : pd.Series or array-like
        Target variable
    n_repeats : int, default=3
        Number of times to repeat the permutation test with different
        train/test splits
    test_size : float, default=0.3
        Proportion of data to use for validation
    random_state : int, optional
        Random state for reproducibility
    metric : str or callable, default='accuracy'
        Metric to use for scoring. Can be 'accuracy', 'roc_auc', or
        a custom scoring function
        
    Returns
    -------
    importance_df : pd.DataFrame
        DataFrame with columns:
        - feature: Feature name
        - importance_mean: Mean importance across repeats
        - importance_std: Standard deviation of importance
        - importance_scores: List of individual scores
        
    Notes
    -----
    The importance score is calculated as:
        (baseline_accuracy - permuted_accuracy) / baseline_accuracy
    
    Higher values indicate more important features.
    
    Examples
    --------
    >>> from sklearn.ensemble import RandomForestClassifier
    >>> rf = RandomForestClassifier(n_estimators=500)
    >>> importance_df = calculate_permutation_importance(rf, X, y, n_repeats=5)
    >>> print(importance_df.sort_values('importance_mean', ascending=False))
    """
    scores = defaultdict(list)
    
    # Select metric function
    if metric == 'accuracy':
        metric_func = metrics.accuracy_score
    elif metric == 'roc_auc':
        metric_func = metrics.roc_auc_score
    elif callable(metric):
        metric_func = metric
    else:
        raise ValueError(f"Unknown metric: {metric}")
    
    # Repeat with different train/test splits
    for repeat in range(n_repeats):
        # Split data
        train_X, valid_X, train_y, valid_y = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Fit model
        model.fit(train_X, train_y)
        
        # Baseline accuracy
        baseline_score = metric_func(valid_y, model.predict(valid_X))
        
        # Test each feature
        for column in X.columns:
            # Create copy with permuted feature
            X_permuted = valid_X.copy()
            X_permuted[column] = np.random.permutation(X_permuted[column].values)
            
            # Calculate score with permuted feature
            permuted_score = metric_func(valid_y, model.predict(X_permuted))
            
            # Importance = relative decrease in accuracy
            importance = (baseline_score - permuted_score) / baseline_score
            scores[column].append(importance)
    
    # Create results dataframe
    importance_df = pd.DataFrame([
        {
            'feature': feature,
            'importance_mean': np.mean(score_list),
            'importance_std': np.std(score_list),
            'importance_scores': score_list
        }
        for feature, score_list in scores.items()
    ])
    
    # Sort by mean importance
    importance_df = importance_df.sort_values('importance_mean', ascending=False)
    importance_df = importance_df.reset_index(drop=True)
    
    return importance_df


def plot_permutation_importance(importance_df, top_n=None, figsize=(8, 6)):
    """
    Plot feature importance with error bars.
    
    Parameters
    ----------
    importance_df : pd.DataFrame
        Output from calculate_permutation_importance
    top_n : int, optional
        Number of top features to plot. If None, plots all features
    figsize : tuple, default=(8, 6)
        Figure size
        
    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object
    ax : matplotlib.axes.Axes
        Axes object
        
    Examples
    --------
    >>> importance_df = calculate_permutation_importance(rf, X, y)
    >>> fig, ax = plot_permutation_importance(importance_df, top_n=15)
    >>> plt.show()
    """
    import matplotlib.pyplot as plt
    
    # Select top N features
    if top_n is not None:
        plot_df = importance_df.head(top_n).copy()
    else:
        plot_df = importance_df.copy()
    
    # Sort for plotting (ascending for horizontal bar)
    plot_df = plot_df.sort_values('importance_mean', ascending=True)
    
    # Create plot
    fig, ax = plt.subplots(figsize=figsize)
    
    y_pos = np.arange(len(plot_df))
    ax.barh(y_pos, plot_df['importance_mean'], 
            xerr=plot_df['importance_std'],
            align='center', alpha=0.7, capsize=5)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(plot_df['feature'])
    ax.set_xlabel('Permutation Importance (Accuracy Decrease)')
    ax.set_title('Feature Importance via Permutation')
    ax.axvline(x=0, color='gray', linestyle='--', linewidth=0.8)
    
    plt.tight_layout()
    return fig, ax


def compare_importance_methods(model, X, y, n_repeats=3):
    """
    Compare permutation importance with tree-based importance (if available).
    
    Parameters
    ----------
    model : sklearn estimator
        Tree-based model (RandomForest, XGBoost, etc.)
    X : pd.DataFrame
        Feature matrix
    y : pd.Series
        Target variable
    n_repeats : int, default=3
        Number of repeats for permutation importance
        
    Returns
    -------
    comparison_df : pd.DataFrame
        DataFrame comparing different importance methods
        
    Examples
    --------
    >>> from sklearn.ensemble import RandomForestClassifier
    >>> rf = RandomForestClassifier(n_estimators=500, random_state=42)
    >>> rf.fit(X, y)
    >>> comparison = compare_importance_methods(rf, X, y)
    """
    # Calculate permutation importance
    perm_importance = calculate_permutation_importance(
        model, X, y, n_repeats=n_repeats
    )
    
    # Get tree-based importance if available
    comparison_df = perm_importance[['feature', 'importance_mean']].copy()
    comparison_df.columns = ['feature', 'permutation_importance']
    
    if hasattr(model, 'feature_importances_'):
        tree_importance = pd.DataFrame({
            'feature': X.columns,
            'tree_importance': model.feature_importances_
        })
        comparison_df = comparison_df.merge(tree_importance, on='feature')
    
    comparison_df = comparison_df.sort_values('permutation_importance', 
                                              ascending=False)
    
    return comparison_df
