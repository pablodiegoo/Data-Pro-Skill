# Political Science Metrics Reference

## Inverse Regression for Rejection
While traditional models predict "Success" or "Approval", political science often needs to understand "Rejection" or "Disapproval".

### Logic
1.  **Inverse Target**: Create a binary target where 1 = Disapproval/Rejection.
2.  **Logistic Regression**: Regress this target against image attributes.
3.  **Shield Identification**: Attributes with the strongest *negative* coefficients are "shields"—their higher performance significantly reduces the probability of rejection.

## Pain Curves
A Pain Curve visualizes the "Deal Breaker" relationship.

### Interpretation
- **X-Axis**: Performance score in a specific attribute (e.g., 0-10).
- **Y-Axis**: Probability of Rejection (0-1.0).
- **Curve Shape**: A steep increase at the lower end of the X-axis indicates a "Basic Requirement" (Must-Have). If the curve is relatively flat, the attribute has less impact on rejection.

## Example: Campaign Labels
Use these labels to map database columns for readable reports:

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
