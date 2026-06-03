# /dps-setup — Generate Quantitative Manifesto

Generates the YAML frontmatter + segment matrix that anchors all subsequent analysis.

## Pipeline

```
Raw data → Python script → setup_manifest.json + setup_segments.csv + setup_report.md
```

## Execution Steps

1. **Read input data** — CSV, copypasta table, or structured summary
2. **Validate** — N, missing rates, column types
3. **Generate config JSON** — map columns to metrics, define segments
4. **Run script**:
   ```bash
   python3 .dps/scripts/quant_analyzer.py data.csv config.json -o .dps/outputs/setup/
   ```
5. **Read output** — load `setup_segments.csv` + `setup_manifest.json`
6. **Render** — Tufte-style manifesto Markdown

## Output Format

```yaml
---
project: "Project Name"
framework: "Data-Pro-Skill v2"
sample_size: N
metrics_tracked: [metric1, metric2]
segments: [segA, segB]
---
```

| Segment | N | % | Core Metric |
|---------|---|----|-------------|
| Seg A | N | % | value |

> **Margin Note:** This document anchors numerical context. No subsequent analysis may contradict metrics established here.

## Flags

- `--json-only`: Output only `setup_manifest.json` (no Markdown rendering)
- `--csv`: Output only `setup_segments.csv`
