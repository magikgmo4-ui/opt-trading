---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01_TARGET
doc_type: automation_target
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 20_AUTOMATION_TARGET - Automation Target

## Resultat cible

Desk Pro doit pouvoir s'executer de facon automatique en mode sur, sans trade reel, a partir des artefacts deja valides.

## Capacites cibles

1. Consommer `signal_event` V1 via l'adapter local
2. Consommer `visual_context` V1 ou ses references equivalentes
3. Consommer `desk_snapshot` comme source image stable
4. Produire un `latest` / `report` / `synthesis` local et partageable
5. Rester en mode dry-run permanent tant qu'aucun GO live distinct n'a ete valide
6. Ne produire aucun side effect externe non autorise

## Mode operationnel cible

| Aspect | Cible |
| --- | --- |
| Mode | dry-run read-only |
| Trigger | cadence determinee ou evenement gate |
| Inputs minimum | `desk_snapshot` frais + `signal_event` V1 optionnel |
| Outputs minimum | synthesis JSON + report texte/HTML/MD |
| Trade reel | interdit |
| Telegram | interdit par defaut |
| systemd enable | interdit avant GO timer dedie |

## Principe de conception

L'automatisation ne doit pas dependre d'un chainage fragile webhook -> capture -> decision. Elle doit pouvoir fonctionner avec des artefacts asynchrones, tolere le stale, et degrader proprement vers un mode synthese partielle si un input manque.
