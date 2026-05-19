# 10_READABILITY_FINDINGS_FROM_V0

## 1_MASTER_TARGET

Extraire les findings de lisibilite du rendu Markdown v0.

## WHY

Le rendu v0 est correct et borne, mais son objectif etait de prouver la chaine `JSON valide -> Markdown local`. Le refinement doit maintenant ameliorer la comprehension humaine sans ajouter de donnees.

## 7_CANONICAL_STATE

Sources relues :

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_RENDER_REAL_01/artifacts/why-runtime-graph.local-render.v0.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_RENDER_REAL_01/artifacts/why-runtime-graph.local-render.v0.report.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_RENDER_REVIEW_AND_NEXT_SURFACES_01/20_READABILITY_GAPS.md
```

## 8_FINDINGS

| Finding | Source | Impact |
| --- | --- | --- |
| Labels edge trop longs | Mermaid v0 | les relations sont exactes mais peu scannables |
| Absence de legende | review #507 | les types `LocalCMS`, `TMUX`, `Daily Journal` ne sont pas expliques dans le graph |
| Provenance trop globale | review #507 | la table provenance existe, mais pas par node/edge |
| Orientation peu explicite | review #507 | le sens des fleches n'est pas decrit |
| Gaps non visibles dans l'artefact | review #507 | le rendu ne dit pas clairement ce qui bloque dashboard, JSON enrichment ou traversal |

## 9_CONFIRMED_STRENGTHS

Le rendu v0 doit conserver :

- source JSON unique ;
- 3 nodes ;
- 3 edges ;
- Markdown statique ;
- limites no-dashboard, no-runtime-live, no-mutation ;
- aucun enrichissement JSON.

## 10_REFINEMENT_NEEDS

Le rendu v1 devrait ajouter :

- aliases courts pour les nodes dans le graph ;
- labels courts pour les edges dans le graph ;
- table `label court -> relation JSON source` ;
- legende de type de node ;
- table de provenance par node et par edge ;
- section `Gaps and blocked next surfaces`.

## 12_INVARIANTS

- Corriger une limite de lecture ne justifie pas de modifier le JSON.
- Corriger une limite de lecture ne justifie pas de creer un dashboard.
- Corriger une limite de lecture ne justifie pas d'interroger un runtime live.

## 17_RESUME_POINT

Le refinement doit etre presentational, borne et compatible avec le JSON v0 existant.
