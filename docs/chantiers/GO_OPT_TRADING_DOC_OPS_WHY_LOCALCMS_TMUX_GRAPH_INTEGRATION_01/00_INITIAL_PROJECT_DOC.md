# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Ouvrir `GO_OPT_TRADING_DOC_OPS_WHY_LOCALCMS_TMUX_GRAPH_INTEGRATION_01` pour documenter comment `LocalCMS` et `TMUX` deviennent les premieres surfaces lisibles, observables et raccordables au WHY runtime graph.

## WHY

Le GO `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_SURFACES_INVENTORY_01`, publie via `PR #485`, a verrouille `LocalCMS` et `TMUX` comme premieres surfaces structurantes a integrer avant tout mapping daily journal ou export JSON reel.

Le besoin n'est plus d'inventorier les familles de surfaces, mais d'expliquer comment un consumer read-only (`LocalCMS`) se raccorde a une spine runtime/session (`TMUX`) dans un modele graph coherent, observable et strictement doc-only.

## 3_INITIAL_NEED

Ce chantier doit clarifier :

- le role de `LocalCMS` comme surface documentaire et graphique read-only ;
- le role de `TMUX` comme surface runtime/session canonique ;
- le modele de liaison `LocalCMS -> TMUX -> WHY graph` ;
- les preuves attendues pour rendre ces relations auditable ;
- la readiness de cette integration avant le prochain GO de mapping journal.

## 5_GO_SCOPE

Ce GO couvre uniquement :

- la definition documentaire du role graph de `LocalCMS` ;
- la definition documentaire du role graph de `TMUX` ;
- leur modele de liaison canonique ;
- l'etat de preparation de cette integration pour la suite du runtime graph.

Ce GO ne couvre pas :

- un render graph reel ;
- un export JSON reel ;
- un connecteur live `LocalCMS` ;
- des commandes `TMUX` runtime ;
- la modification d'un validator, d'une CI ou d'un index global.

## 7_CANONICAL_STATE

Etat etabli a l'ouverture :

- `PR #485` est `MERGED` ;
- merge commit `PR #485` : `ceeacd909deeca22091fa743a038bd7af1db8e01` ;
- `origin/sot/mainline` contient ce merge ;
- le GO inventory precedent est considere clos et ne doit pas etre rouvert sans finding explicite ;
- `TMUX runtime` et `LocalCMS` etaient tous deux `READY_FOR_INTEGRATION` dans l'inventory ;
- `LocalCMS` est retenu comme consumer read-only ;
- `TMUX` est retenu comme spine runtime/session centrale.

## 8_VALIDATED_PLAN

1. Decrire `LocalCMS` comme surface graph read-only.
2. Decrire `TMUX` comme surface runtime/session observable.
3. Formaliser le lien canonique entre `LocalCMS`, `TMUX` et le WHY graph.
4. Definir les preuves et gates minimaux de cette integration.
5. Publier un resume point vers `GO_OPT_TRADING_DOC_OPS_WHY_DAILY_JOURNAL_GRAPH_EXPORT_MAPPING_01` comme prochaine etape avant le premier render graph reel local.

## 12_INVARIANTS

- doc-only ;
- aucun index global ;
- aucun runtime ;
- aucun validator ;
- aucune CI ;
- aucun connecteur live ;
- aucune mutation `LocalCMS` ou `TMUX`.

## 17_RESUME_POINT

```text
BASE:
origin/sot/mainline apres merge de PR #485

CURRENT_GO:
GO_OPT_TRADING_DOC_OPS_WHY_LOCALCMS_TMUX_GRAPH_INTEGRATION_01

THEN:
GO_OPT_TRADING_DOC_OPS_WHY_DAILY_JOURNAL_GRAPH_EXPORT_MAPPING_01
GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01
```

## 18_VERDICT

```text
WIP / DOC_ONLY_LOCALCMS_TMUX_GRAPH_INTEGRATION_OPENED
```

## RISKS

- À qualifier.
