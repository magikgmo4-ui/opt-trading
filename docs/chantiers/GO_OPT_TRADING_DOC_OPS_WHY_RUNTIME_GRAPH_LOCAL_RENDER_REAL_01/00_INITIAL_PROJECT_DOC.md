# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Ouvrir `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_RENDER_REAL_01` pour cadrer le premier rendu local reel du WHY runtime graph a partir du JSON export reel valide.

## WHY

`PR #502` a merge `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01` et publie le premier artefact JSON reel borne du WHY runtime graph.

Le verrou `pas de render avant export JSON reel` est donc leve, mais seulement pour un rendu local, inspectable et reproductible depuis cet artefact valide. Le prochain pas canonique n'est pas un dashboard, ni un runtime live, ni une orchestration graphique autonome.

## 3_INITIAL_NEED

Ce GO doit clarifier :

- le contrat de source JSON unique ;
- le format de sortie minimal du premier rendu local ;
- les limites du graph rendu ;
- le plan de commande read-only ;
- les gates de validation avant toute extension future.

## 5_GO_SCOPE

Ce GO couvre uniquement :

- le premier cadrage de rendu local depuis `why-runtime-graph-export.real.v0.json` ;
- le modele de sortie statique attendu ;
- la reproductibilite manuelle du rendu ;
- les controles qui empechent un glissement vers dashboard ou runtime live.

Ce GO ne couvre pas :

- un dashboard complet ;
- un connecteur live ;
- une mutation runtime ;
- des changements `CI`, validator ou index globaux ;
- une extension automatique aux overlays security, warnings ou gouvernance globale ;
- une decision graph traversal autonome.

## 6_FINAL_TARGET

Produire le cadrage initial du premier rendu local reel du WHY runtime graph depuis le JSON valide, avec un perimetre suffisamment borne pour rendre le prochain artefact graphique reviewable sans introduire de tooling large.

## 7_CANONICAL_STATE

Etat etabli a l'ouverture :

- `PR #502` est `MERGED` ;
- `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01` est `CLOSED_BY_MERGE` ;
- `origin/sot/mainline` contient l'artefact JSON reel valide ;
- la source autorisee du rendu est `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01/artifacts/why-runtime-graph-export.real.v0.json` ;
- le rendu local doit rester un consumer statique du JSON, pas une nouvelle source de verite.

## 8_VALIDATED_PLAN

1. Verrouiller le contrat d'entree sur le JSON valide.
2. Definir le modele de sortie local minimal.
3. Decrire une commande reproductible sans runtime live.
4. Fixer les gates qui bloquent dashboard, mutation et changements globaux.

## 12_INVARIANTS

- `LOCAL_RENDER_ONLY` ;
- `JSON_VALIDATED_SOURCE_ONLY` ;
- `NO_DASHBOARD_FULL` ;
- `NO_RUNTIME_LIVE` ;
- `NO_RUNTIME_MUTATION` ;
- aucun index global ;
- aucune CI automatique ;
- aucun validator modifie sans decision explicite.

## 17_RESUME_POINT

```text
BASE:
origin/sot/mainline apres merge de PR #502

CURRENT_GO:
GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_RENDER_REAL_01

SOURCE_JSON:
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01/artifacts/why-runtime-graph-export.real.v0.json

NEXT:
premier artefact de rendu local borne depuis JSON valide
```

## 18_VERDICT

```text
WIP / LOCAL_RENDER_REAL_GO_OPENED / JSON_SOURCE_LOCKED
```

## RISKS

- À qualifier.
