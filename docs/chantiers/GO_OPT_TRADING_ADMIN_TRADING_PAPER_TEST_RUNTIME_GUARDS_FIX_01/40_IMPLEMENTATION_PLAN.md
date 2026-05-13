---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01_40_IMPLEMENTATION_PLAN
doc_type: chantier/implementation
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01
status: active
scope: bounded-runtime-guard
checked_at: 2026-05-13
---

# 40_IMPLEMENTATION_PLAN

## Fichiers modifies

| Fichier | Changement |
| --- | --- |
| `modules/webhook/paper_guards.py` | nouveau helper pur d'evaluation des guards `PAPER_TEST` |
| `webhook_server.py` | preflight `PAPER_TEST` avant effets de bord, endpoint `/api/paper/guards`, exclusion `PAPER_TEST` du ledger perf |
| `tests/test_paper_test_runtime_guards.py` | tests unitaires des guards |

## Placement du guard

Dans `webhook_server.py`, `require_paper_test_runtime_guards()` est appele immediatement apres validation de `engine` et `signal`, avant:

- `enforce_lock`;
- risk sizing;
- ledger perf;
- event log;
- Telegram;
- execution paper.

## Exclusion ledger perf

Avant patch, `PAPER_TEST` n'etait pas traite comme moteur de test pour le ledger perf.

Apres patch:

```text
TV_TEST, PAPER_TEST, TEST_*, _TEST_* bypassent le ledger perf.
```

## Limite volontaire

Ce GO ne lance pas `PAPER_TEST` et ne modifie pas la configuration runtime cible. Il fournit le guard detectable et le blocage pre-effet de bord. La prochaine tentative paper doit encore capturer un etat AVANT/APRES et verifier `/api/paper/guards` en PASS avant tout payload.
