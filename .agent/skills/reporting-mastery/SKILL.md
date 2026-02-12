---
name: reporting-mastery
description: "Patterns, templates, and Mermaid diagrams for creating world-class technical documentation and reports. Use for: (1) Creating new .md files, (2) Adding Mermaid diagrams, (3) Structuring reports and READMEs, (4) Applying GitHub-style alerts and premium visual standards."
---

# Reporting Mastery

This skill consolidates technical documentation standards and Mermaid diagram visualization to ensure high-impact delivery and technical consistency.

## 1. Markdown Patterns (Premium Visuals)

### Alerts (GitHub Style)
Use for highlighting critical information visually.
```markdown
> [!NOTE]
> Additional context or neutral observations.

> [!TIP]
> Best practices and efficiency suggestions.

> [!IMPORTANT]
> Mandatory requirements or crucial steps.

> [!WARNING]
> Breaking changes or security warnings.

> [!CAUTION]
> Risks of data loss or critical failures.
```

### Code Blocks and Links
- **Code Blocks**: Always specify the language and use the `language:path/to/file` format if applicable.
- **Relative Links**: Always use relative links `./file.md` for internal movement between documents.

## 2. Visualization with Mermaid

Use Mermaid diagrams to explain complex flows and architectures.

### Common Patterns:
- **Sequence Diagram**: For interaction flows between systems/actors.
- **Graph (Flowchart)**: For architectures and logical processes.
- **ER Diagram**: For data modeling and database schemas.

### Diagramming References:
For technical syntax details and complex examples, consult the reference documents:
- [Selection Guide](./references/selection-guide.md): Which diagram to choose for each situation.
- [Mermaid Syntax](./references/syntax.md): Quick guide to commands and shapes.
- [Practical Examples](./references/examples.md): Library of ready-to-use templates.
- [Troubleshooting](./references/troubleshooting.md): How to fix rendering errors.

## 3. Standard Document Structure

Every reference document or report must follow this hierarchy:

1. **Title (H1)**: Clear objective.
2. **Overview**: Executive summary of content.
3. **Mermaid Diagram**: Visual representation of the concept.
4. **Technical Detail**: Tables, code, or specifications.
5. **Workflow**: Step-by-step guide or user manual.
6. **Maintenance Note**: `> [!NOTE] Last updated: YYYY-MM-DD`.

---
> [!TIP]
> When creating Mermaid diagrams, avoid node overload. If the diagram gets too large, break it into subgraphs or multiple files.
