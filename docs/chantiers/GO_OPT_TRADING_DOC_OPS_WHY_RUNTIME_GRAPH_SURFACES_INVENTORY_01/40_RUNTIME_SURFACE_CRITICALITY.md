# 40_RUNTIME_SURFACE_CRITICALITY

## 1_MASTER_TARGET

Evaluer la criticite `R0-R5` des surfaces runtime inventoriees et expliciter les preuves runtime minimales attendues pour chacune.

## WHY

Le futur graph doit pouvoir exprimer la difference entre une surface documentaire, un consumer read-only, une spine runtime critique et un overlay warning-only sans surclasser artificiellement des artefacts de preuve.

## 7_CANONICAL_STATE

Cadre de criticite de travail :

| Surface family | Classe de criticite initiale | Preuves runtime minimales | Review humaine |
| --- | --- | --- | --- |
| TMUX runtime spine | R4/R5 candidate | sessions documentees, placement machine, semantics de restart, traces de run | obligatoire |
| LocalCMS runtime views | R2/R3 candidate | vues read-only documentees, menus/domaines, alignement avec surfaces observees | obligatoire avant integration graph |
| Daily journals | R2/R3 candidate | run ids, chronologie, snapshots, references de preuve | obligatoire sur run de reference |
| OpenClaw runtime security chain | R2/R3 candidate | workflow warning-only, artifact JSON, review d'artefact | obligatoire |
| Validators | R1/R2 candidate | spec, tests ou scans cites, bornes de perimetre | obligatoire si extension |
| WHY lint overlay | R1 candidate | scans, zero-finding ou finding borne, warning model | obligatoire si nouvelle famille warning |
| Security aggregators | R2/R3 candidate | rapport agrege, lineage d'artefact, statut warning-only | obligatoire |
| Observability artefacts | R0/R1 candidate | existence, provenance, fraicheur, lien de surface | obligatoire si preuve unique |

## 8_CRITICALITY_RULES

- Une preuve seule ne depasse pas `R1` si elle n'est rattachee a aucune surface runtime critique.
- Une spine runtime peut etre `R4/R5` meme si ses consumers read-only restent `R2/R3`.
- Les overlays warning-only ne doivent pas etre promus au-dessus des surfaces qu'ils observent sans triage explicite.
- Les classes `R0-R5` definies ici restent des candidats d'inventaire, pas une taxonomie d'execution finale.

## 12_INVARIANTS

- Aucune classe `R0-R5` n'autorise un runtime live.
- Aucune classe `R0-R5` n'autorise une escalation automatique.
- Aucune classe `R0-R5` n'autorise une suppression des gates humains.

## 17_RESUME_POINT

L'export JSON graph reel ne devra etre ouvert qu'apres stabilisation de ces criticites candidates par les GOs LocalCMS/TMUX et daily journal mapping.

## RISKS

- À qualifier.
