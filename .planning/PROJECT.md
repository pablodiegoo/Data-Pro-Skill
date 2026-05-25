# Data-Pro-Skill v2

## What This Is

A multi-harness meta-prompt for market research data analysis. Transforms raw quantitative and qualitative research data into dense, Tufte-style analytical documents. Built as a document-driven system where each command anchors context for the next — `/setup` generates the quantitative manifesto, `/cross` slices variables, `/inject-open` weaves qualitative findings into existing segments, and `/export` consolidates everything into a clean Markdown document ready for Quarto/LaTeX/PDF.

Works across AI harnesses (OpenCode, Gemini, Codex, Hermes, OpenClaw, Claude) — not locked to any single runtime.

## Core Value

One prompt that takes raw market research data and produces a publication-ready analytical document — quantitative first, qualitative as layered extensions — with zero prose fluff, maximum data density, and full reproducibility across any AI harness.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- **SETUP-01**: `/setup` command generates a quantitative manifesto with YAML frontmatter, sample metrics, and segment definitions that anchor all subsequent analysis
- **SETUP-02**: Manifesto includes sample size (N), volumetrics (%), and core metrics (NPS, CSAT, Churn) per segment
- **CROSS-01**: `/cross [VarX] x [VarY]` produces dense Tufte-style crosstab tables with narrative margin notes
- **INJECT-01**: `/inject-open [text]` categorizes open-ended responses within existing quantitative segments (not as standalone analysis)
- **MODE-01**: Three internal modes activated by user command — `/mode:quant` (statistical rigor), `/mode:quali` (anthropological depth), `/mode:strategy` (business recommendation)
- **HARNESS-01**: Core prompt logic must be harness-agnostic — no XML tags, no platform-specific syntax
- **OUTPUT-01**: Analytical output follows Tufte principles — high data density, prohibition of prose fluff ("it's important to note"), margin notes for interpretation, self-explanatory tables with N and conclusions in headers
- **EXPORT-01**: `/export` consolidates all analysis into a single clean Markdown file, ready for Pandoc/Quarto/LaTeX conversion
- **CLARIFY-01**: `/clarify` runs 3-5 provocative questions about business goals and hypotheses before touching data
- **CONSTITUTION-01**: `constitution.md` defines inegotiable statistical rigor rules (margin of error, minimum sample size, confidence levels, bias handling)
- **QUANT_FIRST-01**: Quantitative analysis pipeline is built first as the spine; qualitative analysis is added as extensions/ramifications of quantitative segments

### Out of Scope

- Real-time streaming analysis — batch/document-oriented only
- Mobile app or GUI — pure prompt/markdown experience
- Exclusive Claude-only features — must work on free/open harnesses
- Multi-user collaboration features — single-analyst workflow
- Database or API backend — all data provided inline by user

## Context

Originated from frustration with a v1 that was confusing and mal-structured, producing generic or incomplete analysis even on simple datasets. Extensive research (documented in `coonversa.md`) converged on a hybrid inspiration:

- **GSD** (Get Shit Done): Invisible agent mechanics — user interacts only with the orchestrator, internal agents (Statistician, Critic, Tufte Designer) run as silent loops
- **Spec-Kit**: `/clarify` command forces hypothesis-driven exploration before any calculation; `constitution.md` as rigid ethical/statistical rules
- **BMAD**: Mode separation (`/mode:quant` vs `/mode:quali` vs `/mode:strategy`) prevents methodological contamination
- **Tufte**: Output design — high data density, side-margin interpretation notes, zero fluff prose, minimal ink

The architecture is document-driven: each command appends to a growing analytical document, and the `/setup` manifesto anchors all subsequent context. This prevents the "context rot" problem where the AI drifts from initial specifications.

## Constraints

- **Multi-harness**: Must work on OpenCode, Gemini, Codex, Hermes, OpenClaw, and Claude — avoid XML tags, use YAML frontmatter and pure Markdown
- **Document-driven**: First output (`/setup`) must anchor all sequential analysis — no analysis can contradict established metrics
- **Quant-first**: Quantitative pipeline is the spine; qualitative is layered on top, not parallel
- **Single-analyst**: Designed for individual researchers, not teams

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Document-driven architecture | Prevents context rot by anchoring all analysis to the `/setup` manifesto | — Pending |
| Quantitative-first, qualitative as extension | Most replicable path; avoids parallel command loops for quant/quali | — Pending |
| Invisible GSD-style agents | User only talks to orchestrator; internal Statistician/Critic/Designer run silently | — Pending |
| Tufte-style Markdown output | Agnostic format works across all harnesses, exportable to PDF via Quarto | — Pending |
| Multi-harness from day one | Project goal is to help people on free/open harnesses, not lock to Claude | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-25 after initial definition*
