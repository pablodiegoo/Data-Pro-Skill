# Invisible Agent Loop

Every command triggers three internal agents. Only the final output reaches the user.

## Default Mode (Quant)

```
User → [Orchestrator] → [Statistician] → [Critic] → [Tufte Designer]
                                                              ↓
                                                     Output to user
```

| Stage | Agent | Responsibility |
|-------|-------|----------------|
| 1 | **Statistician** | Validate N, compute distributions, select statistical test, flag quality issues |
| 2 | **Critic** | Detect biases, spurious correlations, overgeneralizations, missing data |
| 3 | **Tufte Designer** | Render output: zero fluff, dense tables, margin notes |

## Qualitative Mode (`/dps-mode:quali`)

Anthropologist is inserted as Stage 3, shifting Tufte Designer to Stage 4:

```
User → Orchestrator → Statistician → Critic → Anthropologist → Tufte Designer → Output
```

| Stage | Agent | Responsibility |
|-------|-------|----------------|
| 1 | **Statistician** | Numerical validation (same as quant) |
| 2 | **Critic** | Audit including qualitative dimensions (verbatim count, generalization risk) |
| 3 | **Anthropologist** | Thematic analysis, verbatim extraction, archetype identification |
| 4 | **Tufte Designer** | Render output (same as quant) |

## Strategy Mode (`/dps-mode:strategy`)

Post-processing after all analysis. Does not modify the agent loop. After the Tufte Designer outputs, append executive summary, prioritization matrix, and action plan.
