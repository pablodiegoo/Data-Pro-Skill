# Data Pro Skill

**An AI skill for data analysis intelligence** — the equivalent of [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) for data science.

Auto-activates for data analysis work. Provides reasoning-based recommendations for statistics, visualization, and reporting.

## Features

| Component | Count | Description |
|-----------|-------|-------------|
| Analysis Types | 30+ | Descriptive, inferential, modeling, NLP, time series |
| Visualization Rules | 35+ | Chart recommendations with when-to-use guidance |
| Color Palettes | 22 | Domain-specific (survey, healthcare, finance) |
| Reasoning Rules | 40+ | Auto-recommendations based on data characteristics |

## Quick Start

The skill activates automatically when you request data analysis work:

```
Analyze this survey data and create a professional report
What statistical test should I use for comparing 3 groups?
Create visualizations for my customer satisfaction data
```

## Search the Knowledge Base

```bash
# General search
python3 .agent/skills/data-pro-max/scripts/search.py "correlation"

# Search by type
python3 .agent/skills/data-pro-max/scripts/search.py --type visualization "bar chart"
python3 .agent/skills/data-pro-max/scripts/search.py --type palette --domain survey
python3 .agent/skills/data-pro-max/scripts/search.py --type rule "missing data"

# Filter by domain
python3 .agent/skills/data-pro-max/scripts/search.py --domain survey --category inferential
```

## Integrated Skills

| Skill | Purpose |
|-------|---------|
| `survey-stats` | Weighting, factor analysis, clustering, TURF |
| `report-writer` | Professional PDF/DOCX generation |
| `mermaid-diagrams` | Flowcharts and architecture diagrams |
| `documentation-mastery` | Rich Markdown documentation |

## License

MIT
