# Statistical Model Evaluation Patterns

## Overview

Educational patterns for evaluating models that go beyond standard performance metrics, focusing on intuition and diagnostic ability.

---

## Pattern 1: Probability Contour Visualizations

### Use Case
Understanding how Gaussian Mixture Models (GMMs) or Linear Discriminant Analysis (LDA) define decision boundaries and uncertainty regions.

### Technique
Map probability density levels to confidence intervals (e.g., 90%, 95%, 99%) and plot them as ellipses or contours over a scatter plot of observations.

---

## Pattern 2: Residual Analysis for Classification

### Use Case
Diagnosing where a model is losing confidence, especially in imbalanced or non-linear scenarios.

### Technique
Plot **Partial Residuals** (predicted log-odds minus actual outcome) against specific features. This reveals if the relationship between a feature and the outcome is truly linear on the logit scale.

---

## Pattern 3: K-Nearest Neighbor (KNN) as a Feature Engine

### Use Case
Adding "non-linear similarity" as a feature for other models (like Logistic Regression).

### Technique
For each entry, calculate the proportion of 'positive' neighbors in its local neighborhood (the "borrower score"). Add this single numeric score as a feature to the primary model.

---

## Integration Reference
- `assets/harvest/scripts/multivariate_normal_contours.py`
- `assets/harvest/scripts/partial_residual_plot.py`
