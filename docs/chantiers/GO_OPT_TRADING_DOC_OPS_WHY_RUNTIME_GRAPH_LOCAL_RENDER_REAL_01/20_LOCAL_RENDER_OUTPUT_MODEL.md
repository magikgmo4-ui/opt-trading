# 20_LOCAL_RENDER_OUTPUT_MODEL

## 1_MASTER_TARGET

Definir le modele de sortie minimal du premier rendu local reel du WHY runtime graph.

## WHY

Le rendu doit etre lisible par review humaine et stable en diff, sans devenir une application, une vue interactive permanente ou un dashboard operationnel.

## 7_CANONICAL_STATE

Sorties recommandees pour le prochain passage executable :

| Sortie | Role | Statut |
| --- | --- | --- |
| `artifacts/why-runtime-graph.local-render.real.v0.svg` | rendu visuel statique inspectable | REQUIRED |
| `artifacts/why-runtime-graph.local-render.real.v0.dot` | representation texte reproductible | RECOMMENDED |
| `artifacts/why-runtime-graph.local-render.real.v0.report.md` | preuve de source, commande et gates | REQUIRED |

## 8_RENDER_CONTENT

Le premier rendu doit exposer :

- 3 nodes source JSON : `LocalCMS`, `TMUX`, `Daily Journal` ;
- 3 edges source JSON : lecture LocalCMS/TMUX, mapping Daily Journal/TMUX, reference Daily Journal/LocalCMS ;
- labels lisibles issus de `nodes[].label` et `edges[].relation` ;
- provenance courte renvoyant vers l'artefact JSON source et le rapport.

## 9_VISUAL_LIMITS

Le rendu ne doit pas inclure :

- layout dashboard multi-panneaux ;
- controles interactifs ;
- refresh automatique ;
- donnees live ;
- overlays non presents dans le JSON ;
- scoring, criticite R0-R5 ou warning layers ajoutes par inference.

## 10_REVIEW_MODEL

La review humaine doit pouvoir verifier :

- que chaque node rendu correspond a une entree `nodes[]` ;
- que chaque edge rendu correspond a une entree `edges[]` ;
- que le fichier source JSON est cite ;
- que la commande de generation est reproductible localement ;
- que l'artefact reste borne au dossier du GO.

## 12_INVARIANTS

- Le SVG est un artefact statique.
- Le DOT, si produit, est un support de reproductibilite.
- Le rapport reste la preuve humaine de controle.
- Aucune sortie ne devient une source runtime ou un index global.

## 17_RESUME_POINT

Le rendu local attendu est un artefact graphique statique accompagne d'un support texte reproductible et d'un rapport court.
