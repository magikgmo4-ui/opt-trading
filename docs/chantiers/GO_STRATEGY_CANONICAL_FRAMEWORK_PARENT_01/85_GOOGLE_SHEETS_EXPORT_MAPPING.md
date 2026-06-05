---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
child_go: GO_STRATEGY_GOOGLE_SHEETS_EXPORT_MAPPING_01
doc_type: google_sheets_export_mapping
repo: opt-trading
status: open
created_at: 2026-05-17
surface: doc-only
---

# 85_GOOGLE_SHEETS_EXPORT_MAPPING

---

## 1_OBJECTIF

Definir un mapping d'export Google Sheets pour les strategies, sans ecriture
automatique.

Invariant :

```text
No automatic Google Sheets write.
```

Sheets est un consumer optionnel et controle.

---

## 2_EXISTING_CONTEXT

LocalCMS `_build_metrics()` lit deja `data/journal/sync_log.jsonl` et expose :

```text
sheets_sync.dry_run
sheets_sync.written
sheets_sync.blocked
sheets_sync.failed
```

Le cadre strategie doit respecter ce modele : tout write est explicite,
controle et auditable.

---

## 3_EXPORT_TABS

Tabs recommandees :

| Tab | Contenu |
| --- | --- |
| `strategy_events` | Une ligne par `ObservationEvent` enrichi. |
| `strategy_summary` | Agregats par `strategy_id` + `strategy_version`. |
| `strategy_gates` | Dernier verdict promotion/retrait. |
| `strategy_replay` | Etat replay et labels Trading Lab. |
| `strategy_perf` | Metrics Perf Engine. |

---

## 4_STRATEGY_EVENTS_COLUMNS

| Column | Source |
| --- | --- |
| `run_id` | `ObservationEvent.run_id` |
| `run_date` | `ObservationEvent.run_date` |
| `strategy_id` | `ObservationEvent.strategy.strategy_id` |
| `strategy_version` | `ObservationEvent.strategy.strategy_version` |
| `setup_type` | `ObservationEvent.strategy.setup_type` |
| `symbol` | `ObservationEvent.signal.symbol` |
| `timeframe` | `ObservationEvent.signal.timeframe` |
| `direction` | `ObservationEvent.signal.direction` |
| `confidence` | `ObservationEvent.signal.confidence` |
| `entry_zone` | `ObservationEvent.trade_plan.entry_zone` |
| `invalidation` | `ObservationEvent.trade_plan.invalidation` |
| `target_zone` | `ObservationEvent.trade_plan.target_zone` |
| `status` | `ObservationEvent.status` |
| `outcome` | `ObservationEvent.outcome` |
| `pnl_net` | `ObservationEvent.pnl_net` |
| `observation_status` | `ObservationEvent.gates.observation_status` |
| `perf_status` | `ObservationEvent.gates.perf_status` |
| `promotion_gate` | `ObservationEvent.gates.promotion_gate` |
| `retirement_gate` | `ObservationEvent.gates.retirement_gate` |
| `source_file` | `ObservationEvent.source_file` |

---

## 5_EXPORT_MODES

| Mode | Autorise | Description |
| --- | --- | --- |
| `DRY_RUN_EXPORT` | Oui | Produit payload/log, aucun write. |
| `MANUAL_REVIEW_EXPORT` | Oui | Operateur inspecte avant write. |
| `CONTROLLED_WRITE` | Seulement child dedie | Write explicite, audite, avec logs. |
| `AUTOMATIC_WRITE` | Non | Interdit par ce parent. |

---

## 6_BLOCKERS

Export bloque si :

```text
strategy_id missing
source_file missing
ObservationEvent invalid
secrets exposed
automatic write requested
runtime mutation requested by parent
```

---

## 7_OUTPUT_EXPECTATION

Le child futur doit produire :

```text
mapping columns
dry-run payload example
validation checklist
operator approval requirement
sync log fields
```

Il ne doit pas activer le write automatique.

## RISKS

- À qualifier.
