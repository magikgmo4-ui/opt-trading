---
doc_id: OPT_TRADING_INDEX_INBOX_MACHINE_STUDENT_PARENT_01
doc_type: index_inbox_entry
repo: opt-trading
project: opt-trading
module: machine_student
go_id: GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01
status: applied
lifecycle_stage: inboxed
topic_keys:
  - opt-trading
  - index_inbox
  - machine_student
  - aggregation
  - parent_continuity
search_tags:
  - surface:index_inbox
  - doc_role:index_inbox_entry
  - aggregation:pending
  - index:global_pending
surface: index
source_kind: derived
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/00_START.md
point_de_reprise: "docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/00_START.md"
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/00_START.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/10_MACHINE_SCOPE.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/20_EXISTING_BRANCHES_INVENTORY.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/30_CHILDREN_INDEX.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/40_LOCAL_OLLAMA_LINK.md
---

# INDEX INBOX — GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01

```yaml
go_id: GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01
status: applied
priority: P1
branch: go/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01
parent_ref: docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/00_START.md
last_established: >-
  Parent machine student ouvert doc-only.
  Arbitrage OLLAMA = student applique.
  Branches Local Ollama inventoriees (1 parent + 23 children + 2 connexes).
  GO enfants cadres, reconciliation en P1 immediat.
next_action: >-
  Agreger cette entree inbox dans GO_INDEX, ACTIVE_STREAMS,
  NEXT_GO_CANDIDATES et REPRISE via le batch d'agregation.
  Ouvrir GO_OPT_TRADING_STUDENT_LOCAL_OLLAMA_PARENT_RECONCILIATION_01.
index_patch_ref: none
updated_at: 2026-05-05
aggregation_status: pending
```

## Note

Cette entree inbox est atomique. Elle ne remplace pas les index globaux.
Elle sert a preparer un batch d'agregation sans creer de conflit sur les fichiers globaux volumineux.
