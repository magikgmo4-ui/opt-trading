---
go_id: GO_TRADING_LAB_V1_ENV_TEST_TZDATA_ZONEINFO_FIX_01
go_type: child
repo: opt-trading
status: open
created_at: 2026-05-18
surface: env / test
---

# GO_TRADING_LAB_V1_ENV_TEST_TZDATA_ZONEINFO_FIX_01

## 00_INITIAL_PROJECT_DOC

### 1_OBJECTIF

Corriger les echecs preexistants de `trading_lab_v1` lies a `ZoneInfo("America/Montreal")` et a l'absence de `tzdata`.

### 2_CONTEXTE

- rollout adapter strategie complet et clos ;
- `modules/trading_lab_v1/tests/test_strategy_id_adapter_readonly.py` passe ;
- `modules/trading_lab_v1/tests/test_core_runner_v1.py` echoue en environnement Python local a cause de `tzdata` manquant.

### 3_SCOPE

- traiter le sujet comme dependance environnement/test ;
- ne pas rouvrir le rollout adapter strategie ;
- ne pas modifier la logique trading sauf necessite minimale.

## RISKS

- À qualifier.
