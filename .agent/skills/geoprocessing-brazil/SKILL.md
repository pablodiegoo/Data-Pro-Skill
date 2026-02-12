---
name: geoprocessing-brazil
description: "Normalization and state-mapping of municipal data and generation of professional choropleth maps of Brazil (UF/State level). Use for: (1) Detecting city/state strings and normalizing names, (2) Attaching regional metadata, (3) Generating professional maps integrating survey data with shapefiles."
---

# Geoprocessing Brazil

This skill unifies the process of geographic data treatment and map visualization for the Brazilian territory.

## 1. Municipality Normalization
Cleaning and standardizing city and state names from diverse strings (e.g., "São Paulo - SP", "Rio/RJ").

- **Script**: `scripts/municipality_mapper.py`
- **Functionality**: Detects, cleans, and attaches metadata (Region, UF, IBGE Code if available).

## 2. Choropleth Map Generation
Creation of thematic maps based on scores or categories by State.

### Capabilities:
- **Automatic Merge**: Joins your data (DataFrame) with Brazil shapefiles.
- **Custom Styling**: Sebrae-friendly color palettes and legend control.

### Usage:
- **Script**: `scripts/map_generator.py`

```python
from scripts.map_generator import generate_brazil_map

# Example: Generate satisfaction map by UF
generate_brazil_map(df, score_col="Score", title="Satisfaction by State", filename="brazil_map.png")
```

## 3. Recommended Workflow

1. **Cleaning**: Use `municipality_mapper` to ensure the UF column is standardized (e.g., 'SP', 'RJ').
2. **Aggregation**: Group your data by the UF column (Example: `df.groupby('UF')['Score'].mean()`).
3. **Visualization**: Pass the resulting DataFrame to `map_generator`.

---
> [!NOTE]
> For city-level maps (beyond UF), check for specific shapefile availability or IBGE APIs.
