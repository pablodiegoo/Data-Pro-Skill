# Numpy Statistical Operations

Low-level, high-speed mathematical operations for DataPro's custom metrics.

## 🧮 Vectorized Statistics

Use Numpy directly for custom formulas to avoid the overhead of Pandas Series if performance is an issue for large arrays.

```python
import numpy as np

# Robust Median Absolute Deviation (MAD)
def get_mad(data):
    median = np.median(data)
    mad = np.median(np.abs(data - median))
    return mad / 0.6745  # Consistent scaling for normal distribution
```

## 📉 Linear Algebra & Distances

Essential for clustering and persona profiling.

- **Euclidean Distance**: `np.linalg.norm(a - b)`
- **Standardization**: `(x - x.mean()) / x.std()`

## ⚡ Speed Tips

1.  **Broadcasting**: Leverage Numpy's broadcasting to perform operations on arrays of different shapes.
2.  **UFuncs**: Use universal functions (`np.add`, `np.log`, `np.exp`) instead of explicit loops.
3.  **No Loops**: If you see a `for` loop over numeric data, replace it with a vectorized Numpy operation.
