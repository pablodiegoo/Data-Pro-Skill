# `/dps-inject-open [text or file]` — Qualitative Injection into Quant Segments

Categorizes open-ended verbatims *inside* the quantitative segments established by `/dps-setup`. Quantitative segments form the **Analytical Spine**; qualitative themes and verbatims are branches attached to that spine — never standalone sections.

---

## 1. Pipeline

```
Open-Ended Responses (CSV/XLSX/ODS column or inline text) + setup_segments.csv
    → scripts/qualitative_categorizer.py
    → quali_themes.csv + quali_verbatims.json + quali_report.md
```

---

## 2. Prerequisites & Hard Gates

1. **Manifesto Gate:** `.dps/outputs/setup/setup_manifest.json` (or `setup_segments.csv`) MUST exist. If absent, halt and output: `"Execute /dps-setup first to define the quantitative segments."`
2. **Article 4 Gate ($N < 30$ Percentage Prohibition):** Whenever a qualitative segment or sub-sample has valid respondents $N < 30$, report theme frequency strictly as raw counts: `"mentioned by n of N participants"` (`"mencionado por n de N participantes"`). **NEVER** compute or display `%` symbols when $N < 30$. When segment $N \ge 30$, report both raw count `n of N` and `X.X% (±Y.Y%, 95% CI)` (`Article 1`).
3. **Minimum Verbatim Gate:** Every reported theme requires at least **2 literal verbatim quotes** in the participants' exact words. Single mentions (`n = 1`) must be grouped under `### Isolated Mentions` (`### Menções Isoladas`) and never promoted to standalone themes.
4. **Silence Gate:** Any manifesto segment with `0` open-ended responses must be explicitly documented with a **Silence Note** explaining the absence of qualitative data.

---

## 3. Execution Steps

1. **Execute Deterministic Categorizer & Verbatim Extractor:**
   ```bash
   python3 .dps/scripts/qualitative_categorizer.py <data_file> --text-col "<open_col>" --segment-col "<seg_col>" --segments .dps/outputs/setup/setup_segments.csv -o .dps/outputs/quali/
   ```
   *(Automatically applies Portuguese/English stopwords from `references/analysis/stopwords_pt.txt`, clusters recurring stems/themes, maps responses to manifesto segments, and enforces the $N < 30$ formatting rule.)*
2. **Run 4-Stage Invisible Agent Loop (Statistician $\rightarrow$ Critic $\rightarrow$ Anthropologist $\rightarrow$ Tufte Designer):**
   - **Statistician:** Audits response count $n_{\text{quali}}$ against segment $N_{\text{quant}}$ ($n_{\text{quali}} \le N_{\text{quant}}$) and flags segments where $n_{\text{quali}} < 30$.
   - **Critic:** Enforces **Article 3** (zero fluff), **Article 4** (zero `%` for $N < 30$, $\ge 2$ literal verbatims per theme), and blocks confirmation bias or paraphrased quotes.
   - **Anthropologist (`agents/agent-anthropologist.md`):** Names themes using concrete participant language (e.g., *"Post-Trial Price Shock"*, not *"Economic Factor"*), extracts representative literal verbatims with participant context, identifies emergent **Archetypes** (Name, Core Need, Pain Point, Quantitative Segment), and writes **Silence Notes**.
   - **Tufte Designer:** Renders segment-nested subsections ready for inclusion in `final_report.md` and `final_report.html`.

---

## 4. Output Format (`quali_report.md`)

```markdown
### Qualitative Enrichment — {Segment Name}

**Quantitative Anchor:** {Segment Name} from Manifesto ($N_{\text{segment}} = {N_{\text{seg}}}$, Core Metric: {metric_val}) · **Responses Analyzed:** {n_quali} of {N_seg} participants

#### Theme 1: {Concrete Theme Name} — mentioned by {k} of {n_quali} participants
> "{Literal verbatim quote 1 in participant's exact words}" — {Participant ID / Demographic / Score context}
> "{Literal verbatim quote 2 in participant's exact words}" — {Participant ID / Demographic / Score context}

> **Margin Note:** {1–3 sharp sentences explaining how this qualitative theme accounts for the quantitative metric or standardized residual $z_{ij}$ observed in {Segment Name}.}

#### Theme 2: {Concrete Theme Name} — mentioned by {m} of {n_quali} participants
> "{Literal verbatim quote 1}" — {Context}
> "{Literal verbatim quote 2}" — {Context}

> **Margin Note:** {Interpretive connection to business decision.}

#### Isolated Mentions ({Segment Name})
- Single-respondent observations ($n = 1$, below theme promotion threshold): *"{short quote}"* ({Context}).

### Qualitative Enrichment — {Segment With Zero Responses}

**Responses Analyzed:** 0 of {N_seg} participants
> **Margin Note — Silence Finding:** Zero open-ended responses recorded in `{Segment Name}` ($N = {N_{\text{seg}}}$). Non-response on spontaneous feedback in this segment indicates passive detachment rather than active friction — verify via structured prompts in the next wave.
```

---

## 5. Completion Criterion

`.dps/outputs/quali/quali_themes.csv`, `quali_verbatims.json`, and `quali_report.md` exist; every segment from `setup_manifest.json` is represented; every theme has $\ge 2$ literal verbatims; and zero `%` symbols appear on any qualitative sub-sample with $N < 30$.
