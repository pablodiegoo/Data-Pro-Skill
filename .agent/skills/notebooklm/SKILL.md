---
name: notebooklm
description: Use this skill when the user wants to interact with Google NotebookLM (notebooklm.google.com). Triggers on requests to query notebooks, search documents, add sources (URLs, GDrive, PDFs), generate audio podcasts/videos from documents, share notebooks, or manage the NotebookLM library. Use this skill for source-grounded answers without hallucination.
---

# NotebookLM Assistant Skill

You have native Model Context Protocol (MCP) tools available to interact directly with the user's Google NotebookLM account. There is no need to run local python scripts or launch browsers manually—the `notebooklm-mcp` server handles everything natively.

## Workflow

1. **Verify Connection**: You should already have access to tools starting with `notebook_`, `source_`, `research_`, `studio_`, etc. If any of these throw an authentication error (`401 Unauthorized`, `Invalid CSRF`), prompt the user to open their terminal and run `nlm login` to re-authenticate. DO NOT try to fix auth yourself.
2. **Understand the Goal**: Identify what the user wants to do: query an existing notebook, add sources, or generate artifacts (like audio overviews).
3. **Execute via Native Tools**: Call the appropriate MCP tools directly.

## Detailed Tool Usage

To avoid cluttering your context, detailed lists of tools and their specific parameters have been moved to reference files. Read these **only** when you need them.

- **Available Tools & Capabilities**: Read `references/mcp_tools.md` for a complete mapping of all 29 tools available to you (CRUD for notebooks, sources, notes, sharing, and studio artifacts). This includes important warnings about operations that require `confirm=True`.
- **Query Best Practices**: Read `references/best_practices.md` if the user wants you to ask a question to a notebook via `notebook_query`. It contains critical instructions on how to handle NotebookLM's grounded responses and when to ask follow-up questions to synthesize a complete answer.

## Key Principles

- **Confirmation Required**: Destructive actions (`notebook_delete`, `source_delete`) and generative actions (`studio_create`, `source_sync_drive`) require you to pass `confirm=True`. You must get explicit user consent before doing this.
- **Asynchronous Work**: Actions like `research_start` and `studio_create` run in the background. You must poll `research_status` or `studio_status` to determine when they are complete.
- **Follow-ups Are Mandatory**: When using `notebook_query`, NotebookLM may provide truncated or narrowly-focused answers based *only* on the sources. Check if "Is that ALL you need to know?" applies, and proactively query again to fill gaps before answering the user.

## Important Note

This skill replaces the legacy Python-based `run.py` wrapper. If you see old references to `scripts/run.py` or `auth_manager.py` in your history, ignore them. You are dealing with native MCP tools now.
