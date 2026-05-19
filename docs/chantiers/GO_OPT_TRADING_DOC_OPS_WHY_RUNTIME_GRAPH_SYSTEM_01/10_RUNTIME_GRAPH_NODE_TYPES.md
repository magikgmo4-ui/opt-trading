# 10_RUNTIME_GRAPH_NODE_TYPES

## Objectif

Definir les types de noeuds du futur WHY runtime graph system.

## Noeuds candidats

| Node type | Role |
| --- | --- |
| PRODUCT | produit ou surface fonctionnelle |
| GO | chantier ou sous-chantier |
| MACHINE | machine physique ou logique |
| RUNTIME_SURFACE | service, script, dashboard ou flux actif |
| EXTERNAL_SURFACE | ClickUp, Botpress, KG, Airtable |
| GOVERNANCE_DOC | document de doctrine ou matrice |
| INVARIANT | contrainte non negociable |
| GATE | validation requise |
| FAILURE_MODE | risque ou derive connue |
| RECOVERY_PATH | chemin de reprise |
| OBSERVABILITY | preuve, log, freshness, endpoint |
| HUMAN_REVIEW | decision humaine requise |
| RUNTIME_CLASS | classe R0-R5 |

## Regles

- Chaque noeud doit avoir un type explicite.
- Les noeuds runtime critiques doivent etre relies a une classe R0-R5.
- Les surfaces externes doivent rester candidates tant qu'aucune integration active n'est validee.
- Les invariants et gates doivent etre representables comme noeuds ou attributs.

## Invariant

Le graphe doit representer l'etat documentaire prouve, sans inferer des noeuds runtime absents.
