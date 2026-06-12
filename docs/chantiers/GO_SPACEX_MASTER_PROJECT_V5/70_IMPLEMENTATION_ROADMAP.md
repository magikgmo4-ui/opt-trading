# Implementation Roadmap

## P0 now

- Apply V5 patch.
- Run smoke.
- Confirm files written.

## P1 TradingView

- Create SPCX chart alerts using `tradingview/spacex_alert_template_v5.json`.
- Send webhook to existing webhook server.
- Route payload to `modules.ipo_tracking.collectors.tradingview_webhook`.

## P2 Bot Vision

- Merge `profiles.spacex.v5.json` into production profile rotation.
- Schedule 10-minute captures.
- Pipe OCR/analysis into Data Center.

## P3 Data Center

- Register `spacex_super_desk.v1` contract.
- Add source scoring dimensions for SPCX producers.

## P4 Telegram + Sheets

- Add SPCX alert dispatcher.
- Add Google Sheets worksheet mapping.

## P5 Backtest Lab

- Feed OHLCV history.
- Run setup sweeps.
- Rank strategies by expectancy and drawdown.

## P6 Desk Pro native

- Convert static `ui/spacex_desk` into native route.
