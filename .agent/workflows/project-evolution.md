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
   - **Existing skill match** → Add to the appropriate skill's `scripts/` directory.
   - **New capability** → Evaluate if it warrants a new skill (use `skill-creator`).
3. Update affected `SKILL.md` files:
   - Add new scripts to the file structure section.
   - Update usage examples if applicable.
   - Add new reference docs to `references/`.

### Phase 2: Rules & Governance Evolution
**Goal**: Strengthen project governance based on real-world findings.

1. Review `assets/harvest/rules/` for proposed rules.
2. For each candidate:
   - Check if it conflicts with existing rules in `.agent/rules/`.
   - If complementary → Merge into existing rule file.
   - If novel → Create new rule file in `.agent/rules/`.
3. Review `assets/harvest/memory/` for decisions that should become rules.

### Phase 3: Workflows Evolution
**Goal**: Improve workflow efficiency and coverage.

1. Review `assets/harvest/workflows/` for improvement proposals.
2. For each proposal:
   - If it improves an existing workflow → Edit the workflow directly.
   - If it's a new workflow → Create in `.agent/workflows/` and register in root `SKILL.md`.
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
   - Edit `.agent/references/structure.json`.
   - Update `datapro setup` in `cli.py` to match.
   - Update `project-onboarding.md` if affected.
3. Ensure `README.md` and root `SKILL.md` reflect any structural changes.

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
