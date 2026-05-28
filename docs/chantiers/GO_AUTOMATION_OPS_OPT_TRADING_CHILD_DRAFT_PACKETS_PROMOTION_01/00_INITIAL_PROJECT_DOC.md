---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_DRAFT_PACKETS_PROMOTION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: automation_ops
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_DRAFT_PACKETS_PROMOTION_01
parent_go_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_SEMIAUTO_RUNTIME_PILOT_01
status: open
lifecycle_stage: in_progress
topic_keys:
  - opt-trading
  - automation_ops
  - job_packets
  - promotion
  - jobs_registry
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-28
working_branch: go/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_DRAFT_PACKETS_PROMOTION_01
links:
  - docs/registry/JOBS_REGISTRY.md
  - scripts/ai/workers/job_packets/
  - scripts/ai/workers/models.registry.json
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_JOBS_REGISTRY_PILOT_02/40_GAPS_AND_NEXT_GO.md
---

# GO_AUTOMATION_OPS_OPT_TRADING_CHILD_DRAFT_PACKETS_PROMOTION_01

## 1_OBJECTIF

Qualifier les 20 job_packets `DRAFT_ONLY` analysables et appliquer les verdicts :
- Promouvoir en `candidate` les packets prêts.
- Déprécier les packets liés à des workers `RETIRED`.
- Documenter les packets bloqués par un chantier parent non fermé (`pending_parent`).
- Mettre à jour `docs/registry/JOBS_REGISTRY.md` en conséquence.

## 2_CONTEXTE

`GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_JOBS_REGISTRY_PILOT_02` (PR #931) a identifié
17-22 job_packets DRAFT_ONLY et déclenché ce GO (décision D1 opérateur, 2026-05-28).

`GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01` (fermé) avait classifié B02 comme
`FALSE_POSITIVE/KEEP — formalize_schema : candidats en attente d'un GO dédié`. Ce GO est ce GO dédié.

## 3_PÉRIMÈTRE

Source : `scripts/ai/workers/job_packets/` (30 fichiers totaux).
Analysés : ~20 DRAFT_ONLY (hors TEST_NEGATIVE, TEST_POSITIVE, WRITE_GATED opérationnel, E2E).

## 4_CONTRAINTES

- Aucune modification de packet en dehors du champ `status`.
- Aucune modification des chantiers parents (POOL_EXTENSION, RUNTIME_LOCK, DOC_OPS_PATCH_ZIP).
- `docs/registry/JOBS_REGISTRY.md` mis à jour uniquement après gate humain.
- Gate humain obligatoire avant toute promotion ou dépréciation.

## 5_LIVRABLES

```
docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_DRAFT_PACKETS_PROMOTION_01/
  00_INITIAL_PROJECT_DOC.md         ← ce fichier
  10_PACKET_INVENTORY.md            ← inventaire complet par famille
  20_QUALIFICATION_TABLE.md         ← verdict par packet
  30_PROOF_INDEX.md                 ← proof pilote semi-auto
  40_GAPS_AND_NEXT_GO.md

artifacts/automation_ops/semiauto_pilot/pilot_<run_id>/
  proof.json
  proof_summary.md
```

## 6_CRITÈRES_DE_FERMETURE

```
- Inventaire complet (10_PACKET_INVENTORY.md)
- Table de qualification (20_QUALIFICATION_TABLE.md) avec verdicts confirmés
- JOBS_REGISTRY.md mis à jour : promotions + dépréciations appliquées
- Pilot proof PASS_DRY_RUN présente
- 17/17 tests PASS
- git diff --check clean
```
