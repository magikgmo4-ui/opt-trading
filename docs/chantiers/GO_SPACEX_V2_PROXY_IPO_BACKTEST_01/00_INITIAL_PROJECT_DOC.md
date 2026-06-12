---
doc_id: GO_SPACEX_V2_PROXY_IPO_BACKTEST_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_SPACEX_V2_PROXY_IPO_BACKTEST_01
parent_go: GO_SPACEX_V2_DESK_TELEGRAM_SHEETS_EXPORT_01
status: draft
lifecycle_stage: impl
surface: docs/chantiers
source_kind: canonical
created_at: 2026-06-12
links:
  - docs/chantiers/GO_SPACEX_V2_SETUP_SELECTION_AND_BACKTEST_PLAN_01/00_INITIAL_PROJECT_DOC.md
  - modules/spcx_v2/setup_detector.py
  - modules/spcx_v2/perf_calculator.py
  - modules/ipo_tracking/backtest_engine.py
  - modules/ipo_tracking/ipo_dataset.py
---

# GO_SPACEX_V2_PROXY_IPO_BACKTEST_01

## [6_FINAL_TARGET]

Rejouer le detector SPCX V2 sur des IPO comparables (proxy universe) pour valider les setups avant que SPCX n'ait assez d'historique.

Proxy universe: RKLB, ASTS, RDW, LUNR, PL, IONQ, ARM, RDDT, COIN, RIVN, HOOD, SNOW, PLTR.

---

## [7_CANONICAL_STATE] — Files

```text
modules/spcx_v2/proxy_backtest.py      # CSV→MarketSnapshot + replay engine
scripts/ipo/spacex_proxy_backtest.sh   # run proxy backtests, produce report
tests/test_spcx_v2_proxy_backtest.py
docs/chantiers/GO_SPACEX_V2_PROXY_IPO_BACKTEST_01/
├── 00_INITIAL_PROJECT_DOC.md
└── FILE_SCOPE.txt
```

---

## [5_GO_PLAN]

### proxy_backtest.py

- `candle_to_snapshot(candle: dict, symbol: str, idx: int) -> MarketSnapshot`
- `load_csv(path: str) -> list[dict]` — lit un CSV de bougies OHLCV
- `replay_csv(csv_path: str, symbol: str) -> list[dict]` — rejoue le detector sur toutes les bougies
- `run_proxy_backtest(symbol: str, csv_path: str) -> dict` — rapport complet
- `run_all_proxy(symbols: list[str]) -> dict` — tous les proxy d'un coup
- Supporte les fichiers CSV avec colonnes: ts, open, high, low, close, volume (optionnel: vwap)
- Génère un MarketSnapshot par bougie avec price_status="live" simulé
- Détecte les setups, loggue les candidats (via paper_logger)
- Simule les résultats (MFE, MAE, R) avec les bougies suivantes
- Agrège les stats par setup_type

### spacex_proxy_backtest.sh

- Appelle `python3 -m modules.spcx_v2.proxy_backtest` avec les bons flags
- `--symbol RKLB --csv data/ipo/proxy/RKLB_ipo.csv`
- `--all` pour runner tous les proxy
- Produit un rapport markdown dans `reports/ipo/spacex/proxy_backtest_*.md`

### Report format

- Table: symbol | setup_type | trades | winrate | expectancy_R | profit_factor | avg_R
- Comparison: SPCX proxy average vs individual proxy
- Heatmap: setup_type × symbol (winrate color-coded)

---

## [11_KEY_DECISIONS]

- Données CSV fournies manuellement ou via Yahoo (pas de téléchargement automatique)
- Simulation: price_status toujours "live" pour le replay (on sait que les données sont historiques)
- Les bougies futures simulent les résultats avec les prix réels suivants
- Pas de slippage ni spread simulé (backtest idéalisé)
- Résultats exportés dans le format paper_logger standard

---

## [12_INVARIANTS]

1. PAPER ONLY — backtest sur données historiques
2. DÉTERMINISME — même CSV = mêmes résultats
3. SIMULATION IDÉALISÉE — slippage 0, commissions 0, pas de spread
4. ZÉRO SECRET — données publiques uniquement

---

## [17_RESUME_POINT]

```text
Proxy IPO backtest engine: CSV → MarketSnapshot → detector → results.
Supporte RKLB, ASTS, RDW, LUNR, PL, IONQ, ARM, RDDT, COIN, RIVN, HOOD, SNOW, PLTR.
Produit rapport markdown avec stats par setup_type et par symbole.
```
