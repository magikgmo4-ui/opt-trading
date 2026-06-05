---
doc_id: OPT_TRADING_BRANCH_PROJECT_MAP_01
doc_type: index
repo: opt-trading
project: opt-trading
status: reference
lifecycle_stage: continuity_index
topic_keys:
  - git
  - branches
  - projects
  - continuity
  - housekeeping
surface: index
source_kind: canonical
updated_at: 2026-04-23
links:
  - docs/index/BRANCH_STATE.md
  - docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md
  - docs/index/GO_INDEX.md
---

# BRANCH_PROJECT_MAP

## Objet

Cette fiche associe les branches du repo `opt-trading` a des projets ou familles de travail.

Elle sert a :
- rendre le parc branches lisible par projet
- distinguer les branches restantes des branches supprimees dans le cycle de housekeeping
- reduire les reclassements approximatifs d'une session a l'autre
- completer `docs/index/BRANCH_STATE.md` par une lecture orientee projet

## Source de verite

La source canonique de statut reste :
- `docs/index/BRANCH_STATE.md`

Cette fiche n'en est qu'une vue projet/famille.

## Regle de maintenance

- toute nouvelle branche significative doit etre associee a un projet/famille ici
- toute suppression executee et tracee dans `BRANCH_STATE.md` doit etre reportee ici
- si l'association n'est pas prouvee, classer en `INCONNUE`
- utiliser une colonne `CONFIDENCE` :
  - `HIGH` = preuve forte (nommage + doc repo + PR mergee)
  - `MEDIUM` = nommage + contexte repo cohérents
  - `LOW` = hypothese prudente
- cette fiche doit rester synchronisee avec `docs/index/BRANCH_STATE.md`

## 1) Branches restantes par projet/famille

| PROJET_FAMILLE | BRANCHES_RESTANTES | CONFIDENCE | BASE |
| --- | --- | --- | --- |
| `AI_TEAM_ARCHITECTURE` | `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`, `go_repos_agent-role_initial_01` | `HIGH` | nommage + doc canon + classement KEEP |
| `OPENCLAW` | `doc/GO_OPENCLAW_INFRA_BASELINE_01`, `docs/tmux-opencode-openclaw-runtime-01`, `feat/project-card-openclaw-01` | `HIGH` | nommage + PR #127 + docs OpenClaw |
| `MEMORY_BRICKS_LOCALCMS` | `docs/memory-bricks-localcms-contract-alignment-01`, `feat/memory-bricks-v2-find`, `feat/memory-bricks-v2-health-status`, `feat/memory-bricks-v2-health-status-clean` | `HIGH` | nommage + famille projet explicite |
| `VALIDATED_PROMPT_FACTORY_CONTEXTUALS` | `feat/project-card-module-contextuals-shell-01`, `feat/project-card-validated-prompt-factory-01` | `HIGH` | PR #128, #129 |
| `MIMO_OPENOBSERVER_STUDENT` | `backup/mimo-b038db9`, `feat/mimo-open-observer-doc-pack-v0`, `feat/student-mimo-bitget-live-equity`, `feat/student-mimo-qualification`, `promo/mimo-v2-bounded-01` | `HIGH` | nommage + continuite session |
| `TRADING_ANALYTICS_COLLECTORS` | `feat/go-strategy-docs-v1`, `integ/trading-dual-stack-doc-pack-01`, `inventory/collectors-baseline-01` | `MEDIUM` | nommage + continuum trading/collectors |
| `GOVERNANCE_GIT_HOUSEKEEPING` | `METHODE_MULTI_MACHINE_GIT_SYNC`, `audit/opt-trading-20260320a`, `docs/github-park-parent-closeout-01`, `docs/github-park-pass-close-01`, `docs/skills-usage-cross-review-01`, `feat/GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01`, `main`, `sot/build`, `sot/mainline` | `HIGH` | nommage + role repo/continuite |
| `SNAPSHOTS_MACHINE` | `save/admin-trading-2026-04-01`, `save/admin-trading-post-reset-2026-04-04`, `save/admin-trading-pre-reset-deskpro-2026-04-04`, `save/admin-trading-pre-reset-git-fleet-2026-04-04`, `save/cursor-ai-2026-04-01`, `save/db-layer-2026-04-01`, `save/fantome-YYYY-MM-DD`, `save/student-2026-04-01` | `HIGH` | prefixe `save/*` explicite |

## 2) Branches supprimees dans le cycle housekeeping publie, par projet/famille

| PROJET_FAMILLE | BRANCHES_SUPPRIMEES | CONFIDENCE | BASE |
| --- | --- | --- | --- |
| `OPENCLAW` | `doc/GO_OPENCLAW_STATE_DIR_REPAIR_10`, `doc/GO_OPENCLAW_STATE_DIR_READ_09`, `docs/go-openclaw-evidence-01-v1`, `docs/openclaw-alignment-decision-07`, `docs/openclaw-alignment-exception-08`, `docs/openclaw-alignment-read-06`, `docs/openclaw-policy-runtime-alignment-05`, `docs/openclaw-state-dir-vigilance-03`, `go/openclaw-sync-02-doc`, `feat/openclaw-registry-expose-01`, `feat/go-openclaw-chain-03-v1` | `HIGH` | journal `BRANCH_STATE` + PR #45 + PR #81 |
| `HERMES_OPENCLAW_RESULTS` | `docs/hermes-openclaw-bridge-05-closeout-01`, `docs/hermes-openclaw-exec01-result-01`, `docs/hermes-result-case01-v1` | `HIGH` | nommage explicite |
| `GITHUB_PARK_GOVERNANCE` | `closeout/collectors-lifecycle-compat-01`, `docs/github-park-audit-expansion-closeout-01`, `docs/github-park-branch-trunk-cross-audit-01`, `docs/chatgpt-profile-baseline-index-01`, `codex/reseau-ssh-runtime-compat-retirement-01-isolate` | `HIGH` | journal `BRANCH_STATE` + PR #152 |
| `SIMEX_DERIVATIVES_COLLECTORS` | `docs/index-simex-link-01`, `docs/simex-presets-01`, `feat/admin-trading-simex-insufficient-candles-evidence-closeout-01`, `feat/admin-trading-simex-insufficient-candles-hardening-01`, `feat/admin-trading-simex-runtime-evidence-closeout-01`, `feat/admin-trading-simex-upstream-failure-hardening-01`, `feat/admin-trading-simex-upstream-hardening-evidence-closeout-01`, `feat/admin-trading-simex-upstream-hardening-evidence-upgrade-01`, `feat/fantome-simex-module-durable-01`, `feat/simex-env-bridge-01`, `feat/simex-units-contract-01`, `feat/simex-wrappers-01`, `feat/collectors-lifecycle-wrapper-harmonization-01`, `feat/antigravity-binance-v1` | `HIGH` | journal `BRANCH_STATE` + PR #19 + PR #82 |
| `PRODUCT_CARDS_PORTFOLIO_DESKPRO_ANALYTICS_BOTVISION` | `feat/product-target-canon`, `feat/project-card-bot-vision-ingestion-01`, `feat/project-card-trading-analytics-chain-01`, `feat/project-cards-canonical-alignment-01`, `feat/project-cards-gate-alignment-01`, `feat/project-portfolio-validated-plans-freeze-01`, `feat/session-documentation-gate`, `feat/docs-index-chantier-inventory-sync-01`, `feat/OT_DESKPRO_RELEASE_OPS_DRILL_01` | `HIGH` | journal `BRANCH_STATE` + PR #120 + PR #124 + PR #125 + PR #126 |
| `ENGINE_RUNTIME_HELPERS_HF` | `feat/engines-plugin`, `feat/execution-engine`, `feat/persistent-state`, `feat/position-engine`, `feat/position-guard`, `feat/student-ops-helpers-01`, `feat/trading-realtime-v1-event-bridge`, `feat/trading-realtime-v1-export`, `feat/trading-realtime-v1-guardrails`, `feat/trading-realtime-v1-reporting`, `feat/trading-realtime-v1-runtime-loop`, `feat/trading-realtime-v1-timer`, `feature/hf-publish-helper-fix-01`, `feature/hf-tools-private-config-fix-01` | `MEDIUM` | nommage coherent + journal `BRANCH_STATE` |
| `MIMO_OPENOBSERVER_STUDENT` | `feat/mimo-gate-replay`, `feat/mimo-open-observer-doc-pack-v0-clean`, `feat/mimo-open-observer-market-calendar-v1`, `feat/mimo-scheduler-promotion`, `feat/student-validation-bitget-readonly-01`, `feat/mimo-open-observer-doc-pack-v0-clean-local`, `feat/mimo-open-observer-doc-pack-v0-clean-working` | `HIGH` | nommage explicite + journal `BRANCH_STATE` |
| `MEMORY_BRICKS` | `feat/memory-bricks-v2-bricks-list` | `HIGH` | nommage explicite |
| `STRATEGY` | `feat/range-strategy-v1-struct` | `HIGH` | nommage explicite |
| `INCONNUE` | `feat/cards01`, `feat/journal-full-reading-macro-plan-recenter`, `opencode/shiny-engine` | `LOW` | preuves repo/PR insuffisantes pour mieux figer |

## 3) Familles/projets presents dans le repo ou la continuite, mais sans branche restante evidente

| PROJET_FAMILLE | ETAT | BASE |
| --- | --- | --- |
| `DESKPRO` | present dans la doc / sans branche restante evidente | PR #124 |
| `BOT_VISION_INGESTION` | present dans la doc / sans branche restante evidente | PR #126 |
| `TRADING_ANALYTICS_CHAIN` | present dans la doc / sans branche restante evidente | PR #125 |
| `VALIDATED_PROMPT_FACTORY` | present dans la doc / sans branche restante evidente hors project-card | PR #128 |
| `MODULE_CONTEXTUALS_SHELL` | present dans la doc / sans branche restante evidente hors project-card | PR #129 |
| `PORTFOLIO_FREEZE_PROJECT_CARDS` | present dans la doc / sans branche restante evidente | PR #120 |
| `RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT` | present dans la doc / sans branche restante evidente | PR #152 |

## 4) Cas encore faibles / a ne pas sur-interpreter

| BRANCH | CLASSEMENT_RETENU | CONFIDENCE | NOTE |
| --- | --- | --- | --- |
| `feat/cards01` | `INCONNUE` | `LOW` | nom trop court, aucune PR/trace probante retrouvee |
| `feat/journal-full-reading-macro-plan-recenter` | `INCONNUE` | `LOW` | probablement doc/methode, mais preuve repo insuffisante |
| `opencode/shiny-engine` | `INCONNUE` | `LOW` | probablement tooling/IDE, mais preuve repo insuffisante |

## 5) Point de reprise

Pour toute suite sur cette cartographie :
1. relire `docs/index/BRANCH_STATE.md`
2. recroiser avec l'etat Git reel
3. ajuster ici seulement si le classement projet/famille change reellement
4. ne pas surclasser un cas faible sans preuve repo/PR/documentaire

## 6) Resume operatoire

- les branches restantes sont maintenant presque entierement lisibles par projet
- les branches supprimees du cycle housekeeping sont rattachees a des familles stables
- il reste 3 cas faibles a conserver explicitement en `INCONNUE`

## RISKS

- À qualifier.
