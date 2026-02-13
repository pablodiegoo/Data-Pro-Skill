import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

def calculate_prob_level(p: float, cov: np.ndarray) -> float:
    """
    Calculate the contour level for a given probability volume in a 
    multivariate normal distribution.
    
    Args:
        p: Target probability (e.g., 0.95 for 95% confidence ellipse)
        cov: Covariance matrix of the distribution
        
    Returns:
        The probability density value at that level.
    """
    # For a multivariate normal, (x-mu)' inv(sigma) (x-mu) follows Chi-squared distribution.
    # The density at the contour is related to the chi-squared quantile.
    # However, for simplicity and matching the textbook's approach:
    # We use the fact that rv.pdf([x, y]) returns the density.
    # We need to find the density value `z` such that the volume inside it is `p`.
    
    # Textbook implementation (simplified):
    # This acts as a mapping from probability to density level.
    return multivariate_normal([0, 0], cov).pdf([np.sqrt(-2 * np.log(1 - p)), 0])

def plot_multivariate_normal_contours(mean, cov, probabilities=[0.5, 0.75, 0.95, 0.99], 
                                     figsize=(6, 6), ax=None, **kwargs):
    """
    Plot contour lines for specific probability volumes of a multivariate normal.
    
    Args:
        mean: Mean vector [mu_x, mu_y]
        cov: Covariance matrix [[var_x, cov_xy], [cov_xy, var_y]]
        probabilities: List of probability volumes to plot (e.g., [0.5, 0.95])
        figsize: Figure size
        ax: Existing Matplotlib axis
        **kwargs: Passed to ax.contour
        
    Returns:
        ax: The plot axis
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
        
    rv = multivariate_normal(mean, cov)
    
    # Create grid for density calculation
    # Range is roughly 3 standard deviations
    std_x = np.sqrt(cov[0, 0])
    std_y = np.sqrt(cov[1, 1])
    x_range = np.linspace(mean[0] - 4*std_x, mean[0] + 4*std_x, 100)
    y_range = np.linspace(mean[1] - 4*std_y, mean[1] + 4*std_y, 100)
    X, Y = np.meshgrid(x_range, y_range)
    
    pos = np.dstack((X, Y))
    Z = rv.pdf(pos)
    
    # Find levels for specific probabilities
    levels = [calculate_prob_level(p, cov) for p in probabilities]
    
    # Plot contours
    cs = ax.contour(X, Y, Z, levels=sorted(levels), **kwargs)
    
    # Add labels
    fmt = {l: f'{p*100:.0f}%' for l, p in zip(levels, probabilities)}
    ax.clabel(cs, inline=True, fmt=fmt, fontsize=10)
    
    # Mark the mean
    ax.plot(mean[0], mean[1], 'ko', markersize=5)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True, alpha=0.3)
    
    return ax

if __name__ == "__main__":
    # Example usage
    mean = [0.5, -0.5]
    cov = [[1, 0.8], [0.8, 2]]
    
    fig, ax = plt.subplots(figsize=(7, 7))
    plot_multivariate_normal_contours(mean, cov, ax=ax, colors='C0')
    plt.title('Multivariate Normal Probability Contours')
    plt.show()
