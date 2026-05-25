# Walking Skeleton — Data-Pro-Skill v2

**Phase:** 1
**Generated:** 2026-05-25

## Capability Proven End-to-End

A market researcher copies SKILL.md and constitution.md to their AI harness, invokes /dps-setup with raw quantitative survey data (N=1450, 3 segments), and the invisible agent loop (Statistician → Critic → Tufte Designer) produces a Tufte-formatted quantitative manifesto with YAML frontmatter, segment matrix with N/percentage/metric columns, margin notes as blockquotes, margin of error on all percentages, and zero prose fluff.

## Architectural Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Document format | Pure Markdown + YAML frontmatter | Universal across all 6 target harnesses (OpenCode, Gemini, Codex, Claude, Hermes, OpenClaw); no XML dependency; any harness can render Markdown |
| Agent architecture | Invisible 3-stage loop (Statistician → Critic → Tufte Designer) | Internal validation without user-facing complexity; user only sees final formatted output; each stage has a dedicated agent file in agents/ |
| Data anchoring | Document-driven: /dps-setup manifesto is single source of truth | Prevents context drift across analysis sessions; all subsequent commands reference manifesto segments; no analysis can contradict established metrics |
| Output style | Tufte principles: high data density, margin notes, self-explanatory tables | Maximizes information per word; tables include N and conclusions in headers; margin notes explain "so what?"; publication-ready output via Quarto/LaTeX |
| Command naming | /dps- prefix on all 9 commands | Distinguishes from GSD infrastructure; avoids harness-native command collision; consistent namespace for all analysis operations |
| Harness compatibility | Lowest common denominator: no XML, no HTML, no platform-specific syntax | Works on all 6 target harnesses without modification; agents/ files use XML internally but SKILL.md is pure Markdown |
| File structure | SKILL.md as orchestrator + constitution.md as rules + agents/ as detailed instructions | Concern separation: orchestration logic (SKILL.md) vs. enforcement rules (constitution.md) vs. agent-specific behaviors (agents/*.md); SKILL.md references others by path |
| Rule enforcement | constitution.md read by Critic agent; violations block output | Mechanical enforcement: each article defines a yes/no test the Critic can apply; violations prevent Designer from delivering output |
| Phase 1 scope | /dps-setup only; all other commands are named stubs | Vertical slice: one working command proves the architecture; other commands receive /dps- names and one-line descriptions for Phase 2+ implementation |

## Stack Touched in Phase 1

- [x] constitution.md — Statistical rigor rules (6 articles, 8 rules)
- [x] SKILL.md — Main meta-prompt: YAML frontmatter, agent loop, /dps-setup, command reference, Tufte rules, DPS naming
- [x] Agent loop — 3-stage invisible processing proven working (Statistician validates, Critic audits, Tufte Designer formats)
- [x] /dps-setup — Manifesto generation proven end-to-end with sample N=1450 dataset
- [x] Multi-harness format — Pure Markdown, zero XML, YAML frontmatter, no platform-specific syntax
- [x] Walking skeleton — output manifest at outputs/00_walking_skeleton_manifest.md

## Out of Scope (Deferred to Later Phases)

- /dps-cross — Crosstab analysis with Tufte-style tables (Phase 2)
- /dps-clarify — Business hypothesis elicitation (Phase 2)
- /dps-plan — Analytical plan design (Phase 2)
- /dps-inject-open — Qualitative response categorization within segments (Phase 3)
- /dps-mode:quali full implementation — Anthropologist persona activation (Phase 3)
- /dps-export — Document consolidation + Quarto/LaTeX conversion (Phase 4)
- /dps-mode:strategy full implementation — BI Director persona (Phase 4)
- Multi-harness compatibility testing — validation across all 6 target harnesses (Phase 4)
- Automated installation scripts — per-harness setup automation (Phase 4)
- Quarto/LaTeX templates — PDF output pipeline (Phase 4)

## Subsequent Slice Plan

- **Phase 2:** /dps-clarify asks business questions, /dps-plan designs analytical approach, /dps-cross produces Tufte-style crosstabs with significance tests — all anchored to the Phase 1 manifesto
- **Phase 3:** /dps-inject-open categorizes open-ended responses within existing quantitative segments, /dps-mode:quali activates full Anthropologist persona — qualitative as a ramification of quantitative
- **Phase 4:** /dps-mode:strategy translates numbers into business recommendations, /dps-export consolidates everything into clean Markdown for Pandoc/Quarto/LaTeX, multi-harness validation across all 6 targets
