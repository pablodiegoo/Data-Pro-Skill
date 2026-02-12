---
description: "Master workflow for knowledge management. Handles upstream contribution processing and project retrospectives to evolve agent skills."
---

# Knowledge Management (Master Workflow)

This workflow handles the evolution of the "Agent Brain." It manages both candidate refinements (staging) and end-of-project insights (retrospectives).

## Phase 1: Contribution Processing (Gatekeeper)
**Goal**: Promote high-value items from `staging/` to core skills.

1.  **Triage**: Apply the **Rule of 3** (Logic must be useful in at least 3 scenarios).
2.  **Promotion Path**:
    - **Analytical Gains**: Update `data-analysis-suite/scripts/` and its `references/`.
    - **Visual/UX Gains**: Update `data-viz` or `reporting-mastery`.
3.  **Refactor**: Remove project-specific hardcoding and translate to **English**.
4.  **Registration**: Update the root `SKILL.md` and `INDEX_OF_SKILLS.md`.

## Phase 2: Project Retrospective (Post-Mortem)
**Goal**: Identify skill drifts and systemic improvements.

1.  **Skill Drift Analysis**:
    - Did we refine any core skill functions?
    - Did we find gaps in existing documentation?
2.  **Iterative Discovery**: Repeat scans of `scripts/` and `docs/` until no further generic improvements are found.
3.  **Documentation**: Create/Update `docs/retrospective.md` with "What went well" vs. "Pain points."
4.  **Rule Evolution**: Propose new global rules in `.agent/rules/` if common failures are detected.

## Phase 3: Cleanup & Sync
1.  Wipe `staging/` files.
2.  Archive project assets and wipe temporary data.
3.  Commit changes with descriptive tags (e.g., `feat: knowledge evolution <context>`).

---
> [!IMPORTANT]
> The primary focus is **genericity**. Project-specific logic stays in the project; only generic methodologies reach the core skills.
