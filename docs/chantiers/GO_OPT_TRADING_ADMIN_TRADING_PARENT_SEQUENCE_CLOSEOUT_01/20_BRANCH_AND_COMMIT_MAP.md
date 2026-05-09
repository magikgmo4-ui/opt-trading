---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01_BRANCH_COMMIT_MAP
doc_type: branch_and_commit_map
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 20_BRANCH_AND_COMMIT_MAP - Branch and Commit Map

## Arbre des branches (chaîne de dépendance)

```
sot/mainline
  └── go/ADMIN_TRADING_PARENT_REVIEW_01 @ 9454396
        └── go/ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01 @ 0a0b01c
              └── go/ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01 @ 20c7026
                    └── go/ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01 @ 8c01d6d
                          └── go/ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01 @ fc5f64a
                                └── go/ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01 @ f458385
                                      └── go/ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01 @ 23febd4
                                            └── go/ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01 @ (ce commit)
```

## Table complète

| Étape | Branche | Commit | Verdict | Notes |
| --- | --- | --- | --- | --- |
| 1 | `go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01` | `9454396` | PASS | Audit machine, runtime, services, gaps |
| 2 | `go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01` | `0a0b01c` | PASS | Webhook endpoints, ports, producer draft |
| 3 | `go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01` | `20c7026` | PASS | signal_event V1 contract defined |
| 4 | `go/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01` | `8c01d6d` | PASS | visual_context V1, desk_bridge compat |
| 5 | `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01` | `fc5f64a` | PASS | Desk Pro consumer audit |
| 6 | `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01` | `f458385` | PASS | Adapter code + 30 tests |
| 7 | `go/GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01` | `23febd4` | PASS | Smoke 40/40 tests |
| 8 | `go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01` | (ce commit) | PASS | Sequence closeout |

## Branche de reprise

L'étape 5 (`DESK_PRO_RUNTIME_REVIEW`) a nécessité une branche de reprise car la branche distante existante était stale (base différente). La reprise a été créée proprement depuis la base correcte.
