---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01_TEST
doc_type: test_report
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01
status: DONE
created_at: 2026-05-26
---

# 30_TEST_REPORT

## Résultats

| Suite | Résultat |
|-------|----------|
| `tests/e2e/test_e2e_report_bundle.py` (65 tests) | 65/65 PASS |
| `tests/e2e/` complet (219 tests) | 219/219 PASS |

## Classes de tests

| Classe | Tests | Couverture |
|--------|-------|------------|
| `TestEnvValidation` | 5 | _validate_env() — required/forbidden flags |
| `TestReportValidation` | 8 | _validate_report() — live_trade, gate_status, dry_run, BLOCKED, missing |
| `TestBundleWriters` | 22 | _build_manifest, _build_payload_refs, _build_summary_md, write_bundle |
| `TestBuildBundleUnit` | 3 | build_bundle() avec --pipeline-output (sans subprocess pipeline) |
| `TestCLIEnvRefused` | 5 | CLI subprocess — exit 1 sur flags incorrects |
| `TestBundleIntegration` | 22 | Run complet subprocess + vérification bundle |

## Tests critiques validés

- `test_result_status_bundled` — status == BUNDLED
- `test_result_verdict_pass` — verdict == PASS
- `test_result_gate_status_approved_paper` — gate_status == APPROVED_PAPER
- `test_result_live_trade_false` — live_trade == false
- `test_result_dry_run_true` — dry_run == true
- `test_manifest_7_modules` — 7 modules présents
- `test_no_secrets_in_bundle_dir` — aucun secret dans le bundle
- `test_build_bundle_live_trade_refused` — live_trade=True → REFUSED
- `test_build_bundle_wrong_gate_status_refused` — gate_status=REJECTED → REFUSED
- `test_no_allow_e2e_flag_exits_1` — exit 1 si flag manquant

## Commandes

```bash
python3 -m pytest tests/e2e/test_e2e_report_bundle.py -q
python3 -m pytest tests/e2e/ -q
```
