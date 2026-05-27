---
doc_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_PERF_MEASUREMENT_01_PLAN
doc_type: measurement_plan
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_PERF_MEASUREMENT_01
---

# 20 — Plan de mesure xau_session_open_v1

## Stratégie de mesure

Compte tenu de l'absence de données de production, la mesure est en deux volets :

### Volet A — Validation pipeline (sample data)

Exécuter `trading_lab_v1` sur `sample_xauusd_m1.csv` pour les deux sessions.  
Objectif : confirmer que le pipeline end-to-end fonctionne et que les sorties sont cohérentes.

### Volet B — Documentation du gap production

Documenter formellement que `perf_status=UNMEASURED` en production reste valide.  
Décrire les conditions minimales pour une future promotion vers `MEASURED`.

## Métriques cibles

| Métrique | Source disponible | Note |
|---|---|---|
| Nombre d'événements | `events_v1.jsonl` | Volet A: 2 (synthétique) |
| Dates couvertes | `local_date` dans features | Volet A: 2026-04-03, 2026-04-04 |
| Variante dominante | `variant_id` dans features | Volet A: `xau_open_sweep_fvg` |
| Win/Loss ratio | `result` dans trades | Indisponible — tous `virtual_open` |
| RR moyen réalisé | `r_realized` dans trades | Indisponible — `result=open` |
| Drawdown max | Non calculable sans exits | Indisponible |
| Telegram latency | Non mesurable dans ce GO | Hors scope |

## Conditions de promotion future (UNMEASURED → MEASURED)

Pour que `perf_status` puisse être mis à jour vers `MEASURED` :

1. Au moins 20 trades avec `result` ∈ {`win`, `loss`, `breakeven`} dans production
2. Couverture minimale: 30 jours de sessions actives
3. Données source: broker live ou Dukascopy (pas sample synthétique)
4. RR réalisé calculable sur base des exits enregistrés
