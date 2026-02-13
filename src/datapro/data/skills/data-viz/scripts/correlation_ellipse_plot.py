"""
Correlation Ellipse Plot

Visualize correlation matrices using ellipses - a grayscale-friendly alternative to heatmaps.
The ellipse orientation and eccentricity represent correlation direction and strength.

Source: Practical Statistics for Data Scientists, Chapter 1
Original: https://stackoverflow.com/a/34558488
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import EllipseCollection
from matplotlib.colors import Normalize


def plot_corr_ellipses(data, figsize=None, **kwargs):
    """
    Plot a correlation matrix using ellipses.
    
    Parameters
    ----------
    data : pandas.DataFrame or numpy.ndarray
        Correlation matrix to visualize. If DataFrame, row/column names are used as labels.
    figsize : tuple, optional
        Figure size (width, height) in inches
    **kwargs : dict
        Additional arguments passed to EllipseCollection (e.g., cmap='bwr_r')
    
    Returns
    -------
    ec : EllipseCollection
        The ellipse collection (useful for adding colorbars)
    ax : matplotlib.axes.Axes
        The plot axes
        
    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame(np.random.randn(100, 5), columns=list('ABCDE'))
    >>> corr = df.corr()
    >>> m, ax = plot_corr_ellipses(corr, figsize=(6, 6), cmap='bwr_r')
    >>> plt.colorbar(m, ax=ax, label='Correlation coefficient')
    >>> plt.show()
    
    Notes
    -----
    - Ellipse width represents correlation strength (wider = stronger)
    - Ellipse angle represents correlation direction (positive/negative)
    - Works well for grayscale publications
    """
    M = np.array(data)
    if not M.ndim == 2:
        raise ValueError('data must be a 2D array')
    
    fig, ax = plt.subplots(1, 1, figsize=figsize, subplot_kw={'aspect': 'equal'})
    ax.set_xlim(-0.5, M.shape[1] - 0.5)
    ax.set_ylim(-0.5, M.shape[0] - 0.5)
    ax.invert_yaxis()

    # xy locations of each ellipse center
    xy = np.indices(M.shape)[::-1].reshape(2, -1).T

    # Set the relative sizes of the major/minor axes according to the strength of
    # the positive/negative correlation
    w = np.ones_like(M).ravel() + 0.01
    h = 1 - np.abs(M).ravel() - 0.01
    a = 45 * np.sign(M).ravel()

    ec = EllipseCollection(
        widths=w, heights=h, angles=a, units='x', offsets=xy,
        norm=Normalize(vmin=-1, vmax=1),
        transOffset=ax.transData, array=M.ravel(), **kwargs
    )
    ax.add_collection(ec)

    # If data is a DataFrame, use the row/column names as tick labels
    if isinstance(data, pd.DataFrame):
        ax.set_xticks(np.arange(M.shape[1]))
        ax.set_xticklabels(data.columns, rotation=90)
        ax.set_yticks(np.arange(M.shape[0]))
        ax.set_yticklabels(data.index)

    return ec, ax


if __name__ == "__main__":
    # Example usage
    import numpy as np
    import pandas as pd
    
    # Create sample correlation matrix
    np.random.seed(42)
    df = pd.DataFrame(
        np.random.randn(100, 5),
        columns=['Variable A', 'Variable B', 'Variable C', 'Variable D', 'Variable E']
    )
    corr_matrix = df.corr()
    
    # Plot
    m, ax = plot_corr_ellipses(corr_matrix, figsize=(7, 6), cmap='bwr_r')
    cb = plt.colorbar(m, ax=ax)
    cb.set_label('Correlation coefficient')
    plt.title('Correlation Matrix Visualization')
    plt.tight_layout()
    plt.show()
