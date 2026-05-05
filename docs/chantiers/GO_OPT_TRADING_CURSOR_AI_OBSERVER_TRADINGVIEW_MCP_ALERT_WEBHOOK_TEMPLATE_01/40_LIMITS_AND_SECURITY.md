# 40_LIMITS_AND_SECURITY

## Limites

- Ce template est un artefact de configuration/test, pas un remplacement runtime.
- Il ne remplace pas le webhook TradingView -> admin-trading.
- Il n'a pas ete teste avec un endpoint reel (Option B : validation JSON sans envoi).
- Les placeholders TradingView (`{{ticker}}`, `{{exchange}}`, etc.) dependent du format TradingView et peuvent varier.

## Regles de securite

- Ne jamais remplacer `trade_allowed: false` par `true` sans GO explicite.
- Ne jamais connecter ce template a un endpoint webhook de production sans GO explicite.
- Ne jamais ajouter d'URL webhook complete contenant un token dans ce template.
- Si une URL webhook est documentee, utiliser uniquement des placeholders ou `localhost`.

## Routes bloquees

| Route | Statut | Note |
|---|---|---|
| admin_trading_runtime | `false` | Non route vers admin-trading |
| desk_ingestion | `false` | Non route vers desk |
| telegram_notify | `false` | Non route vers Telegram |
| live_order | `false` | Aucun ordre |

## Reprise securite

Si le template doit etre active en production, ouvrir un GO separe avec :
- Validation securite explicite
- Approbation du webhook endpoint
- Test en environnement isole
