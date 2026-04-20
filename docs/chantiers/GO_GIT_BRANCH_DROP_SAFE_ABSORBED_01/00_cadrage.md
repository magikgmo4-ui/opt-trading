---
doc_type: chantier
go_id: GO_GIT_BRANCH_DROP_SAFE_ABSORBED_01
status: pass
repo: opt-trading
updated_at: 2026-04-20
links:
  - docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md
  - docs/chantiers/GO_GIT_BACKUP_MAIN_BEFORE_FILTER_ARBITRATION_01/03_decisions.md
  - docs/chantiers/GO_GIT_BRANCH_DROP_SAFE_ABSORBED_01/03_decisions.md
---

# GO_GIT_BRANCH_DROP_SAFE_ABSORBED_01

## Objet

Preparar un passage de suppression remote safe pour un lot strict de branches deja absorbees dans `origin/sot/mainline`, sans suppression locale dans ce GO.

## Cible

Traiter uniquement :

- `feat/GO_OPT_TRADING_GO_INDEX_CLOSED_ENTRIES_CANON_01`
- `feat/project-card-deskpro-01`
- `feat/reseau-ssh-consolidation-lot2-freeze-01`
- `feat/reseau-ssh-consolidation-lot3-minimal-01`
- `feat/student-validation-bitget-readonly-01`
- `feat/workflow-post-change-consolidation-03`
- `fix/collectors-lifecycle-compat-relref-01b`

## ETABLI

- la base operatoire de comparaison reste `origin/sot/mainline`
- les sept branches ciblees existent sur `origin`
- les sept branches ciblees sont deja absorbees dans `origin/sot/mainline`
- aucune suppression locale n'est retenue dans ce passage
- `feat/student-validation-bitget-readonly-01` reste differee en local car la branche est montee dans le worktree `/tmp/opt-trading-consolidate-validated-extracts-01`
- `backup/main-before-filter` reste explicitement hors perimetre de ce GO

## TODO

- supprimer uniquement les refs distantes du lot valide
- executer un `fetch --prune` apres suppression remote
- verifier l'absence post-prune des sept refs distantes
- ne pas melanger ce passage avec une suppression locale differee

## REPRISE

- base Git : `origin/sot/mainline`
- methode : `docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md`
- decision detaillee : `docs/chantiers/GO_GIT_BRANCH_DROP_SAFE_ABSORBED_01/03_decisions.md`

## VERDICT

- PASS - le lot remote cible est supprime en restant strictement separe des suppressions locales et de `backup/main-before-filter`
