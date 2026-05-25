
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def run_segmentation(df, feature_cols, n_clusters=3):
    """
    Performs K-Means clustering on the specified features.
    
    Args:
        df: Pandas DataFrame containing the data.
        feature_cols: List of column names to use for clustering.
        n_clusters: Number of clusters to create.
        
    Returns:
        df_labeled: DataFrame with a new 'cluster' column.
        centroids: DataFrame of cluster centers.
    """
    # 1. Select data and drop NAs
    data = df[feature_cols].dropna()
    
    if data.empty:
        raise ValueError("No data remaining after dropping NaNs in feature columns.")
        
    # 2. Scale data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    
    # 3. PCA (Optional, for visualization/noise reduction, but we'll strict to K-Means for now)
    # pca = PCA(n_components=2)
    # pca_data = pca.fit_transform(scaled_data)
    
    # 4. Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(scaled_data)
    
    # 5. Merge results back
    # usage of .loc to avoid SettingWithCopyWarning if df is a slice
    df_out = df.copy()
    df_out.loc[data.index, 'cluster'] = clusters
    
    # Profile clusters
    # centroids = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=feature_cols)
    return df_out

if __name__ == "__main__":
    # Example Usage
    print("This is a module. Import it to use clustering functions.")
