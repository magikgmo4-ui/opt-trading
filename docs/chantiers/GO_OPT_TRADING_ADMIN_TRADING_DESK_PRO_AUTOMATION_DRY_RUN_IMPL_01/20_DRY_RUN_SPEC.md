---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DRY_RUN_IMPL_01_SPEC
doc_type: dry_run_spec
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DRY_RUN_IMPL_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 20_DRY_RUN_SPEC - Dry Run Spec

## Input

- `signal_event_payload`: V0 ou V1
- `visual_context`: dict V1 optionnel
- `desk_snapshot`: dict requis en phase 1

## Output

Un dict de synthese local contenant:

- `mode="dry_run"`
- `status` dans `PASS`, `WARN`, `FAIL`
- `no_trade=True`
- `no_telegram=True`
- `no_webhook=True`
- `no_systemd=True`
- `errors`: liste structuree
- `warnings`: liste structuree
- `signal_event`, `visual_context`, `desk_snapshot`
- `join_checks`
- `summary`

## Regles de statut

| Cas | Statut |
| --- | --- |
| input critique invalide | `FAIL` |
| input critique valide mais contexte incomplet | `WARN` |
| tout valide sans reserve | `PASS` |

## Regles phase 1

- `desk_snapshot` manquant => blocking
- `visual_context` manquant => warning non bloquant
- `signal_event` V0 => normalise automatiquement via l'adapter
- `signal_event` V1 => accepte tel quel puis valide
- normalisation symbole detectee => warning, pas erreur

## Semantiques de securite

- aucune ecriture runtime live
- aucune requete reseau
- aucun appel systemd
- aucune emission Telegram
- aucune action trade

## RISKS

- À qualifier.
