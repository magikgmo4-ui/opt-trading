---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_ARTIFACT_STABILITY_POST_MERGE_SYNC_01_30_TEST_VALIDATION
doc_type: chantier/test_validation
repo: opt-trading
machine: admin-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_ARTIFACT_STABILITY_POST_MERGE_SYNC_01
status: active
scope: doc-only
executed_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_ARTIFACT_STABILITY_POST_MERGE_SYNC_01/40_NEXT_DECISION.md
---

# 30_TEST_VALIDATION

## Commande initiale

```powershell
ssh admin-trading "cd /opt/trading && PYTHONPATH=. python -m pytest tests/test_signal_event_adapter.py tests/test_admin_trading_contract_compatibility_smoke.py tests/test_desk_pro_dry_run.py tests/test_desk_pro_artifact_output.py -q"
```

Resultat :

```text
/usr/bin/python: No module named pytest
```

## Diagnostic environnement

Un environnement local existe dans `/opt/trading/venv` :

```text
./venv/bin/activate
./venv/bin/pytest
./venv/bin/python
```

## Commande retenue

```powershell
ssh admin-trading "cd /opt/trading && PYTHONPATH=. ./venv/bin/python -m pytest tests/test_signal_event_adapter.py tests/test_admin_trading_contract_compatibility_smoke.py tests/test_desk_pro_dry_run.py tests/test_desk_pro_artifact_output.py -q"
```

## Resultat

```text
..............................................................           [100%]
62 passed in 0.14s
```

## Conclusion tests

Gate desk-pro post-merge : **PASS**.

## RISKS

- À qualifier.
