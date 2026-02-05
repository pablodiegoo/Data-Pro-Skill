---
description: "Guides the post-mortem process to harvest reusable skills, improve workflows, and capture lessons learned."
---

# Project Retrospective & Harvesting

This workflow executes the "Continuous Improvement" cycle. It transforms project-specific wins into permanent Agent capabilities.

## Phase 1: The Harvest (Code & Artifacts)
**Goal**: Identify what should be promoted to the permanent knowledge base.

1.  **Scan `scripts/`**:
    - Identify scripts used repeatedly or that solved a generic problem.
    - *Decision*: Should this become a named Skill or a CLI command?
2.  **Review `workflows/`**:
    - Did we modify any standard workflow?
    - Did we create a new ad-hoc workflow?
    - *Decision*: Update the master workflow in `Data-Pro-Skill`?
3.  **Review `docs/`**:
    - Did we create a new template?
    - Did we find a gap in the `agent_guide.md`?

## Phase 2: Documentation (Lessons Learned)
**Goal**: Stop making the same mistakes.

1.  Create `docs/retrospective.md`.
2.  Answer:
    - **What went well?** (Keep doing this)
    - **What was painful?** (Automate this)
    - **What was missing?** (Build this)
3.  **Action Item**: Update `.agent/rules/` if a new governance rule is needed to prevent recurrence of issues.

## Phase 3: Upstream Promotion (The Merge)
**Goal**: Update the Main Brain.

1.  **Copy Candidates**: Move selected scripts/workflows to a staging bucket (or directly to the `Data-Pro-Skill` repo if you are the maintainer).
2.  **Refactor**: Remove hardcoded project paths.
3.  **Register**: Add the new capability to `SKILL.md` or `agent_guide.md`.

## Phase 4: Closure
1.  Archive project outputs.
2.  Wipe temporary data in `db/processed`.
