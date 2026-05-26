<!-- GSD:project-start source:PROJECT.md -->
## Project

**Data-Pro-Skill v2**

A multi-harness meta-prompt for market research data analysis. Transforms raw quantitative and qualitative research data into dense, Tufte-style analytical documents. Built as a document-driven system where each command anchors context for the next — `/setup` generates the quantitative manifesto, `/cross` slices variables, `/inject-open` weaves qualitative findings into existing segments, and `/export` consolidates everything into a clean Markdown document ready for Quarto/LaTeX/PDF.

Works across AI harnesses (OpenCode, Gemini, Codex, Hermes, OpenClaw, Claude) — not locked to any single runtime.

**Core Value:** One prompt that takes raw market research data and produces a publication-ready analytical document — quantitative first, qualitative as layered extensions — with zero prose fluff, maximum data density, and full reproducibility across any AI harness.

### Constraints

- **Multi-harness**: Must work on OpenCode, Gemini, Codex, Hermes, OpenClaw, and Claude — avoid XML tags, use YAML frontmatter and pure Markdown
- **Document-driven**: First output (`/setup`) must anchor all sequential analysis — no analysis can contradict established metrics
- **Quant-first**: Quantitative pipeline is the spine; qualitative is layered on top, not parallel
- **Single-analyst**: Designed for individual researchers, not teams
<!-- GSD:project-end -->

<!-- GSD:stack-start source:STACK.md -->
## Technology Stack

This is a **document-driven meta-prompt** — not a software application. No compilation, no runtime, no database.

- **Core format:** Markdown + YAML frontmatter (harness-agnostic)
- **Output pipeline:** Markdown → Quarto/LaTeX → PDF (or direct Pandoc)
- **Agent system:** Invisible loop (Statistician → Critic → Tufte Designer) controlled via prompt instructions
- **GSD engine:** `dps-engine/` — workflows, templates, references for project management
- **Testing:** Manual validation across 6 target harnesses (OpenCode, Gemini, Codex, Hermes, OpenClaw, Claude)
- **Version control:** Git + GSD planning artifacts in `.planning/`
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

### Document Format

- **No XML tags.** Use YAML frontmatter and pure Markdown only.
- **No platform-specific syntax.** Test on all 6 target harnesses.
- **Tables:** Always include N (sample size) and conclusion in headers. Self-explanatory.
- **Margin notes:** Use `>` blockquotes after data tables for interpretation.

### Code Style

- **No comments** unless strictly necessary — the prompt is the documentation.
- **No emoji** in analytical output (margin notes may use subtle indicators).
- **No prose fluff.** Never use phrases like "It's important to note that..." or "Based on the data provided...". Go straight to the data.

### Quantitative Rules

- Always compute margin of error for sample-based claims
- Require p < 0.05 for significance claims
- Never generalize from qualitative samples (N < 30 = no percentages)

### Qualitative Rules

- Categorize within existing quantitative segments only
- No standalone qualitative sections — always attached to a quant segment
- Quote verbatims directly, note frequency without false precision
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

### Invisible Agent Loop

```
User command → [Orchestrator] → [Statistician] → [Critic] → [Tufte Designer]
                                                              ↓
                                                     Output to user ONLY
```

Three internal agents run silently per command. The user only sees the Tufte-formatted output:

1. **Statistician** — Validates numerical consistency, calculates distributions, chooses tests
2. **Critic** — Detects biases, spurious correlations, overgeneralizations, missing data
3. **Tufte Designer** — Synthesizes output: zero fluff, max data density, margin notes

### Document-Driven Context

```
/setup  →  outputs/00_project_manifest.md
/cross  →  outputs/01_crosstab_[VarX]_x_[VarY].md
/cross  →  outputs/02_crosstab_[VarA]_x_[VarB].md
/inject →  (enriches existing segments inline)
/export →  outputs/final_report.md (consolidated)
```

The `/setup` manifesto is the single source of truth. No subsequent command can produce output that contradicts metrics established in setup.

### Command Pipeline

Each command appends or enriches the growing analytical document:
- `/setup` — creates the quantitative manifesto (YAML + segment matrix)
- `/cross` — produces Tufte-style crosstab tables with margin notes
- `/inject-open` — categorizes open-ended responses within existing segments
- `/export` — consolidates everything into a clean Markdown file for Quarto/LaTeX/PDF
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

Core analysis skills defined in the meta-prompt:

| Skill | Command | Purpose |
|-------|---------|---------|
| Setup | `/setup` | Generate quantitative manifesto from raw data |
| Crosstab | `/cross` | Slice variables with Tufte-style tables |
| Qualitative | `/inject-open` | Weave open-ended responses into quant segments |
| Export | `/export` | Consolidate to publication-ready Markdown |
| Clarify | `/clarify` | Surface business hypotheses before analysis |
| Plan | `/plan` | Design analytical approach before execution |

Specialized modes: `/mode:quant` (Statistician), `/mode:quali` (Anthropologist), `/mode:strategy` (BI Director)
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
