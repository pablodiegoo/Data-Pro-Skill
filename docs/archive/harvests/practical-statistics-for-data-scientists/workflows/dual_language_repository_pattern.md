# Dual-Language Repository Organization Pattern

## Context

The "Practical Statistics for Data Scientists" repository maintains parallel implementations in **Python** and **R** for the same statistical concepts. This pattern is valuable for educational repositories that need to support multiple programming languages.

## Pattern: Language-Parallel Structure

### Directory Organization
```
project/
├── python/
│   ├── code/           # Standalone .py scripts
│   ├── notebooks/      # Jupyter notebooks
│   └── __init__.py
├── R/
│   ├── code/           # Standalone .R scripts
│   └── notebooks/      # R Markdown files
├── data/               # Shared data (language-agnostic)
├── docs/               # Shared documentation
└── README.md           # Language-agnostic overview
```

### Benefits
1. **Clear separation**: No confusion about which language a file uses
2. **Shared data**: Single source of truth for datasets
3. **Parallel learning**: Readers can compare implementations
4. **Independent execution**: Each language folder is self-contained

### Challenges
1. **Duplication**: Same concepts implemented twice
2. **Sync burden**: Changes must be made in both languages
3. **Testing complexity**: Need to test both implementations

---

## Pattern: Chapter-Based File Naming

### Convention
```
Chapter N - Topic Name.{py,R,ipynb}
```

### Examples
- `Chapter 1 - Exploratory Data Analysis.py`
- `Chapter 2 - Data and sampling distributions.R`
- `Chapter 3 - Statistical Experiments and Significance Testing.ipynb`

### Benefits
1. **Discoverability**: Easy to find content by chapter
2. **Ordering**: Natural alphabetical sort matches book order
3. **Clarity**: Topic is immediately apparent

### Drawbacks
- **Long names**: Can be unwieldy in terminals
- **Renaming**: Chapter reordering requires file renames

---

## Pattern: Common Utilities Module

### Structure
```python
# common.py
def dataDirectory(dataDirectoryName='data'):
    """Find data directory from any execution location"""
    dataDir = Path(__file__).resolve().parent
    while not list(dataDir.rglob('data')):
        dataDir = dataDir.parent
    found = [d for d in dataDir.rglob('data') if d.is_dir()]
    if not found:
        raise Exception(f'Cannot find data directory')
    return found[0]
```

### Usage in Scripts
```python
try:
    import common
    DATA = common.dataDirectory()
except ImportError:
    DATA = Path().resolve() / 'data'
```

### Benefits
1. **Flexible execution**: Works from any directory
2. **Graceful fallback**: Handles missing common module
3. **DRY**: Single implementation of path logic

---

## Pattern: Inline Documentation Style

### Convention
```python
## Section Title
### Subsection Title

# Explanation of what follows
code_here()

# Table X-Y (reference to book)
print(results)
```

### Benefits
1. **Self-documenting**: Code explains itself
2. **Book alignment**: Easy to match code to text
3. **Standalone**: Can be read without the book

### Example
```python
## Estimates of Location
### Example: Location Estimates of Population and Murder Rates

# Table 1-2
state = pd.read_csv(STATE_CSV)
print(state.head(8))

# Compute the mean, trimmed mean, and median for Population
print(state['Population'].mean())
print(trim_mean(state['Population'], 0.1))
print(state['Population'].median())
```

---

## Pattern: Progressive Visualization Complexity

### Approach
1. **Basic plot**: Minimal code, default settings
2. **Styled plot**: Add labels, titles, formatting
3. **Publication-ready**: Full annotations, custom aesthetics

### Example
```python
# Basic
df.plot.hist()

# Styled
ax = df.plot.hist(bins=20, figsize=(6, 4))
ax.set_xlabel('Value')
ax.set_ylabel('Frequency')

# Publication-ready
fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(df['value'], bins=20, edgecolor='black', alpha=0.7)
ax.set_xlabel('Value (units)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Distribution of Values', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

## Pattern: Data File Organization

### Structure
```
data/
├── state.csv              # Small, frequently used
├── house_sales.csv        # Medium size
├── sp500_data.csv.gz      # Large, compressed
└── README.md              # Data dictionary
```

### Naming Convention
- Lowercase with underscores
- Descriptive names (not `data1.csv`)
- Compress large files (`.gz`)

### Benefits
1. **Predictable**: Easy to guess file names
2. **Efficient**: Compression saves space
3. **Documented**: README explains each file

---

## Pattern: Notebook vs. Script Duality

### Maintain Both
- **Notebooks** (`.ipynb`): Interactive exploration, teaching
- **Scripts** (`.py`): Automated execution, testing

### Conversion
```bash
# Notebook → Script
jupyter nbconvert --to script notebook.ipynb

# Script → Notebook (manual)
# Copy code into cells with markdown headers
```

### Benefits
1. **Flexibility**: Choose format for task
2. **Testing**: Scripts can be run in CI/CD
3. **Teaching**: Notebooks show output inline

---

## Anti-Patterns Observed

### ❌ Hardcoded Paths
```python
# BAD
data = pd.read_csv('/Users/author/Desktop/project/data/file.csv')
```

**Solution**: Use relative paths or path discovery
```python
# GOOD
DATA = Path(__file__).parent.parent / 'data'
data = pd.read_csv(DATA / 'file.csv')
```

### ❌ Unnamed Plots
```python
# BAD
plt.plot(x, y)
plt.show()
```

**Solution**: Always label axes
```python
# GOOD
plt.plot(x, y)
plt.xlabel('Time (seconds)')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Over Time')
plt.show()
```

### ❌ Magic Numbers
```python
# BAD
trimmed = trim_mean(data, 0.1)
```

**Solution**: Name and explain constants
```python
# GOOD
TRIM_PROPORTION = 0.1  # Remove 10% from each tail
trimmed = trim_mean(data, proportiontocut=TRIM_PROPORTION)
```

---

## Recommendations for Data-Pro-Skill

### Adopt
1. **Common utilities pattern**: Path discovery utility
2. **Progressive visualization**: Build from simple to complex
3. **Inline documentation**: Self-documenting code style

### Adapt
1. **Language separation**: Not needed (Python-only)
2. **Chapter naming**: Use task-based names instead
3. **Notebook duality**: Already doing this

### Avoid
1. **Hardcoded paths**: Already avoided
2. **Unnamed plots**: Already enforced
3. **Magic numbers**: Already using constants

---

## Implementation Priority

### High
- Add `find_data_directory()` to `data-pro-max` utilities
- Document progressive visualization pattern in `data-viz`

### Medium
- Create educational code standards guide
- Add inline documentation examples to templates

### Low
- Notebook/script conversion workflow
- Multi-language support (if ever needed)
