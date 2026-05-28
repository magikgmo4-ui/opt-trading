# BUNDLE TARGETS — GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_INDEX_SYNC_01

## Chaîne

```
PF_GOVERNANCE_TRANSPORT
-> MT_GOVERNANCE_MASTER_PROJECT_PLAN_INDEX_SYNC
-> MPP_GOVERNANCE_MASTER_PROJECT_PLAN_INDEX
-> 6_FINAL_TARGET: synchroniser index globaux comme MASTER_PROJECT_PLAN_INDEX
-> BUNDLE_TARGET: audit doc-only + constat de synchronisation
-> GO_ID: GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_INDEX_SYNC_01
```

## Targets

| Target | Fichiers | Statut |
|---|---|---|
| T1 — Audit | `10_AUDIT_INDEX_SYNC.md` | ✅ |
| T2 — Plan | `20_INDEX_SYNC_PLAN.md` | ✅ |
| T3 — Validation | `30_VALIDATION.md` | ✅ |
| T4 — Gaps | `40_GAPS_AND_NEXT_GO.md` | ✅ |
| T5 — Closeout | `90_CLOSEOUT.md` | ✅ |
| T6 — FILE_SCOPE | `FILE_SCOPE.txt` | ✅ |
| T7 — Bundle meta | `TARGETS.md` + `target_card.json` | ✅ |

## Index sync — différé

`NEXT_GO_CANDIDATES.md` et `REPRISE.md` : audit effectué, modifications documentées,
mais pas appliquées (lock overlap avec 9 autres GO — gate `no-lock-overlap`).
