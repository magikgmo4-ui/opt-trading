# 40_VALIDATION_GATES

## 1_MASTER_TARGET

Definir les gates de validation du refinement de lisibilite.

## WHY

Un refinement peut facilement glisser vers enrichissement JSON, nouveau render graphique ou dashboard. Les gates doivent verifier que l'amelioration reste presentationnelle et bornee.

## 7_CANONICAL_STATE

Gates retenus :

| Gate | Etat attendu | Motif |
| --- | --- | --- |
| PR #507 mergee | REQUIRED | la decision de refinement doit etre upstream |
| source JSON parseable | REQUIRED | source unique lisible |
| source render v0 presente | REQUIRED | refinement base sur le rendu existant |
| meme nombre de nodes | REQUIRED | pas d'enrichissement graph |
| meme nombre d'edges | REQUIRED | pas d'enrichissement graph |
| labels courts documentes | REQUIRED | lisibilite sans perte de provenance |
| provenance par node/edge | REQUIRED | review humaine conservee |
| Markdown statique | REQUIRED | pas de dashboard |
| runtime live | BLOCKED | aucune interrogation live |
| runtime mutation | BLOCKED | aucune action runtime |
| CI/validator/index global | BLOCKED | hors scope |

## 8_PASS_CRITERIA

Le refinement pourra etre accepte si :

- `python -m json.tool` passe sur le JSON source ;
- le rendu v1 declare le JSON comme source unique ;
- les labels courts sont relies aux relations JSON originales ;
- les nodes et edges restent strictement ceux du JSON ;
- `git diff --check` passe sur le dossier du GO ;
- `git diff --name-only` reste limite au dossier du GO.

## 9_FAIL_CRITERIA

Le refinement doit etre refuse si :

- il ajoute une source live ;
- il modifie le JSON ;
- il ajoute un node ou edge par inference ;
- il cree un dashboard ;
- il lance un service ou un runtime ;
- il modifie CI, validator ou index global.

## 10_CHECK_SKETCH

```text
python -m json.tool docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01/artifacts/why-runtime-graph-export.real.v0.json
git diff --name-only -- docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_RENDER_READABILITY_REFINEMENT_01
git diff --check -- docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_RENDER_READABILITY_REFINEMENT_01
git status --short --branch
```

## 12_INVARIANTS

- `readability refinement != dashboard`.
- `readability refinement != runtime live`.
- `readability refinement != mutation runtime`.
- `readability refinement != JSON rewrite`.
- `readability refinement = presentation improvement from validated JSON`.

## 17_RESUME_POINT

Le GO est pret pour un artefact v1 seulement si le refinement reste Markdown statique et source-locked sur le JSON valide.

## 18_VERDICT

```text
WIP / READABILITY_REFINEMENT_GATES_LOCKED / JSON_SOURCE_ONLY
```
