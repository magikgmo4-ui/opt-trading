# CREDENTIAL_CHANGE_REQUEST — ADD — Telegram Multi-Channel Chat IDs

## Référence

- **GO** : GO_OPT_TRADING_SECURITY_CREDENTIALS_TELEGRAM_MULTICHANNEL_CHILD_01
- **Méthode** : 20_SIMPLE_CHANGE_METHOD_ADD_MODIFY_ROTATE_DEPRECATE.md (parent)
- **Origine** : PR #1063 — feat(telegram): multi-channel routing alerts/pipeline/push/ops
- **Date** : 2026-06-03

## Type

`ADD`

## Credentials à ajouter

| Credential ID | Env Var | Type | Provider | Description |
|---|---|---|---|---|
| `telegram_chat_id_alerts` | `TELEGRAM_CHAT_ID_ALERTS` | `chat_id` | telegram | Canal alertes système — cron WARN, kill switch, dead letter, workers FAIL |
| `telegram_chat_id_pipeline` | `TELEGRAM_CHAT_ID_PIPELINE` | `chat_id` | telegram | Canal pipeline trading — signal, proposition, approbation, résultat |
| `telegram_chat_id_push` | `TELEGRAM_CHAT_ID_PUSH` | `chat_id` | telegram | Canal push contenu — bot_vision, coinglass, market data |
| `telegram_chat_id_ops` | `TELEGRAM_CHAT_ID_OPS` | `chat_id` | telegram | Canal commandes & tools — CLI, tmux, OpenClaw outputs |

## Rôles autorisés

Tous rattachés au rôle `telegram_collector`.

## Fallback

Si une variable n'est pas définie sur la machine, le code (`shared/telegram_channels.py`)
retombe sur `TELEGRAM_CHAT_ID` (credential `telegram_alert_chat_id` existant).

## Actions requises

1. Ajouter les 4 entrées dans `configs/env/registry/credentials.yaml`.
2. Ajouter les 4 IDs dans le rôle `telegram_collector` de `configs/env/registry/roles.yaml`.
3. Mettre à jour `configs/env/roles/telegram_collector.env.example` (valeurs vides).
4. Mettre à jour la procédure locale et la table de scope du chantier précédent.
5. Sur chaque machine autorisée, renseigner les vraies valeurs via `sudoedit /etc/opt-trading/env.d/roles/telegram_collector.env`.

## Validation post-ADD

```bash
python3 scripts/env/validate_credentials.py --machine fantome --job telegram_collect_channel
grep -rn "TELEGRAM_CHAT_ID_" configs/ shared/ scripts/ -- '*.yaml' '*.py' '*.sh' '*.env.example'
# Vérifier : aucune valeur numérique réelle de chat_id
```

## Anti-leak

```bash
# Aucune vraie valeur dans Git — placeholders uniquement
grep -rn "TELEGRAM_CHAT_ID_[A-Z]*=[0-9]" configs/ docs/ scripts/ && echo "LEAK DETECTED" || echo "CLEAN"
```
