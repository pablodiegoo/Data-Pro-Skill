---
name: political-science-metrics
description: "Specialized metrics for political campaigning, including Disapproval Analysis (Pain Curves) and Successor Retention Indices."
---

# Political Science Metrics Skill

This skill provides advanced frameworks for analyzing political survey data, going beyond simple "Vote Intention".

## Scripts

### `disapproval_analysis.py`
Runs an "Inverse Regression" to identify what drives **Rejection** (Disapproval).
Most models predict Approval. This one predicts the *absence* of Approval to find the "Deal Breakers".

**Logic**:
- **Technique**: Logistic Regression with `Target = (Approval == 0)`.
- **Output**:
    - **Rejection Drivers**: Attributes with negative coefficients (meaning their presence prevents rejection).
    - **Pain Curve**: Visualization showing how probability of rejection increases as an attribute score drops.

**Usage**:
```bash
python3 .agent/skills/political-science-metrics/scripts/disapproval_analysis.py
```
*(Note: Ensure your dataset has the standard attributes columns and a binary approval target)*
