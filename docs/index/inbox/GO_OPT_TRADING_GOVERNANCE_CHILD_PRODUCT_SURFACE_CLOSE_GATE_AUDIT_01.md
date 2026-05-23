# GO_OPT_TRADING_GOVERNANCE_CHILD_PRODUCT_SURFACE_CLOSE_GATE_AUDIT_01

Relire les parents actifs et vérifier si leur MASTER_TARGET pointe bien vers un PF_* testable,
ou s’il reste trop abstrait.

## Objectif
Produire un audit de proximité qui vérifie pour chaque parent actif si son MASTER_TARGET déclaré
correspond effectivement à un produit final utilisable (PF_*) testable, ou si le MASTER_TARGET reste
trop abstrait, documentaire ou intermédiaire.

## Contexte
Le registre `PRODUCT_FINAL_SURFACE_REGISTRY_01.md` introduit une couche de classement explicite :
- PF_* = produit/surface finale utilisable de bout en bout
- MASTER_TARGET = horizon supérieur auquel un target contribue

Un écart apparaît quand un parent déclare un MASTER_TARGET qui ne pointe vers aucun PF_* testable,
ce qui rend difficile l’évaluation de la complétion et la décision de closeout.

## Livrable attendu
`docs/governance/PRODUCT_FINAL_SURFACE_CLOSE_GATE_AUDIT_01.md`

## Plan de travail
1. Lister les parents actifs avec un MASTER_TARGET déclaré (via `GO_INDEX.md`, `TARGETS.md`, `target_card.json`)
2. Pour chaque MASTER_TARGET déclaré, vérifier s’il pointe vers un PF_* listé dans 
   `PRODUCT_FINAL_SURFACE_REGISTRY_01.md`
3. Classer les écarts :
   - MASTER_TARGET = PF_* testable → OK
   - MASTER_TARGET = PF_* non testable (documentation uniquement) → à requalifier
   - MASTER_TARGET = abstrait (pas de PF_*) → nécessite correction ou nouveau PF_*
4. Proposer des corrections :
   - requalifier le MASTER_TARGET vers un PF_* existant
   - créer un nouveau PF_* si le domaine manque de représentation
   - ouvrir un nouveau GO pour combler le gap
5. Produire le rapport d’audit avec un tableau de suivi et des recommandations de NEXT_GO

## Liens utiles
- `docs/chantiers/GO_OPT_TRADING_DOC_OPS_TARGET_REGISTRY_FOLLOWUP_01/AUDIT_TARGETS_OPEN_AND_MISIDENTIFIED.md`
- `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md`
- `docs/governance/PRODUCT_FINAL_TARGET_REGISTRY_01.md`
- `docs/index/GO_INDEX.md`
- `bundles/*/bundle_meta/target_card.json`
