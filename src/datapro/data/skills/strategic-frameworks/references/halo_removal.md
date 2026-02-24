# Methodology: Halo Effect Removal

The Halo Effect occurs in survey research when a respondent's overall impression of a subject influences their ratings on specific attributes.

## Theoretical Basis
By calculating the **Personal Mean** (the average of all attribute scores per respondent) and subtracting it from each individual score, we isolate the **relative performance** of each attribute.

## Approaches
1.  **Simple Residual**: $Score_{i,j} - \bar{Score}_i$. Fast and intuitive.
2.  **Regression Residual**: Regressing each attribute against the personal mean. More robust as it accounts for the strength of the halo on each specific attribute.

## Interpretation
- **Positive Residual**: The attribute performed **above** the respondent's average expectation.
- **Negative Residual**: The attribute performed **below** the respondent's average expectation.

## Implementation
See `scripts/halo_removal.py` for the regression-based implementation.
