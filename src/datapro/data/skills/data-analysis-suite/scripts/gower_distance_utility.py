import pandas as pd
import numpy as np

def calculate_gower_distance(df: pd.DataFrame) -> np.ndarray:
    """
    Calculate Gower's distance matrix for a dataframe with mixed data types.
    Gower's distance is defined as the average of partial dissimilarities:
    - Numeric: |x1 - x2| / range(variable)
    - Categorical: 0 if x1 == x2, else 1
    """
    n = len(df)
    distance_matrix = np.zeros((n, n))
    
    # Identify column types
    cols = df.columns
    is_numeric = [pd.api.types.is_numeric_dtype(df[col]) for col in cols]
    ranges = [df[col].max() - df[col].min() if is_numeric[i] else 1 for i, col in enumerate(cols)]
    
    for i in range(n):
        for j in range(i + 1, n):
            partial_distances = []
            for k, col in enumerate(cols):
                val_i = df.iloc[i][col]
                val_j = df.iloc[j][col]
                
                if is_numeric[k]:
                    # Numeric distance scaled by range
                    if ranges[k] == 0:
                        d = 0
                    else:
                        d = abs(val_i - val_j) / ranges[k]
                else:
                    # Categorical distance (binary)
                    d = 0 if val_i == val_j else 1
                    
                partial_distances.append(d)
            
            # Average of partial distances
            dist = np.mean(partial_distances)
            distance_matrix[i, j] = dist
            distance_matrix[j, i] = dist
            
    return distance_matrix

def perform_mixed_clustering(df, n_clusters=4):
    """
    Perform hierarchical clustering on mixed-type data using Gower's distance.
    """
    from scipy.cluster.hierarchy import linkage, fcluster
    from scipy.spatial.distance import squareform
    
    # Calculate Gower distance
    dist_matrix = calculate_gower_distance(df)
    
    # Convert to condensed form for linkage
    condensed_dist = squareform(dist_matrix)
    
    # Hierarchical clustering (complete linkage is often preferred for Gower)
    Z = linkage(condensed_dist, method='complete')
    
    # Extract clusters
    clusters = fcluster(Z, n_clusters, criterion='maxclust')
    
    return clusters

if __name__ == "__main__":
    # Example usage
    data = {
        'age': [25, 32, 45, 22, 50],                   # Numeric
        'income': [50000, 80000, 120000, 40000, 150000], # Numeric
        'owns_home': [True, False, True, False, True],  # Boolean
        'city': ['A', 'B', 'A', 'B', 'C']               # Categorical
    }
    df = pd.DataFrame(data)
    
    dist = calculate_gower_distance(df)
    print("\nGower Distance Matrix:")
    print(np.round(dist, 2))
    
    clusters = perform_mixed_clustering(df, n_clusters=2)
    print("\nClusters:", clusters)
