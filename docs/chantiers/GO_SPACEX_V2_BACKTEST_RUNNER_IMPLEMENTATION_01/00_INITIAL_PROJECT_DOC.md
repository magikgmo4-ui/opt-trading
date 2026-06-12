---
doc_id: GO_SPACEX_V2_BACKTEST_RUNNER_IMPLEMENTATION_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_SPACEX_V2_BACKTEST_RUNNER_IMPLEMENTATION_01
parent_go: GO_SPACEX_V2_BACKTEST_RUNNER_AND_PAPER_LOGGER_01
status: draft
lifecycle_stage: impl
surface: docs/chantiers
source_kind: canonical
created_at: 2026-06-12
links:
  - docs/chantiers/GO_SPACEX_V2_BACKTEST_RUNNER_AND_PAPER_LOGGER_01/00_INITIAL_PROJECT_DOC.md
  - modules/perf_engine/
  - modules/data_center/
  - shared/telegram_notify.py
  - shared/logger.py
---

# GO_SPACEX_V2_BACKTEST_RUNNER_IMPLEMENTATION_01

## [6_FINAL_TARGET]

Implémenter le code du runner paper-only SPCX V2 défini dans le parent GO : `modules/spcx_v2/` avec setup detector, paper logger, perf calculator, runner CLI, scripts, et tests.

---

## [7_CANONICAL_STATE] — Files à créer

```text
modules/spcx_v2/
├── __init__.py
├── config.py
├── setup_detector.py
├── paper_logger.py
├── perf_calculator.py
├── runner.py
└── scripts/
    ├── cmd.sh
    ├── menu.sh
    ├── sanity_check.sh
    └── install_shortcuts.sh

tests/
├── test_spcx_v2_setup_detector.py
├── test_spcx_v2_paper_logger.py
└── test_spcx_v2_perf_calculator.py

docs/chantiers/GO_SPACEX_V2_BACKTEST_RUNNER_IMPLEMENTATION_01/
├── 00_INITIAL_PROJECT_DOC.md
└── FILE_SCOPE.txt
```

---

## [5_GO_PLAN]

### config.py — Configuration centralisée

- Setup catalog (tous les setups du parent GO)
- Seuils de score (trade_ready, liquidity, risk, smart_money, catalyst)
- Chemins de sortie (data/ipo/spacex/paper_log/, data/perf/spcx_v2/)
- Timeframes (1m, 5m, 15m, 30m, 1h)
- Seuils de spread, volume, bars_count

### setup_detector.py — Gates 0–3

- `check_gate_0_data_validity(market_snapshot) -> GateResult`
- `check_gate_1_market_safety(market_snapshot) -> GateResult`
- `check_gate_2_setup_detected(market_snapshot) -> list[SetupMatch]`
- `check_gate_3_score_validation(setup_matches) -> SetupCandidate`
- `detect(market_snapshot) -> SetupCandidate | None`
- Classement A+ / A / B / reject basé sur les scores
- Toutes les fonctions sont pures (pas d'I/O)

### paper_logger.py — Logging papier

- `log_candidate(candidate: SetupCandidate) -> str` (écrit dans JSONL + retourne ID)
- `log_reject(candidate: SetupCandidate) -> str` (écrit dans rejects.jsonl)
- `log_result(candidate_id: str, result: dict) -> None` (met à jour le candidat avec MFE/MAE/R)
- `get_summary() -> dict` (stats agrégées par setup_type et grade)
- `list_candidates(status: str) -> list[SetupCandidate]` (filtre par statut)

### perf_calculator.py — Calculs de performance

- `calculate_mfe(entry, price_series) -> float`
- `calculate_mae(entry, price_series) -> float`
- `calculate_r_multiple(entry, sl, exit_price, direction) -> float`
- `check_tp1_hit(price_series, tp1, direction) -> bool`
- `check_tp2_hit(price_series, tp2, direction) -> bool`
- `check_sl_hit(price_series, sl, direction) -> bool`
- `compute_stats(candidates_with_results: list) -> dict` (winrate, expectancy, profit_factor, drawdown)

### runner.py — CLI + boucle principale

- `runner.py --once` : single-cycle detection + logging
- `runner.py --watch` : continuous loop (polling)
- `runner.py --replay events.jsonl` : replay mode from saved events
- Respecte les 5 invariants du parent GO
- Lit depuis state/events.jsonl ou stdin
- Toute sortie est paper-only

### scripts/

- `cmd.sh` — CLI wrapper (delegates to runner.py)
- `menu.sh` — interactive menu
- `sanity_check.sh` — validates module installation
- `install_shortcuts.sh` — installs wrapper in /usr/local/bin

### tests/

- `test_spcx_v2_setup_detector.py` — gate unit tests + classification
- `test_spcx_v2_paper_logger.py` — log + reject + summary + retrieval
- `test_spcx_v2_perf_calculator.py` — MFE/MAE/R + stats + edge cases

---

## [11_KEY_DECISIONS]

- Toutes les fonctions core sont pures (pas d'I/O directe dans setup_detector, perf_calculator)
- Le logging est le seul composant avec I/O (paper_logger)
- Le runner.py est le seul point d'entrée runtime
- Aucune modification des modules existants
- Aucun bridge vers execution_engine
- Les scores sont calculés, pas hardcodés
- Token Telegram / credentials Sheets via .env uniquement

---

## [12_INVARIANTS]

1. PAPER ONLY — aucune exécution d'ordre
2. NO LIVE PRICE = NO SETUP
3. TOUT EST LOGGÉ (y compris les rejets)
4. ZÉRO SECRET dans le code
5. SCORES DOCUMENTÉS ET TESTABLES

---

## [17_RESUME_POINT]

```text
Implémentation du runner paper-only SPCX V2.
modules/spcx_v2/ avec 4 composants + scripts + tests.
Code pur, pas d'I/O dans la logique métier.
CLI --watch / --once / --replay.
Tests unitaires pour chaque gate et chaque calcul.
```
