---
doc_id: GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01_20_PRE_GATE_REQUIREMENTS
doc_type: chantier/pre_gate_requirements
repo: opt-trading
machine: cursor-ai
status: active
links:
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_ALERT_WEBHOOK_APPLICATION_ACTIVE_01/40_ADMIN_TRADING_GATE.md
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01/70_ADMIN_TRADING_GATE.md
---

# 20_PRE_ADMIN_GATE_REQUIREMENTS

Prerequis avant toute ouverture d'admin-trading pour alert_webhook.

## Inputs requis

| Input | Emplacement | Statut |
| --- | --- | --- |
| Template JSON | `modules/tradingview_observer/templates/alert_webhook_template_v1.json` | PRESENT |
| Flags securite | Dans le template (`trade_allowed`, `admin_trading_runtime`) | ACTIFS |
| Spec template | `docs/chantiers/...ALERT_WEBHOOK_TEMPLATE_01/20_TEMPLATE_SPEC.md` | PRESENT |
| Limits et securite | `docs/chantiers/...ALERT_WEBHOOK_TEMPLATE_01/40_LIMITS_AND_SECURITY.md` | PRESENT |
| Gate admin-trading existante | `docs/chantiers/.../40_ADMIN_TRADING_GATE.md` | PRESENT |
| Parent plan gate | `docs/chantiers/.../70_ADMIN_TRADING_GATE.md` | PRESENT |
| Machine work split | `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` | PRESENT |

## Decisions necessaires avant ouverture

### Decision 1 — Verification cursor-ai complete

- [ ] Plan parent cursor-ai merge et close.
- [ ] Claude artifacts operator pack merge.
- [ ] Bundles workflow actif.
- [ ] alert_webhook application verifiee (template, flags, docs).

### Decision 2 — Demande explicite

Phrase requise de l'operateur :

```text
chantiers pour admin-trading
```

Tant que cette phrase n'est pas prononcee, admin-trading reste ferme.

### Decision 3 — Validation de securite

- [ ] Aucun endpoint webhook production dans le diff.
- [ ] Aucun token, secret, .env dans le diff.
- [ ] `trade_allowed` = `false`.
- [ ] `admin_trading_runtime` = `false`.
- [ ] Conformite `NO_RUNTIME_NO_SENSITIVE_RULES.md`.

### Decision 4 — Contexte machine

- [ ] Machine actuelle = cursor-ai.
- [ ] Le bloc ADMIN_TRADING de `MACHINE_WORK_SPLIT` est le bon contexte.
- [ ] L'operateur sait qu'il change de machine.

### Decision 5 — Etat Bundles

- [ ] Bundles workflow actif pret a etre utilise pour documenter le passage de gate.
- [ ] Aucun bundle admin-trading cree sans demande explicite.

## Ce qui n'est pas un prerequis

- Avoir teste avec un endpoint reel (non necessaire pour la spec).
- Avoir déclenché une alerte reelle (interdit dans cette spec).
- Avoir modifie `webhook_server.py` (interdit).
- Avoir ouvert un service systemd (interdit).
