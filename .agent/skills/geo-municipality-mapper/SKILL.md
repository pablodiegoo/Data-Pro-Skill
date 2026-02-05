---
name: geo-municipality-mapper
description: "Normalization and state-mapping of municipal data. Detects city/state strings, normalizes names, and attaches regional metadata. Robust regex handles variations like 'Cidade - UF' or 'Cidade/UF'."
---

# Geo Municipality Mapper

This skill simplifies the geographic alignment of Brazilian municipal data by normalizing heterogeneous inputs into standard keys.

## Capabilities

- **Name Normalization**: Sanitizes input strings (removes accents, handles casing) to match official IBGE naming conventions.
- **State Detection**: Extracts state codes (UF) from strings like "São Paulo - SP" or "Recife/PE".
- **Regional Metadata**: Enrich datasets with region (Norte, Nordeste, etc.) based on the detected state.

## Usage

```bash
python3 .agent/skills/geo-municipality-mapper/scripts/mapper.py input.csv "City Column" -o normalized_output.csv
```

## Example Transformation
- Input: `Duartina - SP`
- Output: `duartina`, `SP`, `Sudeste`

## Related Skills
- **survey-data-viz**: Use normalized geographic data to feed states/regions into filters and charts.
