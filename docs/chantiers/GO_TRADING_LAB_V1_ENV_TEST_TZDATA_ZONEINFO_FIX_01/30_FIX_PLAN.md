---
go_id: GO_TRADING_LAB_V1_ENV_TEST_TZDATA_ZONEINFO_FIX_01
doc_type: fix_plan
---

# 30_FIX_PLAN

## Plan

1. Ajouter `tzdata` a `requirements.txt`.
2. Installer la dependance dans l'environnement de test courant.
3. Rejouer :
   - `modules/trading_lab_v1/tests/test_core_runner_v1.py`
   - `modules/trading_lab_v1/tests/test_strategy_id_adapter_readonly.py`
   - `python tools/strategy/validate_strategy_registry.py`
4. Verifier qu'aucune logique `trading_lab_v1` n'a ete modifiee.

## RISKS

- À qualifier.
