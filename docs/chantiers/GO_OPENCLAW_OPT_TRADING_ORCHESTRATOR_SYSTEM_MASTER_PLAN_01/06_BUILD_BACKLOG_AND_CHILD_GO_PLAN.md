---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01_BACKLOG
doc_type: backlog
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
status: open
updated_at: 2026-05-16
---

# 06_BUILD_BACKLOG_AND_CHILD_GO_PLAN

## Objet

Convertir les gaps du master plan en child GO exécutables.
Ordre bloquant, dépendances, phase de livraison.

---

## RÈGLE SÉQUENÇAGE

```text
BLOQUANT = ce GO doit être FERMÉ avant d'ouvrir le suivant
PARALLÈLE = peut s'ouvrir simultanément, aucune dépendance technique
DIFFÉRÉ = ouvrir uniquement après les prérequis listés
```

---

## PHASE 1 — DÉBLOQUANT ABSOLU

### GO-01 — Operator Bridge V1

```text
GO_ID:    GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_IMPL_V1_01
STATUT:   À OUVRIR (PRIORITÉ 1)
SCOPE:
  - Implémenter modules/openclaw_operator_bridge/
  - Contrat JSON in/out (voir 04_OPERATOR_BRIDGE_SPEC.md)
  - Whitelist actions : ask, build, evaluate, review
  - Healthcheck : GET /health → {"ok":true}
  - Invocation builder : openclaw agent --agent builder --json (as ghost)
  - Tests : appel mock + appel réel gateway
LIVRABLE:
  modules/openclaw_operator_bridge/ opérationnel local
  smoke PASS sur db-layer
PRÉREQ:   Gateway opérationnel (DONE)
BLOQUE:   proposition_engine, learning_feeder, openclaw_runtime_consolidation
MACHINE:  db-layer
```

---

## PHASE 2 — PARALLÈLE IMMÉDIAT (aucun préreq technique)

### GO-02 — TMUX Runtime Spine

```text
GO_ID:    GO_OPENCLAW_OPT_TRADING_TMUX_RUNTIME_SPINE_01
STATUT:   À OUVRIR (parallèle GO-01)
SCOPE:
  - Définir sessions TMUX canoniques (voir 09_TMUX_RUNTIME_SPINE_PLAN.md)
  - Scripts start/stop/attach/restart par session
  - Session openclaw-core (gateway + bridge)
  - Session screeners (TradingView, Telegram, bot_vision)
  - Session strict-workers (workers pipeline à mesure qu'ils sont créés)
  - Health aggregator TMUX
LIVRABLE:
  scripts/tmux/ avec sessions canoniques
  smoke PASS db-layer (openclaw-core) + admin-trading (screeners)
PRÉREQ:   Gateway opérationnel (DONE)
BLOQUE:   rien — mais améliore supervision de tout le reste
MACHINE:  db-layer + admin-trading
```

### GO-03 — Signal Router V1

```text
GO_ID:    GO_OPT_TRADING_ORCHESTRATOR_CHILD_SIGNAL_ROUTER_V1_01
STATUT:   À OUVRIR (parallèle GO-01)
SCOPE:
  - Recevoir webhook TradingView POST
  - Valider format : {ticker, side, price, timestamp, strategy_id}
  - Normaliser → signal JSON canonique
  - Route vers proposition_engine (stub accepté en phase 1)
  - Intégration marketdata enrichissement (optionnel phase 1)
LIVRABLE:
  modules/signal_router/ opérationnel
  POST test webhook → signal JSON PASS
PRÉREQ:   aucun
BLOQUE:   proposition_engine (input)
MACHINE:  admin-trading
```

### GO-04 — Notification Dispatcher V1

```text
GO_ID:    GO_OPT_TRADING_ORCHESTRATOR_CHILD_NOTIFICATION_DISPATCHER_V1_01
STATUT:   À OUVRIR (parallèle GO-01)
SCOPE:
  - Telegram structuré par étape pipeline
  - Events : signal_reçu, proposition_générée, approbation_requise,
    trade_exécuté, résultat_connu, erreur_pipeline
  - Format message Telegram normalisé par event type
  - Stub intégration pour chaque étape pipeline
LIVRABLE:
  modules/notification_dispatcher/ opérationnel
  Telegram ping test PASS
PRÉREQ:   Telegram opérationnel (DONE)
BLOQUE:   validation_gate (approval flow), chaque étape pipeline
MACHINE:  db-layer ou admin-trading
```

### GO-05 — Market Data Pipeline Smoke

```text
GO_ID:    GO_OPT_TRADING_MARKET_DATA_PIPELINE_SMOKE_01
STATUT:   À OUVRIR (parallèle GO-01)
SCOPE:
  - Smoke collector_binance_spot → marketdata → market_scanner
  - Valider flux data jusqu'à signal enrichi
  - Documenter format signal enrichi (ticker + price + liquidation + dérivés)
  - Gate : si smoke FAIL → documenter gap avant d'ouvrir signal_router avancé
LIVRABLE:
  market data pipeline smoke PASS ou FAIL documenté
PRÉREQ:   aucun
BLOQUE:   signal_router avancé (enrichissement marketdata)
MACHINE:  admin-trading
```

---

## PHASE 3 — APRÈS BRIDGE (débloqué par GO-01)

### GO-06 — Proposition Engine V1

```text
GO_ID:    GO_OPT_TRADING_ORCHESTRATOR_CHILD_PROPOSITION_ENGINE_V1_01
STATUT:   DIFFÉRÉ (après GO-01)
SCOPE:
  - Wrapper decision_engine + opportunity_ranker + probability_engine
  - Appel OpenClaw builder via operator_bridge
  - Input : signal JSON (de signal_router)
  - Output : {action, size, entry, sl, tp, confidence, rationale}
  - Gate interne : smoke engines existants AVANT impl wrapper
LIVRABLE:
  modules/proposition_engine/ opérationnel
  signal JSON → proposition JSON PASS (avec gateway réel)
PRÉREQ:   GO-01 (operator_bridge) + GO-03 (signal_router)
BLOQUE:   validation_gate, trade_executor
MACHINE:  admin-trading ou db-layer
```

### GO-07 — Validation Gate V1

```text
GO_ID:    GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01
STATUT:   DIFFÉRÉ (après GO-06)
SCOPE:
  - Check risk_engine (limites configurées)
  - Check kil_v1 (kill switch actif ?)
  - Si auto-gate : appliquer règles risk limits
  - Si opérateur requis : notification Telegram via notification_dispatcher
  - Attente réponse Telegram (timeout configurable)
  - Output : APPROVED / REJECTED + motif
LIVRABLE:
  modules/validation_gate/ opérationnel
  gate auto PASS + gate Telegram approval PASS
PRÉREQ:   GO-06 (proposition_engine) + GO-04 (notification_dispatcher)
BLOQUE:   trade_executor
MACHINE:  admin-trading
INVARIANT: NO_LIVE_TRADE_WITHOUT_GATE — ce GO est non négociable avant live trading
```

---

## PHASE 4 — APRÈS VALIDATION (débloqué par GO-07)

### GO-08 — Trade Executor V1

```text
GO_ID:    GO_OPT_TRADING_ORCHESTRATOR_CHILD_TRADE_EXECUTOR_V1_01
STATUT:   DIFFÉRÉ (après GO-07)
SCOPE:
  - Input : proposition validée (APPROVED seulement)
  - Appel simex_bitget_bridge (SIMEX_UNITS_V1 contract)
  - Appel execution_engine
  - Output : {trade_id, fill_price, fill_qty, timestamp}
  - Notification Telegram via notification_dispatcher
LIVRABLE:
  modules/trade_executor/ opérationnel
  trade simulé PASS (simex dry-run mode)
PRÉREQ:   GO-07 (validation_gate)
BLOQUE:   result_tracker
MACHINE:  admin-trading
```

### GO-09 — Datasheet Sync Quotidien

```text
GO_ID:    GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_SYNC_DAILY_TRACKING_01
STATUT:   DIFFÉRÉ (après GO-08)
SCOPE:
  - Tracking quotidien gagnant/perdant (Google Sheets primaire)
  - Écriture Airtable (enregistrement orchestration)
  - Wrapper journal_engine → Sheets API
  - Format : ligne par trade → agrégat quotidien → hebdo
  - DB ingestion pipeline (governance docs existants)
LIVRABLE:
  modules/datasheet_writer/ opérationnel
  Sheets row write PASS
PRÉREQ:   GO-08 (trade_executor) → result_tracker débloqué
BLOQUE:   learning_feeder (contexte P&L)
MACHINE:  db-layer ou admin-trading
```

---

## PHASE 5 — LEARNING (débloqué par GO-01 + GO-09)

### GO-10 — Learning Feeder V1

```text
GO_ID:    GO_OPT_TRADING_ORCHESTRATOR_CHILD_LEARNING_FEEDER_V1_01
STATUT:   DIFFÉRÉ (après GO-01 + GO-09)
SCOPE:
  - Input : {signal, proposition, résultat, P&L}
  - Envoi via operator_bridge → OpenClaw builder
  - Stockage memory_bricks (learning store persistant)
  - Format feedback structuré
LIVRABLE:
  modules/learning_feeder/ opérationnel
  learning cycle PASS (gateway réel)
PRÉREQ:   GO-01 (operator_bridge) + GO-09 (datasheet → P&L disponible)
BLOQUE:   rien (terminal du pipeline)
MACHINE:  db-layer
```

---

## PHASE 6 — UI ET CONSOLIDATION

### GO-11 — LocalCMS UI Central Gap Bridge

```text
GO_ID:    GO_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_UI_CENTRAL_GAP_BRIDGE_01
STATUT:   DIFFÉRÉ (après GO-02 TMUX spine)
SCOPE:
  - LocalCMS comme UI centrale système / gouvernance
  - Vues : état runtime OpenClaw, TMUX sessions, workers stricts,
    apps externes, datasheet perf, GO roadmap, healthchecks
  - Voir 08_LOCALCMS_CENTRAL_UI_GAP_PLAN.md pour détail gaps
LIVRABLE:
  LocalCMS consumer avec vues état pipeline PASS
PRÉREQ:   GO-02 (TMUX spine) + signal_router + au moins 1 worker opérationnel
MACHINE:  db-layer
```

---

## BACKLOG CONSOLIDATION (voir 04_CONSOLIDATION_ROADMAP.md)

```text
PHASE 1 (parallèle aux GOs pipeline):
  GO_OPT_TRADING_DESK_PRO_CONSOLIDATION_01
  GO_OPT_TRADING_MARKET_DATA_PIPELINE_SMOKE_01 (= GO-05 ci-dessus)

PHASE 2:
  GO_OPENCLAW_OPT_TRADING_RUNTIME_CONSOLIDATION_01
  GO_OPT_TRADING_BOT_VISION_CONSOLIDATION_01

PHASE 3 (nettoyage):
  GO_OPT_TRADING_PERF_ENGINE_MIGRATION_01
  GO_OPT_TRADING_DEEPSEEK_CLEANUP_01
  GO_OPT_TRADING_OPS_MENUS_CLEANUP_01

PHASE 4 (basse priorité):
  GO_OPT_TRADING_REGISTRY_CONSOLIDATION_01
  GO_OPT_TRADING_SHARED_TRANSFER_VALIDATION_01
  GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 (DÉJÀ OUVERT)
```

---

## RÉSUMÉ — TABLEAU DE BORD CHILD GO

| # | GO_ID | Phase | Bloquant par | Bloque |
| --- | --- | --- | --- | --- |
| 01 | OPERATOR_BRIDGE_IMPL_V1 | 1 | — | 06, 10 |
| 02 | TMUX_RUNTIME_SPINE | 2 | — | 11 |
| 03 | SIGNAL_ROUTER_V1 | 2 | — | 06 |
| 04 | NOTIFICATION_DISPATCHER_V1 | 2 | — | 07, toutes notifs |
| 05 | MARKET_DATA_PIPELINE_SMOKE | 2 | — | 03 avancé |
| 06 | PROPOSITION_ENGINE_V1 | 3 | 01, 03 | 07 |
| 07 | VALIDATION_GATE_V1 | 3 | 06, 04 | 08 |
| 08 | TRADE_EXECUTOR_V1 | 4 | 07 | 09 |
| 09 | DATASHEET_SYNC_DAILY | 4 | 08 | 10 |
| 10 | LEARNING_FEEDER_V1 | 5 | 01, 09 | — |
| 11 | LOCALCMS_UI_CENTRAL_GAP | 6 | 02, 03 | — |

---

## 17_RESUME_POINT

```text
OUVRIR IMMÉDIATEMENT:
  GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_IMPL_V1_01   ← débloque tout le pipeline IA

EN PARALLÈLE (dès que bridge ouvert):
  GO_OPENCLAW_OPT_TRADING_TMUX_RUNTIME_SPINE_01
  GO_OPT_TRADING_ORCHESTRATOR_CHILD_SIGNAL_ROUTER_V1_01
  GO_OPT_TRADING_ORCHESTRATOR_CHILD_NOTIFICATION_DISPATCHER_V1_01
  GO_OPT_TRADING_MARKET_DATA_PIPELINE_SMOKE_01

GATE CRITIQUE AVANT PROPOSITION ENGINE:
  Valider opérationnel decision_engine + risk_engine + execution_engine
  (smoke test des moteurs existants avant de créer les workers)
```

## RISKS

- À qualifier.
