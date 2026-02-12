---
name: data-viz
description: "Generates professional statistical charts (Bar, Pie, Grouped) using Matplotlib and Seaborn. Use this skill to visualize survey data, trends, and distributions for reports."
---

# Data Viz Skill

This skill provides a standardized way to generate high-quality statistical charts for reports. It handles styling (using Sebrae-compatible colors), layout, and saving to files.

## Capabilities

### 1. Bar Charts (`plot_bar`)
Best for comparing categories or counts. Supports vertical and horizontal orientation.

### 2. Pie Charts (`plot_pie`)
Best for showing composition (shares) of a whole. Limit to Top 5-7 categories for readability.

### 3. Grouped Bar Charts (`plot_grouped_bar`)
Best for comparing distributions across segments.

### 4. Evolution Line Charts (Survey Specific)
Best for comparing means of domains across points in time (e.g., Start vs End). Use `plot_evolution_line`.

### 5. Word Clouds
For qualitative text analysis visualization. Use in conjunction with `survey-qual-analyzer` frequencies.

## Usage

```python
import pandas as pd
from scripts.plotter import plot_bar, plot_pie, plot_grouped_bar
from scripts.evolution_plotter import plot_evolution_line

# Load data
df = pd.read_csv("data.csv")

# 1. Simple Bar Chart (Top 10 Cities)
plot_bar(df, x_col="City", title="Respondents by City", filename="output/city_dist.png", orientation='h')

# 2. Evolution of Domains (Survey Pre vs Post)
# Expected columns: 'Cycle', 'Domain', 'Mean'
plot_evolution_line(df_evo, x="Cycle", y="Mean", hue="Domain", title="Evolution of Domains", filename="output/evolution.png")
```

## Aesthetic Standards & Surveys
- **Palette**: Dark blue, cyan, and neutral grays for contrast.
- **Labels**: Always include sample size (n) if available.
- **Premium**: High DPI (300) and clean backgrounds for publication-ready reports.

## Dependencies
Requires `matplotlib`, `seaborn`, and `pandas`.
