# learning_feeder

Feed back les résultats de trade dans le cycle d'apprentissage OpenClaw.

## Flow

```
Proposition + TradeRecord → compose_feedback → [OperatorBridge] + [learning brick JSON]
```

## Commands

```bash
cmd.sh sanity   # validation complète
cmd.sh test     # 29 tests unitaires
cmd.sh feed     # envoyer un feedback via CLI
```

## Output

- `data/learning_bricks/YYYYMMDD/lf_<signal_id>_<request_id>.json` — brick persistée
