# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Ouvrir `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_SURFACES_INVENTORY_01` pour etablir le premier inventaire canonique des surfaces runtime reelles qui alimenteront le futur WHY/runtime graph.

## WHY

Le resume point precedent qui enchainait directement vers un export JSON reel est maintenant invalide.

Les merges OpenClaw, TMUX, LocalCMS, daily journal et WHY/security recents ont change le perimetre source du futur graph : il n'est plus seulement documentaire, il doit representer des surfaces runtime reelles, leurs preuves, leurs overlays et leurs dependances.

## 3_INITIAL_NEED

Avant toute integration graph plus avancee, il faut inventorier de facon canonique :

- les types de surfaces runtime devenues pertinentes ;
- leurs proprietaires ;
- leurs relations ;
- leur criticite `R0-R5` ;
- les preuves runtime disponibles ;
- les points de review humaine obligatoires.

## 5_GO_SCOPE

Ce GO couvre uniquement un inventaire doc-only des surfaces suivantes :

- OpenClaw runtime ;
- TMUX runtime ;
- LocalCMS ;
- daily journals ;
- validators ;
- lint WHY ;
- security aggregators ;
- observability artefacts.

Ce GO ne couvre pas encore :

- l'integration graph LocalCMS/TMUX ;
- le mapping export du daily journal ;
- l'export JSON graph reel ;
- l'overlay WHY lint dans le graph ;
- un dashboard live ;
- un traversal runtime reel.

## 7_CANONICAL_STATE

Etat etabli a l'ouverture :

- `40_RECONCILED_RESUME_POINT.md` porte l'etat `SUPERSEDED_PREVIOUS_ORDER` ;
- le nouvel ordre recommande commence par `graph runtime surfaces inventory` ;
- `PR #468`, `#470`, `#471`, `#474`, `#475` et `#477` modifient le perimetre source du graph ;
- les surfaces influentes confirmees incluent la spine TMUX, LocalCMS, le daily session journal, le runtime security validation aggregator, le WHY lint validator et les control scans ;
- aucun runtime live, aucune CI active et aucun connecteur live ne sont autorises par ce GO.

## 8_VALIDATED_PLAN

1. Lister les types de surfaces runtime a representer.
2. Attribuer ownership et responsabilite de review.
3. Cartographier les relations structurantes entre surfaces.
4. Evaluer leur criticite `R0-R5` et les preuves runtime associees.
5. Publier un resume point qui enchaine vers `GO_OPT_TRADING_DOC_OPS_WHY_LOCALCMS_TMUX_GRAPH_INTEGRATION_01`.

## 12_INVARIANTS

- doc-only ;
- aucun runtime ;
- aucune CI ;
- aucun index global ;
- aucune modification validator ;
- aucun connecteur live ;
- aucune mutation de LocalCMS, TMUX, OpenClaw ou des journals.

## 17_RESUME_POINT

```text
sot/mainline
-> GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_SURFACES_INVENTORY_01
-> GO_OPT_TRADING_DOC_OPS_WHY_LOCALCMS_TMUX_GRAPH_INTEGRATION_01
-> GO_OPT_TRADING_DOC_OPS_WHY_DAILY_JOURNAL_GRAPH_EXPORT_MAPPING_01
-> GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01
```

## 18_VERDICT

```text
WIP / DOC_ONLY_SURFACES_INVENTORY_OPENED
```
