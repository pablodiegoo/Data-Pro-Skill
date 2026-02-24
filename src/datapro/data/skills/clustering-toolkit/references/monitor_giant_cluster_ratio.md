# Regra: Monitorar Giant Cluster Ratio em Clustering DBSCAN

## Problema

O DBSCAN com `eps` muito alto pode criar um único cluster dominante que absorve
a maioria dos ativos do universo. Isso resulta em pares espúrios (ativos de
setores completamente diferentes agrupados juntos) e degrada a performance.

## Regra

> **Sempre calcular e monitorar o Giant Cluster Ratio após cada configuração de DBSCAN.**
> Rejeitar configurações onde `giant_ratio > 0.50` em mais de 20% dos períodos.

## Definição

```
giant_ratio(período) = max(tamanho_cluster) / n_ativos_universo
```

- `giant_ratio < 0.30`: Excelente — clusters bem separados
- `0.30 ≤ giant_ratio < 0.50`: Aceitável
- `giant_ratio ≥ 0.50`: Patológico — reduzir `eps`

## Implementação

```python
from dbscan_cluster_quality import calculate_cluster_metrics, score_configuration

metrics = calculate_cluster_metrics(pairs_df, total_periods=41)
print(f"Giant Ratio Médio: {metrics['Avg_Giant_Ratio']:.2%}")
print(f"Períodos Patológicos: {metrics['Periods_Giant']}/{metrics['Total_Periods']}")

if metrics['Periods_Giant'] > 0.2 * metrics['Total_Periods']:
    print("⚠️ Configuração rejeitada: Giant Cluster Pathology")
```

## Contexto de Mercado

O Giant Cluster Ratio tende a aumentar durante crises (correlações sobem).
É normal ver picos em 2008, 2020. O que não é normal é um ratio alto
**em períodos de mercado normal**.

## Tags

`DBSCAN`, `clustering`, `quality`, `pairs-trading`, `hyperparameter`
