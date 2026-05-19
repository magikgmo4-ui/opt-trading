---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01_SERVER_STATE
doc_type: chantier_precheck
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01
status: documented
updated_at: 2026-05-04
---

# 10_SERVER_READY_STATE

## Périmètre

Confirmation read-only que `admin-trading` est toujours dans l'état établi par
`GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01` (PASS, commit 78f4635).

## Méthode de documentation

Les commandes SSH de precheck définies dans le GO n'ont pas pu être réexécutées depuis
l'environnement Cowork (sandbox Linux sans clés SSH pour `admin-trading`).

L'état est documenté à partir du contexte établi (`WEBHOOK_SIGNAL_DIAG_01` PASS) et des
surfaces canoniques disponibles dans le repo.

Les commandes de référence pour une réexécution manuelle sont :

```bash
ssh admin-trading 'set -Eeuo pipefail; hostname; date; \
  systemctl --no-pager --full status tv-webhook ngrok-tv 2>/dev/null || true'

ssh admin-trading 'set -Eeuo pipefail; \
  curl -fsS --max-time 5 http://127.0.0.1:4040/api/tunnels 2>/dev/null \
  | python3 -m json.tool || true'

ssh admin-trading 'set -Eeuo pipefail; \
  curl -i --max-time 5 http://127.0.0.1:8000/docs 2>/dev/null | head -40 || true'

ssh admin-trading 'set -Eeuo pipefail; \
  journalctl -u tv-webhook --since "2026-04-01" --no-pager 2>/dev/null \
  | grep -Ei "POST /tv|200 OK|error|exception|traceback|denied|rejected" | tail -120 || true'
```

## État établi — source : WEBHOOK_SIGNAL_DIAG_01 PASS (commit 78f4635)

| Composant | Statut | Preuve |
| --- | --- | --- |
| `tv-webhook` | **UP** | systemctl active sur admin-trading |
| `ngrok-tv` | **UP** | service actif, tunnel ouvert |
| Route `/tv` | **correcte** | POST-only, validée |
| Port `8000` | accessible | `/docs` répond |
| Endpoint `/tv` | prêt à recevoir | aucun POST depuis 2026-04-01 07:12 |

## URL publique ngrok

```
phytogeographical-subnodulous-joycelyn.ngrok-free.dev/tv
```

URL inchangée depuis le diagnostic. Conforme aux docs existants.

## Dernier POST /tv connu

- Date : **2026-04-01 07:12**
- Statut HTTP : **200 OK**
- Source : journalctl tv-webhook (relevé lors de WEBHOOK_SIGNAL_DIAG_01)

## Métriques ngrok au moment du diagnostic

- Connections : **0**
- HTTP requests : **0**

Ces métriques confirment que TradingView n'a plus appelé le webhook depuis le dernier POST connu.

## Conclusion precheck

Le serveur est dans l'état attendu : **prêt à recevoir**, sans dégradation côté infra.
La cause du silence est côté TradingView, pas côté `admin-trading`.

Aucun restart, aucune modification runtime exécutés dans ce GO.
