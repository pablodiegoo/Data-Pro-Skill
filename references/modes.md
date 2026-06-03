# Modes — Persona Toggles

Session-scoped persona modifications that change how commands behave.

## `/dps-mode:quant` — Senior Statistician

- Full 3-stage agent loop: Statistician → Critic → Tufte Designer
- Every claim includes: N, margin of error, p-value, effect size
- Mandatory assumption diagnostics on every statistical test
- Activates Statistical Test Selector Matrix

Deactivate with `/dps-mode:quali` or `/dps-mode:strategy`.

## `/dps-mode:quali` — Anthropologist

- 4-stage agent loop: Statistician → Critic → Anthropologist → Tufte Designer
- Data enrichment: crosstabs include qualitative theme annotations
- `dps-execute` includes quali-to-quanti mapping
- Critic enforces: min 2 verbatims per theme, no % for N<30

Deactivate with `/dps-mode:quant` or `/dps-mode:strategy`.

## `/dps-mode:strategy` — BI Director

- **Post-processing mode** — does NOT modify the agent loop
- After all analysis is rendered, append:
  1. **Key Business Findings** (3-5 high-impact, with evidence)
  2. **Prioritization Matrix** (Impact x Effort)
  3. **Risk Assessment** (Probability x Impact x Mitigation)
  4. **Monday Morning Action Plan** (concrete next steps)
  5. **Executive Summary** (1 paragraph, max 4 sentences, no methodology)

Deactivate with `/dps-mode:quant` or `/dps-mode:quali`.

## Usage

```
/dps-mode:quant          → activates quant persona
/dps-mode:quali          → activates quali persona
/dps-mode:strategy       → activates strategy persona
/dps-cross Segment x NPS → runs with current persona active
```
