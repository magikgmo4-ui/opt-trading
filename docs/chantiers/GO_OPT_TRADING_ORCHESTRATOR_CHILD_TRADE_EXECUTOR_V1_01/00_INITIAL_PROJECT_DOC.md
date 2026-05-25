---
doc_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_TRADE_EXECUTOR_V1_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ORCHESTRATOR_CHILD_TRADE_EXECUTOR_V1_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
master_project_plan_id: MPP_OPENCLAW_ORCHESTRATOR_FULL
pf_id: PF_OPENCLAW_ORCHESTRATOR_FULL
status: open
lifecycle_stage: opening
surface: modules/trade_executor
source_kind: canonical
updated_at: 2026-05-25
topic_keys:
  - openclaw
  - orchestration
  - trade-execution
  - paper-trading
  - validation-gate
  - trade-safety
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/00_SYSTEM_MASTER_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_ORCHESTRATOR_CHILD_VALIDATION_GATE_V1_01/00_INITIAL_PROJECT_DOC.md
---

# 00_INITIAL_PROJECT_DOC — Trade Executor V1

## 1_MASTER_TARGET

Contribuer à `PF_OPENCLAW_ORCHESTRATOR_FULL` en ouvrant `modules/trade_executor/` — exécuteur de trades validés par `validation_gate`, mode paper uniquement en V1.

## 2_INITIAL_PROJECT_DOC

Cette fiche ouvre le child produit `GO_OPT_TRADING_ORCHESTRATOR_CHILD_TRADE_EXECUTOR_V1_01`.

```text
PARENT_GO = GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
MASTER_PROJECT_PLAN = MPP_OPENCLAW_ORCHESTRATOR_FULL
PF = PF_OPENCLAW_ORCHESTRATOR_FULL
GO_STRUCTURAL_ROLE = GO_CHILD_ATTACHED_TO_PARENT
```

## 3_INITIAL_NEED

Après `validation_gate` PASS, la prochaine surface bloquante est `trade_executor`. Sans elle, aucune proposition validée ne peut être exécutée, même en paper.

```text
validation_gate PASS
→ trade_executor OUVERT
→ chaîne produit complète jusqu'à l'exécution paper
```

## 4_MASTER_PROJECT_PLAN

```text
signal_router PASS
→ proposition_engine PASS
→ validation_gate PASS
→ trade_executor V1 (ce GO)
→ result_tracker
→ datasheet_writer
→ learning_feeder
```

## 5_GO_PLAN

```text
GO_ID: GO_OPT_TRADING_ORCHESTRATOR_CHILD_TRADE_EXECUTOR_V1_01
FINAL_TARGET: trade_executor V1 complet, convention module respectée, tests, smoke
```

## 6_FINAL_TARGET

- Compléter `modules/trade_executor/` selon la convention module :
  - `__init__.py` — docstring
  - `app/__init__.py` — exports publics
  - `app/__main__.py` — CLI entry point
  - `scripts/cmd.sh` — sanity, test, execute, status
  - `scripts/menu.sh` — menu interactif
  - `scripts/install_shortcuts.sh` — installation wrappers
  - `README.md` — documentation
- Vérifier que tous les tests (28) passent
- Vérifier que la sanity passe
- Produire bundle, patch canonique, zip transportable

## 7_CANONICAL_STATE

Préconditions :

```text
VALIDATION_GATE = PASS (mergé sur sot/mainline)
EXECUTION_ENGINE_PAPER = opérationnel
NOTIFICATION_DISPATCHER = opérationnel
```

État de départ :

```text
TRADE_EXECUTOR = module existant avec code + 28 tests, mais NON OUVERT formellement
CMD.SH = ABSENT
MENU.SH = ABSENT
INSTALL_SHORTCUTS.SH = ABSENT
README.MD = ABSENT
```

## 8_VALIDATED_PLAN

1. Ajouter `__init__.py` docstring
2. Ajouter `app/__init__.py` exports
3. Ajouter `app/__main__.py` CLI entry point
4. Ajouter `scripts/cmd.sh`
5. Ajouter `scripts/menu.sh`
6. Ajouter `scripts/install_shortcuts.sh`
7. Ajouter `README.md`
8. Vérifier tests (28) + sanity
9. Produire bundle / patch / zip
10. Ouvrir PR

## 9_SELECTED_SOLUTION

Module existant à compléter — pas de réécriture du code métier (executor.py, schema.py), seulement ajout des fichiers de convention.

## 10_SELECTED_SETUP

```text
BRANCH = go/GO_OPT_TRADING_ORCHESTRATOR_CHILD_TRADE_EXECUTOR_V1_01
BASE_SHA = HEAD de sot/mainline
MODULE = modules/trade_executor/
DOCS = docs/chantiers/GO_OPT_TRADING_ORCHESTRATOR_CHILD_TRADE_EXECUTOR_V1_01/
BUNDLE_REQUIRED = true
PATCH_REQUIRED = true
ZIP_TRANSPORTABLE_REQUIRED = true
```

## 11_KEY_DECISIONS

- `trade_executor` V1 = paper adapter only — pas de Bitget live
- Invariant dur : `gate_decision.verdict == "APPROVED"` obligatoire
- Aucune modification du code métier existant

## 12_INVARIANTS

```text
NO_LIVE_TRADE_WITHOUT_GATE = true
NO_LIVE_BITGET_IN_V1 = true
NO_SECRET_IN_LOGS = true
NO_OPENCLAW_ORCHESTRATE = true
OPT_TRADING_ORCHESTRATES = true
NO_GLOBAL_INDEX_PATCH_WITHOUT_EXPLICIT_TRIGGER = true
```

## 13_ESTABLISHED

- `validation_gate` = PASS (mergé)
- `execution_engine/adapters/paper` = opérationnel
- `trade_executor` = code existant mais GO non ouvert

## 14_HYPOTHESIS

- Le module peut être ouvert sans modification du code métier
- La convention module peut être satisfaite par ajout uniquement

## 15_REMAINING_GAP

- Fichiers de convention absents
- GO non ouvert formellement

## 16_TODO

1. Ajouter fichiers de convention
2. Vérifier tests passent
3. Produire bundle, patch, zip
4. Ouvrir PR

## 17_RESUME_POINT

```text
Reprendre sur branche:
go/GO_OPT_TRADING_ORCHESTRATOR_CHILD_TRADE_EXECUTOR_V1_01

Prochaine action:
finaliser les fichiers de convention, ouvrir PR.
```

## 18_TO_DOCUMENT

TAGS:
- OPENCLAW
- TRADE_EXECUTOR
- PAPER_TRADING
- VALIDATION_GATE

## 19_TO_REMEMBER

### MEM_CANDIDATE

Après validation_gate PASS, le GO produit suivant est trade_executor V1. Module existant mais non ouvert formellement.
