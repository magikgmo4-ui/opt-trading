---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01_TMUX
doc_type: runtime_plan
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
status: open
updated_at: 2026-05-16
---

# 09_TMUX_RUNTIME_SPINE_PLAN

## Objet

Faire de TMUX la colonne vertébrale runtime d'OpenClaw et du pipeline opt-trading.
Définir les sessions canoniques, panes, logs, restart policy, worker ownership, et healthchecks.

---

## PRINCIPE FONDAMENTAL

```text
TMUX = colonne vertébrale runtime (supervision + isolation)
OpenClaw = orchestrateur IA (s'exécute dans une session TMUX dédiée)
LocalCMS = UI centrale (lit l'état des sessions TMUX)
Desk Pro = UI trading (sessions admin-trading)

RÈGLE:
  Chaque process long-running = 1 pane TMUX nommé
  Chaque session = 1 domaine fonctionnel isolé
  Restart = via script dédié, jamais manuel ad-hoc
  Logs = redirigés vers fichier nommé par session/pane
```

---

## SESSIONS CANONIQUES

### SESSION 1 — openclaw-core (db-layer)

```text
NOM: openclaw-core
MACHINE: db-layer
USER: ghost (accès gateway en tant que ghost)
PANES:
  core:gateway  → gateway_openclaw cmd.sh attach (process openclaw user)
  core:bridge   → openclaw_operator_bridge (à créer — GO-01)
  core:health   → boucle health check gateway + bridge (30s)
  core:logs     → tail -f logs/openclaw-core.log

RESTART POLICY:
  gateway: restart si /health DOWN → gateway_openclaw/cmd.sh restart
  bridge:  restart si /health DOWN → openclaw_operator_bridge/cmd.sh restart

LOGS:
  gateway → logs/gateway_openclaw.log
  bridge  → logs/openclaw_operator_bridge.log

HEALTHCHECK:
  GET ws://127.0.0.1:18789/health → {"ok":true,"status":"live"}
  GET localhost:{BRIDGE_PORT}/health → {"ok":true}
```

### SESSION 2 — screeners (admin-trading)

```text
NOM: screeners
MACHINE: admin-trading
USER: ghost
PANES:
  screeners:tradingview  → tradingview_observer (watch alertes)
  screeners:webhook      → webhook handler (HTTP listener)
  screeners:bot_vision   → bot_vision (daemon capture screenshots)
  screeners:telegram     → notification_dispatcher (Telegram bot)

RESTART POLICY:
  tradingview_observer: restart si process mort
  webhook: restart si port non listenné
  bot_vision: restart si daemon mort
  telegram: restart si bot offline

LOGS:
  tradingview → logs/tradingview_observer.log
  webhook     → logs/webhook.log
  bot_vision  → logs/bot_vision.log
  telegram    → logs/notification_dispatcher.log
```

### SESSION 3 — strict-workers (admin-trading ou db-layer)

```text
NOM: strict-workers
MACHINE: admin-trading (trading workers) + db-layer (learning worker)
USER: ghost
PANES:
  workers:signal_router     → modules/signal_router/ (HTTP listener)
  workers:notification      → modules/notification_dispatcher/
  workers:proposition       → modules/proposition_engine/ (débloqué par bridge)
  workers:validation        → modules/validation_gate/
  workers:executor          → modules/trade_executor/
  workers:result_tracker    → modules/result_tracker/
  workers:datasheet         → modules/datasheet_writer/
  workers:learning          → modules/learning_feeder/ (db-layer)

NOTE: panes créés au fur et à mesure des GO pipeline.
      Session créée dès GO-03 (signal_router).

RESTART POLICY:
  chaque worker: restart si /health DOWN → worker/cmd.sh restart
  pas de restart automatique pour trade_executor (safety: éviter double trade)

LOGS:
  chaque worker → logs/{worker_name}.log
```

### SESSION 4 — trading-pipeline (admin-trading)

```text
NOM: trading-pipeline
MACHINE: admin-trading
USER: ghost
PANES:
  pipeline:kil_v1           → kil_v1 (monitor kill switch état)
  pipeline:simex_bridge     → simex_bitget_bridge (état connexion exchange)
  pipeline:execution        → execution_engine (monitor)
  pipeline:risk             → risk_engine (monitor)
  pipeline:position         → position_engine (monitor)

NOTE: panes créés après smoke des moteurs (gate pré-proposition_engine).

RESTART POLICY:
  kil_v1: NE PAS restart automatiquement (kill switch = safety device)
  simex_bridge: restart si connexion exchange perdue
  engines: restart manuel uniquement (stateful)

LOGS:
  kil_v1       → logs/kil_v1.log
  simex_bridge → logs/simex_bitget_bridge.log
```

### SESSION 5 — market-data (admin-trading)

```text
NOM: market-data
MACHINE: admin-trading
USER: ghost
PANES:
  mdata:binance     → collector_binance_spot (daemon)
  mdata:coingecko   → collector_coingecko (daemon)
  mdata:derivatives → derivatives_collector (daemon)
  mdata:analyzers   → derivatives_analyzer + liquidation_analyzer
  mdata:scanner     → market_scanner (orchestrateur collectors)
  mdata:hub         → marketdata (hub données central)

RESTART POLICY:
  collectors: restart si daemon mort ou erreur fetch > seuil
  analyzers: restart si process mort
  scanner + hub: restart si process mort

LOGS:
  par collector → logs/{collector_name}.log
  scanner       → logs/market_scanner.log
  hub           → logs/marketdata.log
```

### SESSION 6 — apps-connectors (db-layer)

```text
NOM: apps-connectors
MACHINE: db-layer
USER: ghost
PANES:
  apps:airtable   → task_tracker Airtable sync
  apps:clickup    → task_tracker ClickUp sync
  apps:sheets     → datasheet_writer Sheets sync
  apps:health     → boucle health check apps externes (5 min)

NOTE: panes créés au fil des GO (datasheet GO-09, task_tracker GO-09).

LOGS:
  airtable → logs/airtable_sync.log
  clickup  → logs/clickup_sync.log
  sheets   → logs/sheets_sync.log
```

### SESSION 7 — desk-pro (admin-trading)

```text
NOM: desk-pro
MACHINE: admin-trading
USER: ghost
PANES:
  desk:runner        → desk_pro_runner cmd.sh run-and-show
  desk:orchestrator  → desk_pro_orchestrator (conductor)
  desk:perf          → perf cmd.sh (shim → perf_engine)
  desk:logs          → tail -f logs/desk_pro.log

RESTART POLICY:
  desk_pro: restart si FastAPI port non listenné
  perf: restart si process mort

LOGS:
  desk_pro → logs/desk_pro.log
  perf     → logs/perf.log
```

### SESSION 8 — kg-repo (db-layer)

```text
NOM: kg-repo
MACHINE: db-layer
USER: ghost
PANES:
  kg:memory_bricks     → memory_bricks (learning store daemon)
  kg:learning_feeder   → modules/learning_feeder/ (post GO-10)
  kg:health            → boucle health check learning store

NOTE: session créée dès GO-10 (learning_feeder).

LOGS:
  memory_bricks  → logs/memory_bricks.log
  learning_feeder → logs/learning_feeder.log
```

### SESSION 9 — localcms-ui (db-layer)

```text
NOM: localcms-ui
MACHINE: db-layer
USER: ghost
PANES:
  lcms:consumer   → localcms_consumer (FastAPI)
  lcms:health     → boucle health check UI
  lcms:logs       → tail -f logs/localcms.log

RESTART POLICY:
  restart si FastAPI port non listenné

LOGS:
  localcms → logs/localcms_consumer.log
```

---

## HEALTH AGGREGATOR TMUX

```text
SCRIPT: scripts/tmux/health_aggregator.sh
RÔLE: vérifie que toutes les sessions canoniques sont actives
FRÉQUENCE: toutes les 60s
OUTPUT:
  → stdout: SESSION_OK ou SESSION_MISSING par session
  → log: logs/tmux_health.log
  → notification: Telegram si session critique DOWN
SESSIONS CRITIQUES: openclaw-core, screeners, strict-workers
SESSIONS NON CRITIQUES: kg-repo, localcms-ui (peuvent être down sans alerte immédiate)
```

---

## RESTART POLICY GLOBALE

```text
AUTOMATIQUE (restart si DOWN):
  gateway_openclaw   → safety: bridge appelle gateway, pas de trade
  openclaw_operator_bridge
  notification_dispatcher (Telegram)
  signal_router
  market data collectors
  desk_pro (FastAPI)
  localcms_consumer (FastAPI)

MANUEL UNIQUEMENT:
  kil_v1             → safety device — jamais auto-restart
  trade_executor     → safety — éviter double trade
  trading engines    → stateful — restart manuel après investigation

SUPERVISÉ:
  proposition_engine → restart après investigation si FAIL (données perdues)
  validation_gate    → restart après investigation (approbation en attente ?)
```

---

## LOGS — CONVENTION

```text
RÉPERTOIRE: logs/ (relatif à la racine du module ou scripts/tmux/logs/)
FORMAT NOM: {module_name}.log
ROTATION: logrotate ou équivalent (à configurer par session)
LEVEL: INFO par défaut, DEBUG si TMUX_DEBUG=1
RETENTION: 7 jours par défaut
NO_SECRET_IN_LOGS: aucune clé/token dans les logs
```

---

## SCRIPTS REQUIS

```text
scripts/tmux/
  start_all.sh           → démarrer toutes les sessions (ordre: openclaw-core first)
  stop_all.sh            → arrêter toutes les sessions (ordre inverse)
  restart_session.sh     → restart une session par nom
  health_aggregator.sh   → vérifier toutes sessions
  attach.sh              → attacher à une session nommée

Par session:
  scripts/tmux/sessions/
    openclaw-core.sh     → créer session openclaw-core
    screeners.sh         → créer session screeners
    strict-workers.sh    → créer session strict-workers
    trading-pipeline.sh  → créer session trading-pipeline
    market-data.sh       → créer session market-data
    apps-connectors.sh   → créer session apps-connectors
    desk-pro.sh          → créer session desk-pro
    kg-repo.sh           → créer session kg-repo
    localcms-ui.sh       → créer session localcms-ui
```

---

## GO REQUIS

```text
GO_OPENCLAW_OPT_TRADING_TMUX_RUNTIME_SPINE_01
SCOPE:
  - Créer scripts/tmux/sessions/ avec les 9 sessions
  - Implémenter start_all.sh + stop_all.sh + health_aggregator.sh
  - Démarrer openclaw-core + screeners sur db-layer + admin-trading
  - Valider TMUX health aggregator → Telegram notification PASS
LIVRABLE: 9 sessions définies, openclaw-core + screeners actifs
PRÉREQ: gateway_openclaw opérationnel (DONE)
BLOQUE: LocalCMS VUE 2 (TMUX sessions map)
MACHINE: db-layer + admin-trading
```

---

## ARCHITECTURE GLOBALE — RÉSUMÉ

```text
TMUX SPINE (colonne vertébrale):

  db-layer:
    openclaw-core     → gateway + bridge (runtime IA)
    apps-connectors   → Airtable + ClickUp + Sheets sync
    kg-repo           → memory_bricks + learning_feeder
    localcms-ui       → UI centrale système

  admin-trading:
    screeners         → TradingView + webhook + bot_vision + Telegram
    strict-workers    → signal_router → proposition → validation → trade → result → datasheet
    trading-pipeline  → kil_v1 + simex + execution + risk + position
    market-data       → collectors + analyzers + scanner + hub
    desk-pro          → desk_pro + perf + orchestrator

SUPERVISION:
  health_aggregator → vérifie toutes sessions
  → alerte Telegram si session critique DOWN

UI:
  LocalCMS → lit état TMUX sessions
  Desk Pro → UI trading (indépendant de TMUX spine)
```
