---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01_REMOTE_EXEC_PLAN
doc_type: remote_exec_plan
repo: opt-trading
project: opt-trading
module: ai_team_mvp
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01
parent_go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
status: review_required
lifecycle_stage: remote_exec_plan
surface: chantier
source_kind: canonical_draft
updated_at: 2026-05-08
topic_keys:
  - ai_team
  - openclaw
  - db-layer
  - fantome
  - remote_exec
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/01_REMOTE_EXEC_PLAN.md
point_de_reprise: "Section Validation attendue"
links:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/02_REMOTE_EXEC_LOG.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/03_REMOTE_EXEC_STATE.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/REPRISE_DB_LAYER_20260505.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01/RUNTIME_LOG.md
---

# 01_REMOTE_EXEC_PLAN

## Objectif

Executer la Phase 5 reelle depuis `db-layer`, avec `db-layer -> OpenClaw gateway -> SSH -> fantome -> python3 modules/ai_team_mvp/runner.py`, sans `admin-trading`, sans `git write`, sans `opencode run`, et sans ecriture hors `modules/ai_team_mvp/drafts/`.

## Decision canonique

- source orchestratrice: `db-layer`
- cible d'execution: `fantome`
- transport: `SSH`
- gateway OpenClaw: `db-layer`, bind loopback `127.0.0.1:18789`
- runner cible: `python3 modules/ai_team_mvp/runner.py`
- task packet cible: `modules/ai_team_mvp/tasks/orchestrator_chain_v2.json`
- zone d'output autorisee: `modules/ai_team_mvp/drafts/`
- `admin-trading`: hors perimetre

## Etat de depart constate

- machine courante: `db-layer`
- utilisateur operateur courant: `ghost`
- repo local courant: `/opt/trading`
- `openclaw` installe sur `db-layer`: `PASS`
- module local `modules/gateway_openclaw/`: `PASS`
- repo local `/opt/trading` ne contient pas `modules/ai_team_mvp/`
- repo cible reel localise sur `fantome`: `/home/fantome/opt-trading`

## Plan retenu

1. Verifier le gateway OpenClaw sur `db-layer`.
2. Verifier la route SSH `db-layer -> fantome` avec une cle operationnelle deja autorisee.
3. Verifier le repo cible et le runner sur `fantome`.
4. Tenter l'execution reelle via OpenClaw sur `db-layer`.
5. Si OpenClaw bloque, executer la meme commande en SSH direct depuis `db-layer` pour isoler le gap specifique OpenClaw.
6. Verifier les outputs dans `drafts/` et l'absence de `git write`.
7. Documenter le PASS/FAIL et decider la Phase 6.

## Job OpenClaw cible

Commande OpenClaw reelle tentee sur `db-layer`:

```bash
sudo -n -u openclaw openclaw agent --agent orchestrateur --json --timeout 180 --message "On db-layer, execute exactly this shell command and nothing else: sudo -n -u ghost bash -lc 'ssh -o BatchMode=yes -o UserKnownHostsFile=/tmp/fantome_phase5_known_hosts -o StrictHostKeyChecking=yes fantome@192.168.0.191 \"cd /home/fantome/opt-trading && python3 modules/ai_team_mvp/runner.py modules/ai_team_mvp/tasks/orchestrator_chain_v2.json\"'. Return only the raw stdout lines, no commentary."
```

Commande de controle terrain utilisee pour isoler le gap OpenClaw:

```bash
ssh -o BatchMode=yes -o UserKnownHostsFile=/tmp/fantome_phase5_known_hosts -o StrictHostKeyChecking=yes fantome@192.168.0.191 "cd /home/fantome/opt-trading && python3 modules/ai_team_mvp/runner.py modules/ai_team_mvp/tasks/orchestrator_chain_v2.json"
```

## Validation attendue

| Point | Attendu |
|:------|:--------|
| OpenClaw cote `db-layer` | CLI disponible, gateway sain |
| SSH `db-layer -> fantome` | PASS |
| Repo cible | `/home/fantome/opt-trading` present |
| Runner | `runner.py` present |
| ORCHESTRATOR_CHAIN | exit code 0, `CHAIN COMPLETE` |
| Outputs | nouveaux artefacts dans `modules/ai_team_mvp/drafts/` |
| Git | 0 `git add`, `git commit`, `git push` |
| Denied | 0 denied inputs effectifs |
| Secrets | 0 secret/.env/token |
| Runtime trading | 0 write |
| admin-trading | non touche |

## Conditions operatoires constatees

- l'alias SSH `fantome` est absent du `~/.ssh/config` courant sur `db-layer`
- l'IP documentee reste `192.168.0.191`
- la cle hote a ete chargee dans `/tmp/fantome_phase5_known_hosts` via `ssh-keyscan`
- fingerprint ED25519 observe: `SHA256:qPww4rm00lbiaTIS8XixarBxEZznfjc4kMi19zmGZlA`
- ce pinning est temporaire et non persistant: gap TOFU a fermer en Phase 6
- le gateway tourne sous l'utilisateur `openclaw`, alors que le chemin SSH operationnel courant est porte par `ghost`

## Portee de la phase

- aucun usage de `admin-trading`
- aucun `git write`
- aucun `opencode run`
- aucune cle temporaire Phase 3
- `PATCH_DRAFT` reste proposal-only
- aucune ecriture hors `modules/ai_team_mvp/drafts/`

## RISKS

- À qualifier.
