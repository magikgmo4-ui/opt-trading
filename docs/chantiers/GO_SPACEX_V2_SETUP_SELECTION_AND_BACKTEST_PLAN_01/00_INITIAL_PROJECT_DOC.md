---
doc_id: GO_SPACEX_V2_SETUP_SELECTION_AND_BACKTEST_PLAN_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_SPACEX_V2_SETUP_SELECTION_AND_BACKTEST_PLAN_01
parent_go: GO_SPACEX_MASTER_PROJECT_V5
status: draft
lifecycle_stage: design
surface: docs/chantiers
source_kind: canonical
created_at: 2026-06-12
links:
  - docs/chantiers/GO_SPACEX_MASTER_PROJECT_V5/00_MASTER_PROJECT.md
  - docs/chantiers/GO_SPACEX_MASTER_PROJECT_V5/50_MEGA_SETUP_CATALOG.md
  - docs/chantiers/GO_SPACEX_MASTER_PROJECT_V5/60_MEGA_BACKTEST_FRAMEWORK.md
---

# GO_SPACEX_V2_SETUP_SELECTION_AND_BACKTEST_PLAN_01

## [6_FINAL_TARGET]

Définir comment **SPCX V2 choisira les setups**, quels **backtests seront lancés**, et quelles **stratégies seront testées**.

Objectif : éviter les signaux impulsifs sur IPO. Le pipeline doit d'abord **observer**, puis **classer**, puis seulement produire des setups `A+ / A / B / reject`.

---

# [1] Sélection des setups de trading

## [7_CANONICAL_STATE]

Un setup SPCX ne sera sélectionné que si les 4 gates passent.

```text
GATE 0 — DATA VALIDITY
→ price_status = live
→ bars_count > 0
→ volume > 0
→ price_trust > 0
→ source_count >= 1

GATE 1 — MARKET SAFETY
→ spread acceptable
→ volume suffisant
→ pas de halt actif
→ pas de contradiction Nasdaq/Yahoo/TV
→ liquidité exploitable

GATE 2 — SETUP DETECTED
→ ORB / VWAP / FVG / BOS / CHOCH / sweep / IPO reclaim / news breakout

GATE 3 — SCORE VALIDATION
→ trade_ready_score
→ liquidity_score
→ risk_score
→ catalyst_score
→ smart_money_score
```

Si `price_status != live`, aucun setup prix n'est validé.

---

## [8_VALIDATED_PLAN] — logique de sélection

Chaque setup doit avoir :

| Élément              | Requis                                             |
| -------------------- | -------------------------------------------------- |
| `trigger`            | événement clair : break, reclaim, sweep, FVG, VWAP |
| `context`            | IPO, news, volume, secteur, sentiment              |
| `entry_zone`         | zone d'entrée précise                              |
| `invalidation`       | niveau où le setup est faux                        |
| `TP1 / TP2 / runner` | objectifs graduels                                 |
| `risk_R`             | risque en R                                        |
| `score`              | A+, A, B, reject                                   |
| `reason_codes`       | raisons lisibles dans Desk/Telegram                |

Format attendu :

```json
{
  "symbol": "SPCX",
  "setup": "IPO_ORB_15M",
  "grade": "A",
  "entry_zone": "above ORB high + VWAP hold",
  "invalidation": "below VWAP or ORB midpoint",
  "tp_logic": ["TP1 1R", "TP2 2R", "runner VWAP/trend"],
  "scores": {
    "trade_ready": 78,
    "liquidity": 72,
    "risk": 38,
    "smart_money": 70,
    "catalyst": 65
  },
  "status": "paper_only"
}
```

---

# [2] Classes de setups prévues

## A. Setups IPO / first day

| Setup                     | Logique                              | Priorité |
| ------------------------- | ------------------------------------ | -------: |
| `FIRST_PRINT_OBSERVATION` | observer premier bar, pas trader     |       P0 |
| `IPO_ORB_5M`              | break du range 5m avec volume        |       P0 |
| `IPO_ORB_15M`             | break du range 15m plus propre       |       P0 |
| `IPO_ORB_30M`             | setup plus lent / moins bruité       |       P1 |
| `IPO_PRICE_RECLAIM`       | flush sous prix IPO puis reclaim     |       P0 |
| `IPO_PRICE_LOSS`          | perte du prix IPO = danger / no long |       P0 |
| `GAP_AND_GO`              | ouverture forte + VWAP hold + volume |       P1 |
| `FAILED_BREAKOUT_TRAP`    | break raté puis retour range         |       P1 |

Priorité initiale : **observer les 15–30 premières minutes**, ne pas surpondérer le premier print.

---

## B. Setups VWAP

| Setup                   | Logique                                 | Usage               |
| ----------------------- | --------------------------------------- | ------------------- |
| `VWAP_HOLD_LONG`        | prix au-dessus VWAP + pullback tenu     | continuation        |
| `VWAP_RECLAIM`          | prix repasse au-dessus VWAP avec volume | reversal intraday   |
| `VWAP_REJECT`           | rejet sous VWAP                         | danger / avoid long |
| `VWAP_DISTANCE_EXTREME` | prix trop loin de VWAP                  | risque chase        |

VWAP est central pour une IPO parce qu'il donne un repère institutionnel intraday.

---

## C. Setups Smart Money / SMC

| Setup                         | Trigger                        |
| ----------------------------- | ------------------------------ |
| `FVG_BULLISH_RECLAIM`         | FVG bullish + reclaim + volume |
| `FVG_BEARISH_REJECT`          | FVG bearish + rejet            |
| `BOS_CONTINUATION`            | break of structure confirmé    |
| `CHOCH_REVERSAL`              | changement de caractère        |
| `LIQUIDITY_SWEEP_LOW_RECLAIM` | sweep des lows puis reclaim    |
| `LIQUIDITY_SWEEP_HIGH_REJECT` | sweep des highs puis rejet     |
| `ORDER_BLOCK_RETEST`          | retest zone OB avec réaction   |

Ces setups ne sont valides que si TradingView ou Bot Vision confirme la structure.

---

## D. Setups momentum / volume

| Setup                      | Logique                               |
| -------------------------- | ------------------------------------- |
| `RELATIVE_VOLUME_BREAKOUT` | volume anormal + break structure      |
| `VOLUME_ACCELERATION`      | accélération volume 1m/5m             |
| `HIGH_VOLUME_PULLBACK`     | pullback propre après impulsion       |
| `LOW_VOLUME_FADE`          | break sans volume = rejet             |
| `DOLLAR_VOLUME_FILTER`     | setup rejeté si liquidité trop faible |

---

## E. Setups news / catalyst

| Setup                        | Trigger                                |
| ---------------------------- | -------------------------------------- |
| `NEWS_CATALYST_BREAKOUT`     | news forte + break technique           |
| `SEC_FILING_REACTION`        | filing important + réaction prix       |
| `CONTRACT_NEWS_REACTION`     | NASA/DoD/Starlink/launch contract      |
| `NEGATIVE_HEADLINE_RISK_OFF` | news négative + perte VWAP             |
| `NEWS_SPIKE_FADE`            | spike sur headline sans volume durable |

---

## F. Setups accumulation long terme

Ces setups sont séparés des trades intraday.

| Zone              | Conditions                                            |
| ----------------- | ----------------------------------------------------- |
| `BUY_ZONE`        | prix raisonnable + fondamentaux forts + risque faible |
| `ACCUMULATE_ZONE` | valuation acceptable + momentum neutre                |
| `WAIT_ZONE`       | trop cher / pas assez de données                      |
| `DANGER_ZONE`     | euphorie, dilution, lockup, perte technique           |

Facteurs :

```text
starlink
launch_cadence
revenue_growth
contracts
institutional_ownership
valuation
```

---

# [3] Backtests prévus

## [5_GO_PLAN]

Il faut 3 familles de backtests : **proxy historique**, **replay intraday**, puis **forward paper-test SPCX réel**.

---

## A. Backtest proxy IPO

Comme SPCX est nouveau, il n'a pas assez d'historique. Donc on teste d'abord sur des IPO comparables.

| Test                         | Objectif                          |
| ---------------------------- | --------------------------------- |
| `IPO_DAY_ORB_BACKTEST`       | ORB 5m/15m/30m sur jour IPO       |
| `IPO_FIRST_WEEK_BACKTEST`    | comportement J1 à J5              |
| `IPO_GAP_AND_GO_BACKTEST`    | poursuite après ouverture forte   |
| `IPO_PRICE_RECLAIM_BACKTEST` | réaction autour du prix IPO       |
| `FIRST_RED_DAY_BACKTEST`     | premier jour rouge puis reclaim   |
| `IPO_LOCKUP_EVENT_BACKTEST`  | réaction proche expiration lockup |

Univers proxy :

```text
IPO tech / growth / space / defense / AI
RKLB
ASTS
RDW
LUNR
PL
IONQ
ARM
RDDT
COIN
RIVN
HOOD
SNOW
PLTR
```

À adapter selon disponibilité des données.

---

## B. Backtest secteur / halo

| Test                             | Objectif                            |
| -------------------------------- | ----------------------------------- |
| `SPACE_BASKET_RS_BACKTEST`       | SPCX vs RKLB/ASTS/RDW/LUNR/PL       |
| `QQQ_REGIME_FILTER_BACKTEST`     | éviter longs quand QQQ faible       |
| `TSLA_HALO_FILTER_BACKTEST`      | mesurer effet Musk/risk appetite    |
| `NVDA_AI_RISK_FILTER_BACKTEST`   | mesurer corrélation AI momentum     |
| `ARKX_UFO_CONFIRMATION_BACKTEST` | secteur spatial confirme ou diverge |

---

## C. Backtest technique intraday

| Stratégie               | Timeframes    |
| ----------------------- | ------------- |
| ORB 5m                  | 1m / 5m       |
| ORB 15m                 | 1m / 5m / 15m |
| VWAP reclaim            | 1m / 5m       |
| VWAP hold               | 5m / 15m      |
| FVG reclaim             | 5m / 15m      |
| BOS continuation        | 5m / 15m      |
| CHOCH reversal          | 5m / 15m      |
| Liquidity sweep reclaim | 1m / 5m       |
| Gap continuation        | 5m / 15m      |
| High-volume pullback    | 5m            |

---

## D. Backtest score engine

Tester non seulement les setups, mais les scores.

| Test                         | Question                                |
| ---------------------------- | --------------------------------------- |
| `TRADE_READY_THRESHOLD_TEST` | seuil optimal A+/A/B                    |
| `LIQUIDITY_FILTER_TEST`      | spread/volume minimum                   |
| `RISK_SCORE_BLOCKING_TEST`   | quand bloquer un setup                  |
| `NEWS_SCORE_IMPACT_TEST`     | news améliore-t-elle le winrate         |
| `SMC_SCORE_IMPACT_TEST`      | FVG/BOS/CHOCH ont-ils un edge           |
| `SOURCE_CONFIDENCE_TEST`     | score plus fiable si sources concordent |
| `ACCUMULATION_SCORE_TEST`    | utile pour swing/DCA, pas scalp         |

---

## E. Forward paper-test SPCX

C'est le plus important après live print.

```text
Durée initiale : 20 sessions
Mode : paper-only
Aucun ordre réel
Tous les setups loggés, même rejetés
```

À collecter pour chaque setup :

```text
timestamp
setup_type
grade
entry_candidate
SL
TP1
TP2
result_after_15m
result_after_30m
result_after_1h
MFE
MAE
R multiple
reason_codes
scores
data_quality
```

---

# [4] Métriques de validation

## [13_ESTABLISHED]

Un setup ne devient exploitable que si ses stats sont acceptables.

| Métrique              | Utilité                |
| --------------------- | ---------------------- |
| `winrate`             | taux de réussite       |
| `expectancy_R`        | valeur réelle du setup |
| `profit_factor`       | robustesse             |
| `max_drawdown_R`      | risque                 |
| `avg_MFE`             | potentiel              |
| `avg_MAE`             | douleur avant gain     |
| `time_to_TP1`         | efficacité             |
| `false_positive_rate` | bruit                  |
| `setup_frequency`     | rareté                 |
| `slippage_estimate`   | réalité exécution      |
| `spread_cost`         | coût liquidité         |
| `halt_risk_count`     | risque IPO             |
| `score_bucket_perf`   | A+ vs A vs B           |

Critère minimal avant confiance :

```text
expectancy_R > 0
profit_factor > 1.2
false_positive_rate contrôlé
drawdown acceptable
au moins 20 à 50 occurrences proxy ou forward
```

---

# [5] Classement final des setups

## A+

```text
price_status live
volume élevé
spread acceptable
VWAP aligné
ORB ou SMC confirmé
news/catalyst positif ou neutre
risk_score acceptable
trade_ready_score élevé
```

## A

```text
setup valide
volume correct
source_confidence correcte
risque maîtrisé
mais contexte moins fort que A+
```

## B

```text
setup visible
mais volume, liquidité, news ou contexte incomplet
paper-watch seulement
```

## Reject

```text
pas de prix live
spread trop large
volume faible
Nasdaq contradiction
halt risk
chase trop loin VWAP
score risk trop élevé
données contradictoires
```

---

# [16_TODO] — prochain chantier logique

Créer :

```text
GO_SPACEX_V2_SETUP_SELECTION_AND_BACKTEST_PLAN_01
```

Contenu à figer :

```text
1. gates de sélection
2. catalogue setups
3. backtests proxy IPO
4. backtests secteur/halo
5. backtests intraday
6. forward paper-test SPCX
7. métriques de validation
8. règles A+ / A / B / reject
9. invariants no-live-price / no-trade-ready
```

---

# [17_RESUME_POINT]

```text
Les setups seront sélectionnés par gates :
data validity → market safety → setup detected → score validation.

Stratégies testées :
IPO ORB, VWAP reclaim/hold/reject, IPO price reclaim, FVG/BOS/CHOCH, liquidity sweep, volume breakout, news breakout, accumulation zones.

Backtests prévus :
proxy IPO, secteur/halo, intraday replay, score engine, forward paper-test SPCX réel.

Invariant :
aucun setup trade-ready sans premier print live, volume réel, liquidité acceptable et score validé.
```
