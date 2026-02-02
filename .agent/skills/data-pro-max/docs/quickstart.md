# Data Pro Max - Quick Start Guide

## 🚀 Getting Started

### Installation

No installation required! Just use the CLI:

```bash
# From project root
alias datapro='python3 .agent/skills/data-pro-max/scripts/datapro.py'
```

### Basic Workflow

```mermaid
flowchart LR
    A[CSV Data] --> B[datapro analyze]
    B --> C[Analysis Plan]
    C --> D[Manual Analysis]
    D --> E[datapro report]
    E --> F[PDF Report]
```

---

## 📊 Command Reference

### 1. Search Knowledge Base

```bash
# Search all categories
datapro search "correlation"

# Search specific type
datapro search --type analysis "t-test"
datapro search --type visualization "bar"
datapro search --type palette --domain survey
datapro search --type style "executive"
datapro search --type rule "missing"
```

### 2. Analyze Dataset

```bash
# Basic analysis
datapro analyze data.csv

# With domain and goal
datapro analyze survey.csv --domain survey --goal "customer segmentation"

# Output to file
datapro analyze data.csv -o plan.md --json
```

### 3. Generate Reports

```bash
# PDF report with styling
datapro report analysis.md -o report.pdf --title "Q1 Results" --color "2980b9"

# DOCX for editing
datapro report analysis.md --format docx
```

### 4. Full Pipeline

```bash
# Complete workflow in one command
datapro pipeline data.csv -o report.pdf --domain survey --title "Survey Analysis"
```

---

## 🐍 Python Integration

### Using Code Snippets

```python
from pathlib import Path
import csv

# Load snippets
snippets_file = Path(".agent/skills/data-pro-max/data/code_snippets.csv")
with open(snippets_file) as f:
    snippets = {row['id']: row for row in csv.DictReader(f)}

# Get and execute a snippet
snippet = snippets['nps_calc']
exec(snippet['imports'])
exec(snippet['code'])

# Use the function
result = calculate_nps(df, 'recommend_score')
print(f"NPS: {result['nps']}")
```

### Using the Reasoning Engine

```python
import pandas as pd
from reasoning_engine import generate_analysis_plan

df = pd.read_csv("survey.csv")
plan = generate_analysis_plan(df, domain="survey", goal="satisfaction drivers")

print(f"Recommended analyses: {len(plan.recommended_analyses)}")
for a in plan.recommended_analyses[:3]:
    print(f"  - {a['name']}: {a['use_case']}")
```

### Applying Styles

```python
from style_presets import apply_style, list_styles

# List available styles
list_styles()

# Apply a style before plotting
apply_style('executive')

import matplotlib.pyplot as plt
import seaborn as sns

# Now all plots use executive style
sns.barplot(data=df, x='category', y='value')
plt.show()
```

---

## 📁 File Structure

```
data-pro-max/
├── scripts/
│   ├── datapro.py          # Main CLI
│   ├── search.py           # Search engine
│   ├── reasoning_engine.py # Recommendation system
│   └── style_presets.py    # Style management
├── data/
│   ├── analysis_types.csv  # 65+ analyses
│   ├── visualization_rules.csv # 63+ charts
│   ├── visualization_styles.csv # 20 styles
│   ├── palettes.csv        # 42 palettes
│   ├── reasoning_rules.csv # 80+ rules
│   └── code_snippets.csv   # Python snippets
└── docs/
    ├── quickstart.md       # This file
    └── tutorials.md        # Step-by-step guides
```
