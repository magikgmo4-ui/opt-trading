# TradingView Orchestrator

Linux-side runner for dispatching TradingView automation jobs to cursor-ai via SSH.
Reads a `tv_job_v1` JSON packet, tunnels it through the Windows agent, and returns
structured results. Mutation jobs require an explicit `--gate-approved` flag.

## Architecture

```
Linux (tv_runner.py)
  └─ validates job packet (schema, gate, job type)
  └─ SSH → cursor-ai
        └─ SCP job JSON to tradingview_observer/jobs/pending/
              └─ TVOrchestratorAgent (Windows scheduled task)
                    └─ polls pending/ every 2 s
                    └─ dispatches to tradingview-mcp CLI (Node.js + CDP)
                          └─ CDP connects to TradingView Desktop at localhost:9222
                                └─ fetch interceptor patches create_alert network call
                    └─ writes .result.json to jobs/done/
  └─ polls jobs/done/ for result (120 s timeout)
  └─ exits 0 on success, saves report to reports/tradingview/
```

**TradingView Desktop must be running with CDP enabled.** Start via
`TradingView_CDP.vbs` (required for MSIX loopback — `--remote-debugging-port=9222`
is rejected by the App Store build when launched from PowerShell directly).

## Quick start

```bash
# Read-only — no gate needed
python3 modules/tradingview_orchestrator/app/tv_runner.py \
  modules/tradingview_orchestrator/jobs/examples/tv_job_snapshot.json

# Mutation — gate required
python3 modules/tradingview_orchestrator/app/tv_runner.py \
  modules/tradingview_orchestrator/jobs/examples/tv_job_alert_create.json \
  --gate-approved

# Dry-run (shows SSH commands without executing)
python3 modules/tradingview_orchestrator/app/tv_runner.py <job.json> --dry-run
```

Exit codes: `0`=PASS, `1`=INVALID_INPUT, `3`=REJECTED (gate missing), `4`=REFUSED (wrong type), `5`=RUNNER_ERROR

## Job packet format (`tv_job_v1`)

```json
{
  "schema": "tv_job_v1",
  "id": "unique_job_id",
  "type": "alert.create",
  "created_at": "2026-06-12T00:00:00Z",
  "params": { ... },
  "gate": "approved"
}
```

`"gate": "approved"` must be set manually before running a mutation job.
The runner checks this field; missing or wrong value exits code 3.

### Job types

| Type | Gate | Description |
|---|---|---|
| `snapshot` | no | CDP status + quote + state + alerts + values |
| `alert.list` | no | List all active alerts |
| `screenshot` | no | Capture current chart |
| `alert.create` | **yes** | Create a new price alert with webhook |
| `alert.delete` | **yes** | Delete alert by ID |
| `alert.rotate_webhook_key` | **yes** | Re-key all alerts with a new webhook token |
| `indicator.add` | **yes** | Add a study to the chart |
| `indicator.remove` | **yes** | Remove a study by entity ID |
| `indicator.set` | **yes** | Modify study inputs |
| `symbol.set` | **yes** | Change chart symbol |
| `timeframe.set` | **yes** | Change chart timeframe |
| `pine.set` / `pine.save` | **yes** | Edit/save a Pine Script source |
| `layout.switch` | **yes** | Switch to a saved layout |

## Creating an alert — full walkthrough

### 1. Write the job packet

```json
{
  "schema": "tv_job_v1",
  "id": "my_alert_20260612",
  "type": "alert.create",
  "created_at": "2026-06-12T00:00:00Z",
  "params": {
    "condition": "greater_than",
    "price": 1,
    "name": "My Alert",
    "webhook_url": "https://my-tunnel.example.com/tv/endpoint",
    "message": "{\"key\": \"<TV_WEBHOOK_KEY>\", \"source\": \"tradingview\", \"symbol\": \"{{ticker}}\", \"signal\": \"MY_SIGNAL\", \"price\": \"{{close}}\", \"time\": \"{{time}}\"}",
    "frequency": "on_bar_close"
  },
  "gate": "approved"
}
```

Keep `<TV_WEBHOOK_KEY>` or `__TV_WEBHOOK_KEY__` in committed job templates. The
runner materializes the real `TV_WEBHOOK_KEY` from the runtime environment or
`.env` immediately before dispatch and masks it in dry-run output.

Do not use the legacy `webhook` field. `alert.create` jobs must use
`params.webhook_url`; otherwise the runner and Windows agent refuse the job.

### 2. Frequency values

| `frequency` param | TradingView label | Behaviour |
|---|---|---|
| `on_bar_close` | Chaque fois | Fires every bar while condition is met |
| `on_first_fire` | Une fois seulement | Fires once, then deactivates |

Legacy values such as `once_per_bar` and `every_bar_close` are not accepted by
the orchestrator because the TradingView API rejected them during live testing.

### 3. Dispatch

```bash
python3 modules/tradingview_orchestrator/app/tv_runner.py my_alert.json --gate-approved
```

### 4. Webhook body parsing

TradingView strips double-quotes from stored alert messages before delivery.
The webhook body arrives as a JS-object-literal (not valid JSON):

```
{key: abc123, source: tradingview, symbol: SPCX, ...}
```

`webhook_server.py::_parse_tv_body()` handles this: tries `json.loads()` first,
falls back to regex splitting on `, identifier:` boundaries. No action required
on the alert-creation side.

## SpaceX Wire — live alert

The production `BATS:SPCX` alert is defined in `jobs/spacex_wire_alert.json`.
It fires every bar close on the 1-minute chart and posts to `/tv/spacex` via
the Cloudflare Tunnel `spacex-tv.magikgmo4.uk`.

```bash
# Verify last received fire
grep SPACEX_WIRE /opt/trading/state/events.jsonl | tail -1 | python3 -m json.tool
```

## Prerequisites

| Component | Location | Notes |
|---|---|---|
| TradingView Desktop | cursor-ai (Windows) | Must be running with CDP on port 9222 |
| `TradingView_CDP.vbs` | cursor-ai desktop | Mandatory launcher (MSIX loopback workaround) |
| `tradingview-mcp` | `C:\Users\ghost\.claude\tools\tradingview-mcp\` | Node.js v24+; `npm install` + `npx playwright install chromium` |
| TVOrchestratorAgent | Windows Task Scheduler | Runs `tv_agent.ps1` as persistent loop; restart if stale |
| SSH alias `cursor-ai` | `~/.ssh/config` on Linux | Passwordless; used by `tv_runner.py` |

### Restart the Windows agent

```powershell
# On cursor-ai — restart TVOrchestratorAgent task
Stop-ScheduledTask  -TaskName TVOrchestratorAgent
Start-ScheduledTask -TaskName TVOrchestratorAgent
```

### Check agent is alive

```bash
# From Linux
ssh cursor-ai "schtasks /query /tn TVOrchestratorAgent /fo list | Select-String 'Status'"
```

## Output files

- `reports/tradingview/<job_id>.json` — full result saved on Linux after each run
- `modules/tradingview_observer/jobs/done/<job_id>.result.json` — raw agent output on cursor-ai (gitignored)
- `state/events.jsonl` — appended when a webhook fires successfully

## Security notes

- Job packets committed to git must use `<TV_WEBHOOK_KEY>` as the key placeholder.
  The runner substitutes the real value at dispatch time.
- `*.result.json` and `*.json.done` files in `jobs/done/` are gitignored — they
  contain the literal key value from the executed alert message.
- The `--gate-approved` flag is a human checkpoint; do not script it unconditionally.
