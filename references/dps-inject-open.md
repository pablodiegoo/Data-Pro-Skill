# /dps-inject-open [text or file] — Qualitative Injection

Categorizes open-ended responses within existing quantitative segments.

## Pipeline

```
Open-ended responses + segments → Python script → quali_themes.csv + quali_verbatims.json + quali_report.md
```

## Prerequisites

A `/dps-setup` must have been executed first. The manifesto defines the segment structure that qualitative data maps into.

## Execution Steps

1. **Read input** — text pasted inline or CSV file with responses
2. **Validate** — check that segments exist from `/dps-setup`
3. **Run script**:
   ```bash
   python3 .dps/scripts/qualitative_categorizer.py responses.csv --segments .dps/outputs/setup/setup_segments.csv -o .dps/outputs/quali/
   ```
4. **Read output** — themes CSV + verbatims JSON
5. **Render** — subsection within each quantitative segment

## Output Format

```
### Análise Qualitativa — Segment A

**Contexto:** Segment A from manifesto (N=290, Churn=45%)

**Theme 1: Price Barrier** — mentioned by 8 of 12 participants
> "Too expensive for a student. After the trial I quit." — P4, 22yo
> "I like it but the price doesn't justify it." — P7, 19yo

**Theme 2: Lack of Time** — mentioned by 5 of 12 participants
> "I just don't have time to use it anymore." — P12, 28yo
```

## Rules

- N < 30: report raw counts, NEVER percentages
- Min 2 verbatims per theme claimed
- Always attach to a segment — never standalone
