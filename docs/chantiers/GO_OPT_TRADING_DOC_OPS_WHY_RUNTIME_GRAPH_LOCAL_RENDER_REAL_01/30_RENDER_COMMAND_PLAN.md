# 30_RENDER_COMMAND_PLAN

## 1_MASTER_TARGET

Definir un plan de commande read-only pour produire le premier rendu local reel depuis le JSON valide.

## WHY

Le repo doit pouvoir reproduire le rendu sans mutation runtime, sans CI, sans validator et sans dependance a un service live. Le plan doit rester assez simple pour etre execute et audite manuellement dans le prochain passage.

## 7_CANONICAL_STATE

Preconditions attendues :

- branche dediee `go/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_RENDER_REAL_01` ;
- base `origin/sot/mainline` apres merge de `PR #502` ;
- source JSON presente upstream ;
- dossier chantier local disponible ;
- aucun changement hors dossier du GO.

## 8_COMMAND_PLAN

Plan minimal recommande :

1. Lire `why-runtime-graph-export.real.v0.json`.
2. Verifier la syntaxe JSON avec `python -m json.tool`.
3. Extraire uniquement `nodes[]` et `edges[]`.
4. Generer un fichier DOT local dans le dossier `artifacts/`.
5. Generer un SVG local depuis ce DOT si l'outil disponible le permet.
6. Generer un rapport Markdown listant source, commande, nodes, edges et limites.
7. Executer `git diff --check` sur le dossier du GO.

## 9_ACCEPTED_IMPLEMENTATION_BOUNDARY

Implementation acceptable au prochain passage :

- script local au dossier du GO, si necessaire ;
- lecture du JSON source valide uniquement ;
- ecriture d'artefacts uniquement sous le dossier du GO ;
- absence de render serveur ou dashboard ;
- absence de modification runtime, CI, validator ou index global.

## 10_FALLBACK

Si aucun moteur DOT/SVG local n'est disponible, le fallback acceptable est :

- produire le DOT et le rapport ;
- documenter explicitement que le SVG est bloque par dependance locale manquante ;
- ne pas installer ou modifier de tooling global sans decision explicite.

## 11_CHECK_SKETCH

```text
python -m json.tool docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01/artifacts/why-runtime-graph-export.real.v0.json
git diff --name-only -- docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_RENDER_REAL_01
git diff --check -- docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_RENDER_REAL_01
git status --short --branch
```

## 12_INVARIANTS

- Pas de `git clean`.
- Pas de switch force.
- Pas de mutation runtime.
- Pas de lancement de service.
- Pas de CI automatique.
- Pas de validator modifie.
- Pas d'index global.

## 17_RESUME_POINT

Le prochain passage executable peut produire un DOT/SVG statique depuis le JSON valide, avec ecriture limitee au dossier du GO.

## RISKS

- À qualifier.
