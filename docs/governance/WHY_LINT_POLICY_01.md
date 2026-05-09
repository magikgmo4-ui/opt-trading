---
doc_id: WHY_LINT_POLICY_01
repo: opt-trading
status: draft
scope: governance
orientation: IA_AND_HUMAN
parent: SYSTEM_WHY_LAYER_01
---

# WHY_LINT_POLICY_01

## Objectif

Definir une future politique de lint documentaire pour verifier la presence minimale du WHY layer dans les documents critiques.

## Principe

Un lint WHY ne doit pas juger la qualite philosophique d'un document.

Il doit verifier la presence de blocs structurants:
- WHY,
- INVARIANTS,
- FAILURE_MODE ou RISKS,
- TRADEOFFS,
- RESUME_POINT,
- relation au parent produit.

## Surfaces candidates

| Surface | Niveau lint |
| --- | --- |
| `docs/chantiers/*/00_INITIAL_PROJECT_DOC.md` | requis |
| `docs/chantiers/*/*CLOSEOUT*.md` | requis |
| `docs/governance/*.md` | recommande |
| reviews runtime critiques | requis |
| docs purement historiques | optionnel |

## Regles candidates

- Un GO critique sans WHY explicite devrait etre marque `WARN`.
- Un GO runtime sans INVARIANTS devrait etre marque `FAIL`.
- Un closeout sans RESUME_POINT devrait etre marque `WARN`.
- Une modification runtime sans FAILURE_MODE devrait etre bloquee avant APPLY.

## Sorties proposees

| Sortie | Sens |
| --- | --- |
| PASS | WHY suffisant |
| WARN | WHY present mais incomplet |
| FAIL | WHY absent sur surface critique |
| SKIP | surface non critique |

## Invariant

Ce document ne cree aucun enforcement actif. Il cadre seulement une future politique de lint documentaire.
