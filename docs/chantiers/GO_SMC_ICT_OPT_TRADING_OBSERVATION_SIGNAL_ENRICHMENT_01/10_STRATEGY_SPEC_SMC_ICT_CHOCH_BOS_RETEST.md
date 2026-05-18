---
go_id: GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: strategy_spec_instance
strategy_id: SMC_ICT_CHOCH_BOS_RETEST
strategy_version: "0.1.0"
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-17
---

# 10_STRATEGY_SPEC_SMC_ICT_CHOCH_BOS_RETEST

---

## 1_IDENTITE

| Champ | Valeur |
| --- | --- |
| `strategy_id` | `SMC_ICT_CHOCH_BOS_RETEST` |
| `strategy_version` | `0.1.0` |
| `setup_type` | `SWEEP_CHOCH_BOS_FVG_OB_RETEST` |
| `family` | `SMC_ICT` |

---

## 2_DESCRIPTION

La strategie `SMC_ICT_CHOCH_BOS_RETEST` detecte un changement de structure du
marche (CHoCH ou BOS) apres un sweep de liquidite, puis attend un retest de la
zone d'origine (FVG ou Order Block) pour confirmer un signal d'observation.

Elle ne produit pas d'ordre. Elle produit une observation enrichie.

---

## 3_SPEC_JSON

```json
{
  "strategy_id": "SMC_ICT_CHOCH_BOS_RETEST",
  "strategy_version": "0.1.0",
  "setup_type": "SWEEP_CHOCH_BOS_FVG_OB_RETEST",
  "direction": "WATCH_ONLY",
  "symbol": "BTCUSDT",
  "timeframe": "15m",
  "context_timeframes": ["1h", "4h"],
  "signal_source": "bot_vision",
  "evidence_source": [
    { "type": "vision_summary", "path": "data/desk_pro/vision/latest/summary.json" },
    { "type": "vision_analysis", "path": "data/desk_pro/vision/latest/analysis.md" },
    { "type": "journal", "path": "data/journal/daily/<run_id>.json" }
  ],
  "confidence": null,
  "entry_zone": {
    "kind": "range",
    "description": "FVG or OB retest zone after CHoCH/BOS",
    "lower": null,
    "upper": null,
    "unit": "price"
  },
  "invalidation": {
    "rule": "close_through_swing_that_generated_choch_bos",
    "description": "Si le prix cloture au-dela du swing ayant genere le CHoCH/BOS, le setup est invalide."
  },
  "target_zone": {
    "kind": "prior_liquidity",
    "description": "Liquidity pool anterieure ou FVG opposee au-dessus (LONG) ou en-dessous (SHORT)."
  },
  "risk_profile": {
    "mode": "paper_only",
    "max_risk_pct": 0.0,
    "sizing": "not_applicable"
  },
  "observation_status": "CANDIDATE",
  "perf_status": "UNMEASURED",
  "promotion_gate": {
    "requires_observation_event": true,
    "requires_perf_engine_evidence": true,
    "min_sample_size": 30,
    "min_observation_days": 14,
    "kill_switch_tested": true,
    "telegram_dry_run_tested": true,
    "no_closeout_required": true
  },
  "retirement_gate": {
    "max_consecutive_failures": 5,
    "vision_only_decision": "REJECTED",
    "manual_review_required": true
  }
}
```

---

## 4_SPEC_NARRATIVE

La strategie se construit en trois phases :

**Phase 1 — Contexte.**
Sur `1h` ou `4h`, identifier la tendance dominante et les pools de liquidite
cles (Equal Highs/Lows, BSL/SSL). Identifier la zone premium/discount globale.

**Phase 2 — Trigger.**
Sur `15m`, observer un sweep de liquidite suivi d'un CHoCH ou BOS confirme.
Un CHoCH signifie un changement de structure (renversement potentiel).
Un BOS signifie un break de structure dans la direction de la tendance.

**Phase 3 — Entree / Observation.**
Attendre le retest de la zone FVG ou OB creer lors du mouvement ayant produit
le CHoCH/BOS. La confluence avec premium/discount zone filtre les faux signaux.

---

## 5_DIRECTION_MATRIX

| Contexte `1h/4h` | Sweep | CHoCH/BOS `15m` | Direction signal |
| --- | --- | --- | --- |
| Bearish | BSL sweep | CHoCH bullish | LONG watch |
| Bullish | SSL sweep | CHoCH bearish | SHORT watch |
| Bullish | SSL sweep | BOS bearish | SHORT continuation watch |
| Bearish | BSL sweep | BOS bullish | LONG continuation watch |
| Ranging | Equal Highs/Lows | CHoCH ou BOS | WATCH_ONLY (inconclus) |

---

## 6_VERSIONING

`strategy_version` passe a `0.2.0` si :

- les regles de detection changent (ex. timeframe minimum pour CHoCH modifie);
- le seuil de confidence change;
- le mapping `ObservationEvent` change structurellement;
- les gates de promotion changent;
- la source principale d'evidence change.

`strategy_version` ne change pas pour :

- nouveau run ou symbol;
- correction documentaire;
- nouveau screenshot.

---

## 7_REFUSAL_CRITERIA

Ce spec est invalide et doit etre bloque si :

```text
strategy_id absent
invalidation absente
direction = BUY ou SELL direct (avant perf_status = PASS)
evidence = vision_only sans invalidation testable
live trade intent
Bitget order path
automatic Sheets write
```
