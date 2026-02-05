---
name: marketing-science-metrics
description: "Advanced marketing science techniques to remove survey bias (Halo Effect, Response Style) and reveal true attribute importance."
---

# Marketing Science Metrics Skill

This skill provides "De-Biasing" techniques for attribute analysis in surveys.

## Scripts

### `ipsative_analysis.py`
Performs **Ipsative Standardization** (centering around respondent mean) and **Residual Analysis** (removing Halo effect).

**Techniques**:
1.  **Ipsative Analysis**:
    - Problem: Some people give all 10s, others all 5s. This allows "Response Style Bias" to skew correlations.
    - Solution: `Variable_New = Variable_Raw - Respondent_Mean`.
    - Result: Reveals *relative* priorities (what is important *to that person* compared to *their other ratings*).

2.  **Residual Analysis (Halo Removal)**:
    - Problem: If a brand is popular, people rate all attributes high ("Halo Effect").
    - Solution: Regress `Attribute ~ Overall_Image`. The *Residuals* are the "Pure Attribute Performance".

**Usage**:
```bash
python3 .agent/skills/marketing-science-metrics/scripts/ipsative_analysis.py
```
