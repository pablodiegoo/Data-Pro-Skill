# Imbalanced Data Strategies for Classification

## Overview

Imbalanced datasets occur when one class significantly outnumbers another in classification problems. This is common in fraud detection, medical diagnosis, loan default prediction, and many other real-world scenarios.

**Problem**: Standard classifiers trained on imbalanced data tend to:
- Predict the majority class almost exclusively
- Achieve high overall accuracy but poor minority class recall
- Fail to learn meaningful patterns in the minority class

## Strategies

### 1. Undersampling (Majority Class)

**Concept**: Randomly remove samples from the majority class to balance the dataset.

**Pros**:
- Simple and fast
- Reduces training time
- Can improve minority class recall

**Cons**:
- Loses potentially useful information
- May underfit if too aggressive
- Not suitable when minority class is very small

**Implementation**:
```python
# Manual undersampling
n_minority = sum(y == 'default')
majority_indices = y[y == 'paid off'].sample(n_minority).index
minority_indices = y[y == 'default'].index
balanced_indices = majority_indices.union(minority_indices)

X_balanced = X.loc[balanced_indices]
y_balanced = y.loc[balanced_indices]
```

---

### 2. Oversampling (Minority Class)

**Concept**: Duplicate or synthesize samples from the minority class.

#### 2a. Simple Duplication
Randomly duplicate minority class samples until balanced.

**Pros**:
- Retains all original data
- Easy to implement

**Cons**:
- Risk of overfitting (exact duplicates)
- Doesn't add new information

---

#### 2b. SMOTE (Synthetic Minority Over-sampling Technique)

**Concept**: Generate synthetic samples by interpolating between existing minority class samples.

**Algorithm**:
1. For each minority sample, find k nearest neighbors (same class)
2. Randomly select one neighbor
3. Create synthetic sample along the line segment between the two points

**Pros**:
- Creates new, plausible samples
- Reduces overfitting vs. simple duplication
- Widely used and well-tested

**Cons**:
- Can create unrealistic samples in high dimensions
- May amplify noise if minority class has outliers
- Computationally expensive for large datasets

**Implementation**:
```python
from imblearn.over_sampling import SMOTE

X_resampled, y_resampled = SMOTE().fit_resample(X, y)
```

**Variants**:
- **BorderlineSMOTE**: Focuses on samples near decision boundary
- **ADASYN**: Adaptively generates more samples for harder-to-learn examples

```python
from imblearn.over_sampling import ADASYN, BorderlineSMOTE

X_resampled, y_resampled = ADASYN().fit_resample(X, y)
X_resampled, y_resampled = BorderlineSMOTE().fit_resample(X, y)
```

---

### 3. Class Weighting

**Concept**: Assign higher misclassification cost to minority class without changing the dataset.

**How it works**:
- Minority class errors are penalized more heavily during training
- Model learns to pay more attention to minority class
- No data augmentation required

**Pros**:
- No data manipulation
- Computationally efficient
- Preserves original data distribution

**Cons**:
- May not work well with very extreme imbalances
- Requires model support for sample weights

**Implementation**:
```python
from sklearn.linear_model import LogisticRegression

# Calculate weight for minority class
default_weight = 1 / np.mean(y == 'default')
sample_weights = [default_weight if yi == 'default' else 1 for yi in y]

# Train with weights
model = LogisticRegression()
model.fit(X, y, sample_weight=sample_weights)
```

**Automatic class weighting**:
```python
# Many sklearn models support automatic balancing
model = LogisticRegression(class_weight='balanced')
model.fit(X, y)
```

---

### 4. Ensemble Methods

**Concept**: Combine multiple models trained on different balanced subsets.

#### Balanced Random Forest
- Each tree trained on a bootstrap sample with balanced classes
- Combines predictions from all trees

#### EasyEnsemble
- Create multiple balanced subsets via undersampling
- Train separate classifiers on each subset
- Combine predictions

**Pros**:
- Leverages all data (unlike simple undersampling)
- Reduces variance through ensembling
- Often achieves best performance

**Cons**:
- More complex
- Longer training time
- Harder to interpret

---

## Strategy Selection Guide

| Scenario | Recommended Strategy |
|----------|---------------------|
| **Moderate imbalance (1:10)** | Class weighting or SMOTE |
| **Severe imbalance (1:100+)** | Ensemble methods or combination of techniques |
| **Large dataset** | Undersampling + class weighting |
| **Small dataset** | SMOTE or ADASYN |
| **Noisy data** | Class weighting (avoid SMOTE) |
| **Need interpretability** | Class weighting |
| **Maximum performance** | Ensemble methods |

---

## Evaluation Metrics for Imbalanced Data

**Avoid**: Overall accuracy (misleading with imbalanced data)

**Use instead**:
- **Precision**: Of predicted positives, how many are correct?
- **Recall (Sensitivity)**: Of actual positives, how many did we find?
- **F1-Score**: Harmonic mean of precision and recall
- **ROC-AUC**: Area under ROC curve (threshold-independent)
- **PR-AUC**: Area under Precision-Recall curve (better for severe imbalance)

```python
from sklearn.metrics import classification_report, roc_auc_score

# Comprehensive evaluation
print(classification_report(y_true, y_pred))

# ROC-AUC
roc_auc = roc_auc_score(y_true, y_pred_proba)
```

---

## Practical Recommendations

1. **Start with class weighting**: Simple, fast, often effective
2. **Try SMOTE if weighting insufficient**: Especially with small datasets
3. **Use ensemble methods for production**: Best performance, worth the complexity
4. **Always use appropriate metrics**: Accuracy is meaningless
5. **Validate on realistic data**: Test set should reflect real-world distribution
6. **Consider cost-sensitive learning**: If misclassification costs are known

---

## Example Workflow

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report, roc_auc_score

# 1. Split data (stratified to preserve class distribution)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

# 2. Apply SMOTE to training data only
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# 3. Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_resampled, y_train_resampled)

# 4. Evaluate on original test distribution
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred))
print(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.3f}")
```

---

## References

- Chawla et al. (2002). "SMOTE: Synthetic Minority Over-sampling Technique"
- He & Garcia (2009). "Learning from Imbalanced Data"
- Bruce & Bruce (2020). "Practical Statistics for Data Scientists" (Chapter 5)

---

## Key Takeaway

**Never apply resampling to test data**. Only resample the training set. The test set should reflect the real-world class distribution to provide realistic performance estimates.
