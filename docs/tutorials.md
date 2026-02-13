# Data Pro Max — Tutorials

## Tutorial 1: Survey Analysis Pipeline

### Scenario
You have customer satisfaction survey data and need to:
1. Profile the data
2. Calculate key metrics (NPS, satisfaction)
3. Find satisfaction drivers
4. Create segments
5. Generate report

### Step-by-Step

#### Step 1: Analyze the Dataset

```bash
datapro analyze survey.csv --domain survey --goal "satisfaction drivers" -o plan.md
```

#### Step 2: Calculate Key Metrics

```python
import pandas as pd

df = pd.read_csv("survey.csv")

# NPS Calculation
def calculate_nps(df, col):
    promoters = (df[col] >= 9).sum()
    detractors = (df[col] <= 6).sum()
    total = df[col].notna().sum()
    return round((promoters - detractors) / total * 100, 1)

nps = calculate_nps(df, 'recommend_score')
print(f"NPS: {nps}")

# Top-Box Satisfaction
top_box = (df['satisfaction'] >= 4).sum() / df['satisfaction'].notna().sum() * 100
print(f"Top-2 Box: {top_box:.1f}%")
```

#### Step 3: Factor Analysis for Satisfaction Drivers

```python
from factor_analyzer import FactorAnalyzer
import pandas as pd

# Select satisfaction items
sat_cols = ['q1_product', 'q2_service', 'q3_price', 'q4_support', 'q5_delivery']

fa = FactorAnalyzer(n_factors=2, rotation='varimax')
fa.fit(df[sat_cols].dropna())

loadings = pd.DataFrame(
    fa.loadings_,
    index=sat_cols,
    columns=['Factor_1', 'Factor_2']
).round(3)

print(loadings)
```

#### Step 4: Customer Segmentation

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Prepare data
segment_cols = ['satisfaction', 'loyalty', 'usage_frequency']
data = df[segment_cols].dropna()

# Scale and cluster
scaler = StandardScaler()
scaled = scaler.fit_transform(data)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df.loc[data.index, 'segment'] = kmeans.fit_predict(scaled)

# Profile segments
profiles = df.groupby('segment')[segment_cols].mean().round(2)
print(profiles)
```

#### Step 5: Generate Visualizations

```python
import matplotlib.pyplot as plt
import seaborn as sns

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# NPS Distribution
ax = axes[0, 0]
df['recommend_score'].plot.hist(bins=11, ax=ax, color='#3b82f6')
ax.set_title('NPS Distribution')

# Satisfaction by Segment
ax = axes[0, 1]
sns.barplot(data=df, x='segment', y='satisfaction', ax=ax, palette='RdYlGn')
ax.set_title('Satisfaction by Segment')

# Factor Loadings
ax = axes[1, 0]
loadings.plot.barh(ax=ax)
ax.set_title('Factor Loadings')

# Segment Sizes
ax = axes[1, 1]
df['segment'].value_counts().plot.pie(ax=ax, autopct='%1.1f%%')
ax.set_title('Segment Distribution')

plt.tight_layout()
plt.savefig('analysis_charts.png', dpi=150)
plt.close()
```

#### Step 6: Generate Report

```bash
datapro report analysis.md -o report.pdf \
    --title "Customer Satisfaction Analysis" \
    --subtitle "Q1 2026" \
    --color "2980b9"
```

---

## Tutorial 2: A/B Test Analysis

### Scenario
Compare conversion rates between control and treatment groups.

```python
from scipy import stats
import pandas as pd

df = pd.read_csv("ab_test.csv")

# Filter groups
control = df[df['group'] == 'control']['converted']
treatment = df[df['group'] == 'treatment']['converted']

# Chi-square test for proportions
contingency = pd.crosstab(df['group'], df['converted'])
chi2, p, dof, expected = stats.chi2_contingency(contingency)

# Conversion rates
control_rate = control.mean() * 100
treatment_rate = treatment.mean() * 100
lift = (treatment_rate - control_rate) / control_rate * 100

print(f"""
A/B Test Results:
-----------------
Control Conversion: {control_rate:.2f}%
Treatment Conversion: {treatment_rate:.2f}%
Lift: {lift:.1f}%
P-value: {p:.4f}
Significant: {'Yes' if p < 0.05 else 'No'}
""")
```

---

## Tutorial 3: Time Series Analysis

### Scenario
Analyze sales trends over time.

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sales.csv", parse_dates=['date'])
df.set_index('date', inplace=True)

fig, axes = plt.subplots(3, 1, figsize=(12, 10))

# Daily sales
axes[0].plot(df['sales'], color='#3b82f6')
axes[0].set_title('Daily Sales')

# 7-day moving average
df['ma_7'] = df['sales'].rolling(7).mean()
axes[1].plot(df['sales'], alpha=0.3)
axes[1].plot(df['ma_7'], color='#dc2626')
axes[1].set_title('7-Day Moving Average')

# Monthly aggregation
monthly = df['sales'].resample('M').sum()
axes[2].bar(monthly.index, monthly.values, color='#22c55e')
axes[2].set_title('Monthly Sales')

plt.tight_layout()
plt.savefig('timeseries.png', dpi=150)
plt.close()
```

---

## Tutorial 4: Using Weights in Survey Analysis

### Scenario
Apply sample weights for representative results.

```python
import pandas as pd

df = pd.read_csv("survey_with_weights.csv")

# Simple (unweighted) frequency
unweighted = df['satisfaction'].value_counts(normalize=True) * 100

# Weighted frequency
def weighted_frequency(df, col, weight_col):
    result = df.groupby(col)[weight_col].sum()
    return result / result.sum() * 100

weighted = weighted_frequency(df, 'satisfaction', 'weight')

# Compare
comparison = pd.DataFrame({
    'Unweighted %': unweighted,
    'Weighted %': weighted
}).round(1)

print(comparison)

# Weighted mean
weighted_mean = (df['satisfaction'] * df['weight']).sum() / df['weight'].sum()
print(f"\nWeighted Mean Satisfaction: {weighted_mean:.2f}")
```

---

## Common Patterns

### Check Normality Before Tests

```python
from scipy import stats

stat, p = stats.shapiro(df['score'].dropna()[:5000])  # Limit for performance

if p < 0.05:
    print("Data is NOT normally distributed → Use non-parametric tests")
    # Use Mann-Whitney instead of t-test
    # Use Kruskal-Wallis instead of ANOVA
else:
    print("Data is approximately normal → Parametric tests OK")
```

### Calculate Effect Size

```python
import numpy as np

def cohens_d(group1, group2):
    """Calculate Cohen's d effect size."""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std

d = cohens_d(treatment_scores, control_scores)
interpretation = 'small' if abs(d) < 0.5 else 'medium' if abs(d) < 0.8 else 'large'
print(f"Cohen's d: {d:.3f} ({interpretation} effect)")
```

### Handle Missing Data

```python
# Document missing data
missing_report = df.isna().sum().sort_values(ascending=False)
missing_pct = (missing_report / len(df) * 100).round(1)

# Decision tree:
# < 5%: Listwise deletion OK
# 5-30%: Consider imputation
# > 30%: Consider dropping variable

print(missing_pct[missing_pct > 0])
```
