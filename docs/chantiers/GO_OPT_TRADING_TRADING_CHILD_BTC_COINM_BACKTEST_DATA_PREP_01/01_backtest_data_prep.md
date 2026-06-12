---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01_BACKTEST_DATA_PREP
doc_type: backtest_data_prep
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01
status: draft_for_review
lifecycle_stage: child_backtest_data_prep
parent_go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01
topic_keys:
  - opt-trading
  - trading
  - bitcoin
  - btc
  - bitget
  - coin-futures
  - backtest
  - data-prep
  - historical-data
  - candles
  - funding
  - schema
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01/01_backtest_data_prep.md
point_de_reprise: "Définir le pipeline complet de données historiques pour le backtest BTC COIN-M, sans exécution."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01/01_formulas_source_lock.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/01_formulas_compat_review.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/02_professional_variable_impact_review.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/04_math_formulas.md
---

# 01_backtest_data_prep

## 1_MASTER_TARGET

Définir le pipeline complet de données historiques pour le backtest BTC COIN-M : schémas, sources, transformations, validation et contrat de données minimal. Sans exécuter le backtest, sans connecter Bitget en live.

## 2_FORMULAS_REFERENCE

Formules verrouillées par `FORMULAS_SOURCE_LOCK_01` (PR #243, merged PASS). Toute donnée de backtest doit alimenter ces formules :

```text
qty_to_notional_fn(Q_native, contract_spec)       → N_usd = Q_native * contractSize
notional_to_qty_fn(N_usd, contract_spec)          → Q_native = floor(N_usd / sizeMultiplier) * sizeMultiplier
pnl_inverse_bitget_short_fn(Q_native, E, P)       → PnL_u_btc = Q_native * (1/P - 1/E)
funding_bitget_short_fn(Q_native, MarkPrice, r)   → Funding = (Q_native / MarkPrice) * fundingRate
liquidation_bitget_cross_short_fn(...)            → voir section 6 SOURCE_LOCK
maintenance_margin_bitget_cross_fn(...)           → MM = (Q_native / MarkPrice) * MMR_tier
margin_ratio_bitget_cross_fn(...)                 → MR = equity / MM
```

Prix utilisés :

```text
MarkPrice  → PnL non réalisé, liquidation, funding, maintenance margin
IndexPrice → proxy fallback backtest si MarkPrice absent
LastPrice  → display uniquement, jamais pour calcul de risque
EntryPrice → cost basis (avg fill)
```

---

## 3_DATA_SCHEMA

### 3.1 Candle OHLCV (1h)

Schéma d'une bougie horaire BTCUSD COIN-M :

```json
{
  "candle": {
    "symbol": "BTCUSD",
    "productType": "COIN-FUTURES",
    "granularity": "1H",
    "ts_open": "2026-01-01T00:00:00Z",
    "ts_close": "2026-01-01T01:00:00Z",
    "open": 93450.5,
    "high": 93800.0,
    "low": 93200.0,
    "close": 93600.0,
    "volume_btc": 12.345,
    "volume_usd": 1155000.0,
    "trades": 5432,
    "source": "bitget_public_kline"
  }
}
```

Champs obligatoires pour le backtest :

```text
ts_open      → timestamp d'ouverture ISO-8601
open, high, low, close → prix OHLC (LastPrice du carnet)
volume_btc   → volume en BTC (pour vérifier la liquidité)
volume_usd   → volume en USD (pour vérifier l'activité)
```

Champs optionnels :

```text
mark_open, mark_high, mark_low, mark_close → si MarkPrice history dispo séparément
index_open, index_high, index_low, index_close → si IndexPrice history dispo séparément
```

### 3.2 Mark Price history (1h)

```json
{
  "mark_price": {
    "symbol": "BTCUSD",
    "productType": "COIN-FUTURES",
    "ts": "2026-01-01T01:00:00Z",
    "mark_price": 93580.2,
    "index_price": 93550.0,
    "source": "bitget_public_mark_price"
  }
}
```

Champs obligatoires :

```text
ts          → timestamp
mark_price  → prix de référence Bitget
index_price → prix composite spot (fallback si mark absent)
```

### 3.3 Funding Rate history

```json
{
  "funding_rate": {
    "symbol": "BTCUSD",
    "productType": "COIN-FUTURES",
    "ts_settlement": "2026-01-01T08:00:00Z",
    "funding_rate": 0.0001,
    "funding_interval_hours": 8,
    "source": "bitget_public_funding_rate"
  }
}
```

Champs obligatoires :

```text
ts_settlement           → timestamp de settlement du funding
funding_rate            → taux (ex: 0.0001 = 0.01%)
funding_interval_hours  → intervalle de settlement (8h pour BTCUSD)
```

### 3.4 Contract Spec Snapshot

```json
{
  "contract_spec": {
    "symbol": "BTCUSD",
    "productType": "COIN-FUTURES",
    "marginCoin": "BTC",
    "marginMode": "crossed",
    "contractSize": 1,
    "minTradeNum": 0.0001,
    "sizeMultiplier": 0.0001,
    "volumePlace": 4,
    "pricePlace": 1,
    "priceEndStep": 1,
    "tickSize": 0.1,
    "maxLever": 125,
    "fundInterval": 8,
    "makerFeeRate": 0.0002,
    "takerFeeRate": 0.0006,
    "supportMarginCoins": ["BTC", "STETH", "XRP", "ETH", "USDE", "USDC", "BGB"],
    "snapshot_ts": "2026-05-07T00:00:00Z",
    "source": "bitget_public_contracts_endpoint"
  }
}
```

### 3.5 Risk Tier Table

```json
{
  "risk_tiers": [
    { "tier": 1, "notional_max_usd": 50000,   "mmr": 0.005, "max_lever": 125 },
    { "tier": 2, "notional_max_usd": 250000,  "mmr": 0.01,  "max_lever": 100 },
    { "tier": 3, "notional_max_usd": 1000000, "mmr": 0.015, "max_lever": 50  },
    { "tier": 4, "notional_max_usd": 5000000, "mmr": 0.025, "max_lever": 25  },
    { "tier": 5, "notional_max_usd": 10000000,"mmr": 0.05,  "max_lever": 10  },
    { "tier": 6, "notional_max_usd": 20000000,"mmr": 0.10,  "max_lever": 5   },
    { "tier": 7, "notional_max_usd": 50000000,"mmr": 0.15,  "max_lever": 2   },
    { "tier": 8, "notional_max_usd": 100000000,"mmr":0.25,  "max_lever": 1   }
  ],
  "source": "papier_source_lock_01_a_verifier_par_snapshot_api"
}
```

---

## 4_DATA_SOURCES

### 4.1 Bitget API publique — Endpoints

Tous ces endpoints sont publics, sans clé API :

```text
GET /api/v2/mix/market/candles
  ?symbol=BTCUSD
  &productType=COIN-FUTURES
  &granularity=1H
  &startTime={ts_ms}
  &endTime={ts_ms}
  &limit=200

GET /api/v2/mix/market/mark-price
  ?symbol=BTCUSD
  &productType=COIN-FUTURES

GET /api/v2/mix/market/history-fundRate
  ?symbol=BTCUSD
  &productType=COIN-FUTURES
  &pageSize=100

GET /api/v2/mix/market/contracts
  ?productType=COIN-FUTURES
```

### 4.2 Fenêtre de backtest recommandée

```text
Début : 2024-01-01 (2 ans d'historique)
Fin   : dernière bougie complète disponible
Granularité : 1H (720 bougies/mois, ~17500 bougies/an)

Justification : 1H permet de capturer les settlements de funding (8h)
et donne assez de points pour modéliser le DCA et les shorts.
```

### 4.3 Limites API connues

```text
- candles : max 200 par requête, nécessite pagination
- funding rate : max 100 par page, nécessite pagination
- mark price : pas d'historique long terme (live ou récent uniquement)
  → fallback : utiliser IndexPrice comme proxy de MarkPrice
  → ou reconstituer mark = index + basis mobile
- rate limit : ~20 req/s (public), prévoir un délai entre requêtes
```

---

## 5_DATA_PIPELINE

### 5.1 Étapes du pipeline

```text
Étape 1 — COLLECTE
  Télécharger les candles 1H depuis l'API publique Bitget.
  Paginer par tranches de 200 bougies (max 200 par appel).
  Stocker en JSON Lines (*.jsonl) localement.

Étape 2 — MARK PRICE
  Télécharger l'historique MarkPrice si disponible.
  Sinon, collecter l'IndexPrice composite.
  Si aucun des deux : utiliser LastPrice (close de la bougie) avec avertissement.

Étape 3 — FUNDING RATE
  Télécharger l'historique fundingRate.
  Aligner les timestamps de funding sur les bougies (funding à 00h, 08h, 16h UTC).

Étape 4 — CONTRACT SPEC
  Télécharger le snapshot contract spec actuel.
  Vérifier la stabilité dans le temps (contractSize, minTradeNum).
  Si changement historique : documenter.

Étape 5 — VALIDATION
  Vérifier l'absence de trous dans les timestamps.
  Vérifier que high ≥ max(open, close) et low ≤ min(open, close).
  Vérifier que volume_btc > 0 (bougies vides = avertissement).
  Vérifier que les prix sont positifs et cohérents (pas de spike > 2x la bougie précédente).
  Vérifier l'alignement temporel entre candles et funding rates.

Étape 6 — ENRICHISSEMENT
  Ajouter les colonnes calculées à partir des formules SOURCE_LOCK :
    - N_usd par bougie (notional de référence)
    - PnL_u_btc pour un short test (Q_ref, E_ref, P=close)
    - Funding estimé
    - MarkPrice ou proxy
    - Risk tier du notionnel de référence

Étape 7 — EXPORT
  Produire un fichier unique JSON Lines enrichi, prêt à être lu par trading_lab_v1.
  Format : une ligne = une bougie avec tous les champs nécessaires.
```

### 5.2 Détection des gaps

```text
gap_detection_fn :
  Pour chaque paire de bougies consécutives (i, i+1) :
    expected_ts_i+1 = ts_i + granularity
    si ts_i+1 > expected_ts_i+1 : gap détecté

  Action :
    - gap ≤ 2h : forward-fill le dernier prix connu (marqué interpolated=true)
    - gap > 2h : marquer comme missing, ne pas interpoler
    - jour de maintenance Bitget : documenter, ne pas remplir
```

### 5.3 Validation de cohérence des prix

```text
check_price_coherence_fn(candle) :
  - open, high, low, close > 0
  - high >= max(open, close)
  - low <= min(open, close)
  - high - low < 0.20 * close (rejeter si range > 20% en 1h, sauf news event documenté)
  - |close_i - close_i-1| / close_i-1 < 0.15 (rejeter spike > 15% en 1h sans explication)
```

### 5.4 Alignement Funding ↔ Candles

```text
Le funding est réglé toutes les 8 heures (00:00, 08:00, 16:00 UTC).

Pour chaque bougie horaire t :
  funding_rate_applicable_t = funding_rate du dernier settlement ≤ t

Le funding s'applique à la position détenue pendant l'intervalle [t-8h, t].
En backtest simplifié : appliquer le funding rate au moment du settlement,
sur la position size au mark price du settlement.
```

---

## 6_SAMPLE_DATASET

Jeu de test minimal (3 bougies + 1 funding) :

```json
{
  "dataset_meta": {
    "symbol": "BTCUSD",
    "productType": "COIN-FUTURES",
    "granularity": "1H",
    "start_ts": "2026-01-01T06:00:00Z",
    "end_ts": "2026-01-01T09:00:00Z",
    "funding_intervals": 1,
    "source": "synthetic_sample_for_schema_validation"
  },
  "contract_spec": {
    "contractSize": 1,
    "sizeMultiplier": 0.0001,
    "minTradeNum": 0.0001,
    "makerFeeRate": 0.0002,
    "takerFeeRate": 0.0006,
    "fundInterval": 8
  },
  "candles": [
    {
      "ts_open": "2026-01-01T06:00:00Z",
      "open": 93450.5,
      "high": 93500.0,
      "low": 93400.0,
      "close": 93480.0,
      "volume_btc": 8.2,
      "mark_price": 93470.0,
      "index_price": 93440.0
    },
    {
      "ts_open": "2026-01-01T07:00:00Z",
      "open": 93480.0,
      "high": 93600.0,
      "low": 93450.0,
      "close": 93550.0,
      "volume_btc": 10.5,
      "mark_price": 93540.0,
      "index_price": 93510.0
    },
    {
      "ts_open": "2026-01-01T08:00:00Z",
      "open": 93550.0,
      "high": 93700.0,
      "low": 93500.0,
      "close": 93600.0,
      "volume_btc": 15.1,
      "mark_price": 93610.0,
      "index_price": 93580.0,
      "funding_rate_settled": 0.0001
    }
  ],
  "funding_rates": [
    {
      "ts_settlement": "2026-01-01T08:00:00Z",
      "funding_rate": 0.0001,
      "funding_interval_hours": 8
    }
  ]
}
```

---

## 7_CONTRAT_DE_DONNEES_BACKTEST

### 7.1 Format d'entrée pour le backtest engine

Fichier JSON Lines : `btcusd_coinm_backtest_data.jsonl`

Chaque ligne contient une bougie horaire enrichie :

```json
{
  "ts": "2026-01-01T08:00:00Z",
  "open": 93550.0,
  "high": 93700.0,
  "low": 93500.0,
  "close": 93600.0,
  "volume_btc": 15.1,
  "mark_price": 93610.0,
  "index_price": 93580.0,
  "funding_rate": 0.0001,
  "funding_settled": true,
  "is_interpolated": false,
  "is_gap": false
}
```

### 7.2 Enrichissements calculables en backtest (pas dans le fichier)

```text
Depuis les données de base, le backtest engine calcule :
  - N_usd = Q_native * contractSize (pour la position simulée)
  - PnL_u_btc = Q_native * (1/mark_price - 1/entry_price)
  - MM_btc = (Q_native / mark_price) * MMR_tier
  - MR = equity / MM_btc
  - LiqPrice (formule SOURCE_LOCK section 6.3)
  - D = (LiqPrice - mark_price) / mark_price
  - Funding_increment = (Q_native / mark_price) * funding_rate
```

---

## 8_MAPPING_TRADING_LAB_V1

### 8.1 Compatibilité

```text
trading_lab_v1 est le squelette de backtest existant.
Format d'entrée actuel : profils/schémas V1 (event/trade).

Le fichier JSON Lines produit par ce pipeline doit être compatible
avec le reader de trading_lab_v1, ou nécessiter un adaptateur minimal.

Points de compatibilité à vérifier :
  1. trading_lab_v1 attend-il des events ou des bougies ?
  2. trading_lab_v1 utilise-t-il un schéma de colonnes fixe ?
  3. trading_lab_v1 accepte-t-il des champs supplémentaires (mark_price, etc.) ?
```

### 8.2 Adaptateur minimal (si nécessaire)

```text
Si trading_lab_v1 attend un format différent, créer un adaptateur :
  backtest_data_adapter.py
    - lit le fichier JSON Lines
    - convertit chaque ligne en event/trade trading_lab_v1
    - injecte les champs supplémentaires dans le contexte
```

---

## 9_INVARIANTS_QUALITE

```text
Q1. Aucun gap > 2h sans documentation explicite.
Q2. Aucun prix négatif ou nul.
Q3. high ≥ max(open, close), low ≤ min(open, close) pour chaque bougie.
Q4. volume_btc > 0 pour chaque bougie (ou documenté "empty_candle").
Q5. funding_rate présent pour chaque settlement 8h.
Q6. contract_spec snapshot valide pour la période de backtest.
Q7. mark_price présent ou proxy index_price documenté.
Q8. Pas de spike de prix > 15% entre deux bougies consécutives.
Q9. Timestamps monotones croissants, pas de retour dans le temps.
Q10. Toutes les formules utilisées sont PAPER_LOCKED (SOURCE_LOCK_01).
```

---

## 10_VERDICT_GLOBAL

```text
VERDICT = PASS
```

Justification :

```text
- Pipeline de données défini de bout en bout (collecte → export).
- Schémas JSON complets pour candles, mark_price, funding_rate, contract_spec.
- Sources Bitget identifiées (endpoints publics, pas de clé API).
- Validation et invariants de qualité posés.
- Jeu de test minimal fourni pour validation de schéma.
- Compatibilité trading_lab_v1 documentée, adaptateur prévu.
- Formules PAPER_LOCKED référencées comme base de calcul.
- Backtest réel autorisable après ce PASS.
```

## 11_REFUS

```text
REFUSE_BACKTEST si funding_history vide ou absent
REFUSE_BACKTEST si contract_spec snapshot manquant
REFUSE_BACKTEST si gap > 24h sans documentation
REFUSE_BACKTEST si mark_price absent ET index_price absent (pas de proxy)
REFUSE_BACKTEST si candles < 1000 (backtest non significatif)
REFUSE_RUNTIME tant que PAPER_LOCKED (pas API_VERIFIED)
REFUSE_LIVE toujours
```

## 12_INVARIANTS

```text
- aucune connexion exchange live
- aucun backtest réel exécuté dans ce child
- aucun worker runtime
- aucune nouvelle UI
- documentation + schémas + contrats uniquement
- réutilisation obligatoire de trading_lab_v1 pour le backtest engine
- les données doivent rester vérifiables sans clé API Bitget
- BACKTEST réel autorisé seulement après PASS de ce child
- RUNTIME interdit tant que PAPER_LOCKED
- LIVE interdit
```

## 16_TODO — Suite

```text
1. Valider ce document.
2. Si PASS, ouvrir le child backtest réel (WORKER_BACKTEST).
3. Le backtest réel pourra exécuter les formules PAPER_LOCKED sur les données préparées.
4. Après backtest → validation des formules → demande API_VERIFIED → RUNTIME.
5. Après RUNTIME validé → LIVE.
```

## 17_RESUME_POINT

```text
BACKTEST_DATA_PREP_01 créé.
Pipeline de données défini : collecte, validation, enrichissement, export.
Schémas JSON complets pour tous les types de données.
Sources Bitget publiques identifiées.
Jeu de test minimal fourni.
Compatibilité trading_lab_v1 documentée.
Prochaine action : validation utilisateur, puis backtest réel.
RUNTIME et LIVE restent bloqués (PAPER_LOCKED < API_VERIFIED).
```

## 18_TO_DOCUMENT

```text
- 01_backtest_data_prep.md (présent document)
- Schéma candle OHLCV enrichi
- Schéma mark_price
- Schéma funding_rate
- Schéma contract_spec_snapshot
- Schéma risk_tiers
- Pipeline 7 étapes
- Jeu de test 3 bougies + 1 funding
- Contrat JSON Lines final
- Invariants de qualité
- Refus automatiques
```

## 19_TO_REMEMBER

```text
MEM_CANDIDATE:
BACKTEST_DATA_PREP_01 définit le pipeline de données pour le backtest BTC COIN-M.
Les formules utilisées sont PAPER_LOCKED (SOURCE_LOCK_01, PR #243).
Le backtest réel pourra s'exécuter sur ces données avec les formules figées.
Avant RUNTIME, les PAPER_LOCKED doivent devenir API_VERIFIED.
Avant LIVE, risque de liquidation réel + connexion exchange = revue complète obligatoire.
```

## RISKS

- À qualifier.
