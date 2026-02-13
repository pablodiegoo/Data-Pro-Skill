---
description: Deep study of external documents to extract insights, validate applicability, and propose project improvements.
---

# 📚 Document Study Workflow

This workflow combines AI research capabilities to perform deep analysis of documents (papers, articles, reports) and transform them into actionable project insights.

## When to Use
- Analyzing academic papers or technical articles.
- Studying industry benchmarks or competitor reports.
- Evaluating new libraries, frameworks, or statistical methodologies.
- Reviewing RFCs or technical standards.

---

## Phase 1: Preparation & Literacy
**Goal**: Fully comprehend the document before analysis.

1. **Load Document**: Use `read_url_content`, `view_file`, or OCR tools.
2. **Exploratory Reading**: Identify the main structure and target sections relevant to the task.
3. **Reading Summary**: Create a log in `docs/studies/YYYY-MM-DD-<doc-name>.md`.

---

## Phase 2: Knowledge Extraction
**Goal**: Map all useful knowledge.

4. **Key Concepts**: List technical terms, patterns, or frameworks.
5. **Claims & Evidence**: Identify what the author claims and what data supports it.
6. **Tooling**: Map any mentioned technologies or configurations.

---

## Phase 3: Applicability Analysis
**Goal**: Validate what fits the current project context.

7. **Stack Comparison**: Check compatibility with existing architecture/memory.
8. **Cost-Benefit (RICE)**: Evaluate the Reach, Impact, Confidence, and Effort of adopting the new insight.
9. **Classification**:
   - ✅ **Quick Wins**: Immediate implementation possible.
   - 🔄 **Adapt Required**: Needs modification for local context.
   - ❌ **Non-Applicable**: Document reasons for rejection.

---

## Phase 4: Action & Integration
**Goal**: Transform knowledge into concrete tasks.

10. **Brainstorming**: Propose approaches for applicable insights.
11. **Technical Roadmap**: Map short, medium, and long-term improvements.
12. **Archive**: Create the final study artifact in `docs/studies/`.

---

## Phase 5: Handoff
13. **Notify User**: Present a summary with the Top 3 insights and recommended next steps.

---
> [!NOTE]
> For long documents, analysis should be done in chunks to ensure high fidelity and avoid context loss.