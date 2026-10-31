# `/dps-export` — Consolidate & Export Print-Ready Multi-School HTML Report

Consolidates all session artifacts into the project's native language (`pt-BR`, `en`, or `es`) and compiles the primary publication deliverable: a self-contained **Print-Ready HTML** report (`final_report.html`) styled in the project's chosen **Data Design School** (`tufte` [Edward Tufte — Default], `few` [Stephen Few], `knaflic` [Cole Knaflic / Storytelling with Data], `swiss` [Swiss Grid / Jacques Bertin], or `editorial` [The Economist / FT Editorial]; see [`references/design-schools.md`](design-schools.md)) and engineered to print directly to PDF with standard running headers, footers, and page-break discipline (`Constitution Article 8`), paired with its clean source Markdown (`final_report.md`).

---

## 1. Pipeline

```
All Intermediate Outputs (.dps/outputs/setup, cross, advanced, quali, strategy) + [design_school.json / --school]
    → scripts/final_report_generator.py   (Consolidates final_report.md + verification_report.json)
    → scripts/tufte_viz.py                (Generates school-specific SVGs in export/charts/)
    → scripts/tufte_html.py               (Compiles self-contained final_report.html with all 5 school CSS themes + Print Frame)
```

```bash
python3 .dps/scripts/final_report_generator.py --input .dps/outputs/ -o .dps/outputs/export/ [--school <tufte|few|knaflic|swiss|editorial>]
python3 .dps/scripts/tufte_viz.py --input .dps/outputs/ --charts-dir .dps/outputs/export/charts/ [--school <tufte|few|knaflic|swiss|editorial>]
python3 .dps/scripts/tufte_html.py --md .dps/outputs/export/final_report.md [--school <tufte|few|knaflic|swiss|editorial>]
```

---

## 2. Automatic Native Language Detection

Intermediate analytical schemas (`setup_manifest.json`, `00_profile.json`, `cross_stats.json`) use canonical English keys. The exported report (`final_report.md` and `final_report.html`) is rendered in the **dataset's native language**, detected automatically from column labels, `column_mapping.json`, and verbatim content:

| Detected Dataset Signals | Export Language (`lang`) | Typography & Labels |
| :--- | :---: | :--- |
| Portuguese terms (*bairro, renda, idade, satisfação, morador, nota*) | `pt-BR` | *Nota de Margem*, *Base Válida*, *Intervalo de Confiança (IC 95%)* |
| English terms (*income, age, satisfaction, segment, household, churn*) | `en` | *Margin Note*, *Valid Base*, *95% Confidence Interval (95% CI)* |
| Spanish terms (*edad, ingresos, satisfacción, hogar, barrio*) | `es` | *Nota al Margen*, *Base Válida*, *Intervalo de Confianza (IC 95%)* |

---

## 3. Canonical Document Architecture

`final_report.md` and `final_report.html` assemble available session outputs in this exact order:

1. **YAML Frontmatter & Tufte Metadata Banner:** `project`, `framework`, `sample_size`, `global_moe_95ci`, `confidence_level`, `export_date`, `metrics_tracked`, `segments`, `constitution_status`.
2. **Executive Summary & Headline KPI Strip:** If `/dps-mode:strategy` ran, leads with the 4-sentence Executive Summary and KPI cards (Sample $N$, Global MoE, Primary Outcome / NPS, Top Driver).
3. **Methodology, Governance & Data Glossary:** Documents **Schema Mapping** (`column_mapping.json`), **Valid Base** vs **Total Base** rules, weighting posture (`Article 7b`), and **Article 6 Data Quality Gates** (6a Straight-Lining, 6b Percentage Sums, 6c Missingness).
4. **Quantitative Manifesto & Segment Matrix (`/dps-setup`):** Canonical **Segment Matrix** + per-variable distribution **Booktabs Tables** + inline SVG Cleveland dot plots and sparklines.
5. **Bivariate Crosstabs & Hypothesis Tests (`/dps-cross` / `/dps-execute`):** Effect-size leaderboard + detailed contingency/group **Booktabs Tables**, compiled inline SVG charts, **Standardized Residual** callouts ($|z_{ij}| \ge 1.96$), and **Margin Notes**.
6. **Deep Survey Science (`/dps-advanced`, when present):** **Pure Sentiment Stack** (**Ipsative** + **Halo Residuals**), **Priority Matrix** SVG & table, **Key Drivers**, **Dual Clustering** personas, and **TURF** reach curve.
7. **Qualitative Segment Injections (`/dps-inject-open`, when present):** Segment-anchored thematic sections with literal verbatims, raw counts (`n of N` for $N < 30$), emergent archetypes, and silence notes.
8. **Strategic Action Plan (`/dps-mode:strategy`, when present):** Key Business Findings, Impact $\times$ Effort **Prioritization Matrix**, Risk Assessment, and **Monday Morning Action Plan**.
9. **Constitution Verification Stamp (`verification_report.json`):** Mechanical audit pass across Articles 1–8.

---

## 4. Multi-School HTML & Print-to-PDF Engineering Standards (`Article 8`)

`final_report.html` replaces legacy PDF/LaTeX/Quarto toolchains with a single, zero-dependency, self-contained HTML file that renders in the project's locked **Data Design School** (`tufte` default, `few`, `knaflic`, `swiss`, or `editorial` — see [`references/design-schools.md`](design-schools.md)) on screen and prints directly to a publication-grade PDF (`Ctrl+P` $\rightarrow$ *Save as PDF* or headless Chromium):

1. **5 Canonical Data Design Schools (`references/styles/*.css`):**
   - **`tufte` (`tufte.css` — Default):** `Palatino/Georgia` serif prose + `Gill Sans` tables, `#fffff8` ivory background, 58%/36% asymmetric grid with floating `<aside class="margin-note">` sidenotes, `booktabs` tables, and **Cleveland dot plots** with 95% CI whiskers.
   - **`few` (`few.css`):** `Inter / Source Sans` humanist sans-serif, `#f8fafc` full-width perceptual BI grid, **Stephen Few Bullet Graphs** (qualitative range bands + measure bar + target marker), compact tables, and inline `PERCEPTUAL DIAGNOSTIC` callout strips.
   - **`knaflic` (`knaflic.css`):** `Montserrat / Open Sans` executive narrative on `#ffffff`, decluttered **grey context (`#cbd5e1`) + bold preattentive focal accent (`#1e40af` / `#ea580c`)**, Action-Title `h2` banners, and `💡 KEY TAKEAWAY` callout cards.
   - **`swiss` (`swiss.css`):** `Helvetica Neue / Inter` Neo-Grotesque + monospace indices on `#f5f5f0`, exposed `1.5px`/`4px` black modular grid hairlines, inverted black table headers, and **Jacques Bertin retinal lollipop matrices** (Vermilion `#e63946` & Cobalt `#1d3557`).
   - **`editorial` (`editorial.css`):** `IBM Plex Sans` headers + `Merriweather` editorial serif on warm `#fcf8f2` newsprint, signature **`6px` crimson top bar (`#e3120b`)**, Kicker + Headline + Standfirst hierarchy, `EDITORIAL BRIEF` sidebars, and horizontal lollipop range charts with `Source:` footlines.
2. **100% Inline Vector Charts (`tufte_viz.py` & `tufte_html.py`):**
   - All charts from `tufte_viz.py` AND all Markdown `mermaid` (`xychart-beta`, `pie`) blocks are compiled directly into crisp inline `<svg>` elements styled for the active school inside `final_report.html` — zero external JS or image files required.
3. **Standard Print-to-PDF Running Headers & Footers (`Print Frame`):**
   - Combines W3C CSS Paged Media `@page` margin rules (`@top-left`, `@top-right`, `@bottom-left`, `@bottom-right`) with the universal HTML `<table class="print-frame">` (`<thead>` header-spacer + `<tfoot>` footer-spacer) and `position: fixed` `<header class="print-running-header">` / `<footer class="print-running-footer">` bars in `@media print`:
     - **Running Header on Every PDF Page:** Project Title · Framework (`Data-Pro-Skill v2.1`) | Sample $N$ · 95% CI (`±MoE%`) · Export Date.
     - **Running Footer on Every PDF Page:** Constitution Audit Badge (`Articles 1–8 Verified · {School} Standard`) | Confidentiality / Source Note & Page Counter.
   - Enforces `break-inside: avoid; page-break-inside: avoid` on `table`, `figure`, `.chart-container`, `.margin-note`, `.kpi-grid` and `break-after: avoid` on `h1–h4`, plus `thead { display: table-header-group; }` so multi-page tables repeat their column headers cleanly across page breaks.
   - Includes a screen-only (`class="no-print"`) floating utility bar with a live **`🎨 School:`** switcher dropdown (pre-selected to the setup school, allowing instant preview across all 5 schools), a **"📐 Toggle Callouts"** button, and a **"🖨️ Print / Save as PDF"** button (`window.print()`).

---

## 5. Outputs Generated & Completion Criterion

| Output File | Format | Purpose |
| :--- | :--- | :--- |
| `.dps/outputs/export/final_report.html` | Self-Contained Tufte HTML + Inline SVGs + Print Frame | Primary publication deliverable — view in browser or Print to PDF with headers/footers |
| `.dps/outputs/export/final_report.md` | Pure Tufte Markdown + Mermaid | Version-control & GitHub/GitLab source document |
| `.dps/outputs/export/verification_report.json` | JSON Audit Manifest | Mechanical pass/fail verification across Articles 1–8 |

- **Completion Criterion:** `final_report.html`, `final_report.md`, and `verification_report.json` exist; `final_report.html` contains zero raw YAML frontmatter, zero unrendered `mermaid` code fences, embedded Tufte CSS with `@page` and `.print-frame` running header/footer structures, and passes all 8 **Data Constitution** gates.
