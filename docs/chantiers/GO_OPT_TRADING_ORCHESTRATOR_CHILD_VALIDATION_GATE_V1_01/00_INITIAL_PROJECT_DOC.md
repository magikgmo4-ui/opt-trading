---
doc_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
master_project_plan_id: MPP_OPENCLAW_ORCHESTRATOR_FULL
pf_id: PF_OPENCLAW_ORCHESTRATOR_FULL
status: closed
lifecycle_stage: opening
surface: modules/validation_gate
source_kind: canonical
updated_at: 2026-05-24
topic_keys:
  - openclaw
  - orchestration
  - validation-gate
  - telegram-approval
  - risk-gate
  - trade-safety
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/00_SYSTEM_MASTER_PLAN.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_FRESHNESS_AUDIT_01/00_FRESHNESS_AUDIT.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_MASTER_PLAN_ROADMAP_REFRESH_01/01_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_ORCHESTRATOR_CHILD_PROPOSITION_ENGINE_V1_01/01_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_ORCHESTRATOR_CHILD_NOTIFICATION_DISPATCHER_V1_01/00_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_ORCHESTRATOR_CHILD_SIGNAL_ROUTER_V1_01/00_CLOSEOUT.md
---

# 00_INITIAL_PROJECT_DOC — Validation Gate V1

## 1_MASTER_TARGET

Contribuer à `PF_OPENCLAW_ORCHESTRATOR_FULL` en ajoutant la surface `validation_gate`, nécessaire pour empêcher tout passage vers `trade_executor` sans validation explicite ou règle automatique bornée.

## 2_INITIAL_PROJECT_DOC

Cette fiche ouvre le child produit `GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01`.

Le GO est rattaché au parent OpenClaw :

```text
PARENT_GO = GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
MASTER_PROJECT_PLAN = MPP_OPENCLAW_ORCHESTRATOR_FULL
PF = PF_OPENCLAW_ORCHESTRATOR_FULL
GO_STRUCTURAL_ROLE = GO_CHILD_ATTACHED_TO_PARENT
```

## 3_INITIAL_NEED

Après les closeouts PASS de `signal_router`, `notification_dispatcher`, `proposition_engine` et `openclaw_operator_bridge`, la prochaine surface bloquante est `validation_gate`.

Sans validation gate :

```text
NO_LIVE_TRADE_WITHOUT_GATE = non garanti par module dédié
trade_executor = interdit à ouvrir comme exécuteur live
```

## 4_MASTER_PROJECT_PLAN

Chaîne produit visée :

```text
signal_router PASS
→ proposition_engine PASS
→ validation_gate V1
→ trade_executor
→ result_tracker
→ datasheet_writer
→ learning_feeder
```

## 5_GO_PLAN

```text
GO_ID: GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01
FINAL_TARGET: module validation_gate V1 spécifié/implémenté/testé
BUNDLE_TARGET: validation gate auto + Telegram approval flow + no-live-trade guard
```

## 6_FINAL_TARGET

Produire `modules/validation_gate/` avec :

- schémas d'entrée/sortie pour propositions ;
- validation automatique par règles bornées ;
- mode approbation opérateur via `notification_dispatcher` ;
- gestion `APPROVED`, `REJECTED`, `TIMEOUT`, `AUTO_APPROVED`, `AUTO_REJECTED` ;
- garde stricte `NO_LIVE_TRADE_WITHOUT_GATE` ;
- tests unitaires et smoke local ;
- documentation opérationnelle.

## 7_CANONICAL_STATE

Préconditions établies :

```text
OPENCLAW_OPERATOR_BRIDGE = PASS
SIGNAL_ROUTER = PASS
NOTIFICATION_DISPATCHER = PASS
PROPOSITION_ENGINE = PASS
TELEGRAM = OPÉRATIONNEL
```

État de départ :

```text
VALIDATION_GATE = NON OUVERT AVANT CE GO
TRADE_EXECUTOR = INTERDIT TANT QUE VALIDATION_GATE NON PASS
```

## 8_VALIDATED_PLAN

Étapes attendues :

1. Créer `modules/validation_gate/`.
2. Définir les schémas `GateRequest`, `GateDecision`, `GatePolicy`.
3. Ajouter moteur de règles bornées : max risk, kill switch, auto approve/reject selon policy.
4. Ajouter connecteur dry-run vers `notification_dispatcher` pour approval Telegram.
5. Ajouter CLI `cmd.sh` : sanity, validate, smoke, test.
6. Ajouter tests couvrant au moins : approve, reject, timeout, auto approve, auto reject, malformed request, kill switch.
7. Ajouter docs module.
8. Produire closeout avec gates PASS.

## 9_SELECTED_SOLUTION

Module local borné, sans exécution de trade, sans appel exchange, sans secret.

## 10_SELECTED_SETUP

```text
BRANCH = go/GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01
BASE_SHA = 831e2009b60877b77bd4f23a56c8e37618fc51c2
MODULE = modules/validation_gate/
DOCS = docs/chantiers/GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01/
BUNDLE_REQUIRED = true
PATCH_REQUIRED = true
ZIP_TRANSPORTABLE_REQUIRED = true
```

## 11_KEY_DECISIONS

- `validation_gate` ne doit jamais exécuter un trade.
- `validation_gate` produit uniquement une décision signée/loggable.
- `trade_executor` reste non ouvert et non autorisé dans ce GO.
- Les index globaux ne sont pas modifiés à l'ouverture de ce child.

## 12_INVARIANTS

```text
NO_LIVE_TRADE_WITHOUT_GATE = true
NO_TRADE_EXECUTION_IN_THIS_GO = true
NO_SECRET_IN_LOGS = true
NO_OPENCLAW_ORCHESTRATE = true
OPT_TRADING_ORCHESTRATES = true
NO_GLOBAL_INDEX_PATCH_WITHOUT_EXPLICIT_TRIGGER = true
```

## 13_ESTABLISHED

- Le master plan OpenClaw a été rafraîchi.
- Le prochain GO réel est `VALIDATION_GATE_V1_01`.
- Les prérequis directs sont PASS.

## 14_HYPOTHESIS

- Le mode `notification_dispatcher` peut rester dry-run au départ.
- Une policy YAML/JSON minimale suffit pour V1.
- Le gate peut être validé sans exchange ni live trade.

## 15_REMAINING_GAP

- Implémentation module absente.
- Bundle transportable à produire.
- Patch canonique à produire.
- Zip transportable à produire si exécution IDE/autre machine.
- Closeout à produire seulement après tests.

## 16_TODO

1. Implémenter module `modules/validation_gate/`.
2. Ajouter tests.
3. Ajouter docs module.
4. Produire bundle, `.patch` canonique et `.zip` transportable.
5. Ouvrir PR d'implémentation.
6. Fermer child seulement après preuves PASS.

## 17_RESUME_POINT

```text
Reprendre sur branche:
go/GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01

Lire:
docs/chantiers/GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01/00_INITIAL_PROJECT_DOC.md

Prochaine action:
implémenter modules/validation_gate/ avec tests et bundle transportable.
```

## 18_TO_DOCUMENT

TAGS:
- OPENCLAW
- VALIDATION_GATE
- TRADE_SAFETY
- TELEGRAM_APPROVAL
- NO_LIVE_TRADE_WITHOUT_GATE

Blocs à extraire :
- `7_CANONICAL_STATE`
- `12_INVARIANTS`
- `17_RESUME_POINT`

## 19_TO_REMEMBER

### MEM_CANDIDATE

Après refresh du master plan OpenClaw, le GO produit ouvert est `GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01`. Il bloque volontairement `trade_executor` tant que la gate n'est pas PASS.

### SAVE_MEMORY

Non requis automatiquement. À mémoriser seulement sur demande explicite.
