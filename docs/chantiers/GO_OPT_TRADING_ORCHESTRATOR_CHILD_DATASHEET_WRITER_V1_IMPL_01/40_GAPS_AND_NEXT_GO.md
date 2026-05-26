---
doc_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01_GAPS_AND_NEXT_GO
doc_type: gaps_and_next_go
repo: opt-trading
go_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01
status: active
source_kind: canonical
updated_at: 2026-05-26
---

# 40_GAPS_AND_NEXT_GO — Lacunes et prochains GOs

## Ce GO ne livre pas

| Hors scope | Raison |
|---|---|
| Modification de `DatasheetWriter.write()` | Changement de signature évité — adapter standalone |
| Câblage runtime dans l'orchestrateur | GO orchestrateur dédié |
| Appel Google API réel | Credentials + flag hors scope |
| Adapter pour `daily_sessions` | `daily_sessions` = session-level, pas trade-level |
| Adapter pour `strategy_perf` | PK composite (as_of + strategy_id + metric_name + window) — nécessite agrégation |
| Historisation des exports Sheets | Append vs. replace policy à définir par le caller |

## Lacunes connues non bloquantes

- `closed_at` dans `TradeRecord` vient de `datetime.isoformat()` qui produit `+00:00`. L'adapter normalise en `Z`. Si le format de `closed_at` change dans une future version de `ResultTracker`, `_to_iso_utc_z()` peut nécessiter une mise à jour.
- Les colonnes `ticker`, `outcome`, `net_pnl` sont des extras (pas dans `required` du schema `strategy_events`). Elles passent la validation mais ne sont pas contractuellement définies pour ce tab.
- `payload_ref=""` (vide) si le JSONL path n'est pas fourni — la ligne Sheets aura un `payload_ref` vide. Acceptable en V1.

## Prochain GO

**GO_OPT_TRADING_ORCHESTRATOR_CHILD_LEARNING_FEEDER_V1_IMPL_01** — câblage `learning_feeder` → `SheetsWriter` runtime (même pattern que ce GO).
