---
doc_id: GO_DESKPRO_VOICE_OPERATOR_01_LOT_A_AUDIT
doc_type: audit_report
repo: opt-trading
go_id: GO_DESKPRO_VOICE_OPERATOR_01
status: completed
created_at: 2026-06-15
lot: A
---

# 10_LOT_A_DESKPRO_AUDIT

## 1_SCOPE

Audit complet de l'ecosysteme DeskPro et services peripheriques pour identifier toutes les sources de donnees exploitables par l'operateur vocal.

Perimetre : webhook_server, perf_app, Desk Pro, LocalCMS, Memory Bricks, IPO tracking pipeline.

## 2_SOURCE_OF_TRUTH_CANDIDATES

| # | Source | Type | Fraicheur | Voix-ready |
|---|--------|------|-----------|------------|
| 1 | `GET /desk/spacex/command-center` | JSON API | Live | Oui |
| 2 | `GET /desk/status` | JSON API | Live | Oui |
| 3 | `GET /desk/snapshot` | JSON API | Live | Oui |
| 4 | `GET /perf/summary` | JSON API | Live | Oui |
| 5 | `GET /perf/open` | JSON API | Live | Oui |
| 6 | `GET /api/state` | JSON API | Live | Oui |
| 7 | `GET /cms/signals/summary` | JSON API | Live | Oui |
| 8 | `GET /cms/spacex/json` | JSON API | Live | Oui |
| 9 | `GET /desk/alerts` | JSON API | Live | Oui |
| 10 | `data/ipo/spacex/scored/latest_snapshot.json` | Fichier JSON | Pipeline | Oui (via /desk/spacex/snapshot) |
| 11 | `data/ipo/spacex/paper_log/summary.json` | Fichier JSON | Pipeline | Oui (via SPCX V2 runner) |

## 3_SETUPS_LOCATION

### Producteurs de setups

| Producteur | Fichier | Setup types | Format sortie |
|------------|---------|-------------|---------------|
| SPCX V2 detect | `modules/spcx_v2/setup_detector.py` | 35 setups (ipo/vwap/smc/momentum/news/accumulation) | `SetupCandidate` → `paper_log/candidates.jsonl` |
| Desk Pro form | `modules/desk_pro/service/scoring.py` | Probabilite directionnelle | `ScoreResult` (prob 0-1) |
| IPO scoring | `modules/ipo_tracking/scoring/__init__.py` | momentum/news/smart_money/risk/trade_ready/accumulation | `latest_snapshot.json` |
| TV webhook | `webhook_server.py` | COINM_SHORT, USDTM_LONG, GOLD_CFD_LONG | `perf.db` trades table |
| Decision engine | `modules/decision_engine/app/strategy_logic.py` | Signal BUY/SELL/FLAT | `Signal` dataclass |

### Endpoints lisibles

| Endpoint | Setup data exposee |
|----------|-------------------|
| `GET /desk/spacex/command-center` | top_setup, setup_type, probability, action, confidence |
| `GET /perf/open` | trades actifs (COINM_SHORT, USDTM_LONG, GOLD_CFD_LONG) |
| `GET /cms/signals` | signaux Telegram par channel/paire/direction |
| `GET /api/state` | active_engine courant |

### Manques pour l'operateur vocal

- Pas de `GET /read/setups` agregeant tous les setups (SPCX + TV + Telegram)
- Pas de `GET /read/setup/{symbol}` filtrant par symbole
- Les candidats paper_log sont en JSONL, pas exposes via API

## 4_SCORES_LOCATION

### Producteurs de scores

| Producteur | Fichier | Scores produits |
|------------|---------|-----------------|
| SPCX V2 compute_scores | `modules/spcx_v2/setup_detector.py:136` | trade_ready, liquidity, risk, smart_money, catalyst (0-100) |
| IPO score_snapshot | `modules/ipo_tracking/scoring/__init__.py:4` | momentum, news_velocity, sec_activity, smart_money, risk, trade_ready, accumulation (0-1) |
| Desk Pro probability | `modules/desk_pro/service/scoring.py:16` | probability (0-1), score, reasons |
| Orderflow score | `modules/ipo_tracking/scoring/spcx_orderflow_score.py` | Composite 0-100 (liquidity, tape_flow, auction, volume_quality, price_context) |
| Ownership pressure | `modules/ipo_tracking/scoring/spcx_ownership_pressure_score.py` | Composite 0-100 (insider_concentration, lockup_overhang, institutional_quality, cost_basis, greenshoe) |
| VWAP analyzer | `modules/ipo_tracking/scoring/vwap_analyzer.py` | vwap_score 0-100 |

### Endpoints lisibles

| Endpoint | Scores exposes |
|----------|---------------|
| `GET /desk/spacex/command-center` | edge_score, open_score, trade_ready, momentum, risk, smart_money, confidence |
| `GET /desk/spacex/snapshot` | Tous les scores IPO (scores.momentum, scores.trade_ready, etc.) |
| `GET /desk/form` (POST) | probability, score, reasons |
| `GET /perf/strategy/{id}/promotion_gate` | Gate score + events |

### Manques

- Pas de `GET /read/scores` agregeant tous les scores par symbole
- Pas de `GET /read/score/{symbol}` pour un resume mono-symbole
- Pas d'exposition API des scores orderflow/ownership/VWAP (dans latest_snapshot mais pas de route dediee)

## 5_ALERTS_LOCATION

### Producteurs d'alertes

| Producteur | Fichier | Declencheur |
|------------|---------|-------------|
| Desk Pro health | `modules/desk_pro/api/routes.py:104` | Pipeline degraded/down → Telegram + webhook |
| SPCX V2 export | `modules/spcx_v2/export_telegram.py:51` | A+ candidates → Telegram |
| IPO scoring alerts | `modules/ipo_tracking/scoring/spacex_score.py:129` | Score thresholds → Telegram |
| Telegram dispatcher | `modules/ipo_tracking/telegram_dispatcher.py:5` | Generic SpaceX alerts |
| Notification dispatcher | `modules/notification_dispatcher/` | Health/error alerts |
| Coinglass parser | `modules/telegram_screener/parser/coinglass_parser.py:55` | Coinglass liquidation alerts |

### Endpoints lisibles

| Endpoint | Alertes exposees |
|----------|-----------------|
| `GET /desk/alerts?limit=10` | Dernieres N alertes, destinations, etat |
| `GET /desk/status` | alert_state (triggered, cooldown) |
| `GET /desk/errors?limit=20` | Erreurs recentes |

### Manques

- Pas de `GET /read/alerts` agregeant toutes les sources (DeskPro + Telegram + TV + SPCX)
- Pas de `GET /read/alerts/critical` filtrant par severite

## 6_REPORTS_LOCATION

### Producteurs de rapports

| Producteur | Fichier | Format |
|------------|---------|--------|
| IPO daily report | `modules/ipo_tracking/reports.py:6` | Markdown `reports/ipo/spacex/spacex_daily_{date}.md` |
| Orderflow report | `modules/ipo_tracking/reports.py:20` | Markdown `spcx_day1_orderflow_ownership_{date}.md` |
| SPCX V2 daily | `modules/spcx_v2/daily_summary.py:56` | Markdown `spcx_v2_daily_{date}.md` |
| Ops ready check | `scripts/ipo/spacex_ops_ready_check.sh` | Markdown `ops_ready_{ts}.md` |

### Manques

- Pas de `GET /read/report/daily` retournant le rapport en JSON
- Pas de `GET /read/report/summary` avec un resume vocal-friendly
- Les rapports sont en Markdown, non exposes via API REST

## 7_EXISTING_ENDPOINTS

64 endpoints decouverts sur 5 services :

| Service | Port | GET | POST | Total |
|---------|------|-----|------|-------|
| webhook_server | 8000 | 7 | 4 | 11 |
| perf_app | 8010 | 6 | 3 | 9 |
| Desk Pro (/desk) | 8010 | 15 | 2 | 17 |
| LocalCMS (/cms) | 8010 | 23 | 0 | 23 |
| Memory Bricks | — | 7 | 0 | 7 |

Top 3 endpoints pour l'operateur vocal :

1. **`GET /desk/spacex/command-center`** — le plus riche : prix, gap, scores, action, setup, confiance, risques, pipeline health
2. **`GET /desk/status`** — sante globale de tous les services + alert state
3. **`GET /desk/spacex/snapshot`** — snapshot score complet avec orderflow/ownership/VWAP

## 8_MISSING_ENDPOINTS

Gaps identifies :

| Domaine | Endpoint manquant | Priorite |
|---------|-------------------|----------|
| Setups | `GET /read/setups` | P0 |
| Setups | `GET /read/setup/{symbol}` | P0 |
| Scores | `GET /read/scores` | P0 |
| Scores | `GET /read/score/{symbol}` | P0 |
| Alertes | `GET /read/alerts` | P1 |
| Alertes | `GET /read/alerts/critical` | P1 |
| Rapports | `GET /read/report/daily` | P1 |
| Systeme | `GET /read/system` | P0 |

## 9_READ_API_CANDIDATES

Contrat API propose pour Lot B :

```text
GET /read/system
  → etat de tous les services, timers, pipeline_state, degraded flags

GET /read/setups
  → setups actifs : SPCX (candidates A+/A), TV (COINM_SHORT/USDTM_LONG/GOLD_CFD_LONG), Telegram signaux

GET /read/setup/{symbol}
  → setup detaille pour SPCX, BTC, XAU, etc.

GET /read/scores
  → tous les scores probabilistes par symbole

GET /read/score/{symbol}
  → scores detailles : trade_ready, momentum, risk, smart_money, VWAP, orderflow, ownership

GET /read/alerts
  → dernieres alertes toutes sources confondues

GET /read/report/daily
  → resume quotidien vocal-friendly (pas le markdown brut)
```

## 10_RISKS

| Risque | Impact | Mitigation |
|--------|--------|------------|
| DeskPro endpoints non documentes | Voix ne sait pas quoi appeler | Cet audit servira de reference |
| Changement de schema sans versioning | Break du voice operator | Ajouter `schema_version` dans les reponses |
| Endpoints lents (>2s) | Mauvaise experience vocale | Mettre en cache les donnees frequent lues |
| Services down | Silence vocal | Implementer fallback "service indisponible" |
| Donnees degradees prises pour live | Fausse confiance | Lire `pipeline_state` + `source_quality` avant de parler |

## 11_DECISION_FOR_LOT_B

**DECISION : Le contrat API `/read/*` sera implemente comme une couche FastAPI legere dans `modules/voice_operator/` qui agrege les endpoints existants.**

```text
modules/voice_operator/
  api/
    routes.py          ← /read/* endpoints (FastAPI router)
  readers/
    deskpro_reader.py  ← lit GET /desk/* + latest_snapshot
    perf_reader.py     ← lit GET /perf/*
    alerts_reader.py   ← lit GET /desk/alerts + Telegram
    system_reader.py   ← lit /api/state + /desk/status + ops_ready_check
  formatters/
    voice_format.py    ← formate les reponses JSON en texte vocal-friendly
```

Avantages :
- Zero modification des services existants (invariant respecte)
- Read-only, pas de side effects
- Aggregation centralisee
- Les readers sont des wrappers HTTP legers autour des APIs existantes
- Facile a tester independamment

Prochaine etape : Lot B — implementer `modules/voice_operator/api/routes.py` avec les endpoints `/read/*`.
