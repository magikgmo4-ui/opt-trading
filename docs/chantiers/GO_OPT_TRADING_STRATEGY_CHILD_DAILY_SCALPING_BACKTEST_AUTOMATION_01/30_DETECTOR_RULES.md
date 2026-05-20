---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_BACKTEST_AUTOMATION_01_DETECTOR_RULES
doc_type: detector_rules
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_BACKTEST_AUTOMATION_01
status: open
updated_at: 2026-05-20
---

# 30_DETECTOR_RULES

Règles mécaniques reproductibles — proxy SMC/ICT sans subjectivité.

## ORB (Opening Range Breakout)

```text
orb_high = max(high) des N premières minutes de session (défaut N=30)
orb_low  = min(low)  des N premières minutes de session

ORB_BREAKOUT_LONG  : close > orb_high (bougie suivant la fermeture de l'ORB)
ORB_BREAKOUT_SHORT : close < orb_low

ORB_RETEST_LONG  : low <= orb_high et close > orb_high après breakout long
ORB_RETEST_SHORT : high >= orb_low  et close < orb_low  après breakout short
```

## Swing High / Swing Low (proxy structure)

```text
N = fenêtre locale (défaut N=5 bougies de chaque côté)

swing_high[i] = high[i] == max(high[i-N:i+N+1])
swing_low[i]  = low[i]  == min(low[i-N:i+N+1])
```

## Sweep (liquidité)

```text
SWEEP_LOW  : low[i] < swing_low récent ET close[i] > swing_low récent
             → bougie clôture au-dessus du low balayé

SWEEP_HIGH : high[i] > swing_high récent ET close[i] < swing_high récent
             → bougie clôture en dessous du high balayé
```

## CHOCH / BOS proxy

```text
CHOCH_LONG (Change of Character) :
  après un SWEEP_LOW :
  close[i] > dernier swing_high mineur (depuis le swing_low)

BOS_LONG (Break of Structure) :
  close[i] > swing_high précédent (dans la direction du mouvement)

CHOCH_SHORT / BOS_SHORT : symétrique
```

## VWAP regime

```text
VWAP_BULL : close > vwap_session
VWAP_BEAR : close < vwap_session
VWAP_RETEST_LONG  : low <= vwap ET close > vwap après VWAP_BULL
VWAP_RETEST_SHORT : high >= vwap ET close < vwap après VWAP_BEAR
```

## Retest zone

```text
OB_ZONE   : dernière bougie impulsive opposée avant le CHOCH/BOS
FVG_ZONE  : écart entre high[i-1] et low[i+1] sur bougie impulsive
RETEST    : prix retourne dans la zone OB ou FVG sans invalider le sweep
```

## Invalidation

```text
LONG invalidé  : close < low du sweep
SHORT invalidé : close > high du sweep
```

## Paramètres configurables (config.yaml)

```yaml
orb_minutes: 30
swing_n: 5
min_rr: 1.8
min_score: 7
spread_pips: 3.0
slippage_pips: 1.0
risk_pct: 0.5
```
