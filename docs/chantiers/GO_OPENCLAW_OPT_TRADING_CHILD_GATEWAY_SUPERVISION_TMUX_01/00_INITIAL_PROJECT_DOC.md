---
doc_id: GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01
parent_go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: open
lifecycle_stage: cadrage
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-05
topic_keys:
  - openclaw
  - tmux
  - gateway
  - db-layer
  - supervision
reference_canonique_principale: docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Section NEXT_GO"
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/REPRISE_DB_LAYER_20260505.md
---

# GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01

## Classification

- type : child runtime doc-first
- statut : open
- machine cible : `db-layer`
- parent : `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`

## But

Stabiliser le Gateway OpenClaw sur `db-layer` via une supervision `tmux` bornee, sous utilisateur `openclaw`, en loopback only.

## 7_CANONICAL_STATE

- precondition documentaire : PR #212 mergee dans `sot/mainline`
- parent realigne : `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`
- machine cible unique : `db-layer`
- mode de supervision autorise : `tmux` uniquement
- runtime interdit tant que le cadrage n'est pas valide en lecture

## Objectif Exact

Ce child doit cadrer une supervision minimale et controlee du Gateway OpenClaw afin de pouvoir, dans une passe suivante seulement, verifier un demarrage, un arret et une reprise via `tmux` sans passer par un service `systemd` durable et sans ouvrir de bridge runtime.

## ETABLI

- ce child n'existait pas dans le repo au moment du realignement documentaire
- son ouverture vient du plan `11_NEXT_GO_SEQUENCE_AND_IDE_BUNDLE_PLAN.md` du parent OpenClaw
- aucun changement runtime n'est inclus dans ce squelette
- le parent documente deja un usage cible `openclaw@db-layer`, une session `openclaw-gateway` et un bind `127.0.0.1:18789`

## HYPOTHESE

- une supervision `tmux` suffit pour la premiere stabilisation locale
- la session cible peut rester `openclaw-gateway`
- le runtime devra rester borne a `127.0.0.1:18789` pendant toute la phase initiale
- `systemd --user` peut rester hors scope si `tmux` couvre le besoin operatoire immediat

## Perimetre

- cadrage tmux session `openclaw-gateway`
- scripts `start/status/stop` documentes
- verification loopback `127.0.0.1:18789`
- definition des preuves minimales de demarrage / arret / reprise
- commandes de verification lecture-seulement
- aucun bridge V1 tant que la supervision tmux n'est pas validee

## Hors Perimetre

- bridge OpenClaw
- policy runtime large
- exposition WAN
- admin-trading
- systemd durable dans cette passe d'ouverture
- toute modification du runtime trading
- toute execution OpenClaw avant validation du cadrage

## Commandes Audit-Only

Commandes autorisees pour la future passe operatoire, en lecture d'abord :

```bash
cd /opt/trading
bash modules/gateway_openclaw/scripts/cmd.sh status
bash modules/gateway_openclaw/scripts/cmd.sh paths
tmux ls
ss -ltnp | grep 18789 || true
ps -ef | grep -i '[o]penclaw' || true
```

Ces commandes servent uniquement a qualifier l'etat reel avant toute tentative de demarrage.

## Criteres PASS / FAIL

### PASS cadrage

- objectif tmux borne et comprehensible
- session cible, utilisateur cible et bind cible explicitement fixes
- commandes audit-only explicites
- sequence `start/status/stop` definie sans ambiguite
- rollback minimal documente
- preuves attendues explicites

### FAIL cadrage

- ambiguite entre `tmux` et `systemd`
- ambiguite sur l'utilisateur runtime vise
- absence de bornage loopback
- absence de procedure d'arret / reprise
- ouverture prematuree vers bridge, WAN ou `admin-trading`

## Stop / Rollback

Le futur lot operatoire devra prevoir au minimum :

- arret propre de la session `tmux` cible
- verification que le port `18789` n'ecoute plus si l'arret est demande
- retour a l'etat initial sans changement persistant de service systeme
- journalisation de toute action de demarrage/arret

## Preuves Attendues

Preuves minimales a exiger dans la future passe operatoire :

- nom exact de la session `tmux`
- utilisateur effectif du processus
- sortie `status`
- presence ou absence du listener `127.0.0.1:18789`
- preuve d'arret propre
- preuve de reprise propre
- classification finale : `PASS`, `PARTIAL`, ou `FAIL`

## TODO

1. completer si besoin la sequence documentaire `start/status/stop`
2. confirmer le contrat de preuve minimal du lot operatoire
3. garder toute execution OpenClaw hors de ce lot tant que le cadrage n'est pas juge PASS

## NEXT_GO

Point de reprise suivant : valider ce cadrage, puis ouvrir une passe operatoire controlee de supervision `tmux` sur `db-layer`, toujours sans bridge runtime.

## RISKS

- À qualifier.
