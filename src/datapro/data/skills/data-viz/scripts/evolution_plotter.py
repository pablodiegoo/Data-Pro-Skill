import matplotlib
matplotlib.use('Agg') # Force non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from wordcloud import WordCloud

# Global styling configuration
STYLE_CONFIG = {
    'palette': 'viridis',
    'font_family': 'sans-serif',
    'title_size': 14,
    'label_size': 10
}

def setup_style():
    sns.set_theme(style="whitegrid")
    plt.rcParams['font.sans-serif'] = ['Inter', 'Roboto', 'Arial', 'sans-serif']

def plot_evolution_line(df, x, y, hue, title, filename, palette=None):
    """
    Renders an evolution line chart comparing metrics between survey cycles.
    """
    setup_style()
    plt.figure(figsize=(10, 6))
    
    palette = palette or STYLE_CONFIG['palette']
    
    ax = sns.lineplot(data=df, x=x, y=y, hue=hue, marker='o', linewidth=2.5, palette=palette)
    
    plt.title(title, fontsize=STYLE_CONFIG['title_size'], pad=20, weight='bold')
    plt.xlabel(x, fontsize=STYLE_CONFIG['label_size'])
    plt.ylabel(y, fontsize=STYLE_CONFIG['label_size'])
    plt.ylim(0, 10.5) # Standard 0-10 scale
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"✅ Evolution chart saved to {filename}")

def plot_proportions(df, x, hue, title, filename):
    """
    Renders stacked bar charts for longitudinal proportion analysis.
    """
    setup_style()
    # Logic for stacked bars showing percentages
    # ... placeholder for implementation ...

def plot_word_cloud(frequency_csv, title, filename):
    """
    Renders a word cloud from a frequency CSV (Word, Frequency).
    """
    plt.figure(figsize=(10, 6))
    
    # Load frequency data
    df = pd.read_csv(frequency_csv)
    # Convert to dict for wordcloud
    freq_dict = dict(zip(df['Word'], df['Frequency']))
    
    wc = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies(freq_dict)
    
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.title(title, fontsize=STYLE_CONFIG['title_size'], pad=20, weight='bold')
    plt.tight_layout()
    
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"✅ Word Cloud saved to {filename}")
