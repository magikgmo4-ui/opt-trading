---
doc_type: chantier
go_id: GO_GIT_BACKUP_MAIN_BEFORE_FILTER_ARBITRATION_01
status: pass
repo: opt-trading
updated_at: 2026-04-20
links:
  - docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md
  - docs/chantiers/GO_GIT_KEEP_REFERENCE_CANON_CLOSEOUT_01/03_decisions.md
  - docs/chantiers/GO_GIT_BACKUP_MAIN_BEFORE_FILTER_ARBITRATION_01/03_decisions.md
---

# GO_GIT_BACKUP_MAIN_BEFORE_FILTER_ARBITRATION_01

## Objet

Arbitrer le statut final de `backup/main-before-filter` a partir de l'etat Git reel, sans suppression de branche et sans melanger ce passage avec le lot `ABSORBED`.

## Cible

Traiter uniquement :

- `origin/backup/main-before-filter`

## ETABLI

- la base operatoire de comparaison reste `origin/sot/mainline`
- la branche cible est remote-only : aucune branche locale `backup/main-before-filter` n'est presente, seule la ref `origin/backup/main-before-filter` est observee
- `origin/backup/main-before-filter` est un ancetre pur de `origin/main`
- `origin/backup/main-before-filter` est un ancetre pur de `origin/sot/mainline`
- le comptage de divergence contre `origin/sot/mainline` est `835 0`, ce qui confirme l'absence de commit propre hors canon actuel
- la branche apparait deja dans les branches distantes merged dans `origin/sot/mainline`
- aucune reference canonique active a cette branche n'a ete identifiee dans la doc repo, hors traces de bundle et mention d'upload d'archive dans `journal.md`

## TODO

- ne faire aucune suppression de branche dans ce GO
- conserver une suppression eventuelle dans un passage Git distinct
- ne pas melanger cette branche avec `GO_GIT_BRANCH_DROP_SAFE_ABSORBED_01`

## REPRISE

- base Git : `origin/sot/mainline`
- methode : `docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md`
- decision detaillee : `docs/chantiers/GO_GIT_BACKUP_MAIN_BEFORE_FILTER_ARBITRATION_01/03_decisions.md`

## VERDICT

- PASS - `backup/main-before-filter` sort en `DROP_REMOTE_CANDIDATE` sans suppression effectuee dans ce passage
