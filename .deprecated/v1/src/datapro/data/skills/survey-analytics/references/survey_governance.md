# Proposed Rule: Survey Data Ingestion & Governance

**Description:** Standardize how raw survey data is ingested to prevent downstream errors in visualization and ML modeling.

**The Rule:**
1. **Never use raw question text as column names in analytical datasets.** Raw CSVs from survey platforms (like Qualtrics/Google Forms) use the entire question (e.g., `"1. How satisfied are you with X?"`) as the header.
2. **Mandatory Step 1:** The very first step in `01_data_cleaning.py` must be mapping these long strings to standard `snake_case` semantic identifiers (e.g., `satisfaction_x_rating`).
3. **Preserve the Schema:** You MUST save this mapping to `.agent/references/column_mapping.json` (format: `{"snake_case_name": "Original Question Text"}`).
4. **Automated Documentation:** All downstream generated notebooks (EDA, Advanced Analytics) MUST load this `column_mapping.json` and generate an automated "Glossary & Data Schema" Markdown table as the first cell. This ensures the client always knows what `satisfaction_x_rating` actually asked.

**Why:** In the Festival Verão project, preserving the original question text while operating on clean Pythonic variables allowed us to build highly complex ML pipelines without breaking, while still generating human-readable reports that the client could interpret perfectly.
