# 40_FAILURE_MODES_RUNTIME

## Objectif

Documenter les failure modes runtime critiques multi-machine.

## Failure modes runtime

| ID | Failure mode | Surface | Risque |
| --- | --- | --- | --- |
| RFM-01 | webhook inaccessible | TradingView webhook | perte de signaux |
| RFM-02 | Telegram indisponible | bot vision / notifications | perte d'observabilite |
| RFM-03 | snapshots non ingestes | desk bridge | etat stale |
| RFM-04 | orchestration OpenClaw degradee | db-layer | supervision incomplete |
| RFM-05 | collision multi-machine | toutes | etat incoherent |
| RFM-06 | hallucination documentaire IA | gouvernance | mauvaises decisions |
| RFM-07 | runtime non gate | surfaces R4/R5 | risque critique |
| RFM-08 | confusion branche/runtime | gouvernance | derive operatoire |

## Protections actuelles

- separation AUDIT/APPLY,
- split machine,
- PASS/FAIL,
- reprise,
- patch minimal,
- preuves runtime.

## Invariant

Les surfaces R4/R5 devraient toujours:
- avoir un resume point,
- avoir une review humaine,
- documenter les failure modes critiques.
