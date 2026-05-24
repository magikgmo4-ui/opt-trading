---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PARENT_ACCEPTANCE_REVIEW_01_REMAINING_GAPS
doc_type: gaps_and_next_go
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PARENT_ACCEPTANCE_REVIEW_01
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 30_REMAINING_GAPS_AND_NEXT_GO

Ces gaps ne bloquent pas la fermeture du parent. Chacun requiert un GO dédié dans `PF_DATA_CENTER` (OPEN).

---

## Gaps consumer — readers non implémentés

| Gap | Consumer | Contrat | access_pattern | Priorité |
|---|---|---|---|---|
| GAP-C01 | `telegram_screener__signal_context` | `market_metrics.v1` | `latest_only` | Opérationnel — dès activation Telegram screener |
| GAP-C02 | `google_sheets__market_reporting` | `market_metrics.v1` | `latest_only` | Reporting — dès implémentation Sheets consumer |
| GAP-C03 | `strategy_framework__market_context` | `market_metrics.v1` | `by_symbol` | Stratégie — dès implémentation PF_STRATEGY_FRAMEWORK |
| GAP-C04 | `perf_engine__replay_context` | `market_metrics.v1` | `full_history` | Lab — dès besoin replay historique |
| GAP-C05 | `desk_pro__spot_snapshot` | `pair_market_snapshot.v1` | `latest_only` | Spot — dès câblage collector → DC view |

---

## Gaps producer — confirms runtime

| Gap | Producer | Note |
|---|---|---|
| GAP-P01 | `derivatives_collector__bitget` | `last_write: null` — pas de write prod confirmé |
| GAP-P02 | `derivatives_collector__binance` | `last_write: null` — pas de write prod confirmé |
| GAP-P03 | `collector_binance_spot` | `output_path_root` dans DC déclaré mais write vers `data/data_center/` non câblé (écrit encore dans `modules/collector_binance_spot/outputs/`) |
| GAP-P04 | `coinglass` | `NOT_PROVEN_RUNTIME_ADAPTER` permanent — headless seulement, pas de producer DC |

---

## Gaps infrastructure

| Gap | Objet | Note |
|---|---|---|
| GAP-I01 | `manifest.json` par producer | Déclaré dans le plan parent, pas encore créé |
| GAP-I02 | `status.json` par producer | Idem — layout partiel |
| GAP-I03 | Schema versioning `v2+` | `schema_version: v1` fixé, pas de migration path |
| GAP-I04 | `_registry/` live update | `producers.json` et `consumers.json` sont statiques — pas de write runtime |
| GAP-I05 | Contract class `null` pour localcms | `localcms__data_center_health` lit uniquement le registry Python, pas de vue contrat |

---

## PF_DATA_CENTER_UNIVERSAL_SCOPE

`PF_DATA_CENTER` est la **base universelle normalisée de données trading**. Les gaps ci-dessous
ne sont pas des défauts — ils sont des extensions naturelles d'une plateforme ouverte.

Aucun de ces gaps ne bloque la fermeture du parent initial. Chacun est une **extension de
`PF_DATA_CENTER`**, pas une réouverture du parent.

```text
PF_DATA_CENTER = OPEN — data layer universel, non limité à market_metrics.v1 et pair_market_snapshot.v1
```

## NEXT_GO recommandés

### Priorité 1 — Confirm prod writes

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_WRITE_VALIDATION_01
```

Confirmer `last_write` non-null sur bitget et binance après un run réel avec injection dans
`_registry/producers.json`.

### Priorité 2 — Desk Pro spot snapshot reader

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_SPOT_SNAPSHOT_READER_01
```

Câbler `collector_binance_spot` pour écrire vers `data/data_center/spot/collector_binance_spot/`,
activer `write_pair_market_snapshot_view()`, implémenter le reader Desk Pro `desk_pro__spot_snapshot`.
Satisfait GAP-C05 + GAP-P03.

### Priorité 3 — Telegram screener reader

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_TELEGRAM_SCREENER_READER_01
```

Implémenter `telegram_screener__signal_context` quand `PF_TELEGRAM_SCREENER` est activé.
Satisfait GAP-C01.

### Priorité 4 — Registry live update

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_LIVE_UPDATE_01
```

Injecter `last_write` dans `_registry/producers.json` après chaque run producer réel.
Satisfait GAP-I04 + GAP-P01 + GAP-P02.
