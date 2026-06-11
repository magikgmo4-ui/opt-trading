# 20_ACCEPTANCE_REPORT — Runtime Validation

## Verdict: PASS ✅

Date: 2026-06-11 | Admin-trading live

### 1. Views data_center

| View | Count | Status |
|---|---|---|
| market_metrics | 13 symboles | ✅ |
| pair_market_snapshot | 13 symboles | ✅ |
| signal_event | 25 symboles | ✅ |
| telegram_raw | 165 canaux | ✅ |
| runtime_health | services actifs | ✅ |
| telegram_channel_stats | rafraîchi | ✅ |

### 2. LocalCMS

| Page | Status |
|---|---|
| /signals | ✅ 259 signaux, 40 canaux |
| /backtest/summary | ✅ 38 canaux, 160 trades |
| /vision | ✅ Coinglass + screener |
| / (perf KPIs) | ✅ proxy perf:8010 |

### 3. Services systemd

| Service | Status |
|---|---|
| localcms | ✅ active |
| collector-telegram-screener.timer | ✅ active (1h) |
| tv-webhook | ✅ active |
| tv-perf | ✅ active |

### 4. Couverture Desk Pro

| Métrique | Valeur |
|---|---|
| Sources | 12/12 PROVEN |
| MISSING | 0 |
| Score moyen | 0.81 |

### 5. Tests

```bash
pytest tests/data_center/ -q  # 113 passed
cmd.sh telegram stats          # fonctionnel
cmd.sh backtest                # fonctionnel
```

### Notes

- market_metrics et pair_market_snapshot utilisent CoinGecko (gratuit, pas Binance)
- Les views sont atomiques avec contrats versionnés
- L'automatisation horaire couvre les 6 étapes du pipeline
- Aucun MISSING — toutes les sources ont un producer actif
