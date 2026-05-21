---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01_COLLECTOR_INTEGRATION_PLAN
doc_type: integration_plan
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01
status: open
updated_at: 2026-05-20
---

# 40_COLLECTOR_INTEGRATION_PLAN

## Rôle des collectors dans le backtest

Les derivatives collectors ne sont pas une source OHLCV. Ils fournissent une **couche de confirmation contextuelle** : est-ce que le marché micro-structure supporte le setup detecté par les règles chandelles ?

```
OHLCV canonique (Niveau 1)     → détection setups (ORB/VWAP/SMC/COMBINED)
Derivatives collector (Niveau 2) → filtre contextuel optionnel par setup
Bot vision (Niveau 3)           → validation visuelle structurelle
```

## Données disponibles — derivatives_collector

Selon la documentation du repo, `derivatives_collector` collecte :

| Métrique | Description |
|---|---|
| `open_interest` | OI total ou delta OI |
| `funding_rate` | taux de financement perpetual futures |
| `liquidations` | montant liquidé (longs / shorts) par intervalle |
| `long_short_ratio` | ratio positions longs vs shorts (comptes top traders ou global) |
| `volume_delta` | si disponible — acheteurs agressifs vs vendeurs |

## Plan de branchement

### Étape 1 — Export derivatives en CSV aligné M5

Le derivatives_collector doit pouvoir exporter ses données avec :
- Timestamp UTC alignable sur M5
- Granularité minimum 5 minutes (ou resampleable en 5 min)

Format cible :

```text
timestamp,oi,oi_delta,funding,liq_longs,liq_shorts,ls_ratio,source
2024-01-02 08:00:00+00:00,42500000000,+120000000,0.0001,850000,120000,1.42,derivatives_collector
```

### Étape 2 — Merge dans le pipeline backtest

Dans `load_data.py`, après `merge_timeframes(df_exec, df_ctx)` :

```python
# À implémenter dans le rework
if deriv_path.exists():
    df_deriv = load_derivatives(deriv_path)
    df = merge_asof(df, df_deriv, direction="backward")
```

Les colonnes dérivatives sont `NaN` quand non disponibles — le runner ne doit pas crasher en leur absence.

### Étape 3 — Filtres contextuels dans le scorer

Le scorer peut utiliser les données dérivatives comme critères supplémentaires :

```python
# Exemples de filtres contextuels — à calibrer
def score_setup_with_context(setup, row):
    score = score_setup(setup)  # score base chandelles

    # Confirmation long via dérivatives
    if setup.direction == "long":
        if row.get("ls_ratio", 1.0) > 1.3:  # majorité long — crowded
            score -= 1  # signal moins fiable si crowd long
        if row.get("liq_longs", 0) > row.get("liq_longs_threshold", 1e9):
            score += 1  # liquidation longs récente = reset sain
        if row.get("oi_delta", 0) > 0 and row.get("funding", 0) < 0:
            score += 1  # OI monte + funding négatif = long favorisé

    # Confirmation short via dérivatives
    if setup.direction == "short":
        if row.get("ls_ratio", 1.0) < 0.7:  # majorité short — crowded
            score -= 1
        if row.get("liq_shorts", 0) > row.get("liq_shorts_threshold", 1e9):
            score += 1
        if row.get("oi_delta", 0) < 0 and row.get("funding", 0) > 0:
            score += 1

    return min(score, 10)
```

### Étape 4 — Logique métier derivatives pour COMBINED

Exemple concret illustrant l'intent :

```
Setup COMBINED LONG détecté :
  → Sweep low + CHOCH (3 bougies confirmé)
  → Close > VWAP
  → Close > ORB low

Contexte derivatives :
  → OI rising (acheteurs s'engagent)
  → Funding négatif (shorts payent longs)
  → Liquidations longs récentes élevées (cluster nettoyé)
  → L/S ratio < 1.0 (pas crowded longs)

Résultat : setup plus crédible → score += 2-3 points
```

```
Setup COMBINED SHORT détecté :
  → Sweep high + CHOCH
  → Close < VWAP
  → Close < ORB high

Contexte derivatives :
  → OI rising
  → Funding positif (longs payent shorts)
  → Liq shorts récentes élevées
  → L/S ratio > 1.5 (très crowded longs = fuel for shorts)

Résultat : setup très crédible → score += 2-3 points
```

## Ce que ce plan ne fait PAS

- Ne définit pas le derivatives_collector comme source OHLCV
- Ne remplace pas le spread réel
- Ne rend pas les données dérivatives obligatoires pour le runner (optionnelles, enrichissement)
- Ne décide pas de la structure interne du derivatives_collector (celui-ci est documenté séparément)

## Prérequis avant implémentation

1. Définir la granularité temporelle des exports derivatives_collector
2. Confirmer que les timestamps sont UTC-normalisés
3. Tester merge_asof avec des données dérivatives réelles sur une fenêtre de test
4. Calibrer les seuils (ls_ratio, oi_delta, etc.) sur données historiques
