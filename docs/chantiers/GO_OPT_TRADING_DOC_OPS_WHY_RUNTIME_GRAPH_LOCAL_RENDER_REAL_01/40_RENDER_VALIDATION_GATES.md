# 40_RENDER_VALIDATION_GATES

## 1_MASTER_TARGET

Definir les gates minimaux qui valident le premier rendu local reel du WHY runtime graph.

## WHY

Un rendu graphique peut donner une impression de completion superieure au niveau reel de preuve. Les gates doivent donc confirmer que le rendu reste borne, issu du JSON valide et strictement read-only.

## 7_CANONICAL_STATE

Gates retenus :

| Gate | Etat attendu | Motif |
| --- | --- | --- |
| base `PR #502` mergee | REQUIRED | le rendu doit partir du JSON valide upstream |
| source JSON unique | REQUIRED | pas de nouvelle extraction large |
| JSON parseable | REQUIRED | input lisible avant render |
| nodes bornes | REQUIRED | uniquement les nodes de `nodes[]` |
| edges bornees | REQUIRED | uniquement les edges de `edges[]` |
| sortie statique | REQUIRED | pas de dashboard live |
| reproductibilite locale | REQUIRED | commande et artefacts reviewables |
| scope dossier GO | REQUIRED | aucune ecriture hors chantier |
| runtime mutation | BLOCKED | le render ne pilote rien |
| CI/validator/index global | BLOCKED | hors scope sans decision explicite |

## 8_PASS_CRITERIA

Le rendu local pourra etre accepte si :

- l'artefact visuel est produit depuis le JSON valide ;
- chaque node et edge rendu est tracable vers le JSON ;
- le rapport liste la commande exacte et les limites ;
- `git diff --check` passe sur le dossier du GO ;
- `git diff --name-only` ne montre que le dossier du GO ;
- aucun service ou runtime live n'a ete lance.

## 9_FAIL_CRITERIA

Le rendu doit etre refuse si :

- il lit une source autre que le JSON valide ;
- il ajoute des nodes ou edges par inference ;
- il introduit un dashboard ou une boucle de refresh ;
- il modifie runtime, CI, validator ou index global ;
- il ecrit des artefacts hors dossier chantier ;
- il masque la provenance documentaire.

## 12_INVARIANTS

- `render local reel != dashboard complet`.
- `render local reel != runtime live`.
- `render local reel != mutation runtime`.
- `render local reel != CI/validator change`.
- `render local reel = visualisation statique bornee depuis JSON valide`.

## 17_RESUME_POINT

Le GO est pret pour un premier render local seulement si ces gates restent visibles et que la source JSON unique demeure verrouillee.

## 18_VERDICT

```text
WIP / LOCAL_RENDER_GATES_LOCKED / JSON_ONLY_SOURCE
```
