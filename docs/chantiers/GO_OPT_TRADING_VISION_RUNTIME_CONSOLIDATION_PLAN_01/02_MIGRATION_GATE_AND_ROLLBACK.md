---
doc_id: GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_PLAN_01_MIGRATION_GATE_AND_ROLLBACK
doc_type: migration_gate
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_PLAN_01
status: draft_for_review
lifecycle_stage: child_migration_gate
parent_go_id: GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01
topic_keys:
  - opt-trading
  - vision
  - rollback
  - migration-gate
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_PLAN_01/02_MIGRATION_GATE_AND_ROLLBACK.md
point_de_reprise: "Definir les conditions minimales avant toute migration runtime VISION."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_PLAN_01/01_RUNTIME_TOPOLOGY.md
---

# 02_MIGRATION_GATE_AND_ROLLBACK

## 1_MIGRATION GATE

Toute migration runtime future est BLOQUEE tant que les points suivants ne sont pas prouvés :

```text
G1. liste complete des services/timers
G2. liste complete des chemins shared_files
G3. liste complete des producers de captures
G4. preuve que Telegram / Desk Pro ne cassent pas
G5. strategy de rollback testee sur papier
```

## 2_ROLLBACK MINIMAL A PRODUIRE AU GO SUIVANT

```text
- sauvegarde des unit files
- sauvegarde des scripts de lancement
- sauvegarde des chemins de config
- restauration des alias shell precedents
- procedure d'arret/reprise des services
```

## 3_NEXT_GO D'IMPLEMENTATION (SEULEMENT APRES PLAN)

```text
GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01
```
