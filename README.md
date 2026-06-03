<div align="center">

# Data-Pro-Skill v2

**A multi-harness meta-prompt for market research data analysis. Transforms raw quantitative and qualitative data into dense, Tufte-style analytical documents — zero prose fluff, maximum data density.**

**Works on any AI harness: OpenCode, Gemini, Codex, Hermes, OpenClaw, Claude.**

<br>

*"Analysis that used to take hours of manual tweaking now comes out publication-ready."*

</div>

---

## Command Pipeline

Four commands. Each anchors the next. No analysis can contradict previously established metrics.

| Command | What it does |
|---------|-----------|
| `/dps-setup` | Generates the quantitative manifesto (YAML frontmatter + segment matrix) |
| `/dps-cross [VarX] x [VarY]` | Slices variables with dense Tufte-style crosstab tables |
| `/dps-inject-open [text]` | Categorizes open-ended responses within existing quant segments |
| `/dps-export` | Consolidates everything into clean Markdown, ready for Quarto/LaTeX/PDF |

### Specialized Modes

| Command | Persona activated |
|---------|----------------|
| `/dps-mode:quant` | Senior Statistician — correlations, crosstabs, NPS, Churn, CSAT |
| `/dps-mode:quali` | Anthropologist — latent needs, sentiment, archetypes, journeys |
| `/dps-mode:strategy` | BI Director — actionable business recommendations |

---

## Example Output (Tufte Style)

```markdown
---
project: "Churn Survey — Q2 2026"
sample_size: 1450
metrics: [NPS, Frequency, Age, Reason]
---

## Churn Distribution by Age Group

The cancellation peak is in 18-24 years (45% of total Churn, only 20% of the base).

| Age Group | N  | Churn (%) | Qualitative Target |
| :---      |:--:| :--:      | :---               |
| 18-24     | 290 | 45%       | Price Barrier / Perceived Value |
| 25-34     | 580 | 12%       | Lack of Time / Routine Change   |
| 35+       | 580 | 5%        | Technical Usability Issues      |

> **Margin Note:** Qualitative analysis of Segment A reveals a direct correlation between
> rejection and post-trial pricing. Recurring terms: "expensive", "student", "readjustment".
```

---

## Architecture

### Invisible Agent Loop

The user interacts only with the final output. Three agents run silently per command:

```
User → [Orchestrator] → [Statistician] → [Critic] → [Tufte Designer]
                                                          ↓
                                                   Output to user ONLY
```

| Agent | Responsibility |
|--------|---------------|
| **Statistician** | Validates numerical consistency, calculates distributions, selects tests |
| **Critic** | Detects biases, spurious correlations, overgeneralizations, missing data |
| **Tufte Designer** | Synthesizes output — zero fluff, maximum data density, margin notes |

### Document-Driven Context

Each command writes to a shared document. The `/dps-setup` manifesto is the single source of truth — no subsequent analysis can contradict established metrics. This eliminates "context rot" (quality degradation as AI fills its context window).

---

## Data Constitution

Non-negotiable rules defined in `constitution.md`:

- **Statistical Rigor:** Margin of error, minimum sample size, confidence level (p < 0.05)
- **Qualitative Rigor:** Prohibition of generalizations from small samples (e.g., "70% of respondents" when N=10)
- **Bias Treatment:** Confirmation bias detection, spurious correlation flagging
- **Prose Fluff:** Prohibition of phrases like "It's important to note..." or "Based on the data..."

---

## Multi-Harness Compatibility

Designed to work on any AI runtime — no platform-specific features:

| Harness | Status |
|---------|:------:|
| **OpenCode** | ✓ |
| **Gemini CLI** | ✓ |
| **Codex CLI** | ✓ |
| **Claude Code** | ✓ |
| **Hermes** | ✓ |
| **OpenClaw** | ✓ |

No XML. No proprietary syntax. YAML frontmatter + pure Markdown only.

---

## Getting Started

```bash
# Download + run (no npm account needed, Node.js required):
curl -fsSL -o /tmp/dps-install.js https://raw.githubusercontent.com/pablodiegoo/Data-Pro-Skill/main/bin/install.js && node /tmp/dps-install.js

# Or manually copy the files:
# git clone https://github.com/pablodiegoo/Data-Pro-Skill.git
# cp Data-Pro-Skill/SKILL.md Data-Pro-Skill/constitution.md ~/.config/opencode/skills/data-pro-skill/
```

Restart your harness, then start any session with `/dps-setup`.

---

## Project Structure

```
├── SKILL.md              # Main meta-prompt (639 lines, 10 commands)
├── constitution.md        # Statistical rigor rules (6 articles, 8 rules)
├── agents/                # Agent definitions (Statistician, Critic, Tufte, etc.)
├── commands/              # Workflow commands
├── docs/                  # Extended documentation
├── dps-engine/              # GSD engine (workflows, templates, references)
└── .planning/             # Project planning (ROADMAP, STATE, etc.)
```

---

## Getting Started

1. Copy `SKILL.md` and `constitution.md` to your harness's skills directory
2. Start any session with `/dps-setup` and provide your data
3. Run `/dps-cross` to slice variables
4. Use `/dps-inject-open` for qualitative data
5. Run `/dps-export` to get a publication-ready Markdown file

---

## Inspiration

Built by combining the best of four approaches:

| Source | Contribution |
|--------|-------------|
| **Edward Tufte** | High data density, margin notes, zero fluff output |
| **GSD (Get Shit Done)** | Invisible agents, discuss→plan→execute→verify loop |
| **Spec-Kit (GitHub)** | `/dps-clarify` — hypothesis exploration before touching data |
| **BMAD Method** | Persona separation (`/dps-mode:quant`, `/dps-mode:quali`) |

---

## License

MIT License. See [LICENSE](LICENSE).

---

<div align="center">

**Raw data in. Publication-ready analytical documents out. No fluff.**

</div>
