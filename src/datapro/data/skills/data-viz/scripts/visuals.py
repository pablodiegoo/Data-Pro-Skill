import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

def set_style(style='ggplot', palette='husl'):
    plt.style.use(style)
    sns.set_palette(palette)

def plot_weighted_bars(df, cols, title, output_path=None, weight_col='weight'):
    """
    Generates a weighted bar chart for survey items.
    
    Args:
        df: DataFrame containing data and weights.
        cols: List of columns to plot (binary/boolean or specific values).
        title: Chart title.
        output_path: Path to save image (optional).
        weight_col: Name of the weight column.
    """
    
    if weight_col not in df.columns:
        print(f"Warning: Weight column '{weight_col}' not found. Using unweighted counts.")
        df['temp_weight'] = 1
        wc = 'temp_weight'
    else:
        wc = weight_col
        
    results = {}
    total_weight = df[wc].sum()
    
    for col in cols:
        # Calculate sum of weights where col is True/Present
        # Handling different types: 
        # - Boolean/Binary (1/0): sum weights * val
        # - String (Selected): sum weights where not null
        
        if pd.api.types.is_numeric_dtype(df[col]):
             mask = df[col] > 0
        else:
             mask = df[col].notna() & (df[col] != '')
             
        w_sum = df.loc[mask, wc].sum()
        results[col] = (w_sum / total_weight) * 100
        
    res_df = pd.DataFrame(list(results.items()), columns=['Item', 'Percent'])
    res_df = res_df.sort_values('Percent', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=res_df, y='Item', x='Percent')
    plt.title(title)
    plt.xlabel('Weighted %')
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=150)
        plt.close()
        print(f"Saved plot to {output_path}")
    else:
        plt.show()
        
    return res_df
