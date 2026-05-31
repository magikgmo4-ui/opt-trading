---
doc_id: GO_OPENCLAW_OPT_TRADING_DBLAYER_GATEWAY_AGENT_ORCHESTRATION_PARENT_01_CADRAGE
doc_type: cadrage_parent
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_DBLAYER_GATEWAY_AGENT_ORCHESTRATION_PARENT_01
status: closed
lifecycle_stage: closed
created_at: 2026-05-31
closed_at: 2026-05-31
machine: db-layer
openclaw_version: 2026.3.11 (29dc654)
gateway_port: 18789
gateway_user: openclaw
---

# 00_CADRAGE_PARENT — OpenClaw Gateway + Agent Orchestration db-layer

## 1_MASTER_TARGET

Prouver l'orchestration complète via le layer OpenClaw réel sur db-layer :
gateway démarré (tmux `openclaw-gateway`) + agent OpenClaw reçoit un job spec
et dispatche vers `desk_pro_orchestrator` — retour FORMAT 3/4 via l'agent,
gate humain FORMAT 5. Distinguer du path direct Python précédemment validé.

## 2_PRECONDITIONS_VALIDEES

```text
OpenClaw CLI         = 2026.3.11 (29dc654) installé sur db-layer
Gateway port         = 18789, user=openclaw, session=openclaw-gateway (tmux)
Gateway status       = stopped au 2026-05-31 (à démarrer dans CHILD_01)
agent --local        = disponible (embedded, sans gateway)
desk_pro_orchestrator = PAPER PASS (6 runs validés — STABILITY_WINDOW_01)
Boucle FORMAT 1→5    = prouvée en exécution directe Python (CHILD_FIRST_LOOP_JOB_01)
```

## 3_GAPS_IDENTIFIES

| GAP | Description | Child GO cible |
| --- | --- | --- |
| GAP 1 | Gateway stopped — démarrage + smoke reachability non prouvé | CHILD_GATEWAY_START_SMOKE_01 |
| GAP 2 | Agent OpenClaw n'a jamais reçu ni dispatché un job orchestrateur | CHILD_AGENT_FIRST_ORCHESTRATION_JOB_01 |

## 4_CHILD_GOs

| Child | Portée | Mode |
| --- | --- | --- |
| `CHILD_GATEWAY_START_SMOKE_01` | Démarrer gateway + probe reachability + health check | `openclaw gateway start` sous user openclaw |
| `CHILD_AGENT_FIRST_ORCHESTRATION_JOB_01` | Envoyer FORMAT 1 à l'agent OpenClaw → dispatch orchestrateur → FORMAT 3/4 → FORMAT 5 gate | `openclaw agent --local` ou via gateway |

## 5_CONFIGURATION_REFERENCE

```text
Gateway WebSocket : ws://127.0.0.1:18789
Gateway start     : sudo -u openclaw openclaw gateway start  (ou tmux session)
Gateway health    : sudo -u openclaw openclaw health
Agent local       : sudo -u openclaw openclaw agent --local --message "<FORMAT_1>"
Agent via gateway : sudo -u openclaw openclaw agent --message "<FORMAT_1>"
Session tmux      : openclaw-gateway (user openclaw)
Config            : /home/openclaw/.openclaw/openclaw.json
```

## 6_DISTINCTION_PATH_PRECEDENT

```text
Path précédent (CHILD_FIRST_LOOP_JOB_01) :
  ghost → python3 -m modules.desk_pro_orchestrator ... (exécution directe)

Path cible (ce parent) :
  ghost → openclaw agent → OpenClaw agent layer → desk_pro_orchestrator
  ↳ OpenClaw joue le rôle d'orchestrateur — reçoit le job spec, décide du dispatch
```

## 12_INVARIANTS

```text
- Mode PAPER exclusif — aucun ordre réel
- 0 runtime modifié (gateway_openclaw module = read-only pour ce GO)
- FILE_SCOPE.txt dans chaque child dès J1
- Gateway démarré uniquement via les scripts module prévus (cmd.sh / scripts/)
- Aucun secret dans les commits
- Gate humain FORMAT 5 obligatoire sur CHILD_AGENT_FIRST_ORCHESTRATION_JOB_01
```

## 17_RESUME_POINT

```text
docs/chantiers/GO_OPENCLAW_OPT_TRADING_DBLAYER_GATEWAY_AGENT_ORCHESTRATION_PARENT_01/00_INITIAL_PROJECT_DOC.md
Prochain : ouvrir CHILD_GATEWAY_START_SMOKE_01
```
