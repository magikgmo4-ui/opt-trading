---
doc_id: GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01_CADRAGE
doc_type: cadrage
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
  - db
  - copy
  - proof
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01/00_CADRAGE.md
point_de_reprise: "Copier la DB legacy vers le chemin canonique, puis prouver G1/G3/G4."
updated_at: 2026-05-11
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_IMPL_01/90_CLOSEOUT.md
---

# 00_CADRAGE — PERF_DB_CANON_COPY_AND_PROOF_01

## 1_MASTER_TARGET

Créer la DB PERF canonique par copie non destructive, puis prouver G1, G3 et G4 sur le runtime `/opt/trading` réaligné.

## 2_OPERATIONS

```text
1. precheck runtime alignement et intégrité
2. status du script perf_db_relocate.sh
3. copy non destructive via le script
4. vérification checksums, taille, présence
5. preuve launcher path
6. preuve absence relative d'écritures legacy
```

## 3_GARANTIES

```text
- cp -a (non destructif)
- legacy DB intacte, checksum préservé
- canonical DB = copie identique
- aucun restart service
```
