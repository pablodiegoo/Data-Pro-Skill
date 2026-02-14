# Educational Code Documentation Standards

## Context

This rule applies when creating **educational or reference code** (tutorials, textbooks, examples) as opposed to production analytics code.

## Rule: Prioritize Clarity Over Efficiency

> Educational code MUST prioritize readability and pedagogical value over performance optimization.

### Why
- Educational code teaches concepts, not production patterns
- Explicit steps are more valuable than clever one-liners
- Students need to see intermediate results

### Examples

**✅ GOOD (Educational)**
```python
# Calculate trimmed mean step-by-step
sorted_values = sorted(data)
n = len(sorted_values)
trim_count = int(n * 0.1)  # Remove 10% from each tail
trimmed = sorted_values[trim_count:-trim_count]
trimmed_mean = sum(trimmed) / len(trimmed)
print(f"Trimmed mean: {trimmed_mean}")
```

**❌ AVOID (Too concise for learning)**
```python
# One-liner that obscures the process
trimmed_mean = trim_mean(data, 0.1)
```

**✓ ACCEPTABLE (With explanation)**
```python
# Using scipy's built-in function
# This removes 10% from each tail (20% total)
from scipy.stats import trim_mean
trimmed_mean = trim_mean(data, proportiontocut=0.1)
print(f"Trimmed mean: {trimmed_mean}")
```

---

## Rule: Always Include Interpretive Output

> Educational scripts MUST print intermediate results with interpretive labels.

### Why
- Helps learners verify their understanding
- Shows what "good" output looks like
- Enables self-checking

### Examples

**✅ GOOD**
```python
print(f"Sample mean: {mean:.2f}")
print(f"Trimmed mean (10%): {trimmed_mean:.2f}")
print(f"Difference: {abs(mean - trimmed_mean):.2f}")
print("→ Large difference suggests outliers are present")
```

**❌ AVOID**
```python
print(mean, trimmed_mean)  # No context
```

---

## Rule: Use Consistent Example Data

> Educational examples SHOULD use well-known, publicly available datasets.

### Why
- Enables readers to reproduce examples
- Builds familiarity with standard datasets
- Reduces cognitive load

### Recommended Datasets
- **State statistics**: `state.csv` (US state demographics)
- **Housing**: `house_sales.csv` (King County, WA)
- **Loans**: `lc_loans.csv` (Lending Club)
- **Stock prices**: `sp500_data.csv`

### Pattern
```python
# Always include data source comment
# Data: US state statistics (population, murder rate, etc.)
state = pd.read_csv('data/state.csv')
```

---

## Rule: Annotate Visualizations Heavily

> Educational plots MUST include:
> 1. Axis labels with units
> 2. Title describing what is shown
> 3. Annotations for key features
> 4. Legend when multiple series

### Why
- Plots should be self-explanatory
- Readers may view plots separately from code
- Reinforces interpretation skills

### Example
```python
fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(perm_diffs, bins=20, alpha=0.7, edgecolor='black')
ax.axvline(observed_diff, color='red', linewidth=2, label='Observed')
ax.set_xlabel('Difference in Means')
ax.set_ylabel('Frequency')
ax.set_title('Permutation Distribution (n=10,000)')
ax.legend()
ax.text(observed_diff + 5, 100, f'p = {p_value:.3f}', 
        bbox=dict(boxstyle='round', facecolor='wheat'))
plt.tight_layout()
plt.show()
```

---

## Rule: Provide Both Manual and Library Implementations

> When teaching a statistical concept, SHOULD show:
> 1. Manual calculation (for understanding)
> 2. Library function (for practice)
> 3. Comparison to verify equivalence

### Example
```python
# Manual MAD calculation
median_val = df['value'].median()
deviations = abs(df['value'] - median_val)
mad_manual = deviations.median() / 0.6744897501960817

# Using statsmodels
from statsmodels import robust
mad_library = robust.scale.mad(df['value'])

# Verify they match
print(f"Manual MAD: {mad_manual:.2f}")
print(f"Library MAD: {mad_library:.2f}")
print(f"Match: {np.isclose(mad_manual, mad_library)}")
```

---

## Rule: Use Fixed Random Seeds

> Educational code with randomness MUST set a fixed seed.

### Why
- Enables exact reproduction
- Allows readers to verify their results
- Prevents confusion from varying output

### Example
```python
import random
import numpy as np

# Set seeds for reproducibility
random.seed(42)
np.random.seed(42)

# Now random operations are reproducible
sample = np.random.normal(0, 1, 100)
```

---

## Rule: Progressive Complexity

> Educational examples SHOULD build from simple to complex.

### Pattern
1. **Basic**: Single variable, simple operation
2. **Intermediate**: Multiple variables, standard analysis
3. **Advanced**: Full analysis with diagnostics

### Example Structure
```python
# BASIC: Single variable summary
print(df['value'].describe())

# INTERMEDIATE: Compare groups
print(df.groupby('group')['value'].describe())

# ADVANCED: Statistical test with visualization
result = permutation_test(group_a, group_b)
plot_permutation_distribution(result)
```

---

## When This Rule Does NOT Apply

This rule is **NOT** for:
- Production analytics pipelines
- Performance-critical code
- Internal utility functions
- Code that will be maintained long-term

For those cases, follow standard `coding-standards.md` rules.

---

## Integration with Existing Rules

This rule **complements** existing rules:
- Still close figures (`plt.close()`)
- Still check for upstream skills
- Still follow PEP 8 style

The difference is **pedagogical intent** takes priority over production patterns.
