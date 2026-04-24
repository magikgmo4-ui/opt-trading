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
updated_at: 2026-04-24
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
- snapshot de reference : `origin/sot/mainline@64df21f`
- date de reference : `2026-04-24`
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

- branches remote : `42`
- branches locales : `40`
- entrees totales suivies dans le tableau : `70`
- comparaison de reference : `origin/sot/mainline`

| CANON_STATUS | COUNT |
| --- | ---: |
| `KEEP_ACTIVE` | 2 |
| `KEEP_REFERENCE` | 16 |
| `DROP_MERGED` | 4 |
| `DROP_LOCAL_ONLY` | 15 |
| `A_VERIFIER` | 33 |

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
| `codex/remove-infra-context-sanitized` | both | ABSORBED | 0 | 8 | `DROP_MERGED` | `delete_after_doc_patch` | Branche deja absorbee par `origin/sot/mainline` ; conservation active non prouvee | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `codex/reseau-ssh-runtime-compat-retirement-01` | local | DIVERGED | 1 | 55 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `codex/reseau-ssh-runtime-compat-retirement-01-isolate` | local | ABSORBED | 0 | 53 | `DROP_LOCAL_ONLY` | `delete_local_after_doc_patch` | Branche locale deja absorbee par `origin/sot/mainline` et sans remote actif a conserver | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `codex/root-surface-reclass-01` | local | DIVERGED | 2 | 7 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `codex/sot-mainline-backup-a885f0b-prepublish-2026-04-22` | local | DIVERGED | 2 | 58 | `KEEP_REFERENCE` | `exclude_cleanup` | Snapshot / backup / rescue conserve comme reference et rollback potentiel | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `doc/GO_OPENCLAW_INFRA_BASELINE_01` | remote | DIVERGED | 1 | 308 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `docs/github-park-branch-trunk-cross-audit-01` | local | ABSORBED | 0 | 106 | `DROP_LOCAL_ONLY` | `delete_local_after_doc_patch` | Branche locale deja absorbee par `origin/sot/mainline` et sans remote actif a conserver | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `docs/github-park-parent-closeout-01` | remote | DIVERGED | 1 | 107 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `docs/github-park-pass-close-01` | remote | DIVERGED | 4 | 107 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `docs/memory-bricks-localcms-contract-alignment-01` | both | DIVERGED | 5 | 108 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `docs/skills-usage-cross-review-01` | both | DIVERGED | 1 | 107 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `docs/tmux-opencode-openclaw-runtime-01` | both | DIVERGED | 1 | 107 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/bot-vision-watchdog-01` | local | ABSORBED | 0 | 428 | `DROP_LOCAL_ONLY` | `delete_local_after_doc_patch` | Branche locale deja absorbee par `origin/sot/mainline` et sans remote actif a conserver | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/engines-plugin` | local | ABSORBED | 0 | 831 | `DROP_LOCAL_ONLY` | `delete_local_after_doc_patch` | Branche locale deja absorbee par `origin/sot/mainline` et sans remote actif a conserver | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/execution-engine` | local | ABSORBED | 0 | 827 | `DROP_LOCAL_ONLY` | `delete_local_after_doc_patch` | Branche locale deja absorbee par `origin/sot/mainline` et sans remote actif a conserver | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01` | both | DIVERGED | 13 | 298 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/go-strategy-docs-v1` | remote | DIVERGED | 1 | 708 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/journal-api-extractor-bootstrap` | local | DIVERGED | 2 | 235 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/journal-api-extractor-v1` | local | DIVERGED | 6 | 235 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/memory-bricks-api-v2-minimal-impl-01` | local | ABSORBED | 0 | 107 | `DROP_LOCAL_ONLY` | `delete_local_after_doc_patch` | Branche locale deja absorbee par `origin/sot/mainline` et sans remote actif a conserver | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/memory-bricks-v2-find` | remote | DIVERGED | 1 | 505 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/memory-bricks-v2-health-status` | remote | DIVERGED | 1 | 575 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/memory-bricks-v2-health-status-clean` | remote | DIVERGED | 1 | 488 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/mimo-open-observer-doc-pack-v0` | remote | DIVERGED | 22 | 894 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/opt-trading-index-hardening` | local | DIVERGED | 2 | 235 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/persistent-state` | local | ABSORBED | 0 | 820 | `DROP_LOCAL_ONLY` | `delete_local_after_doc_patch` | Branche locale deja absorbee par `origin/sot/mainline` et sans remote actif a conserver | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/position-engine` | local | ABSORBED | 0 | 824 | `DROP_LOCAL_ONLY` | `delete_local_after_doc_patch` | Branche locale deja absorbee par `origin/sot/mainline` et sans remote actif a conserver | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/position-guard` | local | ABSORBED | 0 | 816 | `DROP_LOCAL_ONLY` | `delete_local_after_doc_patch` | Branche locale deja absorbee par `origin/sot/mainline` et sans remote actif a conserver | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/product-target-canon` | local | ABSORBED | 0 | 228 | `DROP_LOCAL_ONLY` | `delete_local_after_doc_patch` | Branche locale deja absorbee par `origin/sot/mainline` et sans remote actif a conserver | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/project-card-module-contextuals-shell-01` | remote | DIVERGED | 1 | 193 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/project-card-openclaw-01` | remote | DIVERGED | 1 | 193 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/project-card-validated-prompt-factory-01` | remote | DIVERGED | 1 | 193 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/reseau-ssh-consolidation-lot2-freeze-01` | local | ABSORBED | 0 | 157 | `DROP_LOCAL_ONLY` | `delete_local_after_doc_patch` | Branche locale deja absorbee par `origin/sot/mainline` et sans remote actif a conserver | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/reseau-ssh-consolidation-lot3-minimal-01` | local | ABSORBED | 0 | 143 | `DROP_LOCAL_ONLY` | `delete_local_after_doc_patch` | Branche locale deja absorbee par `origin/sot/mainline` et sans remote actif a conserver | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/risk-engine` | local | ABSORBED | 0 | 835 | `DROP_LOCAL_ONLY` | `delete_local_after_doc_patch` | Branche locale deja absorbee par `origin/sot/mainline` et sans remote actif a conserver | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/student-mimo-bitget-live-equity` | remote | DIVERGED | 23 | 662 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `feat/student-mimo-qualification` | remote | DIVERGED | 21 | 662 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `fix/desk-ui-toolbox` | local | ABSORBED | 0 | 863 | `DROP_LOCAL_ONLY` | `delete_local_after_doc_patch` | Branche locale deja absorbee par `origin/sot/mainline` et sans remote actif a conserver | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | remote | DIVERGED | 10 | 68 | `KEEP_ACTIVE` | `keep_under_review` | Parent AI team encore present comme support Git d un flux actif reel | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `go_repos_agent-role_initial_01` | remote | DIVERGED | 1 | 68 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche de reference conservee explicitement hors cleanup | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `go/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` | both | ABSORBED | 0 | 1 | `DROP_MERGED` | `delete_after_doc_patch` | Branche deja absorbee par `origin/sot/mainline` ; conservation active non prouvee | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01` | both | DIVERGED | 2 | 15 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01_ALIGNMENT_01` | both | DIVERGED | 1 | 15 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `go/GO_OPT_TRADING_MATRICE_GOUVERNANTE_PROMOTION_01` | both | ABSORBED | 0 | 19 | `DROP_MERGED` | `delete_after_doc_patch` | Branche deja absorbee par `origin/sot/mainline` ; conservation active non prouvee | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `go/matrice-doc-ops-propagation-01` | remote | DIVERGED | 2 | 14 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `go/matrice-maitre-plan-doc-01` | remote | ABSORBED | 0 | 18 | `DROP_MERGED` | `delete_after_doc_patch` | Branche deja absorbee par `origin/sot/mainline` ; conservation active non prouvee | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
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
| `tmp_GO_DB_LAYER_INGESTION_PRECONDITIONS_PATCH_01` | local | ABSORBED | 0 | 210 | `DROP_LOCAL_ONLY` | `delete_local_after_doc_patch` | Branche locale deja absorbee par `origin/sot/mainline` et sans remote actif a conserver | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |
| `wip/GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01` | local | DIVERGED | 1 | 123 | `A_VERIFIER` | `manual_review` | Branche divergente ou ahead encore non justifiee pour suppression | `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01` |

## Journal minimal

- photo canonique rafraichie sur `origin/sot/mainline@64df21f` apres `fetch --all --prune`
- branche parent de reprise `go/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` requalifiee `DROP_MERGED` : le parent reste ouvert dans la continuite, mais sa branche dediee est maintenant absorbee par `sot/mainline`
- branches gardees actives : `sot/mainline`, `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`
- branches gardees en reference : `go_repos_agent-role_initial_01`, `main`, `sot/build`, familles `backup/*`, `rescue/*`, `save/*`
- suppressions immediates preparees sans execution : `codex/remove-infra-context-sanitized`, `go/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01`, `go/GO_OPT_TRADING_MATRICE_GOUVERNANTE_PROMOTION_01`, `go/matrice-maitre-plan-doc-01`, plus le lot local absorbe en `DROP_LOCAL_ONLY`
- entree stale retiree du tableau : `backup/mimo-b038db9`
- branches encore divergentes ou ahead requalifiees en `A_VERIFIER` en attente d'arbitrage explicite ; aucune suppression executee dans ce passage

## Point de reprise

Pour toute nouvelle session de housekeeping :
- repartir de `docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md`
- charger d'abord `docs/index/BRANCH_STATE.md`
- verifier le delta Git reel depuis la date et le commit de reference
- executer uniquement les suppressions qualifiees `DROP_MERGED` et `DROP_LOCAL_ONLY` apres validation explicite
- refaire `git fetch --all --prune`
- passer ensuite a `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`
