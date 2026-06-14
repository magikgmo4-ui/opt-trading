---
doc_id: GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01
status: draft
role: DATA_ARCHITECT_MARKET_MICROSTRUCTURE
created_at: 2026-06-14
---

# GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01

## Objet

Collecter, agréger et archiver le flux d'ordres (orderflow) et la répartition de propriété (ownership) du stock SPCX depuis Day-1 IPO. Produire un ledger unique qui distingue l'intention visible (order book), les transactions exécutées (tape/prints) et la répartition déclarée (SEC ownership filings), **sans prétendre identifier les vrais acheteurs/vendeurs en temps réel**.

## 7_CANONICAL_STATE

```text
SPCX IPO: 2026-06-11 | Prix IPO: $135 | Greenshoe: ~15% (+83M actions)
Modules ipo_tracking existants: collectors spot/perps/multi-venue/fund-halo, scoring, pipeline, market_microstructure
Gaps:
  - Pas de collecteur SIP/tape consolidé avec inférence aggressor side
  - Pas de collecteur L2/carnet de profondeur par niveau
  - Pas de collecteur auction open/close
  - Pas de collecteur SEC ownership (Form 3/4/144, 13D/13G/13F)
  - Pas de collecteur private round cost-basis
  - Pas de bucket d'agrégation 1s/5s/1m filtrant les micro-trades
  - Pas de scoring orderflow (delta volume, imbalance, large prints)
  - Pas de scoring ownership pressure (lock-up expiry, insider selling pressure)
  - Pas de schema orderflow_bucket.v1 ni ownership_ledger.v1
```

## 6_FINAL_TARGET

```text
SPCX_DAY1_ORDERFLOW_OWNERSHIP_LEDGER_V1

Order book depth + tape agrégée + auction data + SEC ownership + private round cost-basis →
  → bucketing 1s/5s/1m filtré micro-trades
  → scoring orderflow (delta, large prints, imbalance)
  → scoring ownership pressure (insider, lock-up, institutional)
  → rapport Day-1 consolidé
```

## 3_INITIAL_NEED

```text
Pour SPCX, il faut comprendre le flux Day-1 sans micro-transactions inutiles:

  1. Order book / carnet d'ordres: intentions visibles d'achat/vente, profondeur, murs
  2. Tape / prints: transactions exécutées, large prints, aggressor side inféré
  3. Ownership / répartition: qui possède quoi après IPO (SEC filings, prospectus)

Ce qu'on peut logger: prix, taille, timestamp, venue, trade condition, bid/ask au trade,
  aggressor side inféré, large prints, block trades, sweeps, orderbook imbalance.

Ce qu'on NE peut PAS logger: "BlackRock a acheté X à 10:03" (identité en temps réel).
```

## 4_MASTER_PROJECT_PLAN

### P0 — lundi (Day-1 immediate)

1. Collector SIP/tape consolidé + NBBO (`spcx_sip_tape.py`)
2. Collector L2 depth broker/vendor (`spcx_l2_depth.py`)
3. Agrégation 1m sans micro-trades (filtre odd lots, <100 shares, <$25K)
4. Large prints > $500K USD
5. Buy/sell initiated volume inféré (quote rule / Lee-Ready)
6. Auction open/close imbalance (`spcx_auction_imbalance.py`)
7. SEC 424B4 + Form 3 insiders parser (`spcx_sec_ownership.py`)

### P1 — semaine suivante

1. Nasdaq TotalView/ITCH historique Day-1 via vendor
2. Form 4/144 watcher (`spcx_insider_forms.py`)
3. 13D/13G watcher
4. 13F quarterly institutional ownership
5. Private round cost-basis reconstruction (`spcx_private_rounds.py`)

### P2 — post-stabilisation

1. Dark pool / TRF détaillé
2. ETF/fund flows
3. Borrow/short inventory
4. Options chain once listed
5. Synthetic perp vs spot basis study

## 8_VALIDATED_PLAN

### Livrables

```text
configs/ipo/spacex_market_data_sources.yaml     — sources priority (direct feed > broker > SIP > TV > Yahoo)
configs/ipo/spacex_orderflow_filters.yaml       — filtres anti-bruit (odd lots, min size, large print threshold)
schemas/ipo/spcx_orderflow_bucket.v1.schema.json  — schema du bucket agrégé
schemas/ipo/spcx_ownership_ledger.v1.schema.json  — schema du ledger ownership

modules/ipo_tracking/collectors/spcx_sip_tape.py          — collector SIP consolidé tape + NBBO
modules/ipo_tracking/collectors/spcx_l2_depth.py          — collector L2/carnet de profondeur
modules/ipo_tracking/collectors/spcx_auction_imbalance.py — collector auction open/close
modules/ipo_tracking/collectors/spcx_sec_ownership.py     — collector SEC 424B4/S-1/Form 3
modules/ipo_tracking/collectors/spcx_insider_forms.py     — collector Form 4/144 watcher
modules/ipo_tracking/collectors/spcx_private_rounds.py    — collector private market cost-basis

modules/ipo_tracking/scoring/spcx_orderflow_score.py      — scoring orderflow (delta, prints, imbalance)
modules/ipo_tracking/scoring/spcx_ownership_pressure_score.py — scoring ownership (insider, lock-up, institutional)

reports/ipo/spacex/spcx_day1_orderflow_ownership_YYYYMMDD.md — rapport Day-1 consolidé
```

### Pipeline cible

```text
RAW feed (SIP / L2 / ITCH / broker)
  → filtre micro-trades (odd lots, <$25K)
  → bucket 1s / 5s / 1m
  → agrégation par prix (OHLC, VWAP, delta volume)
  → score orderflow (imbalance, large prints, sweep probability)
  → snapshot SPCX + rapport
```

## 9_SELECTED_SOLUTION

Architecture "sans micro transactions" : collecter massif, puis agréger en buckets temporels. Les données brutes ne sont pas stockées individuellement — seuls les buckets agrégés et les large prints > $500K sont persistés.

### Modèle de données cible — orderflow bucket

```json
{
  "schema": "spcx_orderflow_bucket_v1",
  "symbol": "SPCX",
  "bucket_seconds": 60,
  "price": { "open", "high", "low", "close", "vwap" },
  "volume": { "shares", "usd", "large_prints_usd" },
  "flow": {
    "buy_initiated_volume",
    "sell_initiated_volume",
    "delta",
    "delta_pct"
  },
  "book": {
    "spread_pct_avg",
    "bid_depth_1pct_usd",
    "ask_depth_1pct_usd",
    "imbalance_avg"
  },
  "quality": {
    "source": "SIP|L2|ITCH|BROKER|TV_DOM",
    "aggressor_side_method": "quote_rule|lee_ready|native|unknown",
    "micro_trades_filtered": true
  }
}
```

### Modèle de données cible — ownership ledger

```json
{
  "schema": "spcx_ownership_ledger_v1",
  "source": "424B4|S-1|Form3|Form4|Form144|13D|13G|13F|press|private_market",
  "as_of_date": "2026-06-12",
  "holder": null,
  "holder_type": "insider|institution|retail_pool|underwriter|fund|unknown",
  "shares": null,
  "class": "Class A|Class B|unknown",
  "ownership_pct": null,
  "voting_power_pct": null,
  "acquisition_price": null,
  "cost_basis_estimated": true,
  "lockup_until": null
}
```

## 10_SELECTED_SETUP

```text
Sources P0:
  SIP/NBBO + tape consolidé → base prix/spread/trades
  L2 broker/vendor → profondeur, murs, imbalance
  Auction open/close → flux institutionnel
  SEC EDGAR → 424B4, S-1, Form 3/4/144, 13D/13G/13F

Filtres:
  ignore_odd_lots: true
  min_trade_size_shares: 100
  min_trade_value_usd: 25000
  large_print_threshold_usd: 500000
  block_trade_threshold_usd: 1000000

Agrégation:
  buckets: 1s, 5s, 60s
  stockage: state/ipo/spacex/orderflow_buckets/ et state/ipo/spacex/ownership/
```

## 11_KEY_DECISIONS

- **Pas d'identité acheteur/vendeur en temps réel** — on infère aggressor side, pas le nom du buyer.
- **Agréger, ne pas stocker les micro-prints** — buckets temporels uniquement, sauf large prints > $500K.
- **Les données brutes SIP/L2 ne sont pas archivées en continu** — seul le bucket agrégé est persisté.
- **Les filings SEC sont parsés offline** — pas de websocket EDGAR, poll périodique ou ingestion manuelle.
- **Le scoring orderflow et ownership pressure sont des modules séparés** — ils lisent les buckets, ne les produisent pas.
- **Ne pas modifier les collectors ipo_tracking existants** — ajouter des nouveaux, sans casser ceux en place.
- **Aucun appel API temps réel non autorisé** — respecter les abonnements market data des sources utilisées.
- **Toute nouvelle source doit être documentée dans `spacex_market_data_sources.yaml`.**

## 12_INVARIANTS

- Ne pas casser les collectors existants (`spcx_spot_orderbook.py`, `spcx_binance_perp.py`, `spcx_multi_venue.py`).
- Ne pas injecter dans le pipeline trading live sans validation.
- Ne pas exposer de données private-market sans disclaimer sur le caractère estimé du cost-basis.
- Ne pas logger les identités d'acheteurs/vendeurs individuels (invalide légalement/impossible techniquement).
- Toute collecte SEC doit respecter les rate limits EDGAR.
- Les schémas produits sont des spécifications JSON Schema, pas du code.
- Les rapports Day-1 sont en markdown dans `reports/ipo/spacex/`, pas dans `docs/`.
- Aucune modification runtime, API, DB, Telegram sans validation explicite.

## 15_REMAINING_GAP

- Pas de feed Nasdaq TotalView/ITCH direct (coût élevé, vendor nécessaire).
- Pas d'accès aux dark pools / TRF détaillé (P2).
- Pas de données options (la chaîne n'existe pas encore).
- Pas d'ETF flows (trop tôt).
- Private round cost-basis sera partiel (données non publiques exhaustivement).

## 16_TODO

1. Créer `configs/ipo/spacex_market_data_sources.yaml` — hiérarchie des sources.
2. Créer `configs/ipo/spacex_orderflow_filters.yaml` — filtres anti-bruit.
3. Spécifier `schemas/ipo/spcx_orderflow_bucket.v1.schema.json`.
4. Spécifier `schemas/ipo/spcx_ownership_ledger.v1.schema.json`.
5. Implémenter les 6 collectors P0 (`spcx_sip_tape`, `spcx_l2_depth`, `spcx_auction_imbalance`, `spcx_sec_ownership`, `spcx_insider_forms`, `spcx_private_rounds`).
6. Implémenter les 2 scoring modules (`spcx_orderflow_score`, `spcx_ownership_pressure_score`).
7. Produire le rapport Day-1 consolidé.
8. P1: Nasdaq TotalView/ITCH historique, Form 4/144 watcher, 13D/13G/13F, private round cost-basis.

## 17_RESUME_POINT

```text
GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01
Chantier ouvert le 2026-06-14.
Reprendre ici : docs/chantiers/GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01/00_INITIAL_PROJECT_DOC.md

Priorité P0 immédiate : configs (sources + filtres), schemas (orderflow_bucket + ownership_ledger),
collectors (sip_tape, l2_depth, auction_imbalance, sec_ownership).
```
