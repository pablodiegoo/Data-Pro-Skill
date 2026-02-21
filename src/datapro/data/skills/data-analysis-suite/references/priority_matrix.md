# Methodology: Priority Matrix (Pain Curves)

The Priority Matrix is a strategic tool used to identify which attributes or services require immediate investment versus those that only need maintenance.

## Matrix Quadrants
The matrix crosses **Importance** (correlation with Overall Satisfaction) against **Performance** (mean score).

1.  **Prioridade Máxima (Oportunidade)**: High Importance / Low Performance.
2.  **Manutenção**: High Importance / High Performance.
3.  **Indiferença (Baixo Valor)**: Low Importance / Low Performance.
4.  **Excesso (Desperdício)**: Low Importance / High Performance.

## Priority Score Formula
$$PriorityScore = Importance \times (Scale_{max} - Performance)$$

This formula mathematically weighs the potential impact (Importance) by the available room for improvement (Performance Gap).

## Implementation
See `scripts/priority_matrix.py` for automated calculation.
