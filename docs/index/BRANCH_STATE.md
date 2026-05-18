---
doc_id: OPT_TRADING_BRANCH_STATE_01
doc_type: index
repo: opt-trading
project: opt-trading
go_id: GO_GIT_BRANCH_STATE_CANON_CREATE_01
status: reference
lifecycle_stage: continuity_index
topic_keys:
  - git
  - branches
  - continuity
  - housekeeping
  - index
surface: index
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Tableau canonique"
updated_at: 2026-05-14
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md
  - docs/index/GO_INDEX.md
  - docs/index/REPRISE.md
  - docs/chantiers/GO_GIT_GO_REPOS_AGENT_ROLE_INITIAL_CLASSIFICATION_01/03_decisions.md
  - docs/chantiers/GO_GIT_OPENCLAW_STATE_DIR_REPAIR_10_CLASSIFICATION_01/03_decisions.md
---

# BRANCH_STATE

## Objet

Cette fiche est la photo canonique courante du parc branches Git de `opt-trading`.

Elle sert a :
- figer l'etat courant branche par branche
- eviter de repartir de zero a chaque session de housekeeping
- tracer les classifications deja decidees
- completer `docs/index/GO_INDEX.md` pour la surface branches

## Hierarchie de lecture

- l'etat reel Git prouve prime
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` gouverne la place du support Git
- `docs/index/BRANCH_STATE.md` est canonique pour la surface branches seulement
- `docs/index/BRANCH_STATE.md` ne gouverne ni la continuite produit ni la structure parent / GO

## En-tete canonique

- repo : `opt-trading`
- branche canonique : `sot/mainline`
- base de comparaison : `origin/sot/mainline`
- snapshot de reference : `origin/sot/mainline@9791516`
- date de reference : `2026-04-28`
- perimetre : branches locales et distantes presentes apres `fetch --prune`

## Regle canonique de maintenance

Toute decision touchant une branche doit mettre a jour cette fiche dans le meme passage documentaire ou operatoire.

Obligations explicites :
- tout ajout de branche significative doit creer ou mettre a jour une ligne ici
- toute suppression locale ou remote executee doit retirer la ligne courante et laisser une trace concise dans le journal minimal
- toute reclassification (`KEEP_ACTIVE`, `KEEP_REFERENCE`, `DROP_MERGED`, `DROP_LOCAL_ONLY`, `A_VERIFIER`) doit etre refletee ici
- toute nouvelle branche `GO_*`, `audit/*`, `save/*`, `inventory/*`, `integ/*` doit etre classee rapidement ici
- cette fiche ne remplace pas `docs/index/GO_INDEX.md`
- cette fiche complete `docs/index/GO_INDEX.md` pour l'etat du parc branches

## Synthese courante

- branches remote : `~-39` (lot supprimé 2026-05-17, décompte exact à recalculer au prochain fetch)
- branches locales : `~-35`
- entrees totales suivies dans le tableau : `83` (tableau non encore rafraichi pour ce lot)
- comparaison de reference : `origin/sot/mainline`
- **derniere operation** : GO_DB_LAYER_REPRISE_AUDIT_01 — lot DROP_MERGED 2026-05-17

| CANON_STATUS | COUNT |
| --- | ---: |
| `KEEP_ACTIVE` | 7 |
| `KEEP_REFERENCE` | 21 |
| `DROP_MERGED` | 16 |
| `DROP_LOCAL_ONLY` | 0 |
| `BLOCKED` | 1 |
| `A_VERIFIER` | 38 |

## Legende de lecture

- `STATUS_VS_SOT_MAINLINE` : `SELF`, `ABSORBED`, `AHEAD_ONLY`, `BEHIND_ONLY`, `DIVERGED`, `PARITY`
- `AHEAD_BY` / `BEHIND_BY` : nombre de commits compares a `origin/sot/mainline`
- `CANON_STATUS` : statut courant de conservation ou de revue
- `ACTION` : geste operatoire recommande a partir du statut courant
- `LAST_REVIEW_GO` : GO de classement le plus recent, ou baseline initiale `GO_GIT_BRANCH_STATE_CANON_CREATE_01`

## Tableau canonique

| BRANCH | SCOPE | STATUS_VS_SOT_MAINLINE | AHEAD_BY | BEHIND_BY | CANON_STATUS | ACTION | JUSTIFICATION | LAST_REVIEW_GO |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| `audit/opt-trading-20260320a` | remote | DIVERGED | 20 | 662 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `backup/pre_push_2026_03_14` | local | ABSORBED | 0 | 714 | `KEEP_REFERENCE` | `exclude_cleanup` | Snapshot / backup / rescue conserve comme reference et rollback potentiel | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `backup/sot-mainline-before-rebase-2026-04-09` | local | DIVERGED | 1 | 397 | `KEEP_REFERENCE` | `exclude_cleanup` | Snapshot / backup / rescue conserve comme reference et rollback potentiel | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `codex/doc-ops-child-branch-cleanup-01` | local | AHEAD_ONLY | 1 | 0 | `KEEP_ACTIVE` | `keep_under_review` | Branche locale de travail du sous-lot cleanup tant qu'il n'est pas merge | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `codex/reseau-ssh-runtime-compat-retirement-01` | local | DIVERGED | 1 | 55 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `codex/root-surface-reclass-01` | local | DIVERGED | 2 | 7 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `codex/sot-mainline-backup-a885f0b-prepublish-2026-04-22` | local | DIVERGED | 2 | 58 | `KEEP_REFERENCE` | `exclude_cleanup` | Snapshot / backup / rescue conserve comme reference et rollback potentiel | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `doc/GO_OPENCLAW_INFRA_BASELINE_01` | remote | DIVERGED | 1 | 1237 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche historique OpenClaw deja ancree dans le canon local ; conservee comme reference | `GO_OPT_TRADING_DB_LAYER_BRANCH_STATE_SEED_01` |
| `docs/github-park-parent-closeout-01` | remote | DIVERGED | 1 | 107 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `docs/github-park-pass-close-01` | remote | DIVERGED | 4 | 107 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `docs/memory-bricks-localcms-contract-alignment-01` | both | DIVERGED | 5 | 108 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `docs/skills-usage-cross-review-01` | both | DIVERGED | 1 | 107 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `docs/tmux-opencode-openclaw-runtime-01` | both | DIVERGED | 1 | 107 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01` | both | DIVERGED | 13 | 298 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/go-strategy-docs-v1` | remote | DIVERGED | 1 | 708 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/journal-api-extractor-bootstrap` | local | DIVERGED | 2 | 235 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/journal-api-extractor-v1` | local | DIVERGED | 6 | 235 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/memory-bricks-v2-find` | remote | DIVERGED | 1 | 505 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/memory-bricks-v2-health-status` | remote | DIVERGED | 1 | 575 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/memory-bricks-v2-health-status-clean` | remote | DIVERGED | 1 | 488 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/mimo-open-observer-doc-pack-v0` | remote | DIVERGED | 22 | 894 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/opt-trading-index-hardening` | local | DIVERGED | 2 | 235 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/project-card-module-contextuals-shell-01` | remote | DIVERGED | 1 | 193 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/project-card-openclaw-01` | remote | DIVERGED | 1 | 193 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/project-card-validated-prompt-factory-01` | remote | DIVERGED | 1 | 193 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/student-mimo-bitget-live-equity` | remote | DIVERGED | 23 | 1480 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche historique student/mimo ; Student/Ollama surface FULLY_CLOSED ; conservee comme reference historique | `GO_OPT_TRADING_MACHINE_STUDENT_POST_AGENT_CLOSURE_INDEXATION_REPAIR_01` |
| `feat/student-mimo-qualification` | remote | DIVERGED | 21 | 662 | `DROP_MERGED` | `delete_local_and_remote` | Branche student/mimo deja supprimee a distance (Delete Final Status REMOTE_DELETED) ; mise a jour de la classification dans ce lot | `GO_OPT_TRADING_MACHINE_STUDENT_POST_AGENT_CLOSURE_INDEXATION_REPAIR_01` |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | both | DIVERGED | 10 | 141 | `KEEP_ACTIVE` | `keep_under_review` | Parent AI team actif, dossier canonique materialise sur `sot/mainline` et reflet `GO_INDEX.md` re-aligne dans ce lot | `GO_OPT_TRADING_REMAINING_GO_BRANCHES_DOC_REPRESENTATION_ALIGNMENT_03` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01` | both | DIVERGED | 8 | 692 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_BRIDGE_GUARD_ADD_01` | remote | DIVERGED | 1 | 806 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_CLOSEOUT_01` | remote | DIVERGED | 1 | 806 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_DESK_BRIDGE_INTEGRATION_SMOKE_01` | remote | DIVERGED | 1 | 806 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01` | remote | DIVERGED | 2 | 806 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_PARENT_REALIGNMENT_01` | remote | DIVERGED | 1 | 806 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche admin-trading de reference — absorbee ou closeout | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01` | remote | DIVERGED | 1 | 806 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche admin-trading de reference — absorbee ou closeout | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01` | remote | DIVERGED | 2 | 806 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01` | both | DIVERGED | 11 | 692 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_BRIDGE_RETRY_01` | remote | DIVERGED | 1 | 806 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche admin-trading de reference — absorbee ou closeout | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AGENT_STANDARD_NEED_VALIDATION_01` | remote | BEHIND_ONLY | 0 | 112 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_ARTIFACT_STABILITY_POST_MERGE_SYNC_01` | remote | BEHIND_ONLY | 0 | 287 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01` | both | BEHIND_ONLY | 0 | 314 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_REVIEW_MERGE_01` | remote | BEHIND_ONLY | 0 | 296 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01` | both | BEHIND_ONLY | 0 | 315 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_SEQUENCE_CLOSEOUT_01` | both | BEHIND_ONLY | 0 | 312 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_STABILITY_WINDOW_01` | both | BEHIND_ONLY | 0 | 313 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_COMBINED_INPUT_SMOKE_01` | both | BEHIND_ONLY | 0 | 239 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DESK_SNAPSHOT_INPUT_01` | both | BEHIND_ONLY | 0 | 242 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DRY_RUN_IMPL_01` | both | BEHIND_ONLY | 0 | 559 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_FIRST_TRIGGER_OBSERVE_01` | both | BEHIND_ONLY | 0 | 552 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_INPUT_ENRICHMENT_PLAN_01` | both | BEHIND_ONLY | 0 | 243 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_INPUT_SEQUENCE_CLOSEOUT_01` | both | BEHIND_ONLY | 0 | 238 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_CONTROLLED_PILOT_EXECUTION_01` | both | BEHIND_ONLY | 0 | 182 | `DROP_MERGED` | `delete_local_and_remote` | Branche admin-trading mergee dans sot/mainline — cleanup candidate apres 2026-05-28 | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_PHASE_2_STABILITY_GATE_01` | both | BEHIND_ONLY | 0 | 103 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_STEADY_STATE_FIRST_14D_REVIEW_01` | both | DIVERGED | 1 | 48 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_OBSERVABILITY_01` | both | BEHIND_ONLY | 0 | 555 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01` | both | BEHIND_ONLY | 0 | 560 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_SEQUENCE_CLOSEOUT_01` | both | BEHIND_ONLY | 0 | 550 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_SIGNAL_EVENT_INPUT_01` | both | BEHIND_ONLY | 0 | 240 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_IMPL_01` | both | BEHIND_ONLY | 0 | 557 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_INSTALL_GATED_01` | both | BEHIND_ONLY | 0 | 556 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_PAYLOAD_FIX_01` | both | BEHIND_ONLY | 0 | 553 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_SPEC_01` | both | BEHIND_ONLY | 0 | 558 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_STABILITY_WINDOW_01` | both | BEHIND_ONLY | 0 | 551 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_START_GATED_01` | both | BEHIND_ONLY | 0 | 554 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_VISUAL_CONTEXT_INPUT_01` | both | BEHIND_ONLY | 0 | 241 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01` | remote | DIVERGED | 1 | 806 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche admin-trading de reference — absorbee ou closeout | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01` | both | DIVERGED | 9 | 692 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01` | both | DIVERGED | 10 | 692 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SMOKE_01` | remote | DIVERGED | 1 | 806 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche admin-trading de reference — absorbee ou closeout | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_FLAGS_CONFIG_01` | remote | BEHIND_ONLY | 0 | 192 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_POSITION_CLOSE_01` | remote | BEHIND_ONLY | 0 | 166 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_01` | remote | BEHIND_ONLY | 0 | 241 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_GATE_01` | remote | BEHIND_ONLY | 0 | 676 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01` | both | DIVERGED | 5 | 692 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01` | both | DIVERGED | 12 | 692 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_MONITORING_AND_SECRETS_AUDIT_01` | remote | DIVERGED | 1 | 48 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_MONITORING_PNL_ALERT_THRESHOLDS_01` | remote | DIVERGED | 1 | 47 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche admin-trading doc complete non merge — classement A_VERIFIER_REVIEW_01 | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_A_VERIFIER_REVIEW_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_01` | remote | BEHIND_ONLY | 0 | 107 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_SEQUENCE_PR_MERGE_01` | both | DIVERGED | 13 | 692 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading aggregation active 6.5k+ lignes — classement A_VERIFIER_REVIEW_01 | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_A_VERIFIER_REVIEW_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01` | remote | BEHIND_ONLY | 0 | 805 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01` | remote | DIVERGED | 1 | 806 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche admin-trading de reference — absorbee ou closeout | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01` | remote | DIVERGED | 1 | 806 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche admin-trading de reference — absorbee ou closeout | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01` | both | DIVERGED | 6 | 692 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01` | remote | DIVERGED | 1 | 806 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche admin-trading de reference — absorbee ou closeout | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01` | both | DIVERGED | 7 | 692 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01` | remote | DIVERGED | 19 | 141 | `KEEP_REFERENCE` | `exclude_cleanup` | Dossier chantier local riche present ; branche absente du Git observe dans la passe db-layer, conservee comme reference documentaire | `GO_OPT_TRADING_DB_LAYER_A_VERIFIER_REVIEW_01` |
| `go/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01` | both | DIVERGED | 18 | 141 | `DROP_MERGED` | `delete_local_and_remote` | Branche doc-only parent bundle storage mergee dans sot/mainline ; branche supprimee localement et a distance | `GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_REMOTE_CLEANUP_01` |
| `go/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01` | remote | DIVERGED | 3 | 49 | `A_VERIFIER` | `manual_review` | Branche GO restante presente dans Git mais sans representation canonique complete sur les surfaces doc courantes | `GO_OPT_TRADING_REMAINING_GO_BRANCHES_DOC_REPRESENTATION_ALIGNMENT_03` |
| `go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01` | remote | DIVERGED | 12 | 141 | `KEEP_ACTIVE` | `keep_under_review` | Branche parent ClickUp continuity ; bundle doc-only merge localement dans sot/mainline (c8362b7), parent maintenu actif pour continuite et suite d implementation | `GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_REVIEW_MERGE_01` |
| `go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01` | both | DIVERGED | 6 | 56 | `BLOCKED` | `keep_under_review` | BLOCKED : branche non mergee avec contenu significatif (124 fichiers, reseau_ssh) ; chantier a closeout mais delta reel trop lourd pour une suppression sans merge explicite | `GO_OPT_TRADING_DOC_OPS_BRANCH_CLEANUP_MATRIX_METHOD_01` |
| `go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01_ISOLATED` | both | BEHIND_ONLY | 0 | 50 | `DROP_MERGED` | `delete_local_and_remote` | Branche merged dans sot/mainline ; supprimee localement et a distance ; worktree nettoye | `GO_OPT_TRADING_DOC_OPS_POST_3_PASS_CANONICAL_REPRISE_01` |
| `go/GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01` | both | BEHIND_ONLY | 0 | 16 | `DROP_MERGED` | `delete_local_and_remote` | Branche merged dans sot/mainline ; closeout present ; mention descriptive dans REPRISE.md conservee hors branche ; branche supprimee localement et a distance | `GO_OPT_TRADING_DOC_OPS_BRANCH_CLEANUP_MATRIX_METHOD_01` |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` | remote | DIVERGED | 12 | 886 | `DROP_MERGED` | `delete_local_and_remote` | Student/Ollama parent ; surface FULLY_CLOSED ; closeout PASS dans `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/90_CLOSEOUT.md` | `GO_OPT_TRADING_MACHINE_STUDENT_POST_AGENT_CLOSURE_INDEXATION_REPAIR_01` |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_CANONICAL_INDEX_AGGREGATION_01` | remote | DIVERGED | 1 | 695 | `DROP_MERGED` | `delete_local_and_remote` | Student/Ollama sub-parent ; surface FULLY_CLOSED | `GO_OPT_TRADING_MACHINE_STUDENT_POST_AGENT_CLOSURE_INDEXATION_REPAIR_01` |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_REVIEW_REALIGN_01` | remote | ABSORBED | 0 | 449 | `DROP_MERGED` | `delete_local_and_remote` | Student/Ollama sub-parent ; PR #251 merged ; surface FULLY_CLOSED | `GO_OPT_TRADING_MACHINE_STUDENT_POST_AGENT_CLOSURE_INDEXATION_REPAIR_01` |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_SELECTIVE_PROPAGATION_01` | remote | DIVERGED | 1 | 695 | `DROP_MERGED` | `delete_local_and_remote` | Student/Ollama sub-parent ; surface FULLY_CLOSED | `GO_OPT_TRADING_MACHINE_STUDENT_POST_AGENT_CLOSURE_INDEXATION_REPAIR_01` |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CAPABILITY_GATE_AND_FALLBACK_01` | remote | ABSORBED | 0 | 43 | `DROP_MERGED` | `delete_local_and_remote` | Agent standardization chain ; surface FULLY_CLOSED | `GO_OPT_TRADING_MACHINE_STUDENT_POST_AGENT_CLOSURE_INDEXATION_REPAIR_01` |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_FIRST_CONTROLLED_CONSUMER_01` | remote | ABSORBED | 0 | 51 | `DROP_MERGED` | `delete_local_and_remote` | Agent standardization chain ; surface FULLY_CLOSED | `GO_OPT_TRADING_MACHINE_STUDENT_POST_AGENT_CLOSURE_INDEXATION_REPAIR_01` |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CONTROLLED_USAGE_RUNBOOK_01` | remote | ABSORBED | 0 | 69 | `DROP_MERGED` | `delete_local_and_remote` | Agent standardization chain ; surface FULLY_CLOSED | `GO_OPT_TRADING_MACHINE_STUDENT_POST_AGENT_CLOSURE_INDEXATION_REPAIR_01` |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_RUNTIME_BASELINE_ADOPTION_01` | remote | ABSORBED | 0 | 71 | `DROP_MERGED` | `delete_local_and_remote` | Agent standardization chain ; FULL_PASS ; surface FULLY_CLOSED | `GO_OPT_TRADING_MACHINE_STUDENT_POST_AGENT_CLOSURE_INDEXATION_REPAIR_01` |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_POLICY_01` | remote | ABSORBED | 0 | 829 | `DROP_MERGED` | `delete_local_and_remote` | Agent standardization chain ; surface FULLY_CLOSED | `GO_OPT_TRADING_MACHINE_STUDENT_POST_AGENT_CLOSURE_INDEXATION_REPAIR_01` |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_ENFORCEMENT_01` | remote | ABSORBED | 0 | 75 | `DROP_MERGED` | `delete_local_and_remote` | Agent standardization chain ; surface FULLY_CLOSED | `GO_OPT_TRADING_MACHINE_STUDENT_POST_AGENT_CLOSURE_INDEXATION_REPAIR_01` |
| `go/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01` | remote | DIVERGED | 2 | 683 | `KEEP_REFERENCE` | `exclude_cleanup` | Machine student parent ; DEFERRED per doc-ops decision ; jamais ouvert formellement ; conserve comme reference | `GO_OPT_TRADING_MACHINE_STUDENT_POST_AGENT_CLOSURE_INDEXATION_REPAIR_01` |
| `go_repos_agent-role_initial_01` | remote | DIVERGED | 1 | 68 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche de reference conservee explicitement hors cleanup | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01` | both | DIVERGED | 2 | 88 | `KEEP_ACTIVE` | `keep_under_review` | Parent ouvert explicitement prouve par la matrice, `GO_INDEX.md` et le dossier chantier ; branche doc-only gardee active | `GO_OPT_TRADING_REMAINING_GO_BRANCHES_DOC_REPRESENTATION_ALIGNMENT_03` |
| `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01_ALIGNMENT_01` | both | DIVERGED | 1 | 88 | `A_VERIFIER` | `manual_review` | Branche d'alignement encore presente dans Git sans dossier chantier propre sur la ligne courante ; maintien en revue seulement | `GO_OPT_TRADING_REMAINING_GO_BRANCHES_DOC_REPRESENTATION_ALIGNMENT_03` |
| `go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | both | DIVERGED | 4 | 22 | `KEEP_ACTIVE` | `keep_under_review` | Parent ouvert explicitement prouve par `GO_INDEX.md`, `ACTIVE_STREAMS.md`, `REPRISE.md`, `PARENT_STATE.md` et desormais cite explicitement dans la matrice | `GO_OPT_TRADING_REMAINING_GO_BRANCHES_DOC_REPRESENTATION_ALIGNMENT_03` |
| `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01` | remote | DIVERGED | 2 | 688 | `DROP_MERGED` | `delete_local_and_remote` | Child doc-only clos ; chaine OpenClaw/TMUX closee documentairement ; cleanup interdit dans cette passe | `GO_OPT_TRADING_DB_LAYER_BRANCH_STATE_SEED_01` |
| `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01` | remote | DIVERGED | 1 | 680 | `KEEP_REFERENCE` | `exclude_cleanup` | Closeout de chaine OpenClaw/TMUX conserve comme trace de reference | `GO_OPT_TRADING_DB_LAYER_BRANCH_STATE_SEED_01` |
| `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01` | remote | DIVERGED | 3 | 681 | `KEEP_REFERENCE` | `exclude_cleanup` | Runtime TMUX clos en PASS avec log local explicite ; branche residuelle conservee comme trace de reference, sans cleanup dans cette passe | `GO_OPT_TRADING_DB_LAYER_REMAINING_A_VERIFIER_REVIEW_01` |
| `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` | remote | DIVERGED | 9 | 905 | `KEEP_ACTIVE` | `keep_under_review` | Parent reel `db-layer` conserve comme ancre documentaire ; aucune reprise runtime requise | `GO_OPT_TRADING_DB_LAYER_BRANCH_STATE_SEED_01` |
| `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_DOC_REALIGN_01` | remote | DIVERGED | 1 | 698 | `KEEP_REFERENCE` | `exclude_cleanup` | Lot de realignement du parent cite comme reference de revue du parent OpenClaw | `GO_OPT_TRADING_DB_LAYER_BRANCH_STATE_SEED_01` |
| `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01` | remote | BEHIND_ONLY | 0 | 372 | `KEEP_ACTIVE` | `keep_under_review` | Child doc-only materialise sous le parent OpenClaw runtime security encore ouvert | `GO_OPT_TRADING_DB_LAYER_A_VERIFIER_REVIEW_01` |
| `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01` | remote | BEHIND_ONLY | 0 | 354 | `KEEP_ACTIVE` | `keep_under_review` | Child doc-only materialise sous le parent OpenClaw runtime security encore ouvert | `GO_OPT_TRADING_DB_LAYER_A_VERIFIER_REVIEW_01` |
| `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_YAML_DRAFT_01` | remote | DIVERGED | 2 | 353 | `KEEP_ACTIVE` | `keep_under_review` | Draft child coherent avec le parent OpenClaw runtime security encore ouvert | `GO_OPT_TRADING_DB_LAYER_A_VERIFIER_REVIEW_01` |
| `go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01` | remote | BEHIND_ONLY | 0 | 374 | `KEEP_ACTIVE` | `keep_under_review` | Parent doc-only ouvert, spec et inbox locales presentes, suite child explicite | `GO_OPT_TRADING_DB_LAYER_A_VERIFIER_REVIEW_01` |
| `go/GO_OPENCLAW_STATE_DIR_REPAIR_10` | remote | DIVERGED | 1 | 814 | `KEEP_REFERENCE` | `exclude_cleanup` | Lot OpenClaw historique deja conserve comme reference de classification | `GO_OPT_TRADING_DB_LAYER_BRANCH_STATE_SEED_01` |
| `go/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_REVIEW_01` | remote | DIVERGED | 1 | 814 | `KEEP_REFERENCE` | `exclude_cleanup` | Closeout distant `PASS` prouve via lecture directe de la branche ; conservee comme trace de review parent db-layer | `GO_OPT_TRADING_DB_LAYER_DEEP_AUDIT_01` |
| `go/GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01` | remote | DIVERGED | 1 | 814 | `KEEP_REFERENCE` | `exclude_cleanup` | Closeout distant `PASS` prouve via lecture directe de la branche ; conservee comme trace de realignement LocalCMS/db-layer | `GO_OPT_TRADING_DB_LAYER_DEEP_AUDIT_01` |
| `go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LIVE_ARTIFACTS_01` | remote | BEHIND_ONLY | 0 | 49 | `A_VERIFIER` | `manual_review` | Branche GO restante presente dans Git mais sans representation canonique complete sur les surfaces doc courantes | `GO_OPT_TRADING_REMAINING_GO_BRANCHES_DOC_REPRESENTATION_ALIGNMENT_03` |
| `go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01` | remote | DIVERGED | 4 | 85 | `A_VERIFIER` | `manual_review` | Branche GO restante presente dans Git mais sans representation canonique complete sur les surfaces doc courantes | `GO_OPT_TRADING_REMAINING_GO_BRANCHES_DOC_REPRESENTATION_ALIGNMENT_03` |
| `go/GO_OPT_TRADING_REMAINING_BRANCHES_TRANSPORT_DELETE_03` | both | AHEAD_ONLY | 1 | 0 | `A_VERIFIER` | `manual_review` | Branche de lot transport/prune annule apres restauration des branches source ; maintien en attente d'une decision explicite | `GO_OPT_TRADING_REMAINING_GO_BRANCHES_DOC_REPRESENTATION_ALIGNMENT_03` |
| `go/GO_OPT_TRADING_REMAINING_BRANCHES_TRANSPORT_DELETE_03_CANCEL_01` | both | AHEAD_ONLY | 1 | 0 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche documentaire de closeout d'annulation conservee comme reference de trace | `GO_OPT_TRADING_REMAINING_GO_BRANCHES_DOC_REPRESENTATION_ALIGNMENT_03` |
| `go/GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_AUDIT_01` | both | DIVERGED | 1 | 2 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche d'audit source conservee comme reference de classement des branches restantes | `GO_OPT_TRADING_REMAINING_GO_BRANCHES_DOC_REPRESENTATION_ALIGNMENT_03` |
| `go/GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_MEMBERSHIP_AUDIT_02` | both | AHEAD_ONLY | 1 | 0 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche d'audit d'appartenance conservee comme reference de preuve documentaire | `GO_OPT_TRADING_REMAINING_GO_BRANCHES_DOC_REPRESENTATION_ALIGNMENT_03` |
| `go/GO_OPT_TRADING_REMAINING_GO_BRANCHES_DOC_REPRESENTATION_ALIGNMENT_03` | both | AHEAD_ONLY | 1 | 0 | `KEEP_ACTIVE` | `keep_under_review` | Lot doc-only courant de realignement des representations canoniques encore en cours | `GO_OPT_TRADING_REMAINING_GO_BRANCHES_DOC_REPRESENTATION_ALIGNMENT_03` |
| `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` | remote | DIVERGED | 18 | 70 | `KEEP_REFERENCE` | `exclude_cleanup` | Dossier chantier local riche et reutilise par des child docs ; branche absente du Git observe dans la passe db-layer | `GO_OPT_TRADING_DB_LAYER_A_VERIFIER_REVIEW_01` |
| `go/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01` | remote | DIVERGED | 1 | 926 | `KEEP_ACTIVE` | `keep_under_review` | Cadrage parent distant prouve avec statut `open`, TODO restants et point de reprise explicite | `GO_OPT_TRADING_DB_LAYER_DEEP_AUDIT_01` |
| `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` | both | DIVERGED | 15 | 12 | `KEEP_ACTIVE` | `keep_under_review` | Parent strict workers actif ; dossier complet sur branche (6 fichiers, closeout draft) ; non merge dans mainline ; a integrer ou poursuivre sur branche | `GO_OPT_TRADING_FANTOME_ACTIVE_PARENTS_CROSSCHECK_01` |
| `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01` | remote | BEHIND_ONLY | 0 | 302 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01` | remote | BEHIND_ONLY | 0 | 330 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01` | remote | BEHIND_ONLY | 0 | 315 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01` | remote | BEHIND_ONLY | 0 | 280 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01` | remote | BEHIND_ONLY | 0 | 310 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01` | remote | BEHIND_ONLY | 0 | 285 | `KEEP_ACTIVE` | `keep_under_review` | Branche admin-trading active classee dans MACHINE_WORK_SPLIT | `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01` |
| `go/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_CLOSEOUT_01` | remote | DIVERGED | 1 | 814 | `KEEP_REFERENCE` | `exclude_cleanup` | Closeout TMUX db-layer conserve comme reference runtime closee | `GO_OPT_TRADING_DB_LAYER_BRANCH_STATE_SEED_01` |
| `go/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_REVIEW_01` | remote | DIVERGED | 1 | 814 | `KEEP_REFERENCE` | `exclude_cleanup` | Review TMUX db-layer conservee comme reference historique | `GO_OPT_TRADING_DB_LAYER_BRANCH_STATE_SEED_01` |
| `go/matrice-doc-ops-propagation-01` | remote | DIVERGED | 2 | 14 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `integ/trading-dual-stack-doc-pack-01` | remote | DIVERGED | 4 | 569 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `inventory/collectors-baseline-01` | remote | DIVERGED | 6 | 408 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `main` | both | DIVERGED | 3 | 894 | `KEEP_REFERENCE` | `exclude_cleanup` | Tronc historique secondaire conserve en reference seulement | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `METHODE_MULTI_MACHINE_GIT_SYNC` | remote | DIVERGED | 14 | 68 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `opencode/brave-river` | local | DIVERGED | 2 | 235 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `opencode/cosmic-circuit` | local | DIVERGED | 1 | 156 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `promo/mimo-v2-bounded-01` | remote | DIVERGED | 3 | 411 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `rescue/derivatives-local-2026-04-09` | local | DIVERGED | 1 | 428 | `KEEP_REFERENCE` | `exclude_cleanup` | Snapshot / backup / rescue conserve comme reference et rollback potentiel | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `rescue/sot-mainline-local-2964fea` | local | DIVERGED | 1 | 702 | `KEEP_REFERENCE` | `exclude_cleanup` | Snapshot / backup / rescue conserve comme reference et rollback potentiel | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `save/admin-trading-2026-04-01` | remote | DIVERGED | 27 | 672 | `KEEP_REFERENCE` | `exclude_cleanup` | Snapshot / backup / rescue conserve comme reference et rollback potentiel | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `save/admin-trading-post-reset-2026-04-04` | remote | DIVERGED | 1 | 456 | `KEEP_REFERENCE` | `exclude_cleanup` | Snapshot / backup / rescue conserve comme reference et rollback potentiel | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `save/admin-trading-pre-reset-deskpro-2026-04-04` | remote | DIVERGED | 6 | 575 | `KEEP_REFERENCE` | `exclude_cleanup` | Snapshot / backup / rescue conserve comme reference et rollback potentiel | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `save/admin-trading-pre-reset-git-fleet-2026-04-04` | remote | DIVERGED | 8 | 575 | `KEEP_REFERENCE` | `exclude_cleanup` | Snapshot / backup / rescue conserve comme reference et rollback potentiel | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `save/cursor-ai-2026-04-01` | both | DIVERGED | 1 | 645 | `KEEP_REFERENCE` | `exclude_cleanup` | Snapshot / backup / rescue conserve comme reference et rollback potentiel | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `save/db-layer-2026-04-01` | remote | DIVERGED | 1 | 748 | `KEEP_REFERENCE` | `exclude_cleanup` | Snapshot / backup / rescue conserve comme reference et rollback potentiel | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `save/fantome-YYYY-MM-DD` | remote | DIVERGED | 1 | 599 | `KEEP_REFERENCE` | `exclude_cleanup` | Snapshot / backup / rescue conserve comme reference et rollback potentiel | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `save/student-2026-04-01` | remote | DIVERGED | 22 | 662 | `KEEP_REFERENCE` | `exclude_cleanup` | Snapshot / backup / rescue conserve comme reference et rollback potentiel | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `sot/build` | remote | ABSORBED | 0 | 862 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche technique sensible `sot/*` conservee comme reference | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `sot/mainline` | both | SELF | 0 | 0 | `KEEP_ACTIVE` | `protect_mainline` | Tronc canonique de continuite | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `wip/GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01` | local | DIVERGED | 1 | 123 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |

## Journal minimal

- photo canonique rafraichie sur `origin/sot/mainline@9791516` apres `fetch --all --prune` et passage de realignement documentaire des branches `GO_OPT_TRADING`
- branche locale de travail ajoutee au tableau : `codex/doc-ops-child-branch-cleanup-01` en `KEEP_ACTIVE` jusqu'au merge de ce sous-lot
- suppressions `DROP_MERGED` executees localement et/ou a distance : `codex/remove-infra-context-sanitized`, `go/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01`, `go/GO_OPT_TRADING_MATRICE_GOUVERNANTE_PROMOTION_01`, `go/matrice-maitre-plan-doc-01`
- suppressions `DROP_LOCAL_ONLY` executees : `codex/reseau-ssh-runtime-compat-retirement-01-isolate`, `docs/github-park-branch-trunk-cross-audit-01`, `feat/bot-vision-watchdog-01`, `feat/engines-plugin`, `feat/execution-engine`, `feat/memory-bricks-api-v2-minimal-impl-01`, `feat/persistent-state`, `feat/position-engine`, `feat/position-guard`, `feat/product-target-canon`, `feat/reseau-ssh-consolidation-lot2-freeze-01`, `feat/reseau-ssh-consolidation-lot3-minimal-01`, `feat/risk-engine`, `fix/desk-ui-toolbox`, `tmp_GO_DB_LAYER_INGESTION_PRECONDITIONS_PATCH_01`
- dossier canonique `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/` materialise sur la ligne courante et reflet `GO_INDEX.md` re-aligne
- mention explicite ajoutee dans la matrice pour `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` et `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`
- frontmatter `go_id` top-level re-aligne dans `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01/`
- branches `GO_OPT_TRADING` encore absentes de la surface branches ajoutees a cette fiche avec classification documentaire minimale
- branches gardees actives : `sot/mainline`, `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`, `codex/doc-ops-child-branch-cleanup-01`, `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01`, `go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`, `go/GO_OPT_TRADING_REMAINING_GO_BRANCHES_DOC_REPRESENTATION_ALIGNMENT_03`
- branches gardees en reference : `go_repos_agent-role_initial_01`, `main`, `sot/build`, `go/GO_OPT_TRADING_REMAINING_BRANCHES_TRANSPORT_DELETE_03_CANCEL_01`, `go/GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_AUDIT_01`, `go/GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_MEMBERSHIP_AUDIT_02`, familles `backup/*`, `rescue/*`, `save/*`
- branches encore divergentes ou ahead maintenues en `A_VERIFIER` en attente d'arbitrage explicite ou de preuve canonique complementaire
- lot de nettoyage `GO_OPT_TRADING_DOC_OPS_BRANCH_CLEANUP_MATRIX_METHOD_01` : 3 branches merged supprimees localement et a distance (`ACTIVE_GOVERNANCE_CLOSEOUT_REVIEW_01`, `CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01`, `INDEX_AGGREGATION_BATCH_01`) ; 1 branche `BLOCKED` (`OPEN_WORK_CONTROL_01`, non mergee, delta reseau_ssh lourd) ; 2 branches `KEEP` (`BUNDLES_REPO_STORAGE_PARENT_01`, `CLICKUP_PARENT_CONTINUITY_01`, non mergees, doc-only)
- post-lot 3/3 PASS : BUNDLES_REPO_STORAGE mergé dans sot/mainline ; OPEN_WORK_CONTROL_01_ISOLATED completement supprimee (worktree retire, branche locale supprimee) ; CLICKUP_PARENT_CONTINUITY conserve hors lot actif (machine fantome)
- branche `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` conservee comme ancre parent `db-layer` ; chaine OpenClaw recente closee dans `sot/mainline` via runtime PASS puis closeout #222 ; aucun `NEXT_GO` obligatoire
- classification Student/Ollama post-fermeture appliquee dans ce lot `GO_OPT_TRADING_MACHINE_STUDENT_POST_AGENT_CLOSURE_INDEXATION_REPAIR_01` : `feat/student-mimo-bitget-live-equity` reclassee KEEP_REFERENCE ; `feat/student-mimo-qualification` et `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` reclassees DROP_MERGED ; 10 branches Student/Ollama manquantes ajoutees en DROP_MERGED ; `go/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01` ajoutee en KEEP_REFERENCE (DEFERRED)
- execution suppression remote Student/Ollama dans `GO_OPT_TRADING_MACHINE_STUDENT_REMOTE_BRANCH_CLEANUP_EXECUTION_01` : 33 branches DELETE_CONFIRMED supprimees (4 parents + 23 lab children + 6 agent standardization) via `git push origin --delete` ; seules les 3 branches KEEP_ARCHIVE conservees : `save/student-2026-04-01`, `feat/student-mimo-bitget-live-equity`, `go/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01`
- seed `db-layer/OpenClaw` applique : 11 entrees manquantes ajoutees a `BRANCH_STATE.md`, 4 lignes reclassifiees/corrigees, aucun runtime ni cleanup Git

## Point de reprise

Pour toute nouvelle session de housekeeping :
- repartir de `docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md`
- charger d'abord `docs/index/BRANCH_STATE.md`
- verifier le delta Git reel depuis la date et le commit de reference
- repartir de `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` pour le routage machine anti-conflit

## Phase Delete (GO_OPT_TRADING_BRANCH_ARBITRATION_DELETE_AND_BRANCH_STATE_03)

- Branches A_SUPPRIMER prévues pour suppression locale et distante (dans le cadre de ce lot):
- audit/opt-trading-20260320a
- docs/github-park-parent-closeout-01
- docs/github-park-pass-close-01
- feat/journal-api-extractor-bootstrap
- feat/journal-api-extractor-v1
- feat/mimo-open-observer-doc-pack-v0
- feat/student-mimo-qualification
- METHODE_MULTI_MACHINE_GIT_SYNC
- wip/GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01

- Statut envisagé: suppression sequenceée et journalisation; main/sot/mainline protégés.
- Prochaine étape: exécuter les suppressions localement puis à distance, puis mettre à jour BRANCH_STATE.md et ajouter un closeout court.

## Delete Final Status (remote audit)

- Branch: audit/opt-trading-20260320a | local: LOCAL_ABSENT | remote: REMOTE_ABSENT
- Branch: docs/github-park-parent-closeout-01 | local: LOCAL_ABSENT | remote: REMOTE_ABSENT
- Branch: docs/github-park-pass-close-01 | local: LOCAL_ABSENT | remote: REMOTE_ABSENT
- Branch: feat/journal-api-extractor-bootstrap | local: LOCAL_DELETED | remote: REMOTE_ABSENT
- Branch: feat/journal-api-extractor-v1 | local: LOCAL_ABSENT | remote: REMOTE_ABSENT
- Branch: feat/mimo-open-observer-doc-pack-v0 | local: LOCAL_DELETED | remote: REMOTE_DELETED
- Branch: feat/student-mimo-qualification | local: LOCAL_ABSENT | remote: REMOTE_DELETED
- Branch: METHODE_MULTI_MACHINE_GIT_SYNC | local: LOCAL_ABSENT | remote: REMOTE_ABSENT
- Branch: wip/GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01 | local: LOCAL_ABSENT | remote: REMOTE_ABSENT

Note: Si une suppression distante échoue pour des credentials, elle est notée comme DELETE_ATTEMPTED_NOT_CONFIRMED et ne doit pas être présentée comme supprimée dans BRANCH_STATE.md.

## Journal post-merge OpenClaw
- 2026-04-28 — GO_OPENCLAW_POST_MERGE_BRANCH_STATE_CLEANUP_01 : branche codex/openclaw-family-consolidation-01 supprimée localement et à distance après merge de PR #167 / GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01; aucune ligne active ne doit être recréée pour cette branche. Les branches satellites OpenClaw laissées de côté restent hors périmètre.

## Lot DROP_MERGED — GO_DB_LAYER_REPRISE_AUDIT_01 (2026-05-17)

Lot de nettoyage db-layer / orchestrator exécuté après audit ahead=0 vs origin/sot/mainline. Toutes les branches ci-dessous avaient ahead=0 (confirmé avant suppression).

**Supprimées localement ET à distance (35 local / 39 remote CONFIRMED_DELETED) :**
- `go/GO_OPT_TRADING_ORCHESTRATOR_CHILD_SIGNAL_ROUTER_V1_01`
- `go/GO_OPT_TRADING_ORCHESTRATOR_CHILD_NOTIFICATION_DISPATCHER_V1_01`
- `go/GO_OPT_TRADING_ORCHESTRATOR_CHILD_PROPOSITION_ENGINE_V1_01`
- `go/GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01`
- `go/GO_OPT_TRADING_ORCHESTRATOR_CHILD_TRADE_EXECUTOR_V1_01`
- `go/GO_OPT_TRADING_ORCHESTRATOR_CHILD_RESULT_TRACKER_V1_01`
- `go/GO_OPT_TRADING_ORCHESTRATOR_CHILD_LEARNING_FEEDER_V1_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_7D_DRY_RUN_OBSERVATION_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_AUTOMATION_SCHEDULER_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_BASELINE_FINAL_CLOSEOUT_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_CONTROLLED_WRITE_PILOT_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_CRON_SYSTEMD_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_GOOGLE_SHEETS_CLOSEOUT_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_GOOGLE_SHEETS_CONTROLLED_SYNC_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_LOCALCMS_HISTORY_VIEW_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_PRODUCTION_GOVERNANCE_DECISION_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_STEADY_STATE_CLOSEOUT_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_STEADY_STATE_OBSERVATION_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_STEADY_STATE_RUN_02_TMUX_ACTIVE_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_SYSTEMD_FIRST_RUN_OBSERVATION_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_SYSTEMD_STEADY_STATE_3_RUN_REVIEW_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_E2E_DRY_RUN_DAILY_SESSION_JOURNAL_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_E2E_DRY_RUN_PIPELINE_WITH_LOCALCMS_VIEW_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_GOOGLE_SHEETS_ADC_AUTH_FALLBACK_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_GOOGLE_SHEETS_CONTROLLED_WRITE_EXECUTION_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_GOOGLE_SHEETS_CREDENTIALS_EXTERNAL_SETUP_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_GOOGLE_SHEETS_CREDENTIALS_SETUP_AND_CONTROLLED_WRITE_RETRY_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_GOOGLE_SHEETS_GSPREAD_DEPENDENCY_FIX_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_LIVE_TRADING_READINESS_DOC_ONLY_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_LOCALCMS_METRICS_DASHBOARD_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_NEXT_PHASE_DECISION_AFTER_DAILY_BASELINE_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PAPER_MODE_EXPANSION_DECISION_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_INDEX_RECONCILIATION_01`
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_FOLLOWUP_04_11_01`
- `go/GO_OPT_TRADING_MACHINE_DB_LAYER_POST_MERGE_RECONCILIATION_01`

**Supprimées à distance uniquement (remote-only) :**
- `go/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_REVIEW_01`
- `go/GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01`
- `go/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_CLOSEOUT_01`
- `go/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_REVIEW_01`

**NON supprimées — anomalie à investiguer (ahead != 0, contradiction avec classification antérieure) :**
- `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01` — 2 ahead (classé DROP_MERGED dans BRANCH_STATE mais ahead réel = 2 ; REVIEW_REQUIRED)
- `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01` — 1 ahead (non classé dans tableau ; ahead réel = 1 ; REVIEW_REQUIRED)
- `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01` — 3 ahead (classé A_VERIFIER avec 1 ahead mais ahead réel = 3 ; REVIEW_REQUIRED)

**Non touchées (A_VERIFIER ou KEEP_ACTIVE) :**
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` — KEEP_ACTIVE (9 ahead)
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PHASE1_30_RUN_14_DAY_OBSERVATION_01` — branche courante Phase 1

## Lot DROP_MERGED — A_VERIFIER finaux (2026-05-17)

Audit complet des 3 branches A_VERIFIER restantes après lot principal. Vérification merge-base + diff contenu.

**`SYSTEM_MASTER_PLAN_01`** (2 ahead) : 8/8 fichiers diff=0 — squash-orphelins.
**`PARENT_DOC_REALIGN_01`** (1 ahead) : diffs non-nuls sur BRANCH_STATE/GO_INDEX = versions anciennes, mainline plus récent ; aucun contenu forward unique.
**`ADC_CONTROLLED_WRITE_RETRY_01`** (4 ahead, local-only) : 1 doc unique (`00_GO_MASTER.md`) absent de mainline. Décision utilisateur Option B : GO ADC considéré supersédé par branches Google Sheets déjà mergées — drop branche entière, doc non mergé.

**Supprimées localement ET à distance :**
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01` — local + remote DELETED
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_DOC_REALIGN_01` — local + remote DELETED

**Supprimée localement uniquement (jamais poussée) :**
- `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_GOOGLE_SHEETS_ADC_CONTROLLED_WRITE_RETRY_01` — local DELETED

## Lot DROP_MERGED — CHILD_GATEWAY_SUPERVISION_TMUX (2026-05-17)

Audit de réconciliation post-PR #517 : 3 branches classées en contradiction (ahead réel vs classification antérieure). Vérification par merge-base + diff de contenu → tous les fichiers présents et identiques sur `sot/mainline` (0 diff lines). Squash-orphelins confirmés.

**Supprimées localement ET à distance :**
- `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01` — local + remote DELETED
- `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01` — local + remote DELETED

**Supprimée localement uniquement (pas de remote) :**
- `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01` — local DELETED
