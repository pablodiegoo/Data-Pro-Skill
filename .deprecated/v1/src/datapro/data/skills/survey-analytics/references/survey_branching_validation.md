# Validating Survey Branching via Co-Occurrence Matrices

## The Pattern
During EDA or cross-tabulation of survey data, analysts often attempt to build heatmaps or correlation matrices between two separate multiple-choice questions (e.g., "What product do you sell?" vs "What training do you need?").

In OS18, attempting to build a co-occurrence heatmap between these two questions resulted in a `ValueError: zero-size array to reduction operation fmin` from Seaborn. 

## The Root Cause
The error was caused because the resulting intersection dataframe was `0x0`. In the Qualtrics survey logic, respondents who answered Question A physically could not (or were not prompted to) answer Question B due to branching, display logic, or skip logic. The mathematical intersection of respondents between the two questions was precisely 0.

## Methodological Best Practice
Before plotting any co-occurrence matrix (`pd.crosstab` or manual intersection counting) on survey data, **always validate the sample overlap**.

1. Compute the overlap size.
2. Filter out zero-sum rows and columns:
   ```python
   co_occurrence = co_occurrence.loc[(co_occurrence.sum(axis=1) > 0), (co_occurrence.sum(axis=0) > 0)]
   ```
3. **CRITICAL CHECK:** Immediately check `co_occurrence.shape`.
   ```python
   if co_occurrence.shape[0] == 0 or co_occurrence.shape[1] == 0:
       print("WARNING: Zero sample overlap between these questions. This indicates mutually exclusive survey branching logic.")
       # Halt plotting
   ```

## Business Value
Instead of spending hours debugging plotting library errors (`seaborn`, `matplotlib`), this pattern instantly identifies structural flaws or intended skip logic in the questionnaire design, allowing the analyst to pivot the research question.
