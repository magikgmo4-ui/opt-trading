# GO_SPACEX_MASTER_PROJECT_V5 — Master Project

## 1_MASTER_TARGET

SpaceX/SPCX becomes a priority asset with a dedicated Super Desk, Trading Lab, Mega Data pipeline, Mega Analysis framework, Mega Setup catalog and Mega Backtest engine.

## 2_INITIAL_PROJECT_DOC

This document is the frozen transportable project reference for V5. It is based on the uploaded `opt-trading-sot-mainline` repository state and the full session requirements.

## 3_INITIAL_NEED

User wants complete coverage of SpaceX/SPCX to own it at the right price and exploit leverage momentum, using every available source: TradingView, Coinglass context, Bot Vision headless, news, multi-timeframe metrics, opening/closing behavior, FVG, BOS, CHOCH, alerts, Data Center, Desk, Trading Lab and long-term data accumulation.

## 4_MASTER_PROJECT_PLAN

1. Stabilize V5 scaffold and smoke test.
2. Inventory existing repo surfaces.
3. Connect real TradingView alerts.
4. Connect Bot Vision profile and scheduler.
5. Persist raw/normalized/scored data.
6. Publish Data Center view `spacex_super_desk.v1`.
7. Publish UI static desk and later Desk Pro native route.
8. Build setup engine.
9. Build backtest engine.
10. Build accumulation engine.
11. Wire Telegram and Google Sheets.
12. Close with E2E validation.

## 7_CANONICAL_STATE

V5 delivers implementation scaffolding aligned to the repo architecture. It is monitor-only and writes local data/report/UI outputs.

## 11_KEY_DECISIONS

- SpaceX/SPCX is top priority.
- Use all useful existing repo sources before new systems.
- Preserve raw data.
- Separate short-term momentum from long-term accumulation.
- Treat leverage as decision support, not automatic execution.

## 12_INVARIANTS

- No live order execution.
- No secrets in repo.
- No removal of existing Data Center, Bot Vision, Telegram, Google Sheets, Desk Pro surfaces.
- All source reliability must be scored.

## 17_RESUME_POINT

Run:

```bash
bash scripts/ipo/spacex_smoke_v5.sh
bash scripts/ipo/spacex_collect_once_v5.sh --offline
```
