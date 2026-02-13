# Context Optimization Examples

This reference contains real-world examples of how to categorize and structure content from large documents.

## Table of Contents

1. [Project Specification Example](#project-specification-example)
2. [API Documentation Example](#api-documentation-example)
3. [Migration Guide Example](#migration-guide-example)
4. [Content Categorization Patterns](#content-categorization-patterns)

---

## Project Specification Example

### Source Document

A typical project specification document with 50+ pages containing:

```
# Project: E-commerce Platform
## 1. Executive Summary
## 2. Technical Requirements
## 3. Architecture
## 4. Database Schema
## 5. API Endpoints
## 6. Deployment Process
## 7. Timeline & Milestones
## 8. Team Structure
```

### Decomposition Strategy

**Step 1**: Split by `#` (level 1):
```bash
python3 decompose.py project_spec.md -o temp -l 1
```

**Step 2**: Categorize outputs:

| Source Section | Destination | Rationale |
|----------------|-------------|-----------|
| `01_executive_summary.md` | `memory/project_facts.md` | Core constraints, goals |
| `02_technical_requirements.md` | `memory/tech_stack.md` | Persistent tech decisions |
| `03_architecture.md` | `references/architecture.md` | On-demand reference |
| `04_database_schema.md` | `references/schema.md` | Large, on-demand |
| `05_api_endpoints.md` | `references/api_docs.md` | Large, on-demand |
| `06_deployment_process.md` | `workflows/deploy.md` | Step-by-step process |
| `07_timeline_milestones.md` | `tasks/milestones.md` | Trackable items |
| `08_team_structure.md` | `memory/team.md` | Persistent context |

---

## API Documentation Example

### Source Document

A large API documentation file (2000+ lines):

```markdown
# API Reference
## Authentication
### OAuth2 Flow
### API Keys
## Users
### GET /users
### POST /users
### PUT /users/{id}
## Products
### GET /products
### POST /products
...
```

### Decomposition Strategy

**Step 1**: Split by `##` (level 2) for major categories:
```bash
python3 decompose.py api_docs.md -o references/api -l 2
```

**Step 2**: Keep as separate reference files:

```
.agent/references/api/
├── 00_INDEX.md           # Auto-generated TOC
├── 01_authentication.md  # Auth methods
├── 02_users.md           # User endpoints
├── 03_products.md        # Product endpoints
└── ...
```

**Step 3**: Add grep hints to SKILL.md or parent reference:
```markdown
For specific endpoints, search with:
- `grep -r "POST /users" .agent/references/api/`
- `grep -r "authentication" .agent/references/api/`
```

---

## Migration Guide Example

### Source Document

A migration guide for upgrading a legacy system:

```markdown
# Migration Guide: v1 to v2
## Prerequisites
## Phase 1: Database Migration
## Phase 2: API Updates
## Phase 3: Frontend Changes
## Rollback Procedures
## Verification Steps
```

### Decomposition Strategy

This is primarily a **workflow** document. Options:

**Option A**: Keep as single workflow (if < 300 lines):
```bash
cp migration_guide.md .agent/workflows/migration_v1_to_v2.md
```

**Option B**: Split into phases (if large):
```bash
python3 decompose.py migration_guide.md -o temp -l 2
```

Then organize:
| Source | Destination |
|--------|-------------|
| `prerequisites.md` | `memory/migration_prereqs.md` |
| `phase_1_database.md` | `workflows/migrate_database.md` |
| `phase_2_api.md` | `workflows/migrate_api.md` |
| `phase_3_frontend.md` | `workflows/migrate_frontend.md` |
| `rollback_procedures.md` | `workflows/migration_rollback.md` |
| `verification_steps.md` | `workflows/migration_verify.md` |

---

## Content Categorization Patterns

### Pattern 1: Rules and Constraints → Memory

**Indicators**:
- "Must", "Always", "Never", "Required"
- Company policies, coding standards
- Architectural decisions (ADRs)

**Example**:
```markdown
# Before (in large doc)
All API endpoints must return JSON.
Authentication is required for all non-public endpoints.
Database transactions must use the Unit of Work pattern.

# After (.agent/memory/api_conventions.md)
## API Conventions
- All endpoints return JSON
- Non-public endpoints require authentication
- Use Unit of Work pattern for transactions
```

### Pattern 2: Step-by-Step Processes → Workflows

**Indicators**:
- Numbered steps
- "First... then... finally..."
- Prerequisites and verification sections

**Example**:
```markdown
# Before (in large doc)
## Deployment Process
1. Run tests locally
2. Create PR and wait for CI
3. Merge to main
4. Deploy with `./scripts/deploy.sh`
5. Verify health endpoints

# After (.agent/workflows/deploy.md)
---
description: Deploy application to production
---
## Prerequisites
- All tests passing locally
- PR approved and CI green

## Steps
// turbo
1. Run `./scripts/deploy.sh`

2. Verify health endpoints respond 200

3. Monitor logs for 5 minutes
```

### Pattern 3: Active Work Items → Tasks

**Indicators**:
- TODO, FIXME, WIP
- Deadlines, priorities
- Assignees, status tracking

**Example**:
```markdown
# Before (in large doc)
## TODO
- [ ] Fix login bug (P0)
- [ ] Add dark mode (P2)
- [ ] Write user docs (P1)

# After (.agent/tasks/backlog.md)
## Backlog

### P0 - Critical
- [ ] Fix login bug

### P1 - High
- [ ] Write user docs

### P2 - Medium
- [ ] Add dark mode
```

### Pattern 4: Large Reference Material → References

**Indicators**:
- Schemas, API specs, data dictionaries
- External library documentation
- Detailed examples (> 100 lines)

**Example**:
```markdown
# Keep large schemas in references
# .agent/references/schema.md

## Database Schema

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| email | VARCHAR(255) | Unique email |
...
```

---

## Anti-Patterns to Avoid

### ❌ Duplicating Content
Don't copy the same information to multiple files. Choose one canonical location.

### ❌ Over-Splitting
Don't create files with < 10 lines. Combine related small sections.

### ❌ Ignoring Hierarchy
Don't flatten a deeply nested document. Preserve logical groupings.

### ❌ Memory Bloat
Don't put everything in `memory/`. It's always loaded. Use `references/` for large docs.

### ❌ Missing Index
For directories with 5+ files, always create an `INDEX.md` with navigation links.
