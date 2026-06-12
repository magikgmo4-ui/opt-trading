---
doc_id: GO_SPACEX_V2_BACKTEST_RUNNER_AND_PAPER_LOGGER_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_SPACEX_V2_BACKTEST_RUNNER_AND_PAPER_LOGGER_01
parent_go: GO_SPACEX_V2_SETUP_SELECTION_AND_BACKTEST_PLAN_01
status: draft
lifecycle_stage: design
surface: docs/chantiers
source_kind: canonical
created_at: 2026-06-12
links:
  - docs/chantiers/GO_SPACEX_MASTER_PROJECT_V5/00_MASTER_PROJECT.md
  - docs/chantiers/GO_SPACEX_MASTER_PROJECT_V5/50_MEGA_SETUP_CATALOG.md
  - docs/chantiers/GO_SPACEX_MASTER_PROJECT_V5/60_MEGA_BACKTEST_FRAMEWORK.md
  - docs/chantiers/GO_SPACEX_V2_SETUP_SELECTION_AND_BACKTEST_PLAN_01/00_INITIAL_PROJECT_DOC.md
  - modules/perf_engine/
  - tools/strategy/
  - data/perf/
  - data/ipo/
---

# GO_SPACEX_V2_BACKTEST_RUNNER_AND_PAPER_LOGGER_01

## [6_FINAL_TARGET]

Implémenter le **runner** qui transforme le plan de sélection/backtest en exécution paper-only : détecter les setups SPCX en temps réel, logger tous les candidats (acceptés et rejetés), calculer les métriques de performance, classifier A+/A/B/reject, et exporter vers les surfaces de sortie (Desk, Sheets, Telegram).

Aucun ordre réel. Monitoring et logging exclusivement.

---

# [1] Architecture cible

## [7_CANONICAL_STATE]

Le runner est composé de 4 composants, tous paper-only :

```text
┌─────────────────────────────────────────────────────────┐
│                   SPCX V2 Runner                         │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Setup        │  │ Paper        │  │ Performance  │  │
│  │ Detector     │──│ Logger       │──│ Calculator   │  │
│  │              │  │              │  │              │  │
│  │ gates 0-3    │  │ candidates   │  │ MFE/MAE/R    │  │
│  │ classify     │  │ accepted     │  │ expectancy   │  │
│  │ A+/A/B/      │  │ rejected     │  │ winrate      │  │
│  │ reject       │  │ results      │  │ drawdown     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │                   Export Layer                    │   │
│  │  Desk Pro  │  Google Sheets  │  Telegram  │  JSON│   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## Composant 1 — Setup Detector

Applique les 4 gates du parent :

```text
GATE 0 — DATA VALIDITY
  price_status = live → bars_count > 0 → volume > 0
  → price_trust > 0 → source_count >= 1

GATE 1 — MARKET SAFETY
  spread acceptable → volume suffisant
  → pas de halt → pas de contradiction sources

GATE 2 — SETUP DETECTED
  match contre catalogue parent :
  IPO_ORB_5M/15M/30M, VWAP_HOLD/RECLAIM/REJECT,
  FVG_BULLISH/BEARISH, BOS_CONTINUATION, CHOCH_REVERSAL,
  LIQUIDITY_SWEEP, IPO_PRICE_RECLAIM, NEWS_CATALYST_BREAKOUT, etc.

GATE 3 — SCORE VALIDATION
  trade_ready_score, liquidity_score, risk_score,
  catalyst_score, smart_money_score
```

Sortie : `setup_candidate` JSON avec `grade: A+|A|B|reject` + `reason_codes`.

---

## Composant 2 — Paper Logger

Logge TOUS les candidats, même rejetés :

```json
{
  "ts": "2026-06-12T14:30:00Z",
  "symbol": "SPCX",
  "setup_type": "IPO_ORB_15M",
  "grade": "A",
  "status": "paper_only",
  "gates": {
    "gate_0_data_validity": "PASS",
    "gate_1_market_safety": "PASS",
    "gate_2_setup_detected": "PASS",
    "gate_3_score_validated": "PASS"
  },
  "scores": {
    "trade_ready": 78,
    "liquidity": 72,
    "risk": 38,
    "smart_money": 70,
    "catalyst": 65
  },
  "entry_zone": "above ORB high + VWAP hold",
  "invalidation": "below VWAP or ORB midpoint",
  "tp_logic": ["TP1 1R", "TP2 2R", "runner VWAP/trend"],
  "reason_codes": ["ORB_15M_BREAK", "VWAP_ALIGNED", "VOLUME_CONFIRMED"]
}
```

Stockage : `data/ipo/spacex/paper_log/YYYY-MM-DD/` ou `data/perf/spcx_v2/`.

---

## Composant 3 — Performance Calculator

Pour chaque setup loggé, recalcule après délai :

| Champ            | Délai     | Calcul                      |
| ---------------- | --------- | --------------------------- |
| `result_15m`     | 15 min    | P&L après 15m               |
| `result_30m`     | 30 min    | P&L après 30m               |
| `result_1h`      | 1 heure   | P&L après 1h                |
| `result_eod`     | clôture   | P&L fin de session          |
| `MFE`            | continu   | Maximum Favorable Excursion |
| `MAE`            | continu   | Maximum Adverse Excursion   |
| `R_multiple`     | clôture   | result / risk_R             |
| `hit_tp1`        | trigger   | bool si TP1 touché          |
| `hit_tp2`        | trigger   | bool si TP2 touché          |
| `hit_sl`         | trigger   | bool si invalidation touchée|

Métriques agrégées par setup_type :

| Métrique              | Seuil minimal       |
| --------------------- | ------------------- |
| `winrate`             | —                   |
| `expectancy_R`        | > 0                 |
| `profit_factor`       | > 1.2               |
| `max_drawdown_R`      | acceptable          |
| `avg_MFE`             | —                   |
| `avg_MAE`             | —                   |
| `time_to_TP1`         | —                   |
| `false_positive_rate` | contrôlé            |
| `setup_frequency`     | —                   |
| `score_bucket_perf`   | A+ vs A vs B        |

---

## Composant 4 — Export Layer

### Desk Pro
- Route `/desk/spcx_v2` ou panneau dans `spacex_super_desk`
- Affiche : setups actifs, derniers candidats, stats agrégées, log rejets
- Rafraîchissement toutes les 5 secondes

### Google Sheets
- Onglet `SPCX_V2_PAPER` dans le spreadsheet SpaceX
- Colonnes : ts, setup_type, grade, entry, SL, TP1, TP2, result_15m, result_30m, result_1h, MFE, MAE, R_multiple, reason_codes
- Append-only, une ligne par setup

### Telegram
- Alertes pour setups A+ uniquement
- Format compact : `[A+] SPCX IPO_ORB_15M | entry >42.50 | SL 41.80 | TP1 43.20 TP2 43.90 | scores: TR78 LQ72 RS38`
- Pas d'alerte pour B/reject
- Résumé EOD : setups vus, classés, résultats

### JSON / fichier
- `data/ipo/spacex/paper_log/latest.json` — dernier état
- `data/ipo/spacex/paper_log/summary.json` — stats accumulées
- `data/ipo/spacex/paper_log/rejects.jsonl` — rejets avec reason_codes (debug)

---

# [2] Implémentation

## [5_GO_PLAN]

### Phase 1 — Scaffold

```text
modules/spcx_v2/
├── __init__.py
├── config.py              # thresholds, paths, timeframes
├── setup_detector.py      # gates 0-3, setup matching
├── paper_logger.py        # candidate logging, reject logging
├── perf_calculator.py     # MFE/MAE/R, stats aggregator
├── export_desk.py         # Desk Pro panel / JSON endpoint
├── export_sheets.py       # Google Sheets append
├── export_telegram.py     # Telegram alerts + EOD summary
├── runner.py              # main loop / scheduler
└── scripts/
    ├── cmd.sh             # CLI entry point
    ├── menu.sh            # interactive menu
    ├── sanity_check.sh    # validates installation
    └── install_shortcuts.sh
```

### Phase 2 — Core logic

1. **setup_detector.py**
   - Importe le catalogue setups depuis la config
   - Implémente les 4 gates comme des fonctions pures
   - Prend un snapshot de marché (price, volume, VWAP, spread, halt)
   - Retourne `SetupCandidate` avec grade + reason_codes

2. **paper_logger.py**
   - `log_candidate(candidate)` → écrit dans `rejects.jsonl` ou `candidates.jsonl`
   - `log_result(candidate_id, perf_data)` → met à jour avec MFE/MAE/R
   - `get_summary()` → stats agrégées par setup_type et grade

3. **perf_calculator.py**
   - Schedule les calculs à T+15m, T+30m, T+1h, EOD
   - Suit le prix en continu pour MFE/MAE
   - Calcule R_multiple, hit_tp1, hit_tp2, hit_sl
   - Agrège les stats par bucket

4. **runner.py**
   - Boucle principale : poll TradingView/Bot Vision → détecter → logguer → attendre → calculer
   - Mode `--once` : un seul cycle
   - Mode `--watch` : continu (pour sessions live)
   - Mode `--replay` : replay depuis fichier JSONL (pour backtest proxy)

### Phase 3 — Exports

5. **export_desk.py**
   - Endpoint FastAPI dans `perf_app.py` ou route standalone
   - JSON /desk/spcx_v2/status, /desk/spcx_v2/candidates, /desk/spcx_v2/stats

6. **export_sheets.py**
   - Utilise `modules/google_sheets_global_schema/` existant
   - Append row par setup loggé
   - Onglet dédié `SPCX_V2_PAPER`

7. **export_telegram.py**
   - Utilise `shared/telegram_notify.py` existant
   - Filtre A+ seulement pour alertes temps réel
   - Résumé EOD pour tous les grades

### Phase 4 — Replay / backtest mode

8. **Replay engine**
   - Lit un fichier de données historiques (bars OHLCV + VWAP + volume)
   - Rejoue le setup detector sur chaque barre
   - Logge les candidats comme en live
   - Calcule les performances avec les prix réels suivants
   - Produit les mêmes exports que le mode live

---

# [3] Intégration avec l'existant

| Module existant                | Rôle pour SPCX V2                    |
| ------------------------------ | ------------------------------------ |
| `modules/perf_engine/`         | modèle position (candidate→active→closed) |
| `tools/strategy/`              | patterns de backtest réutilisables   |
| `modules/desk_pro/`            | surface Desk Pro pour affichage      |
| `modules/google_sheets_global_schema/` | écriture Sheets                |
| `shared/telegram_notify.py`    | envoi alertes Telegram               |
| `data/perf/`                   | stockage résultats paper             |
| `data/ipo/spacex/`             | stockage spécifique SPCX             |
| `modules/data_center/`         | publication canonical values         |
| `modules/bot_vision_step2/`    | capture headless (confirmation SMC)  |

---

# [4] Sources de données pour le runner

## Données temps réel

| Source               | Ce qu'elle fournit                        |
| -------------------- | ----------------------------------------- |
| TradingView webhook  | alertes avec price, volume, indicateurs   |
| Bot Vision headless  | captures charte (confirmation FVG/BOS/CHOCH) |
| Yahoo Finance        | prix, VWAP, volume (fallback)             |
| Nasdaq.com           | halt status, IPO price                    |
| Coinglass            | contexte liquidité / OI (si dispo)        |

## Données historiques (pour replay/backtest)

| Source               | Format          |
| -------------------- | --------------- |
| TV alerts archivées  | JSONL           |
| Bot Vision captures  | JSON            |
| Yahoo daily bars     | CSV             |
| Proxy IPO univers    | CSV (RKLB, ASTS, RDW, LUNR, PL, etc.) |

---

# [5] Invariants

```text
INVARIANT 1 — PAPER ONLY
  Aucun ordre réel. Aucun bridge vers execution_engine.
  Le runner ne peut pas déclencher d'ordre.

INVARIANT 2 — NO LIVE PRICE = NO SETUP
  Si le prix n'est pas live (delayed, stale, manquant),
  aucun setup n'est émis. GATE 0 bloque.

INVARIANT 3 — TOUT EST LOGGÉ
  Même les rejets sont loggés avec reason_codes.
  Rien n'est silencieux.

INVARIANT 4 — AUCUN SECRET
  Pas de clé API dans le code.
  Token Telegram et credentials Sheets via .env uniquement.

INVARIANT 5 — SCORES DOCUMENTÉS
  Chaque score (trade_ready, liquidity, risk, smart_money, catalyst)
  a une règle de calcul explicite et testable.
```

---

# [6] Métriques de succès du chantier

```text
- [ ] Setup detector passe les 4 gates sur données mock
- [ ] Paper logger écrit candidats acceptés et rejetés
- [ ] Perf calculator calcule MFE/MAE/R après délai
- [ ] Export Desk affiche les setups actifs
- [ ] Export Sheets append une ligne par setup
- [ ] Export Telegram alerte A+ seulement
- [ ] Mode --once fonctionne sur un snapshot
- [ ] Mode --replay fonctionne sur données proxy IPO
- [ ] Runner ne déclenche aucun ordre réel
- [ ] Tests unitaires pour chaque gate
- [ ] Tests unitaires pour chaque export
- [ ] Smoke test complet paper-only
```

---

# [7] Exclusions

```text
- Pas d'intégration avec execution_engine
- Pas de bridge vers broker API
- Pas de gestion de position réelle
- Pas de risk management réel (seulement scoring)
- Pas de modification des modules existants sauf ajout de routes Desk Pro
- Pas de backtest proxy IPO réel (juste le mode --replay avec données fournies)
```

---

# [16_TODO] — prochain chantier logique

Après merge de celui-ci :

```text
GO_SPACEX_V2_LIVE_PAPER_TEST_20_SESSIONS_01
```

Objectif : exécuter 20 sessions paper avec SPCX réel, collecter les stats, valider ou invalider chaque setup, et décider quels setups promouvoir en mode live.

---

# [17_RESUME_POINT]

```text
Runner paper-only qui :
1. détecte les setups via les 4 gates du parent
2. loggue tous les candidats (acceptés + rejetés)
3. calcule MFE / MAE / R multiple / winrate / expectancy
4. classe A+ / A / B / reject
5. exporte vers Desk, Sheets, Telegram, JSON

Respecte 5 invariants : paper-only, no-live-price = no-setup,
tout loggé, zéro secret, scores documentés.

S'intègre avec l'existant sans le modifier :
perf_engine, desk_pro, google_sheets, telegram_notify, data_center.

Deux modes : --watch (live) et --replay (backtest proxy).
```
