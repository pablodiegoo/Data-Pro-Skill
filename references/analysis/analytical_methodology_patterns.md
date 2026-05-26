# Statistical Analytical Patterns

## Overview

This reference documents analytical methodologies used in the "Practical Statistics for Data Scientists" codebase that solve common practical problems in data science.

---

## Pattern 1: Clustering with Mixed Data Types (Gower Distance)

### Problem
Standard distance metrics like Euclidean or Manhattan only work on numeric data. When a dataset contains both numeric (age, income) and categorical (gender, home ownership) variables, standard K-Means fails.

### Solution
Use **Gower's distance**, which calculates a dissimilarity between 0 and 1 for each variable and averages them:
- **Numeric**: Normalized absolute difference.
- **Categorical**: 0 if same, 1 if different.
- **Ordered Factor**: Rank-based distance.

### Application
Use Gower distance with **Hierarchical Clustering** (Agglomerative) because K-Means requires a "mean" (centroid) which is not well-defined for categorical data in the same way.

---

## Pattern 2: Multi-Pass Principal Component Interpretation

### Problem
PCA outputs components that are linear combinations of all features, making them hard to explain to stakeholders.

### Solution
Follow a two-stage interpretation process:
1. **Scree Plot Analysis**: Identify the "elbow" where adding more components provides diminishing returns in explained variance.
2. **Loading Analysis**: Plot the weights (loadings) for the top components as bar charts.
   - **Identify Sign**: Group features with same sign (they move together).
   - **Identify Magnitude**: Focus on features with loading absolute value > 0.3.

---

## Pattern 3: Resampling-Based Significance Testing (Permutation)

### Problem
Student's t-test and ANOVA have strict assumptions (normality, equal variance) that real-world data often violates.

### Solution
Use **Permutation Tests** to create a "custom" null distribution by shuffling group labels.
1. Combine all data.
2. Shuffled/randomly re-assign to groups.
3. Calculate test statistic (e.g., difference in means).
4. Repeat 1,000+ times to build the distribution.
5. Compare observed statistic to this distribution.

---

## Pattern 4: Robust Scale Estimation (MAD)

### Problem
Standard deviation is highly sensitive to outliers. A single extreme value can drastically inflate the scale estimate.

### Solution
Use **Median Absolute Deviation (MAD)**:
`MAD = median(|X_i - median(X)|)`

---

## Pattern 5: Handling Class Imbalance with Cost-Sensitive Learning

### Problem
In classification (e.g., loan default), the "minority" class is often the one we care about most. Accuracy is a poor metric.

### Solution
Instead of just SMOTE (data generation), use **Cost-Sensitive Learning**:
1. Assign higher weights to minority class samples during training.
2. Use **Weighted Logistic Regression** or `scale_pos_weight` in boosted models.
3. Evaluate using **Partial Residuals** for the probability scores specifically on the minority class.

---

## Pattern 6: Grouping High-Cardinality Categorical Variables

### Problem
Categorical variables with many levels (e.g., zip codes, product IDs) can lead to overfitting or sparse levels when used directly in models.

### Solution
Instead of using the raw levels, group them based on an emotional or analytical metric. One powerful approach from Chapter 4 is:
1. Fit a preliminary model with essential features.
2. Calculate the **Median Residual** for each categorical level.
3. Rank the levels by their median residual and group them into **quantiles** (e.g., quintiles).
4. Use this new "Group ID" as a categorical feature in the final model.
