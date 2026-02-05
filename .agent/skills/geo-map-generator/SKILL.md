---
name: geo-map-generator
description: "Generates professional choropleth maps of Brazil (State/UF level). Handles shapefile loading, data merging, and customized styling for reports."
---

# Geo Map Generator Skill

This skill provides a reusable tool to generate high-quality maps of Brazil, visualizing data by State (UF). It abstracts away the complexity of `geopandas` and `geobr`.

## Capabilities

- **State-Level Maps**: visualizes data by coloring Brazilian states.
- **Custom Palettes**: Supports categorical (discrete) or continuous color scales.
- **Custom Legends**: Generates clean, publication-ready legends.
- **Pre/Post Comparison**: Easy to generate multiple maps with consistent styling for comparison.

## Dependencies

- `pandas`
- `geopandas`
- `geobr`
- `matplotlib`

## Usage

```bash
# Example: Generate a map from a CSV file
python3 .agent/skills/geo-map-generator/scripts/generator.py \
  --input "data.csv" \
  --geo-col "UF" \
  --value-col "Score" \
  --output "map.png" \
  --title "Average Score by State"
```

## Python API Usage

```python
from scripts.generator import BrazilMapGenerator

# Initialize
generator = BrazilMapGenerator()

# Load Data
data = pd.read_csv("data.csv")

# Plot
generator.plot_state_map(
    data=data,
    geo_col="UF",
    value_col="Score",
    title="My Map",
    output_path="output.png"
)
```
