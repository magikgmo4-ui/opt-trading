---
doc_id: GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01_TARGETS
doc_type: bundle_targets
repo: opt-trading
project: opt-trading
module: bundles
go_id: GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01
status: draft
lifecycle_stage: target_tracking
surface: bundles
source_kind: operational
updated_at: 2026-05-21
topic_keys:
  - opt-trading
  - bundle
  - target
  - master_target
  - ide
reference_canonique_principale: bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/TARGETS.md
point_de_reprise: "17_RESUME_POINT"
links:
  - bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/bundle_meta/target_card.json
  - bundles/BUNDLE_TARGET_INDEX.md
  - docs/governance/BUNDLE_TARGET_AND_MASTER_TARGET_METHOD_01.md
---

# TARGETS — GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01

## 1_MASTER_TARGET

```text
MASTER_TARGET_SESSION_TO_IDE_PATCH_TRANSPORT_01
```

Horizon :

```text
Rendre la session conversationnelle capable de produire des chantiers Git transportables par patch, puis applicables par IDE avec une matrice unique sans reconstruction du plan.
```

## 6_FINAL_TARGET — target du bundle

```text
TARGET_IDE_DEPORTABLE_PATCH_APPLICATION_MATRIX_01
```

Objectif concret :

```text
Fournir un bundle IDE déportable contenant la matrice d'application patch, les prompts/checklists/templates, la méthode de dépôt racine -> bootstrap -> bundles/<GO_ID>/patches/, et les scripts d'application.
```

## Target status courant

```text
ready_for_ide
```

## Critères de complétion

Le target est atteint seulement si :

- le patch est appliqué localement;
- le patch racine n'est pas committé;
- le patch canonique est conservé sous `bundles/<GO_ID>/patches/`;
- `git diff --check` est PASS;
- le commit local existe;
- la vérification avant push est PASS;
- la PR est ouverte;
- la review est conforme;
- le merge est fait ou explicitement non requis.

## Après target atteint

Évaluer :

```text
master_target_reached?
next_bundle_candidate?
global_index_update_candidate?
```

## Décision initiale

```text
master_target_status = partially_reached
global_index_update_candidate = false
next_bundle_candidate = TBD_AFTER_FIRST_IDE_USE
```

Raison : le premier bundle pose la méthode. Le master target sera atteint seulement après usage réel validé sur au moins un patch appliqué par IDE.

## 17_RESUME_POINT

```text
Bundle prêt pour IDE.

Prochaine action:
utiliser ce bundle sur un patch réel, puis statuer target_reached et master_target_status.
```
