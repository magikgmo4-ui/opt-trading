# 80_MIGRATION_PLAN

## Goal

Replace the intermediate bundle chain with one canonical continuation point.

## What to keep

From Stock True Value bundles:

- score formulas;
- configs;
- schemas;
- pure scoring engine;
- fixtures;
- tests;
- dry-run CLI concept;
- Data Center draft contracts.

From SpaceX Intelligence:

- SPCX Tier 0;
- Starlink/xAI ecosystem context;
- catalyst scoring concept;
- watchlist ecosystem;
- weekly report concept.

From SpaceX Final Canonical / V5:

- IPO tracking architecture;
- collectors list;
- data flow;
- scoring signals;
- Data Center handoff;
- monitor-only invariant;
- UI/Desk roadmap;
- backtest catalog.

## What to remove or archive

- duplicate intermediate docs;
- placeholder patch from Bundle 08;
- repeated instructions from each bundle;
- redundant standalone `GO_STOCK_TRUE_VALUE_ENGINE_01` project framing.

## Migration steps

1. Apply final consolidated patch.
2. Run tests.
3. Run fixture-only CLI.
4. Review generated `outputs/stock_true_value/latest/scores.json`.
5. Open separate GO for Data Center registration.
6. Open separate GO for LocalCMS cards.
7. Open separate GO for live collectors.
