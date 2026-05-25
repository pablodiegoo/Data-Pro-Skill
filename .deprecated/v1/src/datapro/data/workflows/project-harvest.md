---
description: "Loop-based investigation of project learnings. Scans scripts, methodologies, patterns, documentation, and architecture to harvest reusable knowledge into assets/harvest/."
---

# Project Harvest

This workflow runs at the **end of a project** (or periodically during long ones) to systematically extract every reusable insight. It runs in a **continuous loop**, scanning different dimensions until no new valuable learnings are found.

> [!IMPORTANT]
> This workflow runs in the **TARGET PROJECT**, not in Data-Pro-Skill. The output goes to `assets/harvest/`.

## Output Structure

```
assets/harvest/
├── overview.md                # Master document: summary of all learnings
├── scripts/                   # Candidate reusable scripts
│   ├── <descriptive_name>.py
│   └── README.md              # Why each script is valuable, what it does
├── database/                  # Proposed improvements for Data-Pro-Max database
│   ├── new_snippets.json      # New code snippets for datapro search/snippet
│   ├── new_analysis_types.csv # New analysis type entries
│   └── README.md              # What each file adds and why
├── rules/                     # Proposed new governance rules
│   └── <rule_name>.md
├── references/                # New reference documentation
│   └── <methodology>.md
├── workflows/                 # Proposed workflow improvements
│   └── <improvement>.md
└── memory/                    # Persistent project context worth preserving
    └── key_decisions.md
```

## Loop Execution

The workflow runs sequentially through **5 scan phases**, then loops back. Stop when a full cycle yields no new findings.

### Phase 1: Scripts Scan
**Goal**: Find reusable analytical code.
1. List ALL scripts in `scripts/`, `scripts/utils/`, `scripts/notebooks/`.
2. For each script, evaluate:
   - **Genericity**: Could this work in another project with different data?
   - **Novelty**: Does Data-Pro-Skill already have this capability?
   - **Quality**: Is the code clean, parameterized, well-documented?
3. For qualifying scripts:
   - Copy to `assets/harvest/scripts/` with a descriptive name.
   - Remove hardcoded paths, column names, and project-specific logic.
   - Add entry to `assets/harvest/scripts/README.md` with rationale.

### Phase 2: Methodology & Patterns Scan
**Goal**: Identify novel analytical approaches used in this project.
1. Scan analysis scripts for techniques not covered by our analytical skills (`survey-analytics`, `causal-inference`, `strategic-frameworks`, `machine-learning-lite`).
2. Check for:
   - New statistical methods or formulas.
   - Innovative data cleaning or transformation patterns.
   - Novel weighting or sampling approaches.
   - Creative visualization techniques.
3. For each finding:
   - Write a reference doc in `assets/harvest/references/`.
   - Include formulas, rationale, and example usage.

### Phase 3: Data & Database Scan
**Goal**: Identify improvements for `datapro` CLI intelligence.
1. Review what code snippets were created ad-hoc during the project.
2. Check `datapro search` and `datapro snippet` — were there gaps?
3. Propose new entries for:
   - `code_snippets.json` → `assets/harvest/database/new_snippets.json`
   - `analysis_types.csv` → `assets/harvest/database/new_analysis_types.csv`
   - `reasoning_rules.csv` → `assets/harvest/database/new_rules.csv`

### Phase 4: Documentation & Governance Scan
**Goal**: Find improvements for rules, references, and skill docs.
1. Review `.agent/rules/` — were any rules broken repeatedly? New rules needed?
2. Review `.agent/references/` — any gaps in documentation?
3. Review `.agent/memory/` — any decisions that should become permanent rules?
4. For each finding:
   - Write proposed rule/reference to `assets/harvest/rules/` or `assets/harvest/references/`.

### Phase 5: Architecture & Organization Scan
**Goal**: Evaluate folder structures, naming conventions, workflow efficiency.
1. Review the project's folder organization against `structure.json`.
2. Identify:
   - Patterns that worked well (promote as best practices).
   - Pain points in the workflow (propose improvements).
   - Missing conventions or unclear guidelines.
3. Write improvement proposals to `assets/harvest/workflows/`.

---

## Loop Control

```
REPEAT:
  run Phase 1 → Phase 5
  count = number of new items added this cycle
  IF count == 0:
    STOP → Write final overview.md
  ELSE:
    Log: "Cycle completed with {count} new findings. Running another pass."
    CONTINUE
```

## Finalization

After the loop ends:
1. Write/update `assets/harvest/overview.md` with:
   - Total findings per category.
   - Priority ranking (High/Medium/Low impact on Data-Pro-Skill).
   - Recommended absorption order.
2. Notify the user that the harvest is ready for `/project-evolution`.

---
> [!TIP]
> Focus on **quality over quantity**. One well-documented, generic script is worth more than ten project-specific ones.
