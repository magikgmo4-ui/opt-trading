---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
doc_type: master_plan
repo: opt-trading
project: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: open
lifecycle_stage: planning
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-23
topic_keys:
  - orchestration
  - openclaw
  - system-design
  - data-flow
  - workers
  - apps
  - roadmap
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/REPRISE_DB_LAYER_20260505.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/11_NEXT_GO_SEQUENCE_AND_IDE_BUNDLE_PLAN.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/04_OPERATOR_BRIDGE_SPEC.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_FRESHNESS_AUDIT_01/00_FRESHNESS_AUDIT.md
---

# 00_SYSTEM_MASTER_PLAN

## NOTE_DE_FRAÎCHEUR_2026-05-23

Ce master plan a été rafraîchi après la fusion de l'audit de fraîcheur PR #764.

Le document historique `01_AUDIT_SURFACES_AND_STATE.md` du 2026-05-14 reste conservé comme audit daté. Les statuts opérationnels ci-dessous reflètent l'état réel post-closeouts du 2026-05-16 :

```text
OPENCLAW_OPERATOR_BRIDGE = PASS
SIGNAL_ROUTER = PASS
NOTIFICATION_DISPATCHER = PASS
PROPOSITION_ENGINE = PASS
NEXT_REAL_GO = GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01
```

---

## 1_MASTER_TARGET

Poser le plan système complet de l'orchestrateur `opt-trading` :
- cartographier toutes les surfaces orchestrées
- définir les workers stricts par rôle
- définir le flux data canonique signal → learning
- définir les apps intégrées et leur rôle
- produire la roadmap child GO exécutable par surface

---

## 2_PARENT_CANONIQUE

```text
PARENT = GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
BRANCHE = go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01 (KEEP_ACTIVE)
REPRISE = REPRISE_DB_LAYER_20260505.md
ÉTAT ÉTABLI:
  - Gateway OpenClaw opérationnel (ghost@db-layer, ws://127.0.0.1:18789)
  - Invocation correcte : openclaw agent as ghost
  - tmux supervision chain : MERGED PASS
  - Bridge V1 spec existe (04_OPERATOR_BRIDGE_SPEC.md)
  - Bridge V1 implémentation : PASS (GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_IMPL_V1_01)
  - Signal Router V1 : PASS (GO_OPT_TRADING_ORCHESTRATOR_CHILD_SIGNAL_ROUTER_V1_01)
  - Notification Dispatcher V1 : PASS (GO_OPT_TRADING_ORCHESTRATOR_CHILD_NOTIFICATION_DISPATCHER_V1_01)
  - Proposition Engine V1 : PASS (GO_OPT_TRADING_ORCHESTRATOR_CHILD_PROPOSITION_ENGINE_V1_01)
```

---

## 3_PRINCIPE_FONDAMENTAL

```text
ORCHESTRATEUR = opt-trading (jamais OpenClaw)
RUNTIME IA    = OpenClaw (gateway + builder agent)
RULE:
  OpenClaw n'orchestre pas.
  OpenClaw exécute des tâches bornées à la demande de opt-trading.
  opt-trading décide. OpenClaw réalise.
```

---

## 4_SURFACES_ORCHESTRÉES

### Surfaces internes

| Surface | Rôle | Machine hôte | État |
| --- | --- | --- | --- |
| `openclaw_gateway` | Runtime IA — exécute les tâches bornées | db-layer | OPÉRATIONNEL |
| `openclaw_operator_bridge` | Contrat d'interface opt-trading → OpenClaw | db-layer | PASS — OPÉRATIONNEL |
| `signal_router` | Normalise les signaux entrants TradingView | admin-trading/db-layer | PASS — NormalizedSignal JSON |
| `notification_dispatcher` | Diffuse les événements pipeline vers Telegram | db-layer | PASS — dry-run dispatch OK |
| `proposition_engine` | Transforme signal normalisé en proposition via OpenClaw | db-layer | PASS — proposition JSON |
| `validation_gate` | Gate auto + approbation Telegram | db-layer | NEXT_GO RÉEL |
| `localcms_consumer` | UI lecture — consomme données opt-trading | db-layer | REALIGNMENT DONE |
| `deploy_module_multi_machine` | Déployeur cross-machine | all | EXISTANT |
| `validated_prompt_factory` | Générateur de prompts validés | db-layer | EXISTANT |
| `workflow_ai` | Orchestrateur workflow IA | db-layer | EXISTANT |

### Surfaces externes — Apps intégrées

| App | Rôle dans le système | Direction | État |
| --- | --- | --- | --- |
| **TradingView** | Source de signal (webhooks, alertes techniques) | → entrant | WEBHOOK OPÉRATIONNEL |
| **Telegram** | Notification opérateur + commandes humaines | ↔ bidirectionnel | OPÉRATIONNEL |
| **Airtable** | Base de données orchestration, tables de décision | ↔ lecture/écriture | PARENT OUVERT |
| **ClickUp** | Tracking GO / tâches / suivi projet | → écriture | CONTINUITY OUVERT |
| **Figma** | Design UI — wireframes LocalCMS / dashboards | → référence | NON INTÉGRÉ |
| **Botpress** | Bot conversationnel / workflow automatisé | ↔ bidirectionnel | IMPL PASS LOCAL — E2E TELEGRAM NON OUVERT |
| **Sheets** | Datasheets résultats / P&L / reporting | → écriture | NON INTÉGRÉ |

---

## 5_WORKERS_STRICTS_PAR_RÔLE

```text
RÈGLE: chaque worker a un rôle unique, borné, sans empiétement.
```

| Worker | Rôle | Input | Output | Interdit | État |
| --- | --- | --- | --- | --- | --- |
| `signal_router` | Reçoit webhook TradingView, valide format, route vers pipeline | webhook HTTP | signal JSON normalisé | décision de trade | PASS |
| `proposition_engine` | Évalue signal, génère proposition de trade via OpenClaw | signal JSON | proposition JSON | exécution directe | PASS |
| `validation_gate` | Présente proposition à l'opérateur (Telegram) ou applique règle auto | proposition JSON | proposition validée / rejetée | trade sans approbation | NEXT_GO |
| `trade_executor` | Exécute trade validé sur l'exchange | proposition validée | trade_id + fill JSON | proposition non validée | NON OUVERT |
| `result_tracker` | Capture résultat trade, calcule P&L brut | trade_id + fill | résultat JSON | écriture datasheet | NON OUVERT |
| `datasheet_writer` | Écrit résultat vers Sheets / Airtable | résultat JSON | ligne datasheet confirmée | calcul P&L | NON OUVERT |
| `learning_feeder` | Envoie contexte résultat vers OpenClaw pour amélioration future | résultat + contexte | feedback structuré | modification de trade | NON OUVERT |
| `notification_dispatcher` | Envoie notifications Telegram aux étapes clés | événement quelconque | message Telegram | décision opérationnelle | PASS |
| `task_tracker` | Sync état pipeline vers ClickUp / Airtable | état pipeline | tâche mise à jour | trade ou notification | NON OUVERT |
| `ui_renderer` | Sert données vers LocalCMS consumer | état + données | réponse UI | écriture base prod | NON OUVERT |

---

## 6_FLUX_DATA_CANONIQUE

```text
signal → proposition → validation → trade → résultat → datasheet → learning
```

### Détail du flux

```
[1] SIGNAL
    TradingView webhook → signal_router
    → format validé : {ticker, side, price, timestamp, strategy_id}
    → état : PASS

[2] PROPOSITION
    signal_router → proposition_engine
    → appel OpenClaw builder : "évalue signal, propose trade"
    → résultat : {action, size, entry, sl, tp, confidence, rationale}
    → état : PASS

[3] VALIDATION
    proposition_engine → validation_gate
    → si auto-gate : check règles risk limits (kill switch)
    → si opérateur : notification Telegram + attente réponse
    → résultat : APPROVED / REJECTED + motif
    → état : NEXT_GO RÉEL

[4] TRADE
    validation_gate → trade_executor (si APPROVED)
    → appel exchange API
    → résultat : {trade_id, fill_price, fill_qty, timestamp}
    → état : NON OUVERT

[5] RÉSULTAT
    trade_executor → result_tracker
    → suivi position : open → close
    → calcul P&L : {gross_pnl, net_pnl, fees, duration}
    → état : NON OUVERT

[6] DATASHEET
    result_tracker → datasheet_writer
    → écriture Sheets : ligne résultat trade
    → écriture Airtable : enregistrement orchestration
    → état : NON OUVERT

[7] LEARNING
    result_tracker → learning_feeder → OpenClaw builder
    → contexte : {signal, proposition, résultat, P&L}
    → feedback structuré : amélioration propositions futures
    → état : NON OUVERT
```

### Flux de notification parallèle

```
Chaque étape clé → notification_dispatcher → Telegram (PASS)
Chaque changement d'état → task_tracker → ClickUp / Airtable (NON OUVERT)
```

---

## 7_RÔLES_APPS_DÉTAILLÉS

### TradingView
```text
RÔLE: source de signal primaire
INTÉGRATION: webhook HTTP POST vers signal_router
DONNÉES SORTANTES: ticker, side, price, alert_message, strategy_id
CONTRAINTE: signal brut non exécutable directement — passe par proposition_engine
ÉTAT: webhook opérationnel ; signal_router PASS
```

### Telegram
```text
RÔLE: canal opérateur — notification + commandes
INTÉGRATION: bot Telegram bidirectionnel
DONNÉES SORTANTES: events, propositions, résultats
DONNÉES ENTRANTES: approbations, rejets, commandes manuelles
CONTRAINTE: jamais source de signal de trade direct
ÉTAT: opérationnel ; notification_dispatcher PASS ; validation_gate NEXT_GO
```

### Airtable
```text
RÔLE: base de données orchestration
TABLES CIBLES:
  - trades (historique complet)
  - propositions (avec statut validation)
  - signaux (archive TradingView)
  - learning_sessions (feedback OpenClaw)
INTÉGRATION: Airtable API (orchestration parent ouvert)
ÉTAT: GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01 OUVERT
```

### ClickUp
```text
RÔLE: tracking GO / tâches / état pipeline
INTÉGRATION: ClickUp API (continuity parent ouvert)
DONNÉES: sync état GO chantiers + pipeline trades actifs
CONTRAINTE: ne pas doubler Airtable — ClickUp = task mgmt, Airtable = data
ÉTAT: GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01 OUVERT
```

### Figma
```text
RÔLE: référence design UI
USAGE: wireframes LocalCMS consumer + dashboards reporting
INTÉGRATION: lecture seule — pas d'API active dans le pipeline trade
ÉTAT: NON INTÉGRÉ — chantier futur LocalCMS UI
```

### Botpress
```text
RÔLE: bot conversationnel + workflow automation
USAGE: interface opérateur avancée, commandes structurées
INTÉGRATION: Botpress API + webhook
CONTRAINTE: wrapper au-dessus de Telegram, pas un remplaçant
ÉTAT: impl PASS local ; GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01 reste non ouvert
```

### Sheets
```text
RÔLE: datasheet résultats + reporting P&L
TABLES CIBLES:
  - trade_results (par session, par jour, par stratégie)
  - pnl_summary (agrégé hebdo/mensuel)
  - signal_log (archive enrichie)
INTÉGRATION: Google Sheets API via datasheet_writer
ÉTAT: NON INTÉGRÉ — dépend de result_tracker
```

---

## 8_ROADMAP_CHILD_GO_PAR_SURFACE

### Séquence déjà PASS

```text
PHASE 1 — Bridge V1 (fondation)
  GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_IMPL_V1_01
  Livrable: modules/openclaw_operator_bridge/ opérationnel local
  Statut: PASS
  Débloque: proposition_engine, learning_feeder

PHASE 2A — Signal Router V1
  GO_OPT_TRADING_ORCHESTRATOR_CHILD_SIGNAL_ROUTER_V1_01
  Livrable: webhook TradingView → signal JSON normalisé
  Statut: PASS

PHASE 2B — Notification Dispatcher V1
  GO_OPT_TRADING_ORCHESTRATOR_CHILD_NOTIFICATION_DISPATCHER_V1_01
  Livrable: événements pipeline → Telegram structuré
  Statut: PASS

PHASE 2C — Proposition Engine V1
  GO_OPT_TRADING_ORCHESTRATOR_CHILD_PROPOSITION_ENGINE_V1_01
  Livrable: signal → OpenClaw → proposition JSON
  Statut: PASS
  Débloque: validation_gate, trade_executor
```

### Séquence obligatoire restante

```text
PHASE 3 — Validation gate
  GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01
  Livrable: gate auto + Telegram approval flow
  Préreq: proposition_engine PASS + notification_dispatcher PASS + Telegram opérationnel
  Statut: NEXT_GO RÉEL
  Bloque: trade_executor live

PHASE 4 — Trade executor
  GO_OPT_TRADING_ORCHESTRATOR_CHILD_TRADE_EXECUTOR_V1_01
  Préreq: validation_gate PASS
  Statut: NON OUVERT

PHASE 5 — Result tracker + datasheet writer
  GO_OPT_TRADING_ORCHESTRATOR_CHILD_RESULT_TRACKER_V1_01
  GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_01
  Préreq: trade_executor opérationnel
  Statut: NON OUVERT

PHASE 6 — Learning feeder
  GO_OPT_TRADING_ORCHESTRATOR_CHILD_LEARNING_FEEDER_V1_01
  Préreq: Bridge V1 PASS + result_tracker
  Statut: NON OUVERT

PHASE 7 — Sheets integration
  GO_OPT_TRADING_ORCHESTRATOR_CHILD_SHEETS_WRITER_V1_01
  Préreq: datasheet_writer
  Statut: NON OUVERT
```

### Séquence parallèle / indépendante

```text
TRACK A — Airtable orchestration
  GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01 (OUVERT)
  → child tables design : trades, propositions, signaux, learning

TRACK B — ClickUp sync
  GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01 (OUVERT)
  → child task_tracker : sync état GO + pipeline

TRACK C — Botpress Telegram E2E
  GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01
  Préreq: Botpress impl PASS local
  Statut: NON OUVERT

TRACK D — Figma / LocalCMS UI
  GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 (OUVERT)
  Préreq: signal_router + résultats disponibles
```

---

## 9_ORDRE_D_OUVERTURE_RECOMMANDÉ

```text
IMMÉDIAT (prochain GO réel):
  1. GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01

APRÈS VALIDATION_GATE:
  2. GO_OPT_TRADING_ORCHESTRATOR_CHILD_TRADE_EXECUTOR_V1_01
  3. GO_OPT_TRADING_ORCHESTRATOR_CHILD_RESULT_TRACKER_V1_01
  4. GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_01
  5. GO_OPT_TRADING_ORCHESTRATOR_CHILD_LEARNING_FEEDER_V1_01

PARALLÈLE NON BLOQUANT:
  6. GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01
  7. Airtable / ClickUp / LocalCMS children selon disponibilité machine
```

---

## 12_INVARIANTS

```text
NO_WAN_EXPOSURE        = OpenClaw reste loopback-only
NO_LIVE_TRADE_WITHOUT_GATE = aucun trade sans validation_gate active
NO_OPENCLAW_ORCHESTRATE = OpenClaw n'orchestre jamais opt-trading
NO_DIRECT_SIGNAL_TRADE  = signal TradingView jamais exécuté sans proposition_engine
NO_SECRET_IN_LOGS       = aucune clé/token dans les logs ou docs
NO_GLOBAL_INDEX_AUTO    = GO_INDEX/ACTIVE_STREAMS non modifiés sans delta prouvé
```

---

## 17_RESUME_POINT

```text
CURRENT_STATE =
  GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_IMPL_V1_01 = PASS
  GO_OPT_TRADING_ORCHESTRATOR_CHILD_SIGNAL_ROUTER_V1_01 = PASS
  GO_OPT_TRADING_ORCHESTRATOR_CHILD_NOTIFICATION_DISPATCHER_V1_01 = PASS
  GO_OPT_TRADING_ORCHESTRATOR_CHILD_PROPOSITION_ENGINE_V1_01 = PASS

NEXT_REAL_GO =
  GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01

PARENTS_OUVERTS_À_CONSERVER:
  GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
  GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01
  GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01
  GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01
  GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01
```

## RISKS

- À qualifier.
