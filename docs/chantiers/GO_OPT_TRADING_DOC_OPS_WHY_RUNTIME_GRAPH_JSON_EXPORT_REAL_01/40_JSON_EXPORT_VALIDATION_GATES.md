# 40_JSON_EXPORT_VALIDATION_GATES

## 1_MASTER_TARGET

Definir les gates minimaux qui valident le premier export JSON reel avant tout render graphique futur.

## WHY

Un export reel ne doit pas etre accepte uniquement parce qu'un fichier JSON existe. Il doit etre borne, explicable, reproductible et encore subordonne a la sequence canonique qui place le render apres validation de cet export.

## 7_CANONICAL_STATE

Gates retenus :

| Gate | Etat attendu | Motif |
| --- | --- | --- |
| base mergee PR #498 | REQUIRED | l'export doit partir du mapping Daily Journal valide |
| scope borne | REQUIRED | pas d'extension implicite a tous les overlays |
| provenance documentaire | REQUIRED | chaque noeud et edge doit etre justifiable |
| read-only | REQUIRED | aucune mutation runtime ou CI |
| artefact versionnable | REQUIRED | diff texte simple et stable |
| render graphique | BLOCKED_AFTER_JSON_ONLY | etape strictement posterieure |

## 8_DECISION

Decision retenue :

1. Valider d'abord un export JSON minimal et inspectable.
2. Reporter tout render, overlay ou extension large apres validation de cet export.
3. Refuser tout livrable qui saute directement de la doc vers le graph rendu.

## 12_INVARIANTS

- `JSON export reel != render graphique complet`.
- `JSON export reel != runtime mutation`.
- `JSON export reel != CI/validator modification automatique`.
- `JSON export reel = artefact borne, inspectable, reproductible`.

## 17_RESUME_POINT

Le GO est considere pret pour execution reelle uniquement si la base mergee est disponible localement, que le JSON reste borne et que tout render reste explicitement differe.

## 18_VERDICT

```text
WIP / JSON_EXPORT_GATES_LOCKED / NO_RENDER_BEFORE_VALID_JSON
```
