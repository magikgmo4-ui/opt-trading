# 20_PHASE_2 — Alertes TradingView : inventaire et contrôle

## Objectif

Valider si tradingview-mcp peut lister, auditer, créer et supprimer des alertes TradingView de manière contrôlée.

## Fonctions à tester

- `alert_list` — lister toutes les alertes existantes
- `alert_create` — créer une alerte test non critique
- `alert_delete` — supprimer cette même alerte test
- Vérification webhook URL si disponible
- Vérification message JSON payload si disponible

## Interdictions

- Ne pas modifier les alertes de production.
- Ne pas supprimer les alertes existantes.
- Ne pas créer d'alerte réelle sans GO explicite.

## Livrables

- Tableau des alertes existantes (nom, symbole, timeframe, statut)
- Champ statut : active / paused / expired / missing / unknown
- Champ webhook : present / missing / unreadable
- Champ JSON payload : present / missing / unreadable
- Verdict sur capacité réelle

## Critère PASS

Le système peut produire un inventaire fiable des alertes et manipuler une alerte test isolée.

## Résultat

**Statut** : [PASS / PARTIAL / FAIL]

**Inventaire** :

| Nom | Symbole | Timeframe | Statut | Webhook | Payload |
|-----|---------|-----------|--------|---------|---------|
|     |         |           |        |         |         |

**Détail** :
