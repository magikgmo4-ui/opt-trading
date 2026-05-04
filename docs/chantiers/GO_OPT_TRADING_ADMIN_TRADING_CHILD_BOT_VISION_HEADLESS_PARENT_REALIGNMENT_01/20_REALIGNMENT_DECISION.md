---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_PARENT_REALIGNMENT_01_DECISION
doc_type: realignment_decision
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_PARENT_REALIGNMENT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 20_REALIGNMENT_DECISION

## Decisions

### D1: bot_vision_headless n'est pas un parent machine autonome

**Justification**:
- Le plan post-PR197 dit: 1 parent par machine, maintenir idealement 1 chantier actif par machine
- admin-trading a deja `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` comme parent canonique
- Creer un deuxieme parent admin-trading fragmente la gouvernance
- bot_vision_headless est un workstream (module capture) sous admin-trading

### D2: bot_vision_headless devient un child/workstream sous admin-trading

**Rattachement**:
- Parent: `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01`
- Child review existant: les docs de review restent valides
- Child impl futur: `GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01`
- Thread: THREAD_MACHINE_ADMIN_TRADING (existant)

### D3: Le parent specialise est classe ABSORBED

**Classification**:
- `GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01` = ABSORBED
- N'a jamais ete dans les index canoniques (GO_INDEX, GO_CLOSED_INDEX, GO_PARENT_THREAD_MAP)
- Le contenu utile (review headless) est conserve dans le child review
- La notion de "parent" pour ce GO etait une erreur de classification

### D4: Conserver le contenu du review, ne pas supprimer

- Les 8 fichiers parent + 7 fichiers child review contiennent de la documentation utile
- Ils restent sur leur branche d'origine (go/GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01)
- Pas de suppression, pas de renommage
- Le prochain GO d'implementation les reference comme sources

### D5: Le prochain GO d'implementation est un child

- GO: `GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01`
- Parent: `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01`
- Type: child implementation (pas un parent)

## Arbre corrige

```
GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 (parent machine, OPEN)
  |
  +-- GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01 (PASS)
  +-- GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01 (PASS)
  +-- GO_OPT_TRADING_ADMIN_TRADING_VISION_INBOX_REPAIR_01 (PASS)
  +-- GO_OPT_TRADING_ADMIN_TRADING_DESK_BRIDGE_RETRY_01 (PASS)
  +-- GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SMOKE_01 (PASS)
  +-- GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_REVIEW_01 (PASS)
  +-- GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_IMPL_01 (NEXT)
  +-- (GO_OPT_TRADING_ADMIN_TRADING_PARENT_BOT_VISION_HEADLESS_CAPTURE_01) [ABSORBED]
```
