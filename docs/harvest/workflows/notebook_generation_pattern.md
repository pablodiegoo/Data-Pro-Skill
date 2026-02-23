# Proposed Workflow Improvement: Dual-Layered Notebook Generation

**Description:** Standardize the reporting architecture for survey-based projects using automated Jupyter Notebook generation.

**The Pattern:**
Instead of writing hundreds of lines of plotting code in a single Python script or manually creating notebooks, adopt a **Generator Pattern**:

1. **Scripts to generate Notebooks, not Images**: Data-Pro should write highly generic Python scripts (`utils/*.py`) whose sole purpose is to output `.ipynb` files containing both the Python code and the execution results.
2. **Dual Layering**:
   - **Layer 1 (EDA Generator)**: Focuses purely on descriptive statistics. It loops through every column, identifies its type (Categorical vs Numeric), and automatically generates the correct distribution plot (Pie vs Bar vs Histogram) and a descriptive table.
   - **Layer 2 (Advanced Generator)**: Focuses strictly on multivariate strategy (Clustering, Random Forest Drivers, PCA, Halo Removal).

**Workflow Integration:**
When a user asks to "analyze this new survey dataset", Data-Pro should NOT try to write a custom EDA script from scratch. It should:
1. Ensure the data is clean and mapped.
2. Execute the existing `eda_notebook_generator.py` and `advanced_analytics_generator.py`.
3. Read the generated notebooks (or images) to write the final Markdown report.

**Why:** It reduces AI context windows (no need to write 300 lines of boilerplate plotting code for every new project), acts as an immediate deliverable for technical clients, and ensures zero human error in basic data visualization.
