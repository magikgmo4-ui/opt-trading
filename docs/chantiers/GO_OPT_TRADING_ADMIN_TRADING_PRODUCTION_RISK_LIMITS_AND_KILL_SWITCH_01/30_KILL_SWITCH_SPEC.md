# 30_KILL_SWITCH_SPEC

## Kill Switch Levels

| Level | Name | Action | Reversibility |
|-------|------|--------|---------------|
| 1 | Soft Stop | Set TRADE_ALLOWED=false | Easy (set true) |
| 2 | Service Stop | Stop tv-webhook.service | Easy (systemctl start) |
| 3 | Hard Stop | Kill process + clear state | Manual restore |
| 4 | Emergency | Physical intervention | Manual |

## Kill Switch Implementation

### Level 1: Soft Stop (Recommended)

```bash
# Set in .env
TRADE_ALLOWED=false

# Or via API (TO IMPLEMENT)
curl -X POST http://127.0.0.1:8000/api/kill-switch -d '{"level": 1}'
```

**Effect**: All new orders rejected at guard check. Existing positions unaffected.

### Level 2: Service Stop

```bash
sudo systemctl stop tv-webhook.service
```

**Effect**: Webhook server stops. No orders possible. Positions frozen.

### Level 3: Hard Stop

```bash
# Stop service
sudo systemctl stop tv-webhook.service

# Clear active engine
echo '{"active_engine": null}' > /opt/trading/state/router_state.json

# Set safe mode
echo "TRADE_ALLOWED=false" >> /opt/trading/.env
```

**Effect**: Service stopped, state cleared, safe mode enabled.

## Kill Switch Verification

| Check | Method | Expected |
|-------|--------|----------|
| TRADE_ALLOWED | grep .env | false |
| Service status | systemctl is-active | inactive |
| Active engine | cat router_state.json | null |
| New orders | POST /tv | HTTP 409 or connection refused |

## Kill Switch API (TO IMPLEMENT)

```python
@app.post("/api/kill-switch")
def kill_switch(level: int = 1):
    if level == 1:
        # Soft stop
        os.environ["TRADE_ALLOWED"] = "false"
        return {"ok": True, "level": 1, "action": "soft_stop"}
    elif level == 2:
        # Service stop (requires systemd)
        subprocess.run(["sudo", "systemctl", "stop", "tv-webhook.service"])
        return {"ok": True, "level": 2, "action": "service_stop"}
    elif level >= 3:
        # Hard stop
        set_router_state(None)
        # ... additional cleanup
        return {"ok": True, "level": 3, "action": "hard_stop"}
```

## Status

**MISSING** — Kill switch not implemented. Specification complete.
