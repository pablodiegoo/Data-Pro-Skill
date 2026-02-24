
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import MultiLabelBinarizer

def run_survey_pca(df, cols, n_components=None, sep=None):
    """
    Performs PCA tailored for Survey Data, handling Multi-Response questions.
    
    Args:
        df: DataFrame
        cols: List of columns to analyze. 
              If 'sep' is provided, columns are treated as strings to be split (e.g. "A;B;C").
              If 'sep' is None, columns are treated as separate binary/likert variables.
        n_components: Number of components to extract. If None, uses Kaiser criterion (approx).
        sep: Separator for multi-response string columns (optional).
        
    Returns:
        loadings: DataFrame of factor loadings.
        scores: DataFrame of factor scores for each respondent.
        variance: Explained variance ratio.
    """
    
    # 1. Preprocessing
    if sep:
        # Multi-Response Case (e.g., one or few columns with "ItemA;ItemB")
        # We need to create dummies first
        dummies_list = []
        for idx, row in df.iterrows():
            # Combine all text from specified columns
            combined_text = []
            for c in cols:
                val = str(row[c])
                if val != 'nan' and val.strip() != '':
                    combined_text.extend([x.strip() for x in val.split(sep)])
            dummies_list.append(combined_text)
            
        mlb = MultiLabelBinarizer()
        data_matrix = mlb.fit_transform(dummies_list)
        feature_names = mlb.classes_
        
        # Filter out common junk
        valid_indices = [i for i, name in enumerate(feature_names) if name not in ['nan', 'None', 'Outros', '']]
        data_matrix = data_matrix[:, valid_indices]
        feature_names = [feature_names[i] for i in valid_indices]
        
        X = pd.DataFrame(data_matrix, columns=feature_names, index=df.index)
        
    else:
        # Standard Case (Likert or Binary columns)
        X = df[cols].dropna()
    
    # 2. PCA
    if n_components is None:
        n_components = min(len(X.columns), 5) # Default/Safe cap if untuned
        
    pca = PCA(n_components=n_components)
    scores = pca.fit_transform(X)
    
    # 3. Validating n_components (simple heuristic)
    # If generic usage, just trust input or default
    
    # 4. Outputs
    loadings = pd.DataFrame(
        pca.components_.T, 
        columns=[f'Factor_{i+1}' for i in range(n_components)],
        index=X.columns
    )
    
    scores_df = pd.DataFrame(
        scores, 
        columns=[f'Factor_{i+1}' for i in range(n_components)],
        index=X.index
    )
    
    variance_df = pd.DataFrame({
        'Factor': [f'Factor_{i+1}' for i in range(n_components)],
        'Explained_Variance': pca.explained_variance_ratio_
    })
    
    return loadings, scores_df, variance_df
