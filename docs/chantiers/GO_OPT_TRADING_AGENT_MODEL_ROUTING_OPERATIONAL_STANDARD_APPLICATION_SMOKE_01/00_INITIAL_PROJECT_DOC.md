---
doc_id: GO_OPT_TRADING_AGENT_MODEL_ROUTING_OPERATIONAL_STANDARD_APPLICATION_SMOKE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_AGENT_MODEL_ROUTING_OPERATIONAL_STANDARD_APPLICATION_SMOKE_01
parent_go_id: GO_OPT_TRADING_AGENT_MODEL_ROUTING_OPERATIONAL_STANDARD_01
machine: fantome
status: cadrage
lifecycle_stage: opening
topic_keys:
  - agent_model_routing
  - application_smoke
  - non_trading
source_kind: canonical
updated_at: 2026-05-14
---

# GO_OPT_TRADING_AGENT_MODEL_ROUTING_OPERATIONAL_STANDARD_APPLICATION_SMOKE_01

## 1_MASTER_TARGET

Appliquer le standard operationnel de routage multi-provider sur 2-3 taches non-trading, verifier la selection provider/model, le fallback ladder, et la conformite strict_workers.

## 2_TACHES DE TEST

| # | Tache | Classification | Provider attendu | Risque |
|---|-------|----------------|------------------|--------|
| 1 | "Lister les 5 GO les plus recents dans docs/chantiers/" | read-only, format libre | 0.5B agent chain | faible |
| 2 | "Compter le nombre de fichiers .md dans docs/agents/" | read-only, format exact | 1.5B direct | faible |
| 3 | Test fallback: 0.5B → 1.5B | smoke, fallback | 0.5B initial, 1.5B fallback | faible |

## 3_CRITERES_PASS

```text
- Chaque tache est classee selon le standard
- Le provider selectionne correspond a la classification
- Le fallback est teste et conforme
- Les traces de decision sont produites
- Non-trading strict
- Aucun write
- Aucun secret
- Conforme strict_workers (A1 read-only)
```

## 4_INVARIANTS

```text
- Non-trading
- Read-only
- Aucun write
- Aucun secret
- Stash branch_arbitration preserve
```

## RISKS

- À qualifier.
