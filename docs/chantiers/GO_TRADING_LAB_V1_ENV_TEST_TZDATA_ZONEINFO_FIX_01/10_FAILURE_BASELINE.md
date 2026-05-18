---
go_id: GO_TRADING_LAB_V1_ENV_TEST_TZDATA_ZONEINFO_FIX_01
doc_type: failure_baseline
---

# 10_FAILURE_BASELINE

## Baseline constatee

Sur `modules/trading_lab_v1/tests/test_core_runner_v1.py` :

- `7` echecs preexistants ;
- symptome principal : `ZoneInfo("America/Montreal")` ;
- exception associee : `ModuleNotFoundError: No module named 'tzdata'`.

## Interpretation

Le code appelle `zoneinfo.ZoneInfo` sur un environnement Windows/Python ou les donnees IANA ne sont pas disponibles sans le package `tzdata`.
