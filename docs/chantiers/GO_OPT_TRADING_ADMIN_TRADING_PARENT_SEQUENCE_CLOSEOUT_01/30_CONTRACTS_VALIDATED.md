---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01_CONTRACTS_VALIDATED
doc_type: contracts_validated
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 30_CONTRACTS_VALIDATED - Contracts Validated

## Contrats définis et validés

### 1. signal_event V1

| Champ | Valeur |
| --- | --- |
| Défini dans | `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01/30_SIGNAL_EVENT_CONTRACT.md` |
| Validé par | `GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01` (adapter V0→V1) |
| Smoke | `GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01` (30/30 tests) |
| Status | **VALIDATED** |

Champs requis: `source`, `event_type`, `engine`, `symbol`, `timeframe`, `direction`, `timestamp`, `status`

### 2. visual_context V1

| Champ | Valeur |
| --- | --- |
| Défini dans | `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01/30_VISUAL_CONTEXT_CONTRACT.md` |
| Validé par | `GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01` (fixture) |
| Status | **VALIDATED** |

Champs requis: `source`, `capture_id`, `symbol`, `timeframe`, `captured_at`, `image_ref`, `status`

### 3. desk_snapshot

| Champ | Valeur |
| --- | --- |
| Défini dans | `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01/40_DESK_BRIDGE_COMPATIBILITY.md` |
| Validé par | `GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01` (fixture) |
| Status | **CONFIRMED** (runtime actif, format observé) |

Champs: `symbol`, `tf`, `snapshot_ts`, `path`, `ingested_at`, `source`, `host`

### 4. Desk Pro synthesis object

| Champ | Valeur |
| --- | --- |
| Défini dans | `GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01/40_CONTRACT_COMPATIBILITY_REVIEW.md` |
| Validé par | `GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01` (smoke test) |
| Status | **VALIDATED** |

Contient: `signal_event` + `visual_context` + `desk_snapshot` + `join_keys`

## Matrice de validation

| Contract | Producer | Consumer | Validation | Status |
| --- | --- | --- | --- | --- |
| signal_event V1 | webhook (V0 → adapter) | Desk Pro | adapter + 30 tests + smoke | VALIDATED |
| visual_context V1 | headless/ShareX | Desk Pro | fixture + smoke | VALIDATED |
| desk_snapshot | desk_bridge | Desk Pro | runtime + fixture + smoke | CONFIRMED |
| Desk Pro synthesis | ensemble | Desk Pro | smoke test | VALIDATED |

## Jointures cross-contract

| Artifact A | Artifact B | Join key | Compatible? |
| --- | --- | --- | --- |
| signal_event | visual_context | symbol + timeframe + timestamp fenêtre | YES |
| signal_event | desk_snapshot | symbol + timeframe + snapshot_ts fenêtre | YES |
| visual_context | desk_snapshot | symbol + timeframe | YES |
| signal_event | visual_context | visual_context_ref = capture_id | YES (ref non produite) |

## RISKS

- À qualifier.
