---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01_OPERATIONAL
doc_type: operational_plan
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
status: open
updated_at: 2026-05-16
---

# 05_OPERATIONAL_RUNTIME_PLAN

## Objet

Documenter ce qui tourne réellement (opérationnel prouvé), ce qui est implémenté mais non prouvé runtime,
et ce qui est seulement documenté ou spécifié. Mapping machine / surface / owner / healthcheck.

---

## NIVEAUX DE CONFIANCE OPÉRATIONNELLE

```text
NIVEAU 3 — OPÉRATIONNEL PROUVÉ   : PASS documenté, cmd.sh validé, ou smoke attesté en prod
NIVEAU 2 — IMPLÉMENTÉ NON PROUVÉ : code présent (app/, cmd.sh), aucun PASS doc
NIVEAU 1 — DOCUMENTÉ SEULEMENT   : spec / chantier existant, impl absente ou partielle
NIVEAU 0 — À PRODUIRE            : absent ou spécifié seulement
```

---

## COUCHE OPENCLAW / RUNTIME IA

| Surface | Niveau | Machine | Owner | Healthcheck |
| --- | --- | --- | --- | --- |
| `gateway_openclaw` | **3** | db-layer | openclaw (user dédié) | `GET /health → {"ok":true,"status":"live"}` |
| `openclaw_operator_bridge` | **0** | db-layer | — | aucun (non implémenté) |
| `menu_openclaw` | **2** | db-layer | ghost | script menu — non prouvé bout-en-bout |
| `model_provider_openclaw` | **2** | db-layer | ghost | non prouvé |
| `configure_openclaw` | **2** | db-layer | ghost | non prouvé |
| `doctor_openclaw` | **2** | db-layer | ghost | non prouvé |
| `validated_prompt_factory` | **3** | db-layer | ghost | cmd.sh sanity PASS |
| `memory_bricks` | **3** | db-layer | ghost | cmd.sh sanity PASS |

### Gateway — détails runtime

```text
PORT:       ws://127.0.0.1:18789 (loopback uniquement — NO_WAN_EXPOSURE)
USER:       openclaw (dédié — jamais sudo, jamais ghost)
TMUX:       session openclaw-gateway
START:      gateway_openclaw/cmd.sh start
STOP:       gateway_openclaw/cmd.sh stop
ATTACH:     gateway_openclaw/cmd.sh attach
HEALTH:     gateway_openclaw/cmd.sh health → {"ok":true,"status":"live"}
INVOCATION: openclaw agent --agent builder --json (as ghost uniquement)
INVARIANT:  openclaw n'orchestre jamais opt-trading
```

---

## COUCHE TMUX (SUPERVISION)

```text
STATUT: OPÉRATIONNEL — chaîne tmux supervisions PASS (mergée sot/mainline)
BACKBONE: tmux est la colonne vertébrale runtime OpenClaw
SESSION ACTIVE CONNUE: openclaw-gateway
AUTRES SESSIONS: à déployer (voir 09_TMUX_RUNTIME_SPINE_PLAN.md)
```

---

## COUCHE INFRA / CONNECTIVITÉ

| Surface | Niveau | Machine | Owner | Healthcheck |
| --- | --- | --- | --- | --- |
| `reseau_ssh` | **3** | all | ghost | scripts/reseau_ssh/scripts/ |
| `reseau_ssh_step1b` | **2** | all | ghost | compat — deprecated |
| `shared_files_sftp` | **2** | all | ghost | non prouvé |
| `shared_sshfs_permanent` | **2** | all | ghost | non prouvé |
| `auth` | **2** | all | ghost | non prouvé |
| `health` | **2** | all | ghost | non prouvé |
| `machines_registry_reader` | **2** | all | ghost | non prouvé |

---

## COUCHE DESK PRO / UI TRADING

| Surface | Niveau | Machine | Owner | Healthcheck |
| --- | --- | --- | --- | --- |
| `desk_pro` | **3** | admin-trading | ghost | FastAPI actif — smoke PASS |
| `desk_pro_runner` | **3** | admin-trading | ghost | cmd.sh run / run-and-show |
| `desk_pro_orchestrator` | **3** | admin-trading | ghost | cmd.sh PASS |
| `desk_pro_dashboard` | **2** | admin-trading | ghost | non prouvé |
| `bot_vision` | **3** | admin-trading | ghost | smoke PASS admin-trading |
| `bot_vision_step2` | **2** | admin-trading | ghost | non prouvé |
| `vision_bot` | **2** | admin-trading | ghost | non prouvé |
| `perf` | **3** | admin-trading | ghost | shim cmd.sh PASS |
| `perf_engine` | **2** | admin-trading | ghost | non prouvé |
| `journal_engine` | **2** | admin-trading | ghost | non prouvé |

---

## COUCHE TRADING / EXCHANGE

| Surface | Niveau | Machine | Owner | Healthcheck |
| --- | --- | --- | --- | --- |
| `simex_bitget_bridge` | **3** | admin-trading | ghost | cmd.sh sanity PASS (SIMEX_UNITS_V1) |
| `kil_v1` | **3** | admin-trading | ghost | cmd.sh PASS (kill switch) |
| `webhook` | **2** | admin-trading | ghost | handlers.py — non prouvé bout-en-bout |
| `tradingview_observer` | **3** | admin-trading (Windows) | ghost | PASS (export PS1) |

### Moteurs trading (non prouvés runtime)

| Moteur | Niveau | Note |
| --- | --- | --- |
| `execution_engine` | **2** | impl app/ — runtime non attesté |
| `decision_engine` | **2** | impl app/ — runtime non attesté |
| `risk_engine` | **2** | impl app/ — runtime non attesté |
| `position_engine` | **2** | impl app/ — runtime non attesté |
| `portfolio_engine` | **2** | impl app/ — runtime non attesté |
| `opportunity_ranker` | **2** | impl app/ — runtime non attesté |
| `probability_engine` | **2** | impl app/ — runtime non attesté |
| `trading_realtime_v1` | **2** | impl app/ — runtime non attesté |
| `trading_lab_v1` | **2** | impl app/ — runtime non attesté |

```text
GATE PRÉ-PROPOSITION-ENGINE :
Valider opérationnel de decision_engine + risk_engine + execution_engine
AVANT d'ouvrir GO_OPT_TRADING_ORCHESTRATOR_CHILD_PROPOSITION_ENGINE_V1_01
```

---

## COUCHE MARKET DATA

| Surface | Niveau | Machine | Owner | Healthcheck |
| --- | --- | --- | --- | --- |
| `collector_binance_spot` | **2** | admin-trading | ghost | V1 minimal — partiel |
| `collector_coingecko` | **2** | admin-trading | ghost | non prouvé |
| `derivatives_collector` | **2** | admin-trading | ghost | non prouvé |
| `derivatives_analyzer` | **2** | admin-trading | ghost | non prouvé |
| `liquidation_analyzer` | **2** | admin-trading | ghost | non prouvé |
| `marketdata` | **2** | admin-trading | ghost | non prouvé |
| `market_scanner` | **2** | admin-trading | ghost | non prouvé |

---

## COUCHE APPS EXTERNES

| App | Niveau | Owner | Healthcheck |
| --- | --- | --- | --- |
| TradingView webhooks | **3** | — | webhook opérationnel (admin-trading) |
| Telegram | **3** | — | notification enable PASS |
| Airtable | **1** | — | GO ouvert, impl à produire |
| ClickUp | **1** | — | GO ouvert, impl à produire |
| Botpress | **2** | — | impl PASS — E2E Telegram non fermé |
| Google Sheets | **0** | — | non initié |
| Figma | **0** | — | différé |
| LocalCMS consumer | **1** | ghost | realignment done — cockpit à produire |

---

## COUCHE AI / PROVIDERS

| Surface | Niveau | Machine | Owner | Note |
| --- | --- | --- | --- | --- |
| `gateway_openclaw` (builder) | **3** | db-layer | openclaw | PRIMARY provider |
| `deepseek_hub` | **2** | db-layer | ghost | alternatif |
| `deepseek_thinking` | **2** | db-layer | ghost | thinking mode |
| `hf_free_platform` | **2** | db-layer | ghost | HF gratuit |
| `deepseek_student` | **0** | — | — | CLOSED définitif |
| `mimo_open_observer` | **0** | — | — | CLOSED définitif |

---

## WORKERS STRICTS (À PRODUIRE — NIVEAU 0)

```text
Aucun worker strict pipeline n'est opérationnel aujourd'hui.
Ils sont à produire comme modules nouveaux wrappant les moteurs existants.

signal_router              → 0 — à produire
proposition_engine         → 0 — à produire (débloqué par operator_bridge)
validation_gate            → 0 — à produire (débloqué par proposition_engine)
trade_executor             → 0 — à produire (débloqué par validation_gate)
result_tracker             → 0 — à produire (débloqué par trade_executor)
datasheet_writer           → 0 — à produire (débloqué par result_tracker)
learning_feeder            → 0 — à produire (débloqué par operator_bridge + result_tracker)
notification_dispatcher    → 0 — à produire (indépendant — Telegram OPÉRATIONNEL)
task_tracker               → 0 — à produire (indépendant — ClickUp OUVERT)
```

---

## MAPPING MACHINE — RÉSUMÉ

```text
MACHINE: db-layer
  → OpenClaw gateway (opérationnel)
  → validated_prompt_factory (opérationnel)
  → memory_bricks (opérationnel)
  → LocalCMS consumer (à cockpiter)
  → reseau_ssh (opérationnel)

MACHINE: admin-trading
  → desk_pro / desk_pro_runner / desk_pro_orchestrator (opérationnel)
  → bot_vision (opérationnel)
  → perf shim (opérationnel)
  → simex_bitget_bridge (opérationnel)
  → kil_v1 (opérationnel)
  → tradingview_observer (opérationnel, Windows)
  → webhook (impl — non prouvé bout-en-bout)
  → market data collectors (impl — non prouvés)
  → trading engines (impl — non prouvés)
```

---

## HEALTHCHECKS PRIORITAIRES À IMPLÉMENTER

```text
1. openclaw_operator_bridge   → /health JSON (à créer avec l'impl)
2. signal_router              → /health + signal count
3. trading engines (smoke)    → decision/risk/execution smoke test
4. market data collectors     → collector_binance_spot smoke
5. notification_dispatcher    → Telegram ping test
6. webhook                    → POST test signal TradingView format
```

## RISKS

- À qualifier.
