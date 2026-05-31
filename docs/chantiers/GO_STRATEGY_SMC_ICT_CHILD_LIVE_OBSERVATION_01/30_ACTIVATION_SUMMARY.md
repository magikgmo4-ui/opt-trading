---
doc_id: GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01_ACTIVATION_SUMMARY
doc_type: activation_summary
go_id: GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01
strategy_id: SMC_ICT_CHOCH_BOS_RETEST
strategy_version: 0.1.0
target_lifecycle: ACTIVE_PAPER
created_at: 2026-05-30
---

# 30_ACTIVATION_SUMMARY

Résumé d'activation préparé par l'opérateur après lecture des specs
(docs 10, 50, 60 du GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01).

---

## 1_STRATÉGIE_ACTIVÉE

```
strategy_id      : SMC_ICT_CHOCH_BOS_RETEST
strategy_version : 0.1.0
lifecycle        : CANDIDATE → ACTIVE_PAPER
mode             : paper_only / dry_run
symbol           : BTCUSDT
timeframe        : 15m (context : 1h, 4h)
window           : 14 jours à partir du 2026-05-30
```

---

## 2_SIGNAUX_À_SURVEILLER

Selon `10_STRATEGY_SPEC` + `20_SMC_ICT_RULES_CHOCH_BOS_MSS` :

### Trigger principal (15m)
1. **Sweep de liquidité** — BSL, SSL, EQH, EQL, PDH/PDL sweep identifié
2. **CHoCH confirmé** — chandelle de clôture franchissant le dernier swing point (renversement)
3. **OU BOS confirmé** — break de structure dans la direction du contexte HTF

### Filtre contexte (1h / 4h)
- Identifier tendance dominante (bullish / bearish / ranging)
- Identifier zones premium / discount (50% du dernier swing majeur)
- Alignement 1h requis pour score > 0.50

### Zone d'entrée observation (15m)
- FVG bullish / bearish créé lors du mouvement ayant produit le CHoCH/BOS
- OU Order Block (dernière bougie directionnelle avant le CHoCH/BOS)
- Retest dans la zone OTE (62-79% Fibonacci du leg)
- Confluence FVG + OB = score optimal

### Invalidation (obligatoire)
- Clôture au-delà du swing ayant généré le CHoCH/BOS → setup invalide
- Si absent → ObservationEvent non enregistré

---

## 3_OBSERVATION_EVENTS_À_POSTER

Format `ObservationEvent` défini dans `50_OBSERVATION_EVENT_MAPPING.md` :

```json
{
  "run_id": "<run_id>",
  "strategy": {
    "strategy_id": "SMC_ICT_CHOCH_BOS_RETEST",
    "strategy_version": "0.1.0",
    "lifecycle_status": "ACTIVE_PAPER"
  },
  "signal": {
    "direction": "LONG_WATCH | SHORT_WATCH | WATCH_ONLY",
    "symbol": "BTCUSDT",
    "timeframe": "15m",
    "context_timeframes": ["1h", "4h"],
    "signal_source": "bot_vision",
    "confidence": 0.0
  },
  "trade_plan": {
    "entry_zone": { "kind": "fvg_ob_confluence", "fvg_lower": null, "fvg_upper": null },
    "invalidation": { "rule": "close_through_swing_that_generated_choch_bos", "level": null },
    "target_zone": { "kind": "prior_liquidity", "level": null },
    "risk_profile": "paper_only"
  },
  "smc_ict_detail": {
    "choch_observed": false,
    "bos_observed": false,
    "sweep_observed": false,
    "fvg_valid": false,
    "ob_valid": false,
    "premium_discount_filter": "EQ"
  },
  "gates": {
    "observation_status": "ACTIVE_PAPER",
    "perf_status": "UNMEASURED",
    "promotion_gate": "BLOCKED_INSUFFICIENT_SAMPLE",
    "retirement_gate": "KEEP_OBSERVING"
  }
}
```

**Règles de posting :**
- `choch_observed` OU `bos_observed` = True obligatoire
- `invalidation` obligatoire (sinon INVALID, ne pas poster)
- `confidence` calculée via scoring `60_SCORING_INITIAL.md`
- Ne poster que si `confidence >= 0.35` (en dessous = bruit, loguer mais ne pas envoyer Telegram)

---

## 4_SCORING_RAPIDE (rappel formule)

| Bloc | Max | Exemples |
|------|-----|---------|
| Structure (CHoCH/BOS/MSS/HTF) | 0.50 | CHoCH+MSS+1h+4h |
| Liquidité / Sweep | 0.28 | PDH sweep + HTF + retour rapide |
| FVG/OB/Premium-Discount | 0.50 | FVG+OB+confluence+OTE+PD |

Seuils :
- `≥ 0.60` → éligible Telegram watch signal
- `≥ 0.70` → Trading Lab replay prioritaire
- `< 0.40` → loguer, ne pas envoyer Telegram

---

## 5_SEUILS_PROMOTION_ACTIVE_LIVE

Définis dans `10_STRATEGY_SPEC.md` section `promotion_gate` :

```
min_sample_size        : 30 ObservationEvents ACTIVE_PAPER
min_observation_days   : 14
kill_switch_tested     : oui (déjà fait)
telegram_dry_run_tested : oui (déjà fait)
no_closeout_required   : oui
perf_engine_evidence   : requis
```

Durée minimale de la fenêtre paper : **14 jours** (2026-05-30 → 2026-06-13).

---

## 6_SEULE_MUTATION_AUTORISÉE

```
95_STRATEGY_REGISTRY.md
  SMC_ICT_CHOCH_BOS_RETEST : observation_status CANDIDATE → ACTIVE_PAPER
```

Aucune autre modification de code, module, workflow, ou secret.
