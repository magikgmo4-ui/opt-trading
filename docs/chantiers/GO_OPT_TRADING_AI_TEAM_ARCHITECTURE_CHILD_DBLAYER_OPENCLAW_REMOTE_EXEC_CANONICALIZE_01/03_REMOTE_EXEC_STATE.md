---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01_REMOTE_EXEC_STATE
doc_type: phase_state
repo: opt-trading
project: opt-trading
module: ai_team_mvp
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01
parent_go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
status: review_required
lifecycle_stage: remote_exec_state
surface: chantier
source_kind: canonical_draft
updated_at: 2026-05-08
topic_keys:
  - ai_team
  - openclaw
  - db-layer
  - fantome
  - remote_exec
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/03_REMOTE_EXEC_STATE.md
point_de_reprise: "Section Point de reprise"
links:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/01_REMOTE_EXEC_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/02_REMOTE_EXEC_LOG.md
---

# 03_REMOTE_EXEC_STATE

## Verdict global

**FAIL** pour le GO strict Phase 5 tel que demande: l'execution OpenClaw reelle depuis `db-layer` n'a pas encore pu porter le SSH jusqu'a `fantome`.

Le meme chemin cible, execute directement depuis le shell `db-layer` via `ghost`, est `PASS` et prouve que le blocage est specifique a la couche OpenClaw applicative, pas au runner distant.

## Scorecard

| Item | Etat | Evidence |
|:-----|:-----|:---------|
| source `db-layer` | `PASS` | machine courante verifiee |
| CLI OpenClaw sur `db-layer` | `PASS` | `/usr/local/bin/openclaw` |
| gateway `db-layer` | `PASS` | `RPC probe: ok`, `127.0.0.1:18789` |
| auth gateway depuis `ghost` | `GAP` | token mismatch |
| SSH `db-layer -> fantome` | `PASS` | session stricte reussie |
| alias `fantome` dans `~/.ssh/config` | `FAIL` | alias absent |
| host key `fantome` | `GAP` | pinning temporaire TOFU seulement |
| repo cible `/home/fantome/opt-trading` | `PASS` | present |
| runner cible | `PASS` | `runner.py` present |
| OpenClaw agent -> SSH `fantome` | `FAIL` | `Connection refused` dans le sandbox agent |
| SSH direct `db-layer -> fantome -> runner.py` | `PASS` | `CHAIN COMPLETE` |
| ORCHESTRATOR_CHAIN | `PASS` | 3/3 PASS |
| outputs dans `drafts/` | `PASS` | 2 nouveaux drafts + observer output |
| `git write` | `PASS` | 0 git write execute |
| denied | `PASS` | 0 denied inputs effectifs |
| secrets | `PASS` | 0 secret detecte |
| runtime trading write | `PASS` | 0 |
| `admin-trading` | `PASS` | non touche |

## Etat courant utile

- le gateway OpenClaw `db-layer` est sain sous l'utilisateur `openclaw`
- le bind reste local: `127.0.0.1:18789`
- l'utilisateur `openclaw` peut deleguer a `ghost` hors agent via `sudo -n`
- l'utilisateur `openclaw` n'a pas de cle SSH operationnelle directe vers `fantome`
- le sandbox agent OpenClaw ne rejoint pas `192.168.0.191:22`, alors que `ghost` y accede depuis le shell hote

## Cause racine probable

1. Identite d'execution scindee:
   - gateway et agent sous `openclaw`
   - chemin SSH operationnel courant sous `ghost`
2. Auth CLI locale scindee:
   - `ghost` ne peut pas piloter le gateway local sans alignement de token
3. Reseau sandbox agent:
   - les tentatives agent vers `192.168.0.191:22` retournent `Connection refused`
   - le meme SSH hors sandbox reussit
4. Routage SSH canonique incomplet sur `db-layer`:
   - alias `fantome` absent du `~/.ssh/config` courant

## Gaps restants

- aligner l'auth gateway pour permettre un pilotage propre depuis `ghost`, ou officialiser l'usage `sudo -n -u openclaw`
- choisir une identite unique pour l'execution OpenClaw reelle:
  - soit provisionner `openclaw` avec une cle SSH operationnelle et un trust hote propre pour `fantome`
  - soit officialiser un wrapper hote `openclaw -> sudo -n -u ghost -> ssh ...` hors sandbox agent
- restaurer ou canoniser l'alias SSH `fantome` sur `db-layer`
- remplacer le pinning TOFU temporaire par une source de confiance durable pour la host key `fantome`
- lever ou contourner la restriction reseau du sandbox agent OpenClaw vers `192.168.0.191:22`

## Decision Phase 6

Phase 6 recommandee:

```text
GO_OPT_TRADING_AI_TEAM_OPENCLAW_STRICT_WORKERS_PHASE_6_DBLAYER_AGENT_IDENTITY_AND_SANDBOX_FIX_01
```

Portee Phase 6:

1. Aligner l'identite d'execution OpenClaw sur `db-layer`.
2. Decider le chemin canonique `openclaw direct SSH` ou `openclaw -> ghost wrapper`.
3. Reparer l'acces reseau/sandbox de l'agent OpenClaw vers `fantome:22`.
4. Restituer un alias SSH `fantome` canonique sur `db-layer` ou documenter explicitement l'IP directe.
5. Rejouer exactement le job OpenClaw Phase 5 jusqu'a obtenir le meme `CHAIN COMPLETE` que le SSH direct.

## Point de reprise

```text
Phase 5 db-layer:
- gateway OpenClaw local: PASS
- SSH direct db-layer -> fantome: PASS
- ORCHESTRATOR_CHAIN distant: PASS
- outputs drafts/: PASS
- OpenClaw agent -> SSH fantome: FAIL

Reprendre depuis l'alignement identite + sandbox + alias SSH,
sans toucher admin-trading, sans git write, sans opencode run.
```
