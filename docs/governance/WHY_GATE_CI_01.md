---
doc_id: WHY_GATE_CI_01
repo: opt-trading
status: draft
scope: governance
orientation: IA_AND_HUMAN
parent: SYSTEM_WHY_LAYER_01
---

# WHY_GATE_CI_01

## Objectif

Definir une future gate CI documentaire orientee WHY layer.

## Vision

Avant merge d'un chantier critique, la CI pourrait verifier:
- presence du WHY,
- presence des invariants,
- coherence parent produit,
- presence du RESUME_POINT,
- presence des failure modes critiques.

## Niveaux possibles

| Niveau | Effet |
| --- | --- |
| advisory | commentaire uniquement |
| warning | warning CI |
| blocking | merge bloque |

## Candidates blocking

- runtime trading critique sans invariants,
- orchestration multi-machine sans reprise,
- runtime apply sans separation AUDIT/APPLY,
- GO critique sans WHY.

## Non-objectifs

- ne pas remplacer la review humaine,
- ne pas evaluer la qualite metier profonde,
- ne pas auto-refactoriser des documents.

## Direction future

Possibilites:
- parser markdown WHY,
- score WHY automatique,
- verification de sections obligatoires,
- correlation runtime risk classification.

## Invariant

Aucune CI active n'est introduite par ce document.

## RISKS

- À qualifier.
