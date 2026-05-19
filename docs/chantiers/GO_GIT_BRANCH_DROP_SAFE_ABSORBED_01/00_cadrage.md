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
- les sept branches ciblees existaient sur `origin` avant execution
- les sept branches ciblees etaient deja absorbees dans `origin/sot/mainline` avant execution
- les sept suppressions remote ont ete executees puis confirmees apres `git fetch origin --prune`
- aucune suppression locale n'a ete retenue dans ce passage
- `feat/student-validation-bitget-readonly-01` reste differee en local car la branche est montee dans le worktree `/tmp/opt-trading-consolidate-validated-extracts-01`
- `backup/main-before-filter` reste explicitement hors perimetre de ce GO
- `origin/doc/GO_OPENCLAW_STATE_DIR_READ_09` a ete observee pendant le `fetch --prune` et doit etre traitee comme sujet separe hors perimetre

## RESULTAT D'EXECUTION

- suppressions remote effectuees pour les sept branches du lot valide
- verification post-prune effectuee : les sept refs ne reapparaissent plus dans `git branch -r`
- garde locale maintenue sur `feat/student-validation-bitget-readonly-01`
- separation de perimetre respectee pour `backup/main-before-filter`
- nouvelle branche distante detectee hors perimetre : `origin/doc/GO_OPENCLAW_STATE_DIR_READ_09`

## REPRISE

- base Git : `origin/sot/mainline`
- methode : `docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md`
- decision detaillee : `docs/chantiers/GO_GIT_BRANCH_DROP_SAFE_ABSORBED_01/03_decisions.md`

## VERDICT

- PASS - le lot remote cible est supprime en restant strictement separe des suppressions locales et de `backup/main-before-filter`
