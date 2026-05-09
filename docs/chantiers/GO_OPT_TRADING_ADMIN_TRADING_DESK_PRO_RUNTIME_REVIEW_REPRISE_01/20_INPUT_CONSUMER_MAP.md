---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01_INPUT_CONSUMER_MAP
doc_type: input_consumer_map
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 20_INPUT_CONSUMER_MAP - Input Consumer Map

## Inputs potentiels de Desk Pro

### 1. desk_snapshot (CONFIRMED — input principal actuel)

| Champ | Valeur |
| --- | --- |
| Producer | `desk_snapshot_ingest` (via `desk_bridge`) |
| Path | `desk/snapshots/latest.json` |
| Format | JSON: `{symbol: {symbol, tf, snapshot_ts, path, ingested_at, source, host}}` |
| Freshness | **FRAIS** — mis à jour toutes les ~10min par desk_bridge |
| Consumer direct | `desk_state`, `desk_analyze`, Desk Pro orchestrator |
| Status | **CONFIRMED** |

### 2. signal_event (AVAILABLE — via events.jsonl)

| Champ | Valeur |
| --- | --- |
| Producer | `tv-webhook` (TradingView → POST /tv) |
| Path | `state/events.jsonl` |
| Format | JSONL: `{engine, signal, symbol, tf, _ts, price, sl, tp, ...}` |
| Freshness | Dépend des alertes TradingView (ad-hoc) |
| Consumer direct | Desk Pro futur (via mapping V0→V1) |
| Status | **AVAILABLE** — format V0, mapping V1 documenté |

### 3. visual_context (AVAILABLE — via snapshots + sidecar)

| Champ | Valeur |
| --- | --- |
| Producer | `bot_vision_headless` / ShareX (fallback) |
| Path | `desk/snapshots/{SYMBOL}/{SYMBOL}_H1_{ts}.png` + sidecar JSON |
| Format | PNG + JSON sidecar |
| Freshness | **FRAIS** — mis à jour par desk_bridge |
| Consumer direct | `desk_analyze` (OpenAI vision), Desk Pro dashboard |
| Status | **AVAILABLE** — consommé indirectement via snapshots |

### 4. tv_inputs (STALE — extraction TV)

| Champ | Valeur |
| --- | --- |
| Producer | `desk_capture_inputs` (`extract_tv_inputs.py`) |
| Path | `desk/inputs/tv_inputs_latest.json` |
| Format | JSON: `{ts_run, source, items: {symbol: {tv: {price, rsi, ema_bias, ...}}}}` |
| Freshness | **STALE** — dernier update 2026-03-03 |
| Consumer direct | `desk_state` |
| Status | **STALE** — extraction non relancée |

### 5. desk_state (STALE — agrégat global)

| Champ | Valeur |
| --- | --- |
| Producer | `desk_state` module |
| Path | `desk/state/latest.json` |
| Format | JSON: `{ts, host, timeframe, symbols, snapshots, tv_inputs, coinglass_inputs, derived, meta}` |
| Freshness | **STALE** — dernier update 2026-03-03 |
| Consumer direct | Desk Pro orchestrator, dashboard |
| Status | **STALE** — dépend de tv_inputs + coinglass_inputs |

### 6. desk_pro run outputs (AVAILABLE — on-demand)

| Champ | Valeur |
| --- | --- |
| Producer | `desk_pro_orchestrator` |
| Path | `data/desk_runs/desk_run_{ts}/` |
| Format | JSON per module (11 modules) + `run_summary.json` |
| Freshness | Dépend de la fréquence de lancement (manuel) |
| Consumer direct | `desk_pro_dashboard`, operator |
| Status | **AVAILABLE** — dernier run 2026-05-04 |

### 7. /shared/desk_pro/latest/ (STALE — export partagé)

| Champ | Valeur |
| --- | --- |
| Producer | `desk_pro_dashboard` (export) |
| Path | `/shared/desk_pro/latest/` |
| Format | JSON + HTML |
| Freshness | **STALE** — dernier export 2026-04-04 |
| Consumer direct | db-layer, student (via SSHFS) |
| Status | **STALE** |

## Matrice d'inputs

| Input | Producer | Path/ref | Format | Freshness | Status |
| --- | --- | --- | --- | --- | --- |
| desk_snapshot | desk_snapshot_ingest | `desk/snapshots/latest.json` | JSON | FRAIS (~10min) | CONFIRMED |
| signal_event | tv-webhook | `state/events.jsonl` | JSONL | ad-hoc | AVAILABLE (V0) |
| visual_context | headless/ShareX | `desk/snapshots/{SYMBOL}/` | PNG + JSON | FRAIS (~10min) | AVAILABLE |
| tv_inputs | desk_capture_inputs | `desk/inputs/tv_inputs_latest.json` | JSON | STALE (2 mois) | STALE |
| desk_state | desk_state | `desk/state/latest.json` | JSON | STALE (2 mois) | STALE |
| run outputs | desk_pro_orchestrator | `data/desk_runs/` | JSON | manuel | AVAILABLE |
| shared export | desk_pro_dashboard | `/shared/desk_pro/latest/` | JSON+HTML | STALE (1 mois) | STALE |

## Desk Pro consomme-t-il signal_event directement?

**Non, pas actuellement.** Le runtime Desk Pro ne lit pas `state/events.jsonl`. Il consomme :
1. `desk/snapshots/latest.json` (via `desk_state` ou directement)
2. `desk/inputs/tv_inputs_latest.json` (via `desk_state`)
3. Les modules internes (probability_engine, decision_engine, etc.) qui ont leurs propres inputs

Pour que Desk Pro consomme `signal_event` V1, un adapter serait nécessaire pour :
- Lire `state/events.jsonl`
- Mapper V0 → V1
- Exposer les signaux dans un format consumable par le pipeline

## Desk Pro consomme-t-il visual_context directement?

**Indirectement, oui.** `desk_analyze` (`analyze_latest.py`) consomme les PNG de `desk/snapshots/latest.json` pour l'analyse OpenAI vision. Le sidecar JSON n'est pas lu directement par Desk Pro.
