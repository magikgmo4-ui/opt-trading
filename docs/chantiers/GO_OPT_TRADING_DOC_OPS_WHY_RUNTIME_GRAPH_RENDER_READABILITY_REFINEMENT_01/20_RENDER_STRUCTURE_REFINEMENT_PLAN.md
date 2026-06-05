# 20_RENDER_STRUCTURE_REFINEMENT_PLAN

## 1_MASTER_TARGET

Definir le plan de structure du rendu Markdown v1.

## WHY

La lisibilite doit venir d'une meilleure organisation du Markdown, pas d'une extension de donnees. La structure v1 doit aider un lecteur a comprendre la source, les nodes, les edges, les gaps et les next surfaces dans cet ordre.

## 7_CANONICAL_STATE

Structure v1 recommandee :

| Section | Role |
| --- | --- |
| Source Lock | rappelle le JSON source unique |
| Graph Summary | resume 3 nodes, 3 edges, no-dashboard |
| Readable Graph | Mermaid avec labels courts |
| Node Legend | explique les types de nodes |
| Edge Legend | mappe labels courts vers relations JSON |
| Provenance Map | rattache provenance par node et edge |
| Readability Gaps | montre ce qui a ete corrige ou reste ouvert |
| Next Surfaces | rappelle blocked/deferred/next |
| Limits | bloque dashboard, runtime live, mutation et CI |

## 8_EDGE_LABEL_PLAN

| Edge JSON | Label court v1 | Motif |
| --- | --- | --- |
| `localcms_view_reads_or_summarizes_tmux_session` | `reads session` | relation lisible sans perdre le sens |
| `run_id_references_tmux_session` | `anchors run` | met l'accent sur l'ancrage `run_id` |
| `journal_reference_points_to_localcms_read_only_view` | `references view` | met l'accent sur la vue read-only |

## 9_NODE_HIERARCHY_PLAN

| Node | Role court v1 | Position logique |
| --- | --- | --- |
| `surface:daily_journal` | run context source | entree temporelle et preuve |
| `surface:localcms` | read-only view | consumer documentaire |
| `surface:tmux` | runtime session spine | surface runtime observee |

## 10_SCOPE_BOUNDARY

Le plan ne change pas :

- IDs JSON ;
- relations JSON ;
- source JSON ;
- nombre de nodes ;
- nombre d'edges ;
- provenance source ;
- gates no-runtime/no-dashboard.

## 12_INVARIANTS

- La structure v1 reste Markdown.
- Le graph v1 reste statique.
- Le JSON reste source de verite.
- Les labels courts sont des aliases de lecture, pas de nouvelles relations.

## 17_RESUME_POINT

Le refinement doit rendre le meme graph plus lisible, pas produire un graph plus riche.

## RISKS

- À qualifier.
