---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_DRY_RUN_LOCALCMS_GATE_01_TEST_REPORT
doc_type: test_report
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_DRY_RUN_LOCALCMS_GATE_01
updated_at: 2026-05-26
---

# 30_TEST_REPORT

## Résultats

| Suite | Fichier | Tests | Résultat |
|-------|---------|-------|----------|
| Gate LocalCMS (unité + subprocess) | `tests/e2e/test_dry_run_pipeline_localcms_gate.py` | 28 | **PASS** |
| E2E existants | `tests/e2e/test_e2e_dry_run_pipeline.py` | 23 | **PASS** |
| **Total** | | **51** | **ALL PASS** |

## Commandes

```bash
python3 -m unittest tests/e2e/test_dry_run_pipeline_localcms_gate.py -v
python3 -m unittest tests/e2e/test_e2e_dry_run_pipeline.py -v
```

## Détail par classe — gate tests

### TestCheckLocalcmsAvailable (3 tests)
- `test_reachable_returns_true` — mock 200 → `(True, "")`
- `test_unreachable_returns_false` — mock OSError → `(False, "Connection refused")`
- `test_never_raises` — jamais d'exception propagée

### TestClassifyLocalcmsGate (11 tests)
- `test_default_mode_present_is_pass`
- `test_default_mode_absent_is_warn_skipped`
- `test_require_mode_absent_is_blocked`
- `test_require_mode_present_is_pass`
- `test_skip_mode_always_warn_skipped`
- `test_skip_mode_no_network_call` — vérifie que `check_localcms_available` n'est pas appelé
- `test_gate_result_has_required_fields`
- `test_blocked_reason_contains_url`
- `test_warn_skipped_does_not_contain_blocked`
- `test_invalid_url_default_is_warn_skipped`
- `test_invalid_url_require_is_blocked`

### TestScriptLocalcmsGate (14 tests subprocess)
- `test_default_mode_absent_localcms_exits_0`
- `test_default_mode_gate_status_warn_skipped`
- `test_default_mode_e2e_status_pass`
- `test_require_mode_absent_localcms_exits_1`
- `test_require_mode_gate_status_blocked`
- `test_require_mode_e2e_status_fail`
- `test_skip_mode_exits_0`
- `test_skip_mode_gate_status_warn_skipped`
- `test_report_has_localcms_gate_key`
- `test_report_backward_compat_localcms_key`
- `test_localcms_gate_has_status_reason_url_mode`
- `test_7_steps_still_present`
- `test_all_ok_true_in_default_mode`
- `test_mode_in_gate_report`

## Vérifications manuelles

```bash
# Default — LocalCMS absent
python3 scripts/e2e/dry_run_pipeline.py
# → rc=0, localcms_gate.status=WARN_SKIPPED, e2e_status=PASS

# Require — LocalCMS absent
REQUIRE_LOCALCMS_E2E=1 python3 scripts/e2e/dry_run_pipeline.py
# → rc=1, localcms_gate.status=BLOCKED, e2e_status=FAIL
```
