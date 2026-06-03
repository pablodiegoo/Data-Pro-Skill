import pandas as pd
import json
import os
import sys

# Default Mapping Path
COLUMN_MAPPING_PATH = ".agent/references/column_mapping.json"

def create_notebook(df_path, output_path="eda_report.ipynb"):
    print(f"Analyzing {df_path}...")
    
    # Load data
    if df_path.endswith('.parquet'):
        df = pd.read_parquet(df_path)
    else:
        df = pd.read_csv(df_path)
        
    # Metadata columns to exclude from individual plots
    metadata_terms = ['id', 'time', 'lat', 'lon', 'researcher', 'consent', 'ref', 'pii']
    
    # Load Column Mapping
    mapping = {}
    if os.path.exists(COLUMN_MAPPING_PATH):
        with open(COLUMN_MAPPING_PATH, "r", encoding="utf-8") as f:
            mapping = json.load(f)
            
    cells = []
    
    # Title and Intro
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            f"# Automated EDA Report: {os.path.basename(df_path)}\n",
            "This notebook was automatically generated to provide a comprehensive view of the dataset."
        ]
    })
    
    # Setup Cell
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import pandas as pd\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "import numpy as np\n",
            "%matplotlib inline\n",
            "sns.set_theme(style=\"whitegrid\")\n",
            "\n",
            f"df = pd.read_parquet('{os.path.abspath(df_path)}') if '{df_path}'.endswith('.parquet') else pd.read_csv('{os.path.abspath(df_path)}')\n",
            "print(f'Dataset loaded: {len(df)} records, {len(df.columns)} columns')"
        ]
    })
    
    # Glossary / Schema
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## 1. Glossary & Data Schema\n", "List of all columns detected in the dataset:"]
    })
    
    # Build schema table with descriptions
    schema_rows = [["Column", "Type", "Original Question/Label"]]
    for col in df.columns:
        orig = mapping.get(col, "-")
        schema_rows.append([f"`{col}`", str(df[col].dtype), orig])
        
    # Helper for markdown tables
    header = "| " + " | ".join(schema_rows[0]) + " |"
    separator = "| " + " | ".join(["---"] * 3) + " |"
    body = "\n".join(["| " + " | ".join(row) + " |" for row in schema_rows[1:]])
    
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [f"{header}\n{separator}\n{body}\n"]
    })
    
    # Analysis Loop
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## 2. Individual Variable Analysis\n"]
    })
    
    for col in df.columns:
        # Skip metadata
        if any(term in col.lower() for term in metadata_terms):
            continue
            
        # Title Logic: "Question (Variable Name)"
        question_label = mapping.get(col, col)
        # Check if the mapping is already snake_case/same as col
        if question_label == col:
            title_text = f"### Variable: `{col}`"
        else:
            title_text = f"### {question_label} (`{col}`)"

        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [f"{title_text}\n"]
        })
        
        # Logic for choosing plots
        code_block = []
        
        # Categorical (Object or Categorical)
        if df[col].dtype == 'object' or df[col].dtype.name == 'category':
            cardinality = df[col].nunique()
            
            if cardinality <= 10:
                # Pie Chart
                code_block = [
                    f"col = '{col}'\n",
                    "counts = df[col].value_counts(normalize=True) * 100\n",
                    "plt.figure(figsize=(6, 6))\n",
                    "counts.plot.pie(autopct='%1.1f%%', cmap='viridis')\n",
                    "plt.title(f'Distribution: {col}')\n",
                    "plt.ylabel('')\n",
                    "plt.show()\n",
                    "display(counts.to_frame('Percentage (%)'))"
                ]
            else:
                # Bar Chart
                code_block = [
                    f"col = '{col}'\n",
                    "counts = df[col].value_counts().head(15)\n",
                    "plt.figure(figsize=(10, 6))\n",
                    "sns.barplot(x=counts.values, y=counts.index, palette='magma')\n",
                    "plt.title(f'Top 15: {col}')\n",
                    "plt.show()\n",
                    "display(df[col].value_counts(normalize=True).head(10).to_frame('Percentage (%)'))"
                ]
                
        # Numeric / Scales
        elif pd.api.types.is_numeric_dtype(df[col]):
            code_block = [
                f"col = '{col}'\n",
                "fig, axes = plt.subplots(1, 2, figsize=(12, 5))\n",
                "sns.histplot(df[col].dropna(), kde=True, ax=axes[0], color='skyblue')\n",
                "axes[0].set_title(f'Histogram: {col}')\n",
                "sns.boxplot(x=df[col].dropna(), ax=axes[1], color='lightgreen')\n",
                "axes[1].set_title(f'Boxplot: {col}')\n",
                "plt.show()\n",
                f"display(df[col].describe().to_frame())"
            ]
            
        if code_block:
            cells.append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": code_block
            })
            
    # Heatmap of correlation (Only for scales/numeric)
    numeric_cols = df.select_dtypes(include=['number']).columns
    numeric_cols = [c for c in numeric_cols if not any(t in c.lower() for t in metadata_terms)]
    
    if len(numeric_cols) > 1:
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Aggregate Analysis (Linear Correlation)\n",
                "**Pearson Correlation**: This heatmap identifies linear relationships between numerical variables. \n",
                "It is valid for continuous data and helps identify which variables move together in a straight-line fashion."
            ]
        })
        
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                f"numeric_cols = {list(numeric_cols)}\n",
                "corr = df[numeric_cols].corr(method='pearson')\n",
                "plt.figure(figsize=(12, 10))\n",
                "sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0)\n",
                "plt.title('Quick Glance: Pearson Correlation')\n",
                "plt.show()"
            ]
        })

    # Saving the notebook
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    
    # Ensure output directory exists before saving
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1)
        
    print(f"Notebook generated successfully: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 eda_notebook_generator.py <path_to_data> [output.ipynb]")
    else:
        path = sys.argv[1]
        out = sys.argv[2] if len(sys.argv) > 2 else "automated_eda.ipynb"
        create_notebook(path, out)
