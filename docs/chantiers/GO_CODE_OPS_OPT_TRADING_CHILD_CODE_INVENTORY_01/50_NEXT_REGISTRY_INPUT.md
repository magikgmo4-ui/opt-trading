---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01_NEXT_REGISTRY_INPUT
doc_type: registry_input
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01
status: open
lifecycle_stage: inventory_complete
topic_keys: [registry_input, code_registry, code_ops, audit_first]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
---

# 50_NEXT_REGISTRY_INPUT

Input pour `GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01`.

Ce document est l'output consommable directement par le prochain child GO pour
initialiser le registre canonique du code.

---

## Structure cible du registre

Per `20_CODE_REGISTRY_SPEC.md` du parent :

```
code_id | path | role | owner_surface | status | entrypoint | inputs | outputs | tests | compatibility | duplicates | risk_level | next_action
```

---

## Lot 1 — Services FastAPI (priorité : HIGH)

| code_id | path | role | owner_surface | status | entrypoint | risk_level | next_action |
|---|---|---|---|---|---|---|---|
| SVC_WEBHOOK_01 | `webhook_server.py` | service | racine | active | `python3 webhook_server.py` | high | verrouiller tests avant refactor |
| SVC_PERF_01 | `perf/perf_app.py` | service | racine | active | `python3 perf/perf_app.py` | high | verrouiller tests avant refactor |
| SVC_BITGET_BRIDGE_01 | `bitget_bridge.py` | adapter | racine | active | `python3 bitget_bridge.py` | high | qualifier relation simex |

---

## Lot 2 — Moteurs runtime (priorité : HIGH)

| code_id | path | role | owner_surface | status | risk_level | duplicates | next_action |
|---|---|---|---|---|---|---|---|
| ENG_RISK_01 | `modules/risk_engine/app/risk_engine.py` | runtime | risk_engine | active | high | — | registre complet |
| ENG_RISK_CALC_01 | `modules/risk_engine/app/risk_calculator.py` | runtime | risk_engine | active | high | — | registre complet |
| ENG_EXEC_01 | `modules/execution_engine/app/execution_engine.py` | runtime | execution_engine | active | high | D02 | qualifier D02 |
| ENG_EXEC_EXECUTOR_01 | `modules/execution_engine/executor.py` | runtime | execution_engine | active | high | D02 | qualifier D02 |
| ENG_POSITION_01 | `modules/position_engine/app/position_engine.py` | runtime | position_engine | active | high | — | registre complet |
| ENG_DECISION_01 | `modules/decision_engine/app/decision_engine.py` | runtime | decision_engine | active | high | — | registre complet |
| ENG_STRATEGY_01 | `modules/decision_engine/app/strategy_logic.py` | runtime | decision_engine | active | high | — | registre complet |
| ENG_PERF_01 | `modules/perf_engine/app/perf_engine.py` | runtime | perf_engine | active | high | D01 | qualifier D01 |
| ENG_PERF_ALT_01 | `modules/perf/engine/` | runtime | perf | active | high | D01 | qualifier D01 |
| ENG_ROUTER_01 | `modules/engines/router.py` | runtime | engines | active | blocked | D03 | qualifier consommateurs |
| ENG_ROUTER_ALT_01 | `modules/router/` | runtime | router | active | blocked | D03 | qualifier relation D03 |
| ENG_SIGNAL_01 | `modules/signal_router/` | adapter | signal_router | active | medium | — | registre complet |

---

## Lot 3 — Desk Pro / Vision (priorité : MEDIUM)

| code_id | path | role | owner_surface | status | risk_level | next_action |
|---|---|---|---|---|---|---|
| DESK_RUNNER_01 | `modules/desk_pro_runner/app/desk_pro_runner.py` | runtime | desk_pro_runner | active | medium | registre complet |
| DESK_ORCH_01 | `modules/desk_pro_orchestrator/app/desk_pro_orchestrator.py` | runtime | desk_pro_orchestrator | active | medium | registre complet |
| DESK_DASH_01 | `modules/desk_pro_dashboard/app/desk_pro_dashboard.py` | runtime | desk_pro_dashboard | active | medium | registre complet |
| DESK_STATE_01 | `modules/desk_state/desk_state.py` | runtime | desk_state | active | medium | registre complet |
| VISION_BOT_01 | `modules/vision_bot/app/vision_bot.py` | runtime | vision_bot | active | medium | registre complet |
| VISION_STEP2_01 | `modules/bot_vision_step2/app/bot_vision_step2.py` | runtime | bot_vision_step2 | active | medium | registre complet |
| VISION_STEP1_01 | `modules/bot_vision/bot_vision_step1/` | legacy | bot_vision | candidate | low | qualifier statut |

---

## Lot 4 — Doublons à qualifier (priorité : BLOQUANTE avant refactor)

| doublon_id | paths | type | action obligatoire |
|---|---|---|---|
| D01 | `modules/perf/engine/` + `modules/perf_engine/app/perf_engine.py` | fonctionnel probable | lire les deux, identifier producteur unique |
| D02 | `modules/execution_engine/executor.py` + `modules/trade_executor/app/executor.py` | rôle executor similaire | identifier consommateurs de chaque |
| D03 | `modules/engines/router.py` + `modules/router/` | routeurs potentiellement redondants | `git grep` pour trouver tous les imports |
| D04 | `modules/simex_bitget_bridge/` + `bitget_bridge.py` | bridges Bitget | qualifier si simex est une couche intermédiaire |
| D05 | scripts doublés `execution_engine/scripts/` | aliasés dans même module | supprimer les scripts aliasés non canoniques |
| D06 | `modules/install_module_openclaw.bak_20260314/` + `modules/ops_wrappers.bak/` | .bak dans repo | ouvrir lot de nettoyage dédié |

---

## Lot 5 — Modules sans sanity_check.sh (priorité : MEDIUM)

22 modules manquent de `sanity_check.sh`. À traiter dans un batch dédié :

```text
modules/configure_openclaw
modules/datasheet_writer
modules/dev_validation_hub
modules/doctor_openclaw
modules/evidence_openclaw
modules/gateway_openclaw
modules/install_module_openclaw
modules/learning_feeder
modules/localcms
modules/menu_openclaw
modules/model_provider_openclaw
modules/notification_dispatcher
modules/openclaw_config_modulaire
modules/openclaw_operator_bridge
modules/openclaw_tmux_operator
modules/proposition_engine
modules/result_tracker
modules/signal_router
modules/trade_executor
modules/trading_lab_v1
modules/trading_realtime_v1
modules/validation_gate
```

---

## Lot 6 — Validateurs à enregistrer (priorité : MEDIUM)

| validator_id | path | tests prouvés | next_action |
|---|---|---|---|
| V01 | `tools/governance/validate_master_target_continuity.py` | non | ajouter test |
| V02 | `tools/openclaw/validate_policy_json_report_schema.py` | oui | registre complet |
| V03 | `tools/openclaw/validate_runtime_security_all.py` | oui | registre complet |
| V04 | `tools/openclaw/validate_skill_policy_static.py` | oui | registre complet |
| V05 | `tools/strategy/validate_strategy_registry.py` | non | ajouter test |
| V06 | `modules/governance/openclaw_mcp_policy_validator/__main__.py` | oui | registre complet |
| V13 | `modules/validation_gate/app/__main__.py` | oui | registre complet |
| V14 | `modules/trae_module_validator/` | inconnu | qualifier rôle |

---

## Schemas à enregistrer (priorité : HIGH)

| contract_id | path | tests | next_action |
|---|---|---|---|
| S01 | `schemas/webhook_event_v1.json` | partiel | compléter couverture |
| S02 | `docs/ot/trading/schemas/trading_event_v1.schema.json` | non | ajouter test |
| S03 | `docs/ot/trading/schemas/trading_trade_v1.schema.json` | non | ajouter test |

---

## Verdict de ce child GO

```text
PASS_INVENTORY_READY

L'inventaire est complet.
Les tables A, B, C, D sont produites.
La carte de risque est produite.
Les doublons suspects sont identifiés (non encore qualifiés).
Le prochain GO peut remplir le registre depuis ce document.

NEXT_GO = GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01
```
