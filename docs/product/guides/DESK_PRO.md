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

# Guide - Desk Pro

## 1_MASTER_TARGET

Stack Desk Pro unifiee avec survivant unique, runbooks complets et dashboard produit.

## FINAL_TARGET

Pipeline operationnel de capture, analyse, execution et visualisation desk trading, avec un module unique et des wrappers standardises.

## CURRENT_STATE

`USABLE_LIMITED` -- Stack operationnelle active avec runbooks, wrappers et dashboard, mais survivant unique non fige et frontiere desk_pro / desk_* en cours de clarification.

## USAGE_ALLOWED_NOW

- Executer le pipeline desk quotidien.
- Visualiser les etats et artefacts desk.
- Capturer, analyser et journaliser les sessions trading.
- Utiliser les wrappers cmd/menu/sanity operationnels.

## USAGE_FORBIDDEN_NOW

- Traiter Desk Pro comme produit fini sans limites.
- Utiliser la coquille `modules/desk_pro/` (gelee).
- Utiliser les scripts racine `scripts/desk_pro_*.sh` (geles).
- Trading live automatise sans validation humaine.

## IMPLEMENTATION_PATH

1. Consolider la stack Desk Pro (survivant unique).
2. Clarifier la frontiere desk_pro vs desk_*.
3. Standardiser les wrappers.
4. Produire un closeout produit.

## CONTINUITY_STATE

Actif -- `GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01` en reprise.

## MACHINE / SURFACE

`admin-trading` (runtime admin reel).

## REPRISE_POINT

```text
docs/status/desk_pro_stack_canonique.md
docs/desk_pro_multi_machine_quick_reference.md
```

## TODO

1. Figer le survivant unique Desk Pro.
2. Documenter la frontiere desk_pro / desk_*.
3. Mettre a jour les wrappers et le runbook.

## REMAINING_GAP

Survivant unique non fige, frontiere desk_pro / desk_* en cours de clarification documentaire.

## NEXT_GO

`GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01`

## PROMOTION_CONDITIONS

`USABLE_LIMITED` -> `USABLE_NOW` quand :
- survivant unique fige,
- frontiere desk_pro / desk_* clarifiee,
- closeout produit pose.

## Ce que c'est

Desk Pro est une stack operationnelle multi-composants de capture, analyse, execution et visualisation desk trading.

## A quoi ca sert

Operer le desk trading avec runbooks, wrappers, script admin reel et dashboard.

## Quand l'utiliser

- Pour executer le pipeline desk quotidien.
- Pour visualiser les etats et artefacts desk.
- Pour capturer, analyser et journaliser les sessions.

## Quand ne pas l'utiliser

- Comme source canonique (le repo prime).
- Comme produit fini sans limites.
- Pour du trading live automatise sans validation humaine.

## Prerequis

- Acces au repo opt-trading.
- Wrappers desk installes (cmd, menu, sanity).
- Acces a `scripts/admin_trading/desk_pro_cmd.sh`.
- Lecture de `docs/status/desk_pro_stack_canonique.md`.

## Commandes / acces

- Runtime admin : `scripts/admin_trading/desk_pro_cmd.sh`
- Wrappers : `cmd-desk_pro_runner`, `menu-desk_pro`, `sanity-desk_pro`
- Dashboard : `cmd-desk_pro_dashboard`
- Carte multi-machine : `docs/desk_pro_multi_machine_map.md`

## Procedure simple

1. `sanity-desk_pro` -- verifier l'etat de la stack.
2. `cmd-desk_pro_runner` -- lancer le pipeline.
3. `cmd-desk_pro_dashboard` ou `/shared/desk_pro/latest/` -- consulter les artefacts.
4. Revenir au repo pour toute decision produit.

## Verification PASS

- `sanity-desk_pro` passe sans erreur.
- `cmd-desk_pro_runner` produit des artefacts lisibles.
- Le dashboard affiche les derniers etats.

## Limites

- Survivant unique non fige.
- Frontiere desk_pro / desk_* floue.
- Scripts racine `scripts/desk_pro_*.sh` geles (OT_OPS_05B).
- Coquille `modules/desk_pro/` gelee.

## Depannage

- Wrapper manquant : `docs/desk_pro_release_ops_runbook.md`.
- Commande echouee : `docs/admin_trading_desk_pro.md`.
- Artefacts pas a jour : `docs/db_layer_desk_pro_runbook.md`.

## Source canonique

- `docs/status/desk_pro_stack_canonique.md`
- `docs/desk_pro_multi_machine_quick_reference.md`
- `docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md`
