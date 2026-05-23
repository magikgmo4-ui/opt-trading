---
doc_id: OPT_TRADING_BUNDLE_TARGET_AND_MASTER_TARGET_METHOD_01
doc_type: governance_method
repo: opt-trading
project: opt-trading
module: bundles
go_id: GO_OPT_TRADING_BUNDLES_TARGET_MASTER_TARGET_METHOD_01
status: draft
lifecycle_stage: governance_candidate
surface: governance
source_kind: canonical_candidate
updated_at: 2026-05-21
topic_keys:
  - opt-trading
  - bundles
  - target
  - master_target
  - patch_transport
  - ide
reference_canonique_principale: docs/governance/BUNDLE_TARGET_AND_MASTER_TARGET_METHOD_01.md
point_de_reprise: "Section 8 - Chaîne canonique"
links:
  - docs/governance/SESSION_PATCH_TRANSPORT_METHOD_01.md
  - docs/governance/GLOBAL_INDEX_UPDATE_TRIGGER_RULE_01.md
  - bundles/BUNDLE_TARGET_INDEX.md
---

# BUNDLE_TARGET_AND_MASTER_TARGET_METHOD_01

## 1. Objet

Définir la relation canonique entre :

```text
plan validé
-> target
-> master_target
-> bundle
-> .patch GitHub
-> instruction IDE
-> évaluation target/master_target
```

## 2. Principe

Un plan validé ne devient pas seulement un texte ou un patch.

Un plan validé devient :

```text
TARGET_CARD + chantier + bundle + .patch + instruction IDE
```

## 3. Définitions

| Terme | Sens |
|---|---|
| `target` | objectif concret et vérifiable du bundle courant |
| `master_target` | horizon supérieur auquel le target contribue |
| `bundle` | paquet opérable pour IDE/opérateur |
| `.patch` | artefact de transport session -> Git |
| `target_reached` | target local atteint selon critères explicites |
| `master_target_reached` | horizon atteint, testé ou utilisable réellement |
| `next_bundle_candidate` | prochain bundle si le master target n'est pas atteint |

## 4. Emplacements canoniques

```text
bundles/BUNDLE_TARGET_INDEX.md
bundles/<GO_ID>/TARGETS.md
bundles/<GO_ID>/bundle_meta/target_card.json
bundles/<GO_ID>/patches/<YYYYMMDD>_<GO_ID>_<slug>.patch
```

## 5. Champs obligatoires `target_card.json`

```json
{
  "go_id": "<GO_ID>",
  "bundle_id": "<GO_ID>_bundle",
  "target_id": "<TARGET_ID>",
  "target_label": "<objectif concret du bundle>",
  "target_status": "planned|ready_for_ide|applied|validated|committed|pr_open|merged|target_reached|blocked|superseded",
  "master_target_id": "<MASTER_TARGET_ID>",
  "master_target_label": "<horizon plus large>",
  "master_target_status": "not_reached|partially_reached|reached|blocked|needs_next_bundle",
  "target_completion_criteria": [],
  "after_target_reached": {
    "evaluate_master_target": true,
    "next_bundle_candidate": "<GO_ID|null>",
    "global_index_update_candidate": false
  }
}
```

## 6. Évaluation après bundle

Quand un bundle atteint son target :

1. relire `TARGETS.md`;
2. relire `bundle_meta/target_card.json`;
3. vérifier les critères de complétion;
4. statuer `target_status`;
5. évaluer `master_target_status`;
6. si master target atteint : proposer batch d'index globaux;
7. si master target non atteint : produire prochain target/bundle;
8. si horizon change : proposer update global via batch.

## 7. Chaîne canonique

```text
PLAN_VALIDÉ_CHAIN:
plan validé -> définir target + master_target -> produire bundle + .patch canonique -> utilisateur dépose patch à la racine -> IDE lit bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/docs/EXEMPLE_MATRICE_APPLICATION_PATCH.md -> IDE applique/valide/commit/push/PR/review -> évaluer target atteint -> évaluer master_target atteint ou prochain bundle.
```

## 8. Règle index globaux

```text
GLOBAL_INDEX_RULE:
les index globaux changent seulement si le master target ou l'horizon change réellement. Sinon parent local + inbox + bundle target status.
```

## 9. Anti-confusion

| Élément | Ne signifie pas automatiquement |
|---|---|
| patch produit | target atteint |
| patch appliqué | master target atteint |
| commit local | produit fini |
| parent fermé | horizon terminé |
| PR mergée | besoin global clos |
| target interne atteint | index global à modifier |

## 10. Formule de décision

```text
Si target atteint et master_target non atteint:
  produire le prochain target/bundle.

Si target atteint et master_target atteint:
  proposer batch d'agrégation index globaux.

Si target bloqué:
  documenter blocker + next target ou remediation bundle.
```

## 11. Mémoire canonique courte

```text
Plan validé = target défini = rattachement master_target = chantier/bundle = .patch GitHub canonique = IDE lit la matrice réelle = target évalué = master_target évalué.
```
