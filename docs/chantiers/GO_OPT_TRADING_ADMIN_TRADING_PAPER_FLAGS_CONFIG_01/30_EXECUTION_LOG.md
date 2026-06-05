# 30_EXECUTION_LOG

## Step 1: Add paper flags to .env

```bash
ssh admin-trading "echo '
# Paper test flags (added by GO_OPT_TRADING_ADMIN_TRADING_PAPER_FLAGS_CONFIG_01)
RUNNER_MODE=PAPER
SIMULATION_MODE=true
TRADE_ALLOWED=false
LEDGER_PATH=/opt/trading/state/ledger_paper.json' >> /opt/trading/.env"
```

Result: OK (no output, no error)

## Step 2: Create paper ledger

```bash
ssh admin-trading "echo '{}' > /opt/trading/state/ledger_paper.json"
```

Result: OK

## Step 3: Clear active_engine

```bash
ssh admin-trading 'python3 -c "import json; f=open(\"/opt/trading/state/router_state.json\",\"w\"); json.dump({\"active_engine\": None, \"updated_at\": \"2026-05-14T05:50:00+00:00\"}, f); f.close()"'
```

Result: OK

## Step 4: Kill stale process on port 8000

```bash
ssh admin-trading "fuser -k 8000/tcp"
```

Result: PID 818184 killed

## Step 5: Restart tv-webhook.service

```bash
ssh admin-trading "sudo systemctl restart tv-webhook.service"
```

Result: OK, service active (running)

## Step 6: Verify guards

```bash
ssh admin-trading "curl -s http://127.0.0.1:8000/api/paper/guards | python3 -m json.tool"
```

Result: `ok: true`, all guards PASS

## RISKS

- À qualifier.
