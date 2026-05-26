# Roadmap: Data-Pro-Skill v2

**4 phases** | **21 requirements** | All v1 mapped ✓

---

### Phase 1: Constitution & Setup

**Goal:** Establish the analytical constitution and `/dps-setup` command that anchors all subsequent analysis with a quantitative manifesto in Tufte style.

**Mode:** mvp

**Requirements:**
- SETUP-01, SETUP-02, CONST-01, OUTP-01, OUTP-02, HARN-01, HARN-02, ARCH-01, ARCH-03

**Plans:** 2 plans

Plans:
- [x] 01-01-PLAN.md — Create constitution.md (6 articles, 8 rules) + SKILL.md (agent loop, /dps-setup, commands, Tufte rules, DPS naming) ✓
- [x] 01-02-PLAN.md — Walking skeleton validation: run /dps-setup with sample data, validate all 9 requirements, create SKELETON.md ✓

**Success Criteria:**
1. `/dps-setup` produces a YAML-frontmatter manifesto with segments, N, volumetrics, and core metrics
2. Output has zero prose fluff — goes straight to data
3. Output is pure Markdown with no XML tags (harness-agnostic)
4. Invisible agent loop (Statistician → Critic → Tufte Designer) is documented in the prompt
5. `constitution.md` defines statistical rigor rules

**Dependencies:** None (ground-up build)

---

### Phase 2: Quantitative Analysis

**Goal:** Deliver the core quantitative analysis pipeline — clarify business goals, plan tests, run crosstabs, and render dense analytical tables.

**Mode:** mvp

**Requirements:**
- CLAR-01, PLAN-01, CROSS-01, CROSS-02, EXEC-01, MODE-01

**Plans:** 3 plans

Plans:
- [ ] 02-01-PLAN.md — Pre-analysis layer: /dps-clarify (adaptive hypothesis questions) + /dps-mode:quant (session-scoped Statistician persona)
- [ ] 02-02-PLAN.md — Core analysis: /dps-cross [VarX] x [VarY] (Tufte crosstab with auto-selected statistical test, full agent loop)
- [ ] 02-03-PLAN.md — Scaling up: /dps-plan (checklist of suggested crosses) + /dps-execute (autonomous multi-cross analysis)

**Success Criteria:**
1. `/clarify` asks 3-5 provocative business questions before any calculation
2. `/plan` outputs an analytical plan with specific tests
3. `/cross [VarX] x [VarY]` produces dense Tufte-style crosstabs with N, %, and margin notes
4. `/mode:quant` activates statistical persona correctly
5. Output is harness-agnostic Markdown

**Dependencies:** Phase 1 (uses `/setup` manifesto as context anchor)

---

### Phase 3: Qualitative Injection

**Goal:** Add qualitative analysis as a ramification of quantitative segments — `/inject-open` categorizes open-ended responses within existing segments, not as standalone analysis.

**Mode:** mvp

**Requirements:**
- INJECT-01, MODE-02, ARCH-02

**Plans:** 2 plans

Plans:
- [ ] 03-01-PLAN.md — Qualitative injection: Anthropologist stage (Stage 3) in agent loop + /dps-inject-open command (theme extraction, verbatim mapping, quali subsections within quant segments)
- [ ] 03-02-PLAN.md — Mode toggle: /dps-mode:quali session-scoped implementation (Anthropologist activation for all subsequent commands per D-08)

**Success Criteria:**
1. `/inject-open [text]` correctly categorizes open-ended responses into quantitative segments defined by `/setup`
2. `/mode:quali` activates anthropological persona
3. Qualitative findings are displayed as margin notes within existing quantitative tables, not as separate sections
4. Zero generalization errors (no "70% of respondents" from N=10 qualitative sample)

**Dependencies:** Phase 2 (uses quantitative segments as categorization framework)

---

### Phase 4: Strategy, Export & Polish

**Goal:** Add strategic translation layer, document export, and final multi-harness compatibility.

**Mode:** mvp

**Requirements:**
- MODE-03, EXPT-01, HARN-03

**Plans:** 2 plans

Plans:
- [ ] 04-01-PLAN.md — /dps-export command (consolidated MD with flags) + /dps-mode:strategy (post-processing BI Director)
- [ ] 04-02-PLAN.md — Multi-harness compatibility validation (HARN-03): zero XML, clean YAML, DPS naming, file ref integrity

**Success Criteria:**
1. `/mode:strategy` translates numbers into business recommendations
2. `/export` consolidates all analysis into a single clean Markdown file
3. Full pipeline works on OpenCode, Gemini, Codex, Hermes, and Claude
4. Output file is ready for Pandoc/Quarto/LaTeX conversion

**Dependencies:** Phase 3 (needs qualitative data integrated into segments)

---
*Created: 2026-05-25*
*Last updated: 2026-05-26*
