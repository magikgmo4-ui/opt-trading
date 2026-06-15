# CDP TradingView Alerts — Integration Spec

## Mode

Monitor-only, evidence-only. No broker, no orders, no auto trading.
Routed to `data_center.signal_event` via `signal_event.v1` contract.

## Alert Templates

### P0 — SPCX (6 alerts)

| Alert | Trigger |
|---|---|
| `vwap_reclaim` | Price closes above VWAP |
| `vwap_loss` | Price closes below VWAP |
| `premarket_high_break` | Price breaks above premarket high |
| `orb_break_high` | Price breaks opening range high |
| `orb_break_low` | Price breaks opening range low |
| `relative_volume_gt_2` | Volume > 2x average |

### P1 — BTC/XAU (8 alerts)

| Alert | Symbol | Trigger |
|---|---|---|
| `vwap_reclaim` | BTC, XAU | VWAP reclaim |
| `vwap_loss` | BTC, XAU | VWAP loss |
| `liquidity_sweep_high` | BTC, XAU | Sweep above high |
| `liquidity_sweep_low` | BTC | Sweep below low |
| `bos_bull` | BTC | Break of structure bullish |
| `bos_bear` | BTC | Break of structure bearish |
| `choch_bull` | BTC | Change of character bullish |
| `choch_bear` | BTC | Change of character bearish |

### P2 — AI/Space Watchlist

| Alert | Symbol | Trigger |
|---|---|---|
| `breakout_high` | NVDA, AMD, AVGO, MU, MRVL, PLTR, RKLB, ASTS, LUNR | Break above resistance |
| `breakdown_low` | Same | Break below support |
| `volume_spike` | Same | Volume > 2x average |

## Payload Format

```json
{
  "source": "tradingview_cdp",
  "contract_class": "signal_event.v1",
  "symbol": "SPCX",
  "timeframe": "5",
  "event": "vwap_reclaim",
  "price": "171.50",
  "volume": "1250000",
  "timestamp": "2026-06-15T12:30:00Z",
  "flags": {"vwap_reclaim": true},
  "risk_mode": "monitor_only",
  "route": "data_center.signal_event"
}
```

## Files

| File | Purpose |
|---|---|
| `tradingview/alerts/cdp/spcx_alerts.json` | P0 SPCX alert templates |
| `tradingview/alerts/cdp/btc_xau_alerts.json` | P1 BTC/XAU alert templates |
| `modules/tradingview/cdp_normalizer.py` | Normalizer + monitor-only validator |

## TradingView Setup

1. Create alerts in TradingView with webhook URL `https://<ngrok>/tv`
2. Use the JSON payload templates from `tradingview/alerts/cdp/`
3. Replace `{{close}}`, `{{volume}}`, `{{timenow}}` with TradingView placeholders
4. Set alert condition matching each event trigger

## Integration with Data Center

Webhook → `webhook_server.py` → `cdp_normalizer.normalize_cdp_alert()` → signal_event pipeline.

No new contracts. Uses existing `signal_event.v1`.

## Validation

```bash
# Test normalizer
python3 -c "
from modules.tradingview.cdp_normalizer import normalize_cdp_alert, validate_monitor_only
r = normalize_cdp_alert({'ticker':'SPCX','interval':'5','event':'vwap_reclaim','close':171.5,'volume':1.25e6,'time':'2026-06-15T12:30:00Z'})
print(r['ok'], r['payload']['event'])
print(validate_monitor_only(r['payload']))
"
```

## Forbidden

- No action/order/execute/buy/sell/tp/sl/entry/exit fields
- No risk_mode other than monitor_only
- No new Data Center contracts during 24h validation
- No broker integration
