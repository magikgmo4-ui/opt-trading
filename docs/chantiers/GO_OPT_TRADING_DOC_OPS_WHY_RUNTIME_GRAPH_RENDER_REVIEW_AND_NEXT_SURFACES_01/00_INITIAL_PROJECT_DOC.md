# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Ouvrir `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_RENDER_REVIEW_AND_NEXT_SURFACES_01` pour reviewer le premier rendu local borne du WHY runtime graph et choisir la prochaine surface canonique.

## WHY

`PR #503` a merge `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_RENDER_REAL_01` et publie le premier rendu Markdown local depuis le JSON export reel valide.

Le prochain pas ne doit pas etre un dashboard ni une extension runtime. Le rendu doit d'abord etre relu comme artefact humain : lisibilite, structure, provenance, limites et gaps doivent etre documentes avant toute decision d'enrichissement JSON, integration LocalCMS, traversal ou prototype dashboard.

## 3_INITIAL_NEED

Ce GO doit clarifier :

- ce que le rendu local v0 prouve deja ;
- quels gaps de lecture restent visibles ;
- quelles surfaces candidates sont ouvertes ou bloquees ;
- quelle prochaine branche canonique doit etre privilegiee ;
- quels gates restent actifs avant toute extension.

## 5_GO_SCOPE

Ce GO couvre uniquement :

- review documentaire du rendu local v0 ;
- analyse des gaps de lisibilite et de structure ;
- comparaison des prochaines surfaces candidates ;
- decision de prochaine suite canonique.

Ce GO ne couvre pas :

- un nouveau render ;
- un dashboard complet ;
- une integration live `LocalCMS` ;
- un traversal autonome ;
- une mutation runtime ;
- des changements `CI`, validator ou index globaux ;
- un enrichissement JSON sans decision explicite.

## 6_FINAL_TARGET

Produire une review structuree du premier rendu local borne et choisir la prochaine action canonique sans sauter directement vers dashboard ou runtime live.

## 7_CANONICAL_STATE

Etat etabli a l'ouverture :

- `PR #503` est `MERGED` ;
- `origin/sot/mainline` contient `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_RENDER_REAL_01` ;
- le rendu local source est `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_RENDER_REAL_01/artifacts/why-runtime-graph.local-render.v0.md` ;
- le rapport source est `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_RENDER_REAL_01/artifacts/why-runtime-graph.local-render.v0.report.md` ;
- le JSON source reste `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01/artifacts/why-runtime-graph-export.real.v0.json`.

## 8_VALIDATED_PLAN

1. Reviewer le rendu v0 comme artefact humain.
2. Identifier les gaps de lisibilite et de structure.
3. Comparer les surfaces candidates suivantes.
4. Retenir le prochain GO canonique le moins risqué.
5. Maintenir dashboard, runtime live, CI, validator et index globaux hors scope.

## 12_INVARIANTS

- `REVIEW_ONLY` ;
- `NO_NEW_RENDER` ;
- `NO_DASHBOARD_FULL` ;
- `NO_RUNTIME_LIVE` ;
- `NO_RUNTIME_MUTATION` ;
- `NO_JSON_ENRICHMENT_WITHOUT_REVIEW_DECISION` ;
- aucun index global ;
- aucune CI automatique ;
- aucun validator modifie.

## 17_RESUME_POINT

```text
BASE:
origin/sot/mainline apres merge de PR #503

CURRENT_GO:
GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_RENDER_REVIEW_AND_NEXT_SURFACES_01

SOURCE_RENDER:
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_RENDER_REAL_01/artifacts/why-runtime-graph.local-render.v0.md

DECISION_TARGET:
choisir la prochaine surface canonique apres review du rendu v0
```

## 18_VERDICT

```text
WIP / RENDER_REVIEW_GO_OPENED / REVIEW_ONLY
```

## RISKS

- À qualifier.
