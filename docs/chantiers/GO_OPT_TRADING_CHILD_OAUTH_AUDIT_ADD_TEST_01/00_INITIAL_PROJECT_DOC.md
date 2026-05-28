---
go_id: GO_OPT_TRADING_CHILD_OAUTH_AUDIT_ADD_TEST_01
status: closed
lifecycle_stage: done
created_at: 2026-05-28
closed_at: 2026-05-28
---

# GO_OPT_TRADING_CHILD_OAUTH_AUDIT_ADD_TEST_01

## Objectif

Ajouter des tests pour `aw_oauth_audit` (`scripts/ai/workers/oauth_scope_audit.py`) — candidate, high risk.

Contrainte : module-level code s'exécute à l'import → tests via subprocess + regex isolation.

## Livrable

`tests/test_oauth_scope_audit.py` — 30 tests, 4 classes :
- `TestScriptOutput` (12) — subprocess : JSON valide, clés requises, status, structure
- `TestScopePatterns` (9) — regex isolation : inline_scope, oauth_assign, permission_assign, google_api
- `TestFindingsLogic` (5) — logique WARN/PASS/high_count isolée
- `TestScriptIntegrity` (3) — fichier, contenu, scan_dirs

## Verdict

```
30/30 PASS
JOBS_REGISTRY.md v1.4 : aw_oauth_audit add_test → keep
```
