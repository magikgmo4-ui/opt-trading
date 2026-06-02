---
doc_id: GO_OPENCLAW_OPT_TRADING_DBLAYER_ORCHESTRATOR_CHILD_FIRST_LOOP_JOB_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_DBLAYER_ORCHESTRATOR_CHILD_FIRST_LOOP_JOB_01
parent_go: GO_OPENCLAW_OPT_TRADING_DBLAYER_ORCHESTRATOR_PAPER_STABILITY_FIRST_JOB_PARENT_01
status: closed
lifecycle_stage: cadrage
created_at: 2026-05-31
machine_cible: db-layer
machine_operateur: fantome
surface: docs/chantiers
source_kind: canonical
topic_keys:
  - openclaw
  - db-layer
  - orchestrator
  - paper
  - loop_contract
  - first_job
  - human_gate
---

# 00_INITIAL_PROJECT_DOC — Child : Premier Job Boucle OpenClaw FORMAT 1→5

## 1_MASTER_TARGET

Exécuter le premier job complet via la boucle OpenClaw contractuelle sur db-layer :
FORMAT 1 (job spec) → OpenClaw → desk_pro_orchestrator PAPER → FORMAT 3 (résultat) →
FORMAT 4 (synthèse) → FORMAT 5 (gate humain). Gate humain obligatoire avant merge.

## 2_PRECONDITIONS

```text
CHILD_PAPER_STABILITY_WINDOW_01 = PR #984 mergée
Loop contract formalisé         = docs/openclaw/loop_contract/ (5 formats)
Gateway db-layer                = port 18789, user openclaw, session openclaw-gateway
Orchestrateur                   = python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator
SSH fantome → db-layer          = validé
```

## 3_BOUCLE_COMPLETE

### FORMAT 1 — Job Spec (ChatGPT → OpenClaw)

```yaml
job_id: FIRST_LOOP_JOB_DB_LAYER_01
intent: exécuter desk_pro_orchestrator en PAPER mode sur db-layer, retourner résultats structurés
scope:
  machine: db-layer
  mode: PAPER
  command: python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator run --config modules/desk_pro_orchestrator/config/run_config.example.json
allowed_ops:
  - read
  - execute_paper
  - log
output_expected: FORMAT_3
constraints:
  - no_live_trade
  - no_secrets
  - no_git_write
  - paper_only
```

### FORMAT 2 — Instruction (OpenClaw → IDE/agent)

```yaml
command: ssh db-layer "cd /opt/trading && python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator run --config modules/desk_pro_orchestrator/config/run_config.example.json"
file_scope: docs/chantiers/GO_OPENCLAW_OPT_TRADING_DBLAYER_ORCHESTRATOR_CHILD_FIRST_LOOP_JOB_01/**
agent_target: fantome
return_format: FORMAT_3
```

### FORMAT 3 — Résultat attendu (IDE → OpenClaw)

```yaml
status: PASS | FAIL | PARTIAL
run_id: desk_run_YYYYMMDD_HHMMSS
modules_ok: 11
modules_failed: 0
actions_observed: [NO_ACTION, PREPARE_LONG, PREPARE_SHORT]
secrets_found: false
live_trade: false
git_status_clean: true
```

### FORMAT 4 — Synthèse (OpenClaw → ChatGPT)

```yaml
verdict: PASS | FAIL
key_findings:
  - run_id documenté
  - 11/11 modules OK
  - mode PAPER respecté
gate_required: true
gate_question: "Confirmes-tu que ce job PAPER peut être mergé et que le parent GO peut avancer vers CHILD_FIRST_LOOP_JOB_01 PASS ?"
```

### FORMAT 5 — Gate Humain

```yaml
decision: APPROVE | REJECT | RESTART
motif: <obligatoire>
authorize_merge: true | false
```

## 4_CRITERES_PASS

| Critère | Requis |
| --- | --- |
| FORMAT 1 rédigé et tracé | OUI |
| FORMAT 2 exécuté (SSH db-layer) | OUI |
| FORMAT 3 produit (run_id + résultats) | OUI |
| modules_ok | 11/11 |
| failed | 0 |
| actions hors périmètre | 0 |
| secrets | 0 |
| live trade | aucun |
| FORMAT 4 synthèse rédigée | OUI |
| FORMAT 5 gate humain = APPROVE | OUI |
| git status post-run | clean |

## 5_LIVRABLES

```text
FIRST_LOOP_JOB_EXECUTION_REPORT.md  — trace FORMAT 1→3, run_id, résultats
FIRST_LOOP_JOB_GATE_REPORT.md       — FORMAT 4 synthèse + FORMAT 5 décision humain
20_ACCEPTANCE_REPORT.md             — verdict final PASS/FAIL
```

## 12_INVARIANTS

```text
- Mode PAPER exclusif — aucun ordre réel, aucun live
- Gate humain FORMAT 5 = APPROVE obligatoire avant merge
- 0 runtime modifié
- FILE_SCOPE.txt présent dès J1
- Aucun secret dans les commits
```

## 17_RESUME_POINT

```text
docs/chantiers/GO_OPENCLAW_OPT_TRADING_DBLAYER_ORCHESTRATOR_CHILD_FIRST_LOOP_JOB_01/00_INITIAL_PROJECT_DOC.md
Prochain : exécuter FORMAT 1→2 (run SSH db-layer), collecter FORMAT 3, rédiger FORMAT 4, soumettre FORMAT 5
```
