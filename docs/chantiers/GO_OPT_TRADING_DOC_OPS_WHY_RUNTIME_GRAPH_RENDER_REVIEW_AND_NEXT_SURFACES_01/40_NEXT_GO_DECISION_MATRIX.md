# 40_NEXT_GO_DECISION_MATRIX

## 1_MASTER_TARGET

Choisir la prochaine suite canonique apres review du rendu local v0.

## WHY

La decision doit eviter deux erreurs : enrichir le modele avant de comprendre les limites de lecture, ou ouvrir un dashboard avant que le render statique soit stable.

## 7_CANONICAL_STATE

Matrice de decision :

| Option | Repond au gap dominant | Risque scope | Readiness | Decision |
| --- | --- | --- | --- | --- |
| render readability refinement | oui | faible | READY | SELECTED |
| JSON enrichment | partiellement | moyen | DEFERRED | NOT_NEXT |
| LocalCMS graph view integration | partiellement | moyen/eleve | DEFERRED | NOT_NEXT |
| graph traversal / navigation | non immediat | eleve | BLOCKED | NOT_NEXT |
| dashboard prototype | non immediat | tres eleve | BLOCKED | NOT_NEXT |

## 8_DECISION

Decision retenue :

```text
NEXT_CANONICAL_GO = GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_RENDER_READABILITY_REFINEMENT_01
```

Motif :

- le rendu v0 est valide et borne ;
- le gap dominant est la lisibilite, pas l'absence de donnees ;
- le JSON doit rester stable pendant un premier refinement de presentation ;
- LocalCMS, traversal et dashboard doivent attendre un render statique plus explicite.

## 9_RECOMMENDED_NEXT_GO_SCOPE

Le prochain GO devrait produire :

- un rendu Markdown v1 depuis le meme JSON valide ;
- des labels courts pour les edges ;
- une legende node/edge ;
- une table `relation courte -> relation JSON source` ;
- une table de provenance par node et par edge ;
- un rapport court prouvant que le JSON n'a pas ete enrichi.

## 10_BLOCKED_UNTIL

| Surface | Gate avant ouverture |
| --- | --- |
| JSON enrichment | finding montrant qu'un besoin ne peut pas etre resolu par presentation |
| LocalCMS graph view integration | rendu statique suffisamment lisible et contrat de vue read-only |
| graph traversal / navigation | graph plus riche et besoin de navigation documente |
| dashboard prototype | gates separes, no-live clarifie, review humaine explicite |

## 12_INVARIANTS

- Ne pas lancer de dashboard depuis ce GO.
- Ne pas modifier runtime, validator, CI ou index global.
- Ne pas produire de nouveau render dans cette review.
- Ne pas enrichir le JSON sans GO dedie.

## 17_RESUME_POINT

La suite canonique recommandee est `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_RENDER_READABILITY_REFINEMENT_01`.

## 18_VERDICT

```text
PASS / NEXT_GO_SELECTED_RENDER_READABILITY_REFINEMENT
```
