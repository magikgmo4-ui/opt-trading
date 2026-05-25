---
doc_id: GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01_INITIAL_PROJECT_DOC
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_VISION_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - vision
  - consolidation
  - family
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_module_family_consolidation_audit.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/03_file_role_cartography.md
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/index/BRANCH_STATE.md
  - docs/status/bot_vision_canonique.md
  - docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md
---

# 00_INITIAL_PROJECT_DOC

## Objet

Cartographier la famille `vision` pour fixer, sans mutation runtime, si elle releve :

- d'une lignee versionnee ;
- d'une stack complementaire ;
- d'un legacy encore porteur de runtime ;
- d'un survivant canonique documentaire distinct du survivant operatoire.

## Perimetre

- `modules/bot_vision`
- `modules/bot_vision_step2`
- `modules/vision_bot`

## Sources lues

- `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_module_family_consolidation_audit.md`
- `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/03_file_role_cartography.md`
- `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
- `docs/index/BRANCH_STATE.md`
- `docs/status/bot_vision_canonique.md`
- `docs/governance/BOT_VISION_CANONICAL_PRODUCT_SYNTH_01.md`
- `docs/product/guides/BOT_VISION.md`
- `docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01/01_VISION_CLUSTER_INVENTORY.md`
- `docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01/01_EXISTING_STATE.md`

## Limite constatee en entree

Les references suivantes demandees dans le prompt ne sont pas presentes dans le checkout courant :

- `docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/17_CURRENT_BASELINE_CANONIZATION.md`
- `docs/chantiers/GO_OPT_TRADING_MODULES_EXHAUSTIVE_INVENTORY_01/13_MODULES_NORMALIZED_REGISTRY_CROSSCHECK.csv`

Le lot continue en s'appuyant sur les autres sources canoniques disponibles et sur la lecture directe des modules cibles.

## Questions a trancher

1. Quel module est reellement consomme aujourd'hui ?
2. Quels callers pointent vers `bot_vision` ?
3. Quels callers pointent vers `bot_vision_step2` ?
4. Quels callers pointent vers `vision_bot` ?
5. L'ensemble est-il une lignee versionnee ou une stack complementaire ?
6. Quel module devient survivant documentaire ?
7. Quelle action registry sera requise ensuite ?
8. Quel GO physique/runtime restera necessaire ?

## Contraintes appliquees

- mode `doc-only`
- aucune suppression
- aucun refactor runtime
- aucune mutation de `registry/modules_registry.yaml`
- aucun re-audit global
- machine_owner: `admin-trading`

## Verdict attendu

`PASS` si la famille peut etre clarifiee par role et action registry differee.
