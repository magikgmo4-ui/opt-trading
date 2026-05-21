---
doc_id: GO_SIGNAL_CHAIN_DRY_RUN_AUTOMATION_01_POLICIES
doc_type: signal_policies
go_id: GO_SIGNAL_CHAIN_DRY_RUN_AUTOMATION_01
status: draft
---

# 40_INVALIDATION_AND_GUARD.md

## Règles d'invalidation

| Condition | Action | Raison |
|---|---|---|
| `confidence < 0.6` | Reject | Faible confiance |
| `price <= 0` | Reject | Prix invalide |
| Sources recoupées = 0 sur 4 | Reject | Aucune confirmation |
| `signal_type` inconnu | Reject | Type non supporté |
| Signal reçu > 60s après timestamp | Reject | Trop vieux (latence) |
| `direction` manquant | Reject | Champ obligatoire absent |
| Kill switch = FULL_STOP | Reject | Kill switch activé |

## Dry-run guard

Le dry-run guard est la barrière de sécurité qui empêche toute émission d'ordre live.

```yaml
dry_run_guard:
  enabled: true
  mode: "strict"                       # strict | permissive | off
  blocks:
    - emission ordre live vers exchange
    - modification de portefeuille
    - appel API trading avec funds réels
  allows:
    - génération d'ordre en dry-run (JSON simulé)
    - journalisation de l'ordre simulé
    - alerte Telegram "ORDRE BLOQUÉ (dry-run)" 
  bypass:
    - Aucun (pas de bypass possible en mode strict)
    - kill switch manual → NORMAL ne débloque pas le guard
```

## Test de non-émission

```bash
# Vérification : aucun appel API live depuis la chaîne de signal
# Le guard intercepte toute tentative avant émission
# L'ordre simulé est stocké dans data/signals/dry_run_orders/
```
