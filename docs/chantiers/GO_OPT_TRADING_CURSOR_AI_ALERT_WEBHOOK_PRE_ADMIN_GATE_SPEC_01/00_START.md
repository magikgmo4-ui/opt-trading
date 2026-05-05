---
doc_id: GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01_00_START
doc_type: chantier/start
repo: opt-trading
branch: go/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01
machine: cursor-ai
status: active
lifecycle_stage: pre_admin_gate_spec
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01/
  - docs/index/inbox/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01.md
---

# 00_START — GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01

## Objet

Preparer la spec de gate avant toute ouverture admin-trading pour alert_webhook, sans ouvrir admin-trading, sans modifier runtime et sans declencher d'alerte reelle.

## Etat valide

- PR #205 : parent operational plan cursor-ai integre.
- PR #206 : Claude artifacts operator pack integre.
- PR #207 : Bundles workflow actif integre.
- `alert_webhook = ACTIVE_CONTINUITY`.
- `admin-trading gate fermee`.
- `Runtime non modifie`.
- `Bundles = workflow actif cursor-ai`, produit non ferme.

## Structure du GO

| Fichier | Contenu |
| --- | --- |
| `00_START.md` | Ce fichier |
| `10_SOURCE_STATE.md` | Etat des sources |
| `20_PRE_ADMIN_GATE_REQUIREMENTS.md` | Prerequis avant ouverture admin-trading |
| `30_SAFE_PAYLOAD_SPEC.md` | Spec de payload safe |
| `40_VALIDATION_MATRIX.md` | Matrice de validation |
| `50_RISKS_AND_BLOCKERS.md` | Risques et blockers |
| `60_OPEN_ADMIN_TRADING_CRITERIA.md` | Criteres d'ouverture future admin-trading |
| `90_CLOSEOUT.md` | Verdict et closeout |

## Invariants

- Machine cible : cursor-ai.
- Ne pas ouvrir admin-trading.
- Ne pas modifier runtime.
- Ne pas declencher d'alerte reelle.
- Ne pas marquer alert_webhook comme ferme.
- Ne pas marquer Bundles produit comme ferme.
- Spec de gate, pas application runtime.
