---
doc_id: GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module:
  go_id: GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - doc_ops
  - branch_arbitration
  - branch_cleanup
  - deletion_control
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01/03_branch_arbitrage_seed.md
point_de_reprise: "17_RESUME_POINT"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01/03_branch_arbitrage_seed.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01/90_closeout.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01/01_audit_a_verifier.md
  - docs/index/BRANCH_STATE.md
---

# GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01 — cadrage

## 1_MASTER_TARGET

Traiter les 7 décisions utilisateur issues des 33 branches `A_VERIFIER_DEEPER` documentées par le cleanup branches, sans suppression ni intégration automatique.

## 2_INITIAL_PROJECT_DOC

Références canoniques:

- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_BRANCH_CLEANUP_01/01_audit_a_verifier.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01/03_branch_arbitrage_seed.md`
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01/90_closeout.md`
- `docs/index/BRANCH_STATE.md`

## 3_INITIAL_NEED

Après merge de PR #166, les décisions utilisateur sur 7 branches doivent être traitées dans un GO séparé:

- 4 branches candidates suppression;
- 3 branches en closeout-only review.

Aucune action destructive ne doit être lancée sans preuve locale/remote et commande explicite.

## 4_MASTER_PROJECT_PLAN

Séquence prévue:

1. Vérifier l’existence locale/remote de chaque branche.
2. Recalculer `ahead_by` / `behind_by` contre `origin/sot/mainline`.
3. Classer les 4 `DROP_*_CANDIDATE` en `READY_TO_DELETE` ou `BLOCKED`.
4. Classer les 3 `CLOSEOUT_ONLY_REVIEW` en `READY_FOR_CLOSEOUT_IMPORT`, `REFERENCE_ONLY`, ou `BLOCKED`.
5. Produire une preuve documentaire avant toute suppression ou import.
6. Exécuter uniquement après validation explicite.

## 5_GO_PLAN

Livrables attendus:

- `00_cadrage.md` — présent fichier.
- `01_branch_proof_matrix.md` — preuve locale/remote des 7 branches.
- `02_execution_plan.md` — commandes exactes, séparées suppression locale / suppression remote / closeout-only review.
- `90_closeout.md` — seulement après validation ou blocage documenté.

## 6_FINAL_TARGET

Obtenir une matrice fiable permettant de savoir:

- quelles branches peuvent être supprimées localement;
- quelles branches peuvent être supprimées remote;
- quelles branches doivent être relues pour closeout-only;
- quelles branches sont bloquées ou à conserver.

## 7_CANONICAL_STATE

Établi:

- PR #166 mergée.
- `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01` fermé et intégré.
- Les 7 décisions utilisateur sont documentées dans `03_branch_arbitrage_seed.md`.
- Aucune suppression n’a encore été exécutée.
- Le présent GO démarre sur branche dédiée:
  - `go/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01`

## 11_KEY_DECISIONS

### DROP_CANDIDATE — à prouver avant suppression

| BRANCH | SCOPE_SEED | INTENTION | EXECUTION_STATUS |
| --- | --- | --- | --- |
| `wip/GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01` | local | DROP_LOCAL_ONLY_CANDIDATE | NOT_EXECUTED |
| `METHODE_MULTI_MACHINE_GIT_SYNC` | remote | DROP_REMOTE_CANDIDATE | NOT_EXECUTED |
| `feat/journal-api-extractor-v1` | local | DROP_LOCAL_ONLY_CANDIDATE | NOT_EXECUTED |
| `audit/opt-trading-20260320a` | remote | DROP_REMOTE_CANDIDATE | NOT_EXECUTED |

### CLOSEOUT_ONLY_REVIEW — à relire avant intégration/fermeture

| BRANCH | SCOPE_SEED | INTENTION | EXECUTION_STATUS |
| --- | --- | --- | --- |
| `docs/github-park-parent-closeout-01` | remote | CLOSEOUT_ONLY_REVIEW | NOT_EXECUTED |
| `docs/github-park-pass-close-01` | remote | CLOSEOUT_ONLY_REVIEW | NOT_EXECUTED |
| `feat/go-strategy-docs-v1` | remote | CLOSEOUT_ONLY_REVIEW | NOT_EXECUTED |

## 12_INVARIANTS

- Ne pas supprimer de branche dans le cadrage.
- Ne pas supprimer de branche sans validation explicite post-preuve.
- Ne pas merger les trois branches closeout-only sans lecture du commit ahead.
- Ne pas modifier les modules runtime.
- Ne pas modifier `docs/index/BRANCH_STATE.md` avant décision finale.
- Ne pas utiliser `git add .`.
- Séparer suppression locale, suppression remote et import closeout-only.

## 15_REMAINING_GAP

- Preuve locale/remote des 7 branches.
- Deltas actualisés contre `origin/sot/mainline`.
- Identification des commandes exactes.
- Décision finale utilisateur avant exécution.

## 16_TODO

1. Produire `01_branch_proof_matrix.md`.
2. Produire `02_execution_plan.md`.
3. Attendre validation explicite avant suppression.
4. Exécuter ou bloquer selon preuves.
5. Produire closeout.

## 17_RESUME_POINT

```powershell
cd C:\Users\ghost\opt-trading
git fetch origin --prune
git checkout go/GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01
git status --short --branch
```

Prochaine action:

```text
Produire 01_branch_proof_matrix.md avec existence locale/remote, ahead/behind, décision provisoire et commande candidate.
```

## 18_TO_DOCUMENT

TAGS:

- `GO_OPT_TRADING_DOC_OPS_BRANCH_ARBITRATION_EXECUTION_01`
- `DROP_CANDIDATE`
- `CLOSEOUT_ONLY_REVIEW`
- `BRANCH_PROOF_MATRIX`

Blocs à extraire:

- `11_KEY_DECISIONS`
- `12_INVARIANTS`
- `17_RESUME_POINT`

## 19_TO_REMEMBER

Memory Bricks projet:

- `BRANCH_ARBITRATION_EXECUTION_REQUIRES_PROOF_BEFORE_DELETE`
- `DROP_CANDIDATES_ARE_NOT_DELETED_BY_CADRAGE`
- `CLOSEOUT_ONLY_REVIEW_REQUIRES_AHEAD_COMMIT_READING`
