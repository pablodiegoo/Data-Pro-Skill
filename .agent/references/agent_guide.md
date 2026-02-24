# DataPro Agent Capabilities

This project is enabled with DataPro Intelligence. Use this guide to understand your super-powers.

## 🚀 Key Workflows (Type these in Chat)
- **Start Project**: `/project-onboarding` - Environment setup, context discovery, governance.
- **Analyze Survey**: `/survey-analysis-pipeline` - End-to-end processing (Prep -> Weight -> Viz -> Report).
- **Study Documents**: `/document-study` - Deep analysis of papers, articles, or methodology.
- **Harvest Learnings**: `/project-harvest` - Extract reusable insights → `assets/harvest/`.
- **Evolve Data-Pro**: `/project-evolution` - Absorb harvest into Data-Pro-Skill (run in repo only).

## 💻 CLI Tools
- `datapro search "correlation"`: Find code snippets and rules.
- `datapro analyze data.csv`: Profiling and plan generation.
- `datapro snippet --list`: Get ready-to-use Python code.
- `datapro convert report.pdf`: Convert PDF/DOCX to Markdown.
- `datapro report analysis.md`: Generate professional PDF/DOCX.

## 📂 Governance Rules
- **`database/raw/`**: **IMMUTABLE**. Drop your CSVs here. Never edit them.
- **`scripts/`**: Number your scripts:
  - `01_prep_*.py`: Cleaning
  - `02_analysis_*.py`: Computing
  - `03_viz_*.py`: Plotting
- **`assets/`**: All graphic outputs (charts, images) go here.
- **`docs/`**: Studies, reports, and project plans.

## 🧠 Brain Structure
- `.agent/memory/`: Project facts and decisions.
- `.agent/references/`: This guide and other docs.
- `.agent/skills/`: Your toolbox.
