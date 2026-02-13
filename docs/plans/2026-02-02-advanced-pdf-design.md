# Design: Advanced PDF Generation Engine (Super Reporter)

**Date**: 2026-02-02  
**Status**: Validated (Brainstorming)  
**Target**: `datapro.reporter` & `datapro.cli`

## 📊 Overview
Expand the current PDF generation capabilities of the DataPro package to support professional themes, flexible layouts, custom branding, and document security features.

## 🏗️ Architecture

### 1. Theme Engine (Estética Executiva & Dinâmica)
Instead of a static LaTeX header, the system will use a dynamic builder:
- **Preset Themes**: 
    - `executive`: Modern, san-serif (Inter/Roboto), deep blue accents.
    - `minimalist`: High whitespace, grayscale, clean typography.
    - `academic`: Serif fonts (Times), standard margins, no cover colors.
    - `dark`: Dark background, light text (experimental).
- **Brand Integration**: 
    - Support for `--logo <path>` to auto-position branding.
    - Automatic color matching if a logo or hex color is provided.

### 2. Layout Control (Controle de Layout)
New CLI flags to control Pandoc/LaTeX geometry:
- `--landscape`: Changes page orientation to horizontal (ideal for large tables).
- `--columns <N>`: Supports multi-column layout (N columns) using the LaTeX `multicol` package.
- `--margins <value>`: Custom margin sizes (default: 2.5cm).

### 3. Security, Navigation & Graphics (Segurança, Navegação e Gráficos)
- `--watermark <TEXT>`: Injects a LaTeX watermark (requires `draftwatermark`).
- `--no-toc`: Disables automatic Table of Contents.
- `--footer <TEXT>`: Custom footer text on every page.
- **MermaidJS Support**: Implement an automated pre-processor that converts Mermaid blocks to images (PNG/PDF) using `mermaid-cli` if available, allowing "simple charts" to be embedded directly in the PDF report instead of requiring external Python plot generation.

## 🛠️ Implementation Plan

### Component Modifications
- **[MODIFY] `src/datapro/reporter.py`**: 
    - Refactor `create_latex_header` to accept a configuration object.
    - Improve Markdown pre-processing to handle complex image scaling and table widths.
    - Add `preprocess_mermaid` function to detect and render diagrams via `mmdc` (mermaid-cli).
    - Support `\begin{multicols}{N}` injection for flexible column layouts.
    - Add new arguments to the `report` subparser.
- **[NEW] `src/datapro/styles.py`** (Expanded): 
    - Store LaTeX font/color snippets for each theme.

## 🧪 Verification Plan
- **Automated**: Test each flag combination generating PDFs and checking return codes.
- **Manual**: Visual review of generated PDFs to ensure font rendering and watermark positioning are correct.

---
> [!IMPORTANT]
> This upgrade requires `xelatex` and several TeX Live packages (`texlive-fonts-extra`, `texlive-xetex`). Fallback to standard PDF engine must be maintained for basic environments.
