---
description: "Guides the integration of harvested artifacts from 'staging/' into the permanent codebase."
---

# Process Contribution (Upstream Integration)

This workflow is the "Gatekeeper" that turns raw code in `staging/` into permanent, polished capabilities.

## Phase 1: Triage
**Goal**: Decide where the artifacts belong.

1.  **Analyze `staging/`**: Read `retrospective.md` (if present) to understand context.
2.  **Categorize**:
    - **Case A**: New Standalone Capability? -> **New Skill**.
    - **Case B**: Enhancement to existing Skill (e.g., new chart)? -> **Update Skill**.
    - **Case C**: Core Logic (e.g., new math/algo)? -> **Update Python Package**.

## Phase 2: Execution

### Case A: Creating a New Skill
**Action**: Use the `skill-creator` skill.
1.  Run: `@.agent/skills/skill-creator/SKILL.md` (or manually follow instructions).
2.  Scaffold the new folder in `.agent/skills/<new_skill>`.
3.  Move scripts from `staging/` to `.agent/skills/<new_skill>/scripts/`.
4.  Create `SKILL.md` for the new skill.

### Case B: Updating Existing Skill
1.  Identify target skill (e.g., `.agent/skills/survey-stats`).
2.  Move script: `mv staging/my_script.py .agent/skills/survey-stats/scripts/`.
3.  **Refactor**: Ensure it imports correctly from its new home.

### Case C: Updating Core Package
1.  Move file to `src/datapro/`.
2.  Register in `src/datapro/__init__.py` or expose in `cli.py`.

## Phase 3: Finalization
1.  **Register**: Update root `SKILL.md` to mention the new/updated capability.
2.  **Clean**: `rm staging/*`.
3.  **Commit**: `git add . && git commit -m "feat: promoted <artifact> from staging"`
