# 30_RUNTIME_RISK_CLASSIFICATION_APPLY

## Objectif

Appliquer la classification WHY runtime aux surfaces connues du repo.

## Classification appliquee

| Surface | Classe | Justification |
| --- | --- | --- |
| docs/chantiers | R0 | aucune execution runtime |
| docs/governance | R0 | doctrine uniquement |
| scripts locaux | R1 | faible impact |
| dashboards observateurs | R2 | impact lecture uniquement |
| ingestion snapshots | R3 | dependance multi-systeme |
| Telegram bot vision | R3 | pont runtime multi-machine |
| OpenClaw orchestration | R3 | orchestration critique |
| webhook TradingView | R4 | signaux trading live |
| execution financiere automatique | R5 | impact financier direct |

## Regles recommandees

| Classe | Exigence minimale |
| --- | --- |
| R0 | reprise |
| R1 | WHY recommande |
| R2 | WHY + RESUME_POINT |
| R3 | WHY + INVARIANTS + FAILURE_MODES |
| R4 | review humaine obligatoire |
| R5 | governance complete + gates fortes |

## Observation

Les surfaces R4/R5 doivent rester rares et fortement gatees.
