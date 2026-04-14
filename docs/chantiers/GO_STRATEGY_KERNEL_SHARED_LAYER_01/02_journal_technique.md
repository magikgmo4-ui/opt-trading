---
doc_id: GO_STRATEGY_KERNEL_SHARED_LAYER_01_JOURNAL
doc_type: chantier_journal
repo: opt-trading
project: trading
module: strategy_kernel
go_id: GO_STRATEGY_KERNEL_SHARED_LAYER_01
status: active
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - trading
  - strategy_kernel
  - journal
surface: trading
source_kind: canonical
updated_at: 2026-04-14
links:
  - docs/chantiers/GO_STRATEGY_KERNEL_SHARED_LAYER_01/00_cadrage.md
  - docs/chantiers/GO_STRATEGY_KERNEL_SHARED_LAYER_01/01_plan.md
  - docs/ot/trading/23_STRATEGY_KERNEL_EXTENSIBILITY_AUDIT_01.md
---

# 02_journal_technique — GO_STRATEGY_KERNEL_SHARED_LAYER_01

## Journal factuel

### 2026-04-14 — base d'analyse retenue
- lecture repo-source de `modules/trading_lab_v1/app/trading_lab_v1.py`
- lecture repo-source de `modules/trading_realtime_v1/app/runtime_loop_v1.py`
- lecture repo-source de `modules/trading_realtime_v1/app/guardrails_v1.py`
- lecture du canon dual stack et des closings LAB / REALTIME associés

### 2026-04-14 — constats principaux
- le design canonique dual stack pousse déjà vers un noyau partagé LAB / REALTIME
- le code réel reste fortement câblé autour de `XAUUSD`, `xauusd_dual_stack_v1` et `xau_session_open_v1`
- le LAB contient déjà des briques utiles de `frame`, `feature extraction`, `variant resolution`, `event / trade projection`
- le REALTIME contient déjà des briques utiles de projection runtime, reporting et guardrails, mais encore câblées XAU et `observation_only`

### 2026-04-14 — qualification des changements
- changement local possible : rendre injectables certaines constantes et identifiants
- changement structurant requis : introduire une vraie couche stratégie partagée, avec séparation explicite entre features, variantes, signal, entrée et risque

### 2026-04-14 — suite retenue
- le prochain GO retenu pour la continuité documentaire est `GO_STRATEGY_KERNEL_SHARED_LAYER_01`
- le lot suivant attendu après cadrage est l'ouverture explicite d'une couche stratégie partagée LAB / REALTIME
