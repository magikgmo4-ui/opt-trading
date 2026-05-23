---
doc_id: GO_OPT_TRADING_BUNDLES_TARGET_MASTER_TARGET_METHOD_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: bundles
go_id: GO_OPT_TRADING_BUNDLES_TARGET_MASTER_TARGET_METHOD_01
status: draft
lifecycle_stage: method_canonization
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-21
topic_keys:
  - opt-trading
  - bundles
  - targets
  - master_target
  - patch_transport
  - ide
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_BUNDLES_TARGET_MASTER_TARGET_METHOD_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/governance/BUNDLE_TARGET_AND_MASTER_TARGET_METHOD_01.md
  - bundles/BUNDLE_TARGET_INDEX.md
  - bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/TARGETS.md
  - bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/bundle_meta/target_card.json
  - docs/index/inbox/GO_OPT_TRADING_BUNDLES_TARGET_MASTER_TARGET_METHOD_01.md
---

# GO_OPT_TRADING_BUNDLES_TARGET_MASTER_TARGET_METHOD_01

## 1_MASTER_TARGET

Canoniser la relation `plan validé -> target -> master_target -> bundle -> patch -> IDE -> évaluation`.

## 2_INITIAL_PROJECT_DOC

Ce chantier ajoute une couche de ciblage opérationnel pour les bundles produits en session conversationnelle.

Il ne modifie pas les index globaux. Il complète la méthode `.patch` en imposant que chaque bundle ait un `target_id`, un `target_status`, un `master_target_id`, des critères de complétion et une décision après target atteint.

## 3_INITIAL_NEED

Chaque plan validé doit venir avec un target. Ce target appartient à un master target. Quand le target d'un bundle est atteint, il faut évaluer si le master target est atteint ou si un prochain target/bundle doit être produit.

## 4_MASTER_PROJECT_PLAN

1. Créer la méthode `BUNDLE_TARGET_AND_MASTER_TARGET_METHOD_01`.
2. Créer un index léger `bundles/BUNDLE_TARGET_INDEX.md`.
3. Ajouter `TARGETS.md` au bundle IDE déportable.
4. Ajouter `bundle_meta/target_card.json`.
5. Créer une entrée inbox locale.
6. Ne pas modifier les index globaux.

## 6_FINAL_TARGET

Après ce patch, tout nouveau bundle doit pouvoir répondre à :

```text
Quel target vise ce bundle?
À quel master target appartient-il?
Comment sait-on que le target est atteint?
Le master target est-il atteint?
Quel est le prochain bundle si non?
Faut-il proposer un batch d'index globaux?
```

## 7_CANONICAL_STATE

La méthode `.patch` existe comme transport session -> IDE.

Cette couche ajoute la décision post-application : target atteint -> master target atteint ou next target/bundle.

## 11_KEY_DECISIONS

- Un plan validé doit définir un target.
- Un target doit être rattaché à un master target.
- Le target est atteint seulement si les critères de complétion sont validés.
- Après target atteint, évaluer le master target.
- Si le master target n'est pas atteint, produire le prochain target/bundle.
- Si le master target est atteint ou l'horizon change, proposer un batch d'index globaux.

## 12_INVARIANTS

- No runtime.
- No trading live.
- No global indexes.
- No target sans master target.
- No bundle sans target card.
- No index global pour target interne seulement.

## 17_RESUME_POINT

```text
GO_OPT_TRADING_BUNDLES_TARGET_MASTER_TARGET_METHOD_01

État:
patch additif prêt pour target/master_target des bundles.

Prochaine action:
appliquer, valider, commit.

Interdits:
index globaux, runtime, trading live, secrets.
```
