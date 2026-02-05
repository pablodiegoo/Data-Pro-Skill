---
name: survey-qual-analyzer
description: "Qualitative text analysis tool for survey open-ended responses. Identifies word frequencies, generates word clouds, and filters sentiment/themes based on conditional segments (e.g., comparing Desistentes vs Non-Desistentes). Use when you have survey columns with categorical feedback or comments."
---

# Survey Qualitative Analyzer

This skill helps transform raw text feedback into actionable insights through frequency analysis and visualization.

## Capabilities

- **Word Frequency Analysis**: Counts occurrences of keywords in text columns.
- **Segment Comparison**: Compare word clouds between different respondent segments (e.g., by region or status).
- **Sentiment/Topic Filtering**: Uses a configurable stop-word list to clean generic language (e.g., "a", "the", "da", "em") and focus on semantic content.

## Usage

### 1. Simple Frequency Count
To get a frequency table of words in a specific column:
```bash
python3 .agent/skills/survey-qual-analyzer/scripts/qual_parser.py input.csv "Column Name" --output frequency.csv
```

### 2. Segmented Analysis
Filter rows before analysis:
```bash
python3 .agent/skills/survey-qual-analyzer/scripts/qual_parser.py input.csv "Feedback" --filter "Status=Desistente"
```

## Related References
- [DASHBOARD_BACKLOG.md](../../tasks/dashboard_backlog.md): For current visualization requests (like word clouds).
