# 30_CALIBRATION_RULES — Règles de transition de grade

## Setup types et grades plafond

| Setup | Condition minimale | Grade max sans CDP | Grade max avec CDP+confluence |
|---|---|---|---|
| support_watch | supports présents | C+ | B- (si CDP low-confidence) |
| vwap_reclaim | CDP vwap_reclaim | B | A- (si aligné + volume) |
| vwap_rejection | CDP vwap_loss | B | A- (si aligné + volume) |

## Règles de montée (upgrade)

```
support_watch → C/C+ (baseline, pas de trigger)
support_watch + CDP → B- (trigger confirmé mais pas de confluence)
vwap_reclaim fresh + LTF bullish → B/B+
vwap_loss fresh + LTF bearish → B/B+
VWAP trigger + volume_spike + HTF/LTF aligned → A-/A
orb_break + volume_spike + VWAP hold → A-
liquidity_sweep + reclaim → B+
```

## Règles de descente (downgrade)

```
stale > 4h → -10 pts, -1 grade
stale > 12h → retour à support_watch (C)
missing critical fields → cap B- maximum
contradiction HTF/LTF → cap B maximum
freshness != fresh → -5 pts confidence
completeness < 50% → -3 pts
```

## Scoring 8 dimensions (weights)

| Dimension | Poids | Impacté par |
|---|---|---|
| htf_alignment | 15 | biais H4 vs setup direction |
| ltf_trigger | 15 | CDP event présent + timeframe |
| vwap_level_quality | 15 | VWAP data ou CDP confirmation |
| volume_orderflow | 15 | volume_spike, relative_volume |
| macro_alignment | 10 | DXY, VIX, risk regime |
| freshness_source | 10 | age données, freshness_state |
| risk_reward | 10 | distance entry→inval vs entry→target |
| backtest_edge | 10 | historique winrate/avg R |

## Grades

```
A+ ≥ 90, A ≥ 80, A- ≥ 70, B+ ≥ 60, B ≥ 50, B- ≥ 40, C ≥ 30, REJECT < 30
```
