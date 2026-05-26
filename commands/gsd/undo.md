---
name: gsd:undo
description: "Safe git revert. Roll back phase or plan commits using the phase manifest with dependency checks."
argument-hint: "--last N | --phase NN | --plan NN-MM"
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
requires: [phase]
---

<objective>
Safe git revert — roll back GSD phase or plan commits using the phase manifest, with dependency checks and a confirmation gate before execution.

Three modes:
- **--last N**: Show recent GSD commits for interactive selection
- **--phase NN**: Revert all commits for a phase (manifest + git log fallback)
- **--plan NN-MM**: Revert all commits for a specific plan
</objective>

<execution_context>
@~/.claude/dps-engine/workflows/undo.md
@~/.claude/dps-engine/references/ui-brand.md
@~/.claude/dps-engine/references/gate-prompts.md
</execution_context>

<context>
$ARGUMENTS
</context>

<process>
Execute end-to-end.
</process>
