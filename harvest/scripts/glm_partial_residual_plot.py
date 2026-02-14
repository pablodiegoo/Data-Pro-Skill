"""
GLM Partial Residual Plot for Logistic Regression

Generates partial residual plots for Generalized Linear Models (GLM),
specifically designed for logistic regression with splines or polynomial terms.

This is an extension of the standard partial residual plot that works with
non-linear transformations in GLM models.

Source: Practical Statistics for Data Scientists, Chapter 5
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.genmod.generalized_linear_model import GLMResults


def glm_partial_residual_plot(model, df, outcome, feature, fig, ax):
    """
    Create a partial residual plot for a GLM model.
    
    Parameters
    ----------
    model : GLMResults
        Fitted GLM model from statsmodels
    df : pd.DataFrame
        Original data used to fit the model
    outcome : str
        Name of the outcome variable (must be binary: 0/1 or categorical)
    feature : str
        Name of the feature to plot partial residuals for
    fig : matplotlib.figure.Figure
        Figure object for DPI calculation
    ax : matplotlib.axes.Axes
        Axes object to plot on
        
    Returns
    -------
    ax : matplotlib.axes.Axes
        Modified axes with the partial residual plot
        
    Notes
    -----
    This function is designed for binary classification models.
    The outcome should be encoded as 0/1 or will be converted internally.
    
    The plot shows:
    - Scatter points: Actual residuals + feature contribution
    - Black line: Model's predicted contribution from the feature
    
    Examples
    --------
    >>> import statsmodels.formula.api as smf
    >>> formula = 'outcome ~ bs(payment_inc_ratio, df=8) + purpose_'
    >>> model = smf.glm(formula=formula, data=loan_data, 
    ...                 family=sm.families.Binomial())
    >>> results = model.fit()
    >>> fig, ax = plt.subplots(figsize=(5, 5))
    >>> glm_partial_residual_plot(results, loan_data, 'outcome', 
    ...                           'payment_inc_ratio', fig, ax)
    """
    # Convert outcome to binary if needed
    if df[outcome].dtype == 'object' or df[outcome].dtype.name == 'category':
        # Assume first category is 0, second is 1
        y_actual = [0 if s == df[outcome].iloc[0] else 1 for s in df[outcome]]
    else:
        y_actual = df[outcome].values
    
    # Get predictions from full model
    y_pred = model.predict(df)
    
    # Store original parameters
    org_params = model.params.copy()
    zero_params = model.params.copy()
    
    # Set parameters of all features except target feature to 0
    for i, name in enumerate(zero_params.index):
        if feature in name:
            continue
        zero_params.iloc[i] = 0.0
    
    # Reinitialize model with zeroed parameters
    model.initialize(model.model, zero_params)
    feature_prediction = model.predict(df)
    
    # Calculate partial contribution on logit scale
    ypartial = -np.log(1 / feature_prediction - 1)
    ypartial = ypartial - np.mean(ypartial)
    
    # Restore original parameters
    model.initialize(model.model, org_params)
    
    # Prepare results dataframe
    results = pd.DataFrame({
        'feature': df[feature],
        'residual': -2 * (y_actual - y_pred),
        'ypartial': ypartial / 2,
    })
    results = results.sort_values(by=['feature'])
    
    # Plot
    ax.scatter(results.feature, results.residual, marker=".", 
               s=72. / fig.dpi)
    ax.plot(results.feature, results.ypartial, color='black')
    ax.set_xlabel(feature)
    ax.set_ylabel(f'Residual + {feature} contribution')
    
    return ax


def glm_partial_residual_grid(model, df, outcome, features, figsize=(12, 8)):
    """
    Create a grid of partial residual plots for multiple features.
    
    Parameters
    ----------
    model : GLMResults
        Fitted GLM model from statsmodels
    df : pd.DataFrame
        Original data used to fit the model
    outcome : str
        Name of the outcome variable
    features : list of str
        List of feature names to create plots for
    figsize : tuple, optional
        Figure size (width, height)
        
    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure containing the grid of plots
    axes : array of matplotlib.axes.Axes
        Array of axes objects
        
    Examples
    --------
    >>> features = ['payment_inc_ratio', 'borrower_score']
    >>> fig, axes = glm_partial_residual_grid(results, loan_data, 
    ...                                       'outcome', features)
    """
    import matplotlib.pyplot as plt
    
    n_features = len(features)
    n_cols = min(3, n_features)
    n_rows = (n_features + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axes.flatten() if n_features > 1 else [axes]
    
    for idx, feature in enumerate(features):
        glm_partial_residual_plot(model, df, outcome, feature, 
                                  fig, axes[idx])
    
    # Hide unused subplots
    for idx in range(n_features, len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    return fig, axes
