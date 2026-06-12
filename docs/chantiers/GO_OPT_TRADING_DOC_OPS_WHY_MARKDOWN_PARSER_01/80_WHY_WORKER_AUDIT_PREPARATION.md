# 80_WHY_WORKER_AUDIT_PREPARATION

## Objectif

Preparer le futur worker d'audit WHY sans implementation active.

## Role futur du worker

Le worker pourrait:
- scanner les documents,
- detecter les sections WHY,
- detecter les gaps,
- produire un score WHY,
- produire un rapport d'audit.

## Dependances requises

| Dependance | Etat |
| --- | --- |
| sections spec | PASS |
| output schema | PASS |
| gap detection | PASS |
| scoring preparation | PASS |
| edge cases | PASS |
| false positive policy | PASS |
| runtime limits | PASS |

## Sorties candidates

| Sortie | But |
| --- | --- |
| why_audit_report.json | audit machine-readable |
| why_gaps.md | rapport humain |
| why_score_summary.md | synthese score |

## Invariants

- Aucun APPLY.
- Aucun merge automatique.
- Aucun blocage runtime autonome.
- Worker orienté audit uniquement.

## 17_RESUME_POINT

Avant implementation reelle du worker:
- stabiliser les conventions markdown WHY,
- stabiliser les classes R0-R5,
- stabiliser la governance WHY.

## RISKS

- À qualifier.
