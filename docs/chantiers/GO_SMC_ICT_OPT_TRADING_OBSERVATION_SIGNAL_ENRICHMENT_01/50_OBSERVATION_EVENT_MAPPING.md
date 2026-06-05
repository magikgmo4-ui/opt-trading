---
go_id: GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: observation_event_mapping
strategy_id: SMC_ICT_CHOCH_BOS_RETEST
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-17
---

# 50_OBSERVATION_EVENT_MAPPING

## Mapping ObservationEvent pour SMC_ICT_CHOCH_BOS_RETEST

---

## 1_OBJECTIF

Definir comment les regles SMC/ICT (docs 20, 30, 40) s'inscrivent dans la
structure `ObservationEvent` definie par le PR #524 et etendue par le parent
`GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01`.

---

## 2_STRUCTURE_BASELINE_PR_524

Champs existants conserves :

```json
{
  "run_id": "20260517_001",
  "session_id": "daily_session_001",
  "run_date": "2026-05-17",
  "started_at": "2026-05-17T08:00:00Z",
  "status": "PASS",
  "dry_run": true,
  "paper_mode": true,
  "outcome": null,
  "pnl_net": 0.0,
  "localcms_ok": true,
  "closeout_required": false,
  "ingested_at": "2026-05-17T08:05:00Z",
  "source_file": "data/journal/daily/20260517_001.json"
}
```

---

## 3_EXTENSION_SMC_ICT

Extension specifique `SMC_ICT_CHOCH_BOS_RETEST` :

```json
{
  "strategy": {
    "strategy_id": "SMC_ICT_CHOCH_BOS_RETEST",
    "strategy_version": "0.1.0",
    "setup_type": "SWEEP_CHOCH_BOS_FVG_OB_RETEST",
    "lifecycle_status": "CANDIDATE"
  },
  "signal": {
    "direction": "WATCH_ONLY",
    "symbol": "BTCUSDT",
    "timeframe": "15m",
    "context_timeframes": ["1h", "4h"],
    "signal_source": "bot_vision",
    "confidence": 0.62
  },
  "trade_plan": {
    "entry_zone": {
      "kind": "fvg_ob_confluence",
      "description": "FVG ou OB retest apres CHoCH bullish",
      "fvg_upper": null,
      "fvg_lower": null,
      "ob_upper": null,
      "ob_lower": null
    },
    "invalidation": {
      "rule": "close_through_swing_that_generated_choch",
      "level": null
    },
    "target_zone": {
      "kind": "prior_liquidity",
      "description": "BSL au-dessus du CHoCH",
      "level": null
    },
    "risk_profile": "paper_only"
  },
  "evidence": [
    {
      "type": "vision_summary",
      "path": "data/desk_pro/vision/latest/summary.json"
    },
    {
      "type": "vision_analysis",
      "path": "data/desk_pro/vision/latest/analysis.md"
    }
  ],
  "smc_ict_detail": {
    "choch_observed": true,
    "bos_observed": false,
    "mss_observed": false,
    "sweep_observed": true,
    "sweep_type": "BSL_sweep",
    "sweep_form": "wick",
    "fvg_valid": true,
    "ob_valid": true,
    "fvg_ob_confluence": true,
    "premium_discount_filter": "DISCOUNT",
    "ote_zone_active": true,
    "htf_alignment": "1h_bearish_context",
    "htf_alignment_confirmed": false
  },
  "gates": {
    "observation_status": "CANDIDATE",
    "perf_status": "UNMEASURED",
    "promotion_gate": "BLOCKED_INSUFFICIENT_SAMPLE",
    "retirement_gate": "KEEP_OBSERVING"
  }
}
```

---

## 4_CHAMP_PAR_CHAMP

### 4.1_strategy

| Champ | Type | Nullable | Description |
| --- | --- | --- | --- |
| `strategy_id` | string | Non | `SMC_ICT_CHOCH_BOS_RETEST` |
| `strategy_version` | string | Non | `0.1.0` |
| `setup_type` | string | Non | `SWEEP_CHOCH_BOS_FVG_OB_RETEST` |
| `lifecycle_status` | enum | Non | `CANDIDATE` initial |

### 4.2_signal

| Champ | Type | Nullable | Description |
| --- | --- | --- | --- |
| `direction` | enum | Non | `WATCH_ONLY`, `LONG_WATCH`, `SHORT_WATCH` |
| `symbol` | string | Non | Paire observee |
| `timeframe` | string | Non | `15m` |
| `context_timeframes` | array | Oui | `["1h", "4h"]` |
| `signal_source` | string | Non | `bot_vision`, `tradingview`, `manual` |
| `confidence` | float | Non | 0.0 a 1.0 |

### 4.3_trade_plan

| Champ | Type | Nullable | Description |
| --- | --- | --- | --- |
| `entry_zone` | object | Oui | FVG/OB zone; null si non identifiee |
| `invalidation` | object | Non | Obligatoire; sinon observation invalide |
| `target_zone` | object | Oui | Pool de liquidite cible |
| `risk_profile` | string | Non | `paper_only` pour v0.1.0 |

### 4.4_smc_ict_detail

Extension propre a `SMC_ICT_CHOCH_BOS_RETEST` :

| Champ | Type | Nullable | Description |
| --- | --- | --- | --- |
| `choch_observed` | bool | Non | CHoCH detecte |
| `bos_observed` | bool | Non | BOS detecte |
| `mss_observed` | bool | Oui | MSS confirme post-CHoCH |
| `sweep_observed` | bool | Oui | Sweep de liquidite observe |
| `sweep_type` | string | Oui | `BSL_sweep`, `SSL_sweep`, `EQH_sweep`, etc. |
| `sweep_form` | string | Oui | `wick`, `body`, `fast_move` |
| `fvg_valid` | bool | Oui | FVG identifie et valide |
| `ob_valid` | bool | Oui | OB identifie et valide |
| `fvg_ob_confluence` | bool | Oui | Confluence presente |
| `premium_discount_filter` | string | Oui | `PREMIUM`, `DISCOUNT`, `EQ` |
| `ote_zone_active` | bool | Oui | Retest dans zone OTE (62-79%) |
| `htf_alignment` | string | Oui | Contexte `1h`/`4h` decrit |
| `htf_alignment_confirmed` | bool | Oui | Alignement confirme |

### 4.5_gates

| Champ | Type | Nullable | Description |
| --- | --- | --- | --- |
| `observation_status` | enum | Non | `CANDIDATE` initial |
| `perf_status` | enum | Non | `UNMEASURED` initial |
| `promotion_gate` | string | Non | Verdict Perf Engine |
| `retirement_gate` | string | Non | Verdict retirement |

---

## 5_REGLES_DE_MAPPING

| Regle | Application |
| --- | --- |
| `invalidation` obligatoire | Si absent -> observation INVALID, ne pas enregistrer |
| `strategy_id` obligatoire | Si absent -> observation non liee a strategie |
| `choch_observed` ou `bos_observed` obligatoire | Au moins un des deux = True |
| `confidence` obligatoire | Calculee via scoring (doc 60) |
| `risk_profile = paper_only` | Fixe en v0.1.0; pas de live |
| `observation_status = CANDIDATE` | Toujours au debut, jamais promouvoir automatiquement |

---

## 6_COMPATIBILITE_BACKWARD

Les anciens `ObservationEvent` sans les champs `strategy`, `smc_ict_detail`
et `gates` restent valides.

Comportement :

```text
Anciens events -> strategy = null, smc_ict_detail = null, gates.observation_status = "UNCLASSIFIED"
Nouveaux events -> champs complets requis
```

Pas de backfill obligatoire.

---

## 7_NO_PARALLEL_PIPELINE

Source canonique unique :

```text
ObservationEvent -> journal daily -> LocalCMS / Telegram / Perf Engine / Trading Lab
```

Interdit :

```text
strategy_events.jsonl separe
smc_ict_events.jsonl separe
telegram_smc_signal sans ObservationEvent
perf_smc_score sans ObservationEvent evidence
```

## RISKS

- À qualifier.
