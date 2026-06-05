---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01_NEXT
doc_type: chantier_next
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01
status: open
updated_at: 2026-05-04
---

# 50_NEXT_GO_DECISION

## Contexte de décision

Ce GO est classé **PARTIAL** : le precheck server-side est documenté depuis le contexte établi,
mais l'inspection du panneau Alerts TradingView n'a pas pu être effectuée depuis l'environnement
Cowork (Chrome extension non connectée, navigateur en lecture seule).

## Décision de prochain GO

### GO retenu

**`GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_ALERT_REACTIVATION_01`**

### Justification

La cause probable est **A (alertes expirées) ou B (alertes pausées/désactivées)** d'après le
contexte établi. Le prochain GO logique est donc la réactivation des alertes TradingView, soit :

1. **Si l'inspection manuelle confirme A ou B** → GO de réactivation directe :
   reconfigurer les alertes expirées/pausées avec la bonne URL ngrok et le bon payload JSON

2. **Si l'inspection révèle D (URL incorrecte)** → correction de l'URL dans les alertes

3. **Si l'inspection révèle E (stratégie absente du chart)** → recharger la stratégie,
   puis recréer les alertes

Dans tous ces cas, le GO de réactivation est le point d'entrée correct.

### GO alternatifs (hors périmètre immédiat)

| GO | Condition de déclenchement |
| --- | --- |
| `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SAFE_TEST_PAYLOAD_01` | Si un test de payload safe (sans trade) est requis avant réactivation |
| `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_HEALTH_ENDPOINT_ADD_01` | Si un endpoint de health-check dédié est jugé nécessaire pour monitoring continu |
| `GO_OPT_TRADING_ADMIN_TRADING_TV_PERF_USER_HARDENING_01` | Si la revue de sécurité utilisateur TradingView est prioritaire |
| `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_CLOSEOUT_OR_NEXT_RUNTIME_REVIEW_01` | Seulement si la réactivation est jugée hors scope de ce parent |

## Prérequis avant d'ouvrir le GO retenu

Avant d'ouvrir `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_ALERT_REACTIVATION_01` :

1. Compléter l'inventaire manuel TradingView (doc 20) — inspection directe du panneau Alerts
2. Confirmer la cause dans doc 40 (A, B, C, D, E, F, G, H, ou I)
3. Identifier les alertes à reconfigurer (nom, symbole, timeframe)
4. S'assurer que l'URL ngrok active est toujours `phytogeographical-subnodulous-joycelyn.ngrok-free.dev/tv`

## Règle de priorité

Ce GO enfant est rattaché au parent `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` (OPEN).
Il ne doit pas modifier la priorité opératoire du tableau canonique (5 GO retenus dans
`docs/index/ACTIVE_STREAMS.md` et `docs/index/GO_INDEX.md`).

## RISKS

- À qualifier.
