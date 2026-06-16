# 50_DOWNGRADE_RULES — Règles de downgrade automatique

## Règles actives dans le scorer

### 1. Stale trigger
```
Si signal_event timestamp > 4h → fraîcheur passe de "fresh" à "stale"
  → freshness_source score passe de 8 à 3
  → confidence_pct -15%
  → grade peut baisser d'un cran
```

### 2. Missing critical fields
```
Si vwap_raw_value absent → vwap_level_quality = 8 (au lieu de 13)
Si volume_confirmation absent → volume_orderflow = 5 (au lieu de 8)
Si orderflow absent → volume_orderflow = 5
Si backtest_edge absent → backtest_edge = 2 (au lieu de 10)
```

### 3. Contradiction HTF/LTF
```
Si htf_trend != ltf_trend et les deux sont non-neutres :
  → htf_alignment score max 5
  → grade cap à B maximum
```

### 4. Complétude faible
```
Si completeness_pct < 50% → confidence_pct -10%
Si completeness_pct < 30% → grade cap à B-
```

### 5. Pas de trigger CDP du tout
```
Si aucun signal dans multitf_analysis_input :
  → fallback à support_watch (C/34 max)
  → pas de upgrade possible sans trigger
```

## Seuils de downgrade

| Condition | Impact |
|---|---|
| signal_age > 4h | -10 pts, grade -1 |
| signal_age > 12h | retour support_watch (C) |
| missing VWAP | -5 pts vwap_quality |
| missing volume | -3 pts volume_orderflow |
| contradiction | cap B max |
| completeness < 30% | cap B- |
| no CDP trigger | cap C+ |
