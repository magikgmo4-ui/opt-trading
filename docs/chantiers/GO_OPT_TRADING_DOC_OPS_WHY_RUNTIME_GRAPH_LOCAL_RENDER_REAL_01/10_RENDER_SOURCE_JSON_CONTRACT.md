# 10_RENDER_SOURCE_JSON_CONTRACT

## 1_MASTER_TARGET

Definir le contrat de source JSON unique du premier rendu local reel du WHY runtime graph.

## WHY

Le rendu local ne doit pas reinterpreter le repo entier. Il doit prouver qu'un artefact graphique borne peut etre produit depuis le JSON valide, sans aller rechercher des donnees runtime live ni des surfaces documentaires non incluses dans l'export.

## 7_CANONICAL_STATE

Source unique autorisee :

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01/artifacts/why-runtime-graph-export.real.v0.json
```

Champs d'entree requis :

| Champ | Usage render local |
| --- | --- |
| `graph_id` | identifiant du graph rendu |
| `generated_at` | contexte temporel de l'export source |
| `go_id` | rattachement au GO source |
| `export_id` | identifiant d'artefact source |
| `scope` | borne explicite du rendu |
| `sources` | provenance documentaire affichee ou reportee |
| `nodes` | noeuds a rendre |
| `edges` | relations a rendre |
| `validation_gates` | rappel des gates de securite documentaire |
| `export_notes` | notes d'invariant reprises dans le rapport |

## 8_ACCEPTED_SOURCE_SCOPE

Le premier rendu local accepte uniquement :

- `surface:localcms` ;
- `surface:tmux` ;
- `surface:daily_journal` ;
- les edges deja presents dans `edges[]` ;
- la provenance deja presente dans `sources[]`, `nodes[].provenance[]` et `edges[].provenance[]`.

## 9_REJECTED_SOURCE_EXPANSION

Le rendu local ne doit pas charger :

- les markdown source amont comme nouvelle base d'extraction ;
- des snapshots runtime live ;
- des logs ou sessions `TMUX` live ;
- des vues `LocalCMS` live ;
- des overlays security ou warnings non presents dans le JSON ;
- des indexes globaux.

## 12_INVARIANTS

- Le JSON valide est la seule source de graph.
- Un noeud rendu doit exister dans `nodes[]`.
- Une edge rendue doit exister dans `edges[]`.
- La provenance doit rester visible dans le rapport ou dans les attributs du rendu.
- `render_graphic: false` dans le JSON source signifie que le JSON n'etait pas lui-meme un render ; ce GO est le consumer local posterieur autorise.

## 17_RESUME_POINT

Le premier render local part d'un JSON deja valide et ne reconstruit pas le graph depuis le repo.
