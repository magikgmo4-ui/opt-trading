---
doc_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
parent_go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: open
lifecycle_stage: audit_first_refactor_planning
topic_keys:
  - opt-trading
  - code_ops
  - refactor
  - normalization
  - code_registry
  - dedup
  - compatibility
  - test_lock
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
base_branch: sot/mainline
working_branch: go/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
base_commit: 2bf4c03bdd57abe6a5afdaf1b5fc948e0a6ffff6
links:
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/10_CODE_INVENTORY_PROTOCOL.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/20_CODE_REGISTRY_SPEC.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/30_DEDUP_AUDIT_PROTOCOL.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/40_COMPATIBILITY_MATRIX.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/50_REFACTOR_BATCH_PLAN.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/60_TEST_LOCK_AND_VALIDATION.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/70_OPERATOR_PROMPTS.md
  - docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/80_OPENING_CHECKPOINT.md
  - docs/index/inbox/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01.md
---

# GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Structurer un chantier parent de refactor Code Ops pour normaliser la base de code `opt-trading` sans mutation fonctionnelle initiale.

Le résultat visé est une base de code plus stable, lisible, compatible et maintenable grâce à :

- un registre canonique des modules, scripts, validateurs, schémas et tests ;
- une règle anti-doublon exploitable avant suppression ou fusion ;
- une matrice de compatibilité Windows / Debian / WSL / tmux / GitHub Actions / usage mobile ;
- un plan de refactor par petits lots, chacun testable et réversible ;
- un verrouillage par tests et validations avant toute modification fonctionnelle.

## 2_INITIAL_PROJECT_DOC

Ce document est la fiche de référence initiale du chantier parent.

Statut :

- `doc-only`
- `audit-first`
- aucune mutation code au démarrage
- aucune suppression
- aucun renommage
- aucun changement d'interface CLI
- aucun changement d'index global sauf nécessité prouvée

Ce document reste stable sauf changement explicite ou implicite du périmètre projet.

## 3_INITIAL_NEED

Demande initiale :

> normalisation du code, registre de codeur/code, anti-doublon, allègement, efficacité, compatibilité, etc. refactor ?

Interprétation validée :

- ce n'est pas un simple nettoyage ;
- c'est un refactor structurant Code Ops ;
- le chantier doit commencer par un inventaire et un registre ;
- l'anti-doublon précède l'allègement ;
- la compatibilité précède toute consolidation durable ;
- la performance ne doit être optimisée qu'après mesure.

## 4_MASTER_PROJECT_PLAN

### Axe A — Inventaire réel

Lister sans mutation :

- modules runtime ;
- scripts CLI ;
- validateurs ;
- schémas ;
- tests ;
- wrappers ;
- adapters ;
- runbooks exécutables ;
- sorties JSON ;
- conventions de logs ;
- doublons suspects ;
- dépendances transverses ;
- surfaces sensibles.

### Axe B — Registre canonique du code

Créer une table de référence par élément de code :

- `code_id`
- `path`
- `role`
- `owner_surface`
- `status`
- `entrypoint`
- `inputs`
- `outputs`
- `tests`
- `compatibility`
- `duplicates`
- `risk_level`
- `next_action`

### Axe C — Anti-doublon

Qualifier chaque doublon présumé :

- duplication exacte ;
- duplication fonctionnelle ;
- wrapper partiellement redondant ;
- ancien script remplacé ;
- variante nécessaire ;
- faux positif.

Aucune suppression sans preuve et sans test.

### Axe D — Compatibilité

Vérifier les surfaces suivantes :

- Debian / Bash ;
- Windows / PowerShell ;
- WSL ;
- tmux ;
- GitHub Actions ;
- chemins longs ;
- encodage UTF-8 ;
- sorties JSON parseables ;
- exécution remote / mobile lorsque pertinente.

### Axe E — Refactor par batch

Définir de petits lots :

- bornés ;
- isolables ;
- testables ;
- réversibles ;
- documentés ;
- non conflictuels avec les autres machines.

### Axe F — Verrouillage

Chaque batch doit finir par :

- tests ;
- smoke commands ;
- validation JSON si applicable ;
- `git diff --check` ;
- rapport d'impact ;
- décision `PASS / REWORK / BLOCKED`.

## 5_GO_PLAN

GO parent :

```text
GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
```

Sous-flux prévus :

```text
GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01
GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01
GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01
GO_CODE_OPS_OPT_TRADING_CHILD_COMPATIBILITY_MATRIX_01
GO_CODE_OPS_OPT_TRADING_CHILD_SAFE_REFACTOR_BATCH_01
GO_CODE_OPS_OPT_TRADING_CHILD_TEST_LOCK_01
```

Ces sous-GO sont des candidats opératoires. Ils ne sont pas ouverts par ce document.

## 6_FINAL_TARGET

Livrer, au niveau parent :

1. un protocole d'inventaire ;
2. un schéma de registre de code ;
3. une méthode anti-doublon ;
4. une matrice de compatibilité ;
5. un plan de refactor par batch ;
6. un verrouillage test/validation ;
7. des prompts opératoires IDE ;
8. un checkpoint de reprise.

## 7_CANONICAL_STATE

État canonique au démarrage :

- repo : `magikgmo4-ui/opt-trading`
- branche base : `sot/mainline`
- branche chantier : `go/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01`
- base prouvée : `2bf4c03bdd57abe6a5afdaf1b5fc948e0a6ffff6`
- surface : `docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/`
- entrée courte : `docs/index/inbox/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01.md`
- mode : `doc-only`
- mutation code : interdite dans cette passe
- index globaux : non modifiés

NEXT_GO naturel :

```text
GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01
```

## 8_VALIDATED_PLAN

Plan validé pour ce parent :

1. créer le dossier chantier parent ;
2. documenter la cible et les invariants ;
3. créer les protocoles d'audit ;
4. créer le schéma de registre ;
5. créer le protocole anti-doublon ;
6. créer la matrice de compatibilité ;
7. créer le plan de batch refactor ;
8. créer le verrouillage test ;
9. créer les prompts opératoires ;
10. créer l'entrée inbox courte ;
11. ne modifier aucun code.

## 9_SELECTED_SOLUTION

Solution retenue :

> Refactor contrôlé par registre, audit-first, puis refactor par lots.

Motif :

- réduit le risque de casse ;
- évite les suppressions accidentelles ;
- rend les doublons explicitement décidables ;
- préserve la compatibilité multi-machine ;
- crée une base de décision durable pour Cursor/IDE et opérations terminal.

## 10_SELECTED_SETUP

Structure documentaire canonique :

```text
docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/
  00_INITIAL_PROJECT_DOC.md
  10_CODE_INVENTORY_PROTOCOL.md
  20_CODE_REGISTRY_SPEC.md
  30_DEDUP_AUDIT_PROTOCOL.md
  40_COMPATIBILITY_MATRIX.md
  50_REFACTOR_BATCH_PLAN.md
  60_TEST_LOCK_AND_VALIDATION.md
  70_OPERATOR_PROMPTS.md
  80_OPENING_CHECKPOINT.md

docs/index/inbox/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01.md
```

## 11_KEY_DECISIONS

| Sujet | Décision |
|---|---|
| Type | parent GO Code Ops |
| Mode initial | doc-only / audit-first |
| Branche dédiée | oui |
| Registre | obligatoire avant refactor |
| Anti-doublon | obligatoire avant allègement |
| Suppression | interdite sans preuve + test |
| Renommage | interdit sans migration |
| Compatibilité | matrice obligatoire |
| Tests | verrouillage avant batch |
| Index globaux | non modifiés dans cette passe |

## 12_INVARIANTS

- Ne pas refactorer sans inventaire.
- Ne pas supprimer sans preuve d'inutilité.
- Ne pas fusionner deux scripts sans identifier les consommateurs.
- Ne pas changer une CLI sans adapter les runbooks/tests.
- Ne pas optimiser sans métrique.
- Ne pas mélanger ce parent avec un chantier produit.
- Ne pas traiter une branche comme source produit.
- Ne pas modifier `GO_INDEX`, `REPRISE`, `ACTIVE_STREAMS`, `NEXT_GO_CANDIDATES` ou `BRANCH_STATE` sans justification explicite.

## 13_ESTABLISHED

- Le chantier est un refactor structurant.
- Le registre est la première pièce durable.
- L'anti-doublon est un audit, pas une suppression.
- La compatibilité est une surface de validation, pas une note secondaire.
- Le premier lot doit produire des preuves documentaires avant toute mutation code.

## 14_HYPOTHESIS

À valider par l'inventaire :

- plusieurs scripts peuvent remplir des rôles proches ;
- certains validateurs peuvent partager une logique commune ;
- certains fichiers peuvent être obsolètes ;
- certains noms ou sorties ne sont pas uniformes ;
- certains chemins ou shells ne sont pas portables ;
- certains tests peuvent manquer pour verrouiller un futur refactor.

## 15_REMAINING_GAP

Manquent encore après ouverture parent :

- inventaire réel des fichiers ;
- registre rempli ;
- détection de doublons prouvés ;
- matrice de compatibilité renseignée par tests ;
- liste priorisée des premiers batchs ;
- décision sur les sous-GO à ouvrir.

## 16_TODO

Actions suivantes :

1. reprendre depuis `sot/mainline` à jour ;
2. ouvrir `GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01` ;
3. produire l'inventaire réel sans mutation ;
4. remplir le registre initial ;
5. qualifier les doublons suspects ;
6. proposer le premier batch sûr.

## 17_RESUME_POINT

Reprise opérationnelle :

```text
Reprendre GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01 depuis docs/chantiers/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01/00_INITIAL_PROJECT_DOC.md.
Le parent est ouvert en doc-only. Ne pas modifier le code.
NEXT_GO = GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01.
```

## 18_TO_DOCUMENT

Blocs à extraire comme documentation canonique :

- `1_MASTER_TARGET`
- `3_INITIAL_NEED`
- `4_MASTER_PROJECT_PLAN`
- `7_CANONICAL_STATE`
- `8_VALIDATED_PLAN`
- `11_KEY_DECISIONS`
- `12_INVARIANTS`
- `16_TODO`
- `17_RESUME_POINT`

## 19_TO_REMEMBER

### MEM_CANDIDATE

- **Refactor Code Ops audit-first** : les demandes de normalisation, registre, anti-doublon, allègement, efficacité et compatibilité doivent être traitées comme refactor structurant, pas comme nettoyage libre.
- **Registre avant refactor** : aucune suppression, fusion ou optimisation durable sans inventaire, registre, anti-doublon et matrice compatibilité.
- **NEXT_GO code inventory** : premier sous-GO naturel après ouverture parent = `GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01`.

### SAVE_MEMORY

Aucun enregistrement bio automatique demandé.
