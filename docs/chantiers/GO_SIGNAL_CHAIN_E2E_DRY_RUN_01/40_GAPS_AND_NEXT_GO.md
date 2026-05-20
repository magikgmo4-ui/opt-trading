---
doc_id: GO_SIGNAL_CHAIN_E2E_DRY_RUN_01_GAPS_AND_NEXT_GO
doc_type: gaps
repo: opt-trading
go_id: GO_SIGNAL_CHAIN_E2E_DRY_RUN_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 40_GAPS_AND_NEXT_GO

## Gaps constates

- Le journal n'affiche que le nombre de previews Telegram; le contenu des messages est uniquement dans le report pipeline (step `1c_notification_dispatcher_dry_run`).
- `daily_session_journal.py --sync-sheets` appelle un subprocess; retour utile mais integrable in-process si besoin.
- Le pipeline utilise `strategy_id=e2e_dry_run`, ce qui declenche des warnings "unknown strategy_id" (strategy registry).
- Les checks LocalCMS sont best-effort; un mode "skip localcms" explicite pourrait stabiliser certains environnements.

## Next GO (candidats)

- Exposer un extrait des messages Telegram (first N chars) dans le daily session journal.
- Ajouter un `strategy_id` de fixture connu (ou enregistrer `e2e_dry_run`) pour eviter les warnings.
- Integrer la sync Sheets en appel direct (module) avec une surface dry-run unifiee (pas de subprocess).
