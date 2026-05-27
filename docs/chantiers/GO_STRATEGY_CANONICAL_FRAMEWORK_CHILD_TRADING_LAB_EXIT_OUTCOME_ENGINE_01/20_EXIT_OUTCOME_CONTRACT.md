---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_TRADING_LAB_EXIT_OUTCOME_ENGINE_01
doc_type: contract
---

# Contrat exit_outcome_v1

## `calc_tp(entry, sl, rr, direction) → float`

```
risk = abs(entry - sl)
tp = entry + risk*rr  (bullish)
tp = entry - risk*rr  (bearish)
```

## `resolve_exit_outcome(entry, sl, rr_planned, direction, post_candles, max_bars=60) → dict`

Scan séquentiel `post_candles[:max_bars]` :

| Condition | Résultat |
|---|---|
| sl_hit ET tp_hit (même chandelier) | loss / `sl_tp_same_candle_conservative_loss` |
| tp_hit seulement | win / `tp_hit` |
| sl_hit seulement | loss / `sl_hit` |
| Épuisement max_bars | timeout / `max_bars_reached` |
| 0 chandeliers fournis | timeout / `no_post_entry_candles` |

Retourne : `{result, r_realized, exit_price, exit_ts, bars_held, outcome_reason, tp}`

## `get_post_entry_candles(all_rows, entry_ts_str, tz_name) → list[dict]`

Filtre strict : `row["ts"] > entry_dt`. Timestamp naïf → localisé avec `tz_name`.

## Clé `entry_candle_ts`

Le timestamp réel du chandelier d'entrée (5e chandelier de la fenêtre de signal) est stocké dans les features et les trades sous `entry_candle_ts`. Ce champ est utilisé par `apply_outcomes` pour éviter la confusion avec `entry_ts` (horodatage d'exécution).
