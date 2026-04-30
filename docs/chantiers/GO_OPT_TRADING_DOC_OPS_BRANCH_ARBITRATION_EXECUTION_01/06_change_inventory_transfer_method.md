---
doc_id: GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01_CHANGE_INVENTORY_TRANSFER_METHOD
doc_type: method_consolidation
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01
status: reference
lifecycle_stage: post_closeout_consolidation
topic_keys:
  - opt-trading
  - doc_ops
  - git
  - branch_arbitration
  - change_inventory
  - cherry_pick
  - selective_transfer
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/01_branch_proof_matrix.md
point_de_reprise: docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/COMMIT_TRANSFER_INVENTORY.md
updated_at: 2026-04-30
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/01_branch_proof_matrix.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/02_execution_plan.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/03_execution_report.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/90_closeout.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/COMMIT_TRANSFER_INVENTORY.md
---

# 06_change_inventory_transfer_method

## 1_MASTER_TARGET

Consolider la méthode Git utilisée par `GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01` : lister les changements au fil du chantier, puis intégrer seulement les deltas validés au lieu de merger aveuglément une branche qui a divergé.

## 3_INITIAL_NEED

Le problème à éviter : plusieurs machines ou chantiers avancent en parallèle, des fichiers communs évoluent, puis un merge tardif importe trop de choses et provoque des conflits ou des régressions documentaires.

La solution : maintenir un inventaire vivant des changements pendant le chantier.

## 7_CANONICAL_STATE

### ETABLI

Le GO existant prouve déjà les principes suivants :

- comparer la branche au canon `sot/mainline` ;
- lister `ahead_by`, `behind_by`, fichiers en avance et décision provisoire ;
- ne pas merger une branche divergée sans revue ;
- autoriser l'import sélectif ou `cherry-pick` seulement après review ;
- ne pas importer aveuglément les index globaux anciens.

### AJOUT_CONSOLIDE

Pour les prochains chantiers similaires, l'inventaire ne doit pas être reconstruit seulement à la fin. Il doit être alimenté au fil de l'eau dans :

`docs/chantiers/<GO_ID>/COMMIT_TRANSFER_INVENTORY.md`

## 8_VALIDATED_PLAN

### Étape 1 — au démarrage du chantier

Créer ou initialiser :

```text
COMMIT_TRANSFER_INVENTORY.md
```

Renseigner :

- branche chantier ;
- base canonique ;
- machine owner ;
- objectif local ;
- fichiers sensibles connus ;
- index globaux à éviter en import aveugle.

### Étape 2 — à chaque commit significatif

Lister immédiatement :

```powershell
git log --oneline -1
git show --name-status --stat --oneline HEAD
```

Puis ajouter une ligne dans `TABLEAU_CHANGEMENTS` avec :

- commit ;
- type ;
- fichiers touchés ;
- portée ;
- risque conflit ;
- mode de transfert recommandé ;
- statut.

### Étape 3 — avant intégration

Comparer au canon :

```powershell
git fetch origin --prune
git rev-list --left-right --count origin/sot/mainline...HEAD
git log --oneline --right-only origin/sot/mainline...HEAD
git diff --name-status origin/sot/mainline...HEAD
git diff --stat origin/sot/mainline...HEAD
```

### Étape 4 — intégrer seulement le delta validé

Choisir une action par changement :

| Cas | Action |
| --- | --- |
| commit propre, récent, isolé | `cherry-pick -n` puis inspection |
| fichier utile unique | import fichier par fichier |
| patch lisible mais commit mélangé | patch contrôlé ou réécriture propre |
| index global ancien | refaire manuellement sur base actuelle |
| branche trop divergée | ne pas merger ; garder référence ou ouvrir GO d'import |
| doute | bloquer et documenter |

### Étape 5 — push/rebase propre

Après transfert validé :

```powershell
git fetch origin --prune
git rebase origin/sot/mainline
git push origin HEAD
```

Si un push forcé devient nécessaire après rebase :

```powershell
git push --force-with-lease origin HEAD
```

## 12_INVARIANTS

- Ne pas merger une branche divergée seulement parce qu'elle contient un fichier utile.
- Ne pas importer aveuglément `GO_INDEX.md`, `ACTIVE_STREAMS.md`, `NEXT_GO_CANDIDATES.md`, `REPRISE.md` ou `BRANCH_STATE.md` depuis une vieille branche.
- Garder les index globaux comme surfaces d'état courant, pas comme payload de cherry-pick automatique.
- Préférer `cherry-pick -n`, import fichier par fichier ou patch contrôlé quand d'autres fichiers ont avancé.
- Un transfert n'est validé qu'après lecture du diff et statut propre.

## 16_TODO

- Utiliser `COMMIT_TRANSFER_INVENTORY.md` dans les prochains chantiers multi-machine ou à risque de divergence.
- Reporter les décisions `TRANSFER_OK`, `REWRITE_REQUIRED`, `INDEX_REDO_REQUIRED`, `BLOCKED`, `DROP` au fil de l'eau.
- Fermer le chantier seulement si l'inventaire permet de rejouer ou d'abandonner proprement chaque changement.

## 17_RESUME_POINT

Pour reprendre la méthode :

```powershell
cd C:\Users\ghost\opt-trading
git fetch origin --prune
git checkout <branche_chantier>
git status --short --branch
git rev-list --left-right --count origin/sot/mainline...HEAD
```

Puis lire :

```text
docs/chantiers/<GO_ID>/COMMIT_TRANSFER_INVENTORY.md
```

## 19_TO_REMEMBER

Memory Bricks projet :

- `CHANGE_INVENTORY_BEFORE_BRANCH_INTEGRATION`
- `LIST_COMMITS_DURING_CHANTIER_NOT_ONLY_AT_CLOSEOUT`
- `SELECTIVE_TRANSFER_BEATS_BLIND_MERGE_FOR_DIVERGED_BRANCHES`
- `OLD_GLOBAL_INDEXES_MUST_BE_REDONE_NOT_IMPORTED_BLINDLY`
