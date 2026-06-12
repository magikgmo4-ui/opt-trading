---
doc_id: GO_SPACEX_V2_TV_SMC_SIGNAL_WIRING_01_ACCEPTANCE
doc_type: acceptance_report
repo: opt-trading
go_id: GO_SPACEX_V2_TV_SMC_SIGNAL_WIRING_01
parent_go: GO_SPACEX_V2_SOURCE_MAXIMIZATION_AUDIT_01
status: CLOSED_PROVED
closed_at: 2026-06-12
prs:
  - "#1143 — SMC structures wired into setup_detector scoring"
  - "#1147 — SpaceX Wire alert created + /tv/spacex body parser fix"
---

# GO_SPACEX_V2_TV_SMC_SIGNAL_WIRING_01 — Acceptance Report

## Verdict: CLOSED / PROVED

All deliverables from the initial project doc are complete and in production.

---

## What was built

### 1. SMC scoring integration (PR #1143)

`modules/spcx_v2/setup_detector.py` — `compute_scores()` now reads SMC structure flags:

| SMC signal | Score delta |
|---|---|
| BOS detected | +15 `smart_money_score` |
| CHOCH detected | +15 `smart_money_score` |
| FVG bullish only | +10 `smart_money_score` |
| 2+ SMC confirmations | `trade_ready` boost |

`reason_codes` in `paper_logger.py` emit: `SMC_BOS`, `SMC_CHOCH`, `SMC_FVG_BULL`, `SMC_FVG_BEAR`, `SMC_MULTI_CONFIRM`.

### 2. SpaceX Wire alert — automated creation (PR #1147)

The alert is live on BATS:SPCX in TradingView Desktop. It fires every bar close where `close > 1` (always true for SPCX), posting the full market context payload to the webhook.

**Alert parameters:**

| Field | Value |
|---|---|
| Symbol | `BATS:SPCX` |
| Condition | `close > 1` (always fires) |
| Frequency | `on_bar_close` (Chaque fois) |
| Webhook | `https://spacex-tv.magikgmo4.uk/tv/spacex` |
| Alert name | `SpaceX Wire` |
| TV alert ID | `4917725195` |

**Webhook payload received by `/tv/spacex`:**

```
{key: <token>, source: tradingview, symbol: SPCX, exchange: BATS,
 interval: <tf>, price: <close>, volume: <vol>, alert_name: SpaceX Wire,
 signal: SPACEX_WIRE, time: <epoch>}
```

Note: TradingView strips double-quotes from stored alert messages. The body
arrives as a JS-object-literal (not valid JSON). `_parse_tv_body()` handles
this transparently with a regex fallback.

### 3. `/tv/spacex` endpoint fix (PR #1147, `webhook_server.py`)

`_parse_tv_body()` added at line 426. The endpoint now uses `await req.body()`
instead of `await req.json()` and passes through the lax parser.

**First confirmed live fire:** 2026-06-12 17:52 UTC — BATS:SPCX bar close,
signal `SPACEX_WIRE` received at `/tv/spacex`, processed without error.

---

## How the automation works

Alert creation goes through the **TradingView Orchestrator pipeline**:

```
Linux (tv_runner.py)
  └── reads tv_job_v1 JSON packet
  └── SSH → cursor-ai
        └── writes job to tradingview_observer/jobs/pending/
              └── TVOrchestratorAgent (Windows scheduled task, tv_agent.ps1)
                    └── polls pending/, picks up job
                    └── calls tradingview-mcp CLI (Node.js + CDP)
                          └── CDP → TradingView Desktop process
                                └── fetch interceptor patches create_alert call
                          └── writes result to jobs/done/
  └── polls jobs/done/ for result file
  └── returns structured output
```

Key component: **fetch interceptor** in `tradingview-mcp/src/core/alerts.js`.
Before opening the alert dialog, the interceptor patches `window.fetch`. When
TV's frontend calls `create_alert`, the interceptor intercepts and rewrites:
- `conditions[0].frequency` — set to `on_bar_close` (not `every_bar_close` which is invalid)
- `conditions[0].series[1].value` — price threshold
- `web_hook` — webhook URL
- `message` — serialized payload
- `name` — alert label

This approach is more reliable than DOM automation since it operates at the
network layer within the page context.

**Frequency API values** (from TV JS bundle constant set):

| API value | TV dialog label |
|---|---|
| `on_first_fire` | Une fois seulement |
| `on_bar_close` | Chaque fois |

---

## Files modified / created

| File | Change |
|---|---|
| `modules/spcx_v2/setup_detector.py` | SMC → score wiring |
| `modules/spcx_v2/pipeline_adapter.py` | SMC field passthrough (prior fix) |
| `webhook_server.py` | `_parse_tv_body()` + `/tv/spacex` body parsing fix |
| `modules/tradingview_orchestrator/jobs/spacex_wire_alert.json` | Job packet (key placeholder) |
| `modules/tradingview_orchestrator/app/tv_runner.py` | Orchestrator runner (prior GO) |
| `modules/tradingview_observer/agent/tv_agent.ps1` | argList fix for alert.create |
| `C:\...\tradingview-mcp\src\core\alerts.js` | `FREQ_API.every_bar` → `on_bar_close` |

---

## How to verify

```bash
# On Linux — check the webhook endpoint is alive
curl -s https://spacex-tv.magikgmo4.uk/health

# Check last received SpaceX Wire event
grep SPACEX_WIRE state/events.jsonl | tail -1

# Check tv_runner can dispatch a read-only snapshot job
python3 modules/tradingview_orchestrator/app/tv_runner.py \
  modules/tradingview_orchestrator/jobs/examples/tv_job_snapshot.json
```

---

## How to create a new alert

1. Write a `tv_job_v1` packet (see `jobs/examples/tv_job_alert_create.json`)
2. Set `"gate": "approved"` after human review
3. Run: `python3 modules/tradingview_orchestrator/app/tv_runner.py <job.json> --gate-approved`
4. Monitor: the runner polls `jobs/done/` for up to 120 s; exits 0 on success
