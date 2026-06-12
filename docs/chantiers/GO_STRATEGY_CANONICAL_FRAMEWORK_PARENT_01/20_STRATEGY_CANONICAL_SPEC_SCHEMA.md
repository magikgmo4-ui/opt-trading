---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
child_go: GO_STRATEGY_CANONICAL_SPEC_SCHEMA_01
doc_type: canonical_strategy_spec_schema
repo: opt-trading
status: open
created_at: 2026-05-17
surface: doc-only
---

# 20_STRATEGY_CANONICAL_SPEC_SCHEMA

---

## 1_OBJECTIF

Definir le schema minimal d'une strategie canonique.

Une strategie canonique est une specification stable qui permet :

- identification par `strategy_id`;
- versioning par `strategy_version`;
- normalisation du signal;
- enrichissement de `ObservationEvent`;
- evaluation Perf Engine;
- affichage LocalCMS;
- watch Telegram;
- replay Trading Lab;
- retrait ou promotion par gate.

---

## 2_SCHEMA_MINIMUM

| Champ | Type | Requis | Description |
| --- | --- | --- | --- |
| `strategy_id` | string | Oui | Identifiant stable, uppercase snake case, non vide. |
| `strategy_version` | string | Oui | Version semantique ou datee, ex. `v0.1.0`. |
| `setup_type` | string | Oui | Famille de setup detectee. |
| `direction` | enum | Oui | `LONG`, `SHORT`, `NEUTRAL`, `WATCH_ONLY`. |
| `symbol` | string | Oui | Actif observe. |
| `timeframe` | string | Oui | Timeframe source ou principal. |
| `signal_source` | enum/string | Oui | `tradingview`, `webhook`, `bot_vision`, `market_data`, `manual`, etc. |
| `evidence_source` | array | Oui | Sources d'evidence: screenshot, webhook payload, market data, journal, human note. |
| `confidence` | number | Oui | Score 0.0 a 1.0; non suffisant seul pour promouvoir. |
| `entry_zone` | object/string | Oui | Zone d'entree theorique ou watch zone. |
| `invalidation` | object/string | Oui | Condition d'invalidation explicite. |
| `target_zone` | object/string | Oui | Objectif theorique ou zone de reaction. |
| `risk_profile` | object/string | Oui | Risque attendu, sizing theorique, constraints. |
| `observation_status` | enum | Oui | `CANDIDATE`, `OBSERVED`, `REJECTED`, `RETIRED`. |
| `perf_status` | enum | Oui | `UNMEASURED`, `MEASURING`, `PASS`, `FAIL`, `INSUFFICIENT_SAMPLE`. |
| `promotion_gate` | object | Oui | Conditions a satisfaire pour promotion. |
| `retirement_gate` | object | Oui | Conditions de retrait ou pause. |

---

## 3_SCHEMA_EXEMPLE

```json
{
  "strategy_id": "SMC_ICT_CHOCH_BOS_RETEST",
  "strategy_version": "v0.1.0",
  "setup_type": "SWEEP_CHOCH_BOS_FVG_OB_RETEST",
  "direction": "WATCH_ONLY",
  "symbol": "BTCUSDT",
  "timeframe": "15m",
  "signal_source": "bot_vision",
  "evidence_source": [
    {
      "type": "screenshot",
      "path": "data/desk_pro/vision/latest/summary.json"
    },
    {
      "type": "journal",
      "path": "data/journal/daily/20260517_001.json"
    }
  ],
  "confidence": 0.62,
  "entry_zone": {
    "kind": "range",
    "lower": null,
    "upper": null,
    "unit": "price"
  },
  "invalidation": {
    "rule": "close_through_structure_invalidates_setup"
  },
  "target_zone": {
    "rule": "prior_liquidity_or_opposing_fvg"
  },
  "risk_profile": {
    "mode": "paper_only",
    "max_risk_pct": 0.0
  },
  "observation_status": "CANDIDATE",
  "perf_status": "UNMEASURED",
  "promotion_gate": {
    "requires_observation_event": true,
    "requires_perf_engine_evidence": true,
    "min_sample_size": 30,
    "min_days": 14
  },
  "retirement_gate": {
    "max_consecutive_failures": 5,
    "manual_review_required": true
  }
}
```

---

## 4_STRATEGY_ID_RULES

`strategy_id` est :

- stable entre runs;
- lisible humainement;
- non derive d'un symbole;
- non derive d'un timeframe;
- non reutilise pour une logique differente;
- obligatoire avant toute emission Telegram strategie;
- obligatoire avant toute insertion dans `ObservationEvent`.

Format recommande :

```text
<FAMILY>_<CORE_SIGNAL>_<CONFIRMATION>
```

Exemples :

| Strategie | `strategy_id` |
| --- | --- |
| SMC/ICT sweep + CHOCH/BOS + retest | `SMC_ICT_CHOCH_BOS_RETEST` |
| Trend following MA + pullback | `TREND_MA_PULLBACK` |
| Mean reversion VWAP | `MEAN_REVERSION_VWAP_RECLAIM` |
| Breakout range | `BREAKOUT_RANGE_EXPANSION` |
| AI vision only candidate | `AI_VISION_STRUCTURE_WATCH` |

---

## 5_VERSIONING

`strategy_version` change si :

- les regles de detection changent;
- le seuil de confidence change;
- le mapping `ObservationEvent` change;
- les gates changent;
- la source principale d'evidence change.

`strategy_version` ne change pas pour :

- nouveau symbole;
- nouveau run;
- nouveau screenshot;
- correction documentaire sans effet sur la logique.

---

## 6_VALIDATION_RULES

Un spec est valide si :

```text
strategy_id is not empty
strategy_version is not empty
setup_type is not empty
direction in LONG/SHORT/NEUTRAL/WATCH_ONLY
confidence between 0.0 and 1.0
invalidation exists
promotion_gate.requires_perf_engine_evidence = true
observation_status starts as CANDIDATE
```

Un spec est refuse si :

```text
strategy_id missing
strategy_id duplicated with incompatible meaning
Vision-only decision
Telegram BUY/SELL direct before validation
live execution intent
Bitget order path
automatic Sheets write requirement
```

---

## 7_OUTPUT_CONTRACT

Le spec ne declenche pas d'action. Il produit un objet d'enrichissement pour :

```text
ObservationEvent.strategy.*
ObservationEvent.signal.*
ObservationEvent.evidence.*
ObservationEvent.gates.*
```

La decision d'action reste hors scope de ce parent.

## RISKS

- À qualifier.
