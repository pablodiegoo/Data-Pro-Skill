"""
Permutation Test Utilities

Resampling-based hypothesis testing functions for non-parametric statistical inference.

Source: Practical Statistics for Data Scientists, Chapter 3
"""

import random
import numpy as np
import pandas as pd
from typing import Callable, Union, List


def permutation_test_two_groups(
    group_a: Union[pd.Series, np.ndarray, List],
    group_b: Union[pd.Series, np.ndarray, List],
    statistic: Callable = None,
    n_permutations: int = 1000,
    alternative: str = 'two-sided',
    random_seed: int = None
) -> dict:
    """
    Perform a permutation test to compare two groups.
    
    Parameters
    ----------
    group_a : array-like
        Data from first group
    group_b : array-like
        Data from second group
    statistic : callable, optional
        Function to compute test statistic. Default is difference in means.
        Should accept two arrays and return a scalar.
    n_permutations : int, default=1000
        Number of permutations to perform
    alternative : {'two-sided', 'greater', 'less'}, default='two-sided'
        Alternative hypothesis
    random_seed : int, optional
        Random seed for reproducibility
    
    Returns
    -------
    dict with keys:
        - 'observed_statistic': The observed test statistic
        - 'p_value': The permutation p-value
        - 'permutation_distribution': Array of permuted statistics
        - 'n_permutations': Number of permutations performed
        
    Examples
    --------
    >>> group_a = [1, 2, 3, 4, 5]
    >>> group_b = [6, 7, 8, 9, 10]
    >>> result = permutation_test_two_groups(group_a, group_b)
    >>> print(f"P-value: {result['p_value']:.4f}")
    
    Notes
    -----
    - Does not assume normality or equal variances
    - Exact p-values for small samples
    - Computationally intensive for large datasets
    """
    if random_seed is not None:
        random.seed(random_seed)
        np.random.seed(random_seed)
    
    # Convert to numpy arrays
    group_a = np.asarray(group_a)
    group_b = np.asarray(group_b)
    
    # Default statistic: difference in means
    if statistic is None:
        statistic = lambda a, b: np.mean(b) - np.mean(a)
    
    # Calculate observed statistic
    observed_stat = statistic(group_a, group_b)
    
    # Combine groups
    combined = np.concatenate([group_a, group_b])
    n_a = len(group_a)
    n_b = len(group_b)
    n_total = n_a + n_b
    
    # Perform permutations
    perm_stats = []
    for _ in range(n_permutations):
        # Randomly shuffle and split
        indices = np.random.permutation(n_total)
        perm_a = combined[indices[:n_a]]
        perm_b = combined[indices[n_a:]]
        perm_stats.append(statistic(perm_a, perm_b))
    
    perm_stats = np.array(perm_stats)
    
    # Calculate p-value based on alternative hypothesis
    if alternative == 'two-sided':
        p_value = np.mean(np.abs(perm_stats) >= np.abs(observed_stat))
    elif alternative == 'greater':
        p_value = np.mean(perm_stats >= observed_stat)
    elif alternative == 'less':
        p_value = np.mean(perm_stats <= observed_stat)
    else:
        raise ValueError("alternative must be 'two-sided', 'greater', or 'less'")
    
    return {
        'observed_statistic': observed_stat,
        'p_value': p_value,
        'permutation_distribution': perm_stats,
        'n_permutations': n_permutations
    }


def permutation_test_anova(
    data: pd.DataFrame,
    value_col: str,
    group_col: str,
    n_permutations: int = 1000,
    random_seed: int = None
) -> dict:
    """
    Perform a permutation-based ANOVA test.
    
    Tests whether group means differ significantly using variance of group means
    as the test statistic.
    
    Parameters
    ----------
    data : pandas.DataFrame
        Data containing values and group labels
    value_col : str
        Name of column containing values
    group_col : str
        Name of column containing group labels
    n_permutations : int, default=1000
        Number of permutations to perform
    random_seed : int, optional
        Random seed for reproducibility
    
    Returns
    -------
    dict with keys:
        - 'observed_variance': Observed variance of group means
        - 'p_value': The permutation p-value
        - 'permutation_distribution': Array of permuted variances
        - 'group_means': Dictionary of observed group means
        
    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'value': [1, 2, 3, 10, 11, 12, 20, 21, 22],
    ...     'group': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C']
    ... })
    >>> result = permutation_test_anova(df, 'value', 'group')
    >>> print(f"P-value: {result['p_value']:.4f}")
    """
    if random_seed is not None:
        random.seed(random_seed)
        np.random.seed(random_seed)
    
    # Calculate observed variance of group means
    group_means = data.groupby(group_col)[value_col].mean()
    observed_variance = group_means.var()
    
    # Perform permutations
    perm_variances = []
    for _ in range(n_permutations):
        # Shuffle values
        permuted_data = data.copy()
        permuted_data[value_col] = np.random.permutation(data[value_col].values)
        
        # Calculate variance of permuted group means
        perm_group_means = permuted_data.groupby(group_col)[value_col].mean()
        perm_variances.append(perm_group_means.var())
    
    perm_variances = np.array(perm_variances)
    
    # Calculate p-value
    p_value = np.mean(perm_variances >= observed_variance)
    
    return {
        'observed_variance': observed_variance,
        'p_value': p_value,
        'permutation_distribution': perm_variances,
        'group_means': group_means.to_dict()
    }


if __name__ == "__main__":
    # Example 1: Two-group comparison
    print("Example 1: Two-group permutation test")
    print("=" * 50)
    
    group_a = [175, 180, 165, 170, 172]
    group_b = [185, 190, 182, 188, 195]
    
    result = permutation_test_two_groups(
        group_a, group_b,
        n_permutations=10000,
        alternative='two-sided',
        random_seed=42
    )
    
    print(f"Observed difference in means: {result['observed_statistic']:.2f}")
    print(f"P-value: {result['p_value']:.4f}")
    print()
    
    # Example 2: ANOVA-style test
    print("Example 2: Permutation ANOVA")
    print("=" * 50)
    
    df = pd.DataFrame({
        'time': [120, 125, 130, 150, 155, 160, 180, 185, 190, 200, 205, 210],
        'page': ['A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C']
    })
    
    result = permutation_test_anova(
        df, 'time', 'page',
        n_permutations=10000,
        random_seed=42
    )
    
    print(f"Observed variance of group means: {result['observed_variance']:.2f}")
    print(f"Group means: {result['group_means']}")
    print(f"P-value: {result['p_value']:.4f}")
