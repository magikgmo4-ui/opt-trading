---
doc_id: GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01
doc_type: child_go
repo: opt-trading
project: opt-trading
module: bundles
go_id: GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01
parent_go: GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01
status: draft
lifecycle_stage: bundle_application
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-21
topic_keys:
  - opt-trading
  - bundles
  - ide
  - deportable
  - no_friction
  - doc_only
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/01_BUNDLE_STORAGE_METHOD.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/04_BUNDLE_IMPLEMENTATION_METHOD.md
  - bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/README_BUNDLE.md
  - bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/patches/README_PATCHES.md
  - docs/index/inbox/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01.md
---

# GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01

## 1_MASTER_TARGET

Créer un bundle IDE déportable, conforme à la méthode existante `bundles/<GO_ID>/`, pour réduire le travail IDE futur en transférant le maximum de cadrage, prompts, checklists, templates et patchs depuis la session conversationnelle.

## 2_INITIAL_PROJECT_DOC

Ce document applique la méthode canonique existante du parent `GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01`.

Il ne crée pas une nouvelle doctrine. Il produit un bundle opérable qui sert de paquet standard pour préparer le travail IDE en amont.

## 3_INITIAL_NEED

L'utilisateur veut maximiser la production faite en session conversationnelle afin de limiter la charge IDE, éviter les frictions avec l'existant, et réduire les contradictions, doublons, fourches et écarts.

## 4_MASTER_PROJECT_PLAN

1. Rattacher le travail au parent bundles existant.
2. Créer un bundle dans `bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/`.
3. Fournir prompts, checklists, templates et patchs de transport.
4. Garder le changement strictement doc-only.
5. Ne pas modifier les index globaux.
6. Fournir une entrée inbox courte.
7. Laisser l'IDE appliquer, valider et committer.

## 5_GO_PLAN

Le bundle contient :

- prompts IDE ;
- checklists exécution / validation / anti-friction ;
- templates patch plan / PR review / CI triage / reprise ;
- manifest ;
- validation report ;
- dossier `patches/` pour conserver les patchs de transport.

## 6_FINAL_TARGET

Un opérateur IDE peut reprendre sans relire toute la conversation :

- quoi faire ;
- quels fichiers toucher ;
- quelles surfaces éviter ;
- quelles validations lancer ;
- où déposer les patchs téléchargés ;
- où les patchs doivent être stockés après bootstrap ;
- quand s'arrêter ;
- quoi retourner à la session conversationnelle.

## 7_CANONICAL_STATE

Le repo possède déjà une méthode canonique pour les bundles sous `GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01`.

Ce GO est une application de cette méthode, pas une couche concurrente.

## 8_VALIDATED_PLAN

Le bundle est créé sous :

```text
bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/
```

La documentation de rattachement est créée sous :

```text
docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01.md
```

L'indexation légère est créée sous :

```text
docs/index/inbox/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01.md
```

## 9_SELECTED_SOLUTION

Créer un bundle doc-only minimal mais opérable :

```text
README_BUNDLE.md
prompts/
checklists/
docs/
patches/
bundle_meta/
```

Aucun script destructif n'est ajouté dans le bundle. Les scripts génériques vivent sous `tools/session_transport/`.

## 10_SELECTED_SETUP

Mode :

```text
ide_bundle + doc_bundle + patch_transport
```

Scope Git :

```text
go/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01
```

## 11_KEY_DECISIONS

- Réutiliser la doctrine bundle existante.
- Ne pas créer de doctrine concurrente.
- Ne pas modifier les index globaux.
- Ne pas toucher au runtime.
- Préférer un patch Git appliquable localement.
- Garder l'IDE en mode exécution / validation / commit.
- Déposer les patchs téléchargés à la racine du repo comme inbox temporaire.
- Déplacer les patchs dans `bundles/<GO_ID>/patches/` via bootstrap avant conservation durable.

## 12_INVARIANTS

- Doc-only.
- No secrets.
- No runtime.
- No trading live.
- No global indexes.
- No refactor.
- No new sovereign doctrine.
- No duplicate bundle method.
- No root-level patch committed.

## 13_ESTABLISHED

- Le parent bundle existe.
- La méthode `bundles/<GO_ID>/` existe.
- L'utilisateur valide l'approche de déporter davantage le travail IDE vers la session conversationnelle.
- Un patch local peut réduire encore la charge IDE.
- La racine du repo sert de zone d'entrée temporaire pour les patchs téléchargés.

## 14_HYPOTHESIS

- Le bundle sera utilisé comme paquet standard pour les prochains travaux IDE.
- Les prompts/checklists/templates peuvent devenir une base réutilisable pour plusieurs GO.
- Le bootstrap des patchs évitera les patchs orphelins à la racine.

## 15_REMAINING_GAP

- Appliquer le patch localement.
- Lancer les validations.
- Committer.
- Ouvrir une PR si souhaité.
- Éventuellement généraliser le bundle après premier usage.

## 16_TODO

1. Placer le patch final téléchargé à la racine du repo local.
2. Appliquer le patch final avec `git apply --check` puis `git apply`.
3. Si d'anciens patchs sont à la racine, utiliser `tools/session_transport/bootstrap_patch_inbox.*`.
4. Vérifier le scope.
5. Lancer `git diff --check`.
6. Inspecter no-secrets.
7. Committer.
8. Retourner le SHA et le statut.

## 17_RESUME_POINT

```text
GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01

État:
patch final combiné préparé en session conversationnelle.

Prochaine action:
déposer le patch final à la racine du repo, appliquer localement, puis bootstrapper tout patch racine restant vers bundles/<GO_ID>/patches/.

Interdits:
index globaux, runtime, trading live, secrets, refactor, patch racine committé.
```
