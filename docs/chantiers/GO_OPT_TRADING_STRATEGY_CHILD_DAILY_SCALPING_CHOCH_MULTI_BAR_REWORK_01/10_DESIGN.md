---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_CHOCH_MULTI_BAR_REWORK_01_DESIGN
doc_type: design
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_CHOCH_MULTI_BAR_REWORK_01
status: open
updated_at: 2026-05-21
---

# 10_DESIGN — CHOCH Multi-Bar Confirmation

## Logique actuelle (défectueuse)

```
bar[i-1] : low < swing_l  (sweep)
bar[i]   : close > swing_l AND close > swing_h  ← CHOCH same-bar requis
```

Probabilité : ~12 occurrences/an sur XAUUSD M5.

## Nouvelle logique

```
bar[i-1] : low < swing_l  (sweep détecté)
bar[i]   : close > swing_l  (récupération confirmée)
bar[i..i+confirm_window] : premier bar dont close > swing_h → CHOCH → ENTRY
```

`confirm_window = 5` (paramètre, défaut 5 barres = 25 min sur M5).

## Pseudo-code

```python
for i in range(lookback + 2, n):
    prev, row = df.iloc[i-1], df.iloc[i]
    swing_l = _last_swing_low(df, i, lookback)
    swing_h = _last_swing_high(df, i, lookback)

    # Sweep low
    if swing_l and prev["low"] < swing_l and row["close"] > swing_l:
        if swing_h:
            for k in range(confirm_window + 1):      # k=0 → même barre (comportement original)
                j = i + k
                if j >= n: break
                if df.iloc[j]["close"] > swing_h:
                    → Setup(entry_bar=j, direction="long", ...)
                    break

    # Sweep high (miroir)
    if swing_h and prev["high"] > swing_h and row["close"] < swing_h:
        if swing_l:
            for k in range(confirm_window + 1):
                j = i + k
                if j >= n: break
                if df.iloc[j]["close"] < swing_l:
                    → Setup(entry_bar=j, direction="short", ...)
                    break
```

## Garanties no look-ahead

- `swing_l` et `swing_h` calculés sur `df.iloc[start:i]` (exclusif) — pas de données futures
- CHOCH cherché sur barres `[i, i+confirm_window]` — toutes disponibles au moment du trade simulé
- Entry price = `df.iloc[j]["close"]` — barre du CHOCH, pas la suivante

## Impact attendu

| Métrique | Avant | Attendu après |
|---|---|---|
| SMC_SWEEP trades/2ans | 19 | 150-400 |
| COMBINED trades/2ans | 6 | 50-150 |
| ORB_ONLY trades | 0 (min_score filter) | 0 (inchangé) |
| Peak RAM | inchangé | inchangé |

## Paramètre confirm_window

Valeur 5 (25 min) choisie comme point de départ :
- Trop petit (1-2) : peu d'amélioration
- Trop grand (10+) : signal dilué, prix trop éloigné du sweep
- 5 barres : standard SMC — le CHOCH doit survenir rapidement après le sweep
