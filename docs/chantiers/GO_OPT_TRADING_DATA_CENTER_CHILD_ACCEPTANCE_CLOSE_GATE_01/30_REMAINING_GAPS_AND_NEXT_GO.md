---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_ACCEPTANCE_CLOSE_GATE_01_REMAINING_GAPS
doc_type: gaps_and_next_go
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_ACCEPTANCE_CLOSE_GATE_01
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 30_REMAINING_GAPS_AND_NEXT_GO

Ces gaps sont hors périmètre du close gate `MARKET_METRICS_CONSUMER_DECOUPLING_BLOCK_01`.
Ils ne bloquent pas l'acceptance. Chacun requiert un GO dédié.

---

## Gaps consumer — readers non implémentés

| Gap | Consumer | access_pattern | Priorité estimée |
|---|---|---|---|
| GAP-C01 | `telegram_screener__signal_context` | `latest_only` | Opérationnel — dès que Telegram screener est activé |
| GAP-C02 | `google_sheets__market_reporting` | `latest_only` | Reporting — dès que Google Sheets consumer existe |
| GAP-C03 | `strategy_framework__market_context` | `by_symbol` | Stratégie — dès que `PF_STRATEGY_FRAMEWORK_REGISTRY` implémenté |
| GAP-C04 | `perf_engine__replay_context` | `full_history` | Lab — dès que replay historique requis |
| GAP-C05 | `localcms__data_center_health` | `status_only` | Ops — lit `_registry/producers.json`, hors `market_metrics.v1` |

---

## Gaps producer — contracts non finalisés

| Gap | Producer | Contrat | Note |
|---|---|---|---|
| GAP-P01 | `collector_binance_spot` | `pair_market_snapshot.v1` | Views non créées — `desk_pro__spot_snapshot` est `not_started` |
| GAP-P02 | `coinglass` | `market_metrics.v1` | `NOT_PROVEN_RUNTIME_ADAPTER` permanent — headless seulement |
| GAP-P03 | `derivatives_collector__bitget` | `market_metrics.v1` | `last_write: null` — pas de write confirmé en prod |
| GAP-P04 | `derivatives_collector__binance` | `market_metrics.v1` | `last_write: null` — pas de write confirmé en prod |

---

## Gaps infrastructure

| Gap | Objet | Note |
|---|---|---|
| GAP-I01 | `manifest.json` par producer | Déclaré dans `10_SELECTED_SETUP` du parent, pas encore créé |
| GAP-I02 | `status.json` par producer | Idem — layout partiel |
| GAP-I03 | Schema versioning `v2+` | `schema_version: v1` fixé, pas de migration path déclaré |
| GAP-I04 | `pair_market_snapshot.v1` views | `data/data_center/views/pair_market_snapshot/` non créé |
| GAP-I05 | Contract class `null` pour `localcms` | Consumer hors market_metrics.v1, pas de vue contrat associée |

---

## Critères `CLOSE_GATE_MASTER_TARGET` du parent — état actuel

Les critères suivants sont issus de `GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md` :

| Critère | Requis | Atteint | Manquant |
|---|---|---|---|
| ≥2 surfaces lisant depuis data/data_center/ | 2 | 1 (Desk Pro) | 1 consumer runtime réel de plus |
| ≥2 producers avec contrats formalisés et testés | 2 | 2 (bitget, binance) | `last_write` null (prod non confirmé) |
| ≥2 consumers avec lecture prouvée depuis data/data_center/ | 2 | 1 (Desk Pro) | 1 consumer implémenté de plus |
| Tests contractuels smoke passant | req. | OUI — 135/135 PASS | — |
| Documentation reprise par consumer actif | req. | Desk Pro documenté | autres consumers not_started |
| Aucun gap bloquant non documenté | req. | OUI — ce document | — |

**Conclusion** : PF_DATA_CENTER ne peut pas être fermé. Il manque au minimum 1 consumer runtime réel de plus.

---

## NEXT_GO recommandés

### Priorité 1 — Valeur opérationnelle immédiate

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_LOCALCMS_HEALTH_READER_01
```

Implémenter `localcms__data_center_health` : lire `_registry/producers.json` depuis LocalCMS.
Hors market_metrics.v1 — périmètre étroit, valeur ops immédiate, satisfait partiellement le critère "≥2 consumers".

### Priorité 2 — Pair market snapshot

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PAIR_SNAPSHOT_VIEW_01
```

Créer `views/pair_market_snapshot/` et déclarer `desk_pro__spot_snapshot` comme 2ème consumer runtime.
Satisfait le critère "≥2 consumers lisant depuis data/data_center/", ce qui rapproche du `CLOSE_GATE_MASTER_TARGET`.

### Priorité 3 — Telegram screener reader

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_TELEGRAM_SCREENER_READER_01
```

Implémenter `telegram_screener__signal_context` quand `PF_TELEGRAM_SCREENER` est activé.

### Priorité 4 — Confirm prod writes

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_WRITE_VALIDATION_01
```

Confirmer `last_write` non-null sur bitget et binance (run réel + injection `_registry/producers.json`).
