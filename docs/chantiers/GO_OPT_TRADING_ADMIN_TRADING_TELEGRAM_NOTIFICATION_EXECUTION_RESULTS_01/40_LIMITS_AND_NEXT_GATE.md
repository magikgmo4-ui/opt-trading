---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_EXECUTION_RESULTS_01_40_LIMITS
doc_type: chantier/limits
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_NOTIFICATION_EXECUTION_RESULTS_01
machine: admin-trading
status: active
lifecycle_stage: telegram_execution_results
---

# 40_LIMITS_AND_NEXT_GATE — Limites et prochaine etape

## Ce qui est valide

| Flux | Statut |
| --- | --- |
| `/tv → risk_quote` | Valide (TV_TEST) |
| `/tv → record_event` | Valide (11/11 + 10/10) |
| `/tv → Telegram notification` | Valide (10 messages recus) |
| `/tv → perf_open` | Bypass confirme (TV_TEST skip) |
| `/tv → executor.execute` | Bypass confirme (PAPER_TEST uniquement) |
| Payloads invalides → 400 | Valide |
| No-trade | Confirme (0 perf ledger) |

## Ce qui n'est PAS valide

| Flux | Statut | Raison |
| --- | --- | --- |
| `/tv → PAPER_TEST → execution` | Non teste | Hors scope de ce GO |
| `/tv → COINM_SHORT → trading reel` | Non teste, interdit | Gate non ouverte |
| `/tv → Telegram + trade reel` | Non teste, interdit | Gate non ouverte |
| Redemarrage service avec Telegram | Valide une fois | Non teste en cycle long |

## Prochaine gate

La prochaine etape logique serait de tester `PAPER_TEST` avec Telegram,
ce qui impliquerait l'execution papier (positions virtuelles, pas de broker).

Ceci necessite un GO separe car il active partiellement le chemin d'execution :

```text
GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_TELEGRAM_EXECUTION_01
```

**Ne pas ouvrir cette gate sans GO explicite et validation prealable des guards.**

## Limites connues

1. **Doublons** : le rejeu du meme script produit des notifications en double.
   Le flux ne deduplique pas. C'est le comportement attendu (pas d'idempotence
   dans le code webhook actuel).

2. **Absence de `tp`** : Les messages Telegram affichent `tp: None` si le
   payload ne contient pas de `tp`. Le code utilise `safe_float(payload.get("tp"))`
   qui retourne `None` si absent.

3. **Pas de rich formatting** : Le message Telegram utilise `parse_mode: "HTML"`
   mais le contenu est en texte brut sans balisage HTML supplementaire.

4. **Pas de retry Telegram** : Si l'API Telegram echoue, l'evenement est
   quand meme enregistre mais la notification peut etre perdue. Pas de
   mecanisme de retry dans le code actuel.
