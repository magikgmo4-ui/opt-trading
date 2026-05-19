# 30_RUNTIME_SURFACE_RELATIONS

## 1_MASTER_TARGET

Cartographier les relations structurantes entre surfaces runtime, consumers, overlays et artefacts qui devront apparaitre dans le futur WHY/runtime graph.

## WHY

L'ordre post-OpenClaw est guide par les relations reelles entre spine runtime, consumers read-only, traces de runs et overlays warning-only, pas par une simple sequence documentaire.

## 7_CANONICAL_STATE

Relations structurantes retenues :

| Source | Relation | Cible | Justification canonique |
| --- | --- | --- | --- |
| TMUX runtime | HOSTS_OR_EXPOSES | runtime sessions | la spine TMUX devient surface runtime canonique |
| LocalCMS | READS_OR_SUMMARIZES | TMUX runtime views | LocalCMS est un consumer read-only pertinent pour le graph |
| Daily journals | RECORDS | runtime runs | les journals portent run ids, chronologie et snapshots |
| Observability artefacts | PROVES | runtime state | les artefacts servent de preuve, pas de source active |
| Security aggregators | OVERLAYS | OpenClaw runtime surfaces | l'agregateur apporte des warnings runtime/security |
| WHY lint | OVERLAYS | graph source docs | WHY lint reste un overlay documentaire warning-only |
| Validators | CHECKS | docs and schemas | les validators bornent la coherence statique |
| OpenClaw runtime | EMITS | JSON reports | la chaine warning-only produit des artefacts lisibles |

## 8_RELATION_RULES

- `OVERLAYS` doit rester distinct de `PROVES` et de `READS_OR_SUMMARIZES`.
- Une relation de preuve ne doit pas etre relue comme une relation de controle live.
- Une relation consumer/read-only ne doit pas etre requalifiee en orchestration runtime.
- Une relation `CHECKS` warning-only ne doit pas devenir gate bloquante dans ce GO.

## 12_INVARIANTS

- Aucun edge defini ici n'autorise une action runtime.
- Aucune relation n'implique un connecteur live.
- Aucune relation ne supprime le besoin de review humaine sur les surfaces critiques.

## 17_RESUME_POINT

Le futur GO de mapping daily journal devra raffiner les relations `RECORDS`, `PROVES` et `READS_OR_SUMMARIZES` avec les structures de run et de snapshot.
