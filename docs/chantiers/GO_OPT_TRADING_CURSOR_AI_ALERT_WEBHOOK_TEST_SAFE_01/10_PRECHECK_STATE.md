---
doc_id: GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_TEST_SAFE_01_10_PRECHECK_STATE
doc_type: chantier/precheck_state
repo: opt-trading
machine: cursor-ai
status: active
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
---

# 10_PRECHECK_STATE — Precheck et etat initial

## Branche de depart

- **Branche** : `go/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_TEST_SAFE_01`
- **Base** : `sot/mainline`
- **HEAD** : `2facaa6` (PR #209 merge)

## Etat Git

- [x] `git status` clean.
- [x] `sot/mainline` synced avec `origin/sot/mainline`.
- [x] Aucun fichier modifie avant creation des docs.

## Rattachement machine

- **Machine proprietaire** : `cursor-ai`.
- **Bloc dans MACHINE_WORK_SPLIT** : CURSOR_AI > alert_webhook.
- **Verification** : alert_webhook est bien dans le bloc CURSOR_AI.
- **Admin-trading** : non reference dans le contexte de ce GO.

## Fichiers sources pertinents

| Fichier | Existe | Contenu |
| --- | --- | --- |
| `modules/tradingview_observer/templates/alert_webhook_template_v1.json` | OUI | Template JSON avec flags securite |
| `docs/chantiers/...ALERT_WEBHOOK_TEMPLATE_01/20_TEMPLATE_SPEC.md` | OUI | Spec du template |
| `docs/chantiers/...ALERT_WEBHOOK_TEMPLATE_01/30_TEST_PROCEDURE.md` | OUI | Options A/B de test |
| `docs/chantiers/...ALERT_WEBHOOK_APPLICATION_ACTIVE_01/30_APPLICATION_REQUIREMENTS.md` | OUI | Preconditions application reelle |
| `docs/chantiers/...ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01/30_SAFE_PAYLOAD_SPEC.md` | OUI | Spec payload safe |
| `docs/chantiers/...ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01/40_VALIDATION_MATRIX.md` | OUI | 12 checks de validation |

## Preconditions confirmees

- [x] Pre-admin gate spec mergee (PR #208).
- [x] Operator reprise packet merge (PR #209).
- [x] Template JSON integre.
- [x] Flags securite actifs : `trade_allowed=false`, `admin_trading_runtime=false`.
- [x] Option A documentee dans `30_APPLICATION_REQUIREMENTS.md`.
- [x] Aucun secret, token, .env present dans le repo.

## Exclusions

- Aucun endpoint de production.
- Aucun admin-trading.
- Aucun webhook_server.py.
- Aucun systemd.
- Aucun risk engine.
