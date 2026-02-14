# Harvested Scripts

This directory contains reusable analytical scripts extracted from the Practical Statistics for Data Scientists repository.

## Scripts Inventory

### 1. `correlation_ellipse_plot.py`
**Source**: Chapter 1 - Exploratory Data Analysis  
**Purpose**: Visualize correlation matrices using ellipses (grayscale-friendly alternative to heatmaps)  
**Genericity**: High - Works with any correlation matrix  
**Value**: Unique visualization pattern not in Data-Pro-Skill

**Use Cases**:
- Academic papers requiring grayscale visualizations
- Correlation analysis with directional indicators
- Publications with print constraints

---

### 2. `partial_residual_plot.py`
**Source**: Chapter 4 - Regression and Prediction  
**Purpose**: Create partial residual plots for polynomial/nonlinear regression models  
**Genericity**: High - Works with statsmodels OLS results  
**Value**: Extends statsmodels' built-in partial residual plots to handle polynomial terms

**Use Cases**:
- Diagnosing nonlinearity in regression models
- Visualizing individual predictor contributions
- Model validation and diagnostics

---

### 3. `permutation_test_utilities.py`
**Source**: Chapter 3 - Statistical Experiments  
**Purpose**: Resampling-based hypothesis testing functions  
**Genericity**: High - Generic permutation test framework  
**Value**: Educational implementation of resampling methods

**Use Cases**:
- A/B testing without parametric assumptions
- Small sample hypothesis testing
- Teaching statistical concepts

---

### 4. `data_directory_finder.py`
**Source**: common.py  
**Purpose**: Automatically locate data directory in project hierarchy  
**Genericity**: High - Works for any project structure  
**Value**: Simple utility for flexible data path management

**Use Cases**:
- Projects with varying directory structures
- Notebooks that need to find data regardless of execution location
- Multi-environment development (local, cloud, containers)

---

### 5. `principal_component_plotting.py`
**Source**: Chapter 7 - Unsupervised Learning  
**Purpose**: Utilities for visualizing PCA scree plots and component loadings  
**Genericity**: High - Works with sklearn PCA results  
**Value**: Standardizes the "interpretation visualization" of PCA which is often manual

**Use Cases**:
- Dimensionality reduction interpretation
- Feature importance visualization
- Cumulative variance analysis

---

### 6. `multivariate_normal_contours.py`
**Source**: Chapter 7 - Unsupervised Learning  
**Purpose**: Plot probability contours for bivariate normal distributions  
**Genericity**: High - Accepts mean and cov matrix  
**Value**: Unique utility to map probability volumes (50%, 95%) to density contours

**Use Cases**:
- Visualizing uncertainty in multivariate data
- Confidence region estimation
- Theoretical distribution exploration

---

### 7. `gower_distance_utility.py`
**Source**: Chapter 7 - Unsupervised Learning  
**Purpose**: Implementation of Gower's distance for mixed-type data  
**Genericity**: High - Works on generic DataFrames  
**Value**: Common gap in standard libraries (scipy/sklearn) for mixed categorical/numeric clustering

**Use Cases**:
- Customer segmentation with mixed attributes
- Hierarchical clustering of survey data
- Dissimilarity analysis for varied features

---

### 8. `glm_partial_residual_plot.py`
**Source**: Chapter 5 - Classification  
**Purpose**: Partial residual plots for GLM (logistic regression) with non-linear terms  
**Genericity**: High - Works with statsmodels GLM results  
**Value**: Extends partial residual plotting to GLM models with splines/polynomials

**Use Cases**:
- Diagnosing non-linearity in logistic regression
- Visualizing feature contributions in classification models
- Model validation for GLM with transformations

---

### 9. `permutation_feature_importance.py`
**Source**: Chapter 6 - Statistical Machine Learning  
**Purpose**: Model-agnostic feature importance via permutation  
**Genericity**: High - Works with any sklearn classifier  
**Value**: Alternative to tree-based importance; measures actual predictive power

**Use Cases**:
- Feature importance for non-tree models (logistic, SVM, neural nets)
- Comparing importance across different model types
- Detecting feature interactions
- Unbiased importance for high-cardinality features

---

## Non-Harvested Scripts

The following scripts were evaluated but **not harvested** because they are:
- Too specific to textbook examples
- Already covered by existing Data-Pro-Skill capabilities
- Simple demonstrations rather than reusable utilities

Examples:
- Basic histogram/boxplot wrappers (already in data-viz)
- Simple statistical calculations (mean, median, etc.)
- Dataset-specific analysis scripts

---

## Integration Notes

### Recommended Absorption Path
1. **Immediate**: `data_directory_finder.py` → Add to `data-pro-max` utilities
2. **High Priority**: `correlation_ellipse_plot.py`, `principal_component_plotting.py` → Add to `data-viz` skill
3. **Medium Priority**: `partial_residual_plot.py`, `multivariate_normal_contours.py` → Add to `data-analysis-suite`
4. **Medium Priority**: `gower_distance_utility.py` → Add to `stats-causal-inference` or a new `clustering-skills` folder
5. **Low Priority**: `permutation_test_utilities.py` → Reference implementation for hypothesis testing

### Dependencies
- matplotlib
- seaborn
- pandas
- numpy
- scipy
- statsmodels
- scikit-learn (for PCA)
