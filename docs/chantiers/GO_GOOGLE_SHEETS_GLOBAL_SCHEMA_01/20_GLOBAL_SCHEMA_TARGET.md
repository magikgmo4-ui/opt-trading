---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01_GLOBAL_SCHEMA_TARGET
doc_type: schema
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: active
source_kind: canonical
updated_at: 2026-05-24
---

# 20_GLOBAL_SCHEMA_TARGET - Tabs + colonnes (V1)

## Objectif

Définir un schéma Sheets global, stable, qui couvre:

- journal daily session (déjà existant)
- événements stratégie (observations)
- perf / scores
- gates / registry lifecycle

Ce schéma reste compatible avec l’écriture contrôlée (dry-run par défaut).

## Tabs V1 (cibles)

### 1) `daily_sessions`

Source: `data/journal/daily/<run_id>.json` via `scripts/sheets/sync_daily_session.py`.

Colonnes (ordre canonique):

```text
run_id
date
signal
side
ticker
action
confidence
verdict
exec_status
fill_price
outcome
net_pnl
datasheet_written
bridge_status
brick_stored
tmux_before
tmux_after
localcms_before_ok
localcms_after_ok
closeout_acknowledged
duration_s
all_ok
```

### 2) `strategy_events`

Rôle: une ligne par event observé / enrichi (taxonomy V1).

Colonnes (min):

```text
event_id
produced_at
event_type
family
run_id
strategy_id
symbol
timeframe
signal_id
source_surface
dry_run
payload_ref
summary
```

### 3) `strategy_perf`

Rôle: agrégats / score vectors.

Colonnes (min):

```text
as_of
strategy_id
metric_name
metric_value
window
source
dry_run
notes
```

### 4) `strategy_gates`

Rôle: décisions de promotion / retrait, et raisons.

Colonnes (min):

```text
as_of
strategy_id
gate_name
verdict
reason
evidence_ref
dry_run
```

### 5) `registry_candidates`

Rôle: candidats registry (draft) avant promotion.

Colonnes (min):

```text
as_of
strategy_id
candidate_name
status
owner
notes
dry_run
```

## Notes

- `payload_ref` doit pointer vers un artefact local (json path / id), pas contenir un payload complet en cellule.
- Les tabs 2-5 restent doc-only tant qu’aucun writer transverse n’est implémenté.

## Ancrage umbrella

- `MASTER_TARGET` : standardiser Google Sheets pour le produit final total
- `Tableau Kanban du bundle` : reste la navigation principale
- `Produit final total voulu` : chaines separees mais liees entre webhook, Desk Pro, Telegram, Sheets, Perf et runtime
- `Prochain item Kanban exact` : `GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_INVENTORY_01`
- `Gaps encore ouverts` : writer transverse absent, tabs 2-5 non materialisees, schema a garder versionne avant toute ecriture
