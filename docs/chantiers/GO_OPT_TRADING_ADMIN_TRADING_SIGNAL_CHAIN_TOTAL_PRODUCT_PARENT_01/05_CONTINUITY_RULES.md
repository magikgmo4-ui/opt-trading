---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01_CONTINUITY_RULES
doc_type: continuity_rules
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01
status: open
source_kind: canonical
updated_at: 2026-05-19
---

# 05_CONTINUITY_RULES

## Regle de continuite obligatoire

Dans chaque document de continuite, reprise, closeout ou rapport rattache a ce parent, mentionner explicitement :

- la `MASTER_TARGET`
- le tableau Kanban du bundle
- le produit final total voulu
- le prochain item Kanban a faire
- les gaps encore ouverts

## Regles de fond

- ne pas fermer le parent umbrella avant livraison ou blocage explicite des surfaces critiques
- ne pas inventer de modules ni de fichiers absents
- ne pas melanger `Telegram Screener inbound` et `Telegram Notification outbound`
- ne pas mettre tous les events Telegram dans un seul chat sans map canonique prouvee
- ne pas transformer Telegram en verite strategie
- ne pas transformer TradingView en verite unique
- ne pas creer de runtime live a ce stade
- ne pas modifier le dispatcher live a cette passe
- ne pas modifier Strategy Registry avant inventaire, schema, replay/backtest et gate
- ne pas creer de Google Sheets implementation avant schema valide

## Regle documentaire locale

Si un fichier bundle demande n'est pas retrouve localement sous son nom exact :

- le signaler comme `NON_TROUVE`
- ne jamais le remplacer silencieusement par une invention
- pointer vers les preuves locales equivalentes si elles existent

## Regle Kanban

`03_PRODUCT_ROADMAP_KANBAN.md` est un miroir de continuite local. La source de navigation reste le tableau Kanban du bundle voulu.

Si un GO bundle exact n'existe pas localement sous son nom :

- le signaler comme `NON_TROUVE`
- utiliser le meilleur GO local reellement present comme mapping explicite
- ne jamais inventer un GO de closeout ou un nouveau parent concurrent

## Prochain item Kanban a faire

`GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`

## Gaps encore ouverts

- bundle exact non retrouve sous les noms fournis
- runtime bundle exact non trouve sous son nom ; mapping local actif sur `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`
- chainage total multi-surfaces encore ouvert
