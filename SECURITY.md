# Security Policy

## Supported Versions

Only the latest `2.x` release line of **Data-Pro-Skill** actively receives security updates and patches.

| Version | Supported |
| :--- | :---: |
| `2.0.x` | ✅ |
| `< 2.0` | ❌ |

## Security Model & Data Privacy Principles

**Data-Pro-Skill** is designed to process potentially sensitive survey, behavioral, and market research datasets locally:

1. **100% Local & Offline Execution:** All Python analytical scripts (`scripts/*.py`), `<svg>` chart compilation (`scripts/tufte_viz.py`), and LaTeX mathematical formula rendering (`scripts/tufte_html.py`) execute locally without sending survey rows or respondent verbatims to external third-party APIs or CDNs.
2. **Zero External Runtime Scripts in Deliverables:** Compiled `final_report.html` reports embed all CSS, `<svg>` vectors, and math typography inline so reports can be opened and printed in air-gapped environments.
3. **Prompt-Injection & File-Read Guards:** When executing inside supported AI harnesses, hooks in `hooks/` guard against prompt injection in untrusted open-ended verbatim columns.

## Reporting a Vulnerability

If you discover a security vulnerability (for example: arbitrary code execution via malformed survey files, XSS injection in `tufte_html.py` verbatim rendering, or path traversal in CLI scripts), please **do not open a public GitHub issue**.

Instead, report it privately via one of the following channels:

1. **GitHub Private Vulnerability Reporting:** Open a private security advisory at [https://github.com/pablodiegoo/Data-Pro-Skill/security/advisories/new](https://github.com/pablodiegoo/Data-Pro-Skill/security/advisories/new).
2. **Direct Email:** Send a detailed report to **pablodiegoo@gmail.com** with the subject `[SECURITY] Data-Pro-Skill: <brief summary>`.

### What to Include

- Affected script or file path (e.g., `scripts/tufte_html.py`, `bin/install.js`).
- Minimal synthetic reproduction steps or sample payload.
- Potential impact (e.g., HTML/SVG injection, path traversal).

### Response Timeline

- **Acknowledgment:** Within 72 hours of submission.
- **Triage & Fix Plan:** Within 7 business days.
- **Public Disclosure:** Coordinated after a patch is released on `main`.
