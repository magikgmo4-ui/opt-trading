---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01_AUDIT
doc_type: audit
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
status: open
updated_at: 2026-05-14
---

# 01_AUDIT_SURFACES_AND_STATE

## Objet

Compte rendu détaillé de l'état réel du système d'orchestration `opt-trading` au 2026-05-14.
Quatre axes : établi en doc / prévu dans les plans / implémenté et opérationnel / reste à produire.
Validation de la couverture de chaque surface dans le plan d'orchestration, avec tmux comme colonne vertébrale.

---

## AXE 1 — CE QUI EST ÉTABLI DANS LA DOCUMENTATION

### 1.1 Orchestrateur parent

| Chantier | Fichiers | Statut doc |
| --- | --- | --- |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` | `00_INITIAL_PROJECT_DOC.md`, `04_OPERATOR_BRIDGE_SPEC.md`, `11_NEXT_GO_SEQUENCE_AND_IDE_BUNDLE_PLAN.md`, `REPRISE_DB_LAYER_20260505.md` | ÉTABLI |

Ce parent documente :
- Gateway validé en foreground (`127.0.0.1:18789`, `{"ok":true,"status":"live"}`)
- Bridge spec V1 complet (contrats, whitelist, journalisation, refus obligatoires)
- Séquence complète : tmux → bridge V1 → mapping agents → smokes
- Reprise 2026-05-05 : child TMUX comme prochain GO (complété depuis)

### 1.2 Chaîne tmux supervision (MERGED PASS)

| Chantier | Verdict | Preuves |
| --- | --- | --- |
| `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01` | PASS | protocole tmux + invariants |
| `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01` | PASS | start/status/stop/health prouvés |
| `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01` | PASS | chaîne fermée, anomalie send-keys documentée |

Invariant runtime établi :
```text
Machine: db-layer | Session: openclaw-gateway | User: openclaw
Bind: 127.0.0.1:18789 | Entry point: cmd.sh start
/health → {"ok":true,"status":"live"}
```

### 1.3 Runtime security (doc active)

| Chantier | Documents | Statut |
| --- | --- | --- |
| `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01` | permission matrix, policy schema, policy YAML draft, static validator | ACTIF |

### 1.4 Botpress adapter (spec + impl PASS)

| Chantier | Verdict | Détail |
| --- | --- | --- |
| `GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01` | PASS | contrat, payload examples, safety gate, error handling |
| `GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_IMPL_01` | PASS | 13/13 smokes, safety gate, rate limiting, circuit breaker |

NEXT_GO documenté : `GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01` — **non ouvert**.

### 1.5 Surfaces externes classifiées

Chantier `GO_OPT_TRADING_DOC_OPS_WHY_EXTERNAL_ORCHESTRATION_SURFACES_01` (11 documents) :

| Surface | Classe WHY | Rôle documenté |
| --- | --- | --- |
| ClickUp | R2/R3 | suivi tâches / opérations |
| Botpress | R3 | agent conversationnel / workflow |
| Knowledge Graph | R3 | représentation relations / vérité projet |
| Airtable | R2/R3 | base structurée / opérations |

Documents produits : classification, runtime risk, autonomy risk, governance, multi-machine impact,
observability requirements, runtime boundaries, human review gates, runtime alignment, reporting architecture, integration roadmap, architecture synthesis.

### 1.6 Airtable orchestration (parent ouvert)

`GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01` — 9 documents :
`00_INITIAL_PROJECT_DOC`, `01_RESEARCH_SYNTHESIS`, `02_INTEGRATION_ARCHITECTURE`,
`03_AIRTABLE_SCHEMA_TRADING_JOURNAL_V1`, `04_PRODUCT_FINISH_PLAN`, `05_IMPLEMENTATION_SPEC`,
`06_INDEXATION_STATUS`, `07_RESUME_POINT_CANONICAL`, `08_SESSION_INDEPENDENT_REPRISE`, `09_BUNDLE_REPRISE`.

Statut : **doc riche, implémentation non démarrée**.

### 1.7 Builder agent chain (MERGED PASS — session précédente)

| Chantier | Verdict |
| --- | --- |
| `FIRST_CONTROLLED_JOB_01` | PASS |
| `DOC_TASK_DRY_RUN_01` | PASS |
| `DOC_PLAN_REVIEW_01` | PASS |
| `DOC_WRITING_01` | PASS — produit BUILDER_OPERATIONAL_GUIDE, ARCHITECTURE_VIEW, CONTROLLED_WORKFLOW, SECURITY_GUARDRAILS |
| `DOC_ADOPTION_01` | PASS |
| `DOC_INDEXATION_REVIEW_01` | PASS |
| `GATEWAY_TOKEN_RECONCILIATION_REVIEW_01` | PASS |
| `GATEWAY_TOKEN_RECONCILIATION_PATCH_01` | PASS |

### 1.8 DB-layer runtime docs (MERGED PASS)

| Chantier | Verdict |
| --- | --- |
| `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_REVIEW_01` | PASS — installation state, gateway/port 18789, tmux modes, deps |
| `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_DB_LAYER_CLOSEOUT_01` | PASS — final runtime state, operation method, deferred items |
| `GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01` | PASS |
| `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_REVIEW_01` | PASS |
| `GO_OPENCLAW_STATE_DIR_REPAIR_10` | PASS |

---

## AXE 2 — CE QUI EST PRÉVU DANS LES PLANS ET BUNDLES IDE

### 2.1 Plan séquence parent (11_NEXT_GO_SEQUENCE_AND_IDE_BUNDLE_PLAN.md)

Séquence verrouillée (2026-04-26) :

```
1. GATEWAY_SUPERVISION_TMUX_01   → DONE PASS
2. OPERATOR_BRIDGE_IMPL_V1_01   → PRÉVU, non ouvert
3. AGENT_SKILL_PROVIDER_MAPPING_01 → PRÉVU, non ouvert
4. BRIDGE_SMOKE_LOCAL_01        → PRÉVU, dépend de 2
```

GOs suivants prévus dans le plan :
```
GO_OPENCLAW_OPT_TRADING_CHILD_SECURITY_POLICY_V1_01    → partiellement couvert par runtime security
GO_OPENCLAW_OPT_TRADING_CHILD_REMOTE_ACCESS_TUNNEL_01  → différé (WAN interdit)
```

### 2.2 Bridge spec — contrat défini (04_OPERATOR_BRIDGE_SPEC.md)

Contenu de la spec :
- Contrat JSON entrée : `{action, params, context, go_id, machine}`
- Contrat JSON sortie : `{status, result, proof, journal_entry}`
- Whitelist actions : status, validate-request, run-task, get-artifact
- Refus obligatoires : shell libre, write prod, bypass GO, secrets
- Module cible : `modules/openclaw_operator_bridge/`
- Structure cible définie : `cmd.sh`, `menu.sh`, `sanity_check.sh`, `app/`, `config/`, `commands/`, `docs/`, `tests/`

### 2.3 Multi-agents crosswalk (GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01)

Mapping doctrine défini :
```text
agent          → rôle conversationnel / exécuteur borné
skill          → capacité encapsulée
provider       → modèle / backend IA
orchestrator   → opt-trading (jamais OpenClaw)
prompt_generator → validated_prompt_factory
deployer       → deploy_module_multi_machine
gateway        → OpenClaw runtime
```

### 2.4 Airtable — schéma trading journal défini

`03_AIRTABLE_SCHEMA_TRADING_JOURNAL_V1.md` définit :
- Tables : trades, positions, signals, strategies, performance
- Relations et champs clés
- API design
- **Implémentation non démarrée**

---

## AXE 3 — CE QUI EST IMPLÉMENTÉ ET OPÉRATIONNEL

### 3.1 Modules opérationnels sur db-layer

| Module | Localisation | Opérationnel | Fonctions |
| --- | --- | --- | --- |
| `gateway_openclaw` | `modules/gateway_openclaw/` | **OUI** | `cmd.sh` : sanity/status/start/stop/logs/attach/health/probe |
| `menu_openclaw` | `modules/menu_openclaw/` | Partiel | app/, docs/, scripts/ — UI CLI |
| `validated_prompt_factory` | `modules/validated_prompt_factory/` | **OUI** | app/, cmd.sh, commands/, contextuals/ |
| `openclaw_config_modulaire` | `modules/openclaw_config_modulaire/` | Partiel | app/, docs/, scripts/ |
| `doctor_openclaw` | `modules/doctor_openclaw/` | Présent | diagnostic OpenClaw |
| `evidence_openclaw` | `modules/evidence_openclaw/` | Présent | collecte preuves |
| `model_provider_openclaw` | `modules/model_provider_openclaw/` | Présent | routing modèle |
| `install_module_openclaw` | `modules/install_module_openclaw/` | Présent | installation |
| `configure_openclaw` | `modules/configure_openclaw/` | Présent | configuration |

### 3.2 Gateway OpenClaw

```text
STATUT: OPÉRATIONNEL
Machine: db-layer
User: openclaw (session tmux) / ghost (builder direct)
Session tmux: openclaw-gateway
Bind: 127.0.0.1:18789
Entry: modules/gateway_openclaw/scripts/cmd.sh start
/health: {"ok":true,"status":"live"}
Builder: openclaw agent --agent builder --json (as ghost)
```

### 3.3 TradingView — webhook opérationnel

```text
STATUT: OPÉRATIONNEL (côté admin-trading)
Module: tradingview_observer, tradingview_observer_openclaw
Webhook: reçoit alertes TradingView
Signal brut: non normalisé pipeline (signal_router absent)
```

### 3.4 Telegram — notifications opérationnelles

```text
STATUT: OPÉRATIONNEL
Bot actif, notifications enable PASS, test execution PASS
Dispatcher structuré: NON (notifications ad hoc)
```

### 3.5 Botpress adapter

```text
STATUT: IMPL PASS (local)
Smokes: 13/13 PASS
Safety gate: 4 intents bloqués
Rate limiting: actif
Circuit breaker: actif
E2E Telegram: NON
```

### 3.6 Runtime security static validator

```text
STATUT: IMPL PASS (merged PR #447 zone)
Outil: tools/openclaw/validate_skill_policy_static.py
Policy YAML: défini
Permission matrix: définie
```

---

## AXE 4 — CE QUI RESTE À PRODUIRE

### 4.1 Priorité 1 — Débloquant (rien ne peut avancer sans ça)

| À produire | GO à ouvrir | Dépend de |
| --- | --- | --- |
| `modules/openclaw_operator_bridge/` | `GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_IMPL_V1_01` | Gateway PASS ✓ |
| `signal_router` — normalisation webhook → signal JSON | `GO_OPT_TRADING_ORCHESTRATOR_CHILD_SIGNAL_ROUTER_V1_01` | Rien (indépendant) |
| `notification_dispatcher` structuré | `GO_OPT_TRADING_ORCHESTRATOR_CHILD_NOTIFICATION_DISPATCHER_V1_01` | Telegram ✓ |

### 4.2 Priorité 2 — Post-bridge

| À produire | GO à ouvrir | Dépend de |
| --- | --- | --- |
| `proposition_engine` (signal → OpenClaw → proposition JSON) | `GO_OPT_TRADING_ORCHESTRATOR_CHILD_PROPOSITION_ENGINE_V1_01` | Bridge V1 |
| `validation_gate` (auto + Telegram approval) | `GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01` | Proposition engine + Telegram ✓ |
| Mapping agents/skills/providers | `GO_OPT_TRADING_MULTI_AGENTS_CHILD_AGENT_SKILL_PROVIDER_MAPPING_01` | Bridge V1 |
| Bridge smoke local | `GO_OPENCLAW_OPT_TRADING_CHILD_BRIDGE_SMOKE_LOCAL_01` | Bridge V1 |

### 4.3 Priorité 3 — Post-trade

| À produire | GO à ouvrir | Dépend de |
| --- | --- | --- |
| `result_tracker` (P&L brut) | `GO_OPT_TRADING_ORCHESTRATOR_CHILD_RESULT_TRACKER_V1_01` | trade_executor |
| `datasheet_writer` (→ Sheets + Airtable) | `GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_01` | result_tracker |
| `learning_feeder` (→ OpenClaw feedback) | `GO_OPT_TRADING_ORCHESTRATOR_CHILD_LEARNING_FEEDER_V1_01` | Bridge V1 + result_tracker |
| Airtable implémentation | enfants de `GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01` | signal_router |
| Sheets writer | `GO_OPT_TRADING_ORCHESTRATOR_CHILD_SHEETS_WRITER_V1_01` | result_tracker |

### 4.4 Priorité 4 — Intégrations finales

| À produire | GO à ouvrir | Dépend de |
| --- | --- | --- |
| Botpress ↔ Telegram E2E | `GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01` | Botpress impl ✓ |
| ClickUp task tracker | enfants de `GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01` | Rien (indépendant) |
| LocalCMS UI consumer | enfants de `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` | données disponibles |
| Figma design | GO futur | LocalCMS |

---

## AXE 5 — SURFACES : INVENTAIRE COMPLET ET COUVERTURE PLAN

### Surfaces internes

| Surface | Présente | Documentée | Impl | Opérationnelle | Dans plan orchestration |
| --- | --- | --- | --- | --- | --- |
| OpenClaw gateway | ✓ | ✓ PASS | ✓ | ✓ | ✓ colonne vertébrale |
| OpenClaw builder agent | ✓ | ✓ PASS | N/A runtime | ✓ | ✓ proposition_engine, learning |
| `openclaw_operator_bridge` | ✗ (spec seule) | ✓ PASS | ✗ | ✗ | ✓ PRIORITÉ 1 |
| `gateway_openclaw` module | ✓ | ✓ | ✓ | ✓ | ✓ |
| `menu_openclaw` | ✓ | Partiel | Partiel | Partiel | Indirect (UI CLI) |
| `validated_prompt_factory` | ✓ | Partiel | ✓ | ✓ | ✓ prompt_generator |
| `workflow_post_change_v2` | ✓ | Partiel | Partiel | ? | Indirect |
| `deploy_module_multi_machine` | ✓ | Partiel | ✓ | ✓ | ✓ deployer |
| `runtime_security` (policy+validator) | ✓ | ✓ | Partiel | Partiel | ✓ validation_gate |
| LocalCMS consumer | ✓ | ✓ | Partiel | Partiel | ✓ ui_renderer |
| tmux supervisor | ✓ | ✓ PASS | ✓ | ✓ | ✓ colonne vertébrale |

### Surfaces externes — Apps

| Surface | Présente | Documentée | Impl | Opérationnelle | Dans plan orchestration |
| --- | --- | --- | --- | --- | --- |
| TradingView webhook | ✓ | ✓ | ✓ | ✓ | ✓ signal source |
| Telegram bot | ✓ | ✓ | ✓ | ✓ | ✓ notification + validation |
| Botpress adapter | ✓ | ✓ PASS | ✓ (local) | ✓ (local) | ✓ operateur avancé |
| Airtable | ✓ (plan) | ✓ riche | ✗ | ✗ | ✓ datastore + journal |
| ClickUp | ✓ (plan) | ✓ | ✗ | ✗ | ✓ task_tracker |
| Sheets | ✗ | ✗ | ✗ | ✗ | ✓ datasheet — À INITIER |
| Figma | ✗ | ✗ | ✗ | ✗ | Référence design — différé |

### Surfaces manquantes dans le plan (gap identifié)

| Surface | Statut | Action |
| --- | --- | --- |
| `tradingview_observer_openclaw` | Module présent, scope flou | À clarifier : overlap avec signal_router ? |
| Knowledge Graph | Classifié R3, chantier `GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` ouvert | Hors pipeline trade — différé |
| Figma | Non documenté | Ajouter dans roadmap LocalCMS UI |

---

## AXE 6 — TMUX COMME COLONNE VERTÉBRALE

### Rôle établi

```text
tmux = superviseur runtime canonique sur db-layer
Pas de systemd (hors scope)
Pas d'exposition WAN directe
```

### Sessions tmux définies

| Session | User | Process | Port | Statut |
| --- | --- | --- | --- | --- |
| `openclaw-gateway` | openclaw | `openclaw gateway` | 127.0.0.1:18789 | OPÉRATIONNEL |

### Sessions tmux prévues (non encore définies)

| Session future | User | Process cible | Dépend de |
| --- | --- | --- | --- |
| `openclaw-bridge` | ghost/openclaw | `openclaw_operator_bridge/cmd.sh` | Bridge V1 impl |
| `signal-router` | opt-trading user | `signal_router.py` | Signal router GO |
| `notification-dispatcher` | opt-trading user | `notification_dispatcher.py` | Dispatcher GO |

### Chantiers tmux actifs sur mainline

| Chantier | Rôle | Statut |
| --- | --- | --- |
| `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` | Parent runtime tmux global | OUVERT |
| `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` | tmux + IDE cadrage | P0 GO_INDEX |
| `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` | implémentation base | EXISTANT |

---

## SYNTHÈSE EXÉCUTIVE

```text
ÉTABLI ET SOLIDE:
  Gateway tmux → OPÉRATIONNEL
  Builder agent → OPÉRATIONNEL
  Botpress adapter → IMPL PASS (local)
  TradingView webhook → OPÉRATIONNEL
  Telegram → OPÉRATIONNEL
  Airtable → DOC RICHE (9 fichiers), impl manquante
  Runtime security → ACTIVE (validator mergé)
  Bridge spec → COMPLÈTE

LACUNE CRITIQUE (bloque tout):
  Bridge V1 implementation → NON OUVERT
  → sans bridge, pas de proposition_engine, pas de learning_feeder

PREMIER GO À OUVRIR:
  GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_IMPL_V1_01

EN PARALLÈLE IMMÉDIAT (indépendant):
  GO_OPT_TRADING_ORCHESTRATOR_CHILD_SIGNAL_ROUTER_V1_01
  GO_OPT_TRADING_ORCHESTRATOR_CHILD_NOTIFICATION_DISPATCHER_V1_01
  GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01

COUVERTURE PLAN ORCHESTRATION:
  Toutes les surfaces documentées sont dans le plan.
  Gap : Sheets (non initié), tradingview_observer_openclaw (scope flou), Figma (différé).
```
