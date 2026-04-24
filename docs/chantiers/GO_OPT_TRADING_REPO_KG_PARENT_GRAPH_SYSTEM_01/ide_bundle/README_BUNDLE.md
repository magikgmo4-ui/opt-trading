---
doc_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01_IDE_BUNDLE_README
doc_type: ide_bundle_readme
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
status: OPEN
lifecycle_stage: test_bundle
topic_keys:
  - repo-graph
  - ide-bundle
  - tests
  - producer
  - consumer
search_tags:
  - bundle:ide
  - tests:concrete
  - source:repo
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/05_master_plan_final_product.md
point_de_reprise: "Lancer 01_GO_PROMPT_TESTS_ULTRA_CONCRETS.md dans l'IDE"
created_at: 2026-04-24
---

# IDE Bundle — Repo KG Tests Ultra Concrets

## Objet

Ce bundle IDE prépare une mission de tests concrets pour le chantier :

```text
GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
```

But : transformer le cadrage Repo KG en protocole de validation exécutable, basé sur l'état réel du repo `opt-trading`.

## Sources lues / respectées

- `modules/validated_prompt_factory/output/prompt_bundle_transfer.txt`
- `docs/master_pack/mission_starter_pack/01_mission_template.md`
- `docs/master_pack/mission_starter_pack/02_validation_checklist.md`
- `docs/ot/trae/08_MULTI_STEP_MISSION_CHECKLIST_V1.txt`
- `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/05_master_plan_final_product.md`
- `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/06_graph_schema_v1.md`
- `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/07_producer_spec_v1.md`
- `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/08_consumer_ace_kg_method_v1.md`
- `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/09_graph_views_v1.md`
- `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/12_indexation_alignment_gap_and_patch.md`

## Fichiers du bundle

```text
ide_bundle/
├─ README_BUNDLE.md
├─ 00_BUNDLE_MANIFEST.md
├─ 01_GO_PROMPT_TESTS_ULTRA_CONCRETS.md
├─ 02_TEST_PLAN_REPO_KG.md
├─ 03_ACCEPTANCE_CHECKLIST.md
├─ 04_EXPECTED_OUTPUTS.md
└─ 05_OPERATOR_NOTES.md
```

## Règles

- Ne pas modifier les surfaces souveraines `GO_INDEX.md`, `BRANCH_STATE.md`, `REPRISE.md` pendant les tests.
- Ne pas scanner `.env`, tokens, secrets, clés, données privées.
- Ne pas implémenter le Producer complet dans ce bundle.
- Produire uniquement des preuves de tests et specs d'acceptation.

## Point de reprise

Lancer dans l'IDE :

```text
01_GO_PROMPT_TESTS_ULTRA_CONCRETS.md
```
