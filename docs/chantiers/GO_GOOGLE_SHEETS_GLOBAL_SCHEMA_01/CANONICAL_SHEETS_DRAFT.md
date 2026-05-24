---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01_CANONICAL_SHEETS_DRAFT
doc_type: schema_tables_draft
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: draft
source_kind: canonical
updated_at: 2026-05-24
---

# CANONICAL_SHEETS_DRAFT — liste des feuilles (V1)

## Règles

- une feuille doit avoir un producer ou un consumer identifié
- une feuille doit avoir une clé primaire (même composite)
- pas de payload complet en cellule : utiliser `*_ref` (path/id)
- timestamps ISO UTC (`YYYY-MM-DDTHH:MM:SSZ`)
- `schema_version` doit être visible (tab registry ou colonne)

## Feuilles candidates (V1)

```text
sheets_registry
go_registry
signal_events
market_metrics
desk_snapshots
telegram_claims
visual_context
watchlists
jobs_registry
run_logs
data_quality
refs_registry
```

## Compatibilité avec le cadrage existant

Le cadrage actuel propose déjà des tabs “journal/perf/registry” (voir `20_GLOBAL_SCHEMA_TARGET.md`) :

```text
daily_sessions
strategy_events
strategy_perf
strategy_gates
registry_candidates
```

Ces deux listes doivent être unifiées via le child “canonical tables” :

- soit renommer/migrer vers la nomenclature “registry/*_events/*_metrics”
- soit conserver les tabs existantes et ajouter les tabs registry manquantes

## Next

```text
GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_CANONICAL_TABLES_01
```

