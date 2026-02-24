# Numbered Reproducible Script Architecture

## The Pattern
Project execution should be managed through strict numerically ordered Python scripts in the `scripts/` directory:
1. `01_prep_data.py` (Data cleaning and Parquet export)
2. `02_create_notebook.py` (Generating exploratory/statistical notebooks)
3. `03_eda_report.py` (Generating Markdown EDA reports)
4. `04_churn_report.py` (Generating Markdown hypothesis reports)
5. `05_relevancia_notebook.py` (Generates client-facing math explanation notebooks)

## Architectural Best Practice
This represents a superior form of project architecture compared to ad-hoc notebook creation. 
By wrapping analytical steps (even notebook generation itself via `nbformat` and `nbconvert`) into purely reproducible Python scripts:
- The entire analysis protocol becomes self-documenting.
- The pipeline can be re-run instantly if the raw data (`database/raw/`) is updated.
- It prevents the "hidden state" problem common in Jupyter Notebook data-science workflows.

## Workflow Recommendation
For all future data analysis projects, the core analytical pipeline should be abstracted out of notebooks and into a numbered `scripts/XX_description.py` format. Notebooks should strictly be the *output* of these scripts or used solely for sandbox visualization, not the source of truth for data transformations.
