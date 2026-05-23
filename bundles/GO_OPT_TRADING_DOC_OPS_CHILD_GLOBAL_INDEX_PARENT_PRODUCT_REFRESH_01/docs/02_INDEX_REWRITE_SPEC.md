# 02_INDEX_REWRITE_SPEC

## GO_INDEX.md — format cible

Doit devenir l'index des parents produits seulement.

Colonnes recommandées :

```markdown
| PARENT_PRODUCT_GO | PRODUIT_UTILISABLE | STATUT | TARGET_COURANT | NEXT_ACTION | SOURCE |
|---|---|---|---|---|---|
```

## ACTIVE_STREAMS.md — format cible

Doit contenir uniquement les parents vivants.

Structure recommandée :

```markdown
### <PARENT_GO_ID>
- produit utilisable :
- statut :
- gap restant :
- target courant :
- next action :
- blocage réel :
```

## NEXT_GO_CANDIDATES.md — format cible

Règle :

```text
1 parent produit -> 1 target ou 1 next GO primaire
```

Colonnes recommandées :

```markdown
| parent produit | produit | priority | next target / next GO | condition | refs |
```

## REPRISE.md — format cible

Doit devenir un point de reprise court.

Sections recommandées :

```markdown
## Point de reprise global
## Parents produits actifs
## Target courant
## Prochaine action forte
## Hors pilotage immédiat
```

## GO_CLOSED_INDEX.md

À modifier seulement si des entrées sont réellement reclassées CLOSED/PASS.

## BRANCH_STATE.md

Ne pas modifier dans ce GO, sauf note minimale si nécessaire :

```text
BRANCH_STATE nécessite un recount Git séparé avant toute opération de cleanup.
```
