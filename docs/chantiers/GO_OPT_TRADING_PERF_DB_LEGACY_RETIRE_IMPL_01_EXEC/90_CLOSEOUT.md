---
doc_id: GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_IMPL_01_EXEC_CLOSEOUT
doc_type: closeout
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_IMPL_01_EXEC
status: final
lifecycle_stage: closeout
parent_go_id: GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01
topic_keys:
  - opt-trading
  - perf
  - closeout
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_IMPL_01_EXEC/90_CLOSEOUT.md
point_de_reprise: "Legacy PERF DB retiré proprement. Toutes les gates sont satisfaites."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_IMPL_01_EXEC/00_CADRAGE.md
---

# 90_CLOSEOUT — PERF_DB_LEGACY_RETIRE_IMPL_01

## 1_VERDICT

```text
VERDICT = PASS
```

## 2_RESULTAT

```text
Implantation livrée :
- perf_db_relocate.sh : retire / unretire
- modules/perf/README.md : doc retire

Exécution sur /opt/trading :
- legacy DB renommé en perf/perf.db.retired_20260512_000848
- canonical DB seul actif : modules/perf/data/perf.db (36864 bytes)
- rollback possible via unretire

Toutes les gates PERF DB sont maintenant satisfaites :
- G1 PROUVÉ : DB canonique réelle
- G3 PROUVÉ : launchers canon-ready
- G4 PROUVÉ : legacy retiré (renommé, non détruit)
```

## 3_ROLLBACK

```text
bash modules/perf/scripts/perf_db_relocate.sh unretire
```

## 4_CHAINE PERF BOUCLEE

```text
restructure plan → canonical shims impl
→ path switch plan → path switch impl
→ DB relocation plan → DB relocation impl
→ DB path switch impl
→ DB legacy retire gate → DB canon proof collection
→ DB canon runtime proof → runtime deploy sync plan
→ runtime deploy sync impl
→ DB canon copy and proof
→ DB legacy retire impl ✓
```
