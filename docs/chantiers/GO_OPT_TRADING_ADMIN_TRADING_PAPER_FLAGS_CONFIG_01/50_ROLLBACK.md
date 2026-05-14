# 50_ROLLBACK

## What Changed

1. `/opt/trading/.env` — added 4 lines (paper flags)
2. `/opt/trading/state/router_state.json` — cleared `active_engine` to null
3. `/opt/trading/state/ledger_paper.json` — created (empty JSON)

## Rollback Steps

### 1. Remove paper flags from .env

```bash
ssh admin-trading "sed -i '/# Paper test flags/,/LEDGER_PATH=/d' /opt/trading/.env"
```

### 2. Restore active_engine

```bash
ssh admin-trading 'python3 -c "import json; f=open(\"/opt/trading/state/router_state.json\",\"w\"); json.dump({\"active_engine\": \"COINM_SHORT\", \"updated_at\": \"2026-02-22T17:24:30.856461+00:00\"}, f); f.close()"'
```

### 3. Remove paper ledger

```bash
ssh admin-trading "rm /opt/trading/state/ledger_paper.json"
```

### 4. Restart service

```bash
ssh admin-trading "sudo systemctl restart tv-webhook.service"
```

### 5. Verify

```bash
ssh admin-trading "curl -s http://127.0.0.1:8000/api/paper/guards | python3 -m json.tool"
```

Expected: `ok: false` with same guard states as BEFORE.

## Risk

Low. Changes are configuration-only, no code changes, no live trading impact.
