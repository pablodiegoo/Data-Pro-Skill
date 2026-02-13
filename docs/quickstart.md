# Data Pro Max — Quick Start Guide

## 🚀 Getting Started

### Installation

```bash
pip install -e .

# Full suite (OCR, advanced stats, PDF export)
pip install "datapro[full,docs]"
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

### 3. Code Snippets

```bash
# List all snippets
datapro snippet --list

# Get a specific snippet by ID
datapro snippet nps_calc
```

### 4. Document Conversion

```bash
# Convert PDF/DOCX to Markdown
datapro convert report.pdf

# Generate PDF report from Markdown
datapro report analysis.md -o report.pdf --title "Q1 Results" --color "2980b9"

# DOCX for editing
datapro report analysis.md --format docx
```

### 5. Project Setup

```bash
# Initialize a new analysis project
datapro setup
```
Creates the full directory structure per [structure.json](../src/datapro/data/structure.json) and installs agent skills.

---

## 🐍 Python Integration

### Using the Library Directly

```python
from datapro import search_knowledge_base, generate_analysis_plan

# Search for analytical techniques
results = search_knowledge_base("regression", search_type="analysis")
for r in results:
    print(f"  {r['name']}: {r['use_case']}")

# Auto-analyze a dataset
import pandas as pd
df = pd.read_csv("survey.csv")
plan = generate_analysis_plan(df, domain="survey", goal="satisfaction drivers")
```

---

## 📁 Project Structure

After running `datapro setup`, your project will have:

```
your-project/
├── scripts/            # Analysis scripts (01_prep, 02_analysis, 03_viz)
├── database/           # Data files (raw/, processed/, final/)
├── docs/               # Studies, reports, plans
├── assets/             # Images, docs, context, harvest
├── .agent/             # Agent Brain (skills, rules, workflows)
└── .gitignore          # Pre-configured for data governance
```
