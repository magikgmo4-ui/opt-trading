---
doc_id: OPT_TRADING_MACHINE_WORK_SPLIT_ANTI_CONFLICT_01
doc_type: index
repo: opt-trading
project: opt-trading
status: reference
lifecycle_stage: continuity_index
topic_keys:
  - machines
  - routing
  - anti-collision
  - branches
  - continuity
  - work_split
surface: index
source_kind: canonical
updated_at: 2026-05-14
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/BRANCH_STATE.md
  - docs/index/BRANCH_PROJECT_MAP.md
  - docs/index/GO_INDEX.md
---

# MACHINE_WORK_SPLIT_ANTI_CONFLICT_01

## Objet

Cette fiche est la vue de routage machine anti-conflit du repo `opt-trading`.

Elle sert a :
- repondre aux demandes "chantiers pour <machine>" sans rearbitrage complet
- eviter les collisions Git entre machines
- offrir une lecture orientee machine du parc branches

## Source de verite

Cette fiche est une vue de routage machine, subordonnee a :
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- `docs/index/BRANCH_STATE.md`
- `docs/index/BRANCH_PROJECT_MAP.md`
- `docs/index/GO_INDEX.md`

La source canonique de statut branche reste `docs/index/BRANCH_STATE.md`.

## Regle de routage

Quand la demande est "chantiers pour <machine>", la reponse doit ressortir directement le bloc machine correspondant de cette fiche :

- "chantiers pour cursor-ai" => bloc **CURSOR_AI**
- "chantiers pour admin-trading" => bloc **ADMIN_TRADING**
- "chantiers pour db-layer" => bloc **DB_LAYER**
- "chantiers pour student" => bloc **STUDENT / OLLAMA**
- "chantiers pour fantome" => bloc **FANTOME**

## Regle de maintenance

- toute nouvelle branche rattachee a une machine doit etre ajoutee dans le bloc correspondant
- toute suppression executee et tracee dans `BRANCH_STATE.md` doit etre reportee ici
- ne pas promouvoir automatiquement une branche dans `GO_INDEX`
- une branche Git ne prouve pas seule un chantier actif
- cette fiche ne remplace pas `BRANCH_PROJECT_MAP.md` ni `GO_INDEX.md`
- cette fiche complete le routage machine

---

## Bloc CURSOR_AI

### DOC_OPS — WHY_LAYER_ACTIVE

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_CURSOR_AI_DOC_OPS_CHILD_WHY_LAYER_AUDIT_01` | WHY layer audit — doc-only ; rattache au parent cursor-ai ; aucun runtime ; aucun GO_INDEX |

### DOC_OPS — WHY_LINT_CONSOLIDATION_ACTIVE

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01` | WHY lint consolidation parent — doc-only ; read-only ; warning-only ; consolide gouvernance / WHY runtime / WHY lint / OpenClaw central ; interdits : runtime, auto-fix, global indexes, MCP live, trade, secret ; next : SPEC_WHY_LINT_EXPERIMENT_01.md |

### TradingView MCP Observer — CLOSED (transport/docs)

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01` | Parent — merged (PR #200), branche supprimee |
| `go/GO_OPT_TRADING_CURSOR_AI_TRADINGVIEW_OBSERVER_OPERATIONS_PARENT_01` | Operations parent — merged, branche supprimee |
| `go/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_POST_MERGE_REPRISE_01` | Post-merge reprise — merged, branche supprimee |
| `go/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_SHARED_PACKET_01` | Shared packet — merged, branche supprimee |
| `go/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_ALERT_WEBHOOK_TEMPLATE_01` | Template — merged, branche supprimee |
| `go/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_PARENT_CLOSEOUT_01` | Parent closeout — FERME (transport/docs) |

### alert_webhook — ACTIVE_CONTINUITY

| Element | Statut |
| --- | --- |
| `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_ALERT_WEBHOOK_APPLICATION_ACTIVE_01` | CONTINUITE ACTIVE (PR #203) — application non fermee |

### Bundles — APPLICATION_DOCUMENTED_NOT_PRODUCT_CLOSED

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01` | Bundles doc — merged, branche supprimee |
| `go/GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_IMPL_01` | Application operateur — merged (PR #202) |

### Live artifacts / Claude cowork — MERGED

| Branche | Note |
| --- | --- |
| `go/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01` | IDE bundle — merged (PR #201) |
| `go/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01` | Claude cowork parent — merged (PR #201) |

### DOC_OPS — HISTORICAL (branches supprimees en cleanup)

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_DOC_OPS_CHILD_ACTIVE_GOVERNANCE_CLOSEOUT_REVIEW_01` | HISTORICAL — supprimee L+R (cleanup) |
| `go/GO_OPT_TRADING_DOC_OPS_CHILD_CONTINUITY_ALIGNMENT_AFTER_OPEN_WORK_CONTROL_01` | HISTORICAL — supprimee L+R (cleanup) |
| `go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01_ISOLATED` | HISTORICAL — supprimee L+R (cleanup + worktree) |
| `go/GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01` | HISTORICAL — supprimee L+R (cleanup) |

### DOC_OPS — BLOCKED

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01` | BLOCKED — conservee, delta reseau_ssh non merge |

### CURSOR_AI — References audit Git

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_REMAINING_BRANCHES_TRANSPORT_DELETE_03` | Branches transport delete |
| `go/GO_OPT_TRADING_REMAINING_BRANCHES_TRANSPORT_DELETE_03_CANCEL_01` | Transport delete cancel |
| `go/GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_AUDIT_01` | Branches matrix audit |
| `go/GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_MEMBERSHIP_AUDIT_02` | Branches matrix membership audit |

---

## Bloc ADMIN_TRADING

### ACTIVE — Runtime actif

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_STEADY_STATE_FIRST_14D_REVIEW_01` | **Point actif principal** — PENDING_OBSERVATION jusqu'au 2026-05-28 |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_STEADY_STATE_OPERATIONS_POLICY_01` | Politique ops associée à la fenêtre 14d |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_PHASE_2_STABILITY_GATE_01` | Gate post-expansion active |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_PHASE_2_EXECUTION_01` | Execution phase 2 |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_PLAN_01` | Plan expansion |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_READINESS_REVIEW_01` | Readiness review |

### ACTIVE — Desk Pro Automation

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01` | Plan global automation |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_OBSERVABILITY_01` | Observabilité active |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_SIGNAL_EVENT_INPUT_01` | Signal event input |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_INPUT_ENRICHMENT_PLAN_01` | Input enrichment plan |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_INPUT_SEQUENCE_CLOSEOUT_01` | Input sequence closeout |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_COMBINED_INPUT_SMOKE_01` | Combined input smoke |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DESK_SNAPSHOT_INPUT_01` | Desk snapshot input |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_VISUAL_CONTEXT_INPUT_01` | Visual context input |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DRY_RUN_IMPL_01` | Dry run impl |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_FIRST_TRIGGER_OBSERVE_01` | First trigger observe |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01` | Artifact observe |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01` | Artifact output |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_STABILITY_WINDOW_01` | Artifact stability window |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_REVIEW_MERGE_01` | Artifact observe review merge |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_SEQUENCE_CLOSEOUT_01` | Artifact sequence closeout |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_IMPL_01` | Timer impl |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_INSTALL_GATED_01` | Timer install gated |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_START_GATED_01` | Timer start |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_PAYLOAD_FIX_01` | Timer payload fix |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_SPEC_01` | Timer spec |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_STABILITY_WINDOW_01` | Timer stability window |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_SEQUENCE_CLOSEOUT_01` | Sequence closeout |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01` | Runtime review reprise |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AGENT_STANDARD_NEED_VALIDATION_01` | Agent standard need validation |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_ARTIFACT_STABILITY_POST_MERGE_SYNC_01` | Post-merge sync artifact stability |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01` | Schema adapter |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01` | Contract compatibility smoke |

### ACTIVE — Bridge & Vision Headless

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_ADMIN_TRADING_BRIDGE_GUARD_ADD_01` | Bridge guard add — hardening |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01` | Bot vision headless impl |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01` | Bot vision headless systemd |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_DESK_BRIDGE_INTEGRATION_SMOKE_01` | Desk bridge integration smoke |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_CLOSEOUT_01` | Bot vision headless closeout |
| `go/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01` | Pipeline review |

### ACTIVE — Paper Tests

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_GATE_01` | Paper test gate |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_01` | Paper test execution |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_POSITION_CLOSE_01` | Paper position close |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_FLAGS_CONFIG_01` | Paper flags config |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_SCENARIOS_EXPANSION_01` | Paper scenarios expansion |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_RETRY_01` | Paper test execution retry |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RETRY_01` | Paper test retry |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01` | Paper test runtime guards fix |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_VALIDATION_GLOBAL_CLOSEOUT_01` | Paper validation global closeout |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_CYCLE_CLOSEOUT_01` | Paper test cycle closeout |
| `go/GO_OPT_TRADING_ADMIN_TRADING_RUNTIME_SYNC_AFTER_PAPER_GUARDS_01` | Runtime sync after paper guards |

### ACTIVE — Production

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_MONITORING_AND_SECRETS_AUDIT_01` | Production monitoring & secrets audit |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_01` | Production risk limits & kill switch |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_IMPL_01` | Production risk limits impl |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_READINESS_CONDITIONS_01` | Production readiness conditions |

### ACTIVE — Intégrations (Telegram, TradingView, Webhook)

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01` | Telegram webhook real usage test |
| `go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01` | Telegram notification enable test |
| `go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_EXECUTE_TEST_01` | Telegram notification execute test |
| `go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_EXECUTION_RESULTS_01` | Telegram notification execution results |
| `go/GO_OPT_TRADING_ADMIN_TRADING_TV_TEST_RUNTIME_CONFIG_CANONICALIZE_01` | TV test runtime config canonicalize |
| `go/GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01` | TradingView alert external check |
| `go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01` | Webhook runtime review reprise |
| `go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01` | Webhook signal diag reprise |

### ACTIVE — TMUX_IDE (branches TMUX liées à admin-trading)

| Branche | Note |
| --- | --- |
| `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01` | TMUX IDE active branch arbitration |
| `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01` | TMUX IDE git base realign |
| `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01` | TMUX IDE git base realign exec |
| `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01` | TMUX IDE linux x64 compat |
| `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01` | TMUX IDE qualify |
| `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01` | TMUX IDE requalify |

### ACTIVE — Parents

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01` | Admin trading parent review |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01` | Parent sequence closeout |
| `go/GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | Parent machine admin-trading |

### REFERENCE — branches mergees ou closeout, documentation conservee

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_BRIDGE_RETRY_01` | Mergé/absorbé — retry implémenté dans flux bridge |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01` | Absorbé dans séquence automation |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SMOKE_01` | Smoke initial — absorbé dans DESK_PRO_AUTOMATION |
| `go/GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01` | Réparation inbox — livrée |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_PARENT_REALIGNMENT_01` | Realignment doc — merge attendu ou absorbé |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01` | Review doc — reference |
| `go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_TV_TEST_EXECUTION_CLOSEOUT_01` | TV_TEST closeout — doc clos |
| `go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01` | Webhook runtime review — absorbé dans reprise |
| `go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01` | Signal diag initial — absorbé dans reprise |

### DROP_MERGED — branches mergees dans sot/mainline, suppression candidate (apres 2026-05-28)

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_CONTROLLED_PILOT_EXECUTION_01` | Controlled pilot — closeout present, contenu absorbé |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_LIMITED_PRODUCTION_PLAN_01` | Limited prod plan — absorbé |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_LIMITED_PRODUCTION_EXECUTION_01` | Limited prod exec — absorbé |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_SMOKE_PLAN_01` | Smoke plan — absorbé |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_SMOKE_EXECUTION_01` | Smoke exec — absorbé |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_EXECUTION_01` | Prod expansion exec — closeout present |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_PRODUCTION_EXPANSION_PHASE_1_STABILITY_GATE_01` | Phase 1 stability gate — gate passee |

### A_VERIFIER — appartenance machine à confirmer

| Branche | Raison |
| --- | --- |
| `go/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01` | Pipeline Botpress operator — vérifier si admin-trading ou autre machine |
| `go/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01` | Strategy indicator — vérifier rattachement machine |
| `go/GO_OPT_TRADING_WEB3_DATA_ADAPTERS_AUDIT_01` | Web3 data adapters audit — vérifier appartenance |
| `go/GO_SKYAI_COMPETITORS_WEB3_AI_DATA_01` | SKYAI competitors Web3 AI data — vérifier appartenance |

---

## Bloc DB_LAYER

> Dernière réconciliation : `GO_DB_LAYER_MACHINE_WORK_SPLIT_RECONCILIATION_01` — 2026-05-17 — source de vérité : `BRANCH_STATE.md@e1c711bd`

### KEEP_ACTIVE

| Branche | Note |
| --- | --- |
| `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` | Ancre db-layer active ; parent OpenClaw orchestrator ; conserver sous revue |

### CURRENT_OBSERVATION

| Branche | Note |
| --- | --- |
| `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PHASE1_30_RUN_14_DAY_OBSERVATION_01` | Branche courante Phase 1 observation ; ne pas nettoyer tant que l'observation est active |

### PARENTS / SUPPORTS CANONIQUES

| Élément | Note |
| --- | --- |
| `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | Parent machine canonique ; statut OPEN dans `GO_INDEX.md` |
| `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` | Support runtime actif ; ne pas rouvrir sans GO enfant explicite |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01` | Child AI team / db-layer remote exec ; à reprendre seulement si la séquence `db-layer → OpenClaw → SSH → fantome` est explicitement relancée |

### DROP_MERGED / CLEANUP JOURNALISÉ

| Famille | Note |
| --- | --- |
| `CHILD_GATEWAY_SUPERVISION_TMUX_*` | Réconcilié et supprimé ; squash-orphelins confirmés dans `BRANCH_STATE.md` |
| `SYSTEM_MASTER_PLAN_01` | Supprimé local + remote ; squash-orphelin confirmé |
| `PARENT_DOC_REALIGN_01` | Supprimé local + remote ; versions anciennes, aucun contenu forward unique |
| `ADC_CONTROLLED_WRITE_RETRY_01` | Supprimé local-only ; Option B validée, branche entière droppée, `00_GO_MASTER.md` non mergé |
| `*_DB_LAYER_REVIEW_01`, `*_DB_LAYER_CLOSEOUT_01`, `UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01` | Branches nettoyées selon journal `BRANCH_STATE.md` |

### Point de reprise DB_LAYER

1. relire `docs/index/BRANCH_STATE.md`
2. conserver `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` comme ancre
3. poursuivre seulement la branche Phase 1 observation si active
4. ne pas rouvrir les lots cleanup sans nouvelle preuve repo

---

## Bloc STUDENT / OLLAMA — CLOSED_FINAL

**État : Student/Ollama est CLOSED_FINAL. Aucun chantier actif, aucun GO ouvert, aucun flux runtime. La chaîne complète audit → indexation → décision → exécution → réconciliation est PASS.**

### STATUT (Student/Ollama)

| Élément | Statut |
| --- | --- |
| Runtime | CLOSED |
| Audit post-fermeture | PASS |
| Indexation | REPAIRED |
| Remote cleanup decision | PASS |
| Remote cleanup execution | EXECUTED (33 branches supprimées) |
| Count reconciliation | PASS |
| GO actifs student | 0 |
| NEXT_STUDENT_GO | NONE — CLOSED_FINAL, aucun flux actif, aucun GO ouvert |

### BRANCHES RESTANTES (KEEP_ARCHIVE uniquement)

| Branche | Note |
| --- | --- |
| `save/student-2026-04-01` | Snapshot machine student ; rollback potentiel |
| `feat/student-mimo-bitget-live-equity` | Branche historique pré-Ollama ; reference phase MIMO |
| `go/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01` | Parent machine student ; DEFERRED per doc-ops ; reference d'intention |

### HISTORIQUE (branches supprimées — ne sont plus des chantiers actifs)

Tous les GO et branches Student/Ollama suivants ont été mergés, clos, puis supprimés du remote. Leurs dossiers chantier restent sur mainline pour référence. Voir `docs/index/GO_CLOSED_INDEX.md` pour la liste complète.

- **Parents (4)** : `LOCAL_OLLAMA_PARENT_01`, `CANONICAL_INDEX_AGGREGATION_01`, `REVIEW_REALIGN_01`, `SELECTIVE_PROPAGATION_01`
- **Lab children (23)** : toutes les branches `CHILD_STUDENT_OPENCLAW_LAB_*` — closeouts PASS, dossiers sur mainline
- **Agent standardization (6)** : `STUDENT_AGENT_CAPABILITY_GATE_AND_FALLBACK_01`, `FIRST_CONTROLLED_CONSUMER_01`, `CONTROLLED_USAGE_RUNBOOK_01`, `RUNTIME_BASELINE_ADOPTION_01`, `SESSION_RETENTION_POLICY_01`, `SESSION_RETENTION_ENFORCEMENT_01` — tous ABSORBED

### PROCHAIN GO STUDENT

**NEXT_STUDENT_GO: NONE**

Justification :
- Student/Ollama runtime : CLOSED
- Aucun GO actif dans `GO_INDEX.md`
- Aucun flux actif dans `ACTIVE_STREAMS.md`
- 33 branches supprimées, 3 KEEP_ARCHIVE conservées
- Standard agent disponible pour futur besoin validé sur une autre surface

Le prochain mouvement machine doit cibler une autre surface : `cursor-ai`, `admin-trading`, `db-layer` ou `fantome`. Voir `docs/index/GO_INDEX.md` et `docs/index/ACTIVE_STREAMS.md` pour les flux actifs.

---

## Bloc FANTOME

| Branche | Note |
| --- | --- |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | AI team architecture parent |
| `go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | AI team architecture parent (go/) |
| `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` | Strict workers parent |
| `go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01` | ClickUp parent continuity — bundle d'implementation ; review/merge cote fantome ; next GO: `GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_REVIEW_MERGE_01` |

---

## Point de reprise

Pour toute suite sur ce routage machine :
1. relire `docs/index/BRANCH_STATE.md`
2. recroiser avec l'etat Git reel
3. ajuster ici seulement si le rattachement machine change reellement
4. ne pas surclasser un cas sans preuve repo/PR/documentaire
