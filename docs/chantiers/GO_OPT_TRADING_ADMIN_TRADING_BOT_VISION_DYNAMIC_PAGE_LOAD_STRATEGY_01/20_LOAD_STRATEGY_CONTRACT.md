---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_DYNAMIC_PAGE_LOAD_STRATEGY_01
surface: ADMIN_TRADING
source_kind: contract
updated_at: 2026-05-19
---

# 20_LOAD_STRATEGY_CONTRACT

## Objectif

Permettre a chaque profil de choisir sa strategie de chargement sans changer les defaults historiques.

## Champs supportes

| Champ | Valeurs | Default | Effet |
| --- | --- | --- | --- |
| `wait_until` | `networkidle`, `domcontentloaded`, `load` | `networkidle` | valeur transmise a `page.goto` |
| `timeout_ms` | entier positif | `30000` | timeout de navigation et timeout par defaut de la page |
| `post_load_wait_ms` | entier positif ou zero | `3000` | attente apres navigation avant screenshot |
| `screenshot_mode` | `viewport` | `viewport` | capture viewport, `fullPage: false` |

## Compatibilite

Un profil existant sans ces champs conserve exactement le comportement precedent :

```json
{
  "wait_until": "networkidle",
  "timeout_ms": 30000,
  "post_load_wait_ms": 3000,
  "screenshot_mode": "viewport"
}
```

## Validation

Les valeurs invalides stoppent uniquement le profil concerne avec un message d'erreur, sans faire echouer toute la boucle de capture.

## Sidecar enrichi

Le JSON sidecar inclut maintenant :

```json
{
  "page_id": "tv_xau_h1",
  "wait_until": "domcontentloaded",
  "timeout_ms": 60000,
  "post_load_wait_ms": 10000,
  "screenshot_mode": "viewport"
}
```

## Limite volontaire

`skip avec reason JSON` n'est pas encore implemente. Le code actuel continue de logger les erreurs de capture et passe au profil suivant, comme avant.
