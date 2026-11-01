# Contributing to Data-Pro-Skill

Thank you for your interest in contributing to **Data-Pro-Skill v2.0** — an autonomous Survey Science, Data Grilling, and Multi-School Print-Ready HTML Reporting skill for AI coding agents.

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Core Architectural Principles

Before submitting a Pull Request, please read these three foundational documents:

1. **[`GLOSSARY.md`](GLOSSARY.md):** Our canonical domain vocabulary (*Leading Words / Leitworte*). Code, prompts, and documentation must use these exact terms without drifting to synonyms.
2. **[`constitution.md`](constitution.md):** The 8-Article Data Constitution governing statistical precision (`±MoE%`), mandatory effect sizes, parametric/non-parametric pairing, small-sample discipline ($N < 30$ raw counts only), quality gates, survey governance, and print-ready HTML output.
3. **[`references/design-schools.md`](references/design-schools.md):** Specification for the 5 **Data Design Schools** (`tufte`, `few`, `knaflic`, `swiss`, `editorial`).

---

## How to Contribute

1. **Fork** the repository on GitHub.
2. **Create a feature or fix branch** from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```
3. **Make your changes** following the coding and documentation standards below.
4. **Verify your changes** by running the full pipeline and verifying the generated HTML/SVG output.
5. **Commit** using [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`):
   ```bash
   git commit -m "feat: add new non-parametric post-hoc test to crosstabs.py"
   ```
6. **Open a Pull Request** filling out the [PR template](.github/pull_request_template.md).

---

## Areas Open for Contribution

| Area | Files / Directory | Guidelines |
| :--- | :--- | :--- |
| **Deep Survey Science Modules** | `scripts/*.py`, `references/analysis/*.md` | Must be self-contained **Deep Modules** that compute both parametric and non-parametric estimators, 95% CI `±MoE%`, $p$-values, and effect sizes automatically. |
| **Data Design Schools & SVG Grammars** | `scripts/design_schools.py`, `scripts/tufte_viz.py`, `references/styles/*.css` | New visual adjustments must preserve high **Data-Ink Ratio**, respect the school's chart grammar, and pass `@media print` pagination (`break-inside: avoid` + `<table class="print-frame">`). |
| **Native LaTeX Math Typography** | `scripts/tufte_html.py`, `references/styles/*.css` | Must remain 100% offline/zero-CDN, handle nested LaTeX constructs cleanly, and never misparse currency strings (`$50–$100`). |
| **Agent Definitions & Workflows** | `SKILL.md`, `agents/*.md`, `references/dps-*.md` | Follow **Progressive Disclosure**: keep `SKILL.md` compact and put detailed methodology rules in `references/`. |
| **Multi-Harness Compatibility** | `bin/install.js` | Test installation across OpenCode, Gemini CLI, Antigravity CLI, Claude Code, Codex CLI, and GitHub Copilot. |

---

## Verification & Local Testing Checklist

Before opening a Pull Request that touches `scripts/` or `references/styles/`, run the end-to-end verification pipeline:

```bash
# 1. Verify Python syntax across all scripts:
python3 -m py_compile scripts/*.py

# 2. Test HTML + native LaTeX math + multi-school compilation against reference outputs:
python3 scripts/final_report_generator.py --input references/outputs/ -o /tmp/dps-test-export/ --school tufte
python3 scripts/final_report_generator.py --input references/outputs/ -o /tmp/dps-test-export/ --school few
python3 scripts/final_report_generator.py --input references/outputs/ -o /tmp/dps-test-export/ --school knaflic
python3 scripts/final_report_generator.py --input references/outputs/ -o /tmp/dps-test-export/ --school swiss
python3 scripts/final_report_generator.py --input references/outputs/ -o /tmp/dps-test-export/ --school editorial

# 3. Verify that constitutional audit passes with 0 critical violations:
cat /tmp/dps-test-export/verification_report.json
```

---

## License

By contributing to **Data-Pro-Skill**, you agree that your contributions will be licensed under its [MIT License](LICENSE).
