---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01_RUNTIME_STATE
doc_type: runtime_state
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 10_DESK_PRO_RUNTIME_STATE - Desk Pro Runtime State (read-only)

Observation le 2026-05-06. Aucun service modifié.

## Modules Desk Pro présents

| Module | Path | Role |
| --- | --- | --- |
| desk_pro | `modules/desk_pro/` | Core: models, aggregator, scoring, UI, API |
| desk_pro_runner | `modules/desk_pro_runner/` | Orchestration entry point (run, dashboard, export) |
| desk_pro_orchestrator | `modules/desk_pro_orchestrator/` | Pipeline executor (11 modules en séquence) |
| desk_pro_dashboard | `modules/desk_pro_dashboard/` | Dashboard rendering (HTML/JSON export) |
| desk_analyze | `modules/desk_analyze/` | Analyse on-demand (OpenAI vision + Binance market data) |
| desk_snapshot_ingest | `modules/desk_snapshot_ingest/` | Ingestion snapshots inbox → desk/snapshots/ |
| desk_state | `modules/desk_state/` | Aggregation état global (snapshots + tv_inputs + coinglass) |
| desk_capture_inputs | `modules/desk_capture_inputs/` | Extraction inputs TradingView |
| desk_common | `modules/desk_common/` | Shared paths/utilities |
| desk_retention | `modules/desk_retention/` | Rétention/cleanup données |

## Desk Pro n'est PAS un service systemd

Desk Pro est un pipeline **manuel/on-demand**, pas un service long-running :
- Pas de `desk_pro.service` dans systemd
- Exécution via `cmd-desk_pro_runner run` ou `desk_pro_orchestrator run`
- Mode: `PAPER` (configurable)
- Output: `data/desk_runs/desk_run_{timestamp}/`

## Derniers runs connus

| Run ID | Timestamp | Modules OK | Modules Failed | Location |
| --- | --- | --- | --- | --- |
| `desk_run_20260504_234500` | 2026-05-04 23:45 UTC | 11 | 0 | `data/desk_runs/` |
| `desk_run_20260504_193959` | 2026-05-04 19:39 UTC | — | — | `data/desk_runs/` |
| `desk_run_20260405_010912` | 2026-04-05 01:09 UTC | — | — | `data/desk_runs/` |

Dernier run observé: **2026-05-04** (récent, contrairement au GAP-01 du parent review qui datait de 2026-04-05).

## Fichiers latest présents

### desk/snapshots/latest.json

| Champ | Valeur |
| --- | --- |
| Path | `/opt/trading/desk/snapshots/latest.json` |
| Last modified | 2026-05-06 03:55:46 EDT |
| Symbols | BTCUSDT.P, ETHUSDT.P, SOLUSDT.P, XAUUSD |
| Format | `{symbol: {symbol, tf, snapshot_ts, path, ingested_at, source, host}}` |
| Freshness | **FRAIS** — mis à jour par desk_bridge toutes les ~10min |

### desk/state/latest.json

| Champ | Valeur |
| --- | --- |
| Path | `/opt/trading/desk/state/latest.json` |
| Last modified | 2026-03-03 18:13:50 EST |
| Schema | `desk_state.v1` |
| Content | snapshots + tv_inputs + coinglass_inputs + derived |
| Freshness | **STALE** — dernier update 2026-03-03 (> 2 mois) |

### desk/inputs/tv_inputs_latest.json

| Champ | Valeur |
| --- | --- |
| Path | `/opt/trading/desk/inputs/tv_inputs_latest.json` |
| Last modified | 2026-03-03 15:32:19 EST |
| Content | Extraction TV: price, RSI, EMA bias, structure, S/R |
| Freshness | **STALE** — dernier update 2026-03-03 |

### /shared/desk_pro/latest/

| Champ | Valeur |
| --- | --- |
| Path | `/shared/desk_pro/latest/` |
| Last modified | 2026-04-04 21:08 EDT |
| Content | `run_summary.json`, `dashboard_latest.html`, engine JSONs |
| Freshness | **STALE** — dernier export 2026-04-04 |

## Chemins d'artefacts confirmés

| Artifact | Path | Format | Status |
| --- | --- | --- | --- |
| Snapshots PNG | `desk/snapshots/{SYMBOL}/{SYMBOL}_H1_{ts}.png` | PNG | CONFIRMED |
| Snapshot index | `desk/snapshots/latest.json` | JSON | CONFIRMED, FRAIS |
| Snapshot history | `desk/snapshots/history.jsonl` | JSONL | CONFIRMED |
| State | `desk/state/latest.json` | JSON | CONFIRMED, STALE |
| TV inputs | `desk/inputs/tv_inputs_latest.json` | JSON | CONFIRMED, STALE |
| TV inputs history | `desk/inputs/tv_inputs_history.jsonl` | JSONL | CONFIRMED |
| Run outputs | `data/desk_runs/desk_run_{ts}/` | JSON per module | CONFIRMED |
| Shared export | `/shared/desk_pro/latest/` | JSON + HTML | CONFIRMED, STALE |

## Synthèse

Desk Pro est un consumer **disponible** mais **non automatisé**. Les inputs frais existent (`desk/snapshots/latest.json`), mais les agrégats (`desk/state/latest.json`, `/shared/desk_pro/latest/`) sont stale. Le pipeline fonctionne quand il est lancé manuellement.

## RISKS

- À qualifier.
