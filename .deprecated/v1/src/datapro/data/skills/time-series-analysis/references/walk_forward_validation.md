# Metodologia: Walk-Forward Validation para Backtesting

## Visão Geral

Walk-forward validation é o padrão ouro para avaliar estratégias de trading.
Evita look-ahead bias ao garantir que os parâmetros do modelo são sempre
estimados **apenas com dados passados** em relação ao período de avaliação.

---

## 1. Estrutura da Janela

```
Tempo →
|←── Formation (24m) ──→|←── Trading (6m) ──→|
                         |←── Formation (24m) ──→|←── Trading (6m) ──→|
                                                  |←── Formation (24m) ──→|←── Trading (6m) ──→|
```

**Parâmetros:**
- `formation_months`: Janela de treino (estimação de parâmetros)
- `trading_months`: Janela de teste (avaliação out-of-sample)
- `step`: Quanto avançar a cada iteração (geralmente = `trading_months`)

---

## 2. O Que é Estimado na Formação vs. Trading

| Componente | Estimado em | Aplicado em |
|------------|-------------|-------------|
| PCA loadings | Formation | Formation (para clustering) |
| DBSCAN clusters | Formation | Formation (para seleção de pares) |
| Spread μ e σ | Formation | Trading (para Z-score) |
| ADF p-value | Formation | Decisão de operar ou não |
| Parâmetros de trading (Z, stop) | **Nunca** (fixos) | Trading |

---

## 3. Diferença entre In-Sample e Out-of-Sample

```
In-Sample (Formation):
  - Estima parâmetros do modelo
  - Não gera trades reais
  - Período: t-24m a t

Out-of-Sample (Trading):
  - Aplica parâmetros estimados
  - Gera trades reais (avaliados)
  - Período: t a t+6m
```

**Regra de ouro:** Nunca usar dados do período de trading para estimar
qualquer parâmetro do modelo.

---

## 4. Armadilhas Comuns (Look-Ahead Bias)

### 4.1 Normalização com dados futuros
```python
# ERRADO: StandardScaler com todos os dados
scaler.fit(all_data)  # Inclui dados futuros!

# CORRETO: StandardScaler apenas com dados de formação
scaler.fit(formation_data)
scaler.transform(trading_data)  # Aplica parâmetros passados
```

### 4.2 ADF com dados de trading
```python
# ERRADO: ADF no período completo
adfuller(full_spread)

# CORRETO: ADF apenas no período de formação
adfuller(formation_spread)
```

### 4.3 Seleção de parâmetros com dados futuros
```python
# ERRADO: Escolher entry_z=2.0 porque maximiza o Sharpe no período completo
# CORRETO: Escolher entry_z=2.0 via grid search em dados históricos anteriores
#          ao início do período de avaliação
```

---

## 5. Métricas de Avaliação Walk-Forward

### Consistência Temporal
Verificar se o Sharpe é positivo na maioria dos períodos individuais:
```python
for period in periods:
    period_sharpe = calc_sharpe(trades[trades['period'] == period])
    # Espera-se: > 60% dos períodos com Sharpe positivo
```

### Estabilidade de Parâmetros
Os pares eleitos devem ter sobreposição razoável entre períodos consecutivos:
```python
overlap = len(set(pairs_t) & set(pairs_t1)) / len(set(pairs_t) | set(pairs_t1))
# Espera-se: overlap > 0.3 (30% de pares em comum)
```

---

## 6. Implementação no TCC_V2

O TCC_V2 usou 41 períodos walk-forward:
- Início: 2005-01-01
- Fim: 2025-01-01
- Formation: 24 meses
- Trading: 6 meses
- Step: 6 meses

Isso resulta em ~20 anos de dados out-of-sample, suficiente para avaliar
a estratégia em múltiplos ciclos de mercado (2008, 2015, 2020).

---

## 7. Referências

- Prado, M. L. de (2018). *Advances in Financial Machine Learning*. Wiley.
- Bailey, D. H., & Prado, M. L. de (2014). The deflated Sharpe ratio. *Financial Analysts Journal*, 70(5), 1-10.
