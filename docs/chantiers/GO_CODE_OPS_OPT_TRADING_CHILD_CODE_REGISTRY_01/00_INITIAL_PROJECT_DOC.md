---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01
parent_go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: open
lifecycle_stage: registry_v1_complete
topic_keys:
  - opt-trading
  - code_ops
  - code_registry
  - audit_first
  - no_mutation
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
working_branch: go/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
links:
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/20_CODE_REGISTRY_SPEC.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/50_NEXT_REGISTRY_INPUT.md
  - docs/registry/CODE_REGISTRY.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01/10_DEDUP_QUALIFICATIONS.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01/20_REGISTRY_DECISION.md
---

# GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Produire le registre canonique v1 du code `opt-trading` à partir de l'inventaire
`GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01`.

Qualifier les doublons suspects D01–D06 avec preuve.

Livrer `docs/registry/CODE_REGISTRY.md` comme première surface exploitable par
le refactor et les child GO suivants.

## 2_INITIAL_PROJECT_DOC

Ce document est la fiche d'ouverture du child GO registre.

Statut :

- `doc-only`
- `audit-first`
- aucune mutation code
- aucune suppression
- registre = documentation, pas décision exécutoire

## 3_INITIAL_NEED

Parent : `GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01`

Input : `GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/50_NEXT_REGISTRY_INPUT.md`

Besoin : registre canonique rempli + doublons qualifiés.

## 4_MASTER_PROJECT_PLAN

1. qualifier D01–D06 par lecture de code + grep imports ;
2. décider du format du registre (Markdown + JSON) ;
3. remplir le registre pour les lots prioritaires (HIGH, puis MEDIUM) ;
4. livrer `docs/registry/CODE_REGISTRY.md` ;
5. documenter les décisions sur les doublons.

## 6_FINAL_TARGET

`docs/registry/CODE_REGISTRY.md` v1 livré et exploitable.
Doublons D01–D06 qualifiés avec verdict.

## 7_CANONICAL_STATE

| Élément | Valeur |
|---|---|
| Scan base | GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01 (2026-05-28) |
| Doublons suspects | 6 (D01–D06) |
| Doublons qualifiés ici | 6 (tous résolus) |
| Entrées registre v1 | ~60 entrées HIGH+MEDIUM |
| Format retenu | Markdown (primaire) |
| Mutation code | aucune |

## 11_KEY_DECISIONS

| Sujet | Décision |
|---|---|
| Format registre | Markdown (CODE_REGISTRY.md) — lisible, versionnable, suffisant pour v1 |
| D01 | NON-doublon — perf/engine est wrapper compat ; perf_engine est canonique |
| D02 | NON-doublon — deux executors distincts (webhook runtime vs dry_run pipeline) |
| D03 | NON-doublon — engines/router.py est le router réel ; modules/router/ est shell vide |
| D04 | NON-doublon — bitget_bridge.py est wrapper entrypoint ; simex est l'implémentation |
| D05 | Anomalie — scripts doublés dans execution_engine, différents, à nettoyer dans batch dédié |
| D06 | DELETE_CANDIDATE — .bak/ dirs à retirer dans batch nettoyage dédié |

## 12_INVARIANTS

- Le registre documente ; il ne supprime pas.
- Un statut DEPRECATED nécessite preuve + consommateur de remplacement.
- La réalité repo prime sur le registre.
- Aucune entrée DELETE_CANDIDATE sans preuve.

## 15_REMAINING_GAP

- Entrées LOW non encore dans le registre v1 (tools/strategy, collectors mineurs).
- Validateur `tools/code_ops/validate_code_registry.py` non encore créé.
- 22 modules sans sanity_check.sh : batch dédié requis.
- D05 et D06 : lots de nettoyage dédiés non encore ouverts.

## 16_TODO

1. ouvrir `GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01` pour D05+D06 ;
2. compléter le registre v1 avec les entrées LOW ;
3. créer `tools/code_ops/validate_code_registry.py` ;
4. proposer le premier batch de refactor sûr.

## 17_RESUME_POINT

```text
Registre v1 livré. Doublons D01–D06 qualifiés.
NEXT_GO = GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01
Lire docs/registry/CODE_REGISTRY.md.
```
