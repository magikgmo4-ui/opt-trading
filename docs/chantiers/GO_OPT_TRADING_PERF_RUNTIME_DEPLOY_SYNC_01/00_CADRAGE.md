---
doc_id: GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01
topic_keys:
  - opt-trading
  - perf
  - runtime
  - deploy-sync
  - audit
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01/00_CADRAGE.md
point_de_reprise: "Préparer le réalignement contrôlé de /opt/trading avec origin/sot/mainline avant toute reprise de la preuve runtime PERF."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_GATE_01/90_CLOSEOUT.md
---

# 00_CADRAGE — GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01

## 1_MASTER_TARGET

Préparer le réalignement contrôlé de la surface runtime réelle `/opt/trading` avec l'état canonique pertinent de `origin/sot/mainline`, afin de pouvoir reprendre ensuite la preuve runtime de la DB PERF canonique.

## 2_CONTEXTE

```text
Le blocage PERF n'est plus seulement documentaire.
La surface runtime réelle /opt/trading est désynchronisée.

Conséquences directes :
- launchers runtime encore sur `perf.perf_app:app`
- dossier canonique `modules/perf/data/` absent sur /opt/trading
- `perf/perf.db` existe encore réellement
- toute preuve runtime collectée sur /opt/trading est polluée par ce drift
```

## 3_SCOPE

```text
INCLUS :
- audit Git read-only de /opt/trading
- audit de l'état runtime PERF réel
- plan de sync contrôlé
- analyse de risques
- rollback plan documentaire

EXCLUS :
- git reset
- git pull
- git rebase
- checkout mainline sur /opt/trading
- restart service
- suppression de perf/perf.db
- toute mutation runtime
```

## 12_INVARIANTS

```text
- audit/plan only
- no mutation
- no reset
- no pull/rebase aveugle
- no service change
- no DB move
- no secret touch
```

## 17_RESUME_POINT

```text
GO ouvert pour documenter le drift réel de /opt/trading et produire un plan de réalignement sûr.
Aucune mutation runtime dans ce lot.
```

## RISKS

- À qualifier.
