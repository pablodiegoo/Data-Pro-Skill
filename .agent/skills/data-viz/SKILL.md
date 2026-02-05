---
name: data-viz
description: "Generates professional statistical charts (Bar, Pie, Grouped) using Matplotlib and Seaborn. Use this skill to visualize survey data, trends, and distributions for reports."
---

# Data Viz Skill

This skill provides a standardized way to generate high-quality statistical charts for reports. It handles styling (using Sebrae-compatible colors), layout, and saving to files.

## Capabilities

### 1. Bar Charts (`plot_bar`)
Best for comparing categories or counts. Supports vertical and horizontal orientation.
- **Vertical**: Good for few categories with short labels.
- **Horizontal**: Good for many categories or long labels.

### 2. Pie Charts (`plot_pie`)
Best for showing composition (shares) of a whole. Limit to Top 5-7 categories for readability.

### 3. Grouped Bar Charts (`plot_grouped_bar`)
Best for comparing distributions across segments (e.g., Satisfaction by Region). Automatically calculates percentages within groups.

## Usage

```python
import pandas as pd
from scripts.plotter import plot_bar, plot_pie, plot_grouped_bar

# Load data
df = pd.read_csv("data.csv")

# 1. Simple Bar Chart (Top 10 Cities)
plot_bar(df, x_col="City", title="Respondents by City", filename="output/city_dist.png", orientation='h')

# 2. Pie Chart (Sector Share)
plot_pie(df, col="Sector", title="Distribution by Sector", filename="output/sector_pie.png")

# 3. Crosstab (Satisfaction x Region)
plot_grouped_bar(df, x_col="Satisfaction", hue="Region", title="Satisfaction by Region", filename="output/sat_region.png")
```

## Dependencies
Requires `matplotlib`, `seaborn`, and `pandas`.
```bash
pip install matplotlib seaborn pandas
```
