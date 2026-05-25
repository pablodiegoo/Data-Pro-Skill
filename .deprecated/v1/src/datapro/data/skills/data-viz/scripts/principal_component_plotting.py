import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def plot_pca_scree(pca, ax=None, figsize=(8, 5)):
    """
    Plot a scree plot showing the percentage of variance explained by each component.
    
    Args:
        pca: Fitted sklearn.decomposition.PCA object
        ax: Existing axis
        figsize: Figure size
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
        
    var_exp = pca.explained_variance_ratio_
    cum_var_exp = np.cumsum(var_exp)
    
    n_components = len(var_exp)
    x = range(1, n_components + 1)
    
    ax.bar(x, var_exp, alpha=0.5, align='center', label='Individual variance')
    ax.step(x, cum_var_exp, where='mid', label='Cumulative variance', color='red')
    
    ax.set_ylabel('Explained variance ratio')
    ax.set_xlabel('Principal component index')
    ax.set_xticks(x)
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    return ax

def plot_pca_loadings(pca, columns, n_components=5, figsize=(10, 8)):
    """
    Visualize the contribution of each original feature to the principal components.
    Creates a set of horizontal bar charts, one per component.
    
    Args:
        pca: Fitted sklearn.decomposition.PCA object
        columns: Names of the original features
        n_components: Number of components to show
        figsize: Figure size
    """
    n_show = min(n_components, pca.n_components_)
    fig, axes = plt.subplots(n_show, 1, figsize=figsize, sharex=True)
    
    if n_show == 1:
        axes = [axes]
        
    # Get loadings (components_)
    loadings = pd.DataFrame(pca.components_[:n_show].T, 
                            index=columns,
                            columns=[f'PC{i+1}' for i in range(n_show)])
    
    max_loading = np.abs(pca.components_[:n_show]).max()
    
    for i in range(n_show):
        ax = axes[i]
        pc_name = f'PC{i+1}'
        
        # Color based on sign
        colors = ['red' if x < 0 else 'blue' for x in loadings[pc_name]]
        
        loadings[pc_name].plot.bar(ax=ax, color=colors)
        ax.axhline(0, color='black', lw=1)
        ax.set_ylabel(pc_name)
        ax.set_ylim(-max_loading * 1.1, max_loading * 1.1)
        
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    # Example usage with dummy data
    from sklearn.preprocessing import StandardScaler
    
    # Create random correlated data
    np.random.seed(42)
    data = np.random.randn(100, 5)
    data[:, 1] = data[:, 0] * 0.8 + np.random.randn(100) * 0.2
    
    df = pd.DataFrame(data, columns=['A', 'B', 'C', 'D', 'E'])
    X = StandardScaler().fit_transform(df)
    
    pca = PCA(n_components=5)
    pca.fit(X)
    
    # Scree plot
    plot_pca_scree(pca)
    plt.title('PCA Scree Plot')
    plt.show()
    
    # Loadings plot
    plot_pca_loadings(pca, df.columns, n_components=3)
    plt.suptitle('Principal Component Loadings')
    plt.show()
