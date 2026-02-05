---
description: "Guides the post-mortem process to harvest reusable skills, improve workflows, and capture lessons learned."
---

# Project Retrospective & Harvesting

This workflow executes the "Continuous Improvement" cycle. It transforms project-specific wins into permanent Agent capabilities.

## Phase 1: The Harvest & The Filter
**Goal**: Identify candidates and **filter out noise**.

### The "Anti-Pollution" Filter (Strict Criteria):
Before promoting anything, apply the **Rule of 3**:
1.  **Usage**: Was this logic useful in at least 3 distinct scenarios?
2.  **Genericity**: Can it run without *any* modification on a completely different dataset? (No hardcoded column names like `"Q3_Satisfaction"`).
3.  **Independence**: Does it drag in fewer than 3 heavy dependencies?

### Scanning:
1.  **Review `scripts/`**:
    - *Passes Filter?* -> Mark as **CANDIDATE**.
    - *Fails Filter?* -> Archive in project `assets/` only.
2.  **Review `workflows/`**:
    - *Project Specific?* -> Keep local.
    - *Methodology Improvement?* -> **CANDIDATE**.
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
