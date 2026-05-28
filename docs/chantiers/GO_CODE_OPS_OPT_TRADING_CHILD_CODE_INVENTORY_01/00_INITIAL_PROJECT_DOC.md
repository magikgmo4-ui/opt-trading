---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01
parent_go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: open
lifecycle_stage: inventory_complete
topic_keys:
  - opt-trading
  - code_ops
  - code_inventory
  - audit_first
  - no_mutation
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
working_branch: go/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
links:
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/10_CODE_INVENTORY_PROTOCOL.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/10_FILE_INVENTORY.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/20_ENTRYPOINTS.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/30_VALIDATORS_AND_SCHEMAS.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/40_RISK_MAP.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/50_NEXT_REGISTRY_INPUT.md
---

# GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Produire l'inventaire réel et complet du code `opt-trading` sans aucune mutation.

Livrer des tables d'inventaire exploitables comme input pour le registre canonique
(`GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01`).

## 2_INITIAL_PROJECT_DOC

Ce document est la fiche d'ouverture du child GO d'inventaire.

Statut :

- `doc-only`
- `audit-first`
- aucune mutation code
- aucune suppression
- aucun renommage
- aucun index global modifié

## 3_INITIAL_NEED

Parent : `GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01`

Besoin transmis par le parent :

> Produire l'inventaire réel des fichiers, entrypoints, validateurs, schémas
> et surfaces à risque avant tout refactor.

## 4_MASTER_PROJECT_PLAN

Protocole appliqué : `10_CODE_INVENTORY_PROTOCOL.md` du parent.

Livrables produits :

1. inventaire fichiers (Table A) ;
2. entrypoints CLI (Table B) ;
3. validateurs et schémas (Table C + D) ;
4. carte de risque ;
5. input registre initial.

## 5_GO_PLAN

GO child hérite de la branche parent :
`go/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01`

Aucune branche enfant créée — héritage direct conforme à la matrice (section 9.3).

## 6_FINAL_TARGET

Tables d'inventaire complètes et carte de risque livrées.

Verdict : `PASS_INVENTORY_READY`

## 7_CANONICAL_STATE

| Élément | Valeur |
|---|---|
| Repo | `magikgmo4-ui/opt-trading` |
| Branche | `go/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01` |
| Scan effectué le | 2026-05-28 |
| Python files (.py) | 543 |
| Shell scripts (.sh) | 683 |
| YAML workflows | 7 |
| Modules avec cmd.sh | 83 |
| Tests | 65 |
| Tools | 53 |
| Mutation code | aucune |
| Index globaux | non modifiés |

## 8_VALIDATED_PLAN

1. lire protocole d'inventaire parent ;
2. scanner avec `git ls-files` ;
3. identifier entrypoints (main guard + argparse) ;
4. identifier validateurs et schémas ;
5. identifier doublons suspects ;
6. classifier par risque ;
7. produire tables d'inventaire ;
8. produire input registre.

## 9_SELECTED_SOLUTION

Scan `git ls-files` + grep ciblé sur les patterns identifiés par le protocole.
Aucun outil externe. Aucune mutation.

## 10_SELECTED_SETUP

```text
docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/
  00_INITIAL_PROJECT_DOC.md
  10_FILE_INVENTORY.md
  20_ENTRYPOINTS.md
  30_VALIDATORS_AND_SCHEMAS.md
  40_RISK_MAP.md
  50_NEXT_REGISTRY_INPUT.md
docs/index/inbox/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01.md
```

## 11_KEY_DECISIONS

| Sujet | Décision |
|---|---|
| Branche | héritée du parent, pas de branche enfant |
| Périmètre scan | tools/, modules/, tests/, .github/workflows/, scripts/, config/ |
| data/ et artifacts/ | exclus sauf contrats |
| Doublons | marqués DUPLICATE_SUSPECT, pas qualifiés définitivement ici |
| Verdict | PASS_INVENTORY_READY |

## 12_INVARIANTS

- Aucun fichier modifié.
- Aucun fichier supprimé.
- Aucun fichier déplacé.
- Aucun index global modifié.
- `deprecated` jamais conclu sans preuve.
- `unknown` utilisé si le rôle n'est pas certain.

## 15_REMAINING_GAP

- Registre canonique non encore rempli (prochain GO).
- Doublons suspects non encore qualifiés définitivement.
- Matrice de compatibilité non encore testée.
- Tests manquants non encore ciblés.

## 16_TODO

Actions suivantes (hors ce child GO) :

1. ouvrir `GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01` ;
2. remplir le registre depuis `50_NEXT_REGISTRY_INPUT.md` ;
3. qualifier les doublons suspects ;
4. proposer le premier batch sûr.

## 17_RESUME_POINT

```text
Inventaire produit. Aucun code modifié.
NEXT_GO = GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01.
Lire 50_NEXT_REGISTRY_INPUT.md pour l'input registre.
```
