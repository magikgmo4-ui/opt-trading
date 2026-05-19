# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Ouvrir `GO_OPT_TRADING_DOC_OPS_WHY_DAILY_JOURNAL_GRAPH_EXPORT_MAPPING_01` pour mapper le Daily Journal vers le futur WHY graph export avant toute generation reelle.

## WHY

Le merge de `PR #492` a ferme l'etape d'integration documentaire `LocalCMS + TMUX` comme surfaces centrales du graph.

La derniere etape documentaire avant un export ou un render reel est maintenant de raccorder les `run_id`, snapshots, chronologies et preuves de journal a ce modele central, sans court-circuiter les gates humains ni transformer le journal en runtime actif.

## 3_INITIAL_NEED

Ce GO doit clarifier :

- le role du Daily Journal comme source de contexte temporel et de run ;
- le mapping `run_id` vers sessions `TMUX`, vues `LocalCMS` et surfaces runtime ;
- la place des snapshots et artefacts de preuve dans le modele graph ;
- les regles minimales avant tout export graph reel.

## 5_GO_SCOPE

Ce GO couvre uniquement :

- le modele documentaire du Daily Journal dans le WHY graph ;
- le mapping des `run_id`, snapshots et chronologies ;
- les prerequis de readiness avant `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01`.

Ce GO ne couvre pas :

- un render graph reel ;
- un export JSON reel ;
- un connecteur live journal ;
- des changements `LocalCMS`, `TMUX`, runtime, validator, CI ou index globaux.

## 7_CANONICAL_STATE

Etat etabli a l'ouverture :

- `PR #492` est `MERGED` ;
- merge commit `PR #492` : `7bbbe891174069ee78769fe7dc3ce57dd8f57773` ;
- `origin/sot/mainline` contient ce merge ;
- l'ordre verrouille reste `LocalCMS/TMUX -> Daily Journal mapping -> graph export real` ;
- le GO precedent a explicitement interdit tout render/export reel avant ce mapping ;
- l'inventory post-OpenClaw avait deja etabli `Daily journals` comme `READY_FOR_MAPPING`.

## 8_VALIDATED_PLAN

1. Definir le role graph du Daily Journal.
2. Mapper `run_id` et chronologies vers les surfaces centrales deja posees.
3. Relier snapshots et artefacts aux noeuds et edges du graph.
4. Publier les gates de readiness avant export reel.

## 12_INVARIANTS

- doc-only ;
- aucun index global ;
- aucun runtime ;
- aucun validator ;
- aucune CI ;
- aucun connecteur live ;
- aucun render/export graph reel.

## 17_RESUME_POINT

```text
BASE:
origin/sot/mainline apres merge de PR #492

CURRENT_GO:
GO_OPT_TRADING_DOC_OPS_WHY_DAILY_JOURNAL_GRAPH_EXPORT_MAPPING_01

THEN:
GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01
```

## 18_VERDICT

```text
WIP / DOC_ONLY_DAILY_JOURNAL_GRAPH_MAPPING_OPENED
```
