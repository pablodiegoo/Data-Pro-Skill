---
description: "Initializes the project directory structure and basic utility files."
---

# Bootstrap Structure Workflow

This workflow ensures that the standard project structure is in place and initialized.

## Step 1: Directory Verification
Ensure the following directories exist:
- `scripts/`
- `db/`
- `assets/`
- `assets/docs/`
- `assets/images/`
- `context/`

Use calling `run_command` with `mkdir -p script db docs assets context` if any are missing.

## Step 2: Initialize Context Files
Ensure basic files are present in `docs/` or root if needed:
- [ ] Create a `README.md` if it doesn't exist.
- [ ] Ensure `.agent/` is properly structured.

## Step 3: Tool Check
Verify that essential skills for the project type are available.
- For survey projects: `survey-stats`, `report-writer`.
- For general analysis: `brainstorming`, `documentation-mastery`.