---
name: tufte-viz
description: "Guidelines and Python code templates for generating Tufte-style, high data-ink ratio visualizations."
---

# Tufte Visualizations: High Data-Ink Ratio Guidelines

To maintain clean, elegant, and highly informative plots that align with Edward Tufte's principles, ensure all Python scripts that generate visualizations conform to these guidelines.

---

## 1. Core Visual Principles

1.  **Maximize the Data-Ink Ratio**: 
    - Strip away everything that isn't data. 
    - No background fills, no border boxes (spines), and no heavy gridlines.
2.  **Typography**:
    - Use clean, legible serif typography for titles, labels, and ticks (e.g., Palatino, Georgia, Garamond, or system serif) rather than standard sans-serif.
3.  **Label Directly (No Legend Box)**:
    - Avoid floating legend boxes. Instead, draw the labels directly at the end of the line or next to the category.
4.  **No 3D or Drop Shadows**:
    - Never use 3D bars, pies, or shadow effects. They distort proportions and violate visual integrity.
5.  **Clean Color Palette**:
    - Use curated, soft, and high-contrast color palettes (e.g., subtle grays with a single vivid accent color to highlight key findings).

---

## 2. Python Code Snippet (Matplotlib / Seaborn)

To apply these rules programmatically, always use the package helper:
```python
from datapro.styles import set_tufte_theme
import matplotlib.pyplot as plt

# 1. Setup the theme
set_tufte_theme()

fig, ax = plt.subplots(figsize=(6, 4), dpi=300)

# 2. Plot data (e.g., line chart)
x = [1, 2, 3, 4]
y1 = [10, 15, 13, 18]
y2 = [12, 11, 14, 16]

ax.plot(x, y1, color='#1c3d5a', lw=1.8)
ax.plot(x, y2, color='#7f8c8d', lw=1.5, ls='--')

# 3. Direct Labeling (Tufte style - no legend box)
ax.text(x[-1] + 0.1, y1[-1], 'Segment A (Core)', color='#1c3d5a', va='center', fontsize=9, weight='bold')
ax.text(x[-1] + 0.1, y2[-1], 'Segment B (Control)', color='#7f8c8d', va='center', fontsize=9)

# 4. Final tweaks (adjust limits for labels)
ax.set_xlim(x[0], x[-1] + 1.2)
ax.set_title('Métrica de Desempenho ao Longo do Tempo', loc='left', pad=15, fontsize=11, weight='bold')

plt.tight_layout()
plt.savefig('outputs/figures/performance_trend.png', bbox_inches='tight')
plt.close()
```

---

## 3. Tufte Chart Checklist

- [ ] Are the top and right borders (spines) hidden?
- [ ] Are the bottom and left spines thin or hidden?
- [ ] Is the font set to a clean serif family?
- [ ] Are the data labels placed directly next to the data rather than in a legend box?
- [ ] Is the background strictly white or transparent (no light grey background fill)?
- [ ] Are the gridlines either thin, dotted light grey, or completely hidden?
