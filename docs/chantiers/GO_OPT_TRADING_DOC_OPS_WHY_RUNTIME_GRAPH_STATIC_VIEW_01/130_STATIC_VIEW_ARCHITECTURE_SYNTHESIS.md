# 130_STATIC_VIEW_ARCHITECTURE_SYNTHESIS

## Objectif

Synthetiser l'architecture de la vue statique WHY/runtime.

## Synthese

Le chantier definit une vue statique locale WHY/runtime:
- lecture seule,
- non destructive,
- audit-oriented,
- multi-machine aware,
- sans runtime live,
- sans connecteurs live,
- sans traversal decisionnel,
- sans dashboard live.

## Architecture retenue

| Couche | Role |
| --- | --- |
| static view scope | definir le perimetre |
| static view inputs | definir les inputs autorises |
| renderer constraints | proteger runtime/governance |
| static view outputs | definir artefacts reviewables |
| overlays | contextualiser WHY/runtime |
| multi-machine context | contextualiser machines |
| observability alignment | relier preuves runtime |
| human review gates | conserver validation humaine |
| render pipeline | preparer rendu local |
| JSON export alignment | preparer export graph |
| governance snapshots | preparer snapshots runtime/governance |
| implementation gates | verrouiller passage reel |

## Resultat structurel

Le repo dispose maintenant d'une base documentaire complete pour preparer:
- premier render graph reel local,
- export JSON reel,
- dashboard prototype,
- traversal runtime reel,
- observabilite runtime multi-machine reelle,
- overlays dynamiques WHY/runtime,
- governance dashboard live futur.

## Note d'etat

Les fichiers `100_STATIC_VIEW_JSON_EXPORT_ALIGNMENT_V2.md`, `110_STATIC_VIEW_GOVERNANCE_SNAPSHOTS_V2.md` et `120_STATIC_VIEW_IMPLEMENTATION_GATES_V2.md` representent l'etat reel cree dans la branche apres comportement intermittent du connecteur GitHub sur les chemins initiaux.

## Invariant final

La vue statique WHY/runtime ne doit jamais devenir une orchestration runtime autonome ni remplacer une validation humaine critique.

## RISKS

- À qualifier.
