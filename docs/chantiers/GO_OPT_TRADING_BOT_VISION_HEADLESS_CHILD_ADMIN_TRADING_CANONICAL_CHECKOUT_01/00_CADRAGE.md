---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_ADMIN_TRADING_CANONICAL_CHECKOUT_01__CADRAGE
doc_type: cadrage
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_ADMIN_TRADING_CANONICAL_CHECKOUT_01
status: open
owner: OpenCode
created_at: 2026-05-31
---

# Cadrage

## Objectif

Créer sur `admin-trading` un checkout canonique propre, séparé du runtime opérateur mutable `/opt/trading`, pour disposer d'une base Git saine alignée sur `origin/sot/mainline`.

## Contraintes

- ne pas casser le runtime réel déjà stabilisé dans `/opt/trading`
- ne pas faire de nettoyage destructif du checkout opérateur historique
- garder la séparation entre :
  - runtime mutable opérateur
  - checkout canonique propre

## Cible

- runtime mutable : `/opt/trading`
- checkout canonique propre : `/home/ghost/opt-trading-mainline-clean`
