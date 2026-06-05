---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01_CANONICAL_FIELD_MODEL
doc_type: field_model
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 40_CANONICAL_FIELD_MODEL

## Objet

Definir comment chaque champ de donnee pro desk doit etre decrit avant mapping vers l'existant.

## Field descriptor cible

Chaque champ canonique doit pouvoir etre documente ainsi :

```yaml
data_key: open_interest
data_class: flow_positioning
priority: P10
semantic_type: numeric_metric
asset_scope:
  - crypto_perp
  - futures
unit_policy: source_declared_required
contract_candidates:
  - market_metrics.v1
  - flow_positioning.v1
source_policy: multi_source_scored
freshness_target: near_realtime
resolver_required: true
deskpro_use: contextual
strategy_use: contextual
perf_use: replay_context
validation_rules:
  - numeric_or_null
  - timestamp_required
  - source_id_required
  - stale_flag_required
quality_metadata_required:
  - source_id
  - producer_id
  - observed_at
  - received_at
  - freshness_score
  - validation_score
  - final_score
current_status: partial_existing_no_score
```

## Semantic types

```text
identifier
numeric_metric
price
volume
ratio
percentage
timestamp
enum_state
text_event
structured_event
image_ref
file_ref
risk_metric
model_score
quality_score
```

## Source policies

```text
single_source_allowed
multi_source_scored
multi_source_consensus
manual_verified_only
internal_state_authoritative
external_reference_authoritative
legacy_until_migrated
```

## Freshness targets

```text
realtime
near_realtime
oneshot
batch_daily
batch_weekly
historical
stale_ok
manual_review
```

## DeskPro use labels

```text
required
high_contextual
contextual
optional
future
not_for_deskpro
```

## Minimum quality metadata

Aucune donnee candidate ne doit devenir best value sans :

```text
source_id
producer_id or source_family
observed_at or event_at
received_at or written_at
schema_version
validation_status
freshness_status
```

Pour les donnees multi-sources, ajouter :

```text
source_score
freshness_score
validation_score
completeness_score
consistency_score
final_score
resolver_decision_id
```

## Regle de fallback

Un fallback peut exister, mais il doit etre declare comme tel. Une donnee fallback ne doit pas masquer une panne de source primaire si le consumer exige `fallback:error`.
