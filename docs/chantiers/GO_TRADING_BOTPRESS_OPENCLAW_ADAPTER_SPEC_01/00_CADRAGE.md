---
doc_id: GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01_CADRAGE
doc_type: cadrage
repo: opt-trading
go_id: GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01
status: open
lifecycle_stage: specification
updated_at: 2026-05-06
links:
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/04_api_contract_openclaw_gateway.md
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/05_safety_gate.md
---

# 00_CADRAGE — Adapter Botpress ↔ OpenClaw

## 1_MASTER_TARGET

Specifier l adapter entre Botpress Operator (Telegram) et OpenClaw Gateway (runtime agent), sans implementation. Contrat pur, testable, sur.

## 3_INITIAL_NEED

Botpress doit parler a OpenClaw via un contrat stable. Cet adapter definit:
- Comment Botpress formate ses requests
- Comment OpenClaw repond
- Comment les erreurs et timeouts sont geres
- Ou la safety gate s applique
- Ou la journalisation se fait

## 6_FINAL_TARGET

Un contrat documente pret pour implementation: un sous-GO pourra coder l adapter en Python/FastAPI en lecture seule, avec safety gate et journalisation.

## Architecture cible

```
Telegram → Botpress → [ADAPTER] → OpenClaw Gateway → student/LONA/Trading Labs
                        ↑ safety gate
                        ↑ journalisation
```

## 12_INVARIANTS

- Spec-only, 0 code runtime
- 0 trade reel automatique
- 0 push Git automatique
- Safety gate = blocage en amont, pas en aval
- Journalisation = trace complete
- OpenClaw Gateway = existant, non modifie par ce GO

## 17_RESUME_POINT

```
docs/chantiers/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01/00_CADRAGE.md
```

## RISKS

- À qualifier.
