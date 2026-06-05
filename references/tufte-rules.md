# Tufte Output Formatting Rules

High data density, minimum ink, zero prose fluff.

## Forbidden Phrases

Start NO paragraph with:
- "It's important to note that..."
- "Based on the data provided..."
- "Interestingly..."
- "It is worth mentioning..."
- "One can observe that..."
- "The data suggests that..."
- "In conclusion..."

Go straight to the data. First sentence = finding, not throat-clearing.

## Table Format

Every table MUST include:
- N (sample size) in its own column
- Conclusion/insight in the header row or caption
- Self-explanatory without surrounding text

```
| Segment | N | % | Core Metric | Insight |
|---------|---|----|-------------|---------|
| Value   | N | % | Value       | Finding |
```

## Margin Notes

After data tables, add interpretation as blockquotes:

```
> **Margin Note:** Sharp, specific insight — never generic.
```

Rules:
- Explain "so what?" — not repeat the table
- Connect to business implications
- Reference qualitative verbatims when available
- Max 3 sentences

## Quantitative Standards

- Percentages: include margin of error: `45% (±3.2%, 95% CI)`
- Test statistics: `χ²(3, N=1450) = 24.7, p < 0.001`
- Effect sizes: `Cohen's d = 0.42 (moderate)`
- 1 decimal for %, 2 decimals for test stats

## Mermaid Charts

Include Mermaid bar charts in Markdown outputs for visual comparison:

```mermaid
xychart-beta
  title "Title"
  x-axis "Label" ["A","B","C"]
  y-axis "Unit" 0 --> 100
  bar [value1, value2, value3]
```

Rules:
- Only use `xychart-beta` type (most portable across harnesses)
- Always include title and axis labels
- Data must match the table it accompanies
- Max 8 bars per chart

## Qualitative Standards

- Verbatims in `"quotes"` with participant context
- Theme frequency: `mentioned by N of M participants` (no % when N<30)
- Always categorized within an existing quantitative segment
