# 01_SESSION_DOCUMENTATION_INTEGRALE

## Résumé de session

LONA est un assistant de stratégie/backtest complémentaire au setup existant.

## Conclusions

- LONA = strategy lab
- OpenClaw = orchestrateur
- MCP = bus outils
- tmux = cockpit
- opt-trading = validation + risk + execution

## Architecture

```text
[tmux] → [OpenClaw] → [MCP] → [LONA] → [opt-trading] → [risk_engine]
```

## Décision

LONA ne doit jamais exécuter directement en live.
