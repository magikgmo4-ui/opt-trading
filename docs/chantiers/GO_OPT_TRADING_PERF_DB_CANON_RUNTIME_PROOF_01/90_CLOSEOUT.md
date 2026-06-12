---
doc_id: GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01_CLOSEOUT
doc_type: closeout
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01
status: final
lifecycle_stage: closeout
parent_go_id: GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01
topic_keys:
  - opt-trading
  - perf
  - closeout
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01/90_CLOSEOUT.md
point_de_reprise: "Preuves runtime réelles PERF collectées : retrait legacy toujours bloqué."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01/01_RUNTIME_DB_RESOLUTION_PROOF.md
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01/02_LAUNCHER_RUNTIME_PROOF.md
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01/03_LEGACY_WRITE_RUNTIME_PROOF.md
---

# 90_CLOSEOUT — GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01

## 1_VERDICT

```text
VERDICT = BLOCKED
```

## 2_RESULTAT

```text
G1 : NON PROUVÉ
  /opt/trading/modules/perf/data/ est absent, aucune DB canonique réelle observée.

G3 : NON PROUVÉ
  la surface runtime /opt/trading utilise encore des launchers anciens pointant vers perf.perf_app:app.

G4 : NON PROUVÉ
  la DB legacy existe réellement ; aucune preuve durable n'établit l'absence d'écritures résiduelles.
```

## 3_DECISION

```text
GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_IMPL_01 reste BLOQUÉ.
```

## 4_NEXT_GO

```text
GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01
```

Mission du GO suivant :

```text
- réaligner /opt/trading avec l'état canonique pertinent de sot/mainline
- seulement ensuite reprendre la preuve runtime DB canonique
```

## RISKS

- À qualifier.
