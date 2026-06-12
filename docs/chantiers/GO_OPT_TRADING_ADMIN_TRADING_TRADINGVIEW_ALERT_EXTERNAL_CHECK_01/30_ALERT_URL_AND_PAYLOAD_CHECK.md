---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01_URL_CHECK
doc_type: chantier_check
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01
status: partial
updated_at: 2026-05-04
---

# 30_ALERT_URL_AND_PAYLOAD_CHECK

## Statut

**PARTIAL** — Vérification UI TradingView non effectuée depuis cet environnement.
Les éléments documentés ci-dessous proviennent du contexte établi et des specs connues.

## URL ngrok de référence (établie — WEBHOOK_SIGNAL_DIAG_01 PASS)

```
https://phytogeographical-subnodulous-joycelyn.ngrok-free.dev/tv
```

Cette URL est :
- stable et inchangée depuis le diagnostic
- conforme aux docs existants dans le repo
- la seule URL valide pour le webhook `/tv` sur admin-trading

## Vérification URL webhook dans TradingView

À vérifier manuellement dans les paramètres de chaque alerte :

| Champ à vérifier | Valeur attendue | Conforme ? |
| --- | --- | --- |
| Webhook URL | `https://phytogeographical-subnodulous-joycelyn.ngrok-free.dev/tv` | À vérifier |
| Méthode | POST (implicite TradingView) | — |
| Chemin | `/tv` (présent dans l'URL) | — |

### Risque spécifique : URL périmée après restart ngrok

Si le service `ngrok-tv` a été redémarré depuis la dernière configuration des alertes TradingView,
l'URL publique ngrok peut avoir changé. Dans ce cas, les alertes TradingView pointent vers
une URL ngrok obsolète qui ne correspond plus au tunnel actif.

Vérification : comparer l'URL dans les alertes TradingView avec l'URL ngrok actuelle (4040/api/tunnels).

L'URL établie `phytogeographical-subnodulous-joycelyn.ngrok-free.dev` est un sous-domaine fixe
(ngrok gratuit ou fixe selon le plan), ce qui réduit ce risque mais ne l'élimine pas.

## Message JSON attendu

### Payload de référence (sans secret)

Le payload JSON envoyé par TradingView vers `/tv` doit contenir les champs requis
par le schéma `schemas/webhook_event_v1.json` du repo.

Structure minimale attendue :

```json
{
  "symbol": "{{ticker}}",
  "action": "{{strategy.order.action}}",
  "price": {{close}},
  "time": "{{time}}"
}
```

Note : le payload exact peut inclure des champs supplémentaires (position_size, comment, etc.)
selon la stratégie source. Le secret d'authentification, s'il existe, **ne doit pas être
documenté ici**.

### Vérification manuelle à effectuer

Dans chaque alerte TradingView :

1. Ouvrir les paramètres de l'alerte (icône crayon)
2. Aller dans l'onglet "Notifications" ou "Webhook"
3. Vérifier la présence du champ "Message" avec un JSON valide
4. Vérifier l'URL webhook (comparer avec la référence ci-dessus)
5. Ne pas cliquer "Test" si le message contient une action de trade réelle

## Checklist URL et payload

```
[ ] URL webhook présente dans l'alerte
[ ] URL = https://phytogeographical-subnodulous-joycelyn.ngrok-free.dev/tv
[ ] Chemin /tv présent (pas /webhook, pas /)
[ ] Message JSON présent
[ ] JSON syntaxiquement valide (pas de texte libre)
[ ] Aucun secret visible dans ce document
```

## Résultat de ce GO

- URL de référence : documentée
- Vérification dans TradingView : **manuelle requise**
- Payload de référence : documenté (sans secret)
- Comparaison UI : **non effectuée** (accès navigateur non disponible)

## RISKS

- À qualifier.
