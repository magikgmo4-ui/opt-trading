# GO_SECURITY_P1_UNKNOWN_VERIFY_ROTATE_01

## Objectif

Vérifier l'âge et l'état des 3 credentials P1 UNKNOWN identifiés dans
`GO_SECURITY_CREDENTIAL_ROTATION_SCHEDULE_01`, et décider : KEEP, ROTATE_NOW, ou DISABLE.

## Périmètre

| Credential | Env Var | TTL | Statut entrant |
|------------|---------|-----|----------------|
| TV Webhook Key | `TV_WEBHOOK_KEY` | 90j | UNKNOWN → STALE probable |
| Ops Admin Key | `OPS_ADMIN_KEY` | 90j | UNKNOWN → STALE probable |
| Telegram Bot Token | `TELEGRAM_BOT_TOKEN` | 365j | UNKNOWN |

## Règles

- Aucune valeur secrète dans ce document ou les fichiers produits
- Les nouvelles valeurs sont générées en terminal et appliquées directement dans `.env`
- Aucune valeur en clair dans les logs, diffs, ou rapports
- Toute rotation est propagée sur toutes les machines concernées

## Dépendances runtime

| Credential | Consommateurs runtime | Impact rotation |
|------------|----------------------|-----------------|
| `TV_WEBHOOK_KEY` | `webhook_server.py`, `emit_tv_payload.py`, `bitget_to_tv_runner.py` | Nécessite update TradingView alerts + reload server |
| `OPS_ADMIN_KEY` | `webhook_server.py` (admin endpoints uniquement) | Reload server suffisant |
| `TELEGRAM_BOT_TOKEN` | `shared/telegram_notify.py`, `bot_vision_step2`, tous modules notif | Propagation fleet + restart services Telegram |

## Résultats attendus

Document `10_AUDIT_FINDINGS.md` : verdict KEEP / ROTATE_NOW / DISABLE pour chacun,
avec commandes de vérification exécutées et plan de rotation si décidé.
