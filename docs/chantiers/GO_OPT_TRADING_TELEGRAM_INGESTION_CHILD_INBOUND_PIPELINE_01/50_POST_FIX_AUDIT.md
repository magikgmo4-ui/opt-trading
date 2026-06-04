# 50_POST_FIX_AUDIT.md

## GO: GO_OPT_TRADING_ANALYSIS_BUNDLES
## Branch: sot/mainline
## Date: 2026-06-04 04:55Z
## Commits: 9c12f116 + dcc2be39

---

## 1. AUDIT SUMMARY — PR #1090 vs Post-Fix

### Before/After Table

| Asset | Field | PR #1090 (3581d833) | Post-Fix (dcc2be39) |
|---|---|---|---|
| BTC | bias | ~~BULLISH~~ | **BEARISH** |
| BTC | confidence | ~~MEDIUM~~ | **LOW** |
| GOLD | bias | ~~BULLISH~~ | **BEARISH** |
| GASOLINE | bias | ~~BULLISH~~ | **BEARISH** |
| MACRO | regime | ~~RISK_ON~~ | **RISK_OFF** (pipeline) |
| ENERGY | regime | ~~BULLISH~~ | **NEUTRAL** |
| COINGLASS | freshness | ~~FRESH~~ | **STALE** (stub detected) |
| VERDICT | bias | ~~ALIGNED BULLISH~~ | **UNKNOWN** |
| VERDICT | score | ~~95/100~~ | **25/100** |

### Current Verdict (runtime)

```json
{
  "freshness_state": "STALE",
  "composite": {
    "btc_bias": "BEARISH",
    "macro_regime": "UNKNOWN",
    "alignment": "UNKNOWN",
    "overall_bias": "UNKNOWN",
    "confidence": "UNKNOWN",
    "score": 25
  },
  "warnings": [
    "BTC bundle stale — analysis may be unreliable",
    "Macro bundle stale — analysis may be unreliable"
  ],
  "missing_inputs": [
    "vision_analysis: stale (>6h old), confidence degraded",
    "market_metrics: data file not found",
    "telegram_signals: no BTC signals found",
    "ALL: no macro data available"
  ]
}
```

### Current Pipeline Report (informational, non-trading)

```json
{
  "regimes": {
    "macro": "RISK_OFF",
    "crypto": "BEARISH",
    "energy": "NEUTRAL"
  },
  "alerts": 0,
  "actionable_signals": 10
}
```

---

## 2. DECISION GATE

```
TRADABLE: NO

GATE CHECKS:
  [BLOCK] confidence = UNKNOWN (macro regime not determined)
  [BLOCK] freshness  = STALE   (all analyses >6h old + market_metrics missing)
  [BLOCK] BTC bundle stale     (vision stale + coinglass stub)
  [BLOCK] Macro bundle stale   (all 14 symbols >6h old)
  [BLOCK] market_metrics MISSING
  [BLOCK] telegram_signals MISSING

PASS CHECKS:
  [OK] 132 tests pass
  [OK] No false bullish from keyword bugs
  [OK] No false FRESH from coinglass stub
  [OK] No false FRESH from aged vision analysis
  [OK] BTC BEARISH (summary = "baissière", plan = unknown → correct)
  [OK] GOLD BEARISH (plan = "short", overrides keyword)
  [OK] GASOLINE BEARISH (plan = "vendre", overrides keyword)
```

**Divergence pipeline/verdict:** Le pipeline report dit `macro=RISK_OFF` (analyse informationnelle, utilise tous les tickets sans filtrer par freshness). Le verdict dit `macro=UNKNOWN` (analyse stricte, n'utilise que les tickets FRESH). Le verdict est plus conservateur et c'est voulu.

---

## 3. REMAINING GAP

| Gap | Impact | Fix |
|---|---|---|
| market_metrics MISSING | BTC bundle ne peut pas etre FRESH | Activer market_metrics_writer sur admin-trading |
| telegram_screener MISSING | Zero signaux Telegram en entree | Appliquer pipeline screener sur les 174 raw messages |
| Coinglass OCR = stub | Detection fiable mais valeurs arbitraires | Activer `requested_real_ocr=true` |
| All vision analyses >6h | Freshness degradee partout | Sync admin-trading plus frequent ou accepter le mode degrade |
| Verdict vs pipeline divergence | Macro regime differe selon le mode | Documente — pas un bug, deux modes differents |

---

## 4. NEXT GO CANDIDATE

**`GO_OPT_TRADING_MARKET_METRICS_FRESH_ENABLE`** — Activer market_metrics_writer sur admin-trading pour que:

1. `data/data_center/views/market_metrics/latest.json` existe
2. BTC bundle passe `FRESH` (vision + market_metrics)
3. Le verdict macro passe de `UNKNOWN` a `RISK_OFF` (ou `RISK_ON` selon le marche)
4. Le score remonte au-dessus de 50 quand les conditions sont reunies
5. Le decision gate puisse passer `TRADABLE` quand les 4 inputs sont FRESH

---

## 5. VERIFICATION

```bash
# State
git log -3 --oneline --decorate
# dcc2be39 fix(btc-core): use vision analysis bias even when stale, degrade confidence
# 9c12f116 fix(analysis-bundles): correct bias extraction, stub detection, age degradation
# 4192f19a Merge pull request #1090

# Tests
python3 -m pytest tests/test_bundle_contracts.py tests/test_verdict_consumer.py tests/test_asset_selector.py tests/test_telegram_ingestion_consumer_router.py -q
# 132 passed

# Sanity
bash modules/analysis_bundles/scripts/sanity_check.sh
# PASS
```
