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
See `correlation_ellipse_plot.py`

### When to Use
- Academic papers with grayscale requirements
- Textbooks and educational materials
- Presentations that will be printed
- Accessibility-first visualizations

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
See `partial_residual_plot.py`

### When to Use
- Diagnosing nonlinearity in regression models
- Validating polynomial term necessity
- Checking for missed transformations
- Model specification testing

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

---

## Pattern 4: Weighted Regression Visualization

### Context
When data quality varies over time or across groups, standard regression gives equal weight to all observations.

---

## Pattern 5: Factor Variable Encoding Visualization

### Context
Categorical variables require encoding for regression. Multiple encoding schemes exist.

---

## General Principles for Educational Visualizations

### 1. **Grayscale First**
- Design for black and white
- Add color as enhancement

### 2. **Reproducible Examples**
- Include complete code
- Use fixed random seeds
