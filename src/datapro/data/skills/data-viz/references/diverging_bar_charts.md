# Diverging Bar Charts for Association Matrices (Residuals)

## The Pattern
When performing a Chi-Square Residual analysis across an Association Matrix (e.g., Platforms vs Churn Reasons), standard heatmaps (`sns.heatmap`) can often be visually overwhelming for business stakeholders because the numbers (Standardized Residuals) are abstract.

A better analytical visualization pattern harvested from OS18 is the **Diverging Bar Chart per Entity**. 

## Implementation Strategy
Instead of one massive matrix, loop through the primary entities (e.g., `['Mercado Livre', 'Shopee', 'Americanas']`) and generate an individual horizontal bar chart (`plt.barh`) for each. 

1. **Calculate the Residual (Relevância)**
   - `Relevancia = abs(O - E) / sqrt(E)`
2. **Determine Direction (Acima / Abaixo da Média)**
   - If `O > E`, the feature is a specific bottleneck/differentiator for that entity (Positive Score).
   - If `O < E`, the feature is less common than average for that entity (Negative Score).
3. **Plotting logic**
   - Multiply the Relevancy score by `-1` if it is "Abaixo da Média".
   - Color code the bars: `#e74c3c` (Red) for values `> 0`, and `#2ecc71` (Green) for values `< 0`.
   - Add a vertical line at `x=0` (`plt.axvline(0, color='black')`).

## Business Value
This visualization immediately answers two questions for the client:
- "Where is this entity specifically failing compared to the market?" (Right side / Red)
- "Where is this entity performing better than the market average?" (Left side / Green)
