---
doc_id: GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01_CLOSEOUT
doc_type: closeout
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01
status: final
lifecycle_stage: closeout
parent_go_id: GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_IMPL_01
topic_keys:
  - opt-trading
  - perf
  - closeout
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01/90_CLOSEOUT.md
point_de_reprise: "Copie DB canonique effectuée. G1 et G3 prouvés. G4 partiel. Legacy conservé."
updated_at: 2026-05-11
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01/01_DB_COPY_LOG.md
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01/02_DB_CANON_PROOF.md
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01/03_LAUNCHER_RUNTIME_PROOF.md
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01/04_LEGACY_WRITE_ABSENCE_PROOF.md
---

# 90_CLOSEOUT — PERF_DB_CANON_COPY_AND_PROOF_01

## 1_VERDICT

```text
VERDICT = PARTIAL
```

## 2_RESULTAT

```text
G1 — DB canonique réelle      : PROUVÉ
G3 — launchers canon-ready     : PROUVÉ
G4 — absence écritures legacy  : PARTIAL (legacy conservé comme safety net)
```

## 3_ETAT CANONIQUE ATTEINT

```text
/opt/trading/modules/perf/data/perf.db
  size  : 36864
  md5   : e2a92f3aa630fde1e59fb4ef88b5666c
  identique a perf/perf.db

/opt/trading/perf/perf.db
  conserve intact

Launchers :
  modules.perf.app:app avec resolve_perf_db_path
  preference automatique pour la DB canonique
```

## 4_DECISION

```text
G1 et G3 sont maintenant satisfaits.
G4 reste partiel car le legacy est conserve comme fallback protégeant
contre les régressions.

GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_IMPL_01 peut maintenant être ouvert,
mais avec la contrainte que le legacy ne doit être retiré qu'après
une période de preuve runtime réelle sans écriture sur perf/perf.db.
```

## 5_NEXT_GO

```text
GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_IMPL_01
```

Condition :

```text
période d'observation runtime réelle avant retrait du legacy.
```
