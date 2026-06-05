---
doc_id: GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01_TMUX_OPERATOR_PROTOCOL
doc_type: operator_protocol
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01
parent_go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: open
lifecycle_stage: protocol
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-05
topic_keys:
  - openclaw
  - tmux
  - gateway
  - db-layer
  - operator_protocol
reference_canonique_principale: docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01/01_TMUX_OPERATOR_PROTOCOL.md
point_de_reprise: "Section NEXT_GO"
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/REPRISE_DB_LAYER_20260505.md
---

# 01_TMUX_OPERATOR_PROTOCOL

## Objet

Décrire le protocole opératoire `tmux` `start / status / stop / evidence` pour la supervision du Gateway OpenClaw sur `db-layer`, sans exécution runtime dans cette passe documentaire.

## 7_CANONICAL_STATE

- machine cible unique : `db-layer`
- session `tmux` cible : `openclaw-gateway`
- utilisateur runtime visé : `openclaw`
- bind attendu : `127.0.0.1:18789`
- bridge interdit
- WAN interdit
- `admin-trading` hors scope
- `systemd` durable hors scope

## Préconditions Git Et Machine

- branche de travail : `go/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01`
- base documentaire intégrée : merge commit `050e625d53b8603b76f9723f826b44291441128a` présent sur `sot/mainline`
- repo de travail : `/opt/trading`
- machine confirmée : `db-layer`
- aucune autre action runtime OpenClaw en parallèle

## Préconditions OpenClaw Locales

Avant toute tentative de démarrage dans une future passe opératoire, vérifier en lecture :

```bash
cd /opt/trading
bash modules/gateway_openclaw/scripts/cmd.sh status
bash modules/gateway_openclaw/scripts/cmd.sh paths
tmux ls
ss -ltnp | grep 18789 || true
ps -ef | grep -i '[o]penclaw' || true
```

Objectif : qualifier l'état initial sans lancer OpenClaw.

## Commande De Création Session tmux

Commande cible à utiliser dans la future passe opératoire :

```bash
tmux new-session -d -s openclaw-gateway
```

La création ne doit être faite que si aucune session `openclaw-gateway` n'existe déjà.

## Commande De Démarrage Gateway Dans tmux

Commande cible prévue pour la future passe opératoire, en foreground dans la session `tmux` :

```bash
tmux send-keys -t openclaw-gateway "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh start" C-m
```

Ce protocole ne l'exécute pas. Il documente seulement la séquence cible.

## Commandes Status

### tmux

```bash
tmux ls
tmux has-session -t openclaw-gateway
tmux capture-pane -pt openclaw-gateway | tail -100
```

### Port et listener local

```bash
ss -ltnp | grep 18789 || true
lsof -iTCP:18789 -sTCP:LISTEN || true
```

### Santé locale si disponible

```bash
curl -fsS http://127.0.0.1:18789/ || true
curl -fsS http://127.0.0.1:18789/health || true
```

### Processus

```bash
ps -ef | grep -i '[o]penclaw' || true
```

## Commandes Stop / Rollback

### Arrêt session tmux

```bash
tmux kill-session -t openclaw-gateway
```

### Vérifications post-arrêt

```bash
tmux has-session -t openclaw-gateway || true
ss -ltnp | grep 18789 || true
lsof -iTCP:18789 -sTCP:LISTEN || true
ps -ef | grep -i '[o]penclaw' || true
```

### Règle rollback

- si l'arrêt ne libère pas le port, classer `FAIL`
- si un processus zombie subsiste, classer `FAIL`
- ne pas introduire de mécanisme persistant compensatoire dans cette phase

## Critères PASS

- session `tmux` créée sous le nom attendu
- Gateway visible dans la session ciblée
- listener actif sur `127.0.0.1:18789`
- statut local concluant si endpoint disponible
- arrêt documenté et port libéré après stop
- aucune modification runtime persistante

## Critères PARTIAL

- Gateway démarre mais `health/status` reste non concluant
- port actif mais réponse locale instable
- arrêt manuel requis mais port finalement libéré

## Critères FAIL

- bind non local
- port déjà occupé sans cause qualifiée
- processus impossible à arrêter proprement
- modification persistante non prévue
- bridge, WAN ou `admin-trading` touché

## Preuves Attendues

- `git status --short --branch`
- `tmux ls`
- `tmux capture-pane -pt openclaw-gateway`
- `ss -ltnp | grep 18789`
- `lsof -iTCP:18789 -sTCP:LISTEN`
- `curl` local si endpoint disponible
- `ps -ef | grep -i '[o]penclaw'`
- journal opérateur court avec verdict `PASS`, `PARTIAL` ou `FAIL`

## HYPOTHESE

- `modules/gateway_openclaw/scripts/cmd.sh start` suffit comme point d'entrée de démarrage
- la supervision `tmux` couvre le besoin initial sans `systemd`
- le bind loopback reste le comportement attendu sur `db-layer`

## GAP

- aucune exécution réelle de `start/status/stop` n'a encore été produite
- les endpoints HTTP exacts restent à confirmer en machine
- la forme du journal opérateur court reste à fixer si besoin

## TODO

1. relire et valider ce protocole comme base de passe opératoire
2. ne lancer la passe runtime qu'après validation explicite
3. consigner les preuves réelles dans un artefact dédié de runtime

## NEXT_GO

```text
GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01
```

Ce prochain GO ouvre la passe opératoire contrôlée, toujours sur `db-layer`, toujours sans bridge ni élargissement de scope.

## RISKS

- À qualifier.
