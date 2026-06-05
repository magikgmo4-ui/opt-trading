# 10_LOCALCMS_GRAPH_SURFACE_ROLE

## 1_MASTER_TARGET

Definir `LocalCMS` comme premiere surface graphique et documentaire read-only a raccorder au WHY runtime graph.

## WHY

Le futur graph ne doit pas partir d'un export technique abstrait. Il doit d'abord expliciter le consumer humain qui lira, synthetisera et presentera les surfaces runtime sans les piloter.

## 7_CANONICAL_STATE

Role retenu pour `LocalCMS` :

| Dimension | Position retenue |
| --- | --- |
| Nature | consumer UI read-only |
| Fonction graph | surface de lecture, de synthese et de navigation |
| Relation canonique | `READS_OR_SUMMARIZES` des vues runtime et artefacts lies |
| Frontiere | ne devient ni orchestrateur runtime ni source de verite primaire |
| Ownership documentaire | `LocalCMS runtime docs` + `doc ops graph consumers` |

Indices documentaires deja etablis :

- `LocalCMS` reste un sujet projet/UI ;
- `db-layer` reste la machine d'execution reelle documentee pour des surfaces `LocalCMS` ;
- des vues read-only, menus/domaines et traces de lecture sont les preuves attendues ;
- `LocalCMS` doit rester distinct d'un connecteur live ou d'un panneau de pilotage runtime.

## 8_EXPECTED_PROOFS

- vues read-only documentees ;
- menus, domaines ou modules relies a des surfaces runtime ;
- captures, indexations ou traces de lecture ;
- alignement explicite avec les surfaces `TMUX` observees ;
- review humaine si ambiguite entre lecture et orchestration.

## 12_INVARIANTS

- `LocalCMS` reste read-only dans ce GO.
- `LocalCMS` ne devient pas une source runtime primaire.
- `LocalCMS` ne remplace ni journal, ni artefact d'observabilite, ni review humaine.

## 17_RESUME_POINT

Le modele `LocalCMS` pose ici devra etre relie dans le fichier de linkage aux sessions `TMUX` et a leurs preuves observables, sans introduire de connecteur actif.

## RISKS

- À qualifier.
