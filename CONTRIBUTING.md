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
    - Assess if they are **Atomic** (do one thing well) and **Generic** (not project-specific).

3.  **Promotion (Upstreaming)**
    - **Scenario A: It's a Script (e.g., specific graph)**
        - Move to `.agent/skills/<category>/scripts/`.
    - **Scenario B: It's a Core Logic (e.g., new statistical test)**
        - Integrate into `src/datapro/` python package.
        - Expose it via `cli.py` if needed.
    - **Scenario C: It's a Workflow improvement**
        - Update the master `.md` file in `.agent/workflows/`.

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
