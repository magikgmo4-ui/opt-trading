---
go_id: GO_TRADING_LAB_V1_ENV_TEST_TZDATA_ZONEINFO_FIX_01
go_type: child
repo: opt-trading
status: closed
closed_at: 2026-05-18
surface: env / test
---

# 90_CLOSEOUT

## Statut

**CLOSED** - gap `tzdata` / `ZoneInfo` corrige sur l'environnement de test.

## Validations

- `modules/trading_lab_v1/tests/test_core_runner_v1.py` : `10/10`
- `modules/trading_lab_v1/tests/test_strategy_id_adapter_readonly.py` : `4/4`
- `python tools/strategy/validate_strategy_registry.py` : OK

## Portee

- ajout de `tzdata` dans `requirements.txt`
- aucune modification de la logique trading

## RISKS

- À qualifier.
