# Metodologia: PCA + DBSCAN para Seleção de Pares em Pairs Trading

## Visão Geral

Esta referência documenta a metodologia de seleção de pares implementada no TCC_V2,
baseada em Sohail (2020), com extensões próprias para o mercado brasileiro.

A abordagem combina **redução dimensional via PCA** com **clusterização via DBSCAN**
para identificar ativos com comportamento de preço estatisticamente similar,
formando pares candidatos para estratégias de arbitragem estatística.

---

## 1. Motivação

O método clássico de pairs trading (Gatev et al., 2006) seleciona pares por
distância mínima de preço normalizado. Isso ignora a estrutura de covariância
do mercado e produz pares espúrios.

A abordagem PCA+DBSCAN:
- Captura a **estrutura fatorial latente** do mercado (fatores de risco comuns)
- Agrupa ativos por **similaridade de exposição** a esses fatores
- Permite incorporar **restrições de domínio** (setor) como features adicionais

---

## 2. Pipeline Completo

```
Preços Brutos
    ↓
Log Returns (diários)
    ↓
StandardScaler (z-score por ativo)
    ↓
PCA (n_components = min(2, n_assets/3))
    ↓  Loadings: shape (n_assets, n_components)
Sector One-Hot Dummies × sector_weight
    ↓  Dummies: shape (n_assets, n_sectors)
Concatenação → Feature Matrix (n_assets, n_components + n_sectors)
    ↓
DBSCAN (eps, min_samples, metric='euclidean')
    ↓
Pares Intra-Cluster (distância euclidiana no espaço híbrido)
    ↓
Walk-Forward Output: pairs_history.csv
```

---

## 3. Parâmetros Críticos

### 3.1 PCA Components (`n_components`)
- **Recomendado:** 2 (captura ~60-70% da variância em mercados emergentes)
- **Regra:** `n_components = min(2, n_assets // 3)` para evitar overfitting
- **Intuição:** PC1 ≈ fator de mercado (beta), PC2 ≈ fator setorial

### 3.2 DBSCAN Epsilon (`eps`)
- **Recomendado:** 0.015 (mercado brasileiro, janela 24 meses)
- **Sensibilidade:** Valores maiores → clusters maiores → mais pares, menos qualidade
- **Patologia:** `eps` muito alto → "giant cluster" (>50% do universo em 1 cluster)
- **Diagnóstico:** Monitorar `Giant Cluster Ratio` ao longo do tempo

### 3.3 DBSCAN Min Samples (`min_samples`)
- **Recomendado:** 3 (mínimo para formar um cluster)
- **Trade-off:** Valores maiores → clusters mais densos, menos pares

### 3.4 Sector Weight (`sector_weight`)
- **Recomendado:** 1.0 (peso igual entre PCA e setor)
- **Efeito:** `sector_weight=0` → clustering puramente estatístico
- **Efeito:** `sector_weight=2.0` → clustering dominado por setor (similar ao clássico)
- **Achado TCC:** `sector_weight=1.0` maximizou Sharpe no mercado brasileiro

---

## 4. Walk-Forward Validation

A metodologia usa janelas deslizantes para evitar look-ahead bias:

```
Formation Window: 24 meses (treino do PCA+DBSCAN)
Trading Window:    6 meses (aplicação dos pares eleitos)
Step:              6 meses (avança a janela)
```

**Importante:** Os pares são re-eleitos a cada período. Um par pode entrar e
sair do portfólio ao longo do tempo, refletindo mudanças na estrutura de mercado.

---

## 5. Diagnóstico de Qualidade dos Clusters

### Giant Cluster Pathology
Ocorre quando um cluster absorbe >50% do universo. Indica que `eps` está
muito alto ou que o mercado está em regime de alta correlação (crises).

**Métricas de diagnóstico:**
```python
giant_ratio = max_cluster_size / n_universe
```
- `giant_ratio < 0.3`: Excelente
- `0.3 ≤ giant_ratio < 0.5`: Aceitável
- `giant_ratio ≥ 0.5`: Patológico → reduzir `eps`

### Número de Clusters ao Longo do Tempo
- Espera-se variação sazonal (crises → menos clusters, maior correlação)
- Queda abrupta para 1-2 clusters = sinal de regime de crise

---

## 6. Extensão: Feature Híbrida

A inovação central do TCC_V2 é a **feature híbrida**:

```python
features = concat([pca_loadings, sector_dummies × sector_weight])
```

Isso permite que o DBSCAN agrupe ativos que são:
1. **Estatisticamente similares** (próximos no espaço PCA)
2. **Economicamente relacionados** (mesmo setor)

Pares que satisfazem ambos os critérios têm maior probabilidade de cointegração
e reversão à média.

---

## 7. Referências

- Sohail, M. (2020). *Pairs Trading Using Machine Learning*. Disponível em: docs/2020-Sohail.pdf
- Gatev, E., Goetzmann, W. N., & Rouwenhorst, K. G. (2006). Pairs trading: Performance of a relative-value arbitrage rule. *Review of Financial Studies*, 19(3), 797-827.
- Ester, M., Kriegel, H. P., Sander, J., & Xu, X. (1996). A density-based algorithm for discovering clusters in large spatial databases with noise. *KDD*, 96(34), 226-231.
