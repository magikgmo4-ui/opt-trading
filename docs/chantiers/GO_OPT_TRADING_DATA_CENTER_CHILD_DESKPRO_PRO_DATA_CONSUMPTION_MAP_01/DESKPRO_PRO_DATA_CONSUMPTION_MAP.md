---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_PRO_DATA_CONSUMPTION_MAP_01_DESKPRO_PRO_DATA_CONSUMPTION_MAP
doc_type: consumption_map
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_PRO_DATA_CONSUMPTION_MAP_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01/20_EXISTING_DESKPRO_CONSUMERS.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_INVENTORY_MAPPING_01/PRO_DESK_DATA_GAP_MATRIX.md
  - modules/desk_pro/service/market_metrics_reader.py
  - modules/desk_pro/service/spot_snapshot_reader.py
  - modules/desk_pro/service/vision_analysis_reader.py
  - modules/desk_pro/service/vision_context_reader.py
  - modules/desk_pro/service/telegram_claim_reader.py
  - modules/desk_pro/service/vision_panel.py
  - modules/desk_pro/service/aggregator.py
  - modules/desk_pro/service/scoring.py
---

# DESKPRO_PRO_DATA_CONSUMPTION_MAP

## Objet

Map de consommation DeskPro : pour chaque categorie P0-P21, indiquer le niveau de consommation (required / optional / future / absent), le reader existant, la view DC cible, et le statut de migration.

## Legende

| Niveau | Definition |
|---|---|
| **REQUIRED** | Donnee indispensable au fonctionnement de DeskPro. Reader existant, view DC existe ou doit exister. |
| **OPTIONAL** | Donnee utile, DeskPro fonctionne sans. Peut etre ajoutee si la donnee devient disponible. |
| **FUTURE** | Donnee non encore disponible (pas de producer/view) mais ciblee pour DeskPro. |
| **ABSENT** | Donnee hors scope DeskPro (compliance, settlement, desk_memory). Consommee par d'autres surfaces. |

| Migration | Definition |
|---|---|
| **OK** | Reader lit la view DC. |
| **LEGACY** | Reader lit un path deskpro/inputs/. A migrer vers DC view. |
| **ORPHELIN** | Reader reference une view DC inexistante. |
| **N/A** | Pas de reader. |

## Map P0-P21 → DeskPro

### P0 — instrument_master

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **FUTURE** |
| Reader | Aucun |
| View DC cible | `data/data_center/views/instrument_master/` |
| Migration | N/A |
| Note | Identification des instruments tradables. Utile pour filtrer le dashboard par classe d'actif. |

### P1 — market_quote / market_trade / ohlcv_bar / order_book

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **REQUIRED** (partiel) |
| Reader | `spot_snapshot_reader.py` → `data/data_center/views/pair_market_snapshot/latest.json` |
| View DC cible | `pair_market_snapshot/` (ABSENTE) |
| Migration | **ORPHELIN** — reader migre mais view absente |
| Note | Prix spot OK. Manque OHLCV, order book, market trades. Creer la view en priorite. |
| Gaps | R01, R33 |

### P2 — position_state / risk_state / capital_state

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **FUTURE** |
| Reader | Aucun |
| View DC cible | `data/data_center/views/position_risk/` |
| Migration | N/A |
| Note | Affichage positions/risque/capital dans DeskPro. Necessite producers dedies. |

### P3 — order_state / fill_event / execution_quality

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **ABSENT** |
| Reader | Aucun |
| View DC cible | N/A |
| Migration | N/A |
| Note | Execution/TCA hors scope DeskPro actuel. Consomme par d'autres surfaces. |

### P4 — liquidity_microstructure

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **REQUIRED** (partiel) |
| Reader | `vision_context_reader.py` → `data/deskpro/inputs/vision_context/coinglass/latest.json` |
|  | `vision_panel.py` → meme path legacy |
| View DC cible | `data/data_center/views/vision_context/coinglass/` (a creer) |
| Migration | **LEGACY** — 2 readers a migrer |
| Note | Liquidations/heatmap visibles dans DeskPro. Manque spread/profondeur/imbalance. |
| Gaps | B01, C05, G03, R05, R09, R34 |

### P5 — options_surface / volatility_surface / derivatives_state

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **FUTURE** |
| Reader | Aucun |
| View DC cible | `data/data_center/views/options_surface/` |
| Migration | N/A |
| Note | Vol surface/greeks pour les desks options. Necessite producer dedie. |

### P6 — rates_credit_funding

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **OPTIONAL** |
| Reader | Aucun |
| View DC cible | `data/data_center/views/rates_funding/` |
| Migration | N/A |
| Note | Taux/funding pour contexte macro. Utile mais pas indispensable. |

### P7 — macro_event

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **OPTIONAL** |
| Reader | Aucun |
| View DC cible | `data/data_center/views/macro_events/` |
| Migration | N/A |
| Note | Calendrier economique dans DeskPro. Nice-to-have. |

### P8 — fundamental_snapshot / earnings_event / filing_event

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **OPTIONAL** |
| Reader | Aucun |
| View DC cible | `data/data_center/views/fundamentals/` |
| Migration | N/A |
| Note | Fondamentaux pour contexte equity. Utile si screener equities est actif. |

### P9 — news_event / catalyst_event / sentiment_context

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **REQUIRED** (partiel) |
| Reader | `vision_context_reader.py` → `data/deskpro/inputs/vision_context/news_sentiment/latest.json` |
|  | `vision_panel.py` → meme path legacy |
| View DC cible | `data/data_center/views/vision_context/news_sentiment/` (a creer) |
| Migration | **LEGACY** — 2 readers a migrer |
| Note | Sentiment visible dans DeskPro. Manque news events structures/catalysts. |
| Gaps | B01, C05, G03, R06, R09, R35 |

### P10 — flow_positioning

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **REQUIRED** |
| Reader | `market_metrics_reader.py` → `data/data_center/views/market_metrics/latest.json` |
|  | `aggregator.py` → utilise market_metrics_reader |
| View DC cible | `market_metrics/` (OK) |
| Migration | **OK** — reader migre avec fallback legacy |
| Note | OI, funding, liquidations, L/S ratio. Contract avec 2 sources (bitget+binance) — resolver cible. |
| Gaps | C03, G06, R11, R12, R36 |

### P11 — technical_context

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **REQUIRED** (partiel) |
| Reader | `vision_analysis_reader.py` → `data/deskpro/inputs/vision_analysis/latest.json` |
| View DC cible | `data/data_center/views/vision_analysis/` (existe partiellement: by_symbol/) |
| Migration | **LEGACY** — reader a migrer vers DC view |
| Note | Support/resistance/trend/key levels. View by_symbol existe (20 symboles), history/ absent. |
| Gaps | B01, C04, D04, G02, R04, R10, R37 |

### P12 — model_signal / research_note

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **FUTURE** |
| Reader | Aucun |
| View DC cible | `data/data_center/views/model_signals/` |
| Migration | N/A |
| Note | Alpha interne, backtests. Affichage dans DeskPro si produit. |

### P13 — alternative_data

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **OPTIONAL** |
| Reader | Aucun |
| View DC cible | `data/data_center/views/alternative_data/` |
| Migration | N/A |
| Note | Web/satellite/social. Premium, pas prioritaire. |

### P14 — crypto_derivatives_state / onchain_flow

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **REQUIRED** (partiel) |
| Reader | `market_metrics_reader.py` (DC view) + `vision_context_reader.py` (legacy coinglass) |
|  | `vision_panel.py` (legacy coinglass) |
| View DC cible | `market_metrics/` (OK) + `vision_context/coinglass/` (a creer) |
| Migration | **MIXTE** — market_metrics OK, vision_context LEGACY |
| Note | OI, funding, liquidations deja visibles. Manque onchain wallets/flows. |
| Gaps | C05, C06, G03, R05, R09, R11, R12, R38 |

### P15 — commodity_inventory

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **OPTIONAL** |
| Reader | Aucun |
| View DC cible | `data/data_center/views/commodities/` |
| Migration | N/A |
| Note | Stocks/meteo/OPEC. Utile si trading commodities. |

### P16 — fx_context

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **OPTIONAL** |
| Reader | Aucun |
| View DC cible | `data/data_center/views/fx_context/` |
| Migration | N/A |
| Note | DXY deja partiellement couvert par vision_analysis. Forwards/carry en plus. |

### P17 — equity_context

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **REQUIRED** (partiel) |
| Reader | `vision_context_reader.py` → `data/deskpro/inputs/vision_context/screener/latest.json` |
|  | `vision_panel.py` → meme path legacy |
| View DC cible | `data/data_center/views/vision_context/screener/` (a creer) |
| Migration | **LEGACY** — 2 readers a migrer |
| Note | Screener equities basique visible. Manque float/short interest/ownership. |
| Gaps | B01, C05, G03, R07, R09, R39 |

### P18 — compliance_state

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **ABSENT** |
| Reader | Aucun |
| View DC cible | N/A |
| Migration | N/A |
| Note | Compliance/audit/restrictions. Hors scope DeskPro. |

### P19 — ops_settlement_state

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **ABSENT** |
| Reader | Aucun |
| View DC cible | N/A |
| Migration | N/A |
| Note | Clearing/settlement. Hors scope DeskPro. |

### P20 — desk_memory

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **FUTURE** |
| Reader | Aucun |
| View DC cible | `data/data_center/views/desk_memory/` |
| Migration | N/A |
| Note | Notes/thesis/handover. Fonctionnalite DeskPro future. |

### P21 — data_quality_state / source_score

| Dimension | Valeur |
|---|---|
| Niveau DeskPro | **OPTIONAL** |
| Reader | Aucun |
| View DC cible | `data/data_center/views/source_scores/` |
| Migration | N/A |
| Note | Scores sources visibles dans DeskPro pour transparence. Pas indispensable. |

## Synthese consommation DeskPro

```text
REQUIRED (migre)     : 1   — P10 (market_metrics)
REQUIRED (orphelin)  : 1   — P1 (spot_snapshot: view absente)
REQUIRED (legacy)    : 4   — P4 (coinglass), P9 (news_sentiment), P11 (vision_analysis), P17 (screener)
REQUIRED (mixte)     : 1   — P14 (market_metrics OK + coinglass legacy)
OPTIONAL             : 7   — P6, P7, P8, P13, P15, P16, P21
FUTURE               : 5   — P0, P2, P5, P12, P20
ABSENT               : 3   — P3, P18, P19
---
TOTAL                : 22
```

## Readers DeskPro : statut et cible

| Reader | Contract | Path actuel | Statut | View DC cible |
|---|---|---|---|---|
| `market_metrics_reader.py` | market_metrics.v1 | DC view + legacy fallback | **OK** | `views/market_metrics/` |
| `spot_snapshot_reader.py` | pair_market_snapshot.v1 | DC view (inexistante) | **ORPHELIN** | `views/pair_market_snapshot/` |
| `vision_analysis_reader.py` | vision_analysis.v1 | legacy | **LEGACY** | `views/vision_analysis/` |
| `vision_context_reader.py` (coinglass) | vision_context.coinglass.v1 | legacy | **LEGACY** | `views/vision_context/coinglass/` |
| `vision_context_reader.py` (news) | vision_context.news_sentiment.v1 | legacy | **LEGACY** | `views/vision_context/news_sentiment/` |
| `vision_context_reader.py` (screener) | vision_context.screener.v1 | legacy | **LEGACY** | `views/vision_context/screener/` |
| `telegram_claim_reader.py` | telegram_claim.v1 | legacy | **LEGACY** | `views/telegram_claim/` |
| `vision_panel.py` (x4) | vision_context.* | legacy (x4) | **LEGACY** | `views/vision_context/*` |
| `aggregator.py` | mix (market_metrics + coinglass) | DC + legacy | **MIXTE** | `views/market_metrics/` + `views/vision_context/coinglass/` |
| `scoring.py` | N/A (compute only) | N/A | **N/A** | N/A |

## Plan de migration DeskPro (priorise)

### Phase 1 — Infrastructure (bloquant)

| # | Action | Impact |
|---|---|---|
| M1 | Creer `views/pair_market_snapshot/` | Debloque spot_snapshot_reader (P1) |
| M2 | Creer `views/vision_context/coinglass/` | Cible pour migration coinglass (P4) |
| M3 | Creer `views/vision_context/news_sentiment/` | Cible pour migration news (P9) |
| M4 | Creer `views/vision_context/screener/` | Cible pour migration screener (P17) |

### Phase 2 — Migration readers (apres infrastructure)

| # | Action | Impact |
|---|---|---|
| M5 | Migrer `vision_analysis_reader.py` → DC view | P11 passe de LEGACY a OK |
| M6 | Migrer `vision_context_reader.py` (coinglass) → DC view | P4 passe de LEGACY a OK |
| M7 | Migrer `vision_context_reader.py` (news) → DC view | P9 passe de LEGACY a OK |
| M8 | Migrer `vision_context_reader.py` (screener) → DC view | P17 passe de LEGACY a OK |
| M9 | Migrer `vision_panel.py` (4 paths) → DC views | Panel lit views DC |
| M10 | Enregistrer `telegram_claim` dans consumers.json | Reader trace |

### Phase 3 — Resolver (apres migration)

| # | Action | Impact |
|---|---|---|
| M11 | Activer resolver market_metrics (bitget vs binance) | P10/P14 multi-source arbitre |
| M12 | Publier canonical_value dans la view | Transparent pour DeskPro |

### Phase 4 — Extensions (futur)

| # | Action | Impact |
|---|---|---|
| M13 | Ajouter OHLCV/order_book pour P1 | Completion spot |
| M14 | Ajouter onchain pour P14 | Completion crypto |
| M15 | Ajouter spread/depth pour P4 | Completion microstructure |
| M16 | Ajouter news events pour P9 | Completion news |
| M17 | Ajouter float/short interest pour P17 | Completion equities |
| M18 | Ajouter nouveaux producers pour P0, P2, P5, P12, P20 | Nouvelles categories |

## Post-migration : etat cible

```text
DeskPro readers → TOUS vers DC views (plus aucun path legacy)
Views DC → toutes existantes pour les contracts REQUIRED
Resolver → actif pour market_metrics.v1
Consumers.json → a jour (telegram_claim inclus)
Legacy paths → supprimes ou archives
```
