---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01_REPRISE_ETAT_SUITE
doc_type: chantier_reprise
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01
status: open
lifecycle_stage: reprise
topic_keys:
  - opt-trading
  - doc_ops
  - branch_cleanup
  - housekeeping
  - continuity
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md
point_de_reprise: "17_RESUME_POINT"
updated_at: 2026-04-24
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md
  - docs/index/BRANCH_STATE.md
  - docs/index/GO_INDEX.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/01_cadrage_parent.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md
---

# GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01 — reprise, état et suite

## 1_MASTER_TARGET

Nettoyer et qualifier les branches restantes de `opt-trading` sans suppression aveugle, en partant de l’état réel Git, de la matrice doc ops, de `GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01` et de `BRANCH_STATE.md`.

## 2_INITIAL_PROJECT_DOC

Documents de référence :

- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/01_cadrage_parent.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md`
- `docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md`
- `docs/index/BRANCH_STATE.md`

## 3_INITIAL_NEED

Reprendre le cleanup des branches restantes sans dépendre de la session, en documentant clairement :

- l’état prouvé ;
- le stash local à vérifier ;
- la branche dédiée existante ;
- la suite opératoire ;
- les limites entre preuve GitHub et preuve locale.

## 4_MASTER_PROJECT_PLAN

Le parent `GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01` fixe la séquence :

1. hygiène Git / branches / supports ouverts ;
2. contrôle des chantiers ouverts / non terminés ;
3. reprise d’un seul flux principal ;
4. carte cible future des parents projet / machine ;
5. ouverture canonique future des parents spécialisés ;
6. audit final de conformité.

Ce sous-GO couvre uniquement l’étape 1.

## 5_GO_PLAN

Sous-GO actif :

- `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01`

But :

- reprendre le classement des branches restantes ;
- traiter les branches encore `A_VERIFIER` ;
- conserver les branches de référence et de secours ;
- ne supprimer que les branches qui satisfont strictement la méthode canonique.

## 6_FINAL_TARGET

Livrable attendu :

- tableau branch-by-branch mis à jour ;
- décision explicite pour chaque branche restante ;
- trace de toute suppression réellement exécutée ;
- mise à jour de `docs/index/BRANCH_STATE.md` si changement réel ;
- closeout du sous-lot avant passage à `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`.

## 7_CANONICAL_STATE

### ETABLI_GITHUB

- Branche dédiée existante : `codex/doc-ops-child-branch-cleanup-01`.
- Avant reprise locale, la branche était behind-only :
  - `ahead_by = 0`
  - `behind_by = 8`
- Les écritures GitHub directes précédentes n’ont pas confirmé de création de fichier.

### ETABLI_LOCAL

- Worktree initial non propre.
- Dossier non suivi initial déplacé hors repo et archivé localement (voir Étape 2).
- stash local présent: `stash@{0}` touchant 6 fichiers (voir Étape 2).
- Le stash n’a pas été appliqué ni supprimé.

### ETABLI_REPO_DOC

- Le parent et le sous-GO existent et sont référencés dans BRANCH_STATE.md.
- BRANCH_STATE.md indique 33 entrées `A_VERIFIER` à qualifier.

## 8_VALIDATED_PLAN

Ordre de reprise :

1. vérifier `git status` ;
2. vérifier `git stash list` ;
3. inspecter le stash si présent ;
4. vérifier la branche courante ;
5. réaligner la branche sur `origin/sot/mainline` si le worktree le permet ;
6. relire `BRANCH_STATE.md` ;
7. traiter les branches `A_VERIFIER` une par une ;
8. ne supprimer aucune branche sans preuve ;
9. journaliser toute suppression réelle ;
10. mettre à jour `BRANCH_STATE.md` ;
11. fermer le sous-lot ou transférer vers `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`.

## 9_SELECTED_SOLUTION

- continuer sur `codex/doc-ops-child-branch-cleanup-01` ;
- documenter l’état réel et la suite dans le dossier du sous-GO ;
- garder la preuve locale comme arbitre pour le stash et les branches locales ;
- ne pas inventer d’état Git depuis GitHub lorsque l’opération n’a pas confirmé.

## 10_SELECTED_SETUP

Branche de travail :

- `codex/doc-ops-child-branch-cleanup-01`

Base canonique :

- `sot/mainline`

Fichiers centraux :

- `docs/index/BRANCH_STATE.md`
- `docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01/00_reprise_etat_suite.md`

## 11_KEY_DECISIONS

- Aucun nouveau parent nécessaire ; l’équivalent existe déjà.
- Aucune suppression de branche dans cette passe.
- Le stash local reste intact et n’est pas appliqué.
- L’untracked est archivé hors repo, non supprimé.
- La branche `codex/doc-ops-child-branch-cleanup-01` reste la branche de reprise.
- Le prochain GO après cleanup reste `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`.

## 12_INVARIANTS

- `sot/mainline` reste la base canonique.
- `BRANCH_STATE.md` est la surface canonique pour l’état du parc branches.
- `GO_INDEX.md` reste la vérité de liste des chantiers non clos.
- `GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md` gouverne la méthode de ménage des branches.
- Une branche n’est supprimable que si elle absorbée, non active, non utile à la reprise, et sans valeur documentaire résiduelle.
- Les familles `backup/*`, `rescue/*`, `save/*`, `audit/*`, `inventory/*`, `integ/*` et branches autour de `GO_*` exigent revue manuelle.
- Ne pas négliger le stash.

## 13_ESTABLISHED

- Le chantier parent existe.
- La branche dédiée existe.
- Le sous-GO est référencé dans le plan parent.
- BRANCH_STATE.md contient une photo du parc branches.
- Il reste des branches `A_VERIFIER` à qualifier.

## 14_HYPOTHESIS

- Le stash local contient probablement des éléments pertinents pour le parent.
- Certaines branches `A_VERIFIER` pourraient être supprimables, mais uniquement après audit.
- Le dossier d’archive hors repo peut être repris plus tard dans un GO séparé s’il correspond à `GO_OPT_TRADING_RESEAU_SHARE_TRANSFER_CONSOLIDATION_01`.

## 15_REMAINING_GAP

À résoudre après reprise :
- décision sur le stash parent ;
- qualification des branches `A_VERIFIER` ;
- mise à jour éventuelle de `BRANCH_STATE.md` ;
- closeout du sous-GO de cleanup.

## 16_TODO

1. Committer ce fichier de reprise;
2. Pousser la branche;
3. Reprendre ensuite l’audit des branches `A_VERIFIER`;
4. Ne supprimer que les branches validées selon la méthode canonique;
5. Produire le closeout.

## 17_RESUME_POINT

Reprise opérationnelle suivante :

1. ouvrir `codex/doc-ops-child-branch-cleanup-01` ;
2. vérifier `git stash list` ;
3. vérifier `docs/index/BRANCH_STATE.md` ;
4. reprendre les branches `A_VERIFIER` une par une ;
5. documenter les décisions ;
6. mettre à jour `BRANCH_STATE.md` ;
7. produire le closeout du sous-GO ;
8. passer à `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`.

## 18_TO_DOCUMENT

TAGS :

- `GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01`
- `BRANCH_STATE`
- `LOCAL_STASH_A_VERIFIER`
- `UNTRACKED_ARCHIVED`
- `GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01`

Blocs à extraire :

- `7_CANONICAL_STATE`
- `11_KEY_DECISIONS`
- `16_TODO`
- `17_RESUME_POINT`

## 19_TO_REMEMBER

Memory Bricks projet :

- `BRANCH_CLEANUP_CONTINUES_ON_CODEX_DOC_OPS_CHILD_BRANCH_CLEANUP_01`
- `LOCAL_STASH_MUST_BE_CHECKED_BEFORE_BRANCH_CLEANUP_CLOSEOUT`
- `UPDATE_REF_NOT_CONFIRMED_BY_GITHUB_CONNECTOR_DO_NOT_ASSUME_FAST_FORWARD`

## RISKS

- À qualifier.
