---
doc_id: GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_TEST_SAFE_01_00_START
doc_type: chantier/start
repo: opt-trading
branch: go/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_TEST_SAFE_01
machine: cursor-ai
status: active
lifecycle_stage: safe_test
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01/
  - docs/index/inbox/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_TEST_SAFE_01.md
---

# 00_START — GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_TEST_SAFE_01

## Objet

Tester l'application alert_webhook avec un endpoint local mock (`http://127.0.0.1:9999/tv-test`), sans admin-trading, sans endpoint de production, sans alerte reelle.

## Pourquoi ce GO apres PR #208 et #209

- PR #208 a defini la pre-admin gate spec (criteres, validation matrix, payload safe).
- PR #209 a clos la sequence cursor-ai positions 1-4.
- Ce GO est l'Option A de `50_NEXT_GO_OPTIONS.md` : test safe de l'application alert_webhook.
- Il applique la spec sans franchir la gate admin-trading.

## Machine

- **Proprietaire** : cursor-ai.
- **Rattachement** : bloc CURSOR_AI > alert_webhook (MACHINE_WORK_SPLIT).
- **Admin-trading** : non ouvert, gate fermee.

## Limites strictes

- Endpoint autorise : `http://127.0.0.1:9999/tv-test` uniquement.
- Aucun endpoint de production.
- Aucun admin-trading.
- Aucune alerte reelle.
- Aucun secret, token, .env.
- Flags securite : `trade_allowed=false`, `admin_trading_runtime=false`.

## Structure du GO

| Fichier | Contenu |
| --- | --- |
| `00_START.md` | Ce fichier |
| `10_PRECHECK_STATE.md` | Precheck et etat initial |
| `20_MOCK_ENDPOINT_SETUP.md` | Setup endpoint mock local |
| `30_TEST_PROCEDURE.md` | Procedure de test safe |
| `40_EXPECTED_RESULTS.md` | Resultats attendus |
| `50_ROLLBACK_PLAN.md` | Plan de rollback |
| `90_CLOSEOUT.md` | Verdict et closeout |

## Invariants

- Doc-only (procedure documentee, pas d'execution runtime automatique).
- Aucun admin-trading.
- Aucun secret.
- Mode de test : validation JSON sans envoi ou avec endpoint localhost uniquement.
