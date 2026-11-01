# Support & Getting Help

Need help installing, running, or customizing **Data-Pro-Skill v2.0**? Here is where to look first.

## 1. Documentation & Reference Guides

Before opening an issue, check the built-in documentation:

- **[README.md](README.md):** Quick start, CLI commands, and overview of the 5 Data Design Schools.
- **[GLOSSARY.md](GLOSSARY.md):** Definitions of all canonical domain terms (*Leading Words*), statistical methods, and visual components.
- **[constitution.md](constitution.md):** The 8 non-negotiable articles governing statistical rigor, small-sample rules ($N < 30$), and print-ready HTML exports.
- **[references/design-schools.md](references/design-schools.md):** Complete guide to the 5 selectable **Data Design Schools** (`tufte`, `few`, `knaflic`, `swiss`, `editorial`).
- **[docs/USER-GUIDE.md](docs/USER-GUIDE.md) & [docs/COMMANDS.md](docs/COMMANDS.md):** Step-by-step usage guide and CLI reference (in PT-BR).

## 2. Common Troubleshooting

### Python Dependencies
Ensure you are running **Python 3.8+** with standard scientific packages installed:
```bash
pip install pandas numpy scipy scikit-learn openpyxl
```

### Selecting or Switching a Data Design School
- **At Setup:** `python3 scripts/quant_analyzer.py your_data.csv --profile --school knaflic -o .dps/outputs/setup/`
- **At Export:** `python3 scripts/final_report_generator.py --data your_data.csv -o .dps/outputs/export/ --school editorial`
- **Live in Browser:** Open `final_report.html` and use the top-bar **`🎨 Design School`** selector before clicking **`🖨️ Print / Save as PDF`**.

## 3. Opening an Issue

- **Bug Reports:** Use the [Bug Report template](https://github.com/pablodiegoo/Data-Pro-Skill/issues/new?template=bug_report.yml) and include the command run, Python/Node versions, and a synthetic reproduction snippet (never upload confidential respondent PII).
- **Feature / Methodology Requests:** Use the [Feature Request template](https://github.com/pablodiegoo/Data-Pro-Skill/issues/new?template=feature_request.yml).
- **Security Vulnerabilities:** Please follow [SECURITY.md](SECURITY.md) instead of opening a public issue.
