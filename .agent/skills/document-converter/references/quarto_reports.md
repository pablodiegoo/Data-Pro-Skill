# Premium Reports with Quarto

For high-quality, professional analytical reports, use **Quarto** instead of the standard Markdown-to-PDF compiler. Quarto allows for sophisticated layouts, mathematical typesetting, and premium title pages.

## Why Quarto?
- **Premium Aesthetics**: Better default typography and layouts.
- **Title Pages**: Full support for `quarto-titlepages` extension.
- **Dynamic Content**: Direct execution of Python code chunks (not recommended for final exports, which should be done via separate analysis scripts).

## Workflow

### 1. Initialize Quarto Project
```bash
quarto create-project --type book # Or manually create _quarto.yml
```

### 2. Premium Title Pages
Install the extension (requires internet):
```bash
quarto add nmfs-opensci/quarto_titlepages
```

### 3. Rendering
```bash
quarto render report.qmd --to pdf
```

## Template Example (`report.qmd`)
See `assets/quarto-templates/quarto_report_template.qmd` for a base structure using the `bg-image` style.
