---
go_id: GO_TRADING_LAB_V1_ENV_TEST_TZDATA_ZONEINFO_FIX_01
doc_type: gate_decision
---

# 40_GATE_DECISION

## Gate

**PASS_TRADING_LAB_TZDATA_ZONEINFO_ENV_TEST_FIX**

## Conditions validees

- `tzdata` ajoute a la surface de dependances ;
- `modules/trading_lab_v1/tests/test_core_runner_v1.py` : `10/10` ;
- `modules/trading_lab_v1/tests/test_strategy_id_adapter_readonly.py` : `4/4` ;
- `python tools/strategy/validate_strategy_registry.py` : `UNREGISTERED prod = 0` ;
- aucune logique trading modifiee.

## RISKS

- À qualifier.
