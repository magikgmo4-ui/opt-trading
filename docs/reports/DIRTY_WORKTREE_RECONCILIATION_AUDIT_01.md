# DIRTY_WORKTREE_RECONCILIATION_AUDIT_01

## 1_MASTER_TARGET
Classifier le dirty worktree hors scope avant toute action destructive ou commit additionnel.

## 7_CANONICAL_STATE
- Repo : `opt-trading`
- Branche : `sot/mainline`
- HEAD : `73a7a699`
- Ahead/behind : `ahead 1 / behind 0` vs `origin/sot/mainline`
- Dirty summary : 3 fichiers tracked modifies, 26 fichiers non suivis, aucun changement ajoute dans cette passe
- Commit recent : `73a7a699 docs: canonize parent chantier decisions`
- Date : `2026-05-17`

## DIRTY_TABLE

| Fichier | Type | Scope probable | Classification | Preuve | Action recommandee |
|---|---|---|---|---|---|
| `docs/index/BRANCH_STATE.md` | tracked | reconciliation branches / indexes | `SEPARATE_GO` | diff massif sur classifications et nouvelles entrees `admin-trading` / `db-layer` | traiter dans un GO separe de reconciliation branch-state |
| `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` | tracked | routing machine / indexes | `SEPARATE_GO` | diff massif sur le bloc `ADMIN_TRADING` et re-routage de nombreuses branches | traiter dans un GO separe machine split |
| `webhook_server.py` | tracked | runtime code | `SEPARATE_GO` | diff très large, 1926 lignes, trailing whitespace deja present | isoler dans un GO technique separe; ne pas corriger opportunement ici |
| `docs/reports/PARENT_CHANTIERS_CLOSEOUT_REOPEN_ACTION_LIST_01.md` | untracked | rapport de decision | `KEEP` | livrable issu de la passe precedente | conserver tel quel pour suivi / commit ulterieur si decide |
| `docs/reports/PARENT_CHANTIERS_PRODUCT_SURFACE_STATUS_AUDIT_01.md` | untracked | rapport d'audit | `KEEP` | livrable issu de la passe precedente | conserver tel quel pour suivi / commit ulterieur si decide |
| `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_A_VERIFIER_REVIEW_01/00_START.md` | untracked | `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | `SEPARATE_GO` | paquet doc-only admin-trading en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_A_VERIFIER_REVIEW_01/10_A_VERIFIER_REVIEW.md` | untracked | `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | `SEPARATE_GO` | paquet doc-only admin-trading en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_A_VERIFIER_REVIEW_01/90_CLOSEOUT.md` | untracked | `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | `SEPARATE_GO` | paquet doc-only admin-trading en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_DOC_RECONCILIATION_01/00_START.md` | untracked | `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | `SEPARATE_GO` | paquet doc-only admin-trading en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_DOC_RECONCILIATION_01/10_RECONCILIATION.md` | untracked | `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | `SEPARATE_GO` | paquet doc-only admin-trading en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_DOC_RECONCILIATION_01/90_CLOSEOUT.md` | untracked | `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | `SEPARATE_GO` | paquet doc-only admin-trading en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01/00_START.md` | untracked | `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | `SEPARATE_GO` | paquet doc-only admin-trading en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01/10_BRANCH_STATE_SEED.md` | untracked | `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | `SEPARATE_GO` | paquet doc-only admin-trading en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01/90_CLOSEOUT.md` | untracked | `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | `SEPARATE_GO` | paquet doc-only admin-trading en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_MACHINE_WORK_SPLIT_UPDATE_01/00_START.md` | untracked | `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | `SEPARATE_GO` | paquet doc-only admin-trading en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_MACHINE_WORK_SPLIT_UPDATE_01/10_MACHINE_WORK_SPLIT_UPDATE.md` | untracked | `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | `SEPARATE_GO` | paquet doc-only admin-trading en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_MACHINE_WORK_SPLIT_UPDATE_01/90_CLOSEOUT.md` | untracked | `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | `SEPARATE_GO` | paquet doc-only admin-trading en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_DB_LAYER_A_VERIFIER_REVIEW_01/00_START.md` | untracked | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `SEPARATE_GO` | paquet doc-only db-layer en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_DB_LAYER_A_VERIFIER_REVIEW_01/10_A_VERIFIER_REVIEW.md` | untracked | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `SEPARATE_GO` | paquet doc-only db-layer en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_DB_LAYER_A_VERIFIER_REVIEW_01/90_CLOSEOUT.md` | untracked | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `SEPARATE_GO` | paquet doc-only db-layer en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_DB_LAYER_BRANCH_DOC_RECONCILIATION_01/00_START.md` | untracked | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `SEPARATE_GO` | paquet doc-only db-layer en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_DB_LAYER_BRANCH_DOC_RECONCILIATION_01/10_RECONCILIATION.md` | untracked | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `SEPARATE_GO` | paquet doc-only db-layer en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_DB_LAYER_BRANCH_DOC_RECONCILIATION_01/90_CLOSEOUT.md` | untracked | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `SEPARATE_GO` | paquet doc-only db-layer en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_DB_LAYER_BRANCH_STATE_SEED_01/00_START.md` | untracked | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `SEPARATE_GO` | paquet doc-only db-layer en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_DB_LAYER_BRANCH_STATE_SEED_01/10_BRANCH_STATE_SEED.md` | untracked | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `SEPARATE_GO` | paquet doc-only db-layer en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_DB_LAYER_BRANCH_STATE_SEED_01/90_CLOSEOUT.md` | untracked | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `SEPARATE_GO` | paquet doc-only db-layer en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_DB_LAYER_DEEP_AUDIT_01/00_START.md` | untracked | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `SEPARATE_GO` | paquet doc-only db-layer en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_DB_LAYER_DEEP_AUDIT_01/10_DEEP_AUDIT.md` | untracked | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `SEPARATE_GO` | paquet doc-only db-layer en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_DB_LAYER_DEEP_AUDIT_01/90_CLOSEOUT.md` | untracked | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `SEPARATE_GO` | paquet doc-only db-layer en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_DB_LAYER_REMAINING_A_VERIFIER_REVIEW_01/00_START.md` | untracked | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `SEPARATE_GO` | paquet doc-only db-layer en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_DB_LAYER_REMAINING_A_VERIFIER_REVIEW_01/10_REMAINING_A_VERIFIER_REVIEW.md` | untracked | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `SEPARATE_GO` | paquet doc-only db-layer en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |
| `docs/chantiers/GO_OPT_TRADING_DB_LAYER_REMAINING_A_VERIFIER_REVIEW_01/90_CLOSEOUT.md` | untracked | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `SEPARATE_GO` | paquet doc-only db-layer en 3 fichiers | garder comme lot dedie; ne pas fusionner au commit audit |

## TRACKED_DIRTY

- `docs/index/BRANCH_STATE.md`
  - type de modification : gros ajouts/reclassifications de branches et statuts.
  - preuve du diff : 89 lignes modifiees, focus sur `admin-trading` / `db-layer` / `OpenClaw`.
  - risque : forte couplage avec la reconciliation de branches; ne pas absorber dans le commit audit.
  - classification : `SEPARATE_GO`.
  - action recommandee : traiter dans un lot documente distinct.

- `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
  - type de modification : re-deploiement majeur du bloc `ADMIN_TRADING` et des routages machine.
  - preuve du diff : 156 lignes modifiees, ajout d'un grand inventaire actif.
  - risque : melange de routage canonique et de reconciliation de branches.
  - classification : `SEPARATE_GO`.
  - action recommandee : lot distinct de machine split / anti-conflict.

- `webhook_server.py`
  - type de modification : gros diff code runtime.
  - preuve du diff : 1926 lignes touchees; `git diff --check` signale des trailing whitespace deja present.
  - risque : correction opportuniste hors scope et possible regressions runtime.
  - classification : `SEPARATE_GO`.
  - action recommandee : dedicacer un GO technique separe; ne pas toucher dans cette passe.

## UNTRACKED_FILES

### KEEP
- `docs/reports/PARENT_CHANTIERS_CLOSEOUT_REOPEN_ACTION_LIST_01.md` : livrable documentaire de decision; garder en attente d'arbitrage utilisateur.
- `docs/reports/PARENT_CHANTIERS_PRODUCT_SURFACE_STATUS_AUDIT_01.md` : livrable documentaire d'audit; garder en attente d'arbitrage utilisateur.

### SEPARATE_GO
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_A_VERIFIER_REVIEW_01/00_START.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_A_VERIFIER_REVIEW_01/10_A_VERIFIER_REVIEW.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_A_VERIFIER_REVIEW_01/90_CLOSEOUT.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_DOC_RECONCILIATION_01/00_START.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_DOC_RECONCILIATION_01/10_RECONCILIATION.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_DOC_RECONCILIATION_01/90_CLOSEOUT.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01/00_START.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01/10_BRANCH_STATE_SEED.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01/90_CLOSEOUT.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_MACHINE_WORK_SPLIT_UPDATE_01/00_START.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_MACHINE_WORK_SPLIT_UPDATE_01/10_MACHINE_WORK_SPLIT_UPDATE.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_MACHINE_WORK_SPLIT_UPDATE_01/90_CLOSEOUT.md`
- `docs/chantiers/GO_OPT_TRADING_DB_LAYER_A_VERIFIER_REVIEW_01/00_START.md`
- `docs/chantiers/GO_OPT_TRADING_DB_LAYER_A_VERIFIER_REVIEW_01/10_A_VERIFIER_REVIEW.md`
- `docs/chantiers/GO_OPT_TRADING_DB_LAYER_A_VERIFIER_REVIEW_01/90_CLOSEOUT.md`
- `docs/chantiers/GO_OPT_TRADING_DB_LAYER_BRANCH_DOC_RECONCILIATION_01/00_START.md`
- `docs/chantiers/GO_OPT_TRADING_DB_LAYER_BRANCH_DOC_RECONCILIATION_01/10_RECONCILIATION.md`
- `docs/chantiers/GO_OPT_TRADING_DB_LAYER_BRANCH_DOC_RECONCILIATION_01/90_CLOSEOUT.md`
- `docs/chantiers/GO_OPT_TRADING_DB_LAYER_BRANCH_STATE_SEED_01/00_START.md`
- `docs/chantiers/GO_OPT_TRADING_DB_LAYER_BRANCH_STATE_SEED_01/10_BRANCH_STATE_SEED.md`
- `docs/chantiers/GO_OPT_TRADING_DB_LAYER_BRANCH_STATE_SEED_01/90_CLOSEOUT.md`
- `docs/chantiers/GO_OPT_TRADING_DB_LAYER_DEEP_AUDIT_01/00_START.md`
- `docs/chantiers/GO_OPT_TRADING_DB_LAYER_DEEP_AUDIT_01/10_DEEP_AUDIT.md`
- `docs/chantiers/GO_OPT_TRADING_DB_LAYER_DEEP_AUDIT_01/90_CLOSEOUT.md`
- `docs/chantiers/GO_OPT_TRADING_DB_LAYER_REMAINING_A_VERIFIER_REVIEW_01/00_START.md`
- `docs/chantiers/GO_OPT_TRADING_DB_LAYER_REMAINING_A_VERIFIER_REVIEW_01/10_REMAINING_A_VERIFIER_REVIEW.md`
- `docs/chantiers/GO_OPT_TRADING_DB_LAYER_REMAINING_A_VERIFIER_REVIEW_01/90_CLOSEOUT.md`

## WEBHOOK_SERVER_ANALYSIS
- Nature du diff : gros changement runtime / application, pas un simple nettoyage.
- Trailing whitespace : present et deja signale par Git.
- Fonctionnalite touchee : serveur webhook, logique de risque, routage, endpoints API et utilitaires runtime.
- Risque de correction opportuniste : eleve, car ce fichier est hors scope de la reconciliation documentaire actuelle.
- Recommandation : `SEPARATE_GO`.

## 13_ESTABLISHED
- Le commit `73a7a699` existe sur `sot/mainline` et la branche est ahead de 1 sur `origin/sot/mainline`.
- Les trois fichiers du commit scoped precedent restent isoles de ce dirty audit.
- `webhook_server.py` contient un gros diff runtime et ne doit pas etre corrige opportunement ici.
- Les rapports `docs/reports/*` proviennent des passes precedentes et sont non suivis.

## 14_HYPOTHESIS
- Les paquets `admin-trading` et `db-layer` non suivis semblent appartenir a des GO documentaires distincts de reconciliation branch/index.
- Les modifications de `BRANCH_STATE.md` et `MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` semblent etre de la meme famille de reconciliation documentaire.

## 15_REMAINING_GAP
- Decider si les deux rapports en `docs/reports/` doivent etre gardes, stashes ou commits plus tard.
- Decider si la reconciliation `BRANCH_STATE.md` / `MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` doit devenir un GO separe ou rester un travail en cours.
- Decider si `webhook_server.py` doit etre stashe, conserve en cours, ou transforme en GO technique dedie.

## 16_TODO
1. Garder les deux rapports `docs/reports/*`.
2. Isoler `BRANCH_STATE.md` et `MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` dans un GO de reconciliation separe.
3. Isoler `webhook_server.py` dans un GO technique separe.
4. Conserver les paquets `admin-trading` et `db-layer` comme GO/documentation separés.
5. Decider ensuite si le commit `73a7a699` peut etre pousse seul.

## 17_RESUME_POINT
Reprendre par la separation explicite des trois zones `KEEP` / `SEPARATE_GO` : rapports, index branch/machine, et `webhook_server.py`.

## 18_TO_DOCUMENT
- TAGS : `dirty_worktree`, `reconciliation`, `separate_go`, `keep`, `read_only_audit`
- Blocs a extraire : classification tracked; classification untracked; analyse `webhook_server.py`

## 19_TO_REMEMBER
MEM_CANDIDATE:
- [Dirty worktree reconciliation map] : `BRANCH_STATE.md` -> `SEPARATE_GO`; `MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` -> `SEPARATE_GO`; `webhook_server.py` -> `SEPARATE_GO`; rapports -> `KEEP`.

SAVE_MEMORY:
- Aucun enregistrement memoire durable sans validation utilisateur explicite.

## RISKS

- À qualifier.
