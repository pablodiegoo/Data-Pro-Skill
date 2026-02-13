# Statistical Visualization Patterns for Educational Content

## Overview

This reference documents visualization patterns from "Practical Statistics for Data Scientists" that are particularly effective for educational and academic content, especially publications with grayscale constraints.

## Pattern 1: Correlation Ellipse Visualization

### Context
Traditional correlation heatmaps rely on color to convey information, making them unsuitable for:
- Grayscale publications
- Print media with limited color
- Accessibility requirements (color-blind readers)

### Solution
Use ellipses to represent correlations where:
- **Ellipse width**: Correlation strength (wider = stronger)
- **Ellipse angle**: Correlation direction (diagonal = positive/negative)
- **Ellipse eccentricity**: Inverse of correlation strength

### Implementation
See `assets/harvest/scripts/correlation_ellipse_plot.py`

### When to Use
- Academic papers with grayscale requirements
- Textbooks and educational materials
- Presentations that will be printed
- Accessibility-first visualizations

### Example Output
```
     A    B    C    D    E
A  [●]  [/]  [\]  [―]  [|]
B  [/]  [●]  [―]  [/]  [\]
C  [\]  [―]  [●]  [|]  [/]
...
```
Where:
- `●` = perfect correlation (1.0)
- `/` = strong positive correlation
- `\` = strong negative correlation
- `―` = weak positive correlation
- `|` = weak negative correlation

---

## Pattern 2: Partial Residual Plots for Nonlinear Diagnostics

### Context
Standard residual plots can miss nonlinear relationships in individual predictors when using polynomial or interaction terms.

### Solution
Partial residual plots isolate the contribution of a single predictor by:
1. Computing residuals from the full model
2. Adding back the contribution of the target predictor
3. Plotting against the predictor values
4. Adding LOWESS smoothing to reveal patterns

### Implementation
See `assets/harvest/scripts/partial_residual_plot.py`

### When to Use
- Diagnosing nonlinearity in regression models
- Validating polynomial term necessity
- Checking for missed transformations
- Model specification testing

### Interpretation
- **Black line**: Fitted relationship for the predictor
- **Gray line**: LOWESS smooth (should match black if model is correct)
- **Scatter**: Partial residuals (should be randomly distributed)

**Good fit**: LOWESS and fitted lines overlap  
**Poor fit**: LOWESS shows curvature not captured by fitted line

---

## Pattern 3: Permutation Test Visualization

### Context
Parametric tests (t-tests, ANOVA) assume normality and equal variances. Permutation tests provide:
- Distribution-free inference
- Exact p-values for small samples
- Intuitive visual interpretation

### Solution
Visualize the permutation distribution with:
1. Histogram of permuted test statistics
2. Vertical line at observed statistic
3. Annotation showing p-value region

### When to Use
- Small sample sizes (n < 30)
- Non-normal distributions
- Teaching hypothesis testing concepts
- A/B testing without assumptions

### Example Visualization
```
Permutation Distribution
     
 200 |     ___
     |    /   \
 150 |   /     \___
     |  /          \___
 100 | /              \___
     |/                   \___
  50 |________________________\___
     |                    |
   0 +--------------------+--------
     -10  -5   0   5  10  15  20
                         ↑
                    Observed (p=0.03)
```

---

## Pattern 4: Weighted Regression Visualization

### Context
When data quality varies over time or across groups, standard regression gives equal weight to all observations.

### Solution
Compare weighted vs. unweighted residuals over time:
1. Fit both weighted and unweighted models
2. Plot absolute residuals by time period
3. Show how weighting reduces recent errors

### When to Use
- Time series with changing variance
- Data quality varies by source
- Recent data more reliable
- Heteroskedastic errors

---

## Pattern 5: Factor Variable Encoding Visualization

### Context
Categorical variables require encoding for regression. Multiple encoding schemes exist.

### Solution
Show side-by-side comparison of:
- One-hot encoding (all categories)
- Dummy encoding (drop first category)
- Effect coding (sum-to-zero constraints)

### When to Use
- Teaching regression with categorical variables
- Explaining coefficient interpretation
- Documenting encoding decisions

---

## General Principles for Educational Visualizations

### 1. **Annotation is Key**
- Label observed statistics
- Mark critical regions
- Add interpretive text

### 2. **Progressive Complexity**
- Start with simple plots
- Add layers of information
- Build to full complexity

### 3. **Grayscale First**
- Design for black and white
- Add color as enhancement
- Test in grayscale

### 4. **Consistent Aesthetics**
- Use same style across chapter
- Maintain aspect ratios
- Standardize font sizes

### 5. **Reproducible Examples**
- Include complete code
- Use fixed random seeds
- Document dependencies

---

## References

- Bruce, P., Bruce, A., & Gedeck, P. (2020). *Practical Statistics for Data Scientists* (2nd ed.). O'Reilly Media.
- Cleveland, W. S. (1993). *Visualizing Data*. Hobart Press.
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information* (2nd ed.). Graphics Press.

---

## Integration with Data-Pro-Skill

### Recommended Additions

1. **data-viz skill**: Add correlation ellipse plot as alternative to heatmap
2. **data-analysis-suite**: Add partial residual plot to regression diagnostics
3. **stats-causal-inference**: Add permutation test visualization examples
4. **document-mastery**: Add educational visualization guidelines

### Priority
- **High**: Correlation ellipse plot (unique capability)
- **Medium**: Partial residual plot (extends existing)
- **Low**: Permutation visualization (educational focus)
