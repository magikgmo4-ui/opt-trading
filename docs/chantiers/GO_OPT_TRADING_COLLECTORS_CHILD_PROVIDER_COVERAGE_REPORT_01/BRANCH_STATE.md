---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01_BRANCH_STATE
doc_type: branch_state
repo: opt-trading
project: opt-trading
module: collectors
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: open
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# BRANCH_STATE

## Branche courante

```
go/GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01
```

## Base (stacking)

```
go/GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
```

Parent PR : #663 — OPEN au 2026-05-23.

## PR cible

- base : `go/GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01`
- head : `go/GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01`

**Ne pas baser sur `sot/mainline` tant que #663 n'est pas mergee.**

## Stacking plan

1. #663 merge dans `sot/mainline` → retarget child PR sur `sot/mainline` ou rebase.
2. Child PR merge dans `sot/mainline` uniquement apres le parent.
3. Ne jamais merger le child avant le parent.

## Fichiers crees dans ce child

```
docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01/
  00_INITIAL_PROJECT_DOC.md
  10_PROVIDER_COVERAGE_REPORT.md
  20_FIXTURE_MATRIX.md
  30_MARKET_METRICS_SCHEMA_TESTS.md
  40_NEXT_PATCHES.md
  BRANCH_STATE.md  ← ce fichier

docs/index/inbox/GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01.md
```

## Verification rapide

```bash
git status --short
git branch --show-current
git diff --name-only origin/go/GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01...HEAD
```

Resultat attendu : uniquement les 7 fichiers listes ci-dessus.

## Prochaine action

Ouvrir la PR child (base = branche parent). Attendre merge de #663 pour retarget.
