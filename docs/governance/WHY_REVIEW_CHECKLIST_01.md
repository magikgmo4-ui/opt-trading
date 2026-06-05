---
doc_id: WHY_REVIEW_CHECKLIST_01
repo: opt-trading
status: draft
scope: governance
orientation: IA_AND_HUMAN
---

# WHY_REVIEW_CHECKLIST_01

## Objectif

Verifier qu'un GO, une review ou une implementation conserve une couche WHY suffisante.

## Checklist WHY

### Intentions

- [ ] Le WHY est explicitement documente.
- [ ] L'intention produit est identifiable.
- [ ] Le cout d'une rupture est mentionne.

### Invariants

- [ ] Les invariants sont documentes.
- [ ] Les surfaces interdites sont identifiees.
- [ ] Les protections runtime sont explicites.

### Failure modes

- [ ] Les derives connues sont identifiees.
- [ ] Les risques IA sont identifies.
- [ ] Les risques multi-machine sont identifies.

### Tradeoffs

- [ ] Les compromis sont documentes.
- [ ] Le choix retenu est justifie.
- [ ] Les alternatives refusees sont comprenables.

### Gouvernance

- [ ] La separation AUDIT/APPLY est respectee.
- [ ] Le GO reste coherent avec le parent produit.
- [ ] L'etat reel est verifie.

### IA-oriented

- [ ] Une IA pourrait comprendre pourquoi certaines actions sont interdites.
- [ ] Une IA pourrait reprendre le chantier sans hallucination majeure.
- [ ] Une optimisation naive serait naturellement bloquee.

## Verdicts

| Niveau | Interpretation |
| --- | --- |
| FAIL | WHY insuffisant |
| PARTIAL | WHY present mais incomplet |
| PASS | WHY coherent et exploitable |
| STRONG_PASS | WHY IA-oriented mature |

## RISKS

- À qualifier.
