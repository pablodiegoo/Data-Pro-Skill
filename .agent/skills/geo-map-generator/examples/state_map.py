#!/usr/bin/env python3
"""
Example: OS12 Map Generation using geo-map-generator skill
"""

import sys
import os
import pandas as pd

# Add skill directory to path to import generator
# logic to find the relative path or install it as a package would be better in prod,
# but for this local agent context, we append the specific path.
current_dir = os.path.dirname(os.path.abspath(__file__))
skill_dir = os.path.dirname(current_dir)
sys.path.append(skill_dir)

from scripts.generator import BrazilMapGenerator, DEFAULT_DISCRETE_PALETTE

# Define custom palette/legend if needed (or use default)
# The OS12 report uses specific labels in the legend, which we can customize.
OS12_PALETTE = DEFAULT_DISCRETE_PALETTE

OS12_LEGEND_ORDER = [
    'Ótimo', 
    'Bom', 
    'Médio', 
    'Ruim', 
    'Péssimo'
]

def main():
    print("Generating Example Map...")
    
    # Mock Data for demonstration if actual file not found
    data = pd.DataFrame({
        'UF': ['SP', 'RJ', 'MG', 'BA', 'AM', 'RS'],
        'Category': ['Ótimo', 'Bom', 'Médio', 'Ruim', 'Péssimo', 'Ótimo']
    })
    
    # Initialize Generator
    gen = BrazilMapGenerator()
    
    # Plot Map
    output_file = os.path.join(current_dir, "example_output.png")
    
    gen.plot_discrete_map(
        data=data,
        geo_col="UF",
        category_col="Category",
        color_map=OS12_PALETTE,
        title="Example Map: Satisfaction by State",
        output_path=output_file,
        legend_order=OS12_LEGEND_ORDER
    )
    
    print(f"Verified! Output saved to: {output_file}")

if __name__ == "__main__":
    main()
