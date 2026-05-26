---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_DRY_RUN_LOCALCMS_GATE_01_EXISTING_E2E_READ
doc_type: surface_read
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_DRY_RUN_LOCALCMS_GATE_01
updated_at: 2026-05-26
---

# 10_EXISTING_E2E_READ

## État avant ce GO

### scripts/e2e/dry_run_pipeline.py (avant)

- 348 lignes, 8 étapes
- Step 1c : `from modules.notification_dispatcher.app.dispatcher import NotificationDispatcher` en dur → crash si `requests` absent du venv
- Step 8 : `check_lcms_endpoints()` appelle les 4 endpoints sans gate structurée
- `localcms_ok` booléen calculé mais **non inclus dans le exit code** (exit basé sur `all_ok` steps 1-7 uniquement)
- `sys.exit(0 if ok else 1)` avec `ok = report.get("all_ok", False)`

### Constat : le rc=1 vient du crash requests, pas de LocalCMS

Le venv n'a pas `requests`. `NotificationDispatcher` l'importe via `shared.telegram_notify`. Le script crashait à step 1c avec `ModuleNotFoundError`. Le exit code 1 ne provenait pas du check LocalCMS (step 8) — il ne l'atteignait pas.

### tests/e2e/test_e2e_dry_run_pipeline.py (avant)

23 tests. Les tests subprocess (`test_pipeline_script_runs`, `test_closeout_no_artifacts`, etc.) échouaient car le script crashait avec rc=1 dans le venv.

### Modules LocalCMS

Pas de `modules/localcms/` ni `modules/data_center/localcms_health_reader.py` dans ce repo. Le check LocalCMS est uniquement dans le script E2E.

## Modes attendus (spec utilisateur)

| Mode | Env var | Résultat si absent | rc |
|------|---------|-------------------|----|
| default | — | WARN_SKIPPED | 0 |
| require | `REQUIRE_LOCALCMS_E2E=1` | BLOCKED | 1 |
| skip | `SKIP_LOCALCMS_E2E=1` | WARN_SKIPPED (no probe) | 0 |
| url custom | `LOCALCMS_URL=http://...` | selon disponibilité | selon mode |
