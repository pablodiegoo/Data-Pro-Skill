# Ipsative and Residual Analysis Reference

## Example: Political Image Labels
When analyzing a candidate's image, use a `label_map` like this to translate technical column names to reader-friendly labels:

```python
label_map = {
    'humilde_respeitosa': 'Humilde e Respeitosa',
    'honesta_correta': 'Honesta e Correta',
    'carismatica': 'Carismática',
    'competente': 'Competente',
    'confianca': 'Inspira Confiança',
    'proxima_pessoas': 'Próxima das Pessoas',
    'preparada_tecnicamente': 'Preparada Tecnicamente',
    'inteligente_resolve': 'Inteligente e Resolve',
    'propostas': 'Boas Propostas',
    'autonomia': 'Tem Autonomia',
    'foco_cidade': 'Foco na Cidade',
    'realidade_populacao': 'Conhece a Realidade'
}
```

## Technical Details

### Ipsative Analysis
- **Problem**: Response style bias (some respondents are structurally more generous or stricter).
- **Transformation**: `Score_centered = Score - Personal_Mean`.
- **Insight**: High values in the centered score indicate an attribute that stands out *relative to the respondent's other ratings*, regardless of their absolute scale.

### Halo Removal (Residuals)
- **Problem**: A strong overall brand image (Halo Effect) inflates all attribute ratings.
- **Transformation**: `Attribute_residual = Attribute - Predicted_by_Overall_Image`.
- **Insight**: Correlations between residuals reveal "pure" connections between attributes that are not driven by the respondent's general sentiment toward the entity.
