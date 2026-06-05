---
doc_id: GO_OPT_TRADING_AGENT_MODEL_ROUTING_OPERATIONAL_ADOPTION_GATE_01
doc_type: adoption_gate
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_AGENT_MODEL_ROUTING_OPERATIONAL_ADOPTION_GATE_01
parent_go_id: GO_OPT_TRADING_AGENT_MODEL_ROUTING_OPERATIONAL_STANDARD_APPLICATION_SMOKE_01
machine: fantome
status: canonical
lifecycle_stage: operational
topic_keys:
  - agent_model_routing
  - adoption_gate
  - operational
source_kind: canonical
updated_at: 2026-05-14
---

# AGENT_MODEL_ROUTING_OPERATIONAL_ADOPTION_GATE_01

Gate d'adoption operationnelle du routage multi-provider. Ce document definit quand et comment le routage peut etre utilise dans les workflows reels.

## 1. STATUS

```text
ADOPTION_GATE_APPROVED
```

Le routage multi-provider a passe les etapes :
- First controlled execution → PASS
- Operational standard → PASS
- Application smoke 3/3 → PASS

Il peut maintenant etre adopte dans les workflows operationnels avec les regles ci-dessous.

## 2. SURFACES AUTORISEES

| Surface | Tache | Provider | Condition |
|---------|-------|----------|-----------|
| Doc-only | READ_INVENTORY, DOC_DRAFT, TRIAGE | 0.5B ou 1.5B | Read-only, non critique |
| Audit | ENDPOINT_AUDIT, COMPLIANCE_AUDIT | 0.5B agent chain | Lecture seule |
| Smoke/probe | READ_INVENTORY, smoke test | 0.5B agent chain | Faible risque |
| Diagnostic | Health check, session check | 0.5B agent chain | Read-only |
| Format-exact | Comptage, listing, extraction | 1.5B direct | Exactitude requise |
| Raisonnement leger | Classification, decision simple | deepseek-r1:1.5b | Non critique |

## 3. SURFACES INTERDITES

| Surface | Raison |
|---------|--------|
| Trading live | Risque financier — necessite approbation humaine |
| Secret handling | .env, tokens, cles — REFUSE automatique |
| Write non approuve | Contourne A4 WRITE_GATED |
| Decision autonome durable | Contourne l'autonomie etroite |
| Index globaux | GO_INDEX.md, BRANCH_STATE.md racine |
| Production sans rollback | Necessite dry-run + approval + rollback |

## 4. CRITERES PASS / NO_GO

```text
PASS (adoption autorisee) si :
- Tache classee dans les surfaces autorisees
- Provider selectionne conforme au standard
- Aucun trading
- Aucun secret
- Aucun write sans WRITE_GATED (A4)
- Trace de decision journalisee
- Session fraiche ou validee

NO_GO (adoption bloquee) si :
- Tache classee dans les surfaces interdites
- Provider non conforme au standard
- Trading detecte
- Secret detecte
- Write tente sans A4
- Pas de trace de decision
```

## 5. CONDITIONS DE PASSAGE

Avant toute execution agent en workflow operationnel :

```text
1. [ ] Classification de la tache (type, risque, format)
2. [ ] Selection provider selon le standard
3. [ ] Verification surface autorisee
4. [ ] Precheck strict_workers (A1/A2/A4)
5. [ ] Journalisation de la decision de routage
6. [ ] Execution bornee
7. [ ] Trace de resultat
8. [ ] Verification post-execution (git status si applicable)
```

## 6. ADOPTION GATE VERDICT

```text
ADOPTION_GATE_PASS
```

Le routage multi-provider est adopte pour les workflows operationnels non-trading.
Les surfaces autorisees sont documentees.
Les surfaces interdites sont explicites.
Les criteres PASS/NO_GO sont definis.

## RISKS

- À qualifier.
