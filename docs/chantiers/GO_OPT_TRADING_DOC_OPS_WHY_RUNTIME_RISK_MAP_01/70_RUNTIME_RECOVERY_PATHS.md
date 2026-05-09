# 70_RUNTIME_RECOVERY_PATHS

## Objectif

Documenter les chemins de reprise runtime critiques.

## Reprises critiques

| Surface | Reprise minimale |
| --- | --- |
| webhook TradingView | etat service + logs + validation endpoint |
| Telegram bot vision | verification bridge + ingestion + chat |
| OpenClaw orchestration | verification tmux + providers + supervision |
| dashboards observateurs | validation freshness data |
| ingestion snapshots | verification latest.json + timestamps |

## Reprise multi-machine

### admin-trading

- verifier services,
- verifier webhooks,
- verifier Telegram,
- verifier logs runtime.

### db-layer

- verifier orchestration,
- verifier providers,
- verifier supervision.

### cursor-ai

- verifier transport documentaire,
- verifier bundles,
- verifier observation.

### student

- verifier Ollama,
- verifier ressources machine,
- verifier environnement labo.

## Invariant

Toute surface R3/R4/R5 devrait avoir:
- un resume point,
- une procedure minimale de reprise,
- une verification d'etat reel.
