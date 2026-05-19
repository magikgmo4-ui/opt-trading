---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01_00_START
doc_type: chantier/start
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01
machine: admin-trading
status: active
lifecycle_stage: real_usage_test
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - bundles/operator-export/README.md
  - bundles/operator-export/HANDOFF.md
  - bundles/operator-export/CHECKLIST_VERIFICATION.md
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01/
---

# 00_START — GO_OPT_TRADING_ADMIN_TRADING_TELEGRAM_WEBHOOK_REAL_USAGE_TEST_01

## Objet

Tester en usage reel controle le flux webhook/Telegram cote admin-trading :
reception, logs, payload controle, guards actifs, preuve de non-trading.

## Contexte

- `alert_webhook` est ACTIVE_CONTINUITY cote cursor-ai.
- La gate admin-trading est documentee mais le perimetre Telegram/webhook n'a jamais ete teste en usage reel depuis la machine admin-trading.
- Ce GO valide la boucle complete de reception webhook -> traitement -> notification Telegram sans franchir la gate de trading.

## Machine

- **Proprietaire** : admin-trading.
- **Rattachement** : bloc ADMIN_TRADING (MACHINE_WORK_SPLIT_ANTI_CONFLICT_01).
- **Machine cible** : admin-trading (Linux, systemd).
- **Mode** : test controle, doc-only + execution supervisee sur machine.

## Base de depart

- Branche : `sot/mainline` synchronisee.
- Lectures obligatoires :
  - `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` — bloc ADMIN_TRADING
  - `bundles/operator-export/README.md` — etat cursor-ai
  - `bundles/operator-export/HANDOFF.md` — handoff operateur
  - `bundles/operator-export/CHECKLIST_VERIFICATION.md` — checklist

## Structure du GO

| Fichier | Contenu |
| --- | --- |
| `00_START.md` | Ce fichier |
| `10_ADMIN_TRADING_PRECHECK.md` | Verification etat admin-trading, guards, runtime |
| `20_TELEGRAM_WEBHOOK_SCOPE.md` | Perimetre complet du flux Telegram/webhook |
| `30_REAL_USAGE_TEST_PLAN.md` | Plan de test en usage reel controle |
| `40_LOGS_AND_EVIDENCE.md` | Logs et preuves de reception |
| `50_GUARDS_AND_NO_TRADE_PROOF.md` | Preuves guards actifs + aucun trade reel |
| `60_ROLLBACK_PLAN.md` | Plan de rollback |
| `90_CLOSEOUT.md` | Verdict PASS/FAIL |

## Contraintes

- `trade_allowed=false`.
- Aucun ordre reel.
- Aucun secret dans le repo.
- Aucun endpoint production non valide.
- Logs et preuves obligatoires.
- Patch minimal (pas de modification runtime).
- Ne pas melanger avec Claude artifacts.

## Invariants

- Machine cible : admin-trading.
- Ne pas ouvrir la gate de trading.
- Ne pas modifier `webhook_server.py` ni `modules/webhook/`.
- Ne pas toucher systemd ni runtime.
- Ne pas exposer `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `TV_WEBHOOK_KEY`.
- `trade_allowed=false` et `admin_trading_runtime=false` dans le template.
- Engine `TV_TEST` ou equivalent TEST uniquement.
- Doc-only cote repo ; execution supervisee cote machine admin-trading.

## Sortie attendue

- Verdict PASS/FAIL.
- Etat admin-trading verifie.
- Preuves de reception webhook.
- Preuves de notification Telegram.
- Preuves de non-trading.
- Branche poussee.
- Point de reprise.
