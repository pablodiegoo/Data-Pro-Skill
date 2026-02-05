---
name: survey-data-viz
description: "Generates professional statistical charts (Bar, Pie, Grouped) using Matplotlib and Seaborn. Use this skill to visualize survey data, trends, and distributions for reports. Optimized for survey-specific needs like 'Before vs After' evolution charts and premium aesthetics."
---

# Survey Data Visualization

This skill provides templates for high-quality survey visualizations with refined aesthetics (contrast, typography, and Sebrae-compatible palettes).

## Capabilities

### 1. Evolution Line Charts (`plot_evolution`)
Best for comparing means of domains across two points in time (e.g., Início vs Final).
- **Format**: Shows multiple lines/markers representing different domains or segments.

### 2. Segmented Bar Charts (`plot_proportions`)
Visualizes distribution of responses (e.g., how many people answered "Ótimo" per region).

### 3. Word Clouds (`plot_word_cloud`)
Specialized for qualitative data. Use this with `survey-qual-analyzer` frequencies.

## Usage

```python
from scripts.evolution_plotter import plot_evolution_line

# Data format expected: DataFrame with 'Cycle', 'Domain', and 'Mean'
plot_evolution_line(df, x="Cycle", y="Mean", hue="Domain", title="Evolution of Domains", filename="output/evolution.png")
```

## Aesthetic Standards
- **Palette**: Dark blue, cyan, and neutral grays for contrast.
- **Fonts**: Clear, sans-serif fonts.
- **Labels**: Always include sample size (n) if available.
