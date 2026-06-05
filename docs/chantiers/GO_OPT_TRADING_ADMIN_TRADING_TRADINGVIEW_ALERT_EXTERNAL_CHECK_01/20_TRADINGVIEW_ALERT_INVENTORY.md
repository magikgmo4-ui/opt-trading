---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01_TV_INVENTORY
doc_type: chantier_inventory
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01
status: partial
updated_at: 2026-05-04
---

# 20_TRADINGVIEW_ALERT_INVENTORY

## Statut de vérification

**PARTIAL** — Le panneau Alertes TradingView n'a pas pu être inspecté depuis l'environnement
Cowork (extension Claude-in-Chrome non connectée, navigateur en lecture seule depuis le sandbox).

La vérification manuelle reste à effectuer selon la checklist ci-dessous.

## Contraintes de vérification

- Aucun test alert si le message peut déclencher un vrai trade
- Ne pas exposer la webhook secret key dans ce document
- Ne pas capturer les informations sensibles du compte TradingView
- Cocher uniquement les faits observables sans déclencher d'ordre

## Checklist de vérification manuelle — panneau Alerts TradingView

Pour chaque alerte liée à opt-trading / webhook / XAU / BTC / crypto / strategy :

### Étapes à effectuer dans TradingView

```
1. Ouvrir le panneau Alerts (icône cloche dans la barre latérale)
2. Identifier toutes les alertes liées à :
   - opt-trading
   - webhook
   - XAU / XAUUSD / Gold
   - BTC / BTCUSD
   - crypto (toute paire)
   - strategy / smartmoney / indicateur webhook
3. Pour chaque alerte relevée, noter :
   - nom de l'alerte
   - symbole (ex: XAUUSD, BTCUSD...)
   - timeframe
   - statut : active / paused / expired / deleted / unknown
   - source de la condition (strategy ou indicateur)
   - webhook activé : oui / non
   - URL webhook présente : oui / non
   - URL webhook correspond à phytogeographical-subnodulous-joycelyn.ngrok-free.dev/tv : oui / non
   - message JSON présent : oui / non
   - dernière exécution visible dans TradingView
   - expiration configurée (date/heure si visible)
4. Vérifier si la stratégie/indicateur source est chargé sur le chart actif
5. Vérifier si le symbole/timeframe du chart correspond aux alertes
6. Vérifier si TradingView affiche une erreur ou un warning sur les alertes
```

## Tableau d'inventaire (à compléter manuellement)

| # | Nom alerte | Symbole | Timeframe | Statut | Source/Strategy | Webhook activé | URL correcte | JSON présent | Dernière exec | Expiration |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | À compléter | — | — | — | — | — | — | — | — | — |
| 2 | À compléter | — | — | — | — | — | — | — | — | — |
| 3 | À compléter | — | — | — | — | — | — | — | — | — |

## Résultat observé lors de ce GO

- Vérification UI TradingView : **non effectuée** (accès navigateur non disponible depuis le sandbox)
- État documenté par défaut depuis contexte établi : TradingView ne génère plus de requêtes
  vers `phytogeographical-subnodulous-joycelyn.ngrok-free.dev/tv` depuis le 2026-04-01 07:12

## Note sur les alertes expirées

TradingView affiche souvent les alertes expirées avec un badge rouge ou une icône de pause.
Si l'alerte était configurée avec une expiration fixe (ex: 1 mois, 2 mois), elle peut être
silencieusement inactive sans notification.

La date du dernier POST connu (2026-04-01 07:12) suggère un arrêt brutal à cette date —
potentiellement une expiration programmée ou un stop de la stratégie source.

## RISKS

- À qualifier.
