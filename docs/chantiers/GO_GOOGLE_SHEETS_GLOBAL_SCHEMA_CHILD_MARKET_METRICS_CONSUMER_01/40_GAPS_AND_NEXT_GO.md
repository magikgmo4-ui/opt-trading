---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01_GAPS_AND_NEXT_GO
doc_type: gaps_and_next_go
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01
status: active
source_kind: canonical
updated_at: 2026-05-26
---

# 40_GAPS_AND_NEXT_GO — Lacunes et prochains GOs

## Ce GO ne livre pas

| Hors scope | Raison |
|---|---|
| Appel Google Sheets API réel | GO ou runtime activation séparé |
| Multi-symbol (by_symbol/) | Consumer lit `latest.json` seulement — un payload à la fois |
| Enregistrement dans `consumers.json` | Le registry consumers.json peut être étendu dans un GO dédié |
| Cron / scheduler | Runtime wiring délégué à orchestrateur |
| Header row dans Sheets | Géré par le caller ou un GO de migration |
| Metric name mapping (ex: `open_interest` → `open_interest_usd`) | Décision de nommage déléguée au GO suivant si nécessaire |

## Lacunes connues non bloquantes

- `map_mm_v1_to_rows()` passe les noms de métriques tels quels depuis le payload v1 (`open_interest`, `funding_rate`). La fixture Sheets dans PR #809 utilisait `open_interest_usd` à titre illustratif. Le schéma n'a pas d'enum sur `metric_name` → aucun impact R1-R10.
- `source_ref` utilise `str(source_path)` pour les paths non-defaults — les chemins absolus apparaîtront tels quels dans Sheets. Normaliser vers un chemin relatif si nécessaire dans un GO suivant.

## Prochains GOs (ordre logique)

1. **GO_OPT_TRADING_DATA_CENTER_CHILD_GOOGLE_SHEETS_CONSUMER_01** — consumer Data Center → Google Sheets plus large (registry + orchestration multi-surfaces), à ouvrir après la preuve bornée `market_metrics`
2. **GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01** — migration des titres de worksheets (renommage canonique si nécessaire)
3. **GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01** — câblage datasheet_writer → SheetsWriter runtime
4. **GO_OPT_TRADING_ORCHESTRATOR_CHILD_LEARNING_FEEDER_V1_IMPL_01** — câblage learning_feeder → SheetsWriter runtime
