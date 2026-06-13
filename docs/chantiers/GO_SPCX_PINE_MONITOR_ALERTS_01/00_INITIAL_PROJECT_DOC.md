# GO_SPCX_PINE_MONITOR_ALERTS_01

## Objective

Add a monitor-only Pine Script template for SPCX TradingView alerts so the
SpaceX webhook path can graduate from simple price-placeholder alerts to native
Pine-side signal logic.

## Scope

- Add `tradingview/spcx_monitor_alerts.pine`.
- Cover heartbeat, VWAP cross up/down, and volume spike monitor signals.
- Keep `TV_WEBHOOK_KEY` as a TradingView input; never commit a live secret.
- Do not change runtime webhook handlers, risk engines, or execution code.

## Acceptance

- Pine static analysis passes.
- TradingView server-side Pine compile returns no errors.
- PR gate file scope is limited to this GO and the Pine template.

## Operational Note

Live use requires adding the indicator to the SPCX chart, setting the
`TV_WEBHOOK_KEY` input in TradingView, and creating one alert on
`Any alert() function call` with webhook `/tv/spacex`.
