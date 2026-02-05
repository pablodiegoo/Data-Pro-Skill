#!/usr/bin/env python3
"""
Brazil Map Generator Skill
Generic tool for generating state-level choropleth maps of Brazil.
"""

import matplotlib
matplotlib.use('Agg') # Headless backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import geobr
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Default Color Palette (Sebrae/OS12 style)
DEFAULT_DISCRETE_PALETTE = {
    'Ótimo': '#2a6b6b',      # Dark teal
    'Bom': '#5cb85c',        # Green
    'Médio': '#f0ad4e',      # Yellow/Orange
    'Ruim': '#e87a5f',       # Light coral
    'Péssimo': '#e85a71',    # Pink/Red
    'Sem dados': '#cccccc'   # Gray
}

class BrazilMapGenerator:
    def __init__(self, year=2020):
        self.year = year
        self._shapefile = None
    
    @property
    def shapefile(self):
        """Lazy load shapefile"""
        if self._shapefile is None:
            print("Loading Brazil state shapefile via geobr...")
            self._shapefile = geobr.read_state(year=self.year)
        return self._shapefile

    def plot_discrete_map(self, 
                          data, 
                          geo_col, 
                          category_col, 
                          color_map, 
                          title, 
                          output_path,
                          legend_order=None):
        """
        Plot a map using discrete categories (e.g. "Good", "Bad").
        
        Args:
            data (pd.DataFrame): Input data containing geo_col and category_col
            geo_col (str): Column with State codes (UF) e.g., 'SP', 'RJ'
            category_col (str): Column with category names
            color_map (dict): Dictionary mapping category names to hex colors
            title (str): Map title
            output_path (str): Path to save the PNG
            legend_order (list): Optional list to force legend order
        """
        
        # Merge data with shapefile
        gdf = self.shapefile.merge(data, left_on='abbrev_state', right_on=geo_col, how='left')
        
        # Fill missing data
        if 'Categoria' not in gdf.columns:
            gdf['Categoria'] = gdf[category_col].fillna('Sem dados')
        
        fig, ax = plt.subplots(1, 1, figsize=(14, 12), facecolor='white')
        
        # Plot categories
        unique_cats = gdf['Categoria'].unique()
        
        for cat in unique_cats:
            if pd.isna(cat) or cat == 'Sem dados':
                color = color_map.get('Sem dados', '#cccccc')
            else:
                color = color_map.get(cat, '#cccccc')
            
            subset = gdf[gdf['Categoria'] == cat]
            if len(subset) > 0:
                subset.plot(ax=ax, color=color, edgecolor='white', linewidth=0.8)
        
        # Ensure 'Sem dados' states are plotted if not already covered
        # (This happens if 'Sem dados' wasn't in the input categories but we have empty map areas)
        # Note: left join keeps all states, so we check for NaNs in the merged column
        missing = gdf[gdf[category_col].isna()]
        if len(missing) > 0:
             missing.plot(ax=ax, color=color_map.get('Sem dados', '#cccccc'), edgecolor='white', linewidth=0.8)

        ax.axis('off')
        ax.set_title(title, fontsize=18, fontweight='bold', pad=20, color='#333333')
        
        # Build Legend
        legend_patches = []
        
        # logical order for legend: if provided use it, else alphabetic
        cats_to_plot = legend_order if legend_order else sorted([c for c in color_map.keys() if c != 'Sem dados'])
        
        for cat in cats_to_plot:
            if cat in color_map:
                legend_patches.append(mpatches.Patch(facecolor=color_map[cat], edgecolor='white', label=cat))
        
        # Always add 'Sem dados' at the end if it's in the map
        if 'Sem dados' in color_map: # and 'Sem dados' not in cats_to_plot:
             legend_patches.append(mpatches.Patch(facecolor=color_map['Sem dados'], edgecolor='white', label='Sem dados'))

        ax.legend(
            handles=legend_patches,
            loc='lower right',
            frameon=False,
            fontsize=15
        )
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Map saved to: {output_path}")
        plt.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Brazil State Map")
    parser.add_argument("--input", required=True, help="Input CSV file")
    parser.add_argument("--geo-col", required=True, help="Column with UF codes")
    parser.add_argument("--value-col", required=True, help="Column with Category values")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--title", required=True, help="Map Title")
    
    args = parser.parse_args()
    
    df = pd.read_csv(args.input)
    
    gen = BrazilMapGenerator()
    gen.plot_discrete_map(
        data=df,
        geo_col=args.geo_col,
        category_col=args.value_col,
        color_map=DEFAULT_DISCRETE_PALETTE,
        title=args.title,
        output_path=args.output
    )
