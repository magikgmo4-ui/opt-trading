---
doc_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01_RUNBOOK
doc_type: runbook_operational
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01
parent_go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: canonical
lifecycle_stage: operational
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-18
topic_keys:
  - openclaw
  - db-layer
  - orchestrator
  - runbook
  - operational
  - dry_run
version: 1.0
---

# DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01

## 1. Overview

Runbook operationnel borne pour l'orchestrateur OpenClaw sur `db-layer`.
Le but est de figer le mode d'usage valide sans ouvrir de nouveau couloir de risque.

## 2. Reference State

```text
fantome = poste operateur
db-layer = cible OpenClaw validee
SSH = transport controle
OpenClaw db-layer = CLI + Gateway V2 + orchestrateur presents
```

## 3. Prechecks

| Controle | Attendu |
|---|---|
| SSH `db-layer` | accessible |
| `hostname` | `db-layer` |
| `pwd` | `/home/ghost` ou sous-chemin controle |
| `git status` | clean |
| `openclaw --version` | present |
| orchestrateur | `modules/desk_pro_orchestrator/` present |
| output dir | `data/desk_runs/` |

## 4. Allowed Commands

```bash
ssh db-layer "hostname && whoami && pwd && cd /home/ghost/opt-trading && git status --short"
ssh db-layer "cd /home/ghost/opt-trading && /usr/local/bin/openclaw --version"
ssh db-layer "cd /home/ghost/opt-trading && python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator status"
ssh db-layer "cd /home/ghost/opt-trading && python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator explain"
ssh db-layer "cd /home/ghost/opt-trading && python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator sample-run"
```

## 5. Forbidden Commands

```text
sudo
live trading
secret access
write libre
rm -rf
chmod -R
chown -R
git commit/push autonome
commandes hors perimetre du runbook
```

## 6. Dry-run / Read-only Procedure

1. valider la session SSH `db-layer`
2. valider le repo et `git status`
3. lancer `status`
4. lancer `explain`
5. lancer `sample-run`
6. verifier `run_summary.json`
7. verifier le clean status apres execution

## 7. Evidence

- sortie `status`
- sortie `explain`
- sortie `sample-run`
- `data/desk_runs/<run_id>/run_summary.json`
- `git status` avant/apres
- trace du run id

## 8. Stop Conditions

```text
CLI openclaw absent -> NEEDS_APPROVAL_INSTALL_DB_LAYER
secret detecte -> STOP
live trading detecte -> STOP
sudo detecte -> STOP
write hors data/desk_runs -> STOP
```

## 9. Conditions Before Bigger Jobs

- runbook reference approuvee
- probes read-only repetables
- aucune dette de clean status
- nouveau GO explicite pour tout write-gated ou job plus large

## RISKS

- À qualifier.
