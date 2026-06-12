# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Ouvrir `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01` pour produire le premier export JSON reel du WHY runtime graph a partir des surfaces documentees et du mapping Daily Journal valide.

## WHY

`PR #498` a merge `GO_OPT_TRADING_DOC_OPS_WHY_DAILY_JOURNAL_GRAPH_EXPORT_MAPPING_01` et ferme la derniere etape de mapping documentaire qui bloquait un export reel.

Le prochain pas canonique n'est pas un render graphique mais un artefact JSON borne, inspectable, reproductible et strictement read-only, afin de prouver que les surfaces centrales peuvent etre exportees sans mutation runtime ni court-circuit des gates humaines.

## 3_INITIAL_NEED

Ce GO doit clarifier :

- quelles surfaces documentees deviennent sources du premier export reel ;
- quel schema JSON minimal suffit pour prouver `nodes`, `edges` et metadonnees de contexte ;
- quelle commande read-only executer pour produire un artefact versionnable ;
- quels gates de validation bloquent encore tout render graphique.

## 5_GO_SCOPE

Ce GO couvre uniquement :

- le premier perimetre source du WHY runtime graph exportable en JSON ;
- le schema JSON minimal du premier export reel ;
- le plan de commande read-only pour produire l'artefact ;
- les gates de validation avant tout render futur.

Ce GO ne couvre pas :

- un render graphique reel ;
- une mutation runtime ;
- un connecteur live ;
- des changements `CI`, validator ou index globaux ;
- une generalisation large a toutes les surfaces runtime du repo.

## 6_FINAL_TARGET

Produire le premier export JSON reel du WHY runtime graph sous forme d'artefact borne, inspectable et auditable, ou formaliser son plan d'execution si l'etat local du repo bloque encore l'execution propre sur la base mergee.

## 7_CANONICAL_STATE

Etat etabli a l'ouverture :

- `PR #498` est `MERGED` ;
- `GO_OPT_TRADING_DOC_OPS_WHY_DAILY_JOURNAL_GRAPH_EXPORT_MAPPING_01` est `CLOSED_BY_MERGE` ;
- `origin/sot/mainline` contient ce merge ;
- la sequence reste `documentation -> mapping -> JSON export -> render futur` ;
- aucun render graphique ne doit preceder la validation du premier export JSON reel ;
- l'etat local courant ne peut pas encore fast-forward proprement sans traiter des fichiers non suivis qui chevauchent maintenant des fichiers suivis upstream.

## 8_VALIDATED_PLAN

1. Figer les surfaces sources minimales du premier export reel.
2. Reduire le schema JSON au plus petit artefact prouvant la spine `nodes + edges + provenance`.
3. Definir la commande read-only d'export et ses preconditions.
4. Verrouiller les gates qui interdisent encore tout render graphique.

## 12_INVARIANTS

- `READ_ONLY_FIRST` ;
- `EXPORT_ONLY_FIRST` ;
- `NO_RENDER_FIRST` ;
- `NO_RUNTIME_MUTATION` ;
- aucun index global ;
- aucune CI automatique ;
- aucun validator modifie sans justification explicite.

## 17_RESUME_POINT

```text
BASE:
origin/sot/mainline apres merge de PR #498

CURRENT_GO:
GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01

NEXT_ONLY_AFTER_JSON_VALIDATION:
render graphique futur
```

## 18_VERDICT

```text
WIP / REAL_JSON_EXPORT_GO_OPENED
```

## RISKS

- À qualifier.
