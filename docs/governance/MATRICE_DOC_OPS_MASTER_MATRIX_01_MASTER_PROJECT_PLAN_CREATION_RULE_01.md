---
doc_id: MATRICE_DOC_OPS_MASTER_MATRIX_01_MASTER_PROJECT_PLAN_CREATION_RULE_01
doc_type: governance_master_matrix_extension
repo: opt-trading
project: opt-trading
module: governance
go_id: GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_CREATION_RULE_MATRIX_01
status: reference
lifecycle_stage: governance
surface: governance
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
topic_keys:
  - opt-trading
  - master_project_plan
  - go_structural_role
  - creation_rule
  - master_matrix
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/REPRISE.md
---

# MATRICE_DOC_OPS_MASTER_MATRIX_01_MASTER_PROJECT_PLAN_CREATION_RULE_01

## Objet

Ajouter à la matrice maître la règle de création structurée des GO et la lecture des index globaux comme `MASTER_PROJECT_PLAN_INDEX`.

Cette extension est canonique pour les ouvertures nouvelles à partir de sa publication.

## 1. Chaîne canonique de continuité

```text
PF_* 
-> 1_MASTER_TARGET 
-> 4_MASTER_PROJECT_PLAN / GO_MASTER_PROJECT_PLAN
-> GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN
-> GO_CHILD_ATTACHED_TO_PARENT
-> BUNDLE_TARGET / NEXT_GO / CLOSE_GATE
```

## 2. Rôles structurels autorisés

La création d’un GO doit déclarer exactement un `GO_STRUCTURAL_ROLE` parmi :

```text
GO_CHILD
GO_CHILD_ATTACHED_TO_PARENT
GO_PARENT
GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN
GO_MASTER_PROJECT_PLAN
```

`GO_ORPHAN` n’est pas un rôle canonique.
Un GO non encore rattaché est soit `GO_CHILD`, soit `GO_PARENT`, avec un `NEXT_ATTACH_TARGET` obligatoire.

## 3. Définitions

| Rôle | Définition | Champs requis |
|---|---|---|
| `GO_CHILD` | GO enfant ciblé, non encore attaché ou en qualification de rattachement | `GO_ID`, `6_FINAL_TARGET`, `NEXT_ATTACH_TARGET` |
| `GO_CHILD_ATTACHED_TO_PARENT` | GO enfant rattaché à un parent clair | `GO_ID`, `PARENT_GO_ID`, `6_FINAL_TARGET`, `BUNDLE_TARGET` si applicable |
| `GO_PARENT` | Parent de continuité pour produit, support, tool ou surface, pas encore relié à un master project plan | `GO_ID`, `parent_scope`, `MASTER_TARGET_CANDIDATE`, `NEXT_ATTACH_TARGET` |
| `GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN` | Parent relié à un `4_MASTER_PROJECT_PLAN` | `GO_ID`, `MASTER_PROJECT_PLAN_ID`, `PF_ID`, `MASTER_TARGET_ID` |
| `GO_MASTER_PROJECT_PLAN` | Plan maître de produit/surface finale ; niveau supérieur de continuité | `MASTER_PROJECT_PLAN_ID`, `PF_ID`, `1_MASTER_TARGET`, `close_gate` |

## 4. Champs obligatoires à la création

Tout nouveau GO doit déclarer :

```yaml
GO_ID: <GO_...>
GO_STRUCTURAL_ROLE: GO_CHILD | GO_CHILD_ATTACHED_TO_PARENT | GO_PARENT | GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN | GO_MASTER_PROJECT_PLAN
PF_ID: <PF_* | null>
MASTER_TARGET_ID: <MT_* | MASTER_TARGET_* | null>
MASTER_PROJECT_PLAN_ID: <MPP_* | null>
PARENT_GO_ID: <GO_* | null>
6_FINAL_TARGET: <cible de phase | null>
BUNDLE_TARGET: <target de bundle | null>
NEXT_ATTACH_TARGET: <rattachement attendu | null>
NEXT_GO: <GO_* | TBD_* | null>
```

## 5. Règles de rattachement

1. Un `GO_CHILD_ATTACHED_TO_PARENT` doit pointer vers un `PARENT_GO_ID`.
2. Un `GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN` doit pointer vers un `MASTER_PROJECT_PLAN_ID`.
3. Un `GO_MASTER_PROJECT_PLAN` doit pointer vers un `PF_ID` et un `1_MASTER_TARGET`.
4. Un `GO_CHILD` non attaché doit avoir un `NEXT_ATTACH_TARGET`.
5. Un `GO_PARENT` non attaché doit avoir un `NEXT_ATTACH_TARGET`.
6. Aucun `GO_CHILD` non attaché et aucun `GO_PARENT` non attaché ne peut être fermé comme livré sans rattachement ou justification explicite.
7. Un support/tool/other doit avoir son propre parent de continuité, puis être rattaché à un `4_MASTER_PROJECT_PLAN`.

## 6. Index global = MASTER_PROJECT_PLAN_INDEX

Les index globaux doivent refléter les `MASTER_PROJECT_PLAN` et leur continuité.

```text
index global
= MASTER_PROJECT_PLAN_INDEX
= PF_* + 1_MASTER_TARGET + 4_MASTER_PROJECT_PLAN + parent + child/bundle + NEXT_GO/CLOSE_GATE
```

Les fichiers de continuité concernés sont :

```text
docs/index/GO_INDEX.md
docs/index/ACTIVE_STREAMS.md
docs/index/NEXT_GO_CANDIDATES.md
docs/index/REPRISE.md
```

Règles :

- Les produits/surfaces finales `PF_*` doivent être visibles dans les index globaux existants.
- Les `MASTER_PROJECT_PLAN_ID` doivent y apparaître avec leur continuité.
- Les supports/tools/other ne flottent pas comme entrées autonomes : ils doivent avoir un parent de continuité ou un rattachement à un `MASTER_PROJECT_PLAN`.
- Les child/bundle targets restent sous leur parent ; ils ne remplacent jamais le `MASTER_PROJECT_PLAN`.
- Les index globaux ne sont pas un journal de micro-GO ; ils portent la continuité produit et les changements structurels.

## 7. Fermeture

Un parent ne peut être fermé que si :

```text
PF_* prouvé utilisable
+ 1_MASTER_TARGET atteint
+ 4_MASTER_PROJECT_PLAN complété ou explicitement déclassé
+ CLOSE_GATE_MASTER_TARGET validé
```

Un child, un bundle, une PR ou un patch ne ferme pas le parent.

## 8. Création minimale recommandée

### Nouveau child non rattaché

```yaml
GO_STRUCTURAL_ROLE: GO_CHILD
PARENT_GO_ID: null
NEXT_ATTACH_TARGET: identifier le parent cible avant fermeture
```

### Nouveau child rattaché

```yaml
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PARENT_GO_ID: GO_...
MASTER_PROJECT_PLAN_ID: MPP_...
```

### Nouveau parent non encore rattaché

```yaml
GO_STRUCTURAL_ROLE: GO_PARENT
MASTER_PROJECT_PLAN_ID: null
NEXT_ATTACH_TARGET: rattacher à MPP_* ou créer GO_MASTER_PROJECT_PLAN
```

### Nouveau parent rattaché

```yaml
GO_STRUCTURAL_ROLE: GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN
PF_ID: PF_...
MASTER_PROJECT_PLAN_ID: MPP_...
MASTER_TARGET_ID: MT_... ou MASTER_TARGET_...
```

### Nouveau master project plan

```yaml
GO_STRUCTURAL_ROLE: GO_MASTER_PROJECT_PLAN
PF_ID: PF_...
MASTER_PROJECT_PLAN_ID: MPP_...
1_MASTER_TARGET: produit final utilisable
close_gate: critères de fermeture
```

## 9. Invariants

```text
GO_ORPHAN n’est pas un rôle canonique.
GO_CHILD et GO_PARENT peuvent être temporaires mais doivent avoir NEXT_ATTACH_TARGET.
GO_CHILD doit évoluer vers GO_CHILD_ATTACHED_TO_PARENT.
GO_PARENT doit évoluer vers GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN.
GO_MASTER_PROJECT_PLAN est le niveau d’organisation global sous PF_* et 1_MASTER_TARGET.
Index global = MASTER_PROJECT_PLAN_INDEX.
```

## 10. NEXT_GO recommandé

```text
GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_CREATION_RULE_APPLY_01
```

Objectif : appliquer cette règle aux prochaines ouvertures et corriger progressivement les GO existants sans migration massive non contrôlée.
