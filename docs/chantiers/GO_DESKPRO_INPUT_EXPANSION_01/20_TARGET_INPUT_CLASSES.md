---
doc_id: GO_DESKPRO_INPUT_EXPANSION_01_TARGET_INPUT_CLASSES
doc_type: contract
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 20_TARGET_INPUT_CLASSES - Inputs cibles (V1)

## Objectif

Unifier les inputs Desk Pro sous des classes “contract-first”, compatibles avec la taxonomie transverse (GO_EVENT_TAXONOMY_01), sans imposer un seul format technique (dataclass vs dict).

## Classes cibles

### A. `signal_event.v1`

Consumer: Desk Pro hub (decision context).

Payload candidat (repo): `modules/desk_pro/signal_event_adapter.py` (dict V1).

Champs pivots:

- `symbol`
- `timeframe`
- `timestamp`
- `direction`

### B. `desk_snapshot.v1`

Consumer: Desk Pro hub (state + vision anchor).

Payload candidat (repo): dict actuel `{symbol, tf, snapshot_ts, path, ...}`.

Champs pivots:

- `symbol`
- `tf`
- `snapshot_ts`
- `path` (image_ref)

### C. `visual_context.v1`

Consumer: Desk Pro hub (vision metadata).

Payload candidat (repo): dict validé par `modules/desk_pro/dry_run.py`.

Champs pivots:

- `capture_id`
- `symbol`
- `timeframe`
- `captured_at`
- `image_ref`

### D. `vision_analysis.v1` (cible)

Consumer: Desk Pro hub (extractions structurées).

Source attendue: pipeline vision/headless (après survivant canonique).

Champs pivots:

- `capture_id` (ref)
- `symbol`, `timeframe`
- `analysis_ts`
- `signals` (structure)

### E. `market_metrics.v1` (cible)

Consumer: Desk Pro hub (context marché).

Source attendue: collectors / coinglass / marketdata.

Champs pivots:

- `symbol`
- `metrics_ts`
- `metrics` (structure)

### F. `telegram_claim.v1` (cible)

Consumer: Desk Pro hub (claims inbound, watch-only).

Source attendue: Telegram screener inbound (après registry channels).

Champs pivots:

- `source_channel_alias`
- `claimed_at`
- `symbol`
- `claim_kind` (`trade_claim` / `setup` / `news`)

## Jointures minimales (policy)

- `symbol` : normalisation autorisée (ex: `BTCUSDT` ↔ `BTCUSDT.P`) mais jamais implicite sans warning
- `timeframe` : doit matcher entre `signal_event.timeframe` et `desk_snapshot.tf` pour une synthèse “PASS”
- `timestamp window` : jointure temporelle tolérée (H1 ± 5 min) uniquement en mode observation

## Ancrage umbrella

- `MASTER_TARGET` : standardiser les inputs Desk Pro du produit final total
- `Tableau Kanban du bundle` : reste la navigation principale
- `Produit final total voulu` : chaines separees mais liees entre webhook, Desk Pro, Telegram, Sheets, Perf et runtime
- `Prochain item Kanban exact` : `GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01`
- `Gaps encore ouverts` : wrappers read-only absents, `vision_analysis`/`market_metrics`/`telegram_claim` encore contractuels, policy de refs a appliquer chez les producers
