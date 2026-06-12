---
doc_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01
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
  - runbook
  - operational
reference_canonique_principale: docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Section 7_CANONICAL_STATE"
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_FIRST_CONTROLLED_JOB_01/90_CLOSEOUT.md
  - docs/index/inbox/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01.md
  - docs/index/GO_INDEX.md
---

# GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_OPERATIONAL_RUNBOOK_01

## Classification

- type : child runbook operationnel
- statut : open
- parent : `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`
- poste operateur : `fantome`
- machine cible unique : `db-layer`
- transport autorise : `SSH` controle uniquement
- mode d'usage vise : usage operationnel borne du runbook, non-trading

## But

Figurer le mode d'usage operationnel valide de l'orchestrateur OpenClaw sur `db-layer`, en restant strictement dans le cadre verifie par le GO #553 : non-trading, dry-run/read-only par defaut, aucun secret, aucun sudo, aucun write libre.

## 7_CANONICAL_STATE

```text
fantome = poste operateur
db-layer = cible OpenClaw validee
SSH = transport controle valide
OpenClaw db-layer = premier job orchestrateur controle MERGED / PASS
runbook = reference d'usage operationnel sans extension runtime
```

## Prechecks db-layer

1. verifier que `sot/mainline` est au moins au SHA `ef0c6af0`
2. verifier que `ssh db-layer` fonctionne
3. verifier `hostname`, `pwd`, `git status` cote `db-layer`
4. verifier `openclaw --version`
5. verifier que `modules/desk_pro_orchestrator/` est present
6. verifier que la sortie reste dans `data/desk_runs/`

## Commandes autorisees

```text
ssh db-layer "..."
cd /home/ghost/opt-trading && python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator status
cd /home/ghost/opt-trading && python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator explain
cd /home/ghost/opt-trading && python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator sample-run
cd /home/ghost/opt-trading && python3 -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator run --config <config_read_only>
git status
git diff
git log --oneline -1
```

## Commandes interdites

```text
sudo
rm -rf
chmod -R
chown -R
git add autonome
git commit autonome
git push autonome
live trading
secret access
write hors `data/desk_runs/`
commande non prevue dans le runbook
```

## Procedure dry-run / read-only

1. ouvrir la session SSH controlee vers `db-layer`
2. valider l'identite machine et le repo
3. lancer `status`
4. lancer `explain`
5. lancer `sample-run` ou un `run --config` explicitement PAPER/read-only
6. verifier les traces, le `run_summary.json`, et le `git status`

## Logs et preuves attendues

- sortie `status`
- sortie `explain`
- sortie `sample-run` ou `run`
- `data/desk_runs/<run_id>/run_summary.json`
- fichiers module JSON sous le run dir
- `git status` propre avant et apres

## Stop conditions

- CLI `openclaw` absent : `NEEDS_APPROVAL_INSTALL_DB_LAYER`
- secret detecte : STOP
- live trading detecte : STOP
- sudo requis : STOP
- write non borne requis : STOP
- effet de bord hors `data/desk_runs/` : STOP

## Conditions avant futur write-gated ou job plus large

1. runbook approuve comme reference de base
2. controls read-only repetables
3. preuves de clean status pre et post
4. no secrets / no live / no sudo maintenus
5. nouveau GO explicite pour tout write-gated ou perimetre plus large

## RISKS

- À qualifier.
