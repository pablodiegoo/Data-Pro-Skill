---
name: context-optimizer
description: "Decomposes large Markdown documentation into an optimized .agent context structure. Use this skill when: (1) Starting a new project with a large requirements document, (2) Migrating legacy docs to .agent structure, (3) Refactoring existing context files for better organization, (4) Converting PDFs or long READMEs into agent-friendly files, or (5) Optimizing context window usage by splitting monolithic docs into Tasks, Memories, Workflows, and References."
---

# Context Optimizer

This skill transforms large, monolithic documents into a modular `.agent/` folder structure optimized for AI agent context consumption. The goal is to minimize context window usage while maximizing information accessibility.

## Quick Reference

| Content Type | Destination | Naming Convention | When to Use |
|--------------|-------------|-------------------|-------------|
| **Core Rules/Facts** | `memory/` | `project_facts.md`, `conventions.md` | Immutable truths, constraints, standards |
| **Processes/How-To** | `workflows/` | `deploy.md`, `review.md` | Step-by-step procedures (turbo-enabled) |
| **Tasks/Plans** | `tasks/` | `backlog.md`, `sprint.md` | Active work items, implementation plans |
| **Reference Docs** | `references/` | `api_docs.md`, `schema.md` | Large docs loaded on-demand |
| **Skills** | `skills/` | `<skill-name>/SKILL.md` | Reusable capabilities with scripts |

## Workflow

### Phase 1: Analyze Source Document

Before splitting, understand the document's structure:

```bash
# Preview structure without splitting
head -100 <input_file> | grep -E "^#{1,3} "
```

Identify:
- **Hierarchical depth**: How many heading levels exist?
- **Content density**: Are sections long enough to justify separate files?
- **Semantic groupings**: Which sections belong together?

### Phase 2: Decompose with Script

Use the bundled script to split the document:

```bash
python3 .agent/skills/context-optimizer/scripts/decompose.py <input_file> -o <output_dir> [options]
```

#### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `input_file` | Large markdown/text file to split | Required |
| `-o, --output` | Output directory for chunks | `<input>_split/` |
| `-l, --level` | Header level to split by (1=`#`, 2=`##`) | `2` |
| `-r, --regex` | Custom regex pattern (group 1 = title) | Markdown headers |
| `--min` | Minimum lines per section | `3` |

#### Examples

```bash
# Split by ## (default)
python3 decompose.py project_spec.md -o .agent/temp_split

# Split by # (top-level only)
python3 decompose.py large_doc.md -o chunks -l 1

# Custom pattern (e.g., numbered sections)
python3 decompose.py report.md -r "^(\d+\.\s+.+)$" -o sections
```

**Output**: Creates numbered files (`01_section_name.md`, `02_...`) plus `00_INDEX.md` and `00_preamble.md`.

### Phase 3: Organize into .agent Structure

After decomposition, manually categorize each chunk:

```
.agent/
├── memory/                 # Persistent context (always loaded)
│   ├── user_global.md      # User preferences, patterns
│   ├── project_facts.md    # Tech stack, constraints, conventions
│   └── decisions.md        # ADRs, architectural decisions
│
├── workflows/              # Step-by-step procedures
│   ├── deploy.md           # Deployment process
│   ├── review.md           # Code review checklist
│   └── testing.md          # Testing procedures
│
├── tasks/                  # Active work items
│   ├── backlog.md          # Feature backlog
│   ├── current_sprint.md   # Active sprint items
│   └── implementation_plan.md  # Current implementation plan
│
├── references/             # On-demand documentation
│   ├── api_docs.md         # API specifications
│   ├── schema.md           # Database/data schemas
│   └── external_libs.md    # Third-party library docs
│
└── skills/                 # Reusable capabilities
    └── <skill-name>/
        └── SKILL.md
```

### Phase 4: Optimize Each File

For each categorized file, apply these optimizations:

#### Memory Files (High Priority)
- **Maximum size**: ~500 lines (always loaded)
- **Format**: Bullet points, tables, concise rules
- **Avoid**: Long explanations, examples (move to references)

#### Workflow Files
- **Format**: Numbered steps with clear actions
- **Include**: `// turbo` annotations for auto-runnable steps
- **Structure**: Prerequisites → Steps → Verification

#### Task Files
- **Format**: Checkbox lists (`[ ]`, `[/]`, `[x]`)
- **Include**: Priority, deadlines, dependencies
- **Update**: Mark items as in-progress/done during work

#### Reference Files
- **Maximum size**: Unlimited (loaded on-demand)
- **Include**: Table of contents for files > 100 lines
- **Add**: Grep patterns in SKILL.md for large files

### Phase 5: Cleanup

Remove temporary files and validate structure:

```bash
# Remove decomposition output
rm -rf .agent/temp_split

# Validate structure (optional)
find .agent -name "*.md" -exec wc -l {} \; | sort -n
```

## Decision Matrix

Use this matrix to decide where content belongs:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Is it a PROCESS/HOW-TO?                      │
│                              │                                  │
│              ┌───────────────┴───────────────┐                  │
│              ▼ YES                           ▼ NO               │
│     ┌────────────────┐              ┌────────────────┐          │
│     │   workflows/   │              │ Is it ACTIVE   │          │
│     │                │              │ work to track? │          │
│     └────────────────┘              └───────┬────────┘          │
│                                     ┌───────┴───────┐           │
│                                     ▼ YES           ▼ NO        │
│                              ┌──────────┐   ┌──────────────┐    │
│                              │  tasks/  │   │ Is it a RULE │    │
│                              │          │   │ or FACT?     │    │
│                              └──────────┘   └──────┬───────┘    │
│                                             ┌──────┴──────┐     │
│                                             ▼ YES         ▼ NO  │
│                                      ┌──────────┐  ┌──────────┐ │
│                                      │ memory/  │  │references/│ │
│                                      └──────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Best Practices

1. **Memory files are expensive** — Keep them under 500 lines total
2. **Use references for large docs** — They're loaded only when needed
3. **One concept per file** — Easier to update and search
4. **Add TOC to large files** — For files > 100 lines, include a table of contents
5. **Use consistent naming** — `snake_case.md` for all files
6. **Delete empty directories** — Don't keep placeholder folders

## Bundled Resources

| Resource | Purpose |
|----------|---------|
| `scripts/decompose.py` | Split markdown by headers or custom regex |
| `references/examples.md` | Real-world categorization examples and patterns |

## Related Skills

- **skill-creator**: For creating new skills from decomposed content
- **documentation-mastery**: For formatting the resulting markdown files
