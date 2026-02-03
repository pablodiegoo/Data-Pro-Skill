# Data Pro Skill

**An AI skill for data analysis intelligence** — the equivalent of [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) for data science.

## 📦 Installation

Since this is now a standard Python package, you can install it using pip:

```bash
# Clone the repository
git clone https://github.com/pablodiegoo/Data-Pro-Skill
cd Data-Pro-Skill

# Install in development mode
pip install -e .
```

### 🌍 Install on another computer (Remote)
If you just want to use the tool on a different machine without cloning the full repository, you can install it directly from GitHub:

```bash
pip install git+https://github.com/pablodiegoo/Data-Pro-Skill
```

For the **full features** (OCR, Factor Analysis, PPTX conversion):
```bash
pip install "datapro[full,docs] @ git+https://github.com/pablodiegoo/Data-Pro-Skill"
```

> [!IMPORTANT]
> To use the **Advanced PDF Engine**, you still need to install the system dependencies:
> `sudo apt install pandoc texlive-xetex texlive-fonts-extra`

## 🚀 CLI Usage

After installation, the `datapro` command will be available in your terminal.

### 🔍 Search Knowledge Base
Find recommendations for statistics, visualizations, and color palettes.
```bash
# General search
datapro search "correlation"

# Filter by type
datapro search --type visualization "bar chart"
datapro search --type palette --domain survey

# Filter by domain and category
datapro search --domain survey --category inferential
```

### � Get Code Snippets
Copy-paste ready-to-use Python code for common data tasks.
```bash
# List all available snippets
datapro snippet --list

# Get a specific snippet by ID
datapro snippet --id nps_calc

# Search snippets by keyword
datapro snippet --query "test"
```

### 📊 Analyze Data
Automatically profile a dataset and generate an analysis plan.
```bash
datapro analyze your_data.csv --domain survey --goal "identify drivers of satisfaction"
```

### 🧹 Data Transformation
Follow the **Tidy Data** principle to optimize visual reporting.
```bash
# Get code for converting Wide to Long (Melting)
datapro snippet --id melt_data
```
> [!TIP]
> **Strategy:** Keep your base in **Wide** format for statistical tests (FA, PCA, Correlations) and transform to **Long** (Melted) specifically for high-impact visualizations and grouped reports.

### �📄 Convert Documents

Ingest external data reports from PDF, Word, or PowerPoint.
```bash
# Convert PDF to Markdown (auto-detects digital vs scan)
datapro convert source_data.pdf

# Force OCR for scanned images
datapro convert scanned_report.pdf --ocr

# Convert all DOCX/PPTX in a directory
datapro convert ./raw_docs/ -o ./processed_md/
```

### 📑 Generate Reports
Export your analysis findings as professional, styled documents using the **Advanced PDF Engine**.

```bash
# Basic professional PDF
datapro report findings.md --title "Survey Results" --subtitle "Q1 2026"

# Advanced design: Theme, Columns and Watermark
datapro report summary.md --theme dark --columns 2 --watermark "INTERNAL USE"

# Branding: Custom logo and colors
datapro report findings.md --logo ./logo.png --color "27ae60"

# Layout: Landscape and custom margins
datapro report data_dense.md --landscape --margins 1.5cm

# Formats: Generate DOCX for manual edits
datapro report findings.md --format docx
```

**Supported Themes:** `executive` (default), `minimalist`, `academic`, `dark`.
**MermaidJS:** Diagram blocks are automatically rendered in PDF if `mmdc` is installed.

### 🛠️ Setup in New Project
Initialize a new project with DataPro analysis power and AI intelligence.
```bash
# Integrates CLI and copies Agent Skills to the CURRENT directory
datapro setup

# Setup in a SPECIFIC directory
datapro setup /path/to/your/new-project
```


## 📚 Library Usage

You can also use `datapro` as a Python library in your scripts or Jupyter notebooks.

```python
from datapro import search_knowledge_base, generate_analysis_plan, get_styles
import pandas as pd

# 1. Search recommendations
recommendations = search_knowledge_base("timeseries", search_type="analysis")

# 2. Analyze a dataframe
df = pd.read_csv("data.csv")
plan = generate_analysis_plan(df, domain="survey")
print(plan.checklist)

# 3. Apply professional styles for plots
styles = get_styles()
styles.apply_matplotlib("presentation")
```

## 🏗️ Project Structure

- `src/datapro/`: Main package source code.
- `src/datapro/data/`: Knowledge base CSVs and JSON snippets.
- `src/datapro/scripts/`: Individual tools and logic.
- `.agent/skills/`: Original skill definitions and metadata for Agent integration.

## ⚖️ License

MIT
