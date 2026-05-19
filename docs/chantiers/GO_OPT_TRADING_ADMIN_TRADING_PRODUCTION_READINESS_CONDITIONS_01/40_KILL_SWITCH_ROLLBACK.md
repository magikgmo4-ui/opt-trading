# 40_KILL_SWITCH_ROLLBACK

## Current State

No kill switch or emergency stop mechanism exists.

## Requirements

| Feature | Description | Status |
|---------|-------------|--------|
| Emergency stop | Immediate halt all trading | MISSING |
| Position close | Close all positions | MISSING |
| Service stop | Stop webhook service | AVAILABLE (systemctl) |
| Rollback | Revert to safe state | MISSING |

## Kill Switch Design

### Level 1: Soft Stop
- Set TRADE_ALLOWED=false
- Reject new orders
- Keep existing positions

### Level 2: Hard Stop
- Stop webhook service
- Close all positions
- Clear active_engine

### Level 3: Emergency
- Kill all processes
- Manual intervention required

## Implementation Plan

1. Add `/api/kill-switch` endpoint
2. Implement soft/hard/emergency modes
3. Add to systemd watchdog
4. Document procedures

## Rollback Procedure

1. Stop webhook: `sudo systemctl stop tv-webhook.service`
2. Set TRADE_ALLOWED=false in .env
3. Clear active_engine in router_state.json
4. Verify no open positions
5. Restart in safe mode

## Status: MISSING

No kill switch implemented. Must be built before production.
