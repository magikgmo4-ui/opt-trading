---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01_COMPAT_MATRIX
doc_type: compatibility_matrix
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 40_COMPATIBILITY_MATRIX - Compatibility Matrix

## Producer → Consumer compatibility

| Producer | Artifact | Consumer | Compatible? | Evidence |
| --- | --- | --- | --- | --- |
| webhook (V0) | signal_event V1 | Desk Pro | YES | `normalize_signal_event_v1` + `validate_signal_event_v1` |
| headless/ShareX | visual_context V1 | Desk Pro | YES | Fixture validation, join keys |
| desk_bridge | desk_snapshot | Desk Pro | YES | Fixture validation, join keys |
| signal_event V1 | visual_context_ref | visual_context V1 | YES | `capture_id` linkage |
| visual_context V1 | desk_snapshot_ref | desk_snapshot | YES | symbol + timeframe join |

## Cross-contract join keys

| Artifact A | Artifact B | Join key | Compatible? | Gap |
| --- | --- | --- | --- | --- |
| signal_event | visual_context | `symbol` + `timeframe` + `timestamp` fenêtre | YES | symbol normalisation nécessaire (BTCUSDT → BTCUSDT.P) |
| signal_event | desk_snapshot | `symbol` + `timeframe` + `snapshot_ts` fenêtre | YES | symbol normalisation nécessaire |
| visual_context | desk_snapshot | `symbol` + `timeframe` | YES | direct |
| signal_event | visual_context | `visual_context_ref` = `capture_id` | YES | ref non produite actuellement |
| signal_event | desk_snapshot | `desk_snapshot_ref` | YES | ref non produite actuellement |

## Desk Pro synthesis compatibility

| Champ synthesis | Source | Format | Compatible? |
| --- | --- | --- | --- |
| `signal_event` | adapter V0→V1 | dict V1 | YES |
| `visual_context` | contrat V1 | dict V1 | YES |
| `desk_snapshot` | desk_bridge | dict | YES |
| `join_keys` | dérivé | dict | YES |

## Known gaps (non bloquants)

| Gap | Impact | Severity | Status |
| --- | --- | --- | --- |
| symbol `BTCUSDT` vs `BTCUSDT.P` | join nécessite normalisation | MEDIUM | DOCUMENTED |
| `visual_context_ref` non produit | ref explicite non disponible | LOW | FUTURE |
| `desk_snapshot_ref` non produit | ref explicite non disponible | LOW | FUTURE |
| `signal_event_ref` non produit | ref explicite non disponible | LOW | FUTURE |
| `payload_hash` non produit (visual_context) | déduplication non disponible | LOW | FUTURE |

## Verdict

**Tous les contrats sont compatibles.** Les gaps sont des enrichissements futurs, pas des blocages.
