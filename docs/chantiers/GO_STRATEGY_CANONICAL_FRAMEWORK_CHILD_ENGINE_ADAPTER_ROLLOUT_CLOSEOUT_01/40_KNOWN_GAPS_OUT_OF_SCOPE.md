---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_ENGINE_ADAPTER_ROLLOUT_CLOSEOUT_01
doc_type: known_gaps
---

# 40_KNOWN_GAPS_OUT_OF_SCOPE

## Gap environnement test

Les echecs restants sur `modules/trading_lab_v1/tests/test_core_runner_v1.py` sont preexistants et hors scope du rollout adapter.

### Symptome

- `ZoneInfo("America/Montreal")`
- `ModuleNotFoundError: No module named 'tzdata'`

### Statut

- non cause par les changements adapter ;
- non necessaire pour valider le rollout read-only ;
- a traiter dans un chantier environnement/test separe.

## Separation de sujets

Ne pas melanger :

1. cloture rollout adapter strategie ;
2. remediation `tzdata` / `ZoneInfo`.

## RISKS

- À qualifier.
