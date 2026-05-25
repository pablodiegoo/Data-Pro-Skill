# Phase 2: Quantitative Analysis — Research

**Researched:** 2026-05-25
**Domain:** Meta-prompt engineering (Markdown prompt for LLM statistical analysis)
**Confidence:** HIGH — domain is well-understood; all assets exist in repo; no external dependencies

## Summary

Phase 2 adds five quantitative command sections to the existing SKILL.md (222 lines, agent loop and `/dps-setup` already built in Phase 1). The additions are pure Markdown prompt text — no code, no packages, no runtime. Each command extends the established pattern: `## Command: /dps-{name}` → `### Execution Steps` → `### Output Format`.

The commands are: `/dps-clarify` (adaptive pre-analysis questions), `/dps-plan` (checklist of suggested crosses), `/dps-cross [VarX] x [VarY]` (Tufte crosstab with auto-selected statistical test), `/dps-execute` (autonomous multi-cross analysis), and `/dps-mode:quant` (Statistician persona activation). All leverage the existing invisible agent loop (Statistician → Critic → Tufte Designer) and reference the Statistical Test Selector Matrix already defined in `agents/agent-statistician.md`.

**Primary recommendation:** Follow the `/dps-setup` pattern precisely — each command is a self-contained Markdown section with Execution Steps referencing the agent loop stages and an Output Format showing the expected Tufte structure. No new architecture; just new prompt instructions.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Adaptive question generation | LLM Context | — | Single-tier meta-prompt; all logic runs in LLM inference. No client/server separation. |
| Statistical test selection | LLM Context | — | Matrix in agent-statistician.md consulted by LLM; no external computation. |
| Crosstab table generation | LLM Context | — | Tufte Designer formats output; all formatting is prompt-instructed Markdown. |
| Multi-cross autonomous execution | LLM Context | — | `/dps-execute` chains multiple agent loop invocations in a single LLM session. |
| Persona activation (`/dps-mode:quant`) | LLM Context | — | Alters agent loop behavior via prompt prefix; no runtime mode switching. |

**Note:** Data-Pro-Skill is a meta-prompt system — all components execute within a single LLM context window. The architectural tiers above are conceptual divisions within the prompt, not separate processes or services.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

1. **D-01:** `/dps-clarify` uses adaptive open-ended questions — the AI generates contextualized questions based on provided data, not a fixed template
2. **D-02:** Five reference categories (not rigid template): (1) business objective, (2) stakeholder hypotheses, (3) expected surprises, (4) dependent decisions, (5) data quality/reliability
3. **D-03:** Maximum 5 questions, minimum 3, adapted to specific context
4. **D-04:** The Statistician agent decides the statistical test based on observed data
5. **D-05:** The Statistical Test Selector Matrix in `agents/agent-statistician.md` serves as a reference guide, not a rigid rule
6. **D-06:** The Critic agent validates test selection (assumptions met? sufficient statistical power?)
7. **D-07:** `/dps-plan` generates a checklist of suggested analyses — it is a suggestion, not a requirement
8. **D-08:** `/dps-execute` runs autonomous analysis without depending on `/dps-plan` — usable standalone
9. **D-09:** If `/dps-plan` was previously run, `/dps-execute` references it as a starting point but adapts to actual data
10. Inherited from Phase 1: `/dps-` prefix, zero XML tags, Tufte output (N + % + margin notes), DPS naming convention, constitution.md dependency

### the agent's Discretion

The planner may choose:
- Exact section ordering within SKILL.md for the new commands (must follow Phase 1 pattern)
- Detailed structure of `/dps-plan` checklist (must be a checklist, not narrative)
- Specific examples embedded in `/dps-clarify` to guide the AI in generating adaptive questions

### Deferred Ideas (OUT OF SCOPE)

- Advanced statistical tests (multiple regression, MANOVA, factor analysis) — future phase or specialized mode
- Automatic distribution visualization — Phase 4 (export)
- Integration with Python/R for precise statistical calculations — out of scope for pure meta-prompt
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CLAR-01 | `/clarify` runs 3-5 provocative questions about business goals and hypotheses before touching data | §Adaptive Question Generation Pattern |
| PLAN-01 | `/plan` outputs an analytical plan specifying which tests/crosses will be run and why | §Checklist Output Format |
| CROSS-01 | `/cross [VarX] x [VarY]` produces dense Tufte-style crosstab tables with margin notes | §Crosstab Command Pattern |
| CROSS-02 | Tables must include N, volumetrics, and conclusion in headers | Inherited from Phase 1 Tufte rules (already in SKILL.md §Table Format) |
| EXEC-01 | `/execute` runs the planned analysis and renders output in Tufte style | §Autonomous Execution Pattern |
| MODE-01 | `/mode:quant` activates statistical persona — correlations, crosstabs, NPS, Churn, CSAT | §Mode Activation Pattern |

**Discrepancy noted:** REQUIREMENTS.md traceability table maps MODE-01 to Phase 3, but both ROADMAP.md (line 40) and CONTEXT.md (line 15) place it in Phase 2. Phase 2 boundary takes precedence — `/dps-mode:quant` is in scope.
</phase_requirements>

## Standard Stack

### Core
| Component | Purpose | Why Standard |
|-----------|---------|--------------|
| Markdown | Prompt format and output format | Harness-agnostic (works on all 6 target platforms); no XML reliance |
| YAML frontmatter | Structured data headers in output | Already used in `/dps-setup` manifesto; parseable by downstream tools |
| `agents/agent-statistician.md` | Statistical test selection reference | Already exists in repo; contains the complete Test Selector Matrix |
| `agents/agent-critic.md` | Test validation and bias audit | Already exists; validates Statistician choices per D-06 |
| `constitution.md` | Statistical rigor enforcement | Already exists; Critic enforces all 6 articles on output |

### Supporting
| Component | Purpose | When to Use |
|-----------|---------|-------------|
| `agents/agent-tufte-designer.md` | Output formatting rules | Every user-visible output (already integrated in agent loop) |

### No External Dependencies

This is a **meta-prompt project**. All "implementation" is Markdown prompt text embedded in SKILL.md. There are no packages to install, no runtimes to configure, no APIs to call. The AI harness reading SKILL.md is the runtime.

**Installation:** Not applicable — no packages, no `npm install`, no `pip install`.

## Package Legitimacy Audit

No external packages — meta-prompt project. Audit section intentionally empty.

## Architecture Patterns

### System Architecture Diagram

```
USER COMMAND (/dps-clarify, /dps-cross, /dps-plan, /dps-execute, /dps-mode:quant)
        │
        ▼
┌───────────────────────────────────────────────┐
│  SKILL.md — Meta-Prompt Context               │
│                                               │
│  ┌─────────────────────────────────────┐      │
│  │ /dps-clarify                         │      │
│  │  • Pre-analysis: no agent loop       │      │
│  │  • Inspect data → generate questions │      │
│  │  • Output: numbered list (3-5 items) │      │
│  └─────────────────────────────────────┘      │
│                                               │
│  ┌─────────────────────────────────────┐      │
│  │ /dps-plan                            │      │
│  │  • Statistician: scan segments       │      │
│  │  • Recommend crosses + tests        │      │
│  │  • Output: checklist table            │      │
│  └─────────────────────────────────────┘      │
│                                               │
│  ┌─────────────────────────────────────┐      │
│  │ /dps-cross [VarX] x [VarY]           │      │
│  │  • Stage 1: Statistician → test      │      │
│  │  • Stage 2: Critic → validate        │      │
│  │  • Stage 3: Tufte Designer → table   │      │
│  │  • Output: Tufte crosstab + margin   │      │
│  └─────────────────────────────────────┘      │
│                                               │
│  ┌─────────────────────────────────────┐      │
│  │ /dps-execute                          │      │
│  │  • Reads manifesto segments           │      │
│  │  • Chains multiple /dps-cross calls   │      │
│  │  • Agent loop per cross               │      │
│  │  • Output: consolidated report        │      │
│  └─────────────────────────────────────┘      │
│                                               │
│  ┌─────────────────────────────────────┐      │
│  │ /dps-mode:quant                       │      │
│  │  • Modifies agent loop behavior       │      │
│  │  • Statistician: deeper numerics      │      │
│  │  • Affects all subsequent commands    │      │
│  └─────────────────────────────────────┘      │
│                                               │
│  Shared:                                     │
│  • constitution.md — enforced by Critic       │
│  • agent-statistician.md — Test Matrix        │
│  • agent-critic.md — 6 audit dimensions       │
│  • agent-tufte-designer.md — output rules     │
└───────────────────────────────────────────────┘
```

### Recommended Project Structure

```
SKILL.md                        # ← ALL new command sections added here
├── ## Internal Agent Loop      # Unchanged from Phase 1
├── ## Command: /dps-setup      # Phase 1 (unchanged)
├── ## Command: /dps-clarify    # NEW — Phase 2
├── ## Command: /dps-plan       # NEW — Phase 2
├── ## Command: /dps-cross      # NEW — replaces stub; Phase 2
├── ## Command: /dps-execute    # NEW — Phase 2
├── ## Command Reference        # Updated with new statuses
├── ## Modes                    # Existing section
│   ├── ### /dps-mode:quant     # NEW — Phase 2 (full implementation)
│   ├── ### /dps-mode:quali     # Phase 3 (stub)
│   └── ### /dps-mode:strategy  # Phase 4 (stub)
└── ## Tufte Output Formatting Rules  # Unchanged
```

### Pattern 1: Command Section Structure (Established Phase 1 Pattern)

**What:** Every command is a Markdown `##` section with three subsections.

**When to use:** For every new command added to SKILL.md.

**Template:**
```markdown
## Command: /dps-{name} — {one-line purpose}

**Purpose:** {what it does, when to use it}

### Execution Steps

1. {step 1 — which agent runs, what it does}
2. {step 2 — next stage}
3. {step 3 — final stage / output}

### Output Format

```markdown
{expected output structure with placeholders}
```
```

**Source:** Established in Phase 1 `/dps-setup` section (SKILL.md lines 77-123).

### Pattern 2: Adaptive Question Generation (`/dps-clarify`)

**What:** Prompt instructions that guide the LLM to generate data-specific business questions rather than a fixed template. The LLM inspects the provided data, identifies gaps and ambiguities, then generates 3-5 questions drawn from the 5 reference categories.

**When to use:** `/dps-clarify` — always first command before any quantitative analysis.

**Key prompt design elements (from D-01, D-02, D-03):**

1. **Data inspection first:** Instruct LLM to scan data for segment names, metric values, variable types, sample size before generating questions
2. **Category menu, not checklist:** The 5 categories are a palette — the LLM selects which are most relevant to the specific data. Not all 5 categories must be used every time.
3. **Specificity rule:** Every question must reference concrete data elements. "What is your business objective?" is forbidden. "Segment C shows NPS -22 with N=145 — what hypothesis do stakeholders have about the drivers of this dissatisfaction?" is correct.
4. **Provocative framing:** Questions should surface assumptions and tensions. "Your data shows no correlation between satisfaction and loyalty (r=0.08, p=0.42). Does this surprise your stakeholders? What alternative metrics do they track for retention?"
5. **Output format:** Numbered list. Each question preceded by its (implicit) category. 3-5 items total.

**Source:** D-01, D-02, D-03 from CONTEXT.md.

### Pattern 3: Statistical Test Selection for Crosstabs (`/dps-cross`)

**What:** The `/dps-cross` command delegates test selection to the Statistician agent, which consults the Test Selector Matrix in `agents/agent-statistician.md`. The Critic then validates the choice. This is a two-stage gated decision, not a single lookup.

**When to use:** `/dps-cross [VarX] x [VarY]` — user specifies two variables.

**Flow:**
1. Statistician determines `VarX` and `VarY` data types (categorical 2-group, categorical 3+ group, continuous)
2. Statistician consults Test Selector Matrix for recommended test
3. Statistician checks assumptions: N ≥ 30 per group for parametric; normality for t-test/ANOVA; expected cell frequencies for χ²
4. If parametric assumptions violated → fall back to non-parametric (Mann-Whitney U, Kruskal-Wallis, Spearman's ρ)
5. Critic validates: right test for data type? assumptions met? Constitution Article 5 (N ≥ 30 for parametric) enforced?
6. Tufte Designer formats: table with N, %, test statistic (χ² or t or F or r with df and p-value), margin note

**Source:** D-04, D-05, D-06 from CONTEXT.md; Test Selector Matrix in agent-statistician.md lines 30-37.

### Pattern 4: Checklist Output for `/dps-plan`

**What:** A structured Markdown table of suggested analyses — not narrative, not prescriptive. Each row is a recommended cross with rationale.

**When to use:** `/dps-plan` — user wants suggested analysis roadmap before committing to execution.

**Output format (recommended):**
```markdown
## Plano Analítico Sugerido

> **⚠️ Este plano é uma sugestão.** `/dps-execute` pode ser executado independentemente
> e adaptará os testes às características reais dos dados. Use como ponto de partida.

**Pré-requisitos:** Manifesto `/dps-setup` deve existir (segmentos definidos).

| # | Cruzamento | Variáveis | Teste Recomendado | Justificativa |
|---|-----------|-----------|-------------------|---------------|
| 1 | {Seg A} × {Metric} | {var1}, {var2} | {χ² / t-test / ANOVA} | {why this cross is relevant — 1 sentence} |
| 2 | {Seg B} × {Metric} | {var1}, {var2} | {test} | {justification} |

**Próximo passo:** Execute `/dps-cross {VarX} x {VarY}` para qualquer cruzamento acima,
ou `/dps-execute` para rodar todos os cruzamentos sugeridos de forma autônoma.
```

**Source:** D-07, D-08, D-09 from CONTEXT.md.

### Pattern 5: Autonomous Multi-Cross Execution (`/dps-execute`)

**What:** `/dps-execute` autonomously identifies crosses worth running (from manifesto segments and available variables), runs each through the agent loop, and produces a consolidated Tufte report. Independent from `/dps-plan` but can reference it if it exists.

**When to use:** `/dps-execute` — user wants full analysis without manually specifying each cross.

**Flow:**
1. Read `/dps-setup` manifesto for segments
2. If `/dps-plan` output exists, scan as starting point; otherwise derive crosses from segment × metric combinations
3. For each cross: run Statistician → Critic → Tufte Designer
4. Consolidate all crosstabs into a single Tufte report
5. Include overall summary with key findings across all crosses

**Source:** D-08, D-09 from CONTEXT.md.

### Anti-Patterns to Avoid

- **Fixed template for `/dps-clarify`:** A hardcoded list of 5 questions violates D-01. The prompt must instruct the LLM to generate questions dynamically based on the data provided.
- **Narrative plan for `/dps-plan`:** Violates D-07 ("checklist, not narrative"). Output must be a table of crosses, not paragraphs.
- **Test selection as hard lookup:** Violates D-05 ("guide, not rigid rule"). The prompt should say "consult the matrix" not "apply the matrix rule."
- **`/dps-execute` requiring `/dps-plan`:** Violates D-08. Both commands must work independently.
- **Duplicating agent logic inline:** Violates Phase 1 pattern ("agents referenced by name — never duplicated inline"). Each command references agent files, does not repeat their instructions.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Statistical test selection logic | Inline decision tree in command prompt | Reference `agents/agent-statistician.md` Test Selector Matrix | Matrix already exists, tested, and covers all Phase 2 test types |
| Data validation rules | Custom validation instructions | `constitution.md` Article enforcement via Critic | Already defines exact checks (MoE, N≥30, % sums); duplicating creates divergence risk |
| Output formatting rules | New formatting instructions per command | `agents/agent-tufte-designer.md` | Single source of truth for Tufte output; already enforced by Designer stage |
| Adaptive question heuristics | Generic "ask good questions" instruction | Category-anchored specificity rules (Pattern 2 above) | Without specificity rules, LLMs generate generic questions like "What is your business goal?" |

**Key insight:** Every Phase 2 command is a thin orchestration layer over existing agent files. The commands specify what to do and in what order; the agents specify how to do it. Do not inline agent logic into command sections — reference the agent files.

## Runtime State Inventory

**Phase type:** Greenfield addition to SKILL.md (no rename, no refactor, no migration). **Omitted** — no runtime state to inventory.

## Common Pitfalls

### Pitfall 1: Over-specifying the Test Selector

**What goes wrong:** Writing `/dps-cross` to rigidly map data types to tests (e.g., "if 2 categorical, ALWAYS use χ²") instead of instructing the Statistician to consult the matrix and exercise judgment.

**Why it happens:** Easier to write deterministic mapping than to trust agent judgment. But this is a meta-prompt — the LLM is the executor, and rigid mappings miss edge cases (small cells, non-normal distributions, unequal variances).

**How to avoid:** Write the Execution Steps as: "Statistician: determine data type of VarX and VarY. Consult the Statistical Test Selector Matrix in agent-statistician.md for the recommended test. Verify assumptions (sample size per group, normality, equal variance). Fall back to non-parametric equivalent if parametric assumptions are violated."

**Warning signs:** Command text contains if/else logic "if categorical then χ² else if continuous then t-test" — this is a flag, not a rule.

### Pitfall 2: Generic Clarify Questions

**What goes wrong:** `/dps-clarify` produces template questions like "What is your business objective?" or "Who is your target audience?" regardless of the data provided.

**Why it happens:** The prompt doesn't explicitly instruct the LLM to inspect the data before generating questions; the LLM defaults to generic consulting-firm questions.

**How to avoid:** The Execution Steps must start with: "Step 1 — Inspect the provided data. Identify segments, metrics, sample size, variable names, and any notable patterns." Only after inspection should the prompt say "Step 2 — Generate 3-5 questions that are specific to this data." Include concrete examples in the prompt that demonstrate specificity.

**Warning signs:** The clarify output contains zero references to specific data elements (segment names, N values, metric names, variable types).

### Pitfall 3: Checklist as Narrative

**What goes wrong:** `/dps-plan` outputs paragraphs like "I recommend running a chi-square test between Segment A and CSAT to check for independence..." instead of a structured checklist table.

**Why it happens:** LLMs default to prose. Without explicit output format constraints, they write paragraphs.

**How to avoid:** The Output Format section of `/dps-plan` MUST show the exact table structure with placeholder values. Include the instruction: "Output ONLY the table. No introductory paragraphs. No concluding remarks."

**Warning signs:** Plan output contains sentences before or after the checklist table.

## Code Examples

### `/dps-clarify` Prompt Pattern

```markdown
## Command: /dps-clarify — Adaptive Business Hypothesis Questions

**Purpose:** Generate 3-5 provocative, data-specific questions about business goals,
stakeholder hypotheses, and analytical assumptions BEFORE any quantitative analysis.
Ensures analysis is hypothesis-driven, not fishing.

### Execution Steps

1. **Inspect the data.** Scan all provided data for: segment names, variable names,
   sample size (N), metric values (NPS, CSAT, churn rate, etc.), and any notable
   patterns (outliers, extreme values, unexpected distributions).

2. **Select relevant categories.** From the 5 reference categories below, select
   the 3-5 most relevant to this specific data:

   | # | Category | What to Probe |
   |---|----------|--------------|
   | 1 | Business Objective | What decision will this analysis inform? |
   | 2 | Stakeholder Hypotheses | What do decision-makers BELIEVE before seeing data? |
   | 3 | Expected Surprises | Where do stakeholders expect the data to challenge assumptions? |
   | 4 | Dependent Decisions | What budget/strategy/timeline decision hinges on this analysis? |
   | 5 | Data Quality & Reliability | Collection method, timing, known biases, missing segments |

3. **Generate questions.** For each selected category, craft ONE question that:
   - References CONCRETE data elements (segment names, N values, metric values)
   - Is provocative — challenges assumptions, not confirms them
   - Cannot be answered with a yes/no
   - Would change the analysis approach depending on the answer

   **Forbidden:** Generic questions ("What is your business objective?")
   **Required:** Data-specific questions ("Segment C (B2B, N=145) shows NPS -22
   while Segment A (B2C, N=520) shows NPS +41. What hypothesis do stakeholders
   have about the B2B product experience driving this gap?")

4. **Output questions.** Numbered 1-{3..5}. No preamble. No closing remarks.

### Output Format

1. [Category 1 — e.g., Business Objective] {Data-specific provocative question}
2. [Category 2 — e.g., Stakeholder Hypotheses] {Data-specific provocative question}
3. [Category 3 — e.g., Data Quality] {Data-specific provocative question}
```
```

### `/dps-cross` Prompt Pattern

```markdown
## Command: /dps-cross [VarX] x [VarY] — Tufte Crosstab with Statistical Test

**Purpose:** Produce a dense, Tufte-style crosstab table comparing two variables with
automatic statistical test selection, significance reporting, and interpretive margin notes.

### Execution Steps

1. **Run the invisible agent loop (Stage 1 → Stage 2 → Stage 3).**

   **Stage 1 — Statistician:**
   - Determine data type of VarX and VarY (categorical 2-group, categorical 3+ group, continuous)
   - Consult the Statistical Test Selector Matrix in `agents/agent-statistician.md`
   - Select the appropriate test based on observed data characteristics
   - Check test assumptions: sample size per group (N ≥ 30 for parametric per constitution.md Article 5),
     normality, homogeneity of variance, expected cell frequencies for χ²
   - Fall back to non-parametric equivalent if assumptions are violated
   - Compute the test statistic, degrees of freedom, p-value, and effect size
   - Compute all percentages with margin of error per constitution.md Article 1

   **Stage 2 — Critic:**
   - Validate test selection: right test for data type?
   - Verify all constitution.md articles are met
   - Flag: small samples, spurious correlations, overgeneralization risks
   - If test is invalid → return to Statistician with correction

   **Stage 3 — Tufte Designer:**
   - Format as dense crosstab table with header containing conclusion
   - Include N, %, test statistic, and margin note
   - Zero prose fluff — go straight to the data

2. **Produce output in this exact structure:**

### Output Format

```markdown
## {VarX} × {VarY} — {Key Finding in Header}

| {VarX} | N | {VarY Category A} | {VarY Category B} | Teste |
| :--- | :--: | :--: | :--: | :--- |
| {Group 1} | {n} | {n} ({pct}% ±{moe}%) | {n} ({pct}% ±{moe}%) | — |
| {Group 2} | {n} | {n} ({pct}% ±{moe}%) | {n} ({pct}% ±{moe}%) | — |
| **Total** | **{N}** | **{n} ({pct}%)** | **{n} ({pct}%)** | {test_statistic}, p={value} |

> **Nota de Margem:** {1-3 sentence sharp interpretation — "so what?" for this cross.
> Never repeat what the table already shows. Connect to business implications.}
```
```
```

### `/dps-plan` Prompt Pattern

```markdown
## Command: /dps-plan — Suggested Analytical Plan

**Purpose:** Generate a checklist of recommended crosstabs and statistical tests
based on the segments defined in the `/dps-setup` manifesto. This is a SUGGESTION —
`/dps-execute` works independently and may adapt based on actual data characteristics.

### Execution Steps

1. **Read the manifesto.** Load the YAML frontmatter and segment matrix from the
   `/dps-setup` output. Extract: segment names, tracked metrics, sample size per segment.

2. **Statistician: recommend crosses.** For each segment × metric combination:
   - Determine data types
   - Consult the Test Selector Matrix in `agents/agent-statistician.md`
   - Recommend the appropriate test

3. **Generate checklist.** Output ONLY the table. No introductory paragraphs. No
   concluding remarks. The table IS the output.

### Output Format

```markdown
## Plano Analítico Sugerido

> **⚠️ Sugestão — não requisito.** `/dps-execute` pode ser executado
> independentemente e adaptará os testes aos dados reais.

**Pré-requisitos:** `/dps-setup` deve ter sido executado.

| # | Cruzamento | Variáveis | Teste Recomendado | Justificativa |
|---|-----------|-----------|-------------------|---------------|
| 1 | {Segment A} × {Metric 1} | {seg_var}, {metric_var} | {test} | {1-sentence rationale} |
| 2 | {Segment B} × {Metric 1} | {seg_var}, {metric_var} | {test} | {1-sentence rationale} |
```
```
```

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Manual validation across 6 target harnesses |
| Config file | None — meta-prompt, no test runner |
| Quick run command | Not applicable (manual testing) |
| Full suite command | Not applicable (manual testing) |

**Nature of validation:** Data-Pro-Skill is a prompt, not software. "Tests" consist of running the SKILL.md meta-prompt on each of the 6 target AI harnesses (OpenCode, Gemini, Codex, Hermes, OpenClaw, Claude) with sample data and verifying:
1. Commands execute without errors
2. Output follows Tufte formatting rules
3. Statistical tests are correctly selected and reported
4. Constitution articles are enforced (no fluff, MoE present, N≥30 checks)

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Verification Method | File Exists? |
|--------|----------|-----------|---------------------|-------------|
| CLAR-01 | `/dps-clarify` generates 3-5 data-specific questions | Manual | Run on sample data; verify questions reference data elements; verify 3-5 count; verify no generic questions | ❌ Wave 0 |
| PLAN-01 | `/dps-plan` outputs checklist table | Manual | Run after `/dps-setup`; verify output is a table with justified crosses; verify no narrative prose | ❌ Wave 0 |
| CROSS-01 | `/dps-cross` produces Tufte crosstab with test statistic | Manual | Run with known variable pair; verify N column, % with MoE, test statistic, margin note present | ❌ Wave 0 |
| CROSS-02 | Tables include N, volumetrics, conclusion in headers | Manual | Verify table headers include conclusion; verify N column exists; verify % column | ❌ Wave 0 |
| EXEC-01 | `/dps-execute` runs autonomous multi-cross analysis | Manual | Run after `/dps-setup`; verify multiple crosstabs produced; verify Tufte formatting on all | ❌ Wave 0 |
| MODE-01 | `/dps-mode:quant` activates statistical persona | Manual | Run `/dps-mode:quant` then `/dps-cross`; verify deeper statistical commentary in output | ❌ Wave 0 |

### Sampling Rate

- **Per section written:** Visual review of prompt text for pattern compliance
- **Post-implementation:** Run all commands on 1 harness (OpenCode) with sample data
- **Phase gate:** All 6 requirements verified on at least 1 harness before `/gsd-verify-work`

### Wave 0 Gaps

- All 6 requirements lack verification infrastructure — meta-prompt project with no automated test framework
- Manual validation plan must be created (walking skeleton: provide sample CSV data, run each command, collect outputs)

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | No | Not applicable — single-user meta-prompt |
| V3 Session Management | No | Not applicable — stateless LLM invocation |
| V4 Access Control | No | Not applicable — no multi-user system |
| V5 Input Validation | Yes (limited) | Prompt should instruct LLM to validate data completeness, type correctness, and flag suspicious inputs before analysis. Already handled by Statistician stage. |
| V6 Cryptography | No | Not applicable — no secrets or sensitive data at rest |

### Known Threat Patterns for Meta-Prompt

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Prompt injection via user-provided data | Spoofing / Tampering | The LLM reading SKILL.md processes user-provided data as content, not instructions. The prompt should clearly delimit "data to analyze" from "command to execute." User data should be treated as input, not extension of the prompt. |
| Statistical hallucination (LLM fabricates test statistics) | Tampering | Constitution enforcement: all test statistics must be derivable from reported data. Critic cross-checks test statistic against N and percentages. Flag any claim that cannot be reconstructed from the data. |
| Harness-specific syntax leakage | Information Disclosure | Enforced by HARN-01 requirement: zero XML tags. Pure Markdown only. All 6 target harnesses support Markdown. |

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Hardcoded statistical decision trees in prompts | Reference-based test selection (agent reads external matrix file) | Phase 1 architecture | Enables updating test logic without changing command prompts |
| Fixed-template clarify questions | Adaptive, data-inspection-first question generation | Phase 2 implementation | Questions become specific to the analysis, not generic consulting scripts |
| Narrative analytical plans | Checklist table format | Phase 2 implementation | Reduces "plan fatigue" — user scans table, picks crosses, executes |

**Deprecated/outdated:** Nothing in this phase removes existing functionality. All Phase 1 content (constitution.md, agent files, `/dps-setup`, Tufte rules) is preserved and referenced.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The LLM runtime can perform statistical test computation (χ², t-test, ANOVA, correlation) without external tools | Standard Stack, `/dps-cross` Pattern | LOW — modern LLMs (Claude 3.5, GPT-4, Gemini 2) reliably compute standard test statistics. If a harness cannot, the command will produce textually plausible but numerically wrong statistics. |
| A2 | The Statistical Test Selector Matrix in agent-statistician.md is sufficient for all test selection decisions in Phase 2 | `/dps-cross` Pattern | LOW — the matrix covers all Phase 2 scope (χ², Fisher's exact, t-test, Mann-Whitney, ANOVA, Kruskal-Wallis, Pearson's r, Spearman's ρ, linear regression). Advanced tests (MANOVA, factor analysis) are deferred to Phase 4. |
| A3 | The Critic agent can mechanically enforce constitution articles via prompt instructions alone | Security Domain | LOW — Critic enforcement is prompt text, not code. A deterministic rules engine would be more reliable, but LLMs at current capability levels can perform these checks on output text. |
| A4 | All 6 target harnesses (OpenCode, Gemini, Codex, Hermes, OpenClaw, Claude) process Markdown YAML frontmatter consistently | Standard Stack | MEDIUM — some harnesses may handle YAML frontmatter differently in output mode. The prompt uses YAML in `Output Format` sections, which the LLM generates as plain text — not parsed YAML. Risk is limited to display formatting differences. |

## Open Questions

1. **Should `/dps-clarify` use the agent loop or bypass it?**
   - What we know: Clarify is pre-analysis — it generates questions before any calculation. No statistical validation needed.
   - What's unclear: Should the Critic review the clarify questions for bias/provocativeness? Does the Tufte Designer format the questions (they're a numbered list, not tables)?
   - Recommendation: Bypass the agent loop for `/dps-clarify`. Questions are conversational, not analytical output. The loop activates only for data-analysis commands (`/dps-cross`, `/dps-execute`). **the agent's Discretion** — planner decides.

2. **How does `/dps-execute` decide which crosses to run when no `/dps-plan` exists?**
   - What we know: It reads manifesto segments and creates segment × metric combinations. But how many? All combinations? Top-N by some heuristic?
   - What's unclear: The exact heuristic for prioritizing crosses (sample size? metric variance? user-provided hints?).
   - Recommendation: Run all segment × metric combinations from the manifesto as a default. Small manifests (3-5 segments, 2-3 metrics) produce ≤15 crosses — tractable for a single LLM invocation. Explicitly note in Execution Steps: "If more than 20 crosses would be generated, prioritize: (1) crosses with largest N per cell, (2) crosses where metrics show high variance between segments."

3. **Is `/dps-mode:quant` a toggle or a persistent mode?**
   - What we know: It "activates persona Estatístico Sênior para todas as operações quantitativas." But how does the LLM remember it's in quant mode across multiple commands?
   - What's unclear: LLMs are stateless — context resets between invocations. A mode toggle works within a single session but not across sessions. Should it be a prefix on every command instead (like `/dps-mode:quant /dps-cross...`)?
   - Recommendation: Document it as a session-scoped mode: "Once activated, all subsequent commands in this session operate in quant mode. The Statistician agent takes a more prominent role — deeper distribution analysis, explicit effect size reporting, and assumption diagnostics." If used as a command prefix, treat as single-command mode activation.

## Environment Availability

**Step 2.6: SKIPPED** — no external dependencies identified. Data-Pro-Skill is a Markdown meta-prompt. The runtime is any AI harness that can read a text file. No tools, no runtimes, no databases, no APIs.

## Sources

### Primary (HIGH confidence)
- `SKILL.md` (lines 1-222) — Established command pattern, agent loop, output formatting rules. Read directly from repo.
- `agents/agent-statistician.md` (lines 1-82) — Statistical Test Selector Matrix. Read directly from repo.
- `agents/agent-critic.md` (lines 1-81) — 6 audit dimensions. Read directly from repo.
- `agents/agent-tufte-designer.md` (lines 1-102) — Output formatting rules. Read directly from repo.
- `constitution.md` (lines 1-160) — 6 articles with enforcement rules. Read directly from repo.
- `CONTEXT.md` Phase 2 (lines 1-113) — User decisions D-01 through D-09. Read directly from repo.

### Secondary (MEDIUM confidence)
- None — all research was on existing project files; no external sources needed.

### Tertiary (LOW confidence)
- None.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no software stack; all components are existing project files verified by direct read
- Architecture: HIGH — pattern is established by Phase 1 `/dps-setup` implementation; new commands follow same structure
- Pitfalls: HIGH — prompt engineering patterns are well-understood; pitfalls are documented from known LLM behaviors
- Statistical methods: HIGH — Test Selector Matrix is already defined and validated in agent-statistician.md

**Research date:** 2026-05-25
**Valid until:** 2026-07-25 (stable domain — meta-prompt patterns don't change rapidly)
