# 40_ROLLBACK_PLAN

## Rollback Scenarios

| Scenario | Trigger | Action | Verification |
|----------|---------|--------|--------------|
| Limit breach | Daily loss exceeded | Soft stop + close positions | Check daily P&L |
| Service failure | Webhook crash | Restart service | systemctl status |
| Bad position | Unexpected behavior | Close position + stop | positions.json |
| Live trading | TRADE_ALLOWED=true | Immediate stop | grep .env |
| Secret exposure | Key leaked | Rotate + stop | git history audit |

## Rollback Procedure

### Step 1: Immediate Stop

```bash
# Option A: Soft stop
ssh admin-trading "sed -i 's/TRADE_ALLOWED=true/TRADE_ALLOWED=false/' /opt/trading/.env"

# Option B: Service stop
ssh admin-trading "sudo systemctl stop tv-webhook.service"
```

### Step 2: Verify Stop

```bash
# Check service
ssh admin-trading "systemctl is-active tv-webhook.service"

# Check guards
ssh admin-trading "curl -s http://127.0.0.1:8000/api/paper/guards"

# Check positions
ssh admin-trading "cat /opt/trading/state/positions.json"
```

### Step 3: Close Positions (if needed)

```python
# Remove position from positions.json
import json
with open("/opt/trading/state/positions.json") as f:
    d = json.load(f)
d.pop("TARGET_SYMBOL", None)
with open("/opt/trading/state/positions.json", "w") as f:
    json.dump(d, f, indent=2)
```

### Step 4: Restore Safe State

```bash
# Ensure paper mode
ssh admin-trading "grep TRADE_ALLOWED /opt/trading/.env"
# Should show: TRADE_ALLOWED=false

# Clear active engine
ssh admin-trading 'echo "{\"active_engine\": null}" > /opt/trading/state/router_state.json'
```

### Step 5: Verify No Live Orders

```bash
# Check events log for live orders
ssh admin-trading "grep -v PAPER_TEST /opt/trading/state/events.jsonl | grep -v TV_TEST"
# Should be empty or only paper entries
```

### Step 6: Document Incident

Create incident report with:
- Trigger
- Actions taken
- Verification results
- Root cause
- Prevention measures

## Rollback Time Estimates

| Action | Time | Complexity |
|--------|------|------------|
| Soft stop | < 1 min | Low |
| Service stop | < 1 min | Low |
| Close positions | < 5 min | Medium |
| Restore config | < 5 min | Medium |
| Full rollback | < 15 min | Medium |

## Status

**PARTIAL** — Rollback procedures documented. Automation recommended.
