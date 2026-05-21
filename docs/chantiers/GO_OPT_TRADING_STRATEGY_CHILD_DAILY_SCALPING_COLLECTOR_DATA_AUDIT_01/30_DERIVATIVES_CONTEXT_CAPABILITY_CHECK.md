---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01_DERIVATIVES_CONTEXT_CAPABILITY_CHECK
doc_type: capability_check
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01
status: closed
audited_at: 2026-05-20
---

# 30_DERIVATIVES_CONTEXT_CAPABILITY_CHECK

## Rôle confirmé : CONTEXT_ONLY

Le `derivatives_collector` n'est pas et ne doit pas être une source OHLCV. Son rôle est strictement la couche de confirmation contextuelle des setups detectors.

## Ce qu'il fournit

| Métrique | Description | Usage pour backtest |
|---|---|---|
| `open_interest` | OI total ou delta | Confirme si les positions s'ouvrent dans le sens du setup |
| `funding_rate` | Taux de financement perpetual | Indique le biais longs/shorts du marché futures |
| `liquidations_long` | Montant liquidé côté long | Cluster de liq longs = potentiel sweep low sain |
| `liquidations_short` | Montant liquidé côté short | Cluster de liq shorts = potentiel sweep high sain |
| `long_short_ratio` | Ratio positions L vs S | > 1.5 = crowded longs (risque fade) |
| `volume_futures` | Volume futures | Confirmation d'engagement |

## Gap vs usage pour XAUUSD

Le `derivatives_collector` est actuellement configuré pour BTCUSDT/ETHUSDT. Pour XAUUSD scalping :

| Question | Statut |
|---|---|
| XAUUSDT derivatives disponible via Bitget ? | À vérifier — XAUUSDT a funding/OI sur Bitget |
| Timestamps UTC alignables sur M5 ? | Snapshot par run → nécessite granularité configurable |
| Profondeur historique derivatives XAUUSDT ? | Non documentée |
| merge_asof compatible ? | Oui si timestamps UTC disponibles |

## Ce qui est accepté sans modification

Pour la couche contextuelle, l'absence de données derivatives pour une période donnée est acceptable. Le runner ne doit pas crasher si les colonnes derivatives sont absentes :

```python
# Dans load_data.py — pattern correct
if deriv_path and deriv_path.exists():
    df_deriv = load_derivatives(deriv_path)
    df = merge_asof(df, df_deriv, direction="backward")
# Sinon : df n'a pas les colonnes derivatives → scorer utilise base score seulement
```

## Décision pour ce GO

`derivatives_collector` = `CONTEXT_ONLY`. Aucune adaptation requise pour débloquer le backtest. Son intégration XAUUSDT est un enrichissement optionnel, documenté dans `40_COLLECTOR_INTEGRATION_PLAN.md` du chantier REWORK.

**Prérequis avant intégration derivatives XAUUSDT :**
1. Confirmer que XAUUSDT perpetual futures est disponible sur Bitget avec OI/funding/liq
2. Ajouter XAUUSDT à la config derivatives_collector
3. Vérifier la granularité temporelle des exports
