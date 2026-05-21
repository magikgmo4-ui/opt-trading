---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01_REVISED_BACKTEST_PROTOCOL
doc_type: backtest_protocol
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01
status: open
updated_at: 2026-05-20
---

# 60_REVISED_BACKTEST_PROTOCOL

## Pipeline cible (post-rework)

```
[1] Source OHLCV canonique (broker export / prod collector)
         ↓
[2] Validation source (bloque si source=smoke_yfinance)
         ↓
[3] Merge M5 + M15 (merge_asof no-lookahead)
         ↓
[4] Merge derivatives optionnel (OI, funding, liq, L/S)
         ↓
[5] Indicators (VWAP, ATR, ORB, swings)
         ↓
[6] Detectors — avec CHOCH fenêtre configurable (3-10 bars)
         ↓
[7] Scorer — avec seuils min_score par variant
         ↓
[8] Simulation — spread depuis feed, pas config hardcodé
         ↓
[9] Journal CSV + metrics
         ↓
[10] Bot vision validation layer (optionnel, hors-pipeline automatique)
         ↓
[11] Verdict markdown — avec source_level et regime_coverage
```

## Reworks requis en code

### A — detectors.py : CHOCH fenêtre configurable

**Problème actuel :**
```python
# same-bar CHOCH — quasi impossible sur M5
swept = prev["low"] < swing_l and row["close"] > swing_l
if swept and swing_h is not None and row["close"] > swing_h:
    setups.append(...)
```

**Correction :**
```python
# Fenêtre de confirmation post-sweep : 1 à N bars suivants
def _confirm_choch_long(df, sweep_bar, swing_h, confirm_window=5):
    """Vérifie si price close > swing_h dans les confirm_window bars après sweep."""
    end = min(sweep_bar + confirm_window + 1, len(df))
    for j in range(sweep_bar + 1, end):
        if df.iloc[j]["close"] > swing_h:
            return j  # retourne le bar de confirmation
    return None

# Dans detect_smc_sweep_only :
swept = prev["low"] < swing_l and row["close"] > swing_l
if swept and swing_h is not None:
    confirm_bar = _confirm_choch_long(df, i, swing_h, confirm_window=choch_window)
    if confirm_bar is not None:
        setups.append(Setup(
            index=df.index[confirm_bar],
            entry_bar=confirm_bar,
            ...
        ))
```

Paramètre `choch_window` dans `config.yaml` (défaut : 5 bougies = 25 minutes M5).

### B — scorer.py : min_score par variant

**Problème actuel :** un seul `min_score` global bloque ORB_ONLY (max 5) et VWAP_PULLBACK (max 4).

**Correction :**
```yaml
# config.yaml
scoring:
  min_score_by_variant:
    ORB_ONLY: 4
    VWAP_PULLBACK_ONLY: 3
    SMC_SWEEP_ONLY: 6
    COMBINED_SMC_ORB_VWAP: 7
```

```python
# simulator.py — utiliser le seuil par variant
def simulate_all(setups, scores, df, config):
    thresholds = config.get("scoring", {}).get("min_score_by_variant", {})
    results = []
    for setup, score in zip(setups, scores):
        min_s = thresholds.get(setup.variant, config.get("min_score", 7))
        if score < min_s:
            continue
        results.append(simulate_trade(setup, score, df, config))
    return results
```

### C — load_data.py : validation source

```python
def validate_source_level(df):
    """Bloque si source=smoke_yfinance pour verdict."""
    if "source" not in df.columns:
        return  # contrat smoke antérieur — passe sans validation
    if (df["source"] == "smoke_yfinance").any():
        raise ValueError(
            "Source smoke_yfinance détectée. "
            "Utiliser une source Niveau 1 (broker export / prod collector) "
            "pour produire un verdict stratégique."
        )
```

### D — simulator.py : spread depuis feed

```python
# Lecture du spread par bar si disponible
spread_pts = row.get("spread", config_spread_fallback)
```

### E — report.py : metadata source dans verdict

```python
# Ajouter au verdict markdown
source_level = "SMOKE" if df["source"].eq("smoke_yfinance").any() else "CANONICAL"
regime_coverage = _compute_regime_coverage(df)
```

## Paramètres config.yaml à ajouter

```yaml
# À ajouter dans config.yaml
detectors:
  choch_confirm_window: 5      # bars après sweep pour confirmer CHOCH

scoring:
  min_score_by_variant:
    ORB_ONLY: 4
    VWAP_PULLBACK_ONLY: 3
    SMC_SWEEP_ONLY: 6
    COMBINED_SMC_ORB_VWAP: 7

data:
  source_level_required: canonical  # canonical | smoke (smoke = CI/test seulement)
  min_window_days: 180
  spread_fallback_pts: 3.0

verdict:
  promotion_requires:
    source_level: canonical
    min_window_days: 180
    min_trades_per_variant: 100
    min_regimes: 3
```

## Critères de verdict valide (post-rework)

```
source_level = canonical
ET fenêtre >= 180 jours
ET SMC_SWEEP_ONLY trades >= 100
ET COMBINED trades >= 100
ET regime_coverage >= 3 (trend / range / high-vol)
→ verdict stratégique autorisé
```

Si l'un de ces critères manque → `NEED_DATA_UPGRADE` dans le verdict markdown, pas de promotion.

## Séquence d'exécution recommandée post-rework

```bash
# 1. Obtenir les données canoniques (ex: MT5 export)
# Placer dans data/market/xauusd_m5_canonical.csv

# 2. Fetch derivatives (si disponible)
python tools/derivatives_collector/export_csv.py \
  --symbol XAUUSD --out data/derivatives/xauusd_deriv.csv

# 3. Run backtest canonique
python tools/strategy/daily_scalping/run_backtest.py \
  --input data/market/xauusd_m5_canonical.csv \
  --context-input data/market/xauusd_m15_canonical.csv \
  --derivatives data/derivatives/xauusd_deriv.csv \
  --out artifacts/backtests/daily_scalping_canonical \
  --source-level canonical

# 4. Lire verdict
cat artifacts/backtests/daily_scalping_canonical/xauusd_m5_verdict.md
```
