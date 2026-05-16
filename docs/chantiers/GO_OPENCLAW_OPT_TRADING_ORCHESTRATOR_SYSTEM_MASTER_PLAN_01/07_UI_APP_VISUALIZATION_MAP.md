---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01_UI_MAP
doc_type: ui_map
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
status: open
updated_at: 2026-05-16
---

# 07_UI_APP_VISUALIZATION_MAP

## Objet

Séparer ce qui est visible d'une UI ou d'une app (visuel, dashboard, chat, table)
de ce qui ne l'est pas (compute, data pipeline, infra, CLI).
Identifier les gaps de visualisation par surface.

---

## PRINCIPE DE SÉPARATION

```text
UI / APP VISUELLE = interface humain-machine avec rendu graphique ou textuel enrichi :
  → dashboards web (FastAPI, HTML, React, etc.)
  → screenshots / capture visuelle
  → apps externes (Telegram, ClickUp, Airtable, Sheets, Figma)
  → bots conversationnels (Botpress)
  → alertes visuelles (TradingView)

NON UI = traitement de données, infrastructure, runtime, CLI sans rendu utilisateur :
  → moteurs de calcul (trading engines)
  → pipelines data (market data)
  → runtime IA (OpenClaw gateway)
  → SSH / infra / registries
  → workers stricts (process internes)
```

---

## SURFACES AVEC UI / APP VISUELLE

### 1. Desk Pro — UI trading réelle

```text
SURFACE: desk_pro (FastAPI + HTML)
TYPE: dashboard web
URL: admin-trading (port configurable)
VUES ACTUELLES:
  → positions en cours
  → P&L brut
  → snapshots
  → bot_vision capture
VUES MANQUANTES:
  → état workers stricts (aucun worker existant)
  → état OpenClaw gateway
  → signal en cours
  → pipeline de décision en temps réel
OWNER: ghost (admin-trading)
STATUT: OPÉRATIONNEL
GAP: cockpit orchestration absent — Desk Pro est UI trading, pas UI système
```

### 2. Perf / Perf Engine — Tracking performance

```text
SURFACE: perf_app.py (web app)
TYPE: dashboard performance paper trading
INTÉGRATION: monté dans Desk Pro via mount.py
VUES ACTUELLES:
  → tracking ideas paper (perf_engine)
  → métriques performance
VUES MANQUANTES:
  → intégration P&L réel (post result_tracker)
  → comparaison paper vs live
STATUT: perf shim OPÉRATIONNEL — perf_engine non prouvé
GAP: migration perf → perf_engine à compléter avant vues live
```

### 3. Bot Vision — Capture visuelle screenshots

```text
SURFACE: bot_vision
TYPE: capture + analyse screenshot trading (admin-trading)
VUES:
  → capture screenshot TradingView
  → analyse visuelle interface
  → intégration desk_pro (observation)
STATUT: OPÉRATIONNEL (admin-trading)
GAP: step2 et vision_bot à consolider (voir 04_CONSOLIDATION_ROADMAP E3)
```

### 4. TradingView Observer — Interface graphique trading

```text
SURFACE: tradingview_observer (Windows + PS1)
TYPE: observation alertes + charts TradingView
INTÉGRATION: webhooks → signal_router
VUES:
  → charts TradingView
  → alertes configurées
  → export signal JSON
STATUT: OPÉRATIONNEL (admin-trading, Windows)
GAP: signal_router à brancher (reçoit le signal TradingView)
```

---

## APPS EXTERNES — VISUALISATION

### 5. Telegram — Notification + commandes opérateur

```text
TYPE: app messaging / bot
DIRECTION: bidirectionnel
VUES ACTUELLES:
  → notifications (enable PASS)
VUES MANQUANTES:
  → propositions formatées
  → boutons approbation/rejet
  → état pipeline en temps réel
  → alertes erreurs workers
STATUT: OPÉRATIONNEL (notification)
GAP: notification_dispatcher à produire pour vues structurées
```

### 6. Botpress — Bot conversationnel

```text
TYPE: bot conversationnel / workflow automation
DIRECTION: bidirectionnel (Botpress ↔ Telegram)
VUES ACTUELLES:
  → impl PASS (partiellement)
VUES MANQUANTES:
  → E2E Telegram/Botpress non fermé
  → commandes structurées pipeline
  → workflow approval opérateur
STATUT: impl PASS — E2E non fermé
GAP: GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01 à fermer
```

### 7. ClickUp — Suivi tâches et GO

```text
TYPE: task management UI
DIRECTION: écriture opt-trading → ClickUp
VUES ACTUELLES:
  → GO chantiers (manuel)
VUES MANQUANTES:
  → sync état pipeline automatique (task_tracker)
  → GO roadmap synchronisée
  → état workers stricts
STATUT: GO ouvert (CONTINUITY)
GAP: task_tracker worker à produire
```

### 8. Airtable — Base de données orchestration

```text
TYPE: database / spreadsheet UI
DIRECTION: lecture / écriture
TABLES CIBLES:
  → trades (historique)
  → propositions (avec statut validation)
  → signaux (archive TradingView)
  → learning_sessions (feedback OpenClaw)
VUES MANQUANTES:
  → tables à créer
  → datasheet_writer à brancher
STATUT: GO ouvert (AIRTABLE_ORCHESTRATION_PARENT)
GAP: tables non créées — datasheet_writer à produire
```

### 9. Google Sheets — Datasheet résultats / P&L

```text
TYPE: spreadsheet
DIRECTION: écriture opt-trading → Sheets
VUES CIBLES:
  → trade_results (par session, jour, stratégie)
  → pnl_summary (agrégé hebdo/mensuel)
  → signal_log (archive enrichie)
STATUT: NON INITIÉ
GAP: datasheet_writer à produire + Sheets API à intégrer
```

### 10. LocalCMS — UI centrale système

```text
TYPE: web UI lecture/gouvernance (db-layer consumer)
DIRECTION: lecture seule (données opt-trading)
VUES ACTUELLES:
  → realignment done — structure présente
VUES MANQUANTES:
  → état runtime OpenClaw
  → TMUX sessions
  → workers stricts (rôle, état, logs)
  → apps externes (état connexion)
  → datasheet performance
  → KG repo
  → GO roadmap cockpit
  → healthchecks centralisés
STATUT: REALIGNMENT DONE — cockpit à produire
GAP: voir 08_LOCALCMS_CENTRAL_UI_GAP_PLAN.md
RÔLE: UI centrale SYSTÈME (distinct de Desk Pro = UI trading)
```

### 11. Figma — Design / Wireframes

```text
TYPE: design tool (référence)
USAGE: wireframes LocalCMS + dashboards reporting
INTÉGRATION: lecture seule — pas d'API active pipeline
STATUT: NON INTÉGRÉ
GAP: différé — chantier futur LocalCMS UI design
```

---

## SURFACES NON UI — TABLEAU COMPLET

### Pipeline trading (compute interne)

```text
execution_engine     → moteur calcul — CLI / API interne
decision_engine      → moteur décision — CLI / API interne
risk_engine          → moteur risque — CLI / API interne
position_engine      → moteur position — CLI / API interne
portfolio_engine     → moteur portfolio — CLI / API interne
opportunity_ranker   → ranker opportunités — CLI / API interne
probability_engine   → calcul probabilité — CLI / API interne
kil_v1               → kill switch — cmd.sh uniquement
simex_bitget_bridge  → exchange connector — cmd.sh SIMEX_UNITS_V1
trading_realtime_v1  → runtime réel — CLI / API interne
trading_lab_v1       → environnement test — CLI / API interne
webhook              → handler HTTP interne
```

### Market data (data pipeline)

```text
marketdata           → hub données — API interne
market_scanner       → scan — API interne
collector_binance_spot → collecte — daemon / cron
collector_coingecko  → collecte — daemon / cron
derivatives_collector → collecte — daemon / cron
derivatives_analyzer → analyse — API interne
liquidation_analyzer → analyse — API interne
```

### OpenClaw runtime (CLI / websocket loopback)

```text
gateway_openclaw     → ws://127.0.0.1:18789 — loopback uniquement
menu_openclaw        → CLI menus
model_provider_openclaw → routing modèle — CLI
configure_openclaw   → config — CLI
doctor_openclaw      → diagnostic — CLI
evidence_openclaw    → preuves — CLI
memory_bricks        → learning store — cmd.sh
validated_prompt_factory → prompt — CLI
```

### AI / Providers (CLI)

```text
deepseek_hub         → provider alternatif — CLI
deepseek_thinking    → thinking mode — CLI
hf_free_platform     → provider HF — CLI
```

### Workers stricts (process internes — à produire)

```text
signal_router              → process HTTP interne
proposition_engine         → process interne
validation_gate            → process interne
trade_executor             → process interne
result_tracker             → process interne
datasheet_writer           → process interne → Sheets (UI externe)
learning_feeder            → process interne
notification_dispatcher    → process interne → Telegram (UI externe)
task_tracker               → process interne → ClickUp (UI externe)
```

### Infra (infrastructure sans rendu)

```text
reseau_ssh           → SSH backbone
shared_files_sftp    → SFTP transfert
shared_sshfs_permanent → SSHFS mount
auth                 → authentification
health               → health checks
git_fleet_guard      → guard fleet
registry_*           → registry readers
naming_normalizer    → normalisation
ops_menu_hub         → CLI menus
ops_super_menu       → CLI menus
```

---

## MATRICE GAP UI — RÉSUMÉ

| Surface | UI actuelle | Gap visualisation | GO requis |
| --- | --- | --- | --- |
| Desk Pro | OUI — dashboard trading | workers stricts absents | GO-DESK_PRO_CONSOLIDATION |
| Perf | OUI — app web | migration perf_engine | GO-PERF_ENGINE_MIGRATION |
| Bot Vision | OUI — screenshots | step2/vision_bot à consolider | GO-BOT_VISION_CONSOLIDATION |
| LocalCMS | OUI — structure | cockpit système complet | GO-11 LOCALCMS_UI_CENTRAL |
| Figma | OUI — wireframes | connecteur différé | différé |
| ClickUp | OUI — tâches | task_tracker à produire | GO-TASK_TRACKER |
| Airtable | OUI — tables | datasheet_writer + tables | GO-09 DATASHEET |
| Google Sheets | OUI — spreadsheet | datasheet_writer + Sheets API | GO-09 DATASHEET |
| Botpress | OUI — bot chat | E2E Telegram non fermé | BOTPRESS_SMOKE_E2E |
| Telegram | OUI — notification | notification_dispatcher | GO-04 DISPATCHER |
| TradingView | OUI — charts/alertes | signal_router à brancher | GO-03 SIGNAL_ROUTER |
