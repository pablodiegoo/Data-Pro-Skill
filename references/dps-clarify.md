# /dps-clarify — Business Hypothesis Clarification

Pre-analysis conversational step. Asks 3-5 adaptive questions before any data processing.

## Behavior

Does NOT run scripts or generate files. Pure conversation to guide subsequent commands.

1. **Scan** — examine columns, types, segments from available data
2. **Ask 3-5 questions** adaptively from these categories:
   - *Business goal* — What decision depends on this?
   - *Hypothesis* — What do you expect to find?
   - *Surprise* — What would be a surprising result?
   - *Data quality* — Any unreliable columns?
3. **Incorporate answers** — feed into `/dps-setup` config and `/dps-plan` suggestions

## Rules

- Max 5, min 3 questions
- Never use a fixed template — adapt to each dataset
- Record answers in `.dps/outputs/clarify_notes.md` if any decisions are made
