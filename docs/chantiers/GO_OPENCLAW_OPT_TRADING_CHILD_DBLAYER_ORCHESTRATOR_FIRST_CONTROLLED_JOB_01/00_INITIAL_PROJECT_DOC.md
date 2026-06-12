---
doc_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01
parent_go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
status: open
lifecycle_stage: cadrage
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-18
topic_keys:
  - openclaw
  - db-layer
  - ssh
  - orchestrator
  - first_job
  - controlled_job
reference_canonique_principale: docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Section 7_CANONICAL_STATE"
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01/90_CLOSEOUT.md
  - docs/index/GO_INDEX.md
---

# GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01

## Classification

- type : child orchestrator first controlled job
- statut : open
- parent : `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`
- poste operateur : `fantome`
- machine cible unique : `db-layer`
- transport autorise : `SSH` controle (valide GO precedent)
- mode d'execution : shell local `db-layer` via `fantome -> SSH`

## But

Lancer un premier job orchestrateur OpenClaw controle sur `db-layer`, en verifiant que le job passe correctement par le CLI `openclaw`, la Gateway V2, et l'orchestrateur `desk_pro_orchestrator`. Rester non-trading, dry-run/read-only par defaut.

## 7_CANONICAL_STATE

```text
fantome = poste operateur
db-layer = cible OpenClaw validee
SSH = transport controle valide
OpenClaw db-layer = CLI + Gateway V2 + orchestrateur presents
Mode = non-trading, dry-run/read-only
```

## Verification pre-execution

1. `sot/mainline` propre au merge SHA `75f416e6`+
2. SSH `db-layer` joignable depuis `fantome`
3. `hostname`, `pwd`, `git status` cote `db-layer`
4. `openclaw --version` ou equivalent
5. Definir la commande exacte du job controle
6. Valider que la commande est read-only / dry-run

## Plan d'execution

1. Verifier SSH + identite machine `db-layer`
2. Verifier repo opt-trading + git status
3. Verifier CLI openclaw + Gateway V2 + orchestrateur
4. Decrire la commande du job controle (dry-run / read-only)
5. Executer le job via CLI openclaw
6. Capturer les traces et sorties
7. Verifier l'etat apres execution (clean)

## Regles de stop

- CLI `openclaw` absent sur `db-layer` : `NEEDS_APPROVAL_INSTALL_DB_LAYER`
- write non prevu : STOP
- secret : STOP
- live trading : STOP
- sudo : STOP
- commande non prevue dans le plan : STOP

## Livrables

- `00_INITIAL_PROJECT_DOC.md`
- `DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_PLAN_01.md`
- `DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_REPORT_01.md`
- `90_CLOSEOUT.md`

## Hors Perimetre

- installation `openclaw` sur `fantome`
- secret
- live trading
- write non borne
- `sudo`
- installation automatique
- remediation runtime hors dry-run

## RISKS

- À qualifier.
