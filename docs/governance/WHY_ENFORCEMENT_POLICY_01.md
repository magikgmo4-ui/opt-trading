---
doc_id: WHY_ENFORCEMENT_POLICY_01
repo: opt-trading
status: draft
scope: governance
orientation: IA_AND_HUMAN
---

# WHY_ENFORCEMENT_POLICY_01

## Objectif

Definir comment le WHY layer doit etre applique et protege dans le repo.

## Principe central

Aucune implementation critique ne devrait etre acceptee sans:
- intention explicite,
- invariants,
- risques identifies,
- logique de reprise,
- coherence produit.

## Enforcement minimal

### GO critiques

Les GO critiques devraient contenir:
- WHY,
- INVARIANTS,
- FAILURE_MODES,
- TRADEOFFS,
- RESUME_POINT.

### Runtime sensible

Toute surface runtime:
- multi-machine,
- trading,
- orchestration,
- webhook,
- ingestion,
- provider routing,

devrait exiger un WHY explicite.

### IA

Toute action proposee par IA devrait:
- verifier les invariants,
- verifier le parent produit,
- verifier les gates,
- verifier les failure modes connus.

## Cas de refus

Un chantier peut etre refuse si:
- le WHY est absent,
- le risque runtime est flou,
- les tradeoffs sont inconnus,
- le GO est decore mais sans intention produit,
- une optimisation casse les invariants.

## Escalade

| Niveau | Action |
| --- | --- |
| WHY faible | review supplementaire |
| WHY absent | blocage |
| runtime critique sans WHY | FAIL immediat |
| derive IA detectee | retour AUDIT |

## Direction future

Possibilites futures:
- scoring automatique WHY,
- lint documentaire WHY,
- gates CI governance,
- validation IA pre-merge,
- registry global invariants/failure modes.
