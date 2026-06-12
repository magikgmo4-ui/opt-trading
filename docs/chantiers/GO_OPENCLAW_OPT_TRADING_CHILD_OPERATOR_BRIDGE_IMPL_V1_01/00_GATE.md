---
doc_id: GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_IMPL_V1_01
doc_type: gate
repo: opt-trading
project: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_IMPL_V1_01
parent_go: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
status: open
lifecycle_stage: gate
surface: modules/openclaw_operator_bridge
source_kind: canonical
updated_at: 2026-05-16
topic_keys:
  - openclaw
  - operator-bridge
  - impl
  - db-layer
  - pipeline
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/06_BUILD_BACKLOG_AND_CHILD_GO_PLAN.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/00_SYSTEM_MASTER_PLAN.md
  - modules/gateway_openclaw/scripts/cmd.sh
---

# 00_GATE — Operator Bridge V1

## 1_MASTER_TARGET

Implémenter `modules/openclaw_operator_bridge/` :
le contrat d'interface entre opt-trading et OpenClaw gateway.

Ce module est le **point bloquant absolu** du pipeline orchestration :
sans lui, aucun worker (proposition_engine, learning_feeder) ne peut appeler OpenClaw.

---

## 2_PARENT_CANONIQUE

```text
PARENT   = GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
MASTER PLAN = docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/
BACKLOG  = 06_BUILD_BACKLOG_AND_CHILD_GO_PLAN.md — GO-01
BLOQUE   = proposition_engine (GO-06), learning_feeder (GO-10)
```

---

## 3_PRINCIPE_FONDAMENTAL

```text
opt-trading envoie une requête bornée au bridge.
Le bridge traduit et appelle OpenClaw builder.
Le bridge retourne la réponse structurée à opt-trading.

OpenClaw n'orchestre jamais — il reçoit une tâche et retourne un résultat.
Le bridge est le seul point de contact entre opt-trading et OpenClaw.
```

---

## 4_ÉTAT_PRÉREQS

```text
GATEWAY OPENCLAW:
  STATUT: OPÉRATIONNEL (ws://127.0.0.1:18789)
  USER: openclaw (dédié)
  SESSION TMUX: openclaw-gateway
  HEALTHCHECK: openclaw gateway health → {"ok":true,"status":"live"}
  INVOCATION BUILDER: openclaw agent --agent builder --json (as ghost)

MACHINE CIBLE: db-layer
REPO: /opt/trading
RÉPERTOIRE CIBLE: modules/openclaw_operator_bridge/
```

---

## 5_CONTRAT_INTERFACE

### Input (opt-trading → bridge)

```json
{
  "action": "ask | build | evaluate | review",
  "payload": {
    "context": "string — contexte signal ou résultat",
    "instruction": "string — tâche bornée",
    "parameters": {}
  },
  "request_id": "uuid",
  "timeout_s": 30
}
```

### Output (bridge → opt-trading)

```json
{
  "request_id": "uuid",
  "status": "ok | error | timeout",
  "result": {
    "content": "string — réponse OpenClaw builder",
    "structured": {}
  },
  "duration_ms": 1234,
  "error": null
}
```

### Whitelist actions

```text
ask       → question ouverte (analyse, explication)
build     → génération de proposition de trade
evaluate  → évaluation d'un signal ou résultat
review    → revue d'une décision ou d'un trade passé
```

### Actions interdites

```text
execute   → jamais — le bridge ne déclenche pas d'action trade
orchestrate → jamais — OpenClaw n'orchestre pas opt-trading
modify_config → jamais — le bridge ne modifie pas la config runtime
```

---

## 6_STRUCTURE_CIBLE

```text
modules/openclaw_operator_bridge/
  app/
    bridge.py          → classe principale OperatorBridge
    client.py          → client HTTP/CLI vers gateway_openclaw
    schema.py          → dataclasses BridgeRequest / BridgeResponse
    exceptions.py      → BridgeError, TimeoutError, ActionNotAllowed
  scripts/
    cmd.sh             → start | stop | health | test
    menu.sh
    sanity.sh
  config/
    bridge_config.yaml → timeout, whitelist actions, gateway endpoint
  tests/
    test_bridge_mock.py  → mock gateway
    test_bridge_live.py  → gateway réel (nécessite gateway actif)
  README.md
```

---

## 7_HEALTHCHECK

```text
ENDPOINT: scripts/cmd.sh health
OUTPUT ATTENDU:
  MODULE=openclaw_operator_bridge
  STATUS=live
  GATEWAY=reachable
  LAST_CALL=<timestamp ou never>

SANITY:
  scripts/sanity.sh
  → vérifie gateway joignable
  → vérifie config chargée
  → vérifie whitelist actions valide
  → PASS ou FAIL avec motif
```

---

## 8_SÉQUENCE_IMPL

```text
ÉTAPE 1 — Structure
  Créer modules/openclaw_operator_bridge/ avec squelette complet
  Écrire schema.py (BridgeRequest, BridgeResponse)
  Écrire exceptions.py

ÉTAPE 2 — Client gateway
  Écrire client.py : invoque `openclaw agent --agent builder --json`
  Format invocation : echo payload_json | openclaw agent --agent builder --json
  Capturer stdout JSON, parser BridgeResponse

ÉTAPE 3 — Bridge principal
  Écrire bridge.py : validate_action + call_client + return_response
  Appliquer whitelist, timeout, error wrapping

ÉTAPE 4 — Scripts opératoires
  Écrire cmd.sh (start/stop/health/test)
  Écrire sanity.sh
  Écrire menu.sh

ÉTAPE 5 — Tests
  test_bridge_mock.py : mock stdout du builder
  test_bridge_live.py : appel réel gateway (gate : gateway actif)

ÉTAPE 6 — Smoke PASS
  Smoke sur db-layer : action "ask" → réponse JSON valide
  Documenter résultat dans 01_SMOKE_LOG.md
```

---

## 9_GATES_DE_SORTIE

```text
GATE 1 — Structure présente
  modules/openclaw_operator_bridge/ avec tous les fichiers listés

GATE 2 — Sanity PASS
  scripts/sanity.sh → PASS (gateway joignable + config valide)

GATE 3 — Test mock PASS
  test_bridge_mock.py → tous les tests PASS

GATE 4 — Smoke live PASS (optionnel si gateway down au moment du GO)
  action "ask" sur gateway réel → {"status":"ok","result":{...}}
  ou DOCUMENTED_SKIP si gateway down avec motif

GATE 5 — Healthcheck PASS
  cmd.sh health → STATUS=live ou STATUS=gateway_unreachable (acceptable)
```

---

## 12_INVARIANTS

```text
NO_WAN_EXPOSURE        = bridge appelle uniquement ws://127.0.0.1:18789 (loopback)
NO_OPENCLAW_ORCHESTRATE = le bridge ne laisse jamais OpenClaw initier une action
NO_LIVE_TRADE_WITHOUT_GATE = le bridge ne touche pas l'exchange
NO_SECRET_IN_LOGS      = aucune clé/token dans logs ou outputs
NO_GLOBAL_INDEX_AUTO   = GO_INDEX/ACTIVE_STREAMS non modifiés sans delta prouvé
ACTION_WHITELIST_STRICT = toute action hors whitelist → BridgeError immédiat
```

---

## 16_TODO

```text
[ ] ÉTAPE 1 — Créer structure modules/openclaw_operator_bridge/
[ ] ÉTAPE 2 — Implémenter client.py (invocation builder)
[ ] ÉTAPE 3 — Implémenter bridge.py (whitelist + timeout + response)
[ ] ÉTAPE 4 — Écrire scripts cmd.sh + sanity.sh + menu.sh
[ ] ÉTAPE 5 — Tests mock PASS
[ ] ÉTAPE 6 — Smoke live PASS (ou DOCUMENTED_SKIP)
[ ] Écrire 01_SMOKE_LOG.md
[ ] Ouvrir PR vers sot/mainline
```

---

## 17_RESUME_POINT

```text
MACHINE: db-layer
RÉPERTOIRE: /opt/trading/modules/openclaw_operator_bridge/
GATEWAY: ws://127.0.0.1:18789 (vérifier actif avant impl)
INVOCATION BUILDER: openclaw agent --agent builder --json (as ghost)
PREMIER LIVRABLE: sanity.sh PASS
SECOND LIVRABLE: test_bridge_mock.py PASS
TROISIÈME LIVRABLE: smoke live action "ask" PASS
DÉBLOQUE: proposition_engine (GO-06), learning_feeder (GO-10)
```

## RISKS

- À qualifier.
