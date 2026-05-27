---
doc_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_PERF_MEASUREMENT_01_AUDIT
doc_type: audit
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_PERF_MEASUREMENT_01
---

# 10 — Audit des surfaces perf existantes

## Surfaces runtime rattachées à xau_session_open_v1

| Surface | Fichier | Rôle | STRATEGY_ID |
|---|---|---|---|
| `trading_realtime_v1` | `app/event_bridge_v1.py` | Pont événement live | hardcodé `"xau_session_open_v1"` |
| `trading_realtime_v1` | `app/runtime_loop_v1.py` | Boucle runtime live | hardcodé `"xau_session_open_v1"` |
| `trading_lab_v1` | `app/trading_lab_v1.py` | Lab de simulation | `DEFAULT_STRATEGY_ID = "xau_session_open_v1"` |

## Profil de stratégie

- Fichier: `docs/ot/trading/schemas/xauusd_dual_stack_v1.profile.yaml`
- `strategy_id`: `xau_session_open_v1`
- Sessions: `gold_open_18h` (18:00–18:10 ET) + `midnight_00h` (00:00–00:10 ET)
- Mode exécution: `observation` (virtuel)
- Variants actifs: 4 (`xau_open_sweep_fvg`, `xau_open_no_sweep_fvg`, `xau_open_sweep_no_fvg`, `xau_open_no_sweep_no_fvg`)
- `rr_min: 2.0`

## État des données de production

| Source | État |
|---|---|
| `state/trading_lab_v1/events_v1.jsonl` | **N'existe pas** — aucun run de production |
| `state/trading_lab_v1/trades_v1.jsonl` | **N'existe pas** |
| `state/trading_lab_v1/features_v1.jsonl` | **N'existe pas** |
| `state/trading_lab_v1/market_runs_v1.jsonl` | **N'existe pas** |
| `state/trading/events_v1.jsonl` | Non trouvé (référencé dans profile.yaml) |
| `state/events.jsonl` | Existe — événements webhook TV génériques, non filtrés par stratégie |

## Données disponibles pour mesure

- **Source canonique**: `modules/trading_lab_v1/data/sample_xauusd_m1.csv`
  - Type: données synthétiques (générées pour tests)
  - Couverture: 2 dates (2026-04-03, 2026-04-04), 12 lignes M1 XAUUSD ~3200 pts
  - Limitation: données non réelles, non représentatives du marché live

## Conclusion audit

Aucune donnée de production disponible. La mesure sera réalisée sur données synthétiques sample uniquement. Verdict attendu: `perf_status` reste `UNMEASURED` en production ; pipeline validé fonctionnel.
