---
phase: 02-quantitative-analysis
plan: 03
subsystem: meta-prompt
tags: [plan, execute, multi-cross, autonomous, checklist]

# Dependency graph
requires:
  - phase: 02-quantitative-analysis
    plan: 01
    provides: /dps-clarify section (insertion anchor), Command Reference structure
  - phase: 02-quantitative-analysis
    plan: 02
    provides: /dps-cross section (insertion anchor + per-cross agent loop reusable by /dps-execute)
provides:
  - /dps-plan command: checklist of suggested crosses (Statistician-only, no agent loop)
  - /dps-execute command: autonomous multi-cross analysis with full agent loop per cross
  - Consolidated Tufte report format with synthesis section
affects: [Phase 3]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Single-agent command (/dps-plan: Statistician only, no Critic, no Designer)"
    - "Autonomous multi-cross execution: derive crosses from manifesto, loop agent per cross, consolidate"

key-files:
  created: []
  modified: [SKILL.md]

key-decisions:
  - "/dps-plan is single-agent (Statistician only) — lightweight recommendation engine, not an analysis command"
  - "/dps-execute works independently from /dps-plan per D-08 — cross derivation from manifesto covers the no-plan case"
  - "/dps-execute treats /dps-plan as starting point per D-09 — adapts to actual data characteristics"
  - "When >20 crosses, prioritize by N and variance; always report which were prioritized and which deferred"
  - "Synthesis ranked by effect size, not p-value — large effect with p=0.06 is more actionable than tiny effect with p=0.001"
  - "Critic audits the synthesis specifically for cross-cross spurious patterns"
  - "Blocked crosses are included with Critic's caveat rather than silently dropped — transparency over completeness"

patterns-established:
  - "Single-agent command pattern: /dps-plan uses only Statistician, explicitly states no Critic, no Designer"
  - "Autonomous execution pattern: read source of truth → derive work items → loop full agent per item → consolidate"

requirements-completed: [PLAN-01, EXEC-01]

# Metrics
duration: 2 min
completed: 2026-05-25
---

# Phase 2 Plan 3: /dps-plan + /dps-execute Summary

**Planning and batch-execution layer: a checklist-based analytical plan generator (Statistician-only) and an autonomous multi-cross executor that reads the manifesto, derives crosses, runs the full agent loop per cross, and produces a consolidated Tufte report with effect-size-ranked synthesis.**

## Performance

- **Duration:** 2 min
- **Started:** 2026-05-25T20:52:39Z
- **Completed:** 2026-05-25T20:54:48Z
- **Tasks:** 3
- **Files modified:** 1 (SKILL.md)

## Accomplishments
- `/dps-plan` command section: single-agent (Statistician only) checklist generator with 4-column table (#, Cruzamento, Teste Recomendado, Justificativa), "Sugestão — não requisito" warning, and prerequisite enforcement (requires /dps-setup)
- `/dps-execute` command section: 5-step autonomous multi-cross pipeline (read manifesto → derive crosses → run agent loop per cross → consolidate → synthesize), independent from /dps-plan
- Cross derivation algorithm: segment × metric combinations from manifesto; prioritization heuristic when >20 (largest N, highest variance) with full transparency about what was deferred
- Consolidated report format: YAML frontmatter, per-cross `##` subsections, and `## Síntese dos Achados` section ranking findings by effect size (not p-value), distinguishing convergent from divergent evidence
- Edge case handling: 1-segment or 1-metric halts with instruction to use /dps-cross instead
- Command Reference table: `/dps-execute` row added, `/dps-plan` status updated — all 4 Phase 2 commands now show "Phase 2 — implemented"

## Task Commits

Each task was committed atomically:

1. **Task 1: Add /dps-plan command section** - `9f98f5f` (feat)
2. **Task 2: Add /dps-execute command section** - `f82a920` (feat)
3. **Task 3: Update Command Reference table for /dps-plan and /dps-execute** - `8c1dd77` (feat)

## Files Created/Modified
- `SKILL.md` — Added `/dps-plan` command section (39 lines) between `/dps-clarify` and `/dps-cross`, added `/dps-execute` command section (31 lines) between `/dps-cross` and Command Reference, updated 2 Command Reference rows

## Decisions Made
- `/dps-plan` uses Statistician only — lightweight recommendation engine, no agent loop (deliberately separates planning from execution)
- `/dps-execute` works independently from `/dps-plan` per D-08 — cross derivation from manifesto covers the no-plan case
- `/dps-execute` treats `/dps-plan` as a starting point per D-09 — adapts to actual data characteristics, never forces plan recommendations
- When >20 crosses, prioritize by N per cell and metric variance; always report which crosses were deferred
- Synthesis is ranked by effect size, not p-value — large effect with p=0.06 is more actionable than tiny effect with p=0.001
- Critic audits the synthesis specifically for cross-cross spurious patterns — highest hallucination risk area
- Blocked crosses are included with Critic's caveat, never silently dropped — transparency over completeness

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None — no external service configuration required. All changes are Markdown prompt text within SKILL.md.

## Next Phase Readiness

- Phase 2 complete: all 6 commands (clarify, plan, cross, execute, mode:quant) fully implemented in SKILL.md
- All 6 Phase 2 requirements (CLAR-01, MODE-01, CROSS-01, CROSS-02, PLAN-01, EXEC-01) satisfied
- Command Reference table: all 4 new Phase 2 commands show "Phase 2 — implemented"
- Remaining stubs: `/dps-inject-open` (Phase 3), `/dps-export` (Phase 4), `/dps-mode:quali` (Phase 3), `/dps-mode:strategy` (Phase 4)
- Ready for Phase 3: Qualitative Injection

---
*Phase: 02-quantitative-analysis*
*Completed: 2026-05-25*
