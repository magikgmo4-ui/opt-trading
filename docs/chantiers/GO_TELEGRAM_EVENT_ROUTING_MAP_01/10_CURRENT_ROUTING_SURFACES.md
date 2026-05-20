---
doc_id: GO_TELEGRAM_EVENT_ROUTING_MAP_01_CURRENT_ROUTING_SURFACES
doc_type: inventory
repo: opt-trading
go_id: GO_TELEGRAM_EVENT_ROUTING_MAP_01
status: reference
source_kind: canonical
updated_at: 2026-05-19
---

# 10_CURRENT_ROUTING_SURFACES - État actuel

## Dispatcher (pipeline events → Telegram)

Preuve:

- `modules/notification_dispatcher/app/dispatcher.py`
- `modules/notification_dispatcher/app/events.py`

Caractéristiques:

- un seul `TELEGRAM_BOT_TOKEN` + un seul `TELEGRAM_CHAT_ID`
- `dispatch(dry_run=True)` retourne `{ok, dry_run, event_type, message}` (pas de post)
- en live: `requests.post("https://api.telegram.org/bot{token}/sendMessage")`

Event types actuels (`PipelineEvent.event_type`):

- `signal_received`
- `proposition_generated`
- `approval_required`
- `trade_executed`
- `result_known`
- `pipeline_error`
- `pipeline_info`

## Helper outbound (generic)

Preuve:

- `shared/telegram_notify.py`

Caractéristiques:

- helper utilitaire (texte) utilisé par plusieurs surfaces (hors dispatcher)
- destinations non standardisées (dépendant de l’appelant)

## Conclusion

Le repo possède déjà l’envoi Telegram, mais la destination est monolithique et ne reflète pas la taxonomie transverse (familles/types) définie dans `GO_EVENT_TAXONOMY_01`.

## Validation locale executee

Commande relancee dans cette passe :

```powershell
python -m pytest modules\notification_dispatcher\tests\test_strategy_id_adapter_readonly.py tests\e2e\test_e2e_dry_run_pipeline.py tests\test_signal_event_adapter.py tests\test_desk_pro_combined_input_smoke.py -q
```

Resultat observe :

```text
68 passed
```

## Ancrage umbrella

- `MASTER_TARGET` : contribuer au produit final total sans modifier l'envoi live
- `Kanban bundle` : reste la reference principale
- `Prochain item Kanban` : `GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01`
- `Gaps encore ouverts` : alias -> env, multi-bots, topics, branchement progressif par famille/type
