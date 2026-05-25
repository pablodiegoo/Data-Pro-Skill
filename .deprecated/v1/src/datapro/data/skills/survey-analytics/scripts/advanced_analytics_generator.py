import pandas as pd
import json
import os
import sys
import numpy as np

# Default Mapping Path
COLUMN_MAPPING_PATH = ".agent/references/column_mapping.json"

def create_advanced_notebook(df_path, target_col=None, output_path="advanced_analytics.ipynb"):
    print(f"Generating Advanced Analytics for {df_path}...")
    
    # Load data
    if df_path.endswith('.parquet'):
        df = pd.read_parquet(df_path)
    else:
        df = pd.read_csv(df_path)
        
    # Metadata columns
    metadata_terms = ['id', 'time', 'lat', 'lon', 'researcher', 'consent', 'ref', 'pii']
    
    # Load Mapping
    mapping = {}
    if os.path.exists(COLUMN_MAPPING_PATH):
        with open(COLUMN_MAPPING_PATH, "r", encoding="utf-8") as f:
            mapping = json.load(f)
            
    cells = []
    
    # Title
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            f"# Advanced Analytics Report: {os.path.basename(df_path)}\n",
            "This notebook focuses on multivariate relationships, predictive importance, and audience segmentation."
        ]
    })
    
    # Setup
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
            "from sklearn.ensemble import RandomForestRegressor\n",
            "from sklearn.cluster import KMeans, DBSCAN\n",
            "from sklearn.preprocessing import StandardScaler\n",
            "from sklearn.decomposition import PCA, FactorAnalysis\n",
            "from sklearn.metrics import silhouette_score\n",
            "%matplotlib inline\n",
            "sns.set_theme(style=\"whitegrid\")\n",
            "\n",
            f"df = pd.read_parquet('{os.path.abspath(df_path)}') if '{df_path}'.endswith('.parquet') else pd.read_csv('{os.path.abspath(df_path)}')\n",
            f"target_col = '{target_col}'\n",
            "pd.options.display.float_format = '{:.5f}'.format\n",
            "numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()\n",
            "metadata = " + str(metadata_terms) + "\n",
            "analysis_cols = [c for c in numeric_cols if not any(m in c.lower() for m in metadata)]\n",
            "print(f'Ready for analysis with {len(analysis_cols)} numeric attributes.')"
        ]
    })
    
    # Glossary / Schema
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## 1. Glossary & Data Schema\n", "List of all columns detected and their survey question mappings:"]
    })
    
    # Build schema table with descriptions
    schema_rows = [["Column", "Type", "Original Question/Label"]]
    for col in df.columns:
        orig = mapping.get(col, "-")
        schema_rows.append([f"`{col}`", str(df[col].dtype), orig])
        
    header = "| " + " | ".join(schema_rows[0]) + " |"
    separator = "| " + " | ".join(["---"] * 3) + " |"
    body = "\n".join(["| " + " | ".join(row) + " |" for row in schema_rows[1:]])
    
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [f"{header}\n{separator}\n{body}\n"]
    })
    
    # 2. Pearson vs Spearman
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Dual Correlation Matrix (Pearson vs Spearman)\n",
            "**Pearson**: Measures linear relationships. Ideal for truly continuous data.\n",
            "**Spearman**: Measures monotonic relationships (rank-based). Ideal for Likert scales and non-linear associations."
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "fig, axes = plt.subplots(2, 1, figsize=(20, 16))\n",
            "\n",
            "corr_p = df[analysis_cols].corr(method='pearson')\n",
            "sns.heatmap(corr_p, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=axes[0])\n",
            "axes[0].set_title('Pearson Correlation (Linear)')\n",
            "\n",
            "corr_s = df[analysis_cols].corr(method='spearman')\n",
            "sns.heatmap(corr_s, annot=True, fmt='.2f', cmap='magma', center=0, ax=axes[1])\n",
            "axes[1].set_title('Spearman Correlation (Rank-based)')\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()\n",
            "\n",
            "print('Pearson Correlation Table:')\n",
            "display(corr_p.round(5))\n",
            "print('Spearman Correlation Table:')\n",
            "display(corr_s.round(5))"
        ]
    })
    
    # 3. Key Driver Analysis
    if target_col and target_col in df.columns:
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"## 3. Key Driver Analysis (Target: `{target_col}`)\n",
                "Identifying which attributes have the strongest impact on the target variable using Random Forest Feature Importance."
            ]
        })
        
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "target = target_col\n",
                "features = [c for c in analysis_cols if c != target]\n",
                "X = df[features].fillna(df[features].median())\n",
                "y = df[target].fillna(df[target].median())\n",
                "\n",
                "rf = RandomForestRegressor(n_estimators=100, random_state=42)\n",
                "rf.fit(X, y)\n",
                "\n",
                "importance = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=False)\n",
                "plt.figure(figsize=(10, 8))\n",
                "sns.barplot(x=importance.values, y=importance.index, palette='viridis')\n",
                "plt.title(f'Key Drivers for {target}')\n",
                "plt.xlabel('Importance Weight')\n",
                "plt.show()\n",
                "\n",
                "print('Feature Importance Table:')\n",
                "display(importance.to_frame('Relative Importance').round(5))"
            ]
        })
        
    # 4. Cluster Analysis
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Cluster Analysis (Audience Personas)\n",
            "We use two complementary methods to group respondents:\n\n",
            "- **K-Means Clustering**: Forces every respondent into one of *K* groups. Best for creating standard marketing **Personas** or when you need a fixed number of segments.\n",
            "- **DBSCAN (Density-Based)**: Finds groups based on how \"crowded\" the data is. It does NOT force everyone into a group—it identifies **Outliers (Noise)** as `-1`. Best for seeing if there are natural, dense sub-populations or for anomaly detection."
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "X_cluster = df[analysis_cols].apply(pd.to_numeric, errors='coerce').fillna(df[analysis_cols].median())\n",
            "scaler = StandardScaler()\n",
            "X_scaled = scaler.fit_transform(X_cluster)\n",
            "\n",
            "# 1. K-Means Approach (Personas)\n",
            "kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)\n",
            "df['KMeans_Cluster'] = kmeans.fit_predict(X_scaled)\n",
            "\n",
            "# 2. DBSCAN Approach (Natural Density & Noise)\n",
            "dbscan = DBSCAN(eps=0.5, min_samples=5)\n",
            "df['DBSCAN_Cluster'] = dbscan.fit_predict(X_scaled)\n",
            "\n",
            "print(f'K-Means created 3 clusters.')\n",
            "print(f'DBSCAN found {len(df[df[\"DBSCAN_Cluster\"] != -1][\"DBSCAN_Cluster\"].unique())} dense groups and {len(df[df[\"DBSCAN_Cluster\"] == -1])} outliers.')"
        ]
    })
    
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Cluster Profile Visualization (K-Means)\n",
            "Comparing mean ratings across the 3 Personas identified."
        ]
    })

    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Ensure only numeric columns are used for the profile\n",
            "numeric_analysis_cols = df[analysis_cols].select_dtypes(include=[np.number]).columns.tolist()\n",
            "cluster_profile = df.groupby('KMeans_Cluster')[numeric_analysis_cols].mean().T\n",
            "\n",
            "plt.figure(figsize=(12, 10))\n",
            "sns.heatmap(cluster_profile.astype(float), annot=True, cmap='RdYlGn', center=5)\n",
            "plt.title('Persona Profiles (K-Means Average Ratings)')\n",
            "plt.show()\n",
            "\n",
            "print('Cluster Mean Profile:')\n",
            "display(cluster_profile.round(5))"
        ]
    })
    
    # 5. Dimensionality Reduction (Strategic Groups)
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Dimensionality Reduction (Strategic Groups)\n",
            "Reducing attributes to main factors using Factor Analysis (via scikit-learn)."
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "fa = FactorAnalysis(n_components=3, random_state=42)\n",
            "fa.fit(X_scaled)\n",
            "loadings = pd.DataFrame(fa.components_.T, columns=['Factor 1', 'Factor 2', 'Factor 3'], index=analysis_cols)\n",
            "\n",
            "plt.figure(figsize=(10, 10))\n",
            "sns.heatmap(loadings, annot=True, cmap='coolwarm', center=0)\n",
            "plt.title('Factor Loadings (Attribute Groupings)')\n",
            "plt.show()\n",
            "\n",
            "print('Factor Loadings Table:')\n",
            "display(loadings.round(5))"
        ]
    })

    # 6. Bias Removal & Residual Analysis (Halo & Ipsative)
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Bias Removal & Residual Analysis\n",
            "Survey ratings are often skewed by the **Halo Effect** (general good/bad impression) or individual response styles. We use these techniques to reveal the 'pure' sentiment:\n\n",
            "- **Ipsative Analysis**: Centering ratings by the respondent's own average. Shows if an attribute is *relatively* better or worse than the person's standard.\n",
            "- **Halo Removal (Residuals)**: Uses linear regression to remove the 'General Impression' bias from individual attribute scores."
        ]
    })
    
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "rating_cols = [c for c in analysis_cols if 'rating' in c.lower() or 'score' in c.lower()]\n",
            "if len(rating_cols) > 2:\n",
            "    # 1. Ipsative Adjustment\n",
            "    df_ratings = df[rating_cols].apply(pd.to_numeric, errors='coerce').fillna(df[rating_cols].median())\n",
            "    personal_mean = df_ratings.mean(axis=1)\n",
            "    df_ipsative = df_ratings.sub(personal_mean, axis=0)\n",
            "    \n",
            "    plt.figure(figsize=(12, 6))\n",
            "    sns.barplot(data=df_ipsative, orient='h', palette='coolwarm', errorbar=None)\n",
            "    plt.title('Ipsative Analysis: Relative Performance (Personal Mean = 0)')\n",
            "    plt.axvline(0, color='black', linestyle='--')\n",
            "    plt.show()\n",
            "    \n",
            "    # 2. Halo removal via Regression Residuals\n",
            "    from sklearn.linear_model import LinearRegression\n",
            "    residuals = {}\n",
            "    for col in rating_cols:\n",
            "        X_halo = personal_mean.values.reshape(-1, 1)\n",
            "        y_halo = df_ratings[col].values\n",
            "         model = LinearRegression().fit(X_halo, y_halo)\n",
            "        pred = model.predict(X_halo)\n",
            "        residuals[col] = (y_halo - pred).mean()\n",
            "        \n",
            "    res_df = pd.Series(residuals).sort_values()\n",
            "    plt.figure(figsize=(10, 8))\n",
            "    colors = ['red' if x < 0 else 'green' for x in res_df.values]\n",
            "    res_df.plot(kind='barh', color=colors)\n",
            "    plt.title('Halo Effect Removal: Residual Value per Attribute')\n",
            "    plt.grid(axis='x', linestyle='--', alpha=0.7)\n",
            "    plt.show()\n",
            "\n",
            "    print('Ipsative Summary (First 10 rows):')\n",
            "    display(df_ipsative.head(10).round(5))\n",
            "    print('Halo Residuals Series:')\n",
            "    display(res_df.to_frame('Residual Score').round(5))"
        ]
    })

    # 7. Chi-Squared Residuals (Categorical Patterns)
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 7. Chi-Squared Residual Analysis (Detecting Anomalies)\n",
            "This analysis identifies where categories (e.g., origin) deviate significantly from the expected average. \n",
            "Values > 2 or < -2 indicate statistically significant 'surprises' in the data."
        ]
    })

    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from scipy.stats import chi2_contingency\n",
            "cat_cols = [c for c in df.columns if (df[c].dtype == 'object' or df[c].dtype.name == 'category') and not any(m in c.lower() for m in metadata)]\n",
            "\n",
            "if len(cat_cols) > 0 and target_col in df.columns:\n",
            "    # Select the first categorical column to cross with target (binned)\n",
            "    main_cat = cat_cols[0]\n",
            "    # Smart Binning: fall back to default labels if duplicates drop too many bins\n",
            "    target_series = df[target_col].fillna(df[target_col].median())\n",
            "    try:\n",
            "        df['target_binned'] = pd.qcut(target_series, 3, labels=['Low', 'Mid', 'High'], duplicates='drop')\n",
            "    except ValueError:\n",
            "        df['target_binned'] = pd.qcut(target_series, 3, duplicates='drop')\n",
            "    \n",
            "    contingency = pd.crosstab(df[main_cat], df['target_binned'])\n",
            "    chi2, p, dof, expected = chi2_contingency(contingency)\n",
            "    \n",
            "    # Standardized Residuals\n",
            "    residuals = (contingency - expected) / np.sqrt(expected)\n",
            "    \n",
            "    plt.figure(figsize=(10, 6))\n",
            "    sns.heatmap(residuals, annot=True, cmap='RdBu_r', center=0)\n",
            "    plt.title(f'Chi-Squared Residuals: {main_cat} vs {target_col}')\n",
            "    plt.show()\n",
            "\n",
            "    print('Standardized Residuals Table:')\n",
            "    display(residuals.round(5))\n",
            "else:\n",
            "    print('Not enough categorical data or target missing for Chi-Squared Analysis.')"
        ]
    })

    # Save
    notebook = {
        "cells": cells,
        "metadata": {"kernelspec": {"display_name": "Python 3", "name": "python3"}},
        "nbformat": 4, "nbformat_minor": 5
    }
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
    print(f"Advanced notebook saved: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 advanced_analytics_generator.py <data> <target> [output.ipynb]")
    else:
        path = sys.argv[1]
        target = sys.argv[2] if len(sys.argv) > 2 else "recommend_score"
        out = sys.argv[3] if len(sys.argv) > 3 else "advanced_analytics.ipynb"
        create_advanced_notebook(path, target, out)
