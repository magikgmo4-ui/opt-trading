# 10_JSON_EXPORT_SOURCE_SURFACES

## 1_MASTER_TARGET

Definir les surfaces documentees minimales qui alimentent le premier export JSON reel du WHY runtime graph.

## WHY

Le premier export reel doit prouver une extraction bornée depuis les sources deja stabilisees, sans tenter de couvrir tout le repo ni d'introduire d'indexation globale.

## 7_CANONICAL_STATE

Surfaces retenues pour le premier export reel :

| Surface | Role dans l'export | Statut | Source documentaire amont |
| --- | --- | --- | --- |
| spine `LocalCMS/TMUX` | noeuds runtime centraux | REQUIRED | `GO_OPT_TRADING_DOC_OPS_WHY_LOCALCMS_TMUX_GRAPH_INTEGRATION_01` |
| Daily Journal | ancrage `run_id`, timeline et preuves | REQUIRED | `GO_OPT_TRADING_DOC_OPS_WHY_DAILY_JOURNAL_GRAPH_EXPORT_MAPPING_01` |
| inventaire surfaces runtime | vocabulaire et relations autorisees | REQUIRED | `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_SURFACES_INVENTORY_01` |
| overlays security | hors premier export minimal | DEFERRED | overlay futur apres export valide |
| WHY lint warnings | hors premier export minimal | DEFERRED | overlay futur apres export valide |
| render/static views | consumer futur uniquement | DEFERRED | pas source canonique du premier export |

## 8_SOURCE_BOUNDARY

Perimetre minimal recommande :

1. Noeuds centraux representant les surfaces `LocalCMS`, `TMUX` et `Daily Journal`.
2. Edges documentant les relations `run_id`, session runtime, timeline et preuves associees.
3. Metadonnees de provenance renvoyant vers les documents source qui justifient chaque noeud ou relation.

Ce premier export ne doit pas embarquer :

- l'ensemble des overlays d'observabilite ;
- des warnings security ;
- des agregations globales inter-GO ;
- des donnees runtime live ;
- des snapshots non relies au mapping Daily Journal deja valide.

## 12_INVARIANTS

- Une source documentaire amont doit exister pour chaque champ exporte.
- Aucun noeud ne doit supposer une relation runtime non documentee.
- Les surfaces differees restent hors JSON initial meme si elles sont deja connues.
- Le premier export privilegie la preuve de chainage sur l'exhaustivite.

## 17_RESUME_POINT

Le premier export JSON reel doit se limiter a la spine `LocalCMS/TMUX` plus le mapping `Daily Journal`, avec provenance documentaire explicite et sans overlays futurs.
