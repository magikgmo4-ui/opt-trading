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
updated_at: 2026-04-22
links:
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

## En-tete canonique

- repo : `opt-trading`
- branche canonique : `sot/mainline`
- base de comparaison : `origin/sot/mainline`
- snapshot de reference : `origin/sot/mainline@b092f48`
- date de reference : `2026-04-22`
- perimetre : branches locales et distantes presentes apres `fetch --prune`

## Regle canonique de maintenance

Toute decision touchant une branche doit mettre a jour cette fiche dans le meme passage documentaire ou operatoire.

Obligations explicites :
- tout ajout de branche significative doit creer ou mettre a jour une ligne ici
- toute suppression locale ou remote executee doit retirer la ligne courante et laisser une trace concise dans le journal minimal
- toute reclassification (`KEEP_ACTIVE`, `KEEP_REFERENCE`, `KEEP_SNAPSHOT`, `ABSORBED`, `REDUNDANT`, `REVIEW`, `DROP_REMOTE_CANDIDATE`, `DROP_LOCAL_ONLY`) doit etre refletee ici
- toute nouvelle branche `GO_*`, `audit/*`, `save/*`, `inventory/*`, `integ/*` doit etre classee rapidement ici
- cette fiche ne remplace pas `docs/index/GO_INDEX.md`
- cette fiche complete `docs/index/GO_INDEX.md` pour l'etat du parc branches

## Synthese courante

- branches remote : `37`
- branches locales : `11`
- entrees totales suivies dans le tableau : `44`
- comparaison de reference : `origin/sot/mainline`

| CANON_STATUS | COUNT |
| --- | ---: |
| `KEEP_ACTIVE` | 2 |
| `KEEP_REFERENCE` | 1 |
| `KEEP_SNAPSHOT` | 9 |
| `ABSORBED` | 3 |
| `REDUNDANT` | 1 |
| `REVIEW` | 22 |
| `DROP_REMOTE_CANDIDATE` | 0 |
| `DROP_LOCAL_ONLY` | 6 |

## Legende de lecture

- `STATUS_VS_SOT_MAINLINE` : `SELF`, `ABSORBED`, `AHEAD_ONLY`, `BEHIND_ONLY`, `DIVERGED`, `PARITY`
- `AHEAD_BY` / `BEHIND_BY` : nombre de commits compares a `origin/sot/mainline`
- `CANON_STATUS` : statut courant de conservation ou de revue
- `ACTION` : geste operatoire recommande a partir du statut courant
- `LAST_REVIEW_GO` : GO de classement le plus recent, ou baseline initiale `GO_GIT_BRANCH_STATE_CANON_CREATE_01`

## Tableau canonique

| BRANCH | SCOPE | STATUS_VS_SOT_MAINLINE | AHEAD_BY | BEHIND_BY | CANON_STATUS | ACTION | JUSTIFICATION | LAST_REVIEW_GO |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | remote | DIVERGED | 9 | 21 | `KEEP_ACTIVE` | `keep_under_review` | Parent AI team architecture encore vivant cote branche | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `METHODE_MULTI_MACHINE_GIT_SYNC` | remote | DIVERGED | 14 | 32 | `REVIEW` | `manual_review` | Nouvelle branche distante observee pendant le prune, hors sous-lot courant, a auditer separement | `GO_GIT_GITHUB_PARK_CLOSEOUT_ABSORBED_RECLASS_01` |
| `audit/opt-trading-20260320a` | remote | DIVERGED | 20 | 615 | `REVIEW` | `manual_review` | Famille sensible a revue manuelle obligatoire | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `backup/mimo-b038db9` | local | DIVERGED | 18 | 625 | `KEEP_SNAPSHOT` | `exclude_cleanup` | Snapshot local de reprise MiMo | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `doc/GO_OPENCLAW_INFRA_BASELINE_01` | remote | DIVERGED | 1 | 261 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `docs/chatgpt-profile-baseline-index-01` | remote | ABSORBED | 0 | 44 | `ABSORBED` | `review_for_drop` | Branche deja absorbee dans origin/sot/mainline | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `docs/github-park-parent-closeout-01` | remote | DIVERGED | 1 | 60 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `docs/github-park-pass-close-01` | remote | DIVERGED | 4 | 60 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `docs/memory-bricks-localcms-contract-alignment-01` | remote | DIVERGED | 5 | 61 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `docs/skills-usage-cross-review-01` | remote | DIVERGED | 1 | 60 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `docs/tmux-opencode-openclaw-runtime-01` | remote | DIVERGED | 1 | 60 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `feat/GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01` | remote | DIVERGED | 13 | 251 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `feat/go-strategy-docs-v1` | remote | DIVERGED | 1 | 661 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `feat/journal-full-reading-macro-plan-recenter` | local | DIVERGED | 3 | 77 | `DROP_LOCAL_ONLY` | `review_or_drop_local` | Branche seulement locale non canonisee sur origin | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `feat/memory-bricks-v2-find` | remote | DIVERGED | 1 | 458 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `feat/memory-bricks-v2-health-status` | remote | DIVERGED | 1 | 528 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `feat/memory-bricks-v2-health-status-clean` | remote | DIVERGED | 1 | 441 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `feat/mimo-open-observer-market-calendar-v1` | local | ABSORBED | 0 | 550 | `DROP_LOCAL_ONLY` | `review_or_drop_local` | Branche locale restante apres suppression remote du sous-lot Mimo / misc | `GO_GIT_MIMO_MISC_ABSORBED_RECLASS_01` |
| `feat/mimo-open-observer-doc-pack-v0` | remote | DIVERGED | 22 | 847 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `feat/mimo-open-observer-doc-pack-v0-clean-local` | local | ABSORBED | 0 | 571 | `DROP_LOCAL_ONLY` | `review_or_drop_local` | Branche seulement locale non canonisee sur origin | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `feat/mimo-open-observer-doc-pack-v0-clean-working` | local | DIVERGED | 2 | 573 | `DROP_LOCAL_ONLY` | `review_or_drop_local` | Branche seulement locale non canonisee sur origin | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `feat/project-card-module-contextuals-shell-01` | remote | DIVERGED | 1 | 146 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `feat/project-card-openclaw-01` | remote | DIVERGED | 1 | 146 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `feat/project-card-validated-prompt-factory-01` | remote | DIVERGED | 1 | 146 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `feat/range-strategy-v1-struct` | remote | ABSORBED | 0 | 166 | `ABSORBED` | `review_for_drop` | Branche deja absorbee dans origin/sot/mainline | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `feat/student-mimo-bitget-live-equity` | both | DIVERGED | 23 | 615 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `feat/student-mimo-qualification` | both | DIVERGED | 21 | 615 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `feat/student-validation-bitget-readonly-01` | local | ABSORBED | 0 | 28 | `DROP_LOCAL_ONLY` | `review_or_drop_local` | Branche seulement locale non canonisee sur origin | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `go_repos_agent-role_initial_01` | remote | DIVERGED | 1 | 21 | `KEEP_REFERENCE` | `exclude_cleanup` | Branche de reference pour le parent AI team architecture | `GO_GIT_GO_REPOS_AGENT_ROLE_INITIAL_CLASSIFICATION_01` |
| `integ/trading-dual-stack-doc-pack-01` | remote | DIVERGED | 4 | 522 | `REVIEW` | `manual_review` | Famille sensible a revue manuelle obligatoire | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `inventory/collectors-baseline-01` | remote | DIVERGED | 6 | 361 | `REVIEW` | `manual_review` | Famille sensible a revue manuelle obligatoire | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `main` | both | DIVERGED | 3 | 847 | `REDUNDANT` | `review_alignment` | Tronc historique secondaire en divergence avec le canon sot/mainline | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `opencode/shiny-engine` | local | ABSORBED | 0 | 532 | `DROP_LOCAL_ONLY` | `review_or_drop_local` | Branche seulement locale non canonisee sur origin | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `promo/mimo-v2-bounded-01` | remote | DIVERGED | 3 | 364 | `REVIEW` | `manual_review` | Branche non absorbee ou divergente a reclassifier explicitement | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `save/admin-trading-2026-04-01` | remote | DIVERGED | 27 | 625 | `KEEP_SNAPSHOT` | `exclude_cleanup` | Branche snapshot nommee save/* a conserver jusqu a arbitrage explicite | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `save/admin-trading-post-reset-2026-04-04` | remote | DIVERGED | 1 | 409 | `KEEP_SNAPSHOT` | `exclude_cleanup` | Branche snapshot nommee save/* a conserver jusqu a arbitrage explicite | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `save/admin-trading-pre-reset-deskpro-2026-04-04` | remote | DIVERGED | 6 | 528 | `KEEP_SNAPSHOT` | `exclude_cleanup` | Branche snapshot nommee save/* a conserver jusqu a arbitrage explicite | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `save/admin-trading-pre-reset-git-fleet-2026-04-04` | remote | DIVERGED | 8 | 528 | `KEEP_SNAPSHOT` | `exclude_cleanup` | Branche snapshot nommee save/* a conserver jusqu a arbitrage explicite | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `save/cursor-ai-2026-04-01` | remote | DIVERGED | 1 | 598 | `KEEP_SNAPSHOT` | `exclude_cleanup` | Branche snapshot nommee save/* a conserver jusqu a arbitrage explicite | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `save/db-layer-2026-04-01` | remote | DIVERGED | 1 | 701 | `KEEP_SNAPSHOT` | `exclude_cleanup` | Branche snapshot nommee save/* a conserver jusqu a arbitrage explicite | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `save/fantome-YYYY-MM-DD` | remote | DIVERGED | 1 | 552 | `KEEP_SNAPSHOT` | `exclude_cleanup` | Branche snapshot nommee save/* a conserver jusqu a arbitrage explicite | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `save/student-2026-04-01` | remote | DIVERGED | 22 | 615 | `KEEP_SNAPSHOT` | `exclude_cleanup` | Branche snapshot nommee save/* a conserver jusqu a arbitrage explicite | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `sot/build` | remote | ABSORBED | 0 | 815 | `ABSORBED` | `review_for_drop` | Branche deja absorbee dans origin/sot/mainline | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |
| `sot/mainline` | both | SELF | 0 | 0 | `KEEP_ACTIVE` | `protect_mainline` | Tronc canonique de continuite | `GO_GIT_BRANCH_STATE_CANON_CREATE_01` |

## Journal minimal

- creation du support canonique `docs/index/BRANCH_STATE.md`
- branche conservee explicitement hors cleanup : `origin/go_repos_agent-role_initial_01` -> `KEEP_REFERENCE` via `GO_GIT_GO_REPOS_AGENT_ROLE_INITIAL_CLASSIFICATION_01`
- branche absorbee puis supprimee du remote : `origin/doc/GO_OPENCLAW_STATE_DIR_REPAIR_10` -> correction doc-only en `DROP_REMOTE_CANDIDATE`, suppression executee, donc absente du tableau courant
- branche d'isolation supprimee du remote : `origin/codex/reseau-ssh-runtime-compat-retirement-01-isolate`, absente du tableau courant apres `fetch --prune`
- branche reclassifiee sans suppression dans ce passage : `origin/doc/GO_OPENCLAW_STATE_DIR_READ_09` -> `DROP_REMOTE_CANDIDATE` via `GO_GIT_OPENCLAW_STATE_DIR_READ_09_CLASSIFICATION_01`
- branche absorbee puis supprimee du remote : `origin/doc/GO_OPENCLAW_STATE_DIR_READ_09` -> reclassification doc-only deja publiee, suppression executee, donc absente du tableau courant
- sous-lot OpenClaw absorbe reclassifie sans suppression dans ce passage : `docs/go-openclaw-evidence-01-v1`, `docs/openclaw-alignment-decision-07`, `docs/openclaw-alignment-exception-08`, `docs/openclaw-alignment-read-06`, `docs/openclaw-policy-runtime-alignment-05`, `docs/openclaw-state-dir-vigilance-03`, `go/openclaw-sync-02-doc` -> `DROP_REMOTE_CANDIDATE` via `GO_GIT_OPENCLAW_ABSORBED_SUBLOT_RECLASS_01`
- sous-lot GitHub park / closeout absorbe reclassifie sans suppression dans ce passage : `closeout/collectors-lifecycle-compat-01`, `docs/github-park-audit-expansion-closeout-01`, `docs/github-park-branch-trunk-cross-audit-01` -> `DROP_REMOTE_CANDIDATE` via `GO_GIT_GITHUB_PARK_CLOSEOUT_ABSORBED_RECLASS_01`
- sous-lot GitHub park / closeout absorbe puis supprime du remote : `closeout/collectors-lifecycle-compat-01`, `docs/github-park-audit-expansion-closeout-01`, `docs/github-park-branch-trunk-cross-audit-01` -> reclassification doc-only deja publiee, suppression executee, donc lignes retirees du tableau courant
- nouvelle branche distante observee pendant `fetch --prune` : `origin/METHODE_MULTI_MACHINE_GIT_SYNC` -> entree ajoutee avec statut `REVIEW` en attente d'audit separe
- sous-lot Hermes absorbe reclassifie sans suppression dans ce passage : `docs/hermes-openclaw-bridge-05-closeout-01`, `docs/hermes-openclaw-exec01-result-01`, `docs/hermes-result-case01-v1` -> `DROP_REMOTE_CANDIDATE` via `GO_GIT_HERMES_ABSORBED_RECLASS_01`
- sous-lot Hermes absorbe puis supprime du remote : `docs/hermes-openclaw-bridge-05-closeout-01`, `docs/hermes-openclaw-exec01-result-01`, `docs/hermes-result-case01-v1` -> reclassification doc-only deja publiee, suppression executee, donc lignes retirees du tableau courant
- sous-lot Simex absorbe reclassifie sans suppression dans ce passage : `docs/index-simex-link-01`, `docs/simex-presets-01`, `feat/admin-trading-simex-insufficient-candles-evidence-closeout-01`, `feat/admin-trading-simex-insufficient-candles-hardening-01`, `feat/admin-trading-simex-runtime-evidence-closeout-01`, `feat/admin-trading-simex-upstream-failure-hardening-01`, `feat/admin-trading-simex-upstream-hardening-evidence-closeout-01`, `feat/admin-trading-simex-upstream-hardening-evidence-upgrade-01`, `feat/fantome-simex-module-durable-01`, `feat/simex-env-bridge-01`, `feat/simex-units-contract-01`, `feat/simex-wrappers-01` -> `DROP_REMOTE_CANDIDATE` via `GO_GIT_SIMEX_ABSORBED_RECLASS_01`
- sous-lot Simex absorbe puis supprime du remote : `docs/index-simex-link-01`, `docs/simex-presets-01`, `feat/admin-trading-simex-insufficient-candles-evidence-closeout-01`, `feat/admin-trading-simex-insufficient-candles-hardening-01`, `feat/admin-trading-simex-runtime-evidence-closeout-01`, `feat/admin-trading-simex-upstream-failure-hardening-01`, `feat/admin-trading-simex-upstream-hardening-evidence-closeout-01`, `feat/admin-trading-simex-upstream-hardening-evidence-upgrade-01`, `feat/fantome-simex-module-durable-01`, `feat/simex-env-bridge-01`, `feat/simex-units-contract-01`, `feat/simex-wrappers-01` -> reclassification doc-only deja publiee, suppression executee, donc lignes retirees du tableau courant
- sous-lot Product / cards / session absorbe reclassifie sans suppression dans ce passage : `feat/product-target-canon`, `feat/project-card-bot-vision-ingestion-01`, `feat/project-card-trading-analytics-chain-01`, `feat/project-cards-canonical-alignment-01`, `feat/project-cards-gate-alignment-01`, `feat/project-portfolio-validated-plans-freeze-01`, `feat/session-documentation-gate`, `feat/docs-index-chantier-inventory-sync-01`, `feat/OT_DESKPRO_RELEASE_OPS_DRILL_01` -> `DROP_REMOTE_CANDIDATE` via `GO_GIT_PRODUCT_CARDS_SESSION_ABSORBED_RECLASS_01`
- sous-lot Product / cards / session absorbe puis supprime du remote : `feat/product-target-canon`, `feat/project-card-bot-vision-ingestion-01`, `feat/project-card-trading-analytics-chain-01`, `feat/project-cards-canonical-alignment-01`, `feat/project-cards-gate-alignment-01`, `feat/project-portfolio-validated-plans-freeze-01`, `feat/session-documentation-gate`, `feat/docs-index-chantier-inventory-sync-01`, `feat/OT_DESKPRO_RELEASE_OPS_DRILL_01` -> reclassification doc-only deja publiee, suppression executee, donc lignes retirees du tableau courant
- sous-lot Runtime / engine / helpers absorbe reclassifie sans suppression dans ce passage : `feat/engines-plugin`, `feat/execution-engine`, `feat/persistent-state`, `feat/position-engine`, `feat/position-guard`, `feat/student-ops-helpers-01`, `feat/trading-realtime-v1-event-bridge`, `feat/trading-realtime-v1-export`, `feat/trading-realtime-v1-guardrails`, `feat/trading-realtime-v1-reporting`, `feat/trading-realtime-v1-runtime-loop`, `feat/trading-realtime-v1-timer`, `feature/hf-publish-helper-fix-01`, `feature/hf-tools-private-config-fix-01` -> `DROP_REMOTE_CANDIDATE` via `GO_GIT_RUNTIME_ENGINE_HELPERS_ABSORBED_RECLASS_01`
- sous-lot Runtime / engine / helpers absorbe puis supprime du remote : `feat/engines-plugin`, `feat/execution-engine`, `feat/persistent-state`, `feat/position-engine`, `feat/position-guard`, `feat/student-ops-helpers-01`, `feat/trading-realtime-v1-event-bridge`, `feat/trading-realtime-v1-export`, `feat/trading-realtime-v1-guardrails`, `feat/trading-realtime-v1-reporting`, `feat/trading-realtime-v1-runtime-loop`, `feat/trading-realtime-v1-timer`, `feature/hf-publish-helper-fix-01`, `feature/hf-tools-private-config-fix-01` -> reclassification doc-only deja publiee, suppression executee, donc lignes retirees du tableau courant
- sous-lot Mimo / misc absorbe reclassifie sans suppression dans ce passage : `feat/antigravity-binance-v1`, `feat/cards01`, `feat/collectors-lifecycle-wrapper-harmonization-01`, `feat/go-openclaw-chain-03-v1`, `feat/memory-bricks-v2-bricks-list`, `feat/mimo-gate-replay`, `feat/mimo-open-observer-doc-pack-v0-clean`, `feat/mimo-open-observer-market-calendar-v1`, `feat/mimo-scheduler-promotion`, `feat/openclaw-registry-expose-01` -> `DROP_REMOTE_CANDIDATE` via `GO_GIT_MIMO_MISC_ABSORBED_RECLASS_01`
- sous-lot Mimo / misc absorbe puis supprime du remote : `feat/antigravity-binance-v1`, `feat/cards01`, `feat/collectors-lifecycle-wrapper-harmonization-01`, `feat/go-openclaw-chain-03-v1`, `feat/memory-bricks-v2-bricks-list`, `feat/mimo-gate-replay`, `feat/mimo-open-observer-doc-pack-v0-clean`, `feat/mimo-open-observer-market-calendar-v1`, `feat/mimo-scheduler-promotion`, `feat/openclaw-registry-expose-01` -> suppression remote executee; seule la branche locale `feat/mimo-open-observer-market-calendar-v1` reste au tableau
- reliquat OpenClaw `DROP_REMOTE_CANDIDATE` supprime du remote : `docs/go-openclaw-evidence-01-v1`, `docs/openclaw-alignment-decision-07`, `docs/openclaw-alignment-exception-08`, `docs/openclaw-alignment-read-06`, `docs/openclaw-policy-runtime-alignment-05`, `docs/openclaw-state-dir-vigilance-03`, `go/openclaw-sync-02-doc` -> suppression executee, donc lignes retirees du tableau courant

## Point de reprise

Pour toute nouvelle session de housekeeping :
- repartir de `docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md`
- charger d'abord `docs/index/BRANCH_STATE.md`
- verifier le delta Git reel depuis la date et le commit de reference
- mettre a jour cette fiche avant toute suppression effective
