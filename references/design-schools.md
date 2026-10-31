# Data Design Schools — Visual, Typographic & Chart Grammar Reference

Data-Pro-Skill supports **five canonical Data Design Schools**. While **Edward Tufte (`tufte`)** is the default publication standard, the user can pick any of the five schools during `/dps-setup`, `/dps-grill`, or `/dps-export` (or via `node bin/install.js` and `--school <id>`), and switch between them interactively inside `final_report.html`.

All five schools strictly obey the statistical and methodological laws of [`constitution.md`](../constitution.md) (**Articles 1–8**: mandatory 95% CI `±MoE%`, exact $p$-value + effect size, **Deletion Test**, $N < 30$ qualitative raw counts, non-parametric fallbacks, Article 6 Quality Gates, Article 7 Survey Governance, and Article 8 Print-to-PDF running headers and footers).

---

## 1. The 5 Canonical Data Design Schools (Quick Selector)

| # | School ID (`--school`) | Aliases | Founding Authority | Primary Chart Grammar | Layout & Callout Architecture | Best For |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **`tufte`** *(Default)* | `classic`, `sidenotes` | **Edward R. Tufte** (*The Visual Display of Quantitative Information*, 1983) | **Cleveland Dot Plot** with 95% CI whiskers, **Sparklines**, **Small Multiples** | Ivory `#fffff8`, Palatino serif, 58% body + 36% right column with floating `§N` **Margin Notes**, classic **Booktabs Tables** | Academic research, scientific studies, public policy, long-form analytical reports |
| **2** | **`few`** | `perceptual`, `bullet`, `bi` | **Stephen Few** (*Show Me the Numbers*, 2004; *Information Dashboard Design*, 2006) | **Bullet Graphs** (qualitative bands + measure bar + `|` target line + 95% CI) | Alabaster `#f8fafc`, Inter/Source Sans, **100% full-width perceptual grid**, compact tables, inline `PERCEPTUAL DIAGNOSTIC` strips | Business Intelligence (BI), operational KPI tracking, multi-metric benchmarking |
| **3** | **`knaflic`** | `storytelling`, `swd`, `executive` | **Cole Nussbaumer Knaflic** (*Storytelling with Data*, 2015) | **Preattentive Focus Horizontal Bars** (muted grey context `#cbd5e1` + bold focal `#1e40af`/`#ea580c`) | Pure white `#ffffff`, Montserrat/Open Sans, centered single-column narrative, **Action-Title Banners** & `💡 KEY TAKEAWAY` cards | C-suite executive presentations, board decks, stakeholder alignment, strategy briefs |
| **4** | **`swiss`** | `bertin`, `muller-brockmann`, `grid` | **Josef Müller-Brockmann** (*Grid Systems*, 1981) & **Jacques Bertin** (*Sémiologie Graphique*, 1967) | **Bertin Retinal Lollipops & Reorderable Matrices** (`■` above / `●` below mean) | Architect stone `#f5f5f0`, Neo-Grotesque Helvetica/Inter + monospace, **exposed `1.5px`/`4px` black modular grid**, Vermilion `#e63946` & Cobalt `#1d3557` | Design-forward research manifestos, urban/demographic studies, multivariate matrices |
| **5** | **`editorial`** | `economist`, `ft`, `journalism` | **The Economist Style Guide** & **Financial Times Visual Vocabulary** (Alan Smith) | **Editorial Crimson-Rule Lollipop & Range Charts** with `Source:` footlines | Warm newsprint `#fcf8f2`, **signature `6px` crimson top bar (`#e3120b`)**, **Kicker + Headline + Standfirst**, right-column `EDITORIAL BRIEF` sidebars | Market research publications, public opinion polling, industry benchmark reports |

---

## 2. Detailed Specification by School

### School 1: `tufte` — Edward Tufte (Classic Data-Ink & Sidenote School)
- **Stylesheet:** [`references/styles/tufte.css`](styles/tufte.css)
- **Visual Philosophy:** Maximize **Data-Ink Ratio**; eliminate chartjunk, heavy gridlines, and decorative boxes. Integrate prose, tables, and vector graphics seamlessly on warm ivory paper (`#fffff8`), placing numbered sidenotes (`<aside class="margin-note">`) in a 36% right column beside the 58% prose column.
- **Typography:** `et-book, Palatino, Georgia, serif` for body prose; `"Gill Sans", "Helvetica Neue", Inter, sans-serif` for tables and KPI cards.
- **Table Rules:** Classic `booktabs` horizontal rules (`2px` top, `1px` header bottom, `2px` bottom, **zero vertical borders**, `tabular-nums`).
- **Signature SVG Graphics (`tufte_viz.py --school tufte`):** Cleveland dot plots with dotted horizontal leader lines, 95% CI error whiskers (`±MoE%`), dashed grand-mean reference lines, inline sparklines, and small multiples.

### School 2: `few` — Stephen Few (Perceptual Dashboard & Bullet-Graph School)
- **Stylesheet:** [`references/styles/few.css`](styles/few.css)
- **Visual Philosophy:** Engineered around human preattentive visual perception (Gestalt proximity, enclosure, alignment, and muted vs. alert saturation). Eliminates asymmetric empty margins in favor of a **100% full-width analytical grid** so eyes scan directly across metrics without scrolling past whitespace.
- **Typography:** Clean humanist sans-serif (`Inter`, `Source Sans Pro`, `Segoe UI`) across headings, body, and tables for high-speed numeric scanning.
- **Table & Callout Rules:** High-density full-width tables framed in `1px solid #cbd5e1` with uppercase slate headers (`#f1f5f9`). Margin notes render as full-width inline **Perceptual Diagnostic** strips (`border-left: 4px solid #0d9488`) directly below the table they annotate.
- **Signature SVG Graphics (`tufte_viz.py --school few`):** **Stephen Few Bullet Graphs** combining three qualitative background performance bands (`#cbd5e1` / `#e2e8f0` / `#f1f5f9`), a central quantitative measure bar (dark slate `#0f172a`, or preattentive crimson `#dc2626` when significantly lagging), a perpendicular vertical target/mean marker (`|`), and 95% CI whiskers.

### School 3: `knaflic` — Cole Nussbaumer Knaflic (Storytelling with Data / Preattentive Focus School)
- **Stylesheet:** [`references/styles/knaflic.css`](styles/knaflic.css)
- **Visual Philosophy:** **Declutter + Focus Attention**. Never force an executive to hunt for the insight: push all baseline, context, and non-significant categories into **recessive grey (`#cbd5e1` / `#64748b`)**, and apply **one bold preattentive focal color** (`#1e40af` Executive Blue for the primary driver/leader, `#ea580c` Action Rust for the critical pain point) exclusively to the finding that drives Monday-morning action.
- **Typography:** Bold geometric sans-serif (`Montserrat`, `Plus Jakarta Sans`) for Action-Title headings; `Open Sans` / `Inter` for clean single-column executive prose.
- **Table & Callout Rules:** Decluttered borderless tables where the lead/focal row and total row are highlighted in soft blue tint (`#eff6ff`) with bold numerals while secondary rows recede in `#475569`. Margin notes render as prominent **`💡 KEY TAKEAWAY` Callout Cards**.
- **Signature SVG Graphics (`tufte_viz.py --school knaflic`):** **SWD Preattentive Focus Horizontal Bar Charts** (zero gridlines, grey context bars, saturated focal bar with `★` marker and direct end-of-bar value + `±MoE` labels).

### School 4: `swiss` — Swiss Grid & Jacques Bertin (International Typographic & Semiology School)
- **Stylesheet:** [`references/styles/swiss.css`](styles/swiss.css)
- **Visual Philosophy:** Combines Josef Müller-Brockmann's **Mathematical Modular Grid** with Jacques Bertin's **Semiology of Graphics** (the 7 retinal variables: planar position, size, value, texture, color, orientation, shape). Treats the report as an architectural blueprint with exposed `1.5px` and `4px` solid black (`#0a0a0a`) structural grid lines.
- **Typography:** Neo-Grotesque sans-serif (`Helvetica Neue`, `Helvetica`, `Inter`) flush-left ragged-right, uppercase tightly-tracked section titles, and `JetBrains Mono` / `Consolas` monospace index markers (`01 // SECTION`, `[§01 // GRID MODULE]`).
- **Table & Callout Rules:** Exposed architectural grid tables (`2px solid #0a0a0a` outer border, `1px solid #0a0a0a` cell gridlines, inverted `#0a0a0a` black header bar with `#ffffff` white monospace text). Right-column notes render as hard-edged modular boxes with `3px 3px 0 #e63946` International Vermilion offset shadows.
- **Signature SVG Graphics (`tufte_viz.py --school swiss`):** **Bertin Retinal Lollipop & Coordinate Grids** with exposed rectangular plot frames, `2px` black stems, dual retinal shape + color coding (`■` Cobalt `#1d3557` for above-benchmark, `●` Vermilion `#e63946` for below-benchmark), and monospace right-aligned numeric columns.

### School 5: `editorial` — The Economist / Financial Times Editorial (Data Journalism School)
- **Stylesheet:** [`references/styles/editorial.css`](styles/editorial.css)
- **Visual Philosophy:** Authoritative data journalism modeled on *The Economist* and the *FT Visual Vocabulary*. Anchored by warm newsprint/salmon-ivory paper (`#fcf8f2`), the iconic **`6px solid #e3120b` Economist Crimson top bar** with rectangular red section tags above every `h2`, and a three-tier **Kicker + Headline + Standfirst** hierarchy.
- **Typography:** Editorial sans-serif (`IBM Plex Sans`, `Franklin Gothic`, `Helvetica Neue`) for kickers, headlines, tables, and chart labels, paired with `Merriweather` / `Charter` / `Georgia` serif for narrative journalism.
- **Table & Callout Rules:** Top `3px solid #e3120b` crimson bar on all tables and chart containers, warm `#dfd8ce` horizontal rules, and right-column **`EDITORIAL BRIEF`** sidebars (`background: #f4ece1; border-top: 3px solid #e3120b`).
- **Signature SVG Graphics (`tufte_viz.py --school editorial`):** **Editorial Crimson-Tag Lollipop & Range Charts** featuring the top-left red rectangle (`32×5px #e3120b`), bold headline + italic standfirst, subtle vertical reference gridlines, `#005689` editorial navy bars with `#e3120b` crimson lead highlight, and mandatory `Source: Data-Pro-Skill Survey Analysis (95% CI)` footlines.

---

## 3. How to Select or Switch Schools

1. **During Interactive Setup (`/dps-setup` or `/dps-grill`):**
   - Ask the user which **Data Design School** matches their audience (or pass `--school <tufte|few|knaflic|swiss|editorial>`):
     ```bash
     # Pick interactively in terminal during setup:
     python3 .dps/scripts/quant_analyzer.py <data.csv> --pick-school -o .dps/outputs/setup/

     # Or lock a specific school directly:
     python3 .dps/scripts/quant_analyzer.py <data.csv> --school knaflic -o .dps/outputs/setup/
     ```
   - The selection is saved to `.dps/outputs/setup/design_school.json`, `setup_manifest.json`, and `00_profile.json`, automatically driving `/dps-export`.
2. **During Project Installation (`node bin/install.js`):**
   - The interactive installer prompts for the default **Data Design School** (`1–5`, defaulting to `1. tufte`), or accepts `node bin/install.js --school few`, saving it to `.dps/config.json`.
3. **During Export (`/dps-export`):**
   - Automatically inherits the school locked in `/dps-setup`, or overrides it via `--school`:
     ```bash
     python3 .dps/scripts/final_report_generator.py --input .dps/outputs/ -o .dps/outputs/export/ --school editorial
     ```
4. **Live Inside `final_report.html`:**
   - Every exported `final_report.html` embeds all five stylesheets and includes an interactive **`🎨 School:`** dropdown in the top `.no-print` toolbar so stakeholders can switch between `Edward Tufte`, `Stephen Few`, `Cole Knaflic (SWD)`, `Swiss Grid / Bertin`, and `Economist / FT Editorial` in real time before printing to PDF (`Ctrl+P`).
