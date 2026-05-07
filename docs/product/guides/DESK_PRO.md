---
doc_id: OPT_TRADING_GUIDE_DESK_PRO
doc_type: user_guide
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/status/desk_pro_stack_canonique.md
  - docs/desk_pro_multi_machine_quick_reference.md
  - docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md
---

# Guide utilisateur - Desk Pro

## Ce que c'est

Desk Pro est une stack operationnelle multi-composants de capture, analyse, execution et visualisation desk trading.

## A quoi ca sert

Elle sert a operer le desk trading avec des runbooks, wrappers cmd/menu/sanity, un script admin reel et un dashboard de visualisation.

## Quand l'utiliser

- pour executer le pipeline desk quotidien ;
- pour visualiser les etats et artefacts desk ;
- pour capturer, analyser et journaliser les sessions trading.

## Quand ne pas l'utiliser

- comme source canonique (le repo prime) ;
- comme produit fini sans limites (le survivant unique n'est pas fige) ;
- pour du trading live automatise sans validation humaine.

## Prerequis

- acces au repo opt-trading ;
- wrappers desk installes (cmd, menu, sanity) ;
- acces a `scripts/admin_trading/desk_pro_cmd.sh` (runtime admin) ;
- lecture de `docs/status/desk_pro_stack_canonique.md` pour comprendre la structure.

## Commandes / acces

- Runtime admin : `scripts/admin_trading/desk_pro_cmd.sh`
- Wrappers : `cmd-desk_pro_runner`, `menu-desk_pro`, `sanity-desk_pro`
- Dashboard : `cmd-desk_pro_dashboard`
- Carte multi-machine : `docs/desk_pro_multi_machine_map.md`
- Runbook : `docs/desk_pro_multi_machine_quick_reference.md`

## Procedure simple

1. Verifier l'etat de la stack : `sanity-desk_pro`.
2. Lancer le pipeline desk : `cmd-desk_pro_runner`.
3. Consulter les artefacts : `cmd-desk_pro_dashboard` ou via `/shared/desk_pro/latest/`.
4. En cas d'incident : `docs/admin_trading_desk_pro_incident_recovery.md`.
5. Revenir au repo pour toute decision produit.

## Verification PASS

- `sanity-desk_pro` passe sans erreur ;
- `cmd-desk_pro_runner` produit des artefacts lisibles ;
- le dashboard affiche les derniers etats ;
- la documentation de la stack est accessible et a jour.

## Limites

- le survivant unique n'est pas fige : la stack comporte plusieurs composants sans produit unifie ;
- la frontiere entre `desk_pro*` et `desk_*` est encore en cours de clarification ;
- les wrappers `desk_pro` en racine (`scripts/desk_pro_*.sh`) sont geles, ne pas les utiliser ;
- la coquille `modules/desk_pro/` est gelee, ne pas l'utiliser comme module actif.

## Depannage

- Si un wrapper manque : `docs/desk_pro_release_ops_runbook.md`.
- Si une commande echoue : verifier `docs/admin_trading_desk_pro.md`.
- Si les artefacts ne sont pas a jour : relire `docs/db_layer_desk_pro_runbook.md`.

## Source canonique

- `docs/status/desk_pro_stack_canonique.md`
- `docs/desk_pro_multi_machine_quick_reference.md`
- `docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md`
- `docs/desk_pro_multi_machine_map.md`

## NEXT_GO

`GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01`
