---
go_id: GO_TRADING_LAB_V1_ENV_TEST_TZDATA_ZONEINFO_FIX_01
doc_type: dependency_decision
---

# 20_ENV_DEPENDENCY_DECISION

## Decision

Ajouter `tzdata` dans `requirements.txt`.

## Justification

- le repo utilise deja `requirements.txt` comme surface de dependances ;
- le probleme est environnemental, pas metier ;
- ajouter la dependance est plus petit et plus propre qu'un fallback metier dans `trading_lab_v1`.

## Non-choix

- pas de refactor `ZoneInfo` ;
- pas de fallback applicatif custom ;
- pas de changement de logique de dates/timezones.

## RISKS

- À qualifier.
