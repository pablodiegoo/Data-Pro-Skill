
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Set global style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

# Sebrae-ish colors (Blue/Cyan tones)
SEBRAE_PALETTE = ["#005CA9", "#00A4E4", "#FBB700", "#666666", "#CCCCCC"]
sns.set_palette(sns.color_palette(SEBRAE_PALETTE))

def save_plot(filename):
    """Saves the current plot to the specified filename."""
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Chart saved to: {filename}")

def plot_bar(df, x_col, y_col=None, title="", filename="bar_chart.png", orientation='v'):
    """
    Creates a bar chart.
    If y_col is None, counts occurrences of x_col.
    If y_col is provided, aggregates (mean/sum) can be pre-calculated or raw.
    """
    plt.figure()
    if y_col is None:
        # Count plot
        if orientation == 'v':
            ax = sns.countplot(data=df, x=x_col, order=df[x_col].value_counts().index)
            plt.xticks(rotation=45, ha='right')
        else:
            ax = sns.countplot(data=df, y=x_col, order=df[x_col].value_counts().index)
    else:
        # Bar plot (numeric vs categorical)
        if orientation == 'v':
            ax = sns.barplot(data=df, x=x_col, y=y_col, ci=None)
            plt.xticks(rotation=45, ha='right')
        else:
            ax = sns.barplot(data=df, y=x_col, x=y_col, ci=None)
            
    plt.title(title, fontsize=14, fontweight='bold', pad=20)
    
    # Add labels
    for container in ax.containers:
        ax.bar_label(container)
        
    save_plot(filename)

def plot_pie(df, col, title="", filename="pie_chart.png", limit=10):
    """
    Creates a pie chart for categorical data.
    """
    plt.figure(figsize=(8, 8))
    counts = df[col].value_counts().head(limit)
    
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=SEBRAE_PALETTE)
    plt.title(title, fontsize=14, fontweight='bold')
    save_plot(filename)

def plot_grouped_bar(df, x_col, hue, title="", filename="grouped_bar.png"):
    """
    Creates a grouped bar chart (Cross-tabulation visualization).
    """
    plt.figure()
    
    # Calculate percentages for better comparison
    prop_df = (df[x_col]
           .groupby(df[hue])
           .value_counts(normalize=True)
           .rename('percentage')
           .reset_index())

    ax = sns.barplot(x=x_col, y='percentage', hue=hue, data=prop_df)
    
    plt.title(title, fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    
    # Format Y axis as percentage
    from matplotlib.ticker import PercentFormatter
    ax.yaxis.set_major_formatter(PercentFormatter(1.0))
    
    save_plot(filename)

if __name__ == "__main__":
    print("This module provides plotting functions. Import it to use.")
