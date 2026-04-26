---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_ARCHIVE_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_ARCHIVE_01
status: open
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - step1b
  - archive
surface: docs
source_kind: canonical
updated_at: 2026-04-25
links:
  - _archive/legacy_modules/reseau_ssh_step1b/README.md
  - modules/reseau_ssh/README.md
  - docs/status/reseau_ssh_canonique.md
---

# GO_OPT_TRADING_RESEAU_SSH_STEP1B_ARCHIVE_01 - Cadrage

## Objet

Sortir `modules/reseau_ssh_step1b` du flux actif du repo et le basculer en archive repo-side.

Le lot ne nettoie pas les copies machine-side. Il borne seulement l'etat canonique du repo.

## Etat de depart

- les commandes `baseline-*` du canonique ne deleguent plus vers `step1b`
- plus aucun alias `step1b` n'est publie sur `db-layer`, `admin-trading`, `student`, `fantome`
- `step1b` ne porte plus qu'un historique de helpers non publies

## Cible

- move repo-side vers `_archive/legacy_modules/reseau_ssh_step1b/`
- suppression des pointeurs actifs restants vers `modules/reseau_ssh_step1b`
- realignement des docs actives de continuite

## Target
1 module canonique par famille.
