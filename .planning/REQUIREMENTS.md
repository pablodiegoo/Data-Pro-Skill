# Requirements: Data-Pro-Skill v2

**Defined:** 2026-05-25
**Core Value:** One prompt that transforms raw market research data into publication-ready analytical documents — quantitative first, qualitative as layered extensions — with zero prose fluff, maximum data density, across any AI harness.

## v1 Requirements

### Setup & Constitution

- [ ] **SETUP-01**: `/setup` command generates a quantitative manifesto with YAML frontmatter, sample metrics (N, volumetrics), and segment definitions that anchor all subsequent analysis
- [ ] **SETUP-02**: Manifesto includes sample size (N), volumetrics (%), and core metrics (NPS, CSAT, Churn) per segment
- [ ] **CONST-01**: `constitution.md` defines inegotiable rules: margin of error, minimum sample size, confidence levels, bias handling, prohibition of qualitative generalizations from small samples

### Clarify & Plan

- [ ] **CLAR-01**: `/clarify` runs 3-5 provocative questions about business goals and hypotheses before touching data
- [ ] **PLAN-01**: `/plan` outputs an analytical plan specifying which tests/crosses will be run and why

### Analysis Commands

- [ ] **CROSS-01**: `/cross [VarX] x [VarY]` produces dense Tufte-style crosstab tables with margin notes for interpretation
- [ ] **CROSS-02**: Tables must include N, volumetrics, and conclusion in headers
- [ ] **INJECT-01**: `/inject-open [text]` categorizes open-ended responses within existing quantitative segments — never as standalone analysis
- [ ] **EXEC-01**: `/execute` runs the planned analysis and renders output in Tufte style

### Modes

- [ ] **MODE-01**: `/mode:quant` activates statistical persona — correlations, crosstabs, NPS, Churn, CSAT, clean Python scripts
- [ ] **MODE-02**: `/mode:quali` activates anthropological persona — latent needs, sentiment analysis, archetypes, journeys, verbatims
- [ ] **MODE-03**: `/mode:strategy` activates BI Director persona — translates numbers into business recommendations

### Output & Export

- [ ] **OUTP-01**: Analytical output follows Tufte principles — high data density, no prose fluff, margin notes for interpretation, self-explanatory tables
- [ ] **OUTP-02**: Prohibition of phrases like "it's important to note" or "based on the data provided" — go straight to the data
- [ ] **EXPT-01**: `/export` consolidates all analysis into a single clean Markdown file ready for Pandoc/Quarto/LaTeX conversion

### Harness Compatibility

- [ ] **HARN-01**: Core prompt logic uses no XML tags or platform-specific syntax
- [ ] **HARN-02**: Uses YAML frontmatter and pure Markdown for structured output
- [ ] **HARN-03**: Works on OpenCode, Gemini, Codex, Hermes, OpenClaw, and Claude

### Architecture

- [ ] **ARCH-01**: Quantitative pipeline built first as the spine
- [ ] **ARCH-02**: Qualitative analysis added as extensions/ramifications of quantitative segments — not parallel
- [ ] **ARCH-03**: Invisible agent loop — Statistician validates numbers, Critic checks biases, Tufte Designer renders output; only the final output shown to user

## v2 Requirements

### Advanced Analysis

- **ADVN-01**: Time-series trend analysis across multiple data collection waves
- **ADVN-02**: Statistical significance testing built into crosstabs
- **ADVN-03**: Weighted sample adjustment for demographic representation

### Collaboration

- **COLL-01**: Multi-researcher workspace with shared context
- **COLL-02**: Versioned analysis history

### Visualization

- **VIZ-01**: Automatic chart generation recommendations (what chart type for which data)
- **VIZ-02**: Mermaid diagram integration for flow/journey mapping

## Out of Scope

| Feature | Reason |
|---------|--------|
| Real-time streaming analysis | Batch/document-oriented only |
| Mobile app or GUI | Pure prompt/markdown experience |
| Platform-specific features | Must work on free/open harnesses |
| Multi-user collaboration | Single-analyst workflow |
| Database or API backend | All data provided inline by user |
| Video or rich media analysis | Text and structured data only |
| Automated PPT/Keynote generation | Markdown → Quarto/PDF is the target |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| SETUP-01 | Phase 1 | Pending |
| SETUP-02 | Phase 1 | Pending |
| CONST-01 | Phase 1 | Pending |
| CLAR-01 | Phase 2 | Pending |
| PLAN-01 | Phase 2 | Pending |
| CROSS-01 | Phase 2 | Pending |
| CROSS-02 | Phase 2 | Pending |
| INJECT-01 | Phase 3 | Pending |
| EXEC-01 | Phase 2 | Pending |
| MODE-01 | Phase 3 | Pending |
| MODE-02 | Phase 3 | Pending |
| MODE-03 | Phase 4 | Pending |
| OUTP-01 | Phase 1 | Pending |
| OUTP-02 | Phase 1 | Pending |
| EXPT-01 | Phase 4 | Pending |
| HARN-01 | Phase 1 | Pending |
| HARN-02 | Phase 1 | Pending |
| HARN-03 | Phase 4 | Pending |
| ARCH-01 | Phase 1 | Pending |
| ARCH-02 | Phase 3 | Pending |
| ARCH-03 | Phase 1 | Pending |

**Coverage:**
- v1 requirements: 21 total
- Mapped to phases: 21
- Unmapped: 0 ✓

---
*Requirements defined: 2026-05-25*
*Last updated: 2026-05-25 after initial definition*
