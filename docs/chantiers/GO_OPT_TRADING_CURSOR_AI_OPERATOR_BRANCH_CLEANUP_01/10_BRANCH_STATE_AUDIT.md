---
doc_id: GO_OPT_TRADING_CURSOR_AI_OPERATOR_BRANCH_CLEANUP_01_10_BRANCH_STATE_AUDIT
doc_type: chantier/branch_state_audit
repo: opt-trading
machine: cursor-ai
status: active
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
---

# 10_BRANCH_STATE_AUDIT

## Branches cursor-ai remote

| Branche remote | Statut | Note |
| --- | --- | --- |
| `origin/go/...CURSOR_AI_CLAUDE_COWORK_LIVE_ARTIFACTS_REVIEW_01` | PRESENT | Historique, MACHINE_WORK_SPLIT |
| `origin/go/...CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_PARENT_CLOSEOUT_01` | PRESENT | CLOSED (transport/docs), MACHINE_WORK_SPLIT |

Toutes les branches cursor-ai de la sequence PR #205-#213 sont **supprimees en remote** (auto-delete via `gh pr merge --delete-branch`).

## Branches cursor-ai locales (stale)

Ces branches locales ont ete mergees mais sont encore presentes localement :

| Branche locale | PR | Remote supprimee | Action recommandee |
| --- | --- | --- | --- |
| `go/...PARENT_OPERATIONAL_PLAN_01` | #205 | OUI | Supprimer localement |
| `go/...CLAUDE_ARTIFACTS_OPERATOR_PACK_01` | #206 | OUI | Supprimer localement |
| `go/...BUNDLES_APPLICATION_ACTIVE_01` | #207 | OUI | Supprimer localement |
| `go/...ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01` | #208 | OUI | Supprimer localement |
| `go/...OPERATOR_REPRISE_PACKET_01` | #209 | OUI | Supprimer localement |
| `go/...ALERT_WEBHOOK_TEST_SAFE_01` | #210 | OUI | Supprimer localement |
| `go/...BUNDLES_MAINTENANCE_01` | #211 | OUI | Supprimer localement |
| `go/...OPERATOR_EXPORT_01` | #213 | OUI | Supprimer localement |

## Branches cursor-ai locales conservees

| Branche locale | Raison |
| --- | --- |
| `go/...OPERATOR_BRANCH_CLEANUP_01` | Branche de travail actuelle |
| `go/...CLAUDE_COWORK_LIVE_ARTIFACTS_REVIEW_01` | Reference MACHINE_WORK_SPLIT |
| `go/...OBSERVER_TRADINGVIEW_MCP_PARENT_CLOSEOUT_01` | CLOSED (transport/docs) |

## Resume

- **8 branches locales stales** a supprimer.
- **2 branches locales conservees** (historique).
- **0 branche orpheline non documentee**.
- **Aucune collision machine** (toutes dans bloc CURSOR_AI).

## RISKS

- À qualifier.
