---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_REGISTRY_REGULARIZATION_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: child_chantier_initial
strategy_id: xau_session_open_v1
strategy_version: v0.1.0
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-18
constraints:
  - no_runtime_mutation
  - no_live_trade
  - no_bitget_order
  - no_automatic_sheets_write
  - no_secrets
  - no_modules_strategy_consolidation
  - no_global_index_modification
---

# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_REGISTRY_REGULARIZATION_01

## 00_INITIAL_PROJECT_DOC

---

## 1_OBJECTIF

Régulariser la stratégie `xau_session_open_v1` comme stratégie officielle
registrée dans le cadre canonique (`GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01`).

`xau_session_open_v1` est la seule stratégie ACTIVE identifiée comme utilisée
par le runtime (`trading_realtime_v1`, `trading_lab_v1`) mais jamais registrée
dans le framework canonique. Ce GO comble ce gap de gouvernance.

---

## 2_STRATEGY_IDENTITY

| Champ | Valeur |
|---|---|
| `strategy_id` | `xau_session_open_v1` |
| `strategy_version` | `v0.1.0` |
| `family` | `session_open` |
| `model` | `mechanical` |
| `symbol` | XAUUSD |
| `runtime_surface` | `trading_realtime_v1` |
| `lab_surface` | `trading_lab_v1` |
| `profile` | `xauusd_dual_stack_v1` |
| `lifecycle` | ACTIVE (non documenté avant ce GO) |
| `lifecycle_canonique` | CANDIDATE (dans le cadre canonique) |

---

## 3_SCOPE_DU_CHILD

Ce child couvre :

```text
00_INITIAL_PROJECT_DOC.md
10_RUNTIME_SURFACE_AUDIT.md
20_STRATEGY_SPEC_XAU_SESSION_OPEN_V1.md
30_REGISTRY_ENTRY.md
40_GATE_DECISION.md
90_CLOSEOUT.md
```

Modification externe :

```text
docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/95_STRATEGY_REGISTRY.md
  → ajout entrée xau_session_open_v1
```

Ce child ne couvre pas :

```text
modules/strategy/ creation
runtime code modification
trading behaviour change
new strategy creation
engine migration
GO_INDEX.md / ACTIVE_STREAMS.md modification
```

---

## 4_HERITAGE_DU_PARENT

Ce child applique le cadre canonique à `xau_session_open_v1` :

| Section parente | Application |
|---|---|
| `20_STRATEGY_CANONICAL_SPEC_SCHEMA` | Spec instancié pour xau_session_open_v1 |
| `30_STRATEGY_LIFECYCLE_GATES` | Gates documentées pour le cas ACTIVE |
| `95_STRATEGY_REGISTRY` | Nouvelle entrée registry |

---

## 5_CONTRAINTES

| Contrainte | Statut |
|---|---|
| doc-only | Oui |
| no runtime mutation | Oui |
| no live trade | Oui |
| no Bitget order | Oui |
| no automatic Sheets write | Oui |
| no secrets | Oui |
| no modules/strategy/ consolidation | Oui |
| no GO_INDEX / ACTIVE_STREAMS mod | Oui |

---

## 6_VERDICT_ATTENDU

```text
PASS_REGISTRY_REGULARIZATION_DOC_ONLY
```

## RISKS

- À qualifier.
