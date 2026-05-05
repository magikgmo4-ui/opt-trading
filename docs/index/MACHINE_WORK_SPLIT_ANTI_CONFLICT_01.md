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
updated_at: 2026-05-05
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

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_ADMIN_TRADING_BRIDGE_GUARD_ADD_01` | Bridge guard add |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_CLOSEOUT_01` | Bot vision headless closeout |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_DESK_BRIDGE_INTEGRATION_SMOKE_01` | Desk bridge integration smoke |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01` | Bot vision headless impl |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_PARENT_REALIGNMENT_01` | Bot vision headless parent realignment |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01` | Bot vision headless review |
| `go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_SYSTEMD_01` | Bot vision headless systemd |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_BRIDGE_RETRY_01` | Desk bridge retry |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01` | Desk pro runtime review |
| `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SMOKE_01` | Desk pro smoke |
| `go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01` | Admin trading parent review |
| `go/GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01` | TradingView alert external check |
| `go/GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01` | Vision inbox repair |
| `go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01` | Webhook runtime review |
| `go/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01` | Webhook signal diag |
| `go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01` | Telegram webhook real usage test |
| `go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_TV_TEST_EXECUTION_CLOSEOUT_01` | TV_TEST execution closeout |
| `go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_ENABLE_TEST_01` | Telegram notification enable test |
| `go/GO_OPT_TRADING_ADMIN_TRADING_TV_TEST_RUNTIME_CONFIG_CANONICALIZE_01` | TV_TEST runtime config canonicalize |
| `go/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01` | Pipeline Botpress operator parent |
| `go/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01` | Strategy indicator parent |
| `go/GO_OPT_TRADING_WEB3_DATA_ADAPTERS_AUDIT_01` | Web3 data adapters audit |
| `go/GO_SKYAI_COMPETITORS_WEB3_AI_DATA_01` | SKYAI competitors Web3 AI data |

---

## Bloc DB_LAYER

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_REVIEW_01` | Machine db-layer parent review |
| `go/GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01` | UI LocalCMS db-layer consumer realignment |
| `go/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_REVIEW_01` | Tmux runtime db-layer review |
| `go/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_CLOSEOUT_01` | Tmux runtime db-layer closeout |
| `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` | OpenClaw orchestrator parent |
| `go/GO_OPENCLAW_STATE_DIR_REPAIR_10` | OpenClaw state dir repair |
| `doc/GO_OPENCLAW_INFRA_BASELINE_01` | OpenClaw infra baseline |
| `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01` | Airtable orchestration parent |
| `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` | Repo KG parent graph system |
| `go/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01` | Repo surfaces parent cartography |

---

## Bloc STUDENT / OLLAMA

| Branche | Note |
| --- | --- |
| `go/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01` | Machine student parent |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` | Local Ollama parent |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_CANONICAL_INDEX_AGGREGATION_01` | Canonical index aggregation |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_SELECTIVE_PROPAGATION_01` | Selective propagation |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_CLOSEOUT_01` | Lab closeout |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_GATEWAY_SESSION_FIX_01` | Gateway session fix |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_APPLY_01` | Install apply |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_AUTHORIZATION_01` | Install authorization |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_DRYRUN_01` | Install dryrun |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_SOURCE_PROOF_01` | Install source proof |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_LOCAL_OLLAMA_BINDING_SMOKE_01` | Local Ollama binding smoke |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_01` | Model pull eval 01 |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_01_RETRY` | Model pull eval retry |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_03` | Model pull eval 03 |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_04` | Model pull eval 04 |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_04_RETRY` | Model pull eval 04 retry |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_NETWORK_DIAG_01` | Network diag |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_DISK_FIX_01` | Ollama disk fix |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_E2E_SMOKE_01` | Ollama E2E smoke |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_MODEL_EVALUATION_01` | Ollama model evaluation |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_PROVIDER_ROUTING_AUDIT_01` | Provider routing audit |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_PROVIDER_SWITCH_APPLY_01` | Provider switch apply |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_PROVIDER_SWITCH_DRYRUN_01` | Provider switch dryrun |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01` | Qualification |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_SCOPE_VALIDATION_01` | Scope validation |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_TIMEOUT_TUNING_01` | Timeout tuning |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_01` | Workspace slim |

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
