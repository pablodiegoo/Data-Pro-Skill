# Invisible Agent Loop — Internal Verification Protocol

Every analytical command (`/dps-setup`, `/dps-cross`, `/dps-execute`, `/dps-advanced`, `/dps-inject-open`, `/dps-export`) runs an internal multi-agent verification loop before emitting output.

**Golden Rule:** Stage 1 (**Statistician**), Stage 2 (**Critic**), and Stage 3 (**Anthropologist**) are strictly internal. Never print their intermediate reports to the user. The user sees **ONLY Stage 4 (Tufte Designer)**.

---

## 1. Loop Topologies by Mode

### A. Discovery Mode (`/dps-grill` / `/dps-clarify`)
```
User ↔ [0. Data Griller (agent-griller.md)] → column_mapping.json + 00_data_glossary.md + clarify_notes.md
```
Runs **Fact Reconnaissance** first, then interviews the user in **Frontier Rounds** across the 5-branch **Design Tree**.

### B. Quantitative Default (`/dps-mode:quant`)
```
User → [Orchestrator] → [1. Statistician] → [2. Critic] → [4. Tufte Designer] → User Output
                             ↑                   │
                             └─── (Hard Block) ──┘
```

### C. Qualitative Enriched (`/dps-inject-open` or `/dps-mode:quali`)
```
User → [Orchestrator] → [1. Statistician] → [2. Critic] → [3. Anthropologist] → [2. Critic Quali Gate] → [4. Tufte Designer] → User Output
```

### D. Executive Strategy Post-Processor (`/dps-mode:strategy`)
```
Completed Validated Analysis → [Strategist (agent-strategist.md)] → [4. Tufte Designer] → Strategic Output
```

---

## 2. Stage Contracts & Handoff Gates

| Stage | Agent File | Inputs | Mandatory Checks | Output / Gate |
| :---: | :--- | :--- | :--- | :--- |
| **0** | [`agents/agent-griller.md`](../agents/agent-griller.md) | Raw dataset + user prompt | Run `--profile` first; never ask user for dataset facts; ask full **frontier** with `❓ Q#` and `➡️` defaults | Writes `column_mapping.json`, `00_data_glossary.md`, `clarify_notes.md` |
| **1** | [`agents/agent-statistician.md`](../agents/agent-statistician.md) | Dataset + `setup_manifest.json` | Verify **Valid Base** ($n$) vs **Total Base** ($N$); apply weights (`Article 7b`); compute 95% CI MoE (`Article 1`); check $N \ge 30$ & Shapiro-Wilk normality (`Article 5`); check **Branching Overlap** (`Article 7c`); compute test stat, exact $p$, effect size, and **Standardized Residuals** $z_{ij}$ | Internal `Statistician Report` passed to Critic |
| **2** | [`agents/agent-critic.md`](../agents/agent-critic.md) | Stage 1 Report + [`constitution.md`](../constitution.md) | Mechanical Yes/No audit across **Articles 1–8**: MoE present? $p < 0.05$ + effect size for significance claims? Zero forbidden fluff phrases? Zero `%` on quali $N < 30$? Non-parametric fallback when $N < 30$? Straight-lining (6a), $100\% \pm 0.5\%$ sum (6b), $>10\%$ missingness (6c) disclosed? | **PASS** $\rightarrow$ Stage 3/4; **BLOCK** $\rightarrow$ return to Stage 1/3 with exact violation |
| **3** | [`agents/agent-anthropologist.md`](../agents/agent-anthropologist.md) | Open-ended text + `setup_segments.csv` | Attach every theme to a manifesto segment; raw counts (`n of N`) when $N < 30$; $\ge 2$ literal `"verbatims"` per theme; record **Silence Notes** for $0$-response segments | Internal `Anthropologist Report` audited by Critic, then passed to Designer |
| **4** | [`agents/agent-tufte-designer.md`](../agents/agent-tufte-designer.md) | Validated Stage 1–3 Reports + [`tufte-rules.md`](tufte-rules.md) + [`design-schools.md`](design-schools.md) | Headline finding in every heading; self-explanatory tables with `N` and `±MoE%`; inline SVG / Mermaid charts; 1–3 sentence **Margin Notes** answering *"So what?"*; **Print-Ready HTML** in the setup-selected **Data Design School** (`tufte` default, `few`, `knaflic`, `swiss`, or `editorial`) on `/dps-export` | **Sole user-visible output** |
