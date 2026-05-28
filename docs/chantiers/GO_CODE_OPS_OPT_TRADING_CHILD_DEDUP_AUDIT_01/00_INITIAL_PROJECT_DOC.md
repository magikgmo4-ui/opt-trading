---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01
parent_go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: open
lifecycle_stage: dedup_audit_complete
topic_keys:
  - opt-trading
  - code_ops
  - dedup
  - anti_doublon
  - audit_first
  - no_mutation
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
working_branch: go/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
links:
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/30_DEDUP_AUDIT_PROTOCOL.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01/10_DEDUP_QUALIFICATIONS.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01/10_DUPLICATE_CANDIDATES.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01/20_CONSUMER_MAP.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01/30_DECISION_TABLE.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01/40_SAFE_MERGE_CANDIDATES.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01/50_BLOCKED_OR_RISKY_CASES.md
  - docs/registry/CODE_REGISTRY.md
---

# GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Qualifier définitivement les anomalies A01–A06 et produire les lots de travail
dédiés pour chaque catégorie d'action.

Résultat attendu : chaque anomalie a un verdict, une preuve, et un `next_action`
exécutable dans un batch ultérieur.

## 2_INITIAL_PROJECT_DOC

Statut :

- `doc-only`
- `audit-first`
- aucune mutation code dans ce GO
- les suppressions (D05, D06) et ajouts (A01) sont déférés à des lots dédiés

## 3_INITIAL_NEED

Input :
- `GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01/20_REGISTRY_DECISION.md` — anomalies A01–A06
- `GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01/10_DEDUP_QUALIFICATIONS.md` — D05, D06

## 6_FINAL_TARGET

Tables de décision complètes. Verdicts prouvés. Lots de travail définis.
Registre mis à jour pour A03 (modules/router/).

## 7_CANONICAL_STATE

| Anomalie | Verdict | Lot requis |
|---|---|---|
| D05 — scripts doublés execution_engine | LEGACY_REPLACED — DELETE_AFTER_PROOF | batch nettoyage scripts |
| D06 — .bak dirs | DELETE_AFTER_PROOF — preuve confirmée | batch nettoyage .bak |
| A01 — 22 modules sans sanity_check.sh | BATCH_PLAN livré | GO_sanity_check_batch |
| A02 = D05 | idem D05 | idem |
| A03 — modules/router/ | FALSE_POSITIVE — registre mis à jour | non (corrigé ici) |
| A04 — validate_master_target_continuity sans test | ADD_TEST | batch tests |
| A05 — validate_strategy_registry sans test | ADD_TEST | batch tests |
| A06 — schemas S02+S03 sans test | ADD_TEST | batch tests |

## 11_KEY_DECISIONS

| Sujet | Décision |
|---|---|
| D05 suppression | différée — lot dédié avec commit réversible |
| D06 suppression | différée — lot dédié avec commit réversible |
| A01 | batch plan livré ici ; 22 sanity_check.sh à créer par lot |
| A03 | registre corrigé : modules/router/ = FALSE_POSITIVE / CANDIDATE / KEEP |
| A04–A06 | ADD_TEST batch à ouvrir après le lot compatibilité |

## 15_REMAINING_GAP

- Lots de suppression D05 + D06 non encore ouverts.
- 22 sanity_check.sh non encore créés.
- Tests A04/A05/A06 non encore ajoutés.
- Matrice de compatibilité non encore renseignée.

## 16_TODO

1. ouvrir lot nettoyage D05 (`GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_SCRIPTS_01`) ;
2. ouvrir lot nettoyage D06 (`GO_CODE_OPS_OPT_TRADING_CHILD_CLEANUP_BAK_01`) ;
3. ouvrir lot sanity_check.sh (`GO_CODE_OPS_OPT_TRADING_CHILD_SANITY_CHECK_BATCH_01`) ;
4. ouvrir lot tests ADD_TEST ;
5. ouvrir child GO compatibilité.

## 17_RESUME_POINT

```text
Dedup audit complet. Aucun code modifié.
Registre mis à jour pour modules/router/.
NEXT_GO = GO_CODE_OPS_OPT_TRADING_CHILD_COMPATIBILITY_MATRIX_01
ou ouvrir lot nettoyage D05/D06 en priorité.
```
