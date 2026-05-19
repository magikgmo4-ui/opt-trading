---
doc_id: GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01_70_ADMIN_TRADING_GATE
doc_type: chantier/admin_trading_gate
repo: opt-trading
machine: cursor-ai
status: active
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
---

# 70_ADMIN_TRADING_GATE

## Statut

**ADMIN-TRADING = NON OUVERT, GATE FERMEE**

## Conditions avant ouverture future

1. **Decision explicite requise** : l'operateur doit demander explicitement l'ouverture admin-trading.
2. **Spec de gate prealable** : `GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01` doit etre executee et close.
3. **Verification cursor-ai complete** :
   - Plan parent merge et close.
   - Claude artifacts operator pack merge.
   - Bundles produit au statut voulu.
   - alert_webhook application verifiee.
4. **Aucune action runtime automatique** : meme apres ouverture, les actions runtime sur admin-trading necessitent une decision explicite.

## Elements interdits sans ouverture

- Toute modification runtime.
- Toute action sur le serveur webhook.
- Toute action sur systemd.
- Toute action sur le risk engine.
- Tout commit touchant admin-trading.

## Regle de gate

- La gate est assuree par le routage machine (MACHINE_WORK_SPLIT).
- Cursor-ai ne cree pas de branches admin-trading sans demande.
- Toute violation de gate = rollback immediat.

## Branches admin-trading existantes

Les branches admin-trading existent dans le repo mais sont sous controle de la machine admin-trading. Cursor-ai ne les manipule pas sans ouverture explicite.

Voir `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`, bloc ADMIN_TRADING.
