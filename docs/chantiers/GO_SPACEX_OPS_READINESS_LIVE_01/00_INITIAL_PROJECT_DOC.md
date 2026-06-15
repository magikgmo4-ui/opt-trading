---
doc_id: GO_SPACEX_OPS_READINESS_LIVE_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_SPACEX_OPS_READINESS_LIVE_01
parent_go: GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01
status: open
role: OPS_REVIEW_SPCX_READINESS
created_at: 2026-06-14
---

# GO_SPACEX_OPS_READINESS_LIVE_01

## Objet

Verifier et hardenir le stack SPCX pour la session live de lundi. Le code est deploye mais il manque les validations runtime, le monitoring freshness, et les garde-fous source_quality.

## 7_CANONICAL_STATE

```text
Code: merge sur sot/mainline (317c34b1)
admin-trading: deploye, timers actifs
Services: webhook_server:8000, perf_app:8010
Gaps:
  - Pas de ops_ready_check.sh automatise
  - Pas de freshness watchdog (stale detection)
  - Pas de source_quality explicite (direct vs fallback)
  - Pas de degraded mode / trade_ready cap
  - Modifs locales non sauvegardees en patch
  - CDP cursor-ai non verifie
  - CI non visible sur le commit
```

## 6_FINAL_TARGET

```text
SPCX_OPS_READY_LIVE_V1

Avant lundi matin:
  1. Modifs locales sauvegardees en patch
  2. Ops_ready_check.sh fonctionnel
  3. Source_quality dans latest_snapshot (live/delayed/fallback/synthetic)
  4. Freshness watchdog avec degraded mode
  5. CDP cursor-ai verifie
  6. Smoke complet passe
```

## 4_MASTER_PROJECT_PLAN

### P0 — avant lundi matin

1. Sauvegarder les modifs locales (`webhook_server.py`, `capture_headless.js`) en patch
2. Creer `scripts/ipo/spacex_ops_ready_check.sh` — verif complete du stack
3. Ajouter `source_quality` dans le pipeline de scoring
4. Ajouter freshness watchdog dans `run_full_pipeline()` avec degraded mode
5. Verifier CDP cursor-ai (port 9222, alert-list)
6. Smoke complet

### P1 — apres premiere session

1. CI minimale (syntax, schema, import, scorers tests)
2. Freshness watchdog integration Telegram alerts
3. Ops_ready_check.sh → rapport automatique

## 8_VALIDATED_PLAN

### Livrables

```text
scripts/ipo/spacex_ops_ready_check.sh          — verif runtime complete
modules/ipo_tracking/source_quality.py          — classification quality source
modules/ipo_tracking/freshness_watchdog.py      — stale detection + degraded mode
reports/ipo/spacex/local_runtime_overrides.patch — sauvegarde modifs locales
```

## 9_SELECTED_SOLUTION

### ops_ready_check.sh

Check automatise de tous les composants avant session:
- git commit attendu
- services (webhook:8000, perf:8010, cloudflared)
- timers (orderflow 1m, EOD backtest)
- dernier snapshot frais
- dernier bucket orderflow
- dernier event webhook
- CDP cursor-ai (port 9222, alert-list)
- disk free
- journal errors

### source_quality.py

Classification explicite par source:
- spot_price: live | delayed | fallback | synthetic
- orderbook: l2_direct | sip_nbbo | broker | tv_dom | fallback
- tape: sip | vendor | synthetic | unavailable
- perp: synthetic_direct | proxy
- ownership: sec_reported | estimated | unknown

### freshness_watchdog.py

A chaque cycle pipeline:
- last_orderflow_bucket_age_seconds
- last_spcx_price_age_seconds
- last_tv_webhook_age_seconds
Si stale > seuil → pipeline_state = "degraded" → trade_ready cap → Telegram warning

## 11_KEY_DECISIONS

- Les modifs locales sur admin-trading ne seront PAS commitees dans le repo (sont specifiques a admin-trading)
- Le source_quality est un champ obligatoire dans latest_snapshot, pas optionnel
- Le degraded mode cap le trade_ready a 40 max (jamais A/A+ en degraded)
- Le ops_ready_check.sh doit etre idempotent et rapide (<10s)
- SPCXUSDT perp ne valide jamais la liquidite Nasdaq spot

## 12_INVARIANTS

- Ne pas modifier webhook_server.py ou capture_headless.js (modifs locales preservees)
- Ne pas toucher aux timers systemd deja actifs
- Ne pas executer d'ordre live (monitor-only)
- Ne pas exposer de secrets dans les scripts/reports
- Toute classification source_quality doit etre documentee dans le schema

## 15_REMAINING_GAP

- CI GitHub: pas de workflow run visible sur le merge commit
- Real TradingView fire: a confirmer lundi
- L2/tape feed reel: depend du vendor/broker branche
- CDP cursor-ai: depend de la machine Windows

## 16_TODO

1. Creer ops_ready_check.sh
2. Sauvegarder modifs locales en patch
3. Implem source_quality.py
4. Implem freshness_watchdog.py
5. Wirer dans pipeline.py
6. Smoke + verifier sur admin-trading

## 17_RESUME_POINT

```text
GO_SPACEX_OPS_READINESS_LIVE_01
Chantier ouvert le 2026-06-14.
Objectif: hardenir le stack SPCX pour la session live de lundi.
Reprendre ici: docs/chantiers/GO_SPACEX_OPS_READINESS_LIVE_01/
```
