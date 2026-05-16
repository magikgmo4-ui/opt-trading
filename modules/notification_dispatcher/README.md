# notification_dispatcher

Envoie des notifications Telegram structurées pour chaque étape du pipeline opt-trading.

## Event types

| Event | Déclencheur |
|-------|------------|
| `signal_received` | signal TradingView reçu et normalisé |
| `proposition_generated` | proposition de trade générée par OpenClaw |
| `approval_required` | approbation opérateur requise |
| `trade_executed` | trade exécuté sur l'exchange |
| `result_known` | résultat trade connu (P&L calculé) |
| `pipeline_error` | erreur à une étape du pipeline |
| `pipeline_info` | info générale (démarrage, statut) |

## Commandes

```bash
scripts/cmd.sh dry signal_received ticker=BTCUSDT side=BUY price=65000 tf=1h strategy_id=v1
scripts/cmd.sh send pipeline_info message="système démarré"   # nécessite TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID
scripts/cmd.sh sanity
scripts/cmd.sh test
```

## Config

```bash
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

## Usage Python

```python
from modules.notification_dispatcher.app import NotificationDispatcher, PipelineEvent

dispatcher = NotificationDispatcher()
dispatcher.dispatch(PipelineEvent(
    event_type="signal_received",
    payload={"ticker": "BTCUSDT", "side": "BUY", "price": 65000, "tf": "1h", "strategy_id": "v1"},
))
```

## État

```
Tests    11/11 PASS
Sanity   PASS
Dry-run  PASS (7/7 event types)
Live     nécessite TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID
```
