# How to Contribute & Evolve "Data Pro Max"

This document outlines the **Lifecyle of a Skill**, defining how we capture project learnings and turn them into permanent Agent capabilities.

## The Evolution Cycle

1.  **Incubation (In-Project)**
    - Don't try to build a perfect "Skill" immediately.
    - Solve the problem inside your current project using `scripts/` or `notebooks/`.
    - **Tagging**: If a script feels generic, add a comment header: `# CANDIDATE FOR PROMOTION`.

2.  **Harvesting (End-of-Project)**
    - Run the `@/project-retrospective` workflow.
    - Identify the "Candidate" scripts.
    - **Action**: Copy the selected files (AND `retrospective.md`) to the `staging/` folder in this repository.

3.  **Promotion (Upstreaming)**
    - **Action**: Run the `@/process-contribution` workflow.
    - **From `staging/`**: Review the files.
    - **Refactor**: Clean up code.
    - **Move**:
        - **Scenario A: It's a Script** -> Move to `.agent/skills/<category>/scripts/`.
        - **Scenario B: Core Logic** -> Integrate into `src/datapro/`.
        - **Scenario C: Workflow** -> Update `.agent/workflows/`.
        - **Scenario D: Lesson Learned** -> Read `retrospective.md` and update `agent_guide.md` or `SKILL.md`.
    - **Cleanup**: Delete the file from `staging/`.

## Best Practices for Reusability

- **No Hardcoded Paths**: Use `argparse` or function arguments for input/output paths.
- **Dependencies**: If you use a new library (`scipy`, `networkx`), add it to `pyproject.toml`.
- **Documentation**: Every new Skill needs a `SKILL.md` (or update existing one).
- **Interface**: Prefer CLI availability (`datapro <command>`) over hidden scripts.

## Registering Changes
After promoting a feature:
1.  Update `SKILL.md` (Root) to advertise the new power.
2.  Update `scripts/code_snippets.json` if it's a reusable snippet.
3.  Bump version in `src/datapro/__init__.py`.
