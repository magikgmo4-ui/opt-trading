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
1_MASTER_TARGET
-> 4_MASTER_PROJECT_PLAN
-> 6_FINAL_TARGET
-> BUNDLE_TARGET
-> GO_ID / bundle
-> .patch GitHub / .zip de transport si utile
-> instruction IDE
-> évaluation BUNDLE_TARGET / FINAL_TARGET / MASTER_TARGET
```

## 2. Principe

Un plan validé ne devient pas seulement un texte ou un patch.

Un plan validé devient :

```text
TARGET_CARD + chantier + bundle + .patch + instruction IDE
```

## 3. Registre cible applique au bundle

| Niveau | Nom | Sens dans cette méthode |
|---|---|---|
| L0 | `1_MASTER_TARGET` | produit final utilisable, opérationnel, vérifiable et livrable |
| L1 | `4_MASTER_PROJECT_PLAN` | checklist des livrables requis pour fermer proprement le parent |
| L2 | `6_FINAL_TARGET` | résultat attendu de la phase actuelle |
| L3 | `BUNDLE_TARGET` | livrable concret du bundle courant |
| L4 | `GO_ID` | unité d'exécution traçable qui porte le bundle |
| L5 | `NEXT_GO` | suite obligatoire si la target supérieure n'est pas atteinte |

Mapping opérationnel minimal :

- `TARGETS.md` doit expliciter au moins `1_MASTER_TARGET` et `6_FINAL_TARGET`
- dans `target_card.json`, `target_id` / `target_label` portent le `BUNDLE_TARGET`
- dans `target_card.json`, `master_target_id` / `master_target_label` portent le `1_MASTER_TARGET`
- `4_MASTER_PROJECT_PLAN` reste porté par le chantier parent quand une fermeture parent devient recevable

## 4. Emplacements canoniques

```text
bundles/BUNDLE_TARGET_INDEX.md
bundles/<GO_ID>/TARGETS.md
bundles/<GO_ID>/bundle_meta/target_card.json
bundles/<GO_ID>/patches/<YYYYMMDD>_<GO_ID>_<slug>.patch
```

## 5. Champs obligatoires `target_card.json`

Dans ce fichier, le mot `target` désigne le `BUNDLE_TARGET` de niveau L3.

Le `6_FINAL_TARGET` reste documenté dans `TARGETS.md` et le `1_MASTER_TARGET`
reste l'horizon produit auquel le bundle contribue.

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

Quand un bundle atteint son `BUNDLE_TARGET` :

1. relire `TARGETS.md`;
2. relire `bundle_meta/target_card.json`;
3. vérifier les critères de complétion;
4. statuer `target_status` du `BUNDLE_TARGET`;
5. évaluer si le `6_FINAL_TARGET` de la phase est atteint ou reste partiel;
6. évaluer `master_target_status` du `1_MASTER_TARGET`;
7. si le `1_MASTER_TARGET` est atteint : vérifier le `4_MASTER_PROJECT_PLAN` avant toute fermeture parent;
8. si le `1_MASTER_TARGET` n'est pas atteint : produire le prochain `NEXT_GO` ou prochain bundle.

## 7. Chaîne canonique

```text
PLAN_VALIDE_CHAIN:
1_MASTER_TARGET -> 4_MASTER_PROJECT_PLAN -> 6_FINAL_TARGET -> BUNDLE_TARGET -> GO_ID -> bundle + .patch canonique -> utilisateur depose patch a la racine -> IDE lit bundles/GO_OPT_TRADING_BUNDLES_CHILD_IDE_DEPORTABLE_PACK_01/docs/EXEMPLE_MATRICE_APPLICATION_PATCH.md -> IDE applique/valide/commit/push/PR/review -> evaluer BUNDLE_TARGET -> evaluer 6_FINAL_TARGET -> evaluer 1_MASTER_TARGET ou NEXT_GO.
```

## 8. Règle index globaux

```text
GLOBAL_INDEX_RULE:
les index globaux changent seulement si le 6_FINAL_TARGET ou le 1_MASTER_TARGET change reellement l'etat global. Sinon parent local + inbox + statut du BUNDLE_TARGET.
```

## 9. Anti-confusion

| Élément | Ne signifie pas automatiquement |
|---|---|
| patch produit | BUNDLE_TARGET atteint |
| patch appliqué | 6_FINAL_TARGET atteint |
| commit local | produit fini |
| parent fermé | 4_MASTER_PROJECT_PLAN complété |
| PR mergée | 1_MASTER_TARGET atteint |
| target interne atteint | index global à modifier |

## 10. Formule de décision

```text
Si BUNDLE_TARGET atteint et 6_FINAL_TARGET non atteint:
  produire le prochain bundle ou NEXT_GO de phase.

Si 6_FINAL_TARGET atteint mais 1_MASTER_TARGET non atteint:
  ouvrir le prochain NEXT_GO et maintenir le parent ouvert.

Si 1_MASTER_TARGET atteint:
  verifier 4_MASTER_PROJECT_PLAN puis proposer batch d'agregation index globaux ou fermeture parent.

Si BUNDLE_TARGET bloque:
  documenter blocker + next bundle ou remediation.
```

## 11. Mémoire canonique courte

```text
Plan valide = 1_MASTER_TARGET fixe = 6_FINAL_TARGET borne = BUNDLE_TARGET transporte = GO_ID execute = patch canonique applique = BUNDLE_TARGET evalue = 1_MASTER_TARGET rejuge.
```
