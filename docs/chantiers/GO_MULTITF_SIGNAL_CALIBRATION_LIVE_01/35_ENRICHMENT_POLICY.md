# 35_ENRICHMENT_POLICY — Architecture d'enrichissement du scorer

## Pipeline 3-phases

```
Data Center sources
        ↓
multitf_analysis_input.v1
        ↓
PHASE 1 — Core setup detection (triggers only)
        ↓
PHASE 2 — Context enrichment (macro, volume, orderflow, backtest, true_value)
        ↓
PHASE 3 — Caps and downgrades (stale, missing, contradiction)
        ↓
final setup verdict
        ↓
Voice / DeskPro / Priorités
```

## Règles cardinales

1. **Core trigger required for grade ≥ B.** Sans CDP vwap_loss/reclaim/ORB/sweep/BOS, le grade max est C+.
2. **Enrichment cannot create a setup.** Il peut booster B→B+ ou C→C+, mais pas C→B sans trigger.
3. **Enrichment can raise or lower within caps.** Macro alignment, volume confirmation, backtest edge ajustent le score dans les limites des caps.
4. **Stale core trigger always downgrades.** Freshness non-fresh → -5 à -15 pts.
5. **Missing enrichment does not reject a setup.** L'absence de backtest ou de true_value n'invalide pas un setup avec trigger.
6. **Missing core evidence caps at C.** Sans price ou H4 trend, un setup directionnel ne peut pas dépasser C.

## Rôle des données

| Bloc | Rôle | Crée setup ? | Booste ? | Downgrade ? |
|---|---|---|---|---|
| Multi-TF OHLCV | verdict | oui | oui | oui |
| VWAP / ORB / levels | verdict | oui | oui | oui |
| CDP signal_event | trigger | oui | oui | oui |
| Volume / RVOL | confirmation | non seul | oui | oui |
| Orderflow / OI / funding | confirmation | non seul | oui | oui |
| Macro DXY/VIX/SPY | contexte | non | oui | oui |
| Backtest edge | calibration | non | oui | non |
| True value (SPCX) | contexte | non | oui | non |
| Source quality/freshness | garde-fou | non | oui | oui |
| Risk context | filtre | non | non | oui |

## Implémentation dans le scorer

```python
# Phase 1 — _detect_core_setups()
# Détecte: vwap_rejection, vwap_reclaim, orb_break_long, orb_break_short,
#          liquidity_sweep, structure_break, support_watch (fallback)
# Populate: core_evidence[]

# Phase 2 — _apply_enrichment()
# Lit: macro_context, orderflow, timeframes, source_quality, backtest, true_value
# Ajuste: score_breakdown (8 dimensions)
# Populate: enrichment_evidence[]

# Phase 3 — _apply_caps_and_downgrades()
# Vérifie: CDP trigger présent, freshness, contradiction HTF/LTF, critical missing
# Applique: caps (C+ sans trigger, B max contradiction, B max critical missing)
# Populate: downgrade_reasons[]
```

## Structure de sortie d'un setup

```json
{
  "setup_id": "btc_vwap_reject_m15",
  "setup_type": "vwap_rejection",
  "grade": "B+",
  "score": 68,
  "core_evidence": ["CDP vwap_loss @ 66700", "H4 bearish aligned"],
  "enrichment_evidence": ["H4 bearish aligned with short setup", "CDP trigger: vwap_loss"],
  "downgrade_reasons": [],
  "entry_zone": [66856, 67057],
  "invalidation": 68000,
  "targets": [65000],
  "risk_reward": 1.6,
  "probability_pct": 60,
  "confidence_pct": 70,
  "score_breakdown": {
    "htf_alignment": 14,
    "ltf_trigger": 15,
    "vwap_level_quality": 8,
    "volume_orderflow": 8,
    "macro_alignment": 5,
    "freshness_source": 8,
    "risk_reward": 6,
    "backtest_edge": 4
  },
  "missing": ["W1", "D1", "M5"]
}
```
