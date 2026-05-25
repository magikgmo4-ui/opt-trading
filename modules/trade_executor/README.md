# trade_executor

Execute des propositions de trade validées par `validation_gate`. V1 : paper adapter uniquement.

## Flow

```
GateDecision(APPROVED) + Proposition → TradeRequest → PaperAdapter → TradeResult
```

## Invariant

- `NO_LIVE_TRADE_WITHOUT_GATE` — gate_decision.verdict doit être `APPROVED`
- Pas de Bitget live en V1

## Commands

```bash
cmd.sh sanity         # validation complète
cmd.sh test           # 28 tests unitaires
cmd.sh execute        # exécution dry-run via CLI
cmd.sh status         # vérifier le module
```

## TradeResult status

| Status | Condition |
|--------|-----------|
| dry_run | `TradeRequest.dry_run=True` + gate approved |
| filled | `TradeRequest.dry_run=False` (paper adapter) |
| rejected | gate non approved |
| error | adapter error |

## Env

| Variable | Default | Description |
|----------|---------|-------------|
| `GATE_APPROVAL_DIR` | `data/gate_approvals/` | Répertoire des fichiers d'approbation |

## Dépendances

- `modules/validation_gate` — fournit `GateDecision`
- `modules/proposition_engine` — fournit `Proposition`
- `modules/execution_engine` — fournit `PaperAdapter`
- `modules/notification_dispatcher` — notifications Telegram
