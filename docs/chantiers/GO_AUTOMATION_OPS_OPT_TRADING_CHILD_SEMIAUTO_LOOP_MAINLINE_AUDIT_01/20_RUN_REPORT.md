# 20_RUN_REPORT

## Run ID

`pilot_0e1e6443`

## Date

2026-05-28

## Verdict pilote

`PASS_DRY_RUN` — exit 0

---

## Résultats d'audit

### PRs ouvertes

**0 PRs ouvertes.** Mainline propre.

### 8 derniers commits sot/mainline

| Commit | Message |
|--------|---------|
| `fade2d0f` | docs(registry): clarify mimo open observer state (#925) |
| `116914d1` | Merge pull request #923 — GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_MERGED_SCOPE_BYPASS_01 |
| `ad32df00` | Merge pull request #875 — GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TERMUX_TASKER_RUNTIME_PROOF_01 |
| `ae41b092` | fix(gated-pr): ignore inactive GO scope locks |
| `89d08081` | Merge pull request #924 — GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_PILOT_REAL_CASE_01 |
| `1e1faeb9` | feat(GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_PILOT_REAL_CASE_01): premier run réel pilote semi-auto |
| `e7d0ef76` | fix(gated-pr): ignore merged GO scope locks |
| `9b9f66d9` | Merge pull request #920 — GO_OPT_TRADING_DATA_CENTER_CHILD_BINANCE_SPOT_COLLECTOR_RUNTIME_01 |

### Module semiauto_pilot

`modules/automation_ops/semiauto_pilot/` — présent, 5 fichiers Python.

### Tests

```
17/17 PASS
```

---

## Observation

`sot/mainline` est dans un état post-merge stable :
- Aucune PR ouverte.
- Derniers merges : automation_ops, android, github_actions, data_center.
- Module semi-auto opérationnel.
- Tests inchangés.

## Gate humain

`human_gate_required: true`

Décision requise : `next_go` vide — aucun GO suivant imposé. Opérateur choisit.
