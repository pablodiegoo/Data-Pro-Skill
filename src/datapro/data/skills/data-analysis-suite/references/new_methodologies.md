# Harvested Methodologies & Patterns - Festival Verão 2026

## 1. Dual Clustering (K-Means vs. DBSCAN)
**Problem**: Traditional K-Means clustering forces every respondent into a bucket, even if they are noise or don't fit well. This leads to muddy personas.
**New Pattern**: Run *both* algorithms side-by-side.
- Use **K-Means** strictly for defining fixed " मार्केटिंग Personas " (e.g., finding the 3 main types of attendees).
- Use **DBSCAN** for Density/Outlier detection to identify respondents who belong to no cluster (`-1`) or to find tightly packed natural sub-populations that K-Means missed.
*Implementation found in*: `advanced_analytics_generator.py`

## 2. Dual Correlation (Pearson vs. Spearman)
**Problem**: Pearson correlation assumes linearity. Survey data (Likert scales 0-10) is often monotonic but non-linear.
**New Pattern**: Plotting two heatmaps side-by-side. 
- **Pearson** for true continuous financial/age data.
- **Spearman** for rank-based relationships between satisfaction scores. Differences between the two charts often highlight non-linear thresholds (e.g., satisfaction only drops after a score falls below 4).
*Implementation found in*: `advanced_analytics_generator.py`

## 3. The "Pure Sentiment" Stack (Ipsative + Residuals)
**Problem**: Survey respondents have different baselines. A "7" for a harsh critic is amazing; an "8" for an easy grader is terrible (Halo Effect/Response Bias).
**New Pattern**:
- **Ipsative Centering**: Subtract the respondent's *personal mean* rating from every score they gave. This shows their *relative* preferences.
- **Halo Removal**: Run a quick linear regression predicting a specific attribute score based on their personal mean score. The *residuals* represent the true, bias-free assessment of that attribute.
*Implementation found in*: `advanced_analytics_generator.py`

## 4. Chi-Squared Residual Heatmapping
**Problem**: Crosstabs are hard to read quickly to find statistical anomalies.
**New Pattern**: Calculate the Chi-Squared expected values for a crosstab, compute the standardized residuals `(observed - expected) / sqrt(expected)`, and plot *that* as a seaborn heatmap. Any cell with a value > 2 or < -2 visually pops out as a statistically significant anomaly (e.g., Tourists unexpectedly rating Parking very low).
*Implementation found in*: `advanced_analytics_generator.py`
