---
doc_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01
status: open
lifecycle_stage: cadrage_execution_future
topic_keys:
  - opt-trading
  - reseau_ssh
  - runtime
  - compat
  - retirement
  - rollback
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/status/reseau_ssh_canonique.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/10_step_09_execution_resultats.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CANONICAL_RENAME_REGISTRY_01/01_plan_operationnel_step_by_step.md
---

# GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01 - Cadrage

## Objet

Ouvrir le lot borne de reduction de compatibilite apres migration reussie des alias courts `reseau_ssh`.

Ce lot ne vise plus la bascule machine-side.

Il vise maintenant :
- la sortie progressive de `scripts/reseau_ssh` du flux actif
- la prevention de toute republication legacy des alias courts
- la qualification des wrappers racine et des callers residuels avant retrait ou archivage

## Etat de depart retenu

Etat canonique actuel :
- module canonique final : `modules/reseau_ssh`
- implementation interne : `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2`
- transition utile : `modules/reseau_ssh_step1b`
- compat runtime restante : `scripts/reseau_ssh`
- archive historique : `_archive/legacy_modules/reseau_ssh_step1`

Etat machine-side prouve :
- `db-layer` : alias courts -> `modules/reseau_ssh/scripts/*` avec `PASS`
- `admin-trading` : alias courts -> `modules/reseau_ssh/scripts/*` avec `PASS`
- `student` : alias courts -> `modules/reseau_ssh/scripts/*` avec `PASS`
- `fantome` : alias courts -> `modules/reseau_ssh/scripts/*` avec `PASS`

Conclusion :
- `scripts/reseau_ssh` n'est plus requis comme point d'entree court sur les 4 hotes cibles
- il reste seulement comme surface de compatibilite, de rollback et de derive potentielle si son installeur legacy est rejoue

## Risque principal

Le principal risque repo-side n'est plus un symlink machine-side.

Le principal risque est la republication accidentelle des alias courts vers le backend legacy via :
- `scripts/reseau_ssh/install_reseau_ssh.sh`

## Perimetre de ce lot

Dans le perimetre :
- `scripts/reseau_ssh/`
- wrappers racine historiques `scripts/reseau_ssh_cmd.sh` et `scripts/reseau_ssh_menu.sh`
- readmes et docs de statut associes
- preparation du bundle Git futur

Hors perimetre de cette premiere passe :
- retrait de `modules/reseau_ssh_step1b`
- retrait des alias suffixes `*_reseau_ssh_step2`
- nettoyage distant des copies rollback sur les machines
- archivage physique immediat de `scripts/reseau_ssh`

## Strategie retenue

La reduction de compatibilite se fait en deux temps :

1. garde-fou repo-side
   - empecher que `install_reseau_ssh.sh` republie les alias courts vers `scripts/reseau_ssh`
2. qualification avant retrait
   - prouver qu'aucun caller repo-side critique ne depend encore des wrappers legacy
   - decider ensuite entre maintien rollback-only ou archivage

## Point de reprise

Le lot de bascule machine-side est termine.

Le prochain point de reprise est :
- audit des surfaces residuelles dans `scripts/reseau_ssh`
- qualification des wrappers racine
- preparation des commits et de la PR sans execution Git

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
