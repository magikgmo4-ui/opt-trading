---
doc_id: GO_OPT_TRADING_CURSOR_AI_OPERATOR_REPRISE_PACKET_01_60_ADMIN_TRADING_GATE_STATUS
doc_type: chantier/admin_trading_gate_status
repo: opt-trading
machine: cursor-ai
status: active
links:
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01/70_ADMIN_TRADING_GATE.md
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01/60_OPEN_ADMIN_TRADING_CRITERIA.md
---

# 60_ADMIN_TRADING_GATE_STATUS

## Statut

**ADMIN-TRADING = FERME, NON OUVERT**

## Phrase d'activation

```text
chantier pour admin-trading
```

Cette phrase doit etre prononcee explicitement par l'operateur. Aucune autre formulation n'ouvre la gate.

## Conditions avant ouverture

| # | Condition | Statut actuel |
| --- | --- | --- |
| 1 | Demande explicite "chantier pour admin-trading" | NON DEMANDE |
| 2 | Validation matrix (12 checks) | NON APPLIQUE (gate fermee) |
| 3 | Sequence cursor-ai complete (positions 1-4) | EN COURS (position 4 active) |
| 4 | Contexte machine valide (passage cursor-ai → admin-trading) | NON APPLICABLE |
| 5 | Bundles workflow actif disponible | OK |

## Interdits tant que la gate est fermee

- Modifier `webhook_server.py`.
- Modifier ou creer des unites systemd.
- Modifier le risk engine.
- Modifier tout module sous `modules/admin-trading/`.
- Creer des branches admin-trading depuis cursor-ai.
- Activer `trade_allowed: true`.
- Activer `admin_trading_runtime: true`.
- Router un template vers un endpoint de production.

## Ce que la gate n'empeche pas

- Lire la documentation admin-trading existante.
- Documenter des specs de gate (comme ce GO).
- Preparer des bundles cursor-ai (sans contenu admin-trading).

## Apres ouverture (futur)

Meme apres ouverture de la gate, chaque action runtime sur admin-trading necessite une decision explicite. La gate ouvre le droit de travailler sur admin-trading, pas le droit de tout modifier sans controle.
