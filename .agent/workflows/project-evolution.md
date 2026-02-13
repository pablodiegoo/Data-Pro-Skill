---
description: "Absorb harvested learnings into Data-Pro-Skill. Filters for high-value, high-reuse items across ALL project components: skills, rules, workflows, references, database, and structure."
---

# Project Evolution

This workflow runs **exclusively in the Data-Pro-Skill repository**. It absorbs harvested learnings from one or more target projects (via `/project-harvest`) and evolves the **entire project** — skills, rules, workflows, references, database, and structure.

> [!CAUTION]
> This workflow modifies Data-Pro-Skill core files. Every change must be justified and documented. Never absorb without filtering.

## Prerequisites

1. A completed `/project-harvest` folder (`assets/harvest/`) from at least one project.
2. Access to the Data-Pro-Skill repository.
3. Read `assets/harvest/overview.md` for context.

## Absorption Gate (Mandatory Filter)

Every candidate item from the harvest **MUST** pass ALL criteria:

| Criterion | Question | Fail Action |
|-----------|----------|-------------|
| **Rule of 3** | Will this be useful in ≥3 future projects? | Skip — too niche. |
| **Data Science Focus** | Is this relevant to analyst/scientist daily work? | Skip — out of scope. |
| **Non-Redundant** | Does a similar capability already exist in the project? | Merge/enhance instead of duplicate. |
| **Production-Ready** | Is the code clean, parameterized, English-only? | Refactor before absorbing. |
| **Weight Check** | Will this add cognitive load without proportional value? | Skip — too superficial. |

## Evolution Phases

### Phase 1: Skills Evolution
**Goal**: Enhance existing skills or create new ones.

1. Review `assets/harvest/scripts/README.md` for candidates.
2. For each qualifying script:
   - **Existing skill match** → Add to the skill's `scripts/` directory.
   - Product skills live in `src/datapro/data/skills/`.
   - Shared skills live in `.agent/skills/` (listed in `deploy_manifest`).
   - **New capability** → Evaluate if it warrants a new skill (use `skill-creator`).
3. Update affected `SKILL.md` files:
   - Add new scripts to the file structure section.
   - Update usage examples if applicable.
   - Add new reference docs to `references/`.

### Phase 2: Rules & Governance Evolution
**Goal**: Strengthen project governance based on real-world findings.

1. Review `assets/harvest/rules/` for proposed rules.
2. For each candidate:
   - Check if it conflicts with existing rules in `src/datapro/data/rules/`.
   - If complementary → Merge into existing rule file.
   - If novel → Create new rule file in `src/datapro/data/rules/`.
3. Review `assets/harvest/memory/` for decisions that should become rules.

### Phase 3: Workflows Evolution
**Goal**: Improve workflow efficiency and coverage.

1. Review `assets/harvest/workflows/` for improvement proposals.
2. For each proposal:
   - If it improves an existing workflow → Edit it in `src/datapro/data/workflows/`.
   - If it's a new workflow → Create in `src/datapro/data/workflows/` and register in root `SKILL.md`.
   - Exception: `/project-evolution` itself stays in `.agent/workflows/` (this repo only).
3. Verify all workflow cross-references are consistent.

### Phase 4: References & Documentation Evolution
**Goal**: Expand the knowledge base for specialized skills.

1. Review `assets/harvest/references/` for new methodologies.
2. For each reference:
   - Assign to the most relevant skill's `references/` folder.
   - Update the skill's `SKILL.md` to link the new reference.
3. Check if `document-mastery` patterns need updating.

### Phase 5: Database Evolution
**Goal**: Enhance the `datapro` CLI intelligence.

1. Review `assets/harvest/database/` for proposed additions.
2. For each data file:
   - **`new_snippets.json`** → Merge into `src/datapro/data/code_snippets.json`.
   - **`new_analysis_types.csv`** → Merge into `src/datapro/data/analysis_types.csv`.
   - **`new_rules.csv`** → Merge into `src/datapro/data/reasoning_rules.csv`.
3. Validate: Run `datapro search` and `datapro snippet` to confirm new entries work.

### Phase 6: Structure & Organization Evolution
**Goal**: Keep the project architecture optimal.

1. Review harvest proposals for folder improvements.
2. If `structure.json` needs updating:
   - Edit `src/datapro/data/structure.json` (canonical source).
   - Copy updated file to `.agent/references/structure.json` (agent access).
   - Update `datapro setup` in `cli.py` to match.
   - Update `project-onboarding.md` in `src/datapro/data/workflows/` if affected.
3. Ensure `README.md` and root `SKILL.md` reflect any structural changes.

### Phase 7: Verify & Cleanup (Mandatory)
**Goal**: Confirm every absorbed item is correctly registered, then clean up harvest to prevent repo pollution.

This phase runs as a **loop** over every item that was absorbed in Phases 1-6:

```
FOR EACH absorbed_item IN harvest:
    1. VERIFY: Confirm the item exists at its target location
       - Script: Check file exists in skill's scripts/ directory
       - Rule: Check src/datapro/data/rules/ contains the new rule
       - Snippet: Run `datapro search <keyword>` to confirm it's findable
       - Reference: Check skill's references/ directory
       - Workflow: Check src/datapro/data/workflows/
    
    2. IF verified:
       DELETE the source file from assets/harvest/<subfolder>/
       LOG: "✅ Absorbed and cleaned: <filename>"
    
    3. IF NOT verified:
       LOG: "❌ FAILED verification: <filename> — keeping source"
       SKIP deletion (do not lose data)
```

After the loop:
1. If `assets/harvest/<subfolder>/` is empty → delete the subfolder.
2. If `assets/harvest/` is empty → delete the directory.
3. Update `assets/harvest/overview.md`:
   - If all items absorbed → delete `overview.md` too.
   - If some items remain → update overview with only the remaining items.

> [!WARNING]
> **Never delete a harvest file without first confirming the target exists.** The verify-then-delete pattern is mandatory. If verification fails, the harvest file must be preserved.

## Documentation

After all phases complete:
1. Update version in `pyproject.toml` and `__init__.py` (patch bump).
2. Create a changelog entry in `docs/plans/YYYY-MM-DD-evolution.md` documenting:
   - What was absorbed and why.
   - What was rejected and why.
   - Source project(s) the learnings came from.
3. Commit with descriptive tag: `feat: project evolution from <source_project>`.

---
> [!IMPORTANT]
> The primary goal is **enrichment without bloat**. The project must remain lean and focused on data analysis. Every addition competes for agent context window space.
