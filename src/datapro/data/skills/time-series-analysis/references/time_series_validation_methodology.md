# Metodologia: Backtest de Pairs Trading (Modelo Sohail 2020)

## Visão Geral

Esta referência documenta a metodologia de backtest implementada no TCC_V2,
baseada em Sohail (2020), com extensões para stop-loss, filtros de volatilidade
e otimização de parâmetros via grid search.

---

## 1. Spread Normalizado (Sohail vs. OLS)

O modelo Sohail **não usa regressão OLS** para calcular o spread. Em vez disso,
usa preços normalizados pelo primeiro preço do período de formação:

```
spread(t) = P1(t)/P1(0) - P2(t)/P2(0)
```

**Vantagem:** Elimina o viés de estimação do hedge ratio (β) e é mais robusto
a mudanças de regime. O spread tem interpretação direta: retorno relativo acumulado.

**Comparação com OLS:**
```
OLS:    spread(t) = P1(t) - β × P2(t)    # β estimado na janela de formação
Sohail: spread(t) = P1(t)/P1(0) - P2(t)/P2(0)  # sem parâmetro estimado
```

---

## 2. Z-Score e Sinais de Trading

O Z-score padroniza o spread usando estatísticas da janela de formação:

```
Z(t) = (spread(t) - μ_form) / σ_form
```

Onde `μ_form` e `σ_form` são calculados **apenas** no período de formação
(sem look-ahead bias).

### Regras de Sinal

| Condição | Ação |
|----------|------|
| Z < -entry_z | Long Spread (compra P1, vende P2) |
| Z > +entry_z | Short Spread (vende P1, compra P2) |
| Z cruzou exit_z (convergência) | Fechar posição |
| \|Z\| > stop_z | Stop-loss por Z-score |
| Dias abertos > stop_time | Stop-loss temporal |

### Parâmetros Recomendados (TCC_V2)

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| `entry_z` | 2.0 | Threshold padrão Sohail |
| `exit_z` | 0.5 | Convergência parcial (evita reversão incompleta) |
| `stop_z` | 4.0 | Protege contra divergência extrema |
| `stop_time` | 63 dias | ~3 meses (evita capital preso) |

---

## 3. Filtro de Cointegração (ADF)

Antes de operar um par, o spread da janela de formação é testado com o
**Augmented Dickey-Fuller (ADF)**:

```python
from statsmodels.tsa.stattools import adfuller
p_value = adfuller(spread_formation, autolag='AIC')[1]
if p_value > 0.05:
    skip_pair()  # Spread não-estacionário → não operar
```

**Impacto:** Reduz o universo de pares em ~40-60%, mas melhora significativamente
a taxa de acerto (win rate) e o Sharpe ratio.

---

## 4. Filtro de Volatilidade (Extensão Sohail)

O paper original sugere que pares com **leg longa de baixa volatilidade** têm
melhor performance. Implementação:

1. Calcular volatilidade anualizada de cada ativo: `σ = std(log_returns) × √252`
2. Dividir em 4 quartis: Q1 (baixa) a Q4 (alta)
3. Só operar Long Spread quando o ativo comprado (leg longa) está em Q1

**Achado TCC:** O filtro de volatilidade **não melhorou** o Sharpe no mercado
brasileiro. A análise de sensibilidade mostrou que o critério de entrada (Z-score)
tem maior impacto que o quartil de volatilidade.

---

## 5. Grid Search de Parâmetros

O TCC_V2 implementou um grid search completo com cache de resultados:

```python
grid_entry = [2.0, 2.5, 3.0]
grid_stop_z = [3.0, 4.0, 999.0]
grid_time = [None, 21, 42, 63, 126]
# Total: 3 × 3 × 5 = 45 combinações por estratégia
```

**Otimização crítica:** Validar cointegração **uma única vez** antes do grid search,
não a cada iteração. Reduz o tempo de ~45h para ~2h.

```python
# ERRADO (lento):
for params in grid:
    run_backtest(pairs, use_coint_filter=True)  # ADF em cada iteração

# CORRETO (rápido):
valid_pairs = run_backtest(all_pairs, use_coint_filter=True)  # Uma vez
for params in grid:
    run_backtest(valid_pairs, use_coint_filter=False)  # Sem ADF
```

---

## 6. Métricas de Performance

### Sharpe Ratio (Diário)
```
Sharpe = (mean(daily_pnl) / std(daily_pnl)) × √252
```

**Nota:** `daily_pnl` é calculado agrupando trades por data de entrada,
não por data de saída. Isso subestima ligeiramente o Sharpe mas é mais
conservador e auditável.

### Win Rate
```
WinRate = n_trades_pnl_positivo / n_trades_total
```

### Maximum Drawdown
```
Drawdown(t) = (equity(t) - max(equity[0:t])) / max(equity[0:t])
MaxDD = min(Drawdown)
```

---

## 7. Referências

- Sohail, M. (2020). *Pairs Trading Using Machine Learning*. Disponível em: docs/2020-Sohail.pdf
- Sharpe, W. F. (1966). Mutual fund performance. *Journal of Business*, 39(1), 119-138.
- Engle, R. F., & Granger, C. W. J. (1987). Co-integration and error correction. *Econometrica*, 55(2), 251-276.
