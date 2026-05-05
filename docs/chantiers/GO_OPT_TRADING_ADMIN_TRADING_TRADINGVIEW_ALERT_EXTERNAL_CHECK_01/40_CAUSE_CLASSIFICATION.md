---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01_CAUSE
doc_type: chantier_classification
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_TRADINGVIEW_ALERT_EXTERNAL_CHECK_01
status: partial
updated_at: 2026-05-04
---

# 40_CAUSE_CLASSIFICATION

## Rappel des faits établis

| Fait | Source |
| --- | --- |
| `tv-webhook` UP, `ngrok-tv` UP, route `/tv` correcte | WEBHOOK_RUNTIME_REVIEW_01 PASS |
| Dernier POST `/tv` 200 OK : 2026-04-01 07:12 | WEBHOOK_SIGNAL_DIAG_01 PASS |
| ngrok metrics : 0 connections / 0 HTTP requests | WEBHOOK_SIGNAL_DIAG_01 PASS |
| Conclusion : TradingView ne génère plus de requêtes | WEBHOOK_SIGNAL_DIAG_01 PASS |
| URL publique ngrok conforme aux docs | WEBHOOK_SIGNAL_DIAG_01 PASS |

## Classification des causes

### Causes confirmées ou hautement probables

| Code | Cause | Probabilité | Justification |
| --- | --- | --- | --- |
| **A** | Alertes expirées | **HAUTE** | Arrêt brutal au 2026-04-01 07:12. TradingView configure souvent une date d'expiration. Cohérent avec l'absence totale de signal depuis. |
| **B** | Alertes désactivées / pausées | **HAUTE** | Possible manuellement ou automatiquement si la stratégie source s'est arrêtée. |
| **C** | Alertes supprimées | **MOYENNE** | Possible si gestion manuelle. Pas de preuve directe. |
| **E** | Stratégie/indicateur source absent du chart | **MOYENNE** | Si la stratégie Pine Script a été retirée du chart, l'alerte perd sa source et s'arrête. |

### Causes éliminées

| Code | Cause | Statut | Justification |
| --- | --- | --- | --- |
| **D** | Webhook URL manquante ou incorrecte | Peu probable (non confirmé) | L'URL ngrok est stable (`phytogeographical-subnodulous-joycelyn`). Sauf si redémarrage ngrok a changé le sous-domaine après la dernière config des alertes. |
| — | Côté serveur : tv-webhook DOWN | **ÉLIMINÉE** | WEBHOOK_RUNTIME_REVIEW_01 PASS prouve que tv-webhook est UP. |
| — | Côté ngrok : tunnel DOWN | **ÉLIMINÉE** | WEBHOOK_SIGNAL_DIAG_01 PASS prouve que ngrok-tv est UP. |
| — | Route /tv incorrecte | **ÉLIMINÉE** | Route vérifiée POST-only, correcte. |

### Causes non vérifiables depuis cet environnement

| Code | Cause | Statut |
| --- | --- | --- |
| **F** | Mauvais symbole/timeframe | À vérifier manuellement dans TradingView |
| **G** | Message JSON absent ou invalide | À vérifier manuellement |
| **H** | TradingView plan/limite/permissions bloquant les webhooks | À vérifier dans les paramètres du compte |
| **I** | Cause non visible depuis UI, besoin test safe | Possible si A/B/C/E non confirmés |

## Cause la plus probable (depuis contexte établi)

**A — Alertes expirées**, seule ou combinée avec **B — Alertes pausées / désactivées**.

Raisonnement :
- Le signal s'est arrêté nettement au 2026-04-01 07:12, sans dégradation progressive
- Aucune requête ngrok depuis cette date (0 connections)
- L'infrastructure server-side est intacte et fonctionnelle
- Comportement cohérent avec une expiration d'alerte TradingView (date limite atteinte)
  ou avec un arrêt de la stratégie source (stratégie stoppée ou sortie de position sans
  reprise de l'alerte)

## Niveau de confiance

| Niveau | Condition |
| --- | --- |
| MOYEN | Cause A ou B probable d'après les faits indirects |
| — | Confirmation directe requiert l'inspection UI TradingView |

## Éléments restant à vérifier (bloquants pour PASS complet)

1. Ouvrir le panneau Alerts TradingView → inventorier les alertes (doc 20)
2. Vérifier le statut actif/expiré/paused de chaque alerte
3. Vérifier la présence et la valeur de l'URL webhook dans chaque alerte (doc 30)
4. Vérifier si la stratégie source est chargée sur le chart
5. Vérifier si TradingView affiche un warning ou une erreur sur les alertes
