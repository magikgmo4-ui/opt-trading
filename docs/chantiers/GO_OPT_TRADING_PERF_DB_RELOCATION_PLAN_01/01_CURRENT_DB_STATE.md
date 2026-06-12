---
doc_id: GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01_CURRENT_DB_STATE
doc_type: current_db_state
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01
status: draft_for_review
lifecycle_stage: child_current_state
parent_go_id: GO_OPT_TRADING_PERF_PATH_SWITCH_IMPL_01
topic_keys:
  - opt-trading
  - perf
  - db
  - current-state
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01/01_CURRENT_DB_STATE.md
point_de_reprise: "Documenter l'état actuel de perf.db et de son chemin."
updated_at: 2026-05-07
links:
  - perf/perf_app.py
---

# 01_CURRENT_DB_STATE

## 1_ETAT ACTUEL

```text
DB path current default:
  perf/perf.db

Code source:
  DB_PATH = os.getenv("PERF_DB_PATH", os.path.join(APP_DIR, "perf.db"))

Conséquence:
  - la DB vit à côté de perf/perf_app.py
  - le chemin peut déjà être overridé par env
  - aucun switch de chemin n'est nécessaire pour faire fonctionner le runtime actuel
```

## 2_TABLES CONNUES

```text
tables:
  - events
  - trades

pragmas:
  - journal_mode=WAL
  - synchronous=NORMAL
  - busy_timeout=5000
  - foreign_keys=ON
```

## 3_RISQUES DE L'ETAT ACTUEL

```text
- code et data cohabitent dans perf/
- scripts externes peuvent supposer perf/perf.db implicitement
- un move brut peut casser l'historique ou créer deux DB concurrentes
```

## RISKS

- À qualifier.
