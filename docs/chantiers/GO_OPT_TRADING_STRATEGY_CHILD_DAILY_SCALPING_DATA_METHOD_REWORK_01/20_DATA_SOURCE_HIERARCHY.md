---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01_DATA_SOURCE_HIERARCHY
doc_type: data_source_hierarchy
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01
status: open
updated_at: 2026-05-20
---

# 20_DATA_SOURCE_HIERARCHY

## Principe

La source de données détermine la validité du verdict. Une hiérarchie claire évite toute confusion entre smoke technique et verdict stratégique.

## Hiérarchie des sources

### Niveau 1 — Source primaire (verdict valide)

```
broker export / prod api collector
```

| Propriété | Exigence |
|---|---|
| Instrument | XAUUSD spot (pas GC=F) |
| Granularité | M5 + M15 minimum |
| Champs | timestamp, open, high, low, close, volume, bid, ask, spread |
| Timezone | UTC normalisé |
| Sessions | définies par le broker (London/NY/Asia/Overlap) |
| Fenêtre | minimum 6 mois, idéal 12-24 mois |
| Régimes | doit couvrir trend, range, news, high-vol |

**Sources acceptées :**
- Export CSV MetaTrader 4/5 (History Center → XAUUSD M5)
- Export TradingView Premium (données broker, pas Yahoo)
- Prod api collector du repo (quand disponible pour XAUUSD)
- Dukascopy tick data → resampleé en M5

### Niveau 2 — Source secondaire (backtest contextuel)

```
prod derivatives_collector output
```

| Propriété | Exigence |
|---|---|
| Données | OI, funding, liquidations, L/S ratio |
| Granularité | alignée sur M5/M15 via merge_asof |
| Usage | filtre contextuel, pas source OHLCV |
| Contrainte | ne remplace pas bid/ask/spread |

### Niveau 3 — Source fallback (smoke uniquement)

```
Yahoo Finance / GC=F
```

| Propriété | Valeur |
|---|---|
| Usage autorisé | smoke technique, test du runner, CI |
| Usage interdit | verdict stratégique, promotion paper forward |
| Raison | proxy futures, pas bid/ask, fenêtre 60j max, timezone inconsistante |
| Marquage obligatoire | `DATA_SOURCE=SMOKE_ONLY` dans les outputs |

### Niveau 4 — Source interdite comme OHLCV

```
TradingView alertes / webhooks
bot vision / visual_context screenshots
```

Ces sources produisent des signaux ou de l'évidence visuelle. Elles ne sont jamais une source OHLCV canonique.

## Règle de promotion

```
Un verdict PROMOTE_TO_PAPER_FORWARD ne peut être émis que si :
  DATA_SOURCE in [broker_export, prod_api_collector]
  ET fenêtre >= 180 jours
  ET nb_regimes >= 3 (trend, range, high-vol)
  ET SMC_SWEEP_ONLY et COMBINED ont chacun >= 100 trades
```

Si l'une de ces conditions est manquante → verdict = `NEED_DATA_UPGRADE`, pas PROMOTE.

## Flow de validation source

```
Source définie
  → Level 1? → verdict autorisé
  → Level 2? → contexte seulement, combine avec Level 1
  → Level 3? → output marqué SMOKE_ONLY, pas de verdict
  → Level 4? → refus, error dans runner
```
