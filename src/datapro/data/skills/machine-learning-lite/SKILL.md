---
name: machine-learning-lite
description: "Tactical and highly interpretable Machine Learning. Use for: (1) Extracting Feature Importance via Random Forest, (2) Running Permutation Tests, (3) Handling Imbalanced Data (SMOTE)."
---

# Machine Learning Lite

This skill restricts the agent to using simple, highly interpretable Machine Learning methods focused on inference rather than production deployment. Deep learning or black-box predictions are strictly out of scope.

## Core Capabilities

### 1. Interpretability & Testing
- **`permutation_feature_importance.py`**: Calculates the true model importance of variables by randomly shuffling them.
- **`permutation_test_utilities.py`**: Rigorous statistical testing without assuming underlying data distributions.

## Guidelines
- Always prefer Random Forest or Logistic Regression for feature extractability.
- If classes are highly skewed, refer to `references/imbalanced_data_strategies.md`.
