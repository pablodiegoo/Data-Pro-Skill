# Harvest Action Plan: Practical Statistics

Following the harvest of the "Practical Statistics for Data Scientists" repository, this plan outlines the recommended promotion path for each item into the upstream `Data-Pro-Skill` ecosystem.

## 1. Skill Promotion (Python Scripts)

| Script | Target Skill | Priority | Note |
| :--- | :--- | :--- | :--- |
| `data_directory_finder.py` | `data-pro-max` (utilities) | **P0 (Immediate)** | Standardizes pathing across all projects. |
| `correlation_ellipse_plot.py` | `data-viz` | **P1 (High)** | Improves grayscale/print analysis. |
| `principal_component_plotting.py` | `data-viz` | **P1 (High)** | Adds interpretability to PCA tasks. |
| `permutation_test_utilities.py` | `stats-causal-inference` | **P2 (Medium)** | Core for non-parametric testing. |
| `partial_residual_plot.py` | `stats-causal-inference` | **P2 (Medium)** | Essential for non-linear regression audit. |
| `gower_distance_utility.py` | *new* `clustering-skills` | **P2 (Medium)** | Handle mixed categorical/numeric data. |
| `multivariate_normal_contours.py`| `data-viz` | **P3 (Low)** | Specific for GMMs and LDA visibility. |

## 2. Methodology Absorption (References)

| Document | Target Location | Goal |
| :--- | :--- | :--- |
| `analytical_methodology_patterns.md` | `stats-causal-inference/references/` | Institutionalize Gower, PCA and MAD theory. |
| `educational_visualization_patterns.md` | `data-viz/references/` | Guidelines for making visuals pedagogically clear. |
| `evaluation_and_diagnostics.md` | `stats-causal-inference/references/` | Formalize residual-based ML auditing. |

## 3. Database Updates (`datapro` CLI)

- **Snippets**: Import all items from `assets/harvest/database/all_snippets.json` into the central `datapro` library.
- **Analysis Types**: Register "Robust EDA" and "Permutation Testing" as official analysis types.
- **Reasoning Rules**: Implement rules from `new_rules.csv` to trigger "Robust Scale Suggestion" (MAD) when high outliers are detected.

## 4. Governance & Workflow

- Adopt the **Language-Parallel Verification** pattern from `dual_language_repository_pattern.md` for any new educational components created in the future.
- Use `educational_code_standards.md` when documenting code for stakeholders to ensure clarity over performance-first orientation.
