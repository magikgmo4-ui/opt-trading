---
doc_id: ADMIN_TRADING_BRANCH_DOC_RECONCILIATION_10
doc_type: reconciliation_table
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BRANCH_DOC_RECONCILIATION_01
status: active
surface: chantier
updated_at: 2026-05-14
---

# 10_RECONCILIATION — Tableau de recroisement

## Sources croisées

| Source | Nb entrées | Note |
| --- | ---: | --- |
| MACHINE_WORK_SPLIT bloc ADMIN_TRADING | 25 | Vue routage documentée |
| BRANCH_STATE.md (entrées GO_OPT_TRADING_ADMIN_TRADING_*) | 0 | Absence totale |
| Remote GitHub (origin/go/GO_OPT_TRADING_ADMIN_TRADING_*) | 54 | Branches réelles |
| Remote GitHub (origin/go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_*) | 6 | Branches TMUX_IDE liées |
| Chantiers locaux (docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_*) | 73 | Dossiers chantiers existants |

## Classification des branches ADMIN_TRADING

### ACTIVE — branches avec chantier actif documenté ou runtime en cours

| Branche | Chantier local | Note |
| --- | --- | --- |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_STEADY_STATE_FIRST_14D_REVIEW_01` | Oui | **Point actif principal** — PENDING_OBSERVATION jusqu'au 2026-05-28 |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_STEADY_STATE_OPERATIONS_POLICY_01` | Oui | Politique ops associée à la fenêtre 14d |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_PHASE_2_STABILITY_GATE_01` | Oui | Gate post-expansion |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_PHASE_2_EXECUTION_01` | Oui | Execution phase 2 |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_PLAN_01` | Oui | Plan expansion |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_READINESS_REVIEW_01` | Oui | Readiness review |
| `DESK_PRO_AUTOMATION_OBSERVABILITY_01` | Oui | Observabilité active |
| `DESK_PRO_AUTOMATION_TIMER_IMPL_01` | Oui | Timer impl — runtime |
| `DESK_PRO_AUTOMATION_TIMER_INSTALL_GATED_01` | Oui | Timer install gated |
| `DESK_PRO_AUTOMATION_TIMER_START_GATED_01` | Oui | Timer start |
| `DESK_PRO_AUTOMATION_TIMER_PAYLOAD_FIX_01` | Oui | Timer payload fix |
| `DESK_PRO_AUTOMATION_TIMER_SPEC_01` | Oui | Timer spec |
| `DESK_PRO_AUTOMATION_TIMER_STABILITY_WINDOW_01` | Oui | Timer stability |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_CONTROLLED_PILOT_EXECUTION_01` | Oui | Controlled pilot (history) |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_LIMITED_PRODUCTION_EXECUTION_01` | Oui | Limited prod exec |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_LIMITED_PRODUCTION_PLAN_01` | Oui | Limited prod plan |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_EXECUTION_01` | Oui | Prod expansion exec |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_PHASE_1_STABILITY_GATE_01` | Oui | Phase 1 stability gate |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_SMOKE_EXECUTION_01` | Oui | Smoke exec |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_SMOKE_PLAN_01` | Oui | Smoke plan |
| `DESK_PRO_AUTOMATION_PLAN_01` | Oui | Plan global automation |
| `DESK_PRO_AUTOMATION_SIGNAL_EVENT_INPUT_01` | Oui | Signal event input |
| `DESK_PRO_AUTOMATION_INPUT_ENRICHMENT_PLAN_01` | Oui | Input enrichment plan |
| `DESK_PRO_AUTOMATION_INPUT_SEQUENCE_CLOSEOUT_01` | Oui | Input sequence closeout |
| `DESK_PRO_AUTOMATION_COMBINED_INPUT_SMOKE_01` | Oui | Combined input smoke |
| `DESK_PRO_AUTOMATION_DESK_SNAPSHOT_INPUT_01` | Oui | Desk snapshot input |
| `DESK_PRO_AUTOMATION_VISUAL_CONTEXT_INPUT_01` | Oui | Visual context input |
| `DESK_PRO_AUTOMATION_DRY_RUN_IMPL_01` | Oui | Dry run impl |
| `DESK_PRO_AUTOMATION_FIRST_TRIGGER_OBSERVE_01` | Oui | First trigger observe |
| `DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01` | Oui | Artifact observe |
| `DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01` | Oui | Artifact output |
| `DESK_PRO_AUTOMATION_ARTIFACT_STABILITY_WINDOW_01` | Oui | Artifact stability window |
| `DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_REVIEW_MERGE_01` | Oui | Artifact observe review merge |
| `DESK_PRO_AUTOMATION_ARTIFACT_SEQUENCE_CLOSEOUT_01` | Oui | Artifact sequence closeout |
| `DESK_PRO_AUTOMATION_SEQUENCE_CLOSEOUT_01` | Oui | Sequence closeout |
| `BRIDGE_GUARD_ADD_01` | Oui | Bridge guard — hardening |
| `CHILD_BOT_VISION_HEADLESS_IMPL_01` | Oui | Headless impl |
| `CHILD_BOT_VISION_HEADLESS_SYSTEMD_01` | Oui | Headless systemd |
| `CHILD_BOT_VISION_HEADLESS_DESK_BRIDGE_INTEGRATION_SMOKE_01` | Oui | Bridge integration smoke |
| `CHILD_BOT_VISION_HEADLESS_CLOSEOUT_01` | Oui | Headless closeout |
| `PAPER_TEST_GATE_01` | Oui | Paper test gate |
| `PAPER_TEST_EXECUTION_01` | Oui | Paper test exec |
| `PAPER_POSITION_CLOSE_01` | Oui | Paper position close |
| `PAPER_FLAGS_CONFIG_01` | Oui | Paper flags config |
| `PAPER_SCENARIOS_EXPANSION_01` | Oui | Paper scenarios |
| `PAPER_TEST_EXECUTION_RETRY_01` | Oui | Paper exec retry |
| `PAPER_TEST_RETRY_01` | Oui | Paper test retry |
| `PAPER_TEST_RUNTIME_GUARDS_FIX_01` | Oui | Paper runtime guards fix |
| `PAPER_VALIDATION_GLOBAL_CLOSEOUT_01` | Oui | Paper validation closeout |
| `PAPER_TEST_CYCLE_CLOSEOUT_01` | Oui | Paper cycle closeout |
| `PRODUCTION_MONITORING_AND_SECRETS_AUDIT_01` | Oui | Prod monitoring |
| `PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_01` | Oui | Risk limits (partially impl) |
| `PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_IMPL_01` | Oui | Risk limits impl |
| `PRODUCTION_READINESS_CONDITIONS_01` | Oui | Readiness conditions |
| `RUNTIME_SYNC_AFTER_PAPER_GUARDS_01` | Oui | Runtime sync |
| `DESK_PRO_RUNTIME_REVIEW_REPRISE_01` | Oui | Runtime review reprise |
| `DESK_PRO_AGENT_STANDARD_NEED_VALIDATION_01` | Oui | Agent standard validation |
| `DESK_PRO_ARTIFACT_STABILITY_POST_MERGE_SYNC_01` | Oui | Post-merge sync |
| `DESK_PRO_SCHEMA_ADAPTER_01` | Oui | Schema adapter |
| `CONTRACT_COMPATIBILITY_SMOKE_01` | Oui | Contract compatibility smoke |
| `WEBHOOK_RUNTIME_REVIEW_REPRISE_01` | Oui | Webhook runtime review reprise |
| `WEBHOOK_SIGNAL_DIAG_REPRISE_01` | Oui | Webhook signal diag reprise |
| `TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01` | Oui | Telegram webhook real usage test |
| `TELEGRAM_NOTIFICATION_ENABLE_TEST_01` | Oui | Telegram notification enable |
| `TELEGRAM_NOTIFICATION_EXECUTE_TEST_01` | Oui | Telegram notification execute |
| `TELEGRAM_NOTIFICATION_EXECUTION_RESULTS_01` | Oui | Telegram notification results |
| `TV_TEST_RUNTIME_CONFIG_CANONICALIZE_01` | Oui | TV test runtime config |
| `TRADINGVIEW_ALERT_EXTERNAL_CHECK_01` | Oui | TradingView alert check |
| `BOT_VISION_HEADLESS_PIPELINE_REVIEW_01` | Oui | Pipeline review |
| `PARENT_REVIEW_01` | Oui | Parent review |
| `PARENT_SEQUENCE_CLOSEOUT_01` | Oui | Parent sequence closeout |
| `MACHINE_ADMIN_TRADING_PARENT_01` | Oui | Parent machine admin-trading |

### ACTIVE — TMUX_IDE (branches TMUX liées à admin-trading)

| Branche | Chantier local | Note |
| --- | --- | --- |
| `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01` | Oui | TMUX IDE arbitration |
| `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01` | Oui | Git base realign |
| `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01` | Oui | Git base realign exec |
| `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01` | Oui | Linux compat investigation |
| `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01` | Oui | TMUX IDE qualify |
| `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01` | Oui | TMUX IDE requalify |

### REFERENCE — branches mergees ou closeout, documentation conservee

| Branche | Note |
| --- | --- |
| `DESK_BRIDGE_RETRY_01` | Merge/absorbé — retry implémenté dans le flux bridge |
| `DESK_PRO_RUNTIME_REVIEW_01` | Mergé dans FIRST_14D_REVIEW ou absorbé dans la séquence automation |
| `DESK_PRO_SMOKE_01` | Smoke initial — absorbé dans la séquence DESK_PRO_AUTOMATION |
| `VISION_INBOX_REPAIR_01` | Réparation inbox — livrée, branche résiduelle |
| `TELEGRAM_WEBHOOK_TV_TEST_EXECUTION_CLOSEOUT_01` | TV_TEST closeout — doc clos |
| `CHILD_BOT_VISION_HEADLESS_PARENT_REALIGNMENT_01` | Realignment doc — merge attendu ou absorbé |
| `CHILD_BOT_VISION_HEADLESS_REVIEW_01` | Review doc — reference |
| `WEBHOOK_RUNTIME_REVIEW_01` | Webhook runtime review — mergée ou absorbée dans la reprise |
| `WEBHOOK_SIGNAL_DIAG_01` | Signal diag initial — mergée ou absorbée dans la reprise |

### DROP_MERGED — branches mergees dans sot/mainline, suppression possible

| Branche | Preuve | Action recommandée |
| --- | --- | --- |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_EXECUTION_01` | Closeout présent, contenu absorbé dans mainline | delete_local_and_remote |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_CONTROLLED_PILOT_EXECUTION_01` | Closeout présent | delete_local_and_remote |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_SMOKE_PLAN_01` | Absorbé dans séquence | delete_local_and_remote |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_SMOKE_EXECUTION_01` | Absorbé dans séquence | delete_local_and_remote |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_LIMITED_PRODUCTION_PLAN_01` | Absorbé | delete_local_and_remote |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_LIMITED_PRODUCTION_EXECUTION_01` | Absorbé | delete_local_and_remote |
| `DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_PHASE_1_STABILITY_GATE_01` | Gate passée | delete_local_and_remote |

Note: Ces classifications `DROP_MERGED` sont **proposées** par cette réconciliation. Leur exécution effective nécessite un GO de cleanup dédié hors scope de ce chantier doc-only.

### A_VERIFIER — besoins de verification supplementaire

| Branche | Raison |
| --- | --- |
| `GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01` | Présent dans MACHINE_WORK_SPLIT mais pas clairement admin-trading — vérifier appartenance machine |
| `GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01` | Présent dans MACHINE_WORK_SPLIT admin-trading — vérifier si rattachement correct ou si bloc STRATEGY |
| `GO_OPT_TRADING_WEB3_DATA_ADAPTERS_AUDIT_01` | Présent dans MACHINE_WORK_SPLIT admin-trading — vérifier appartenance machine |
| `GO_SKYAI_COMPETITORS_WEB3_AI_DATA_01` | Présent dans MACHINE_WORK_SPLIT admin-trading — vérifier appartenance machine |

## Écarts documentaires

### Surface doc vs realite Git

| Metrique | Valeur |
| --- | ---: |
| Entrees dans bloc MACHINE_WORK_SPLIT ADMIN_TRADING | 25 |
| Remote branches go/GO_OPT_TRADING_ADMIN_TRADING_* | 54 |
| Remote branches go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_* | 6 |
| Chantiers locaux ADMIN_TRADING | 73 |
| Entrees dans BRANCH_STATE.md pour ADMIN_TRADING | **0** |

### Constats

1. **MACHINE_WORK_SPLIT** est très en retard : 25 entrées vs 54 branches réelles. Manque toute la séquence DESK_PRO_AUTOMATION_*, PAPER_TEST_*, PRODUCTION_*.
2. **BRANCH_STATE.md** a zéro entrée pour les branches GO_OPT_TRADING_ADMIN_TRADING_*. Ces 54+ branches ne sont pas tracées dans l'index canonique des branches.
3. De nombreux chantiers locaux existent sans branche remote associée (ou inversement).
4. Les TMUX_IDE branches (6) sont listées dans aucun des deux index pour admin-trading.
