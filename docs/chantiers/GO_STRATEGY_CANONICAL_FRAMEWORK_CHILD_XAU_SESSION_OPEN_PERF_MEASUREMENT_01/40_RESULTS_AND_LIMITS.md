---
doc_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_PERF_MEASUREMENT_01_RESULTS
doc_type: results
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_PERF_MEASUREMENT_01
measured_at: 2026-05-27
data_source: synthetic_sample
---

# 40 — Résultats et limites de la mesure

## Run réalisé

Source: `modules/trading_lab_v1/data/sample_xauusd_m1.csv` (données synthétiques)

### Session gold_open_18h — 2026-04-03

| Champ | Valeur |
|---|---|
| `sequence_complete` | `True` (6 candles M1) |
| `variant_id` | `xau_open_sweep_fvg` |
| `first5_direction` | `bullish` |
| `sweep_detected` | `True` |
| `fvg_detected` | `True` |
| `first5_range_points` | `11.0 pts` |
| `entry` | `3207.0` |
| `sl` | `3197.0` (10 pts) |
| `rr_planned` | `2.0` |
| `result` | `open` (virtuel, pas d'exit) |

### Session midnight_00h — 2026-04-04

| Champ | Valeur |
|---|---|
| `sequence_complete` | `True` (6 candles M1) |
| `variant_id` | `xau_open_sweep_fvg` |
| `first5_direction` | `bearish` |
| `sweep_detected` | `True` |
| `fvg_detected` | `True` |
| `first5_range_points` | `8.0 pts` |
| `entry` | `3203.5` |
| `sl` | `3211.0` (7.5 pts) |
| `rr_planned` | `2.0` |
| `result` | `open` (virtuel, pas d'exit) |

## Synthèse de mesure

| Métrique | Valeur | Validité |
|---|---|---|
| Événements traités | 2 | Synthétique uniquement |
| Dates couvertes | 2 (2026-04-03, 2026-04-04) | Synthétique |
| Sessions actives | 2/2 (`gold_open_18h`, `midnight_00h`) | OK |
| Variante dominante | `xau_open_sweep_fvg` (100%) | Non représentatif |
| Win/Loss ratio | **Non calculable** — pas d'exits | — |
| RR réalisé moyen | **Non calculable** — `r_realized=None` | — |
| Drawdown max | **Non calculable** — pas de série temporelle PnL | — |
| Pipeline fonctionnel | **OUI** — features → events → trades OK | Validé |

## Limites de validité

1. **Données synthétiques**: 12 lignes M1, 2 sessions, générées pour test. Non représentatives du marché réel XAUUSD.
2. **Pas d'exits**: tous les trades sont en `result=open` / `execution_state=virtual_open`. Aucun RR réalisé disponible.
3. **Pas de données production**: `state/trading_lab_v1/` n'a aucun historique.
4. **Variant non diversifié**: les 2 observations donnent `xau_open_sweep_fvg` — pas de base pour comparer les 4 variants.

## Verdict perf_status

```
perf_status: UNMEASURED
Justification: aucune donnée de production disponible.
              pipeline validé fonctionnel sur données synthétiques.
              mesure réelle requiert ≥ 20 trades closés en production.
```

La mise à jour de `perf_status` dans `95_STRATEGY_REGISTRY.md` n'est **pas réalisée** dans ce GO — les conditions minimales ne sont pas remplies (cf. `20_XAU_SESSION_OPEN_MEASUREMENT_PLAN.md`).
