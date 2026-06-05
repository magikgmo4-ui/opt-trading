---
doc_id: GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01_COMMIT_TRANSFER_INVENTORY
doc_type: method_consolidation
repo: opt-trading
project: opt-trading
module:
  go_id: GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01
status: reference
lifecycle_stage: consolidation
topic_keys:
  - opt-trading
  - doc_ops
  - branch_arbitration
  - commit_inventory
  - selective_transfer
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/01_branch_proof_matrix.md
point_de_reprise: "17_RESUME_POINT"
updated_at: 2026-04-30
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/01_branch_proof_matrix.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/03_execution_report.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/90_closeout.md
---

# 06_commit_transfer_inventory

## 1_MASTER_TARGET

Consolider la methode d'integration Git par inventaire vivant des changements: lister les commits, fichiers touches, risques et mode de transfert recommande au fil du chantier, puis integrer uniquement les changements valides au lieu de merger aveuglement une branche entiere.

## 2_INITIAL_PROJECT_DOC

Reference canonique principale:

- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/01_branch_proof_matrix.md`

References d'execution:

- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/03_execution_report.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01/90_closeout.md`

## 3_INITIAL_NEED

Eviter les conflits Git dans un contexte multi-chantiers et multi-machines lorsque plusieurs fichiers ou index avancent en parallele.

Le besoin est de ne plus attendre la fin d'une branche pour reconstruire le delta. Le chantier doit produire son inventaire de transfert au fil de l'eau.

## 4_MASTER_PROJECT_PLAN

Principe retenu:

1. chaque chantier conserve ses commits sur sa branche dediee ou son support Git retenu;
2. chaque commit significatif est inscrit dans un inventaire local du chantier;
3. l'inventaire qualifie les fichiers touches, le risque de conflit et le mode de transfert recommande;
4. l'integration finale ne merge pas necessairement la branche entiere;
5. l'integration reprend seulement les changements valides via cherry-pick preview, import fichier, patch controle, rebase ou merge si la branche est propre.

## 5_GO_PLAN

Le present GO avait deja prouve la logique suivante:

- lister branches candidates;
- mesurer statut vs `sot/mainline`;
- relever `ahead_by`, `behind_by` et fichiers en avance;
- classer les decisions avant execution;
- interdire merge/cherry-pick/import tant que la revue n'est pas faite.

Cette consolidation ajoute la variante au fil de l'eau: l'inventaire est maintenu pendant le chantier, pas seulement reconstruit au closeout.

## 6_FINAL_TARGET

Chaque chantier multi-machine, multi-surface, divergent ou a risque d'integration doit pouvoir fournir:

- liste des commits significatifs;
- fichiers touches;
- type de changement;
- risque de conflit;
- transfert recommande;
- statut de transfert;
- commandes candidates de reprise.

## 7_CANONICAL_STATE

### ETABLI

- `GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01` a prouve une matrice d'arbitrage avant action.
- Le GO a execute des suppressions locales/remotes controlees.
- Aucun merge n'a ete execute.
- Aucun cherry-pick n'a ete execute.
- Aucun import strategie n'a ete execute.
- Une branche strategie a ete conservee comme reference en attente d'un flux separe.

### CONSOLIDATION

La methode generalisee devient:

> Un chantier produit une liste de changements transferables; l'integration canonique integre cette liste validee, pas forcement toute la branche.

## 8_VALIDATED_PLAN

### A. Pendant le chantier

Apres chaque commit significatif:

```powershell
git log --oneline -1
git show --name-status --stat --oneline HEAD
```

Ajouter ou mettre a jour une ligne dans `COMMIT_TRANSFER_INVENTORY.md` du chantier.

### B. Avant integration

```powershell
git fetch origin --prune
git rev-list --left-right --count origin/sot/mainline...origin/<BRANCHE_CHANTIER>
git log --oneline --right-only origin/sot/mainline...origin/<BRANCHE_CHANTIER>
git diff --name-status origin/sot/mainline...origin/<BRANCHE_CHANTIER>
git diff --stat origin/sot/mainline...origin/<BRANCHE_CHANTIER>
```

### C. Transfert selectif

Options autorisees selon classification:

- `merge` seulement si branche propre, recente, non divergente dangereuse;
- `cherry-pick -n <sha>` pour preview sans commit immediat;
- import fichier par fichier si le commit melange trop de choses;
- patch controle si le delta doit etre decoupe;
- abandon ou reference-only si le changement est obsolete;
- re-ecriture manuelle des index globaux si les index ont avance ailleurs.

## 9_SELECTED_SOLUTION

Maintenir un fichier par chantier:

`docs/chantiers/<GO_ID>/COMMIT_TRANSFER_INVENTORY.md`

Ce fichier ne remplace pas `GO_INDEX.md`, `BRANCH_STATE.md` ou la matrice gouvernante. Il est une preuve locale de transfert pour le chantier.

## 10_SELECTED_SETUP

Template minimal:

```md
# COMMIT_TRANSFER_INVENTORY — <GO_ID>

## ETABLI
- Branche chantier:
- Base canonique:
- Machine owner:
- Dernier fetch/rebase connu:
- Dernier push connu:

## TABLEAU_CHANGEMENTS

| Date | Commit | Type | Fichiers touches | Portee | Risque conflit | Transfert recommande | Statut |
| --- | --- | --- | --- | --- | --- | --- | --- |
| YYYY-MM-DD | <sha> | docs/runtime/index/test | <paths> | local/global | low/medium/high | merge/cherry-pick-n/import-file/patch/manual/reject | pending/done/blocked/reference |

## DECISIONS

- `<sha>`: decision courte.

## NEXT_TRANSFER

- Prochain transfert recommande:
- Commande candidate:
```

## 11_KEY_DECISIONS

- L'inventaire se fait au fil de l'eau.
- Le merge global devient une option, pas le chemin par defaut.
- Les vieux index globaux ne sont pas importes aveuglement.
- Une branche divergente peut rester reference-only si le delta utile est faible ou obsolete.
- Un commit melange peut etre refuse comme cherry-pick direct et transforme en import fichier ou patch controle.

## 12_INVARIANTS

- Ne pas merger une branche divergente seulement parce qu'elle contient un fichier utile.
- Ne pas importer aveuglement `GO_INDEX.md`, `ACTIVE_STREAMS.md`, `NEXT_GO_CANDIDATES.md`, `REPRISE.md` ou `BRANCH_STATE.md` depuis une branche vieillie.
- Toujours lister commits, fichiers touches et ahead/behind avant integration.
- Preferer `cherry-pick -n` pour preview quand le commit semble transferable.
- Aucun transfert ne doit partir d'un worktree sale.
- Le support Git ne remplace pas la decision produit/chantier.

## 13_ESTABLISHED

La consolidation est documentaire. Elle n'execute aucun transfert Git.

## 14_HYPOTHESIS

Certains chantiers futurs pourraient necessiter un template plus strict par machine owner ou par famille produit.

## 15_REMAINING_GAP

Aucun fichier template global n'est encore cree dans `docs/governance/` ou `templates/`. Cette consolidation reste locale au GO existant.

## 16_TODO

1. Reutiliser cette methode dans les prochains chantiers multi-machine ou divergents.
2. Creer un template global seulement si la methode devient recurrente.
3. Si un GO dedie est ouvert plus tard, rattacher ce document comme preuve source.

## 17_RESUME_POINT

Pour appliquer la methode a un chantier actif:

```powershell
cd C:\Users\ghost\opt-trading
git fetch origin --prune
git checkout <branche_chantier>
git status --short --branch
git log --oneline -5
git diff --name-status origin/sot/mainline...HEAD
```

Puis creer ou mettre a jour:

```text
docs/chantiers/<GO_ID>/COMMIT_TRANSFER_INVENTORY.md
```

## 18_TO_DOCUMENT

TAGS:

- `COMMIT_TRANSFER_INVENTORY`
- `SELECTIVE_TRANSFER`
- `CHERRY_PICK_PREVIEW`
- `NO_BLIND_MERGE`
- `NO_BLIND_INDEX_IMPORT`

## 19_TO_REMEMBER

Memory Bricks projet:

- `COMMIT_TRANSFER_INVENTORY_PER_CHANTIER`
- `INTEGRATE_VALIDATED_CHANGES_NOT_WHOLE_BRANCH`
- `CHERRY_PICK_N_FOR_PREVIEW_BEFORE_COMMIT`
- `GLOBAL_INDEXES_MUST_NOT_BE_IMPORTED_BLINDLY`

## RISKS

- À qualifier.
