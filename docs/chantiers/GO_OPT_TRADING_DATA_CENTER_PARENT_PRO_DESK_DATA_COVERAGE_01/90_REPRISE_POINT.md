---
doc_id: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 90_REPRISE_POINT

## 7_CANONICAL_STATE

Parent ouvert :

```text
GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
```

Role structurel :

```text
GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN
PF_ID = PF_DATA_CENTER
MASTER_PROJECT_PLAN_ID = MPP_DATA_CENTER_NORMALIZED_REGISTRY
```

## 1_MASTER_TARGET

Construire la couverture Data Center pro-grade des donnees utilisees par des desks professionnels, avec scoring multi-sources, best-value resolver et consommation DeskPro via views Data Center.

## 4_MASTER_PROJECT_PLAN

1. Audit existant.
2. Inventaire canonique P0-P21.
3. Mapping inventaire -> existant.
4. Gap matrix.
5. Source scoring.
6. Best-value resolver.
7. DeskPro consumption map.

## 12_INVARIANTS

- Ne pas doubler DeskPro.
- Ne pas ingerer dans DeskPro.
- Ne pas faire lire DeskPro dans les producers raw.
- Ne pas creer de reader fantome.
- Data Center score et resout.
- DeskPro consomme les views.

## 16_TODO

Ouvrir le child GO :

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01
```

## 17_RESUME_POINT

Reprendre par l'audit de l'existant : lire `producers.json`, `consumers.json`, les docs DeskPro input expansion, les docs Data Center view migration, les readers `modules/desk_pro/service/`, puis produire la coverage matrix et les gaps avant tout schema scoring/resolver.
