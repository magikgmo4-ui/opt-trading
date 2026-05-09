# 20_MACHINE_RUNTIME_DEPENDENCIES

## Objectif

Cartographier les dependances runtime entre machines.

## Machines

| Machine | Role principal |
| --- | --- |
| admin-trading | runtime trading / bots / webhook |
| db-layer | orchestration / OpenClaw / infra |
| cursor-ai | observation / docs / transport |
| student | laboratoire local / Ollama |
| fantome | gouvernance / architecture |

## Dependances principales

| Source | Depend de | Risque |
| --- | --- | --- |
| Telegram bot vision | ShareX + ingestion desk | rupture multi-systeme |
| webhook TradingView | reseau + Telegram + runtime webhook | perte de signaux |
| OpenClaw orchestration | providers + tmux + services | orchestration degradee |
| dashboards observateurs | data runtime | faux etat visible |
| Ollama local | ressources machine | indisponibilite IA locale |

## Dependances critiques multi-machine

### admin-trading <-> db-layer

- orchestration,
- supervision,
- runtime critique.

### cursor-ai <-> admin-trading

- observation,
- transport documentaire,
- bundles.

### student <-> db-layer

- laboratoire local,
- experimentation IA.

## Invariant

Toute dependance multi-machine critique devrait avoir:
- reprise,
- invariants,
- gates,
- failure modes documentes.
