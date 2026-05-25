<!-- GSD:project-start source:PROJECT.md -->
## Project

**Data-Pro-Skill v2**

A multi-harness meta-prompt for market research data analysis. Transforms raw quantitative and qualitative research data into dense, Tufte-style analytical documents. Built as a document-driven system where each command anchors context for the next — `/setup` generates the quantitative manifesto, `/cross` slices variables, `/inject-open` weaves qualitative findings into existing segments, and `/export` consolidates everything into a clean Markdown document ready for Quarto/LaTeX/PDF.

Works across AI harnesses (OpenCode, Gemini, Codex, Hermes, OpenClaw, Claude) — not locked to any single runtime.

**Core Value:** One prompt that takes raw market research data and produces a publication-ready analytical document — quantitative first, qualitative as layered extensions — with zero prose fluff, maximum data density, and full reproducibility across any AI harness.

### Constraints

- **Multi-harness**: Must work on OpenCode, Gemini, Codex, Hermes, OpenClaw, and Claude — avoid XML tags, use YAML frontmatter and pure Markdown
- **Document-driven**: First output (`/setup`) must anchor all sequential analysis — no analysis can contradict established metrics
- **Quant-first**: Quantitative pipeline is the spine; qualitative is layered on top, not parallel
- **Single-analyst**: Designed for individual researchers, not teams
<!-- GSD:project-end -->

<!-- GSD:stack-start source:STACK.md -->
## Technology Stack

Technology stack not yet documented. Will populate after codebase mapping or first phase.
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
