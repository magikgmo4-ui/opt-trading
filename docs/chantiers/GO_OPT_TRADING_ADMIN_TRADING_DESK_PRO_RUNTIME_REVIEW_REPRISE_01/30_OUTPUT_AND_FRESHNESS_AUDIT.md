---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01_OUTPUT_FRESHNESS
doc_type: output_and_freshness_audit
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 30_OUTPUT_AND_FRESHNESS_AUDIT - Output and Freshness Audit

## Outputs Desk Pro

### 1. Run Summary JSON

| Champ | Valeur |
| --- | --- |
| Output | `data/desk_runs/desk_run_{ts}/run_summary.json` |
| Format | JSON: `{run_id, run_timestamp, mode, modules_executed, modules_ok, modules_failed, module_results, summary}` |
| Last updated | 2026-05-04 23:45 UTC |
| Consumer | operator, dashboard |
| Status | **AVAILABLE** |

### 2. Module Output JSONs

| Champ | Valeur |
| --- | --- |
| Output | `data/desk_runs/desk_run_{ts}/{module_name}.json` |
| Format | JSON (per module: market_scanner, probability_engine, decision_engine, etc.) |
| Last updated | 2026-05-04 23:45 UTC |
| Consumer | dashboard, operator |
| Status | **AVAILABLE** |

### 3. Dashboard HTML

| Champ | Valeur |
| --- | --- |
| Output | `/shared/desk_pro/latest/dashboard_latest.html` |
| Format | HTML |
| Last updated | 2026-04-04 21:08 EDT |
| Consumer | operator (browser) |
| Status | **STALE** |

### 4. Shared Export (run_summary, engine JSONs)

| Champ | Valeur |
| --- | --- |
| Output | `/shared/desk_pro/latest/` |
| Format | JSON (`run_summary.json`, `journal_engine.json`, `perf_engine.json`, `portfolio_engine.json`) |
| Last updated | 2026-04-04 21:08 EDT |
| Consumer | db-layer, student (via SSHFS) |
| Status | **STALE** |

### 5. desk_state (agrégat)

| Champ | Valeur |
| --- | --- |
| Output | `desk/state/latest.json` + `desk/state/history.jsonl` |
| Format | JSON (desk_state.v1 schema) |
| Last updated | 2026-03-03 18:13 EST |
| Consumer | Desk Pro orchestrator, dashboard |
| Status | **STALE** |

### 6. desk_analyze (Telegram /analyze)

| Champ | Valeur |
| --- | --- |
| Output | Telegram message + `/srv/sftp/shared_files/shared/vision_outbox/analyze_{ts}.txt` |
| Format | Text/Markdown |
| Last updated | On-demand (Telegram trigger) |
| Consumer | operator (Telegram) |
| Status | **AVAILABLE** (on-demand) |

### 7. Snapshot Index (desk_snapshot_ingest output)

| Champ | Valeur |
| --- | --- |
| Output | `desk/snapshots/latest.json` + `desk/snapshots/history.jsonl` |
| Format | JSON + JSONL |
| Last updated | 2026-05-06 03:55:46 EDT |
| Consumer | desk_state, desk_analyze, Desk Pro |
| Status | **FRAIS** |

## Stale semantics

| Artifact | Stale threshold | Current age | Verdict |
| --- | --- | --- | --- |
| `desk/snapshots/latest.json` | > 30min (H1) | ~10min | **FRAIS** |
| `desk/state/latest.json` | > 45min (configurable `stale_min`) | > 2 mois | **STALE** |
| `desk/inputs/tv_inputs_latest.json` | > 45min | > 2 mois | **STALE** |
| `/shared/desk_pro/latest/` | > 24h | > 1 mois | **STALE** |
| `data/desk_runs/` (latest) | > 24h | ~10h | **STALE** (acceptable pour manuel) |

## Missing semantics

| Artifact | Missing? | Impact |
| --- | --- | --- |
| `shared/desk_pro/latest/` | NON (existe mais stale) | db-layer/student voient des données vieilles |
| `desk/inputs/coinglass_latest.json` | OUI (référence dans desk_state mais absent) | coinglass_inputs vide dans desk_state |
| `signal_event` dans Desk Pro | OUI (pas de reader) | Desk Pro ne consomme pas les signaux webhook |
| `visual_context_ref` dans desk_snapshot | OUI (pas de champ) | Pas de lien snapshot → signal_event |

## Matrice de fraîchesse

| Output | Path | Format | Last updated | Consumer/operator use | Status |
| --- | --- | --- | --- | --- | --- |
| run_summary | `data/desk_runs/.../run_summary.json` | JSON | 2026-05-04 | operator review | AVAILABLE |
| module outputs | `data/desk_runs/.../{module}.json` | JSON | 2026-05-04 | dashboard | AVAILABLE |
| dashboard HTML | `/shared/desk_pro/latest/dashboard_latest.html` | HTML | 2026-04-04 | operator browser | STALE |
| shared export | `/shared/desk_pro/latest/` | JSON+HTML | 2026-04-04 | db-layer, student | STALE |
| desk_state | `desk/state/latest.json` | JSON | 2026-03-03 | orchestrator | STALE |
| snapshot index | `desk/snapshots/latest.json` | JSON | 2026-05-06 | desk_state, analyze | FRAIS |
| analyze output | vision_outbox/analyze_{ts}.txt | TXT | on-demand | Telegram | AVAILABLE |

## RISKS

- À qualifier.
