---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01_00_GO_OPEN
doc_type: chantier/go_open
repo: opt-trading
machine: cursor-ai
target_machine: admin-trading
target_path: /opt/trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01
status: active
scope: bounded-runtime-guard
opened_at: 2026-05-13
base: sot/mainline
base_commit: f488ada2
branch: go/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01/10_SOURCE_STATE.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01/20_GUARD_GAP_ANALYSIS.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01/30_RUNTIME_GUARD_SPEC.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01/40_IMPLEMENTATION_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01/50_VALIDATION_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01/60_ROLLBACK.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01/90_CLOSEOUT.md
  - docs/index/inbox/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RUNTIME_GUARDS_FIX_01.md
---

# 00_GO_OPEN

## Objectif

Rendre les guards runtime `PAPER_TEST` detectables et non ambigus avant toute nouvelle tentative de paper test sur `admin-trading:/opt/trading`.

## Contexte

PR `#338` a documente `GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_EXECUTION_01` en `FAIL_CONTROLLED_NO_RUN`.

Blocages etablis:

- `RUNNER_MODE` absent;
- `SIMULATION_MODE` absent;
- `TRADE_ALLOWED` absent;
- `tv-bitget-runner.service=activating`;
- `active_engine=COINM_SHORT`;
- guards runtime non detectables.

## Invariants

- Aucun live trading.
- Aucun ordre reel.
- Aucun payload `PAPER_TEST`.
- Aucun secret dans le repo.
- `db-layer` et OpenClaw hors scope.
- Toute modification runtime doit etre bornee, justifiee et testee.

## Decision de scope

Ce GO modifie uniquement le chemin de guard runtime local au webhook et ajoute des tests unitaires. Il ne lance pas le service, ne modifie pas la configuration cible et n'envoie pas de signal.
