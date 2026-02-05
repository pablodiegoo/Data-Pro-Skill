---
description: "Scans the project for context, data sources, and industry background."
---

# Context Bootstrap Workflow

This workflow focuses on absorbing the project's background and identifying its technical requirements.

## Step 1: File Inventory
1.  Use `list_dir` on the project root and `db/` to identify available data.
2.  Search for keywords like "Brief", "OS", "Proposta", or "Escopo" using `find_by_name`.

## Step 2: Content Analysis
1.  Read the main proposal/brief file.
2.  Extract:
    -   **Client Name**
    -   **Project Goal**
    -   **Key Deadlines**
    -   **Data Types** (CSV, Survey, etc.)

## Step 3: Population of .agent/references
1.  Create or update files in `.agent/references/` with the gathered info.
2.  Suggest specific mappings if a data dictionary is found (using `dictionary-mapper` if applicable).
