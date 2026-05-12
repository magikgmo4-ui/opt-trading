---
doc_id: GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01_RUNTIME_GIT_DRIFT_AUDIT
doc_type: runtime_git_drift_audit
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01
status: draft_for_review
lifecycle_stage: child_runtime_audit
parent_go_id: GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01
topic_keys:
  - opt-trading
  - perf
  - runtime
  - git-drift
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01/01_RUNTIME_GIT_DRIFT_AUDIT.md
point_de_reprise: "Établir exactement l'écart Git de /opt/trading par rapport à origin/sot/mainline."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01/00_CADRAGE.md
---

# 01_RUNTIME_GIT_DRIFT_AUDIT

## 1_SURFACE AUDITÉE

```text
/opt/trading -> /home/fantome/opt-trading
```

## 2_ETAT GIT OBSERVÉ

```text
current branch : go/GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01
HEAD SHA       : f4aaa196cf17c41a93eb8344997e40eab9d9e25c
ahead/behind   : 0 / 232 vs origin/sot/mainline
```

## 3_DIRTY FILES OBSERVÉS

```text
.env.example
docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/06_graph_schema_v1.md
docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/07_producer_spec_v1.md
docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/09_graph_views_v1.md
docs/index/BRANCH_STATE.md
docs/index/GO_INDEX.md
graph_bundle.json
producer_repo_kg_v1.py
```

## 4_DIFF SUMMARY

```text
8 files changed
31887 insertions(+)
23463 deletions(-)
```

## 5_CONCLUSION GIT

```text
/opt/trading n'est pas une surface runtime alignée sur l'état canonique actuel.
Elle est :
- sur une branche ancienne non liée au sujet PERF runtime courant
- en retard de 232 commits
- sale localement

Donc toute preuve runtime collectée sur cette surface doit être traitée comme
preuve d'un runtime désaligné, pas comme preuve de l'état canonique.
```
