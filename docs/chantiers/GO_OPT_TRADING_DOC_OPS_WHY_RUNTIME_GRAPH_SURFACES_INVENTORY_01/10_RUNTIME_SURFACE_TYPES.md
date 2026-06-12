# 10_RUNTIME_SURFACE_TYPES

## 1_MASTER_TARGET

Classifier les surfaces runtime devenues pertinentes pour le futur WHY/runtime graph apres les merges post-OpenClaw.

## WHY

Sans taxonomie canonique des surfaces, le futur graph risque de melanger artefacts de preuve, composants runtime, consumers read-only et overlays de validation.

## 7_CANONICAL_STATE

Typologie retenue pour ce GO :

| Surface family | Sous-types principaux | Role dans le futur graph |
| --- | --- | --- |
| OpenClaw runtime | policy chain, warning-only workflow, JSON report | overlay runtime/security et preuve de controle |
| TMUX runtime | spine, sessions, machine placement, restart semantics | structure runtime centrale et surfaces critiques |
| LocalCMS | cockpit read-only, navigation centrale, vues runtime | consumer read-only et facade d'observation |
| Daily journals | run traces, run ids, snapshots, execution chronology | unite canonique de trace et de contexte |
| Validators | static validators, doc validators, quality gates warning-only | verification statique des surfaces et docs |
| WHY lint | rule refinement, control scans, warning families | overlay documentaire warning-only |
| Security aggregators | validation aggregator, warning reports, artifact lineage | agregation de signaux de conformite |
| Observability artefacts | JSON artifacts, logs, snapshots, reports | preuves runtime et etat observable |

## 8_CLASSIFICATION_RULES

- Une surface runtime active et un artefact de preuve ne doivent pas partager la meme classe conceptuelle.
- Les consumers read-only doivent etre distingues des producteurs runtime.
- Les overlays `warning-only` doivent rester separes des surfaces qu'ils observent.
- Un document de governance n'est pas une surface runtime, meme s'il gouverne une surface runtime.

## 12_INVARIANTS

- Aucun sous-type n'implique une activation runtime.
- Aucun sous-type n'implique un export JSON deja stabilise.
- Aucune taxonomie n'autorise a inferer une surface non prouvee dans le repo.

## 17_RESUME_POINT

Le futur GO d'integration LocalCMS/TMUX devra partir de cette taxonomie pour relier consumers, runtime spine et artefacts sans confondre leurs roles.

## RISKS

- À qualifier.
