## Summary

<!-- Briefly describe what this Pull Request changes and why. -->

### Related Issue

<!-- Link the issue this PR resolves, e.g., Closes #12 -->

---

## Type of Change

- [ ] **Bug Fix** (`fix:`) — Corrects statistical calculation, HTML/SVG rendering, LaTeX math parsing, or CLI behavior
- [ ] **New Feature / Methodology** (`feat:`) — Adds a survey science capability, Data Design School enhancement, or command workflow
- [ ] **Documentation & Domain Model** (`docs:`) — Updates `README.md`, `GLOSSARY.md`, `constitution.md`, or `references/`
- [ ] **Refactoring / Performance** (`refactor:`) — Improves code structure without altering statistical or visual contracts

---

## 8-Article Data Constitution & Design School Checklist

- [ ] Follows canonical domain vocabulary from [`GLOSSARY.md`](../GLOSSARY.md)
- [ ] Complies with [`constitution.md`](../constitution.md) (95% CI `±MoE%`, paired effect sizes, $N < 30$ raw count discipline, Answer-First prose)
- [ ] Preserves rendering across all 5 **Data Design Schools** (`tufte`, `few`, `knaflic`, `swiss`, `editorial`) and `@media print` PDF pagination
- [ ] `python3 -m py_compile scripts/*.py` passes with zero errors
