# Harvested Scripts from Festival Verão 2026

This directory contains generic, reusable scripts and patterns extracted during the project harvest.

## 1. `eda_notebook_generator.py`
**Why it's valuable**: Completely automates the creation of a comprehensive EDA Jupyter Notebook from any Parquet or CSV dataset. It intelligently handles dynamic schemas, builds Markdown glossaries from external JSON mappings, and auto-selects charts (Pie vs. Bar vs. Histogram) based on the data type and cardinality.
**What to do with it**: Add to the `data-pro-max` or `data-analysis-suite` as a core automated reporting tool.

## 2. `advanced_analytics_generator.py`
**Why it's valuable**: Automates advanced statistical modeling (Random Forest Feature Importance, KMeans vs DBSCAN clustering, PCA/Factor Analysis, and Residual/Halo removal) into a highly readable, client-ready Jupyter Notebook. This is an extremely powerful asset that standardizes complex data science workflows.
**What to do with it**: Combine with `data-analysis-suite` as a master script for rapid insights generation.

## 3. `duckdb_fuzzy_cleaner.py`
**Why it's valuable**: Extracts the specific pattern of using DuckDB's `read_csv_auto` to parse messy CSV headers, combined with a Python fuzzy-matching system (handling trailing spaces etc.) against a canonical dictionary. This handles common SurveyMonkey/Qualtrics export issues beautifully.
**What to do with it**: Integrate into the `data-manipulation` skill as a standard ingestion pattern for messy CSVs.

## 4. `qualitative_categorizer.py`
**Why it's valuable**: A simple, fast, and generic rule-engine for categorizing spontaneous open-ended text answers based on dictionary keyword lookups. Great for rapid qualitative analysis when LLM APIs are not available or too slow.
**What to do with it**: Add to `data-manipulation` or `data-analysis-suite` toolkits for processing qualitative survey columns.
