---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01_INBOX
doc_type: inbox_entry
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01
pf_id: PF_OPENCLAW_ORCHESTRATOR_FULL
status: DONE
created_at: 2026-05-26
closed_at: 2026-05-26
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01

**Objectif** : Créer un générateur de bundle transportable transformant un run post-gate en bundle auditabl à 5 fichiers.

**Résultat** : PASS

## Ce qui a été fait

- `scripts/e2e/build_e2e_report_bundle.py` : validations env/report + `BundleRefused` + 5 fichiers bundle
- `.gitignore` : entrée explicite `data/e2e_report_bundles/`
- `tests/e2e/test_e2e_report_bundle.py` : 65 tests (unit + intégration)

## Résultats tests

| Suite | Résultat |
|-------|----------|
| `tests/e2e/test_e2e_report_bundle.py` (65 tests) | 65/65 PASS |
| `tests/e2e/` complet (219 tests) | 219/219 PASS |

## Sortie nominale

```json
{
  "status": "BUNDLED",
  "bundle_dir": "data/e2e_report_bundles/20260526_120000",
  "run_id": "20260526_120000",
  "verdict": "PASS",
  "gate_status": "APPROVED_PAPER",
  "dry_run": true,
  "live_trade": false,
  "modules": {
    "signal_router": "PASS",
    "proposition_engine": "PASS",
    "validation_gate": "PASS",
    "trade_executor": "PASS",
    "result_tracker": "PASS",
    "datasheet_writer": "PASS",
    "learning_feeder": "PASS"
  }
}
```

## Chantier

`docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01/`
