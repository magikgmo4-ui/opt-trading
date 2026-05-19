---
doc_id: WHY_RUNTIME_RISK_CLASSIFICATION_01
repo: opt-trading
status: draft
scope: governance
orientation: IA_AND_HUMAN
parent: SYSTEM_WHY_LAYER_01
---

# WHY_RUNTIME_RISK_CLASSIFICATION_01

## Objectif

Classifier les surfaces runtime selon leur criticite WHY.

## Classification candidate

| Classe | Description |
| --- | --- |
| R0 | doc-only |
| R1 | tooling local non critique |
| R2 | runtime observable |
| R3 | orchestration multi-machine |
| R4 | trading live / execution critique |
| R5 | systeme critique avec impact financier direct |

## Exigences WHY par classe

| Classe | WHY requis |
| --- | --- |
| R0 | optionnel |
| R1 | recommande |
| R2 | WHY + RESUME_POINT |
| R3 | WHY + INVARIANTS + FAILURE_MODES |
| R4 | WHY + gates + tradeoffs + reprise |
| R5 | governance complete + review humaine obligatoire |

## Exemples

| Surface | Classe candidate |
| --- | --- |
| docs/chantiers | R0 |
| scripts locaux | R1 |
| dashboard observateur | R2 |
| orchestration OpenClaw | R3 |
| webhook trading live | R4 |
| execution financiere automatique | R5 |

## Direction future

Cette classification pourrait servir:
- au WHY lint,
- aux CI gates,
- aux reviews runtime,
- aux audits IA.

## Invariant

Cette classification reste informative tant qu'aucune enforcement runtime n'est validee.
