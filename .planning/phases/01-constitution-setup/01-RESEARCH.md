# Phase 01: Constitution & Setup — Research

**Researched:** 2026-05-25
**Domain:** Meta-prompt architecture for market research data analysis (document-driven, multi-agent, multi-harness)
**Confidence:** HIGH

## Summary

Phase 1 establishes the foundation of Data-Pro-Skill v2: a meta-prompt that orchestrates invisible agents to produce Tufte-style analytical documents from raw market research data. The phase creates three deliverables: `constitution.md` (inegotiable statistical rigor rules), `SKILL.md` (main meta-prompt orchestrating agent loop and commands), and the `/dps-setup` command logic (generates quantitative manifesto anchoring all subsequent analysis).

This is a document-driven meta-prompt — not a software application. No compilation, no runtime, no packages. The "implementation" is prompt engineering: writing clear, constraint-rich Markdown instructions that any AI harness can execute. The core technical challenge is translating the existing agent architecture (already defined in `agents/`) into a single, portable SKILL.md that works identically across six different AI harnesses (OpenCode, Gemini, Codex, Hermes, OpenClaw, Claude).

**Primary recommendation:** Use the tufte-claude-skill SKILL.md structure as a pattern — YAML frontmatter for harness auto-detection, then sequential workflow instructions referencing separate files. Embed the invisible agent loop (Statistician → Critic → Tufte Designer) as mandatory internal processing steps before any user-visible output. Write the constitution in legal-article format (rule + rationale + violation consequence) for maximum enforceability by the Critic agent.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Agent loop orchestration | SKILL.md (prompt instructions) | — | The meta-prompt itself is the orchestrator — no runtime tier separation |
| Statistical validation | agent-statistician.md (read by AI at inference) | constitution.md (rules source) | Statistician agent applies the rules; constitution is the reference document |
| Bias/quality auditing | agent-critic.md (read by AI at inference) | constitution.md (rules source) | Critic flags violations; constitution defines what constitutes a violation |
| Output formatting | agent-tufte-designer.md (read by AI at inference) | constitution.md (prose fluff rules) | Designer enforces Tufte principles from both its own rules and constitution |
| Command routing | SKILL.md (prompt instructions) | — | Command matching happens at the prompt level |
| Manifesto generation | SKILL.md /dps-setup instructions | agent-tufte-designer.md (output format) | Setup instructions define expected output; Designer formats it |
| Rule enforcement | constitution.md | agent-critic.md | Constitution defines rules; Critic audits compliance |

## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01 (Manifesto YAML):** YAML frontmatter with: `project`, `framework` ("Data-Pro-Skill v2"), `sample_size`, `metrics_tracked` (array), `segments` (array)
- **D-02 (Manifesto table):** Simple Markdown table with columns: Segmento | N | % | Métrica Core
- **D-03:** No suggested cross-tabulation map in the manifesto — keep it simple and focused
- **D-04 (Core rules):** 5 core rules: (1) mandatory margin of error on sample claims, (2) p < 0.05 for significance, (3) prohibition of prose fluff, (4) prohibition of % in qualitative samples N<30, (5) minimum N for parametric tests
- **D-05 (Data quality rules):** Straight-lining detection in Likert, validation of % sum = 100%, flag missing data >10%
- **D-06 (Constitution format):** Suggested structure: 6 articles, each with rule + justification + consequence of violation
- **D-07 (Agent files):** Separate files in `agents/` — already created (agent-statistician.md, agent-critic.md, agent-tufte-designer.md)
- **D-08 (SKILL.md orchestration):** SKILL.md references and orchestrates agents: "Before responding, run internally: 1. Validate numbers (Statistician), 2. Audit biases (Critic), 3. Format Tufte output (Designer). Only the Designer's output is displayed."
- **D-09 (Specialized agents):** agent-anthropologist.md and agent-strategist.md activated by `/dps-mode:quali` and `/dps-mode:strategy`
- **D-10 (Command naming):** All meta-prompt commands use prefix `/dps-`: `/dps-setup`, `/dps-cross`, `/dps-inject-open`, `/dps-export`, `/dps-clarify`, `/dps-plan`, `/dps-mode:quant`, `/dps-mode:quali`, `/dps-mode:strategy`
- **D-11 (Naming):** In internal texts of the meta-prompt, replace "GSD" with "DPS". The `dps-engine/` engine keeps its original name as infrastructure dependency.

### the agent's Discretion

The planner has freedom to:
- Exact paragraph structure in constitution.md (as long as it covers the 8 decided rules)
- Organization of SKILL.md sections (as long as it covers agent loop, commands, output rules)
- Variable names in the YAML frontmatter of the manifesto (as long as they include the decided fields)

### Deferred Ideas (OUT OF SCOPE)

- Translation of the meta-prompt to other languages (English, Spanish) — future phase
- Automated installation script for each harness — phase 4 (export)
- Quarto/LaTeX templates for `/dps-export` — phase 4
- DPS logo and visual identity — out of meta-prompt scope

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| SETUP-01 | `/dps-setup` generates quantitative manifesto with YAML frontmatter, sample metrics, and segment definitions | See §Standard Stack (YAML frontmatter pattern), §Architecture Patterns (Manifesto Generation Pattern) |
| SETUP-02 | Manifesto includes sample size (N), volumetrics (%), and core metrics per segment | See §Architecture Patterns (Manifesto Generation Pattern) |
| CONST-01 | `constitution.md` defines inegotiable rules: margin of error, minimum sample size, confidence levels, bias handling | See §Architecture Patterns (Constitution Format), §Code Examples |
| OUTP-01 | Output follows Tufte principles — high data density, no prose fluff, margin notes, self-explanatory tables | See §Architecture Patterns (Tufte Output Pattern), §Code Examples |
| OUTP-02 | Prohibition of prose fluff phrases | See §Architecture Patterns (Tufte Output Pattern), §Code Examples |
| HARN-01 | No XML tags or platform-specific syntax | See §Common Pitfalls (Pitfall 1: XML tags in meta-prompts) |
| HARN-02 | YAML frontmatter and pure Markdown | See §Standard Stack, §Architecture Patterns |
| ARCH-01 | Quantitative pipeline built first as the spine | See §Architecture Patterns (Quantitative-First Pipeline Pattern) |
| ARCH-03 | Invisible agent loop (Statistician → Critic → Tufte Designer) | See §Architecture Patterns (Invisible Agent Loop Pattern) |

## Standard Stack

### Core

| Library/Format | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Markdown | N/A (plain text) | Document format for all outputs and prompt text | Universal across all 6 target harnesses — no rendering dependency |
| YAML Frontmatter | N/A (plain text) | Structured metadata in documents | Parsed by all major AI harnesses; no XML dependency [VERIFIED: aparente/tufte-claude-skill uses identical pattern with 724 stars] |
| Blockquotes (`>`) | N/A (Markdown syntax) | Margin notes in Tufte-style output | Native Markdown, works on all harnesses |

### Supporting

| Library/Format | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Quarto/LaTeX | N/A (downstream) | PDF generation from Markdown output | Phase 4 export — not relevant for Phase 1 |
| Pandoc | N/A (downstream) | Document format conversion | Phase 4 export — not relevant for Phase 1 |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Markdown tables | JSON arrays | JSON is stricter but less readable for AI outputs and human review |
| YAML frontmatter | TOML frontmatter | TOML less supported across harnesses; YAML has broader AI parsing coverage |
| Blockquote margin notes | HTML `<aside>` tags | HTML breaks on non-browser harnesses; Markdown blockquotes work universally |

**Version verification:** No packages to verify — this is a meta-prompt project using only plain text formats (YAML, Markdown). The "stack" is format specifications, not installable libraries.

## Package Legitimacy Audit

> **SKIPPED** — This phase installs zero external packages. Data-Pro-Skill v2 is a document-driven meta-prompt: pure Markdown + YAML frontmatter. No npm, pip, cargo, or other package manager dependencies. The only "dependencies" are the AI harnesses themselves (OpenCode, Gemini, Codex, Hermes, OpenClaw, Claude), which are runtime execution environments, not installable packages.

## Architecture Patterns

### System Architecture Diagram

```
USER INPUT (raw data + commands)
    │
    ▼
┌─────────────────────────────────┐
│  SKILL.md (Orchestrator)         │
│  ┌─────────────────────────────┐ │
│  │ 1. COMMAND ROUTING          │ │
│  │    /dps-setup → manifesto   │ │
│  │    /dps-cross → crosstab    │ │
│  │    /dps-mode:quali → persona│ │
│  └──────────┬──────────────────┘ │
│             ▼                    │
│  ┌─────────────────────────────┐ │
│  │ 2. INVISIBLE AGENT LOOP     │ │
│  │  ┌───────────────┐          │ │
│  │  │ Statistician   │──┐      │ │
│  │  │ (validate nums)│  │      │ │
│  │  └───────┬───────┘  │      │ │
│  │          ▼           │      │ │
│  │  ┌───────────────┐  │      │ │
│  │  │ Critic         │◄─┘      │ │
│  │  │ (audit bias)   │         │ │
│  │  └───────┬───────┘         │ │
│  │          ▼                  │ │
│  │  ┌───────────────┐         │ │
│  │  │ Tufte Designer │         │ │
│  │  │ (format output)│         │ │
│  │  └───────┬───────┘         │ │
│  └──────────┼────────────────┘ │
│             │                   │
│  ┌──────────▼────────────────┐ │
│  │ 3. CONSTITUTION GATE      │ │
│  │    constitution.md rules   │ │
│  │    enforced by Critic      │ │
│  └──────────┬────────────────┘ │
└─────────────┼───────────────────┘
              ▼
    OUTPUT (Tufte-formatted Markdown)
    Only the Designer's output reaches user
```

**Data flow through the system:**
1. User provides raw data + a command (e.g., `/dps-setup`)
2. SKILL.md routes to the appropriate command handler
3. The invisible agent loop processes: Statistician validates numbers → Critic audits biases against constitution.md → Tufte Designer formats output
4. Only the Designer's Markdown output is shown to the user
5. For `/dps-setup`, the output becomes the anchoring document for all subsequent commands

### Recommended Project Structure

```
/
├── SKILL.md                   # ★ PHASE 1 DELIVERABLE — Main meta-prompt
├── constitution.md            # ★ PHASE 1 DELIVERABLE — Statistical rigor rules
├── agents/                    # Agent definitions (already exist)
│   ├── agent-statistician.md
│   ├── agent-critic.md
│   ├── agent-tufte-designer.md
│   ├── agent-anthropologist.md
│   └── agent-strategist.md
├── AGENTS.md                  # Project conventions (exists)
├── docs/                      # Documentation (exists)
│   ├── COMMANDS.md
│   └── ARCHITECTURE.md
└── .planning/                 # GSD planning (exists)
```

### Pattern 1: Invisible Agent Loop Pattern

**What:** The SKILL.md instructs the AI to run three internal processing stages before producing any user-visible output. The user only sees the Tufte Designer's formatted result — never the Statistician or Critic internal reports.

**When to use:** On every command execution, before displaying output.

**Example:**
```markdown
## Internal Agent Loop (NEVER SHOWN TO USER)

Before responding to any command, execute this internal loop silently:

### Stage 1: Statistical Validation (Statistician)
- Verify all numbers are internally consistent
- Calculate margin of error: MoE = z_crit √(p(1-p)/n) where n=sample, z_crit=1.96
- Flag N<30 cases
- Output: Statistician Report (internal only)

### Stage 2: Bias & Quality Audit (Critic)
- Scan for confirmation bias, selection bias, overgeneralization
- Check compliance with constitution.md rules
- Flag missing data >10%
- Output: Critic Audit (internal only)

### Stage 3: Tufte Formatting (Designer)
- Synthesize Statistician + Critic findings
- Strip all prose fluff (see constitution.md Article 3)
- Format tables with N and conclusions in headers
- Add margin notes as blockquotes
- Output: Final user-visible response
```

[CITED: agents/agent-statistician.md, agents/agent-critic.md, agents/agent-tufte-designer.md — existing agent definitions define these three stages]

### Pattern 2: Manifesto Generation Pattern (/dps-setup)

**What:** The `/dps-setup` command produces a YAML + Markdown manifesto that becomes the single source of truth for all subsequent analysis. Every later command must reference this manifesto and never contradict its metrics.

**When to use:** First command in any analysis session.

**Example:**
```markdown
### /dps-setup Command

When the user invokes `/dps-setup` with raw data:

1. Run the invisible agent loop (Statistician → Critic → Designer)
2. Produce output in this exact structure:

---
project: "{project_name}"
framework: "Data-Pro-Skill v2"
sample_size: {N}
metrics_tracked: [{metric1}, {metric2}, ...]
segments: [{seg1}, {seg2}, ...]
---

# {Project Name} — Manifesto Quantitativo

> **Nota de Margem:** Este documento ancora o contexto numérico.
> Nenhuma análise posterior pode contradizer as métricas estabelecidas aqui.

## Matriz de Segmentos

| Segmento | N | % | Métrica Core |
| :--- | :--: | :--: | :--- |
| {Segmento A} | {n} | {pct}% | {metric_value} |
| {Segmento B} | {n} | {pct}% | {metric_value} |
```

[CITED: .deprecated/v1/coonversa.md lines 95-118 — Gemini's blueprint for /setup output; USER DECISIONS D-01, D-02, D-03 — CONTEXT.md]

### Pattern 3: Constitution Format Pattern

**What:** A 6-article legal-style document where each article has: (1) the rule, (2) the statistical/methodological justification, (3) the consequence of violation — what the Critic agent must flag if the rule is broken.

**When to use:** constitution.md is read by the Critic agent during every analysis command.

**Example:**
```markdown
## Article 1 — Margin of Error Obligatory on Sample Claims

**Rule:** Every claim derived from a sample must report the margin
of error at 95% confidence level.

**Justification:** Point estimates without confidence intervals imply
false precision. A reported "45% prefer Brand A" without MoE
misleads the reader into believing certainty where none exists.

**Violation Consequence:** The Critic must flag the claim and refuse
to pass it to the Designer until MoE is computed and displayed.

**Computation:** MoE = z_crit × √(p(1-p)/n) where z_crit = 1.96 for
95% confidence, p = proportion, n = sample size.

## Article 2 — Statistical Significance Threshold
...
```

[CITED: USER DECISIONS D-04, D-06 — CONTEXT.md; USER DECISIONS from Spec-Kit constitution pattern defined in coonversa.md]

### Pattern 4: Tufte Output Pattern

**What:** All analytical output follows strict formatting rules: tables with N and conclusions in headers, blockquote margin notes for interpretation, zero prose fluff.

**When to use:** Every user-visible output from the Tufte Designer agent.

**Example:**
```markdown
## Forbidden Prose Fluff Phrases

NEVER start a paragraph with any of these:
- "It's important to note that..."
- "Based on the data provided..."
- "Interestingly..."
- "It is worth mentioning..."
- "One can observe that..."
- "The data suggests that..."
- "In conclusion..."

## Table Format

Every table:
| Segmento | N  | %  | Métrica | Conclusão |
| :---     |:--:|:--:| :--:    | :---      |
| Grupo A  | 290 | 45 | NPS: -15 | Maior rejeição — investigar qualitativo |

## Margin Note Format

> **Nota de Margem:** [sharp, specific insight — never generic, 1-3 sentences max]
```

[CITED: agents/agent-tufte-designer.md lines 12-101 — existing output rules; aparente/tufte-claude-skill SKILL.md — Tufte principles applied in prompt format]

### Pattern 5: Quantitative-First Pipeline Pattern

**What:** The quantitative pipeline is the spine. Qualitative analysis (`/dps-inject-open`) can only enrich existing quantitative segments — never create standalone sections. The `/dps-setup` manifesto defines the segments that qualitative data must be categorized into.

**When to use:** This is an architectural constraint, encoded in SKILL.md instructions and enforced by constitution.md.

**How it works in the prompt:**
```markdown
## Architecture: Quantitative-First

The `/dps-setup` manifesto is the spine. All subsequent commands:
1. MUST read the manifesto for context
2. MUST reference segments defined in the manifesto
3. MUST NOT create segments not in the manifesto
4. MUST NOT contradict metrics established in the manifesto

For qualitative data (`/dps-inject-open`):
- Categorize ALL responses within existing manifesto segments
- Never create standalone qualitative sections
- Use the segment table from `/dps-setup` as the categorization framework
```

[CITED: USER DECISIONS from CONTEXT.md; ARCH-01, ARCH-02 from REQUIREMENTS.md]

### Anti-Patterns to Avoid

- **Command name collision:** Using `/setup` instead of `/dps-setup` — the prefix `/dps-` is locked. Similarly, never use "GSD" in meta-prompt internal text, only "DPS". [CITED: D-10, D-11]
- **XML tags in prompt:** `<role>`, `<constraints>`, `<instructions>` blocks break on Gemini and Codex harnesses. Use plain Markdown with `###` headings and `**bold**` emphasis instead. [CITED: HARN-01 from REQUIREMENTS.md]
- **Emoji in analytical output:** The existing agent files use emoji (📊, 🧠, 💼) — but project conventions say "No emoji in analytical output." These should not propagate to user-visible output. [CITED: CONVENTIONS.md]
- **Mixing agent formats:** The existing agent `.md` files use YAML frontmatter + XML-wrapped role sections. This is fine for reference files, but the SKILL.md orchestrator MUST use pure Markdown with no XML. [CITED: HARN-01, HARN-02]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Agent orchestration logic | Custom state machine or subprocess calls | Sequential prompt instructions (Stage 1 → Stage 2 → Stage 3) | AI harnesses execute prompt instructions natively — no runtime needed |
| Format validation | Scripts to check YAML/Markdown output | Constitution.md rules enforced by Critic agent at inference time | The AI itself validates output during the invisible loop |
| Cross-harness compatibility | Platform-specific directives or feature flags | Pure Markdown + YAML (lowest common denominator across all 6 harnesses) | Any harness can render Markdown; YAML frontmatter is universally parseable |

**Key insight:** The "don't hand-roll" principle applies differently to meta-prompts than to software. Here, the guidance is about NOT embedding logic that could be handled by the AI inference process itself. The invisible agent loop IS the computation — no external scripts needed.

## Runtime State Inventory

> Omitted — this is a greenfield phase. No rename, refactor, or migration involved.

## Common Pitfalls

### Pitfall 1: XML Tags in Multi-Harness Meta-Prompts

**What goes wrong:** Using `<role>`, `<constraints>`, `<instructions>` XML-wrapped sections in SKILL.md (as seen in the existing agent files). These XML tags are a Claude/OpenCode convention and fail silently or produce garbled output on Gemini CLI, Codex CLI, and Hermes — which either strip unknown tags or treat their content as literal text.

**Why it happens:** The existing agent files were written in the GSD template format which uses XML-wrapped role blocks. Developers naturally copy this pattern into SKILL.md without realizing it breaks harness compatibility.

**How to avoid:** Write SKILL.md entirely in pure Markdown. Use `###` headings for sections, `**bold**` for emphasis, and numbered lists for sequential instructions. The existing agent files in `agents/` can keep their format (they're reference documents), but the SKILL.md that gets copied to harness skill directories must contain zero XML.

**Warning signs:** Opening `<role>` or `<constraints>` tags anywhere in SKILL.md. If you see them, stop and rewrite as Markdown.

[CITED: HARN-01 from REQUIREMENTS.md; CONVENTIONS.md "No XML tags"; verified against coonversa.md blueprint which explicitly warns against XML tags]

### Pitfall 2: Over-Prescribing the AI's Internal Reasoning

**What goes wrong:** SKILL.md says "run these 15 statistical tests, then check 8 bias dimensions, then apply 12 formatting rules" — overwhelming the prompt and causing the AI to skip steps or produce inconsistent outputs.

**Why it happens:** Desire for completeness leads to enumerating every possible statistical test and bias check in the SKILL.md, when these should be in the agent reference files that the AI reads on-demand.

**How to avoid:** SKILL.md should contain the ORCHESTRATION LOGIC (what stages run, in what order, what each stage is responsible for). The detailed rules (how to perform each test, what specific biases to check) belong in the reference files: `agents/agent-statistician.md`, `agents/agent-critic.md`, `agents/agent-tufte-designer.md`, and `constitution.md`. SKILL.md tells the AI "read file X for detailed rules" rather than copying all rules inline.

**Warning signs:** SKILL.md exceeding 200 lines of detailed rules. Individual testing checklists inline rather than as file references.

[CITED: D-07, D-08 from CONTEXT.md — agents in separate files, SKILL.md orchestrates]

### Pitfall 3: Inconsistent Handling of the "DPS" Naming Convention

**What goes wrong:** SKILL.md uses "GSD" in some places and "DPS" in others, confusing the AI about which system it's operating under. The engine directory is `dps-engine/` but the meta-prompt's internal identity is "Data-Pro-Skill" (DPS).

**Why it happens:** Mixed naming from two sources — the infrastructure (GSD workflows, GSD commands) and the analysis system (DPS commands, DPS constitution). Both coexist in the same repo.

**How to avoid:** Strict rule: In SKILL.md and constitution.md, EVERY command uses `/dps-` prefix and every system reference uses "DPS". The `dps-engine/` directory and `commands/gsd/` path are file system details — never mentioned in user-facing prompt text. Enforcement checklist:
- `/dps-setup` ✓ (never `/setup`)
- "DPS constitution" ✓ (never "GSD constitution")
- "Data-Pro-Skill v2" ✓ (never "GSD Data-Pro")
- `dps-engine/` directory path ✓ (only when referencing file locations for the AI to read)

**Warning signs:** Grepping SKILL.md for "GSD" returning matches in non-file-path contexts.

[CITED: D-10, D-11 from CONTEXT.md]

### Pitfall 4: Constitution Enforcement Gap

**What goes wrong:** The constitution.md defines rules, but the SKILL.md doesn't explicitly instruct the Critic agent to read and enforce them. Result: rules exist on paper but never get applied during analysis.

**Why it happens:** Assumption that "the AI will read constitution.md because it's in the project." In practice, the SKILL.md must explicitly say "Read constitution.md. Enforce every rule. Flag violations."

**How to avoid:** In the SKILL.md Critic stage instructions, include:
```markdown
### Stage 2: Critic (Bias & Quality Audit)

Before proceeding to output, read `constitution.md` and verify:
1. Every sample claim has margin of error (Article 1)
2. All significance claims have p < 0.05 (Article 2)
3. Output contains zero prose fluff (Article 3)
4. No qualitative sample N<30 reports percentages (Article 4)
5. Parametric tests only when N meets minimum (Article 5)
6. Data quality: no straight-lining, sum checks, missing data >10% (Article 6)

Any violation: flag and block Designer output until fixed.
```

**Warning signs:** constitution.md exists but no reference to it in SKILL.md Critic instructions. [CITED: CONST-01 from REQUIREMENTS.md]

### Pitfall 5: Harness-Specific Frontmatter Fields

**What goes wrong:** SKILL.md YAML frontmatter uses fields only recognized by one harness — e.g., `tools: Bash` (OpenCode-specific agent field) in a file that's supposed to work on Gemini and Codex.

**Why it happens:** The existing agent files use `tools: Bash` and `color: blue` in their YAML frontmatter. Copying this pattern to SKILL.md inserts harness-specific metadata.

**How to avoid:** SKILL.md YAML frontmatter should only use universal fields:
```yaml
---
name: data-pro-skill
description: Market research data analysis meta-prompt. Transforms raw quantitative and qualitative data into dense Tufte-style analytical documents with invisible agent loop (Statistician → Critic → Tufte Designer).
---
```
Fields like `tools`, `color`, `model` are OpenCode-specific and should NOT appear in SKILL.md.

**Warning signs:** Any frontmatter field beyond `name` and `description` in SKILL.md.

[CITED: HARN-01, HARN-02 from REQUIREMENTS.md; verified against tufte-claude-skill SKILL.md (aref-vc) which uses only name/description in frontmatter]

## Code Examples

Verified patterns from official and reference sources:

### SKILL.md Frontmatter Pattern (Harness-Agnostic)

```markdown
---
name: data-pro-skill
description: |
  Market research data analysis meta-prompt. Transforms raw quantitative
  and qualitative research data into dense Tufte-style analytical documents.
  Invisible agent loop: Statistician → Critic → Tufte Designer.
  Commands: /dps-setup, /dps-cross, /dps-inject-open, /dps-export,
  /dps-clarify, /dps-plan. Modes: /dps-mode:quant, /dps-mode:quali,
  /dps-mode:strategy. Works across OpenCode, Gemini, Codex, Hermes,
  OpenClaw, Claude.
---

# Data-Pro-Skill v2

... [pure Markdown instructions, no XML tags] ...
```

[CITED: tufte-claude-skill SKILL.md (aref-vc) — uses only name/description in frontmatter; ADAPTED for Data-Pro-Skill context]

### Constitution Article Template

```markdown
## Article {N} — {Title}

### Rule
{One clear, testable statement. The Critic must be able to answer "is
this violated?" with yes/no.}

### Justification
{Why this rule exists — the methodological or statistical reasoning.
Reference the harm prevented by following the rule.}

### Violation Consequence
{What the Critic agent must do when this rule is broken. Example:
"Flag the output. Block delivery to Designer until corrected."}

### Computation / Detection
{If applicable, the formula or detection method. Example: MoE formula
for Article 1, straight-lining heuristic for Article 6 data quality.}
```

[CITED: USER DECISIONS D-04, D-05, D-06 — CONTEXT.md; coonversa.md discussion about "legal-article style" constitution]

### Agent Loop Instruction Template (for SKILL.md)

```markdown
## Internal Agent Loop

Before producing ANY user-visible output after a command, execute
this internal processing sequence. The user NEVER sees Stage 1 or
Stage 2 output — only Stage 3.

### Stage 1: Statistician (Numerical Validation)
Read `agents/agent-statistician.md` for detailed instructions.
- Validate all numbers are internally consistent
- Compute margin of error for all sample-based claims
- Select appropriate statistical tests
- Flag data quality issues (missing >10%, outliers, straight-lining)

### Stage 2: Critic (Bias & Quality Audit)
Read `agents/agent-critic.md` and `constitution.md`.
- Audit for all bias dimensions defined in agent-critic.md
- Verify compliance with ALL articles in constitution.md
- Flag any violation — block output if constitution rules broken

### Stage 3: Tufte Designer (Output Formatting)
Read `agents/agent-tufte-designer.md`.
- Synthesize Statistician + Critic findings
- Strip ALL prose fluff phrases (constitution.md Article 3)
- Format tables with N columns and conclusions in headers
- Add margin notes as blockquotes
- Produce final user-visible response
```

[CITED: D-07, D-08 from CONTEXT.md; existing agent files define the three stages]

### Forbidden Prose Fluff Pattern (for constitution.md Article 3)

```markdown
## Article 3 — Prohibition of Prose Fluff

### Rule
Output must go straight to the data. The following phrases and their
variants are FORBIDDEN as paragraph openers or content fillers:

- "It's important to note that..."
- "Based on the data provided..."
- "Interestingly..."
- "It is worth mentioning..."
- "One can observe that..."
- "The data suggests that..."
- "In conclusion..."
- "As we can see..."

### Detection
The Critic scans output for these phrases before the Designer
delivers. Any match = violation. The sentence must be rewritten
or deleted.

### Justification
Prose fluff adds words without adding information. It reduces data
density — the ratio of meaningful content to total text. Tufte's
principle: "Maximize data-ink ratio." In prose, this means maximize
information per word.

### Violation Consequence
Critic returns output to Designer with fluff phrases highlighted.
Designer must remove or rewrite before delivery.
```

[CITED: agents/agent-tufte-designer.md lines 12-23; OUTPUT-01, OUTPUT-02 from REQUIREMENTS.md]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Single-harness AI skills (Claude-only XML) | Multi-harness pure Markdown SKILL.md | 2025-2026 trend | Any AI can execute; no platform lock-in |
| AI outputs prose-heavy analysis | Tufte-style dense data tables + margin notes | Established in tufte-claude-skill (2025) | Higher information density; reader gets answers faster |
| Separate agent files with platform-specific directives | Single SKILL.md with file references, no XML | Current best practice | Portability across OpenCode, Gemini, Codex, Claude, Hermes, OpenClaw |
| Direct statistical analysis (AI decides tests) | Agent loop with mandatory validation stages | GSD pattern (2025) | Reduces AI hallucination in numerical claims |

**Deprecated/outdated:**
- **XML-wrapped prompt sections:** `<role>`, `<constraints>`, `<instructions>` — incompatible with Gemini CLI and Codex CLI. Replaced by pure Markdown with `###` headings.
- **Platform-specific agent directives:** `tools: Bash`, `color: blue` in YAML frontmatter — only relevant to OpenCode agents, don't port to other harnesses. For SKILL.md, use only `name` and `description`.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | All 6 target harnesses (OpenCode, Gemini, Codex, Hermes, OpenClaw, Claude) can parse YAML frontmatter and render Markdown tables | Standard Stack | LOW — YAML and Markdown are universal plain-text formats; risk is minor rendering differences, not parsing failures |
| A2 | The existing agent files in `agents/` will remain as-is and are only reference documents read by the AI at inference time, not copied to harness skill directories | Architecture Patterns | LOW — the SKILL.md references them by path; this is the documented pattern for reference-file skills |
| A3 | The AI harness executing SKILL.md will have access to the project directory and can read `agents/` and `constitution.md` files at inference time | Architecture Patterns | MEDIUM — some harnesses may sandbox file access; OpenCode and Claude Code support this; Gemini CLI and Codex may need the files to be in a specific location. The planner should verify file access behavior for each target harness. |
| A4 | The invisible agent loop (sequential prompt instructions) is sufficient to make the AI perform statistical validation, bias auditing, and Tufte formatting in sequence | Architecture Patterns | LOW — this pattern is validated by the GSD agent loop in production |

## Open Questions

1. **How should SKILL.md handle the case where `agents/` files are not accessible to the AI?**
   - What we know: Claude Code and OpenCode can read project files at inference. Gemini CLI and Codex CLI behavior with file references is less documented.
   - What's unclear: Whether all 6 harnesses can follow "Read `agents/agent-statistician.md`" instructions.
   - Recommendation: Include the core statistical rules and bias dimensions inline in SKILL.md as a fallback, with the reference file pattern as the primary approach.

2. **Should the constitution.md be referenced from SKILL.md, or should its rules be duplicated inline?**
   - What we know: D-08 says SKILL.md references and orchestrates agents. The constitution is a separate file that the Critic reads.
   - What's unclear: Whether one layer of indirection (SKILL.md → constitution.md) is reliable across all harnesses.
   - Recommendation: Embed the FORBIDDEN PHRASES list and core checks inline in SKILL.md (they're short). Reference constitution.md for detailed justifications and edge cases. Redundancy for critical rules is safer than relying entirely on file access.

3. **What exactly constitutes "prose fluff" vs "necessary context" in an analytical output?**
   - What we know: The agent-tufte-designer.md lists 7 forbidden phrases. But the boundary is fuzzy — "The retention rate is 78% (±3.2%, 95% CI), driven primarily by..." is the "driven primarily by" fluff?
   - What's unclear: How to define a clean rule that the Critic can enforce mechanically.
   - Recommendation: Define fluff as "any sentence or clause that can be deleted without removing a number, named entity, or finding." Pure context-free deletion test.

## Environment Availability

> **SKIPPED** — This phase has no external dependencies. Data-Pro-Skill v2 is a document-driven meta-prompt: the only "environment" needed is an AI harness (OpenCode, Gemini, Codex, Hermes, OpenClaw, or Claude) — which is the execution context by definition. No databases, services, CLIs, runtimes, or package managers are required to create or test `constitution.md`, `SKILL.md`, or the `/dps-setup` command logic.
>
> The phase deliverables are: two Markdown files (`constitution.md`, `SKILL.md`) and embedded command logic (the `/dps-setup` prompt instructions). Testing consists of copying SKILL.md to a harness skill directory and invoking `/dps-setup` with sample data — manual validation only.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Manual validation across 6 target harnesses |
| Config file | none — this is a meta-prompt, not software |
| Quick run command | `cp SKILL.md ~/.opencode/skills/data-pro-skill/ && /dps-setup [sample_data]` (OpenCode example) |
| Full suite command | Test `/dps-setup` on all 6 harnesses with identical sample input; compare outputs for consistency |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SETUP-01 | `/dps-setup` produces YAML manifesto with segments, N, volumetrics | manual | Copy SKILL.md to harness, run `/dps-setup` with sample CSV data | ❌ Wave 0 |
| SETUP-02 | Manifesto table has N, %, Métrica Core columns | manual | Verify output table structure matches D-02 spec | ❌ Wave 0 |
| CONST-01 | constitution.md defines margin of error, p<0.05, bias handling | manual | Read constitution.md, verify 6 articles cover 8 rules per D-04/D-05 | ❌ Wave 0 |
| OUTP-01 | Output follows Tufte principles: data density, margin notes, self-explanatory tables | manual | Inspect `/dps-setup` output for blockquote notes, N in table headers | ❌ Wave 0 |
| OUTP-02 | No prose fluff phrases in output | manual | Grep output for forbidden phrases list | ❌ Wave 0 |
| HARN-01 | No XML tags in SKILL.md or constitution.md | manual | Grep files for `<role>`, `<constraints>`, `<instructions>` tags | ❌ Wave 0 |
| HARN-02 | YAML frontmatter and pure Markdown used | manual | Verify YAML parses without errors; no platform-specific syntax | ❌ Wave 0 |
| ARCH-01 | Quantitative pipeline described as spine in SKILL.md | manual | Read SKILL.md architecture section — verify quant-first language | ❌ Wave 0 |
| ARCH-03 | Invisible agent loop described in SKILL.md | manual | Verify 3-stage internal loop instructions present | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** `grep -c '<role>\|<constraints>' SKILL.md constitution.md` (expect 0)
- **Per wave merge:** Manual validation: copy SKILL.md to 1 harness, test `/dps-setup` with sample data
- **Phase gate:** All 6 harnesses tested with identical `/dps-setup` input — outputs consistent, no XML tags, zero fluff phrases

### Wave 0 Gaps
- [ ] `outputs/00_test_manifest.md` — sample `/dps-setup` output to validate manifesto format (covers SETUP-01, SETUP-02)
- [ ] `outputs/01_fluff_audit.md` — run `/dps-setup` output through fluff phrase grep (covers OUTP-02)
- [ ] `outputs/02_xml_audit.md` — grep SKILL.md and constitution.md for forbidden XML tags (covers HARN-01)
- [ ] `outputs/03_loop_audit.md` — verify SKILL.md contains 3-stage internal agent loop (covers ARCH-03)
- [ ] `outputs/04_constitution_audit.md` — verify constitution.md has 6 articles covering all 8 rules (covers CONST-01)
- [ ] Framework install: none — no test framework to install; manual validation only

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | N/A — this is a meta-prompt, no authentication layer |
| V3 Session Management | no | N/A — stateless document-driven system |
| V4 Access Control | no | N/A — single-analyst workflow, no multi-user |
| V5 Input Validation | yes | constitution.md Article 5 (data quality: straight-lining detection, % sum validation, missing data >10% flag) and Article 1 (sample-based claims require MoE) |
| V6 Cryptography | no | N/A — no encrypted data handling |

### Known Threat Patterns for Meta-Prompt Systems

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Data hallucination (AI fabricates numbers) | Spoofing | Statistician agent validates all numbers against input data; Critic flags unsupported claims |
| Confirmation bias (AI confirms user's hypotheses regardless of data) | Tampering | Critic agent explicitly audits for confirmation bias; SKILL.md instructions require null hypothesis testing |
| Overgeneralization from small samples (N<30) | Information Disclosure | constitution.md Article 4 prohibits percentages from small qualitative samples; Critic enforces |
| Spurious correlation claims | Repudiation | constitution.md Article 2 requires p<0.05; Critic checks confounding variables |
| Missing data bias (conclusions from incomplete data) | Elevation of Privilege | constitution.md Article 6 flags missing >10%; Critic reports missingness patterns |
| Prose fluff masking weak findings | Tampering | constitution.md Article 3 prohibits fluff phrases; Critic scans output before delivery |

**Key insight for this phase:** The "security" concern in a meta-prompt is statistical integrity and output honesty — not traditional web application security. The constitution.md IS the security control framework. Each article prevents a specific class of analytical harm, and the Critic agent IS the enforcement mechanism.

## Sources

### Primary (HIGH confidence)
- `agents/agent-statistician.md` — Agent definitions: sample profile, distribution, test selection, data quality, output format (82 lines)
- `agents/agent-critic.md` — Audit dimensions: 6 bias categories, missing data patterns, output format (81 lines)
- `agents/agent-tufte-designer.md` — Output rules: forbidden phrases, table format, margin notes, qualitative integration (102 lines)
- `.planning/phases/01-constitution-setup/01-CONTEXT.md` — User decisions D-01 through D-11, locked constraints, discretion areas (121 lines)
- `.deprecated/v1/coonversa.md` — Original Gemini conversation defining blueprint: /setup output example (lines 95-118), agent loop definition (lines 126-137), Tufte output rules (lines 140-163) [CITED throughout]
- `AGENTS.md` — Project conventions: no XML tags, no emoji, no prose fluff, table format, agent loop architecture (137 lines)
- `.planning/REQUIREMENTS.md` — 21 v1 requirements, traceability matrix, Phase 1 mapped requirements: SETUP-01/02, CONST-01, OUTP-01/02, HARN-01/02, ARCH-01/03 (113 lines)
- `aref-vc/tufte-claude-skill` (GitHub) — Reference implementation of Tufte principles as a Claude skill: SKILL.md structure pattern, 10 Tufte principles distilled [VERIFIED: public repo, 170 stars, 17 forks, MIT license]
- `aparente/tufte-viz` (GitHub Gist) — Tufte visualization skill with SKILL.md, principles reference, eraser test, collision test [VERIFIED: public gist, 725 stars, 84 forks]

### Secondary (MEDIUM confidence)
- `docs/ARCHITECTURE.md` — Project architecture documentation: agent loop diagram, project structure, multi-harness compatibility table [project documentation, not externally verified]
- `docs/COMMANDS.md` — Command reference: `/setup` expected input/output format, mode descriptions [project documentation, not externally verified]
- `.planning/PROJECT.md` — Project definition, core value, constraints, key decisions [project documentation, not externally verified]

### Tertiary (LOW confidence)
- None — all claims in this research are either from project-internal locked decisions (CONTEXT.md), existing agent files, or verified public reference implementations (tufte-claude-skill). No unverified WebSearch claims.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — only plain text formats (Markdown, YAML), no version ambiguity, verified against public reference implementations
- Architecture: HIGH — patterns derived from locked user decisions (CONTEXT.md), existing agent files, and validated against the tufte-claude-skill reference implementation
- Pitfalls: HIGH — XML tag pitfall is verified by HARN-01 requirement and tufte-claude-skill SKILL.md pattern; naming convention pitfall is from D-10/D-11 locked decisions; over-prescribing pitfall is from knowledge of AI context window limitations

**Research date:** 2026-05-25
**Valid until:** 2026-06-25 (30 days — meta-prompt architecture is stable; the core patterns are well-established in the tufte-claude-skill reference)
