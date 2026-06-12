# GO_SPACEX_FINAL_CANONICAL_01 — Master Project

## 1_MASTER_TARGET

Faire de SpaceX / SPCX l'actif prioritaire de `opt-trading`, avec un système complet dédié:

- SPACEX_DESK.
- SPACEX_TRADING_LAB.
- SPACEX_DATA_CENTER.
- SPACEX_ALERT_ENGINE.
- SPACEX_NEWS_ENGINE.
- SPACEX_INSTITUTIONAL_ENGINE.
- SPACEX_ACCUMULATION_ENGINE.
- SPACEX_BACKTEST_ENGINE.
- SPACEX_BOT_VISION_FLOW.
- SPACEX_TRADINGVIEW_FLOW.

Le système doit supporter deux objectifs simultanés:

1. Court terme: capturer momentum, volatilité, IPO opening range, FVG, VWAP reclaim, gaps et catalystes.
2. Long terme: accumuler au bon prix via modèle fondamental + technique + institutionnel + régime de marché.

Invariant: monitor-only. Aucune exécution automatique d'ordre réel.

## 2_INITIAL_PROJECT_DOC

Ce document remplace les bundles V1 à V5. Il est autonome et canonique.

Les anciens bundles ont été fusionnés et leurs contenus utiles ont été intégrés ou conservés dans `legacy_inputs/`.

## 3_INITIAL_NEED

Le besoin initial validé: préparer un screening complet et une collecte API complète de toutes les données concernant l'IPO SpaceX, utiliser toutes les sources disponibles dans le repo, brancher TradingView, Coinglass/contexte, Bot Vision headless, actualités, métriques multi-timeframe, open/close, FVG, alertes, accumulation long terme, setups court terme et backtests.

## 4_MASTER_PROJECT_PLAN

### Axe A — Source Coverage

Couvrir toutes les sources disponibles ou branchables:

- TradingView: indicateurs, alertes, webhook JSON, Pine templates, multi-TF.
- Bot Vision Headless: screenshots, OCR, analysis, visual context.
- Data Center: raw, normalized, scored, views.
- Telegram: alertes et signal routing.
- Google Sheets: export reporting.
- SEC/EDGAR: filings et documents IPO.
- Market Data: Yahoo public fallback, Nasdaq/quote providers, OHLCV.
- News: RSS/Yahoo fallback, Reuters-like, CNBC, MarketWatch, Benzinga, SEC, SpaceX, Starlink, NASA, DoD.
- Institutional: ETF, 13F, analystes, lockup, secondary, insiders.
- Coinglass/contexte: funding/liquidation/heatmap lorsque pertinent, surtout comme régime de risque et rotation capital crypto/AI/space.

### Axe B — Mega Data

Stocker trois niveaux:

- raw: réponse source originale.
- normalized: contrat stable interne.
- scored: signaux synthétiques et scores.

### Axe C — Mega Analysis

Produire analyses:

- price action.
- smart money.
- volatility.
- volume / relative volume.
- opening range.
- FVG / BOS / CHOCH / OB / liquidity.
- news velocity.
- institutional flow.
- sector halo.
- long-term accumulation.

### Axe D — Mega Setups

Cataloguer et backtester:

- IPO Opening Range Breakout 5m/15m/30m.
- Gap and Go.
- VWAP Reclaim.
- FVG Reclaim.
- IPO Price Flush + Reclaim.
- First Red Day Trap.
- High Relative Volume Continuation.
- News Catalyst Breakout.
- Sector Halo Momentum.
- Accumulation Pullback.

### Axe E — Desk/UI

Créer une vue dédiée:

- Market status.
- Scores.
- Alerts.
- News.
- Technical/smart-money.
- Correlations.
- Long-term accumulation.
- Backtest summaries.

## 5_GO_PLAN

1. Appliquer le patch final sur une branche dédiée.
2. Lancer le smoke test final.
3. Valider les sorties `data/`, `reports/`, `ui/`.
4. Ouvrir PR vers `sot/mainline`.
5. Child GO #1: inventaire réel branchable dans la machine prod.
6. Child GO #2: branchement TradingView + Bot Vision réel.
7. Child GO #3: Telegram + Google Sheets + Desk Pro native.
8. Child GO #4: backtests multi-setup.

## 6_FINAL_TARGET

Un système fonctionnel minimal immédiatement:

- CLI `python3 -m modules.ipo_tracking.cli smoke`.
- Collect-once offline/online.
- Rapport daily.
- UI statique.
- Patch autonome.
- Docs master.
- Configs TradingView/Bot Vision.
- Backtest ORB initial.

## 7_CANONICAL_STATE

Ce bundle final est la seule version à appliquer. Ne pas appliquer V1, V2, V3, V4 ou V5 séparément.

## 11_KEY_DECISIONS

- SpaceX/SPCX devient prioritaire.
- Monitor-only obligatoire.
- Toutes les sources utiles sont conservées.
- Données raw non détruites.
- Les anciens bundles sont remplacés par cette version finale.

## 12_INVARIANTS

- Pas d'ordre réel automatique.
- Pas de pipeline parallèle non intégré au repo.
- Réutiliser le repo existant avant de créer du nouveau.
- Garder la traçabilité des sources.
- Un signal sans source fiable reste hypothèse, pas décision.

## 17_RESUME_POINT

Appliquer `GO_SPACEX_FINAL_CANONICAL_01.patch`, lancer `bash scripts/ipo/spacex_final_smoke.sh`, puis ouvrir PR.
