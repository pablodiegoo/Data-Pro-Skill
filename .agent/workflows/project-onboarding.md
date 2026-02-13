---
description: "Master workflow for project onboarding. Handles environment setup, context discovery, and automated rules generation."
---

# Project Onboarding (Master Workflow)

This workflow is the mandatory starting point for all new analytical projects. It ensures the agent is grounded in the project's data and business objectives.

## Phase 1: Environment & Setup
**Goal**: Initialize the project structure.
1.  **Action**: Use the `datapro setup` terminal command.
2.  **Verify**: Ensure the directory tree complies with [structure.json](file:///.agent/references/structure.json).
3.  **Mandatory Directories**: 
    - `scripts/` (utils/ notebooks/)
    - `database/` (raw/ metadata/ processed/ final/)
    - `docs/` (studies/ reports/ plans/)
    - `assets/` (images/ docs/ context/)
    - `.agent/` (rules/ references/ skills/ workflows/ memory/)

## Phase 2: Context Discovery (Deep Search)
**Goal**: Identify available data and objectives.
1.  **Inventory**: Run `list_dir` on root and `database/` to map data files.
2.  **Analysis**: Read the primary brief or proposal.
3.  **Extraction**:
    - Business Objective & Success Criteria.
    - Universe Targets (mandatory for weighting).
    - Data Dictionary/Schema.
4.  **Knowledge Base**: Populate `.agent/references/` with extracted facts.

## Phase 3: Automated Governance
**Goal**: Generate technical rules tailored to the project.
1.  **Rules Generation**: Create specialized files in `.agent/rules/`:
    - `coding-standards.md`: Python & DuckDB best practices.
    - `data-governance.md`: Reproducibility and immutability rules.
    - `quality-assurance.md`: Pre-flight and weighted audit checks.

## Phase 4: Strategy & Roadmap
**Goal**: Define "How" it will be built.
1.  **Project Brief**: Create `docs/plans/project-brief.md` summarizing the technical strategy.
2.  **Task Initiation**: Create the initial `task.md` with the first concrete steps.
3.  **User Sign-off**: Present the brief to the user for final approval.

---
> [!IMPORTANT]
> Skip no phases. Discovery and Governance provide the "guardrails" for the entire execution.