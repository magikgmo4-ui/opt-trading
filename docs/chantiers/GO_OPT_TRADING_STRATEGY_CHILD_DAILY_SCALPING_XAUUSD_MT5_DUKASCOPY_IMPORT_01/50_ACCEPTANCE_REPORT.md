---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01_ACCEPTANCE_REPORT
doc_type: acceptance_report
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01
status: pending
updated_at: 2026-05-20
---

# 50_ACCEPTANCE_REPORT

**Statut : PENDING — en attente de la source MT5 ou Dukascopy fournie par l'opérateur.**

## Critères d'acceptance

| Critère | Requis | Statut |
|---|---|---|
| `xauusd_m5_canonical.csv` produit | ✅ | ⏳ pending |
| `xauusd_m15_canonical.csv` produit | ✅ | ⏳ pending |
| Tous champs canoniques présents | ✅ | ⏳ pending |
| source ∈ [mt5_export, dukascopy] | ✅ | ⏳ pending |
| Fenêtre ≥ 180 jours | ✅ | ⏳ pending |
| Barres M5 ≥ 50 000 | ✅ | ⏳ pending |
| Validation `validate_canonical()` PASS | ✅ | ⏳ pending |
| Backtest `run_backtest.py` s'exécute sans crash | ✅ | ⏳ pending |
| SMC_SWEEP_ONLY ou COMBINED ≥ 1 setup | ✅ | ⏳ pending |

## À remplir après run

```text
Source utilisée      :
Broker/plateforme    :
Période couverte     :
Barres M5            :
Barres M15           :
Spread moyen M5      :

Backtest résultats (min_score=7) :
  ORB_ONLY           : trades= xx  exp= x.xx  pf= x.xx  → VERDICT
  VWAP_PULLBACK_ONLY : trades= xx  exp= x.xx  pf= x.xx  → VERDICT
  SMC_SWEEP_ONLY     : trades= xx  exp= x.xx  pf= x.xx  → VERDICT
  COMBINED           : trades= xx  exp= x.xx  pf= x.xx  → VERDICT

Décision finale      :
Prochaine étape      :
```

## Commandes de run

```bash
# 1. Normaliser (selon source choisie)
python tools/strategy/daily_scalping/normalize_mt5.py \
    --input data/market/raw/xauusd_m5_raw_mt5.csv \
    --output data/market/xauusd_m5_canonical.csv \
    --timeframe M5 --broker-tz UTC+2

# 2. Valider
python -c "
import pandas as pd, sys
sys.path.insert(0, '.')
df = pd.read_csv('data/market/xauusd_m5_canonical.csv')
print('cols:', list(df.columns))
print('rows:', len(df))
print('source:', df['source'].unique())
print('period:', df['timestamp'].iloc[0], '->', df['timestamp'].iloc[-1])
"

# 3. Backtest
python tools/strategy/daily_scalping/run_backtest.py \
    --input data/market/xauusd_m5_canonical.csv \
    --context-input data/market/xauusd_m15_canonical.csv \
    --out artifacts/backtests/daily_scalping_canonical \
    --min-score 7

# 4. Lire verdict
cat artifacts/backtests/daily_scalping_canonical/xauusd_m5_verdict.md
```
