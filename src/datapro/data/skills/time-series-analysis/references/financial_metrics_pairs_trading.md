# Referência: Métricas Financeiras para Estratégias de Arbitragem Estatística

> Extraído e enriquecido da skill `pairs-trading-analyst` do TCC_V2.
> Absorção recomendada: módulo de referência dentro da skill `backtesting`.

---

## 1. Métricas Fundamentais

### A. Cointegração (Engle-Granger)

**Definição:** Relação estacionária de longo prazo entre duas séries não-estacionárias.

**Teste:** Augmented Dickey-Fuller (ADF) nos resíduos da regressão OLS:
```
y = β·x + α + ε
```

**Validação:**
- `p-value < 0.05` → Rejeitamos H₀ (raiz unitária). **Par cointegrado. ✅**
- `p-value ≥ 0.05` → Falha na cointegração. **Descartar. ❌**

```python
from statsmodels.tsa.stattools import adfuller
p_value = adfuller(spread, autolag='AIC')[1]
is_cointegrated = p_value < 0.05
```

---

### B. Half-Life (Meia-Vida de Reversão)

**Definição:** Tempo esperado para o spread retornar à metade do seu desvio à média.
Baseado no processo Ornstein-Uhlenbeck:

```
dz_t = -θ(z_t - μ)dt + σ·dW_t
```

**Cálculo:**
```python
import numpy as np
from statsmodels.regression.linear_model import OLS

spread_lag  = spread.shift(1).dropna()
spread_diff = spread.diff().dropna()
theta = OLS(spread_diff, spread_lag).fit().params[0]
half_life = -np.log(2) / theta
```

**Critério de Aceitação:**
| Half-Life | Interpretação |
|-----------|---------------|
| < 1 dia | Reversão instantânea — ruído ou custo alto demais |
| 1–60 dias | ✅ Ideal para pairs trading |
| > 60 dias | Capital preso por muito tempo — risco de divergência |

---

### C. Sharpe Ratio (Anualizado)

**Fórmula:**
```
Sharpe = E[R_p - R_f] / σ_p × √252
```

**Parâmetros para o mercado brasileiro (B3):**
- `R_f` = CDI diário (taxa atual ~10.75% a.a. → ~0.0404% ao dia)
- Para Sharpe simples (Information Ratio): usar `R_f = 0`

**Interpretação:**
| Sharpe | Avaliação |
|--------|-----------|
| < 1.0 | Ruim |
| 1.0 – 1.5 | Aceitável |
| 1.5 – 2.0 | Bom |
| > 2.0 | Excelente (ou Overfitting — investigar!) |

```python
daily_pnl = trades.set_index('Entry Date')['PnL'].resample('D').sum().fillna(0)
sharpe = (daily_pnl.mean() / daily_pnl.std()) * np.sqrt(252)
```

---

### D. Maximum Drawdown (MDD)

**Fórmula:**
```
DD(t) = (equity(t) - max(equity[0:t])) / max(equity[0:t])
MDD   = min(DD)
```

**Interpretação para estratégias de pairs trading:**
| MDD | Avaliação |
|-----|-----------|
| < -10% | Excelente |
| -10% a -20% | Aceitável |
| -20% a -30% | Preocupante |
| > -30% | Inaceitável (risco de ruin) |

---

### E. Jensen's Alpha

**Definição:** Retorno da estratégia acima do esperado pelo CAPM.

**Fórmula:**
```
R_pair - R_f = α + β(R_market - R_f) + ε
```

**Parâmetros B3:**
- `R_f` = CDI
- `R_market` = IBOV (retorno diário)

```python
from statsmodels.regression.linear_model import OLS
import statsmodels.api as sm

X = sm.add_constant(ibov_excess_returns)
model = OLS(strategy_excess_returns, X).fit()
alpha = model.params['const']  # Jensen's Alpha (diário)
alpha_annual = alpha * 252
```

---

## 2. Checklist de Validação de Pares

Antes de aprovar um par para operar:

- [ ] **Liquidez:** Volume médio diário > R$ 5MM (evitar slippage excessivo)
- [ ] **Correlação:** Pearson > 0.80 (filtro de cluster)
- [ ] **Estacionariedade:** ADF p-value < 0.05 (filtro de spread)
- [ ] **Half-Life:** Entre 1 e 60 dias de trading
- [ ] **Volatilidade do Spread:** Suficiente para cobrir 2× os custos de transação
- [ ] **Justificativa Econômica:** Mesmo setor ou cadeia produtiva relacionada

---

## 3. Gestão de Risco — Stop Loss

**Regra:** Nunca usar stop loss fixo em pairs trading.
Divergências temporárias são esperadas e fazem parte da estratégia.

**Stop Loss Recomendado:**

| Tipo | Implementação | Quando Usar |
|------|---------------|-------------|
| **Z-Score Stop** | Sair se `|Z| > 4.0` | Quebra estrutural da cointegração |
| **Time Stop** | Sair após N dias | Capital preso em trade morto |
| **Percentile Stop** | Sair se spread > 99º percentil histórico | Evento extremo |

**Nunca usar:**
- Stop loss baseado em % de perda fixa (ex.: -5%)
- Stop loss baseado em preço absoluto

---

## 4. Armadilhas Comuns (Checklist Anti-Overfitting)

### Data Snooping
- [ ] **Look-ahead Bias:** μ e σ do Z-score calculados APENAS na janela de formação?
- [ ] **Survivorship Bias:** A lista de tickers inclui empresas que faliram/foram deslistadas?
- [ ] **Data Mining:** Os parâmetros foram selecionados em out-of-sample ou in-sample?

### Deficiências Metodológicas
- [ ] **Justificativa Econômica:** O par tem relação fundamental ou é coincidência numérica?
- [ ] **Custos Reais:** A estratégia é lucrativa após slippage de 0.1% por leg?
- [ ] **Selic Flutuante:** O Sharpe usa CDI diário variável ou uma média fixa?

---

## 5. Referências

- Gatev, E., Goetzmann, W. N., & Rouwenhorst, K. G. (2006). Pairs trading: Performance of a relative-value arbitrage rule. *Review of Financial Studies*, 19(3), 797-827.
- Vidyamurthy, G. (2004). *Pairs Trading: Quantitative Methods and Analysis*. Wiley.
- Engle, R. F., & Granger, C. W. J. (1987). Co-integration and error correction. *Econometrica*, 55(2), 251-276.
