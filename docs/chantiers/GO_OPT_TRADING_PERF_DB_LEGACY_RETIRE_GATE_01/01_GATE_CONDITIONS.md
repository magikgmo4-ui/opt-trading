---
doc_id: GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_GATE_01_GATE_CONDITIONS
doc_type: gate_conditions
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_GATE_01
status: draft_for_review
lifecycle_stage: child_gate_conditions
parent_go_id: GO_OPT_TRADING_PERF_DB_PATH_SWITCH_IMPL_01
topic_keys:
  - opt-trading
  - perf
  - db
  - gate
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_GATE_01/01_GATE_CONDITIONS.md
point_de_reprise: "Conditions minimales avant retrait du fallback legacy PERF DB."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_GATE_01/00_CADRAGE.md
---

# 01_GATE_CONDITIONS

## 1_CONDITIONS

```text
G1. la DB canonique existe réellement sur les environnements cibles
G2. PERF_DB_PATH n'est plus nécessairement legacy pour démarrer
G3. les launchers ont tourné de façon stable sur la DB canonique
G4. aucune écriture résiduelle n'est observée sur perf/perf.db
G5. rollback documenté si une vieille automation réveille encore le legacy
```

## 2_PROOFS ATTENDUES

```text
- logs de démarrage avec PERF_DB_PATH canonique
- preuve /perf/ui et /desk OK après switch
- preuve que les écritures vont bien vers la DB canonique
- absence de dépendance shell restante au chemin legacy
```
