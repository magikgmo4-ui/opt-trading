# 20_CLOSE_METHOD_DECISION

## Mechanisms Evaluated

| Mechanism | Available | Suitable | Reason |
|-----------|-----------|----------|--------|
| POST /tv SELL PAPER_TEST | Yes | No | Would flip BUY→SHORT, not close |
| API /api/positions/close | No | No | Endpoint doesn't exist |
| PositionManager.close_position() | Yes | No direct API | Python method, no HTTP route |
| Direct positions.json edit | Yes | Yes | Clean removal, no side effects |

## Decision

**Direct edit of `/opt/trading/state/positions.json`** — remove the `BTC/USDT` key.

## Why

1. No dedicated close endpoint exists in webhook_server.py
2. Sending SELL would flip to SHORT (not close)
3. `PositionManager.close_position("BTC/USDT")` works but has no HTTP route
4. Direct JSON edit is clean: removes entry, no new position created
5. Paper mode only — no real money or orders affected

## Risk

Low. Removing a paper position entry from a JSON file has no real-world effect.
