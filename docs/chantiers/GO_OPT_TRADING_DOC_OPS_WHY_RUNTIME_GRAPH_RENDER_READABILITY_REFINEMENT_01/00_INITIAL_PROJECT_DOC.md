# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Ouvrir `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_RENDER_READABILITY_REFINEMENT_01` pour raffiner la lisibilite du rendu Markdown local existant du WHY runtime graph.

## WHY

`PR #507` a merge `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_RENDER_REVIEW_AND_NEXT_SURFACES_01` et documente que le prochain mouvement canonique est un refinement de lisibilite, pas un dashboard ni une extension runtime.

Le rendu v0 est valide comme premiere preuve locale, mais il reste difficile a lire : labels longs, absence de legende, provenance trop globale et orientation des edges peu explicitee.

## 3_INITIAL_NEED

Ce GO doit clarifier :

- quels findings de lisibilite viennent du rendu v0 ;
- quelle structure Markdown v1 corrige les problemes sans changer de source ;
- comment rendre les nodes, edges et provenances plus lisibles ;
- quels gates bloquent toujours dashboard, runtime live, mutation et refonte JSON large.

## 5_GO_SCOPE

Ce GO couvre uniquement :

- refinement du rendu Markdown existant ;
- conservation du JSON valide comme source unique ;
- labels courts et tables de correspondance ;
- legende explicite pour node types et edge types ;
- separation claire entre graph, gaps et next surfaces.

Ce GO ne couvre pas :

- dashboard ;
- runtime live ;
- mutation runtime ;
- enrichissement JSON large ;
- changements `CI`, validator ou index globaux ;
- integration LocalCMS live ;
- traversal ou navigation autonome.

## 6_FINAL_TARGET

Produire un cadrage de refinement lisible du rendu local existant, pret a alimenter un artefact Markdown v1 borne depuis le meme JSON valide.

## 7_CANONICAL_STATE

Etat etabli a l'ouverture :

- `PR #507` est `MERGED` ;
- `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_RENDER_REVIEW_AND_NEXT_SURFACES_01` est `CLOSED_BY_MERGE` ;
- la decision active est `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_RENDER_READABILITY_REFINEMENT_01` ;
- la source render v0 reste `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_RENDER_REAL_01/artifacts/why-runtime-graph.local-render.v0.md` ;
- la source JSON reste `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01/artifacts/why-runtime-graph-export.real.v0.json`.

## 8_VALIDATED_PLAN

1. Reprendre les findings de review du rendu v0.
2. Definir une structure Markdown v1 plus lisible.
3. Conserver les 3 nodes et 3 edges du JSON valide.
4. Ajouter labels courts, legende, provenance par node/edge et section gaps.
5. Garder dashboard, runtime live, CI, validator et index globaux hors scope.

## 12_INVARIANTS

- `READABILITY_REFINEMENT_ONLY` ;
- `NO_DASHBOARD` ;
- `NO_RUNTIME_LIVE` ;
- `NO_RUNTIME_MUTATION` ;
- `NO_JSON_REWRITE` ;
- aucun index global ;
- aucune CI automatique ;
- aucun validator modifie.

## 17_RESUME_POINT

```text
BASE:
origin/sot/mainline apres merge de PR #507

CURRENT_GO:
GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_RENDER_READABILITY_REFINEMENT_01

SOURCE_RENDER_V0:
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_RENDER_REAL_01/artifacts/why-runtime-graph.local-render.v0.md

TARGET:
refinement Markdown lisible depuis le meme JSON valide
```

## 18_VERDICT

```text
WIP / READABILITY_REFINEMENT_GO_OPENED / NO_DASHBOARD
```
