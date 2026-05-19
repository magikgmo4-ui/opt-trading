# 20_TEMPLATE_SOURCE_STATE

## Template intégré

- **Fichier**: `modules/tradingview_observer/templates/alert_webhook_template_v1.json`
- **Schema**: `opt_trading_tradingview_alert_template_v1`
- **Mode**: `test_only`
- **Signal**: `TEST_ONLY`
- **Trade allowed**: `false`
- **Admin runtime**: `false`

## Fichiers documentaires associés

| Fichier | Contenu |
|---|---|
| `...ALERT_WEBHOOK_TEMPLATE_01/10_SCOPE_AND_INVARIANTS.md` | Scope et invariants |
| `...ALERT_WEBHOOK_TEMPLATE_01/20_TEMPLATE_SPEC.md` | Spec complete du template |
| `...ALERT_WEBHOOK_TEMPLATE_01/30_TEST_PROCEDURE.md` | Options A/B de test |
| `...ALERT_WEBHOOK_TEMPLATE_01/40_LIMITS_AND_SECURITY.md` | Limites et sécurité |
| `...ALERT_WEBHOOK_TEMPLATE_01/90_CLOSEOUT.md` | PASS_DOC_ONLY |

## Limites actives

- Test avec endpoint réel non effectué (Option B : validation JSON sans envoi)
- Aucun endpoint webhook production connecté
- Aucune alerte réelle déclenchée
- Placeholders TradingView (`{{ticker}}`, etc.) non validés en conditions réelles

## Sécurité

- Tous les flags de sécurité sont actifs
- Aucun token, secret, URL webhook réelle
- Admin-trading non connecté
