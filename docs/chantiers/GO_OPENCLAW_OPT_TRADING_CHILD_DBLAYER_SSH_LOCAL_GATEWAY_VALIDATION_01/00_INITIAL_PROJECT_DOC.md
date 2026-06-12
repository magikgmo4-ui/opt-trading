---
doc_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: openclaw_operator_bridge
go_id: GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01
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
  - gateway_v2
  - orchestrateur
  - dry_run
reference_canonique_principale: docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Section NEXT_GO"
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/REPRISE_DB_LAYER_20260505.md
  - docs/index/inbox/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/03_REMOTE_EXEC_STATE.md
  - docs/index/GO_INDEX.md
---

# GO_OPENCLAW_OPT_TRADING_CHILD_DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_01

## Classification

- type : child validation gate
- statut : open
- parent : `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`
- poste operateur : `fantome`
- machine cible unique : `db-layer`
- transport autorise : `SSH` controle
- mode d'execution vise : shell local `db-layer`

## But

Ouvrir une validation explicite `fantome -> SSH -> db-layer` afin de verifier `OpenClaw` localement sur `db-layer`, sans reclasser cette sequence en faux "local" cote `fantome`.

## 9_SELECTED_SOLUTION

```text
db-layer local via session SSH controlee
-> validation SSH gate minimale
-> verification CLI/Gateway localement sur db-layer
-> verification orchestrateur localement
-> dry-run builder local db-layer
```

## 13_ESTABLISHED

Techniquement, une commande lancee apres `ssh db-layer` s'execute bien sur `db-layer`.

Le verrou de gouvernance ne porte pas seulement sur l'endroit ou tourne le processus, mais aussi sur le transport `SSH` et le controle remote depuis `fantome`.

| Cas | Statut |
| --- | --- |
| session terminal directe sur `db-layer` | `local db-layer` |
| `fantome -> ssh db-layer "commande"` | `remote exec depuis fantome` |
| `fantome -> ssh db-layer`, puis travail dans le shell distant | `hybride : transport SSH, execution locale db-layer` |

## 7_CANONICAL_STATE

- `fantome` reste le poste operateur
- `db-layer` reste la vraie cible `OpenClaw` / orchestrateur
- `SSH` est assume comme surface gouvernee et non masque sous l'etiquette `local`
- aucune installation `openclaw` sur `fantome`
- aucune commande remote destructive
- aucun secret
- aucun live trading
- aucun write libre
- aucun `sudo`
- aucune installation sans approval humain explicite

## Verification locale attendue sur `db-layer`

1. verifier `hostname` et l'identite machine
2. verifier la presence du repo `opt-trading`
3. verifier `git status`
4. verifier la presence du CLI `openclaw`
5. verifier `Gateway V2`
6. verifier l'orchestrateur `OpenClaw`
7. lancer un dry-run builder local uniquement

## Regle de stop

Si le CLI `openclaw` est absent sur `db-layer` :

```text
NEEDS_APPROVAL_INSTALL_DB_LAYER
```

Actions obligatoires :

1. afficher la commande exacte retenue pour l'installation
2. demander un approval humain explicite
3. stopper avant toute installation

## Livrables

- `00_INITIAL_PROJECT_DOC.md`
- `DBLAYER_SSH_LOCAL_GATEWAY_VALIDATION_REPORT_01.md`
- `90_CLOSEOUT.md`

## Hors Perimetre

- installation `openclaw` sur `fantome`
- WAN libre
- secrets
- live trading
- write non borne
- `sudo`
- installation automatique
- remediation runtime hors dry-run local

## NEXT_GO

Executer la passe SSH/local `db-layer` strictement dans ce cadre, puis completer le rapport et le closeout avec verdict `PASS`, `FAIL` ou `NEEDS_APPROVAL_INSTALL_DB_LAYER`.

## RISKS

- À qualifier.
