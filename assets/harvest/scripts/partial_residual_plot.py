"""
Partial Residual Plot for Polynomial Regression

Create partial residual plots that work with polynomial and nonlinear regression models.
Extends statsmodels' built-in partial residual plots to handle polynomial terms.

Source: Practical Statistics for Data Scientists, Chapter 4
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


def partial_residual_plot(model, df, outcome, feature, ax=None):
    """
    Create a partial residual plot for a specific feature in a regression model.
    
    This implementation works with polynomial regression models, unlike statsmodels'
    built-in plot_ccpr which only handles linear terms.
    
    Parameters
    ----------
    model : statsmodels regression result
        Fitted regression model (e.g., from smf.ols().fit())
    df : pandas.DataFrame
        Original data used to fit the model
    outcome : str
        Name of the outcome/dependent variable
    feature : str
        Name of the feature to plot
    ax : matplotlib.axes.Axes, optional
        Axes to plot on. If None, creates new figure.
    
    Returns
    -------
    ax : matplotlib.axes.Axes
        The plot axes
        
    Examples
    --------
    >>> import statsmodels.formula.api as smf
    >>> import pandas as pd
    >>> 
    >>> # Fit polynomial regression
    >>> model = smf.ols('y ~ x + np.power(x, 2)', data=df).fit()
    >>> 
    >>> # Create partial residual plot
    >>> fig, ax = plt.subplots(figsize=(6, 6))
    >>> partial_residual_plot(model, df, 'y', 'x', ax)
    >>> plt.show()
    
    Notes
    -----
    - Black line shows the fitted relationship for the feature
    - Gray line shows LOWESS smoothing of the partial residuals
    - Scatter points show partial residuals + feature contribution
    - Useful for diagnosing nonlinearity in individual predictors
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))
    
    # Get predictions from full model
    y_pred = model.predict(df)
    
    # Determine columns required for model
    required = set(model.params.index).intersection(df.columns)
    required.add(feature)
    copy_df = df[list(required)].copy().astype('float')
    
    # Zero out all features except the one we're plotting
    for c in copy_df.columns:
        if c == feature:
            continue
        copy_df.loc[:, c] = 0.0
    
    # Get prediction with only this feature
    feature_prediction = model.predict(copy_df)
    
    # Calculate partial residuals
    results = pd.DataFrame({
        'feature': df[feature],
        'residual': df[outcome] - y_pred,
        'ypartial': feature_prediction - model.params[0],  # Remove intercept
    })
    results = results.sort_values(by=['feature'])
    
    # Add LOWESS smoothing
    smoothed = sm.nonparametric.lowess(results.ypartial, results.feature, frac=1/3)
    
    # Plot
    ax.scatter(results.feature, results.ypartial + results.residual, alpha=0.5)
    ax.plot(smoothed[:, 0], smoothed[:, 1], color='gray', linewidth=2, label='LOWESS')
    ax.plot(results.feature, results.ypartial, color='black', linewidth=2, label='Fitted')
    ax.set_xlabel(feature)
    ax.set_ylabel(f'Residual + {feature} contribution')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return ax


if __name__ == "__main__":
    # Example usage with polynomial regression
    import statsmodels.formula.api as smf
    import numpy as np
    
    # Generate sample data with nonlinear relationship
    np.random.seed(42)
    n = 200
    x = np.random.uniform(0, 10, n)
    y = 2 * x + 0.5 * x**2 - 0.02 * x**3 + np.random.normal(0, 5, n)
    
    df = pd.DataFrame({'x': x, 'y': y})
    
    # Fit polynomial regression
    model = smf.ols('y ~ x + np.power(x, 2) + np.power(x, 3)', data=df).fit()
    
    print(model.summary())
    
    # Create partial residual plot
    fig, ax = plt.subplots(figsize=(8, 6))
    partial_residual_plot(model, df, 'y', 'x', ax)
    plt.title('Partial Residual Plot: Polynomial Regression')
    plt.tight_layout()
    plt.show()
