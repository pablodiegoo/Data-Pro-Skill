# Tufte & Multi-School Output & Print-Ready HTML Formatting Rules

Every user-visible output from the **Designer** (`final_report.html`, `final_report.md`, and interactive command outputs) obeys Edward Tufte's foundational principles of analytical design (**maximize Data-Ink Ratio, eliminate chartjunk and prose fluff, make every table self-explanatory, and engineer HTML to print to PDF with standard running headers and footers**), while supporting **five selectable Data Design Schools** ([`references/design-schools.md`](design-schools.md)) chosen during `/dps-setup` (`tufte` [Default], `few`, `knaflic`, `swiss`, or `editorial`).

---

## 1. Positive Prose Steering & The Deletion Test (`Article 3`)

Open every section, paragraph, and **Margin Note** with a **numeric finding**, a **named segment**, or a **falsifiable analytical claim**.

### The 8 Forbidden Throat-Clearing Phrases (EN / PT / ES)
Never start a paragraph or sentence with:
1. *"It's important to note that..."* / *"É importante notar que..."*
2. *"Based on the data provided..."* / *"Com base nos dados fornecidos..."*
3. *"Interestingly..."* / *"Interessantemente..."*
4. *"It is worth mentioning..."* / *"Vale mencionar que..."*
5. *"One can observe that..."* / *"Pode-se observar que..."*
6. *"The data suggests that..."* / *"Os dados sugerem que..."*
7. *"In conclusion..."* / *"Em conclusão..."*
8. *"As we can see..."* / *"Como podemos ver..."*

**The Deletion Test:** If removing a sentence loses no number, no named segment/entity, and no analytical conclusion, delete the sentence immediately.

---

## 2. Booktabs Tables (`Article 1`, `Article 6b`, `Article 8`)

Every analytical table follows classic `booktabs` typographic discipline:
- **Conclusion-First Section Heading:** The heading above the table states the finding (`## Origin × Spend — Tourists Spend R$ 48.20 More Per Capita Than Residents`), never a generic label (`## Crosstab of Origin and Spend`).
- **Mandatory Columns:**
  1. Left-aligned category/segment name (`:---`)
  2. Center/right-aligned sample size `N` (`:---:` or `---:`)
  3. Proportions with 95% CI Margin of Error `X.X% (±Y.Y%, 95% CI)` or scale `Mean ± SD (Median, IQR)`
  4. Diagnostic/Test or Anomaly column ($z_{ij}$, Priority Score, or core takeaway)
- **Mandatory Footer Row:** Every table ends with a bold **Valid Base** (`**Valid Base**` / `**Base Válida**`) row and, when $n_{\text{valid}} < N_{\text{total}}$, a **Total Base** disclosure row. For multi-response (`RM`) tables, explicitly note: `_(Multiple Response — sum exceeds 100%, Base = N respondents)_`.
- **Visual Styling in HTML (`tufte.css`):**
  - Top border: `2px solid #111111`
  - Header bottom border: `1px solid #111111`
  - Subtle row hairlines: `1px solid #e6e6dc`
  - Bottom border: `2px solid #111111`
  - **Zero vertical gridlines** and **zero heavy background fills**.
  - Numeric cells apply `font-variant-numeric: tabular-nums` so decimals align vertically.

---

## 3. Margin Notes (Sidenotes)

Follow every table or visual chart with a sharp interpretive **Margin Note**:

```markdown
> **Margin Note:** χ²(2, N=1450) = 38.42, p < 0.001, Cramér's V = 0.23 (moderate). Standardized residual z = +4.12 in the 18–24 segment confirms post-trial pricing is a structural defection trigger ("Too expensive after student trial ended" — P4, 22yo), warranting a student tier.
```

Rules:
- **Answer "So What?":** Explain the causal mechanism, business implication, or statistical anomaly ($|z_{ij}| \ge 1.96$) — never repeat numbers already visible in the table.
- **Length:** 1–3 dense sentences maximum.
- **HTML Rendering:** `scripts/tufte_html.py` transforms every `> **Margin Note:**` / `> **Nota de Margem:**` / `> 💡 **Insight:**` blockquote into a numbered `<aside class="margin-note">` floating in the 36% right margin column alongside the table it annotates.

---

## 4. Quantitative & Qualitative Notation Standards

| Element | Standard Format | Constitutional Rule |
| :--- | :--- | :--- |
| **Sample Proportions** | `45.2% (±3.1%, 95% CI)` | **Article 1** (1 decimal for `%` and `MoE`) |
| **Chi-Square Test** | `χ²(3, N=1450) = 24.71, p < 0.001, Cramér's V = 0.26 (moderate)` | **Article 2** (exact stat, df, N, p, effect size) |
| **Parametric Group Test** | `t(288) = 3.42, p = 0.001, Cohen's d = 0.41 (moderate)` or `F(2, 867) = 14.20, p < 0.001, η² = 0.06` | **Article 2 & 5** ($N \ge 30$/group, normal) |
| **Non-Parametric Group Test** | `Mann-Whitney U = 8420, p = 0.002, r_rb = 0.28` or `Kruskal-Wallis H(3) = 19.84, p < 0.001, ε² = 0.14` | **Article 5** ($N < 30$, skewed, or ordinal) |
| **Dual Correlation** | `Pearson r = +0.54 (p < 0.001), Spearman ρ = +0.68 (p < 0.001)` | **Article 2 & 5** (`new_methodologies.md`) |
| **Local Cell Anomaly** | `z = +3.14* (p = 0.002)` | **Article 2** ($|z_{ij}| \ge 1.96$) |
| **Qualitative Theme ($N < 30$)** | `mentioned by 8 of 12 participants` (`mencionado por 8 de 12 participantes`) | **Article 4** (zero `%` symbols when $N < 30$, $\ge 2$ literal quotes) |

---

## 5. Visualizations: Inline Tufte SVGs & Mermaid (`tufte_viz.py` & `tufte_html.py`)

1. **Markdown Deliverables (`.md`):** Include `mermaid` `xychart-beta` bar charts (max 8–10 bars) or `pie` charts (when $\le 5$ mutually exclusive categories) with sanitized labels and exact `Valid Base` percentages.
2. **HTML Deliverables (`final_report.html`):**
   - `tufte_html.py` automatically compiles Markdown `mermaid` `xychart-beta` and `pie` blocks into **native Tufte inline `<svg>` charts** (zero external JS dependencies, 100% offline and print-safe).
   - `tufte_viz.py` generates high data-ink ratio SVGs in `.dps/outputs/export/charts/`:
     - **Cleveland Dot Plots** with 95% CI error whiskers (`±MoE%`) and grand-mean reference lines.
     - **Diverging NPS / Likert Bars** (`Detractors | Passives | Promoters`).
     - **Chi-Squared Standardized Residual Heatmaps** highlighting $|z_{ij}| \ge 1.96$.
     - **Priority Matrix 4-Quadrant Scatter Plots** (`Derived Importance × Performance`).
     - **Small Multiples & Sparklines** across segments.

---

## 6. Print-to-PDF Standards: Running Header, Running Footer & Pagination (`Article 8`)

`final_report.html` is engineered as the primary publication artifact, printing directly to PDF (`Ctrl+P` / `Save as PDF`) with standards-compliant headers, footers, and pagination:

1. **Dual Print Frame Architecture (`references/styles/tufte.css` & `scripts/tufte_html.py`):**
   - **W3C CSS Paged Media (`@page`):** Sets `@page { size: A4 portrait; margin: 18mm 15mm 18mm 15mm; }` with `@top-left`, `@top-right`, `@bottom-left`, and `@bottom-right` page counter rules.
   - **Universal Browser Print Frame (`<table class="print-frame">`):** Wraps the report body inside a full-width layout table containing a repeating `<thead><tr><td><div class="print-header-space"></div></td></tr></thead>` and `<tfoot><tr><td><div class="print-footer-space"></div></td></tr></tfoot>` paired with `position: fixed` `<header class="print-running-header">` and `<footer class="print-running-footer">` elements in `@media print`. This guarantees that Chromium, Firefox, Safari, and WeasyPrint repeat the header and footer on every printed page without ever overlapping body text or tables.
2. **Running Header Content:**
   - **Left:** `{Project Name} — Data-Pro-Skill v2.1 Analytical Report`
   - **Right:** `Sample N = {N} ({global_moe_95ci}, 95% CI) · {export_date}`
3. **Running Footer Content:**
   - **Left:** `Constitution Audit: Verified (Articles 1–8) · Edward Tufte Standard`
   - **Right:** `Confidential · Print-Ready HTML Deliverable`
4. **Pagination Discipline:**
   - `break-inside: avoid; page-break-inside: avoid` on `table`, `figure`, `.chart-container`, `.margin-note`, `blockquote`, and `.kpi-grid`.
   - `break-after: avoid; page-break-after: avoid` on `h1, h2, h3, h4`.
   - `thead { display: table-header-group; }` on all data tables so multi-page tables repeat their column headers at the top of the next page.
   - Background switches from screen ivory (`#fffff8`) to pure print white (`#ffffff`) with `print-color-adjust: exact` for crisp vector chart and badge rendering.
