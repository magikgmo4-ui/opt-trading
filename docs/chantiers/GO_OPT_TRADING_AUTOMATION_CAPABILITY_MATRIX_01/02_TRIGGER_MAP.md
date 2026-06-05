---
doc_id: GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01_TRIGGER_MAP
doc_type: trigger_map
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01
status: draft_for_review
lifecycle_stage: child_trigger_map
topic_keys:
  - opt-trading
  - automation
  - triggers
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01/02_TRIGGER_MAP.md
point_de_reprise: "Carte des déclencheurs par surface."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01/01_AUTOMATION_MATRIX.md
---

# 02_TRIGGER_MAP

## 1_PAR TYPE DE DÉCLENCHEUR

### TIMER
```text
- Desk Pro Automation → systemd timer (desk_pro_orchestrator)
- Bot Vision step2 → systemd timer (send, prune)
- DeepSeek Student → timer optional (daily-ai-report)
- PERF Telegram alerts → timer (no-activity, drawdown)
```

### WEBHOOK
```text
- TradingView Pipeline → webhook HTTP (alerte TV)
- PERF event ingestion → POST /perf/event
```

### WATCH LOOP
```text
- Bot Vision vision_bot → polling 2s (inbox)
```

### MANUAL / ON-DEMAND
```text
- OpenClaw Runtime → invocation opérateur
- DeepSeek Student → cmd-deepseek_*
- Collectors → cmd.sh / desk_pro pipeline
- Repo KG → cmd.sh
- Simex Bitget Bridge → cmd.sh
- Ops Menu Hub → menu.sh
```

### SUBPROCESS (via Desk Pro)
```text
- Collectors → appelés par desk_pro_orchestrator
- PERF Engine → appelé par desk_pro_orchestrator
```

## 2_SURFACES SANS TRIGGER AUTOMATIQUE

```text
- Collectors : pas de timer autonome confirmé
- Repo KG : régénération manuelle
- Simex Bitget Bridge : exécution supervisée
```

## 3_SURFACES AVEC DÉCLENCHEUR AUTOMATIQUE ACTIF

```text
- Desk Pro Automation : timer actif
- Bot Vision : watch + timers actifs
- TradingView Pipeline : webhook actif
- PERF : listener 8010 + Telegram timers
```

## RISKS

- À qualifier.
