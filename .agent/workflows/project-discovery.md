---
description: "Orchestrator for project onboarding. Manages structure setup, context gathering, and planning."
---

# Project Discovery Orchestrator

This workflow coordinates various sub-workflows to move a project from a raw request to a structured implementation plan. It is the mandatory starting point for all AGP/Antigravity projects.

## Overview
The discovery process is divided into specialized phases, each handled by a dedicated submodule workflow.

## Phase 1: Environment Setup
Goal: Ensure the project has the standard AGP folder structure.
- **Action**: Call @[/bootstrap-structure].
- **Output**: Directories `script`, `db`, `docs`, `assets`, `context` and basic files.

## Phase 2: Context & Data Discovery
Goal: Identify what needs to be done and what data is available.
- **Action**: Call @[/context-bootstrap].
- **Output**: Populated `.agent/references/` and data inventory.

## Phase 3: Governance & Rules
Goal: Define how the project will be built and structured.
- **Action**: Call @[/build-project-rules].
- **Output**: `.agent/rules/` populated with Coding Standards and DS Governance.

## Phase 4: Goal & Deliverable Mapping
Goal: Align with the user on "Why" and "What".
- **Interaction**: Ask the user about:
    1.  The "Big Question" (Business impact).
    2.  Success criteria.
    3.  Deliverable formats (PDF, Dashboard, etc.).

## Phase 5: Strategy & Finalization
Goal: Define the "How" and create the roadmap.
- **Action**: Call @[/discovery-completion].
- **Output**: `project-brief.md` and initial `task.md`.

---
**Best Practice**: Never skip Phase 1 and 2. They provide the necessary grounding for any technical task.
