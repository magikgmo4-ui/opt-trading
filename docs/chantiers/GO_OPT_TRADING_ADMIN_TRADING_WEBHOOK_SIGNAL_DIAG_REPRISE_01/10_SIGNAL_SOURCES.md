---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01_SIGNAL_SOURCES
doc_type: signal_sources
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_REPRISE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 10_SIGNAL_SOURCES - Signal Sources

## Regle de lecture

- aucun secret lu
- aucune alerte reelle envoyee
- aucune requete HTTP emise vers le webhook, ngrok ou TradingView externe

## Sources confirmees

| Source | Statut | Preuve | Chemins / fonctions |
| --- | --- | --- | --- |
| Ingress webhook `TradingView -> POST /tv` | CONFIRMED | route FastAPI et docs | `webhook_server.py:364-493`, `docs/API.md:3-6`, `docs/ARCHITECTURE.md:7-16` |
| Validation d'acces HMAC / localhost-only | CONFIRMED | garde d'entree avant normalisation | `webhook_server.py:338-351` |
| Normalisation vers evenement interne | CONFIRMED | construction du dict `evt` | `webhook_server.py:439-454` |
| Persistance normalisee dans `state/events.jsonl` | CONFIRMED | `record_event(evt)` puis `append_jsonl` | `webhook_server.py:143-148`, `webhook_server.py:456` |
| Exposition read-only des evenements | CONFIRMED | endpoint `/api/events` | `webhook_server.py:507-510` |
| Exposition read-only des metriques derivees | CONFIRMED | endpoint `/api/metrics` | `webhook_server.py:512-514`, `webhook_server.py:262-335` |
| Vue UI des derniers signaux | CONFIRMED | dashboard `/dash` et lecture `/api/events` | `webhook_server.py:759`, `webhook_server.py:671-722` |

## Sources ou comportements hypotheses

| Source / comportement | Statut | Pourquoi |
| --- | --- | --- |
| Payload TradingView exact hors repo | HYPOTHESIS | le format d'alerte amont n'est pas documente ici au-dela des champs lus dans `tv_webhook()` |
| Logging brut dans `logs/tv_webhooks.jsonl` | HYPOTHESIS | mention documentaire dans `docs/ARCHITECTURE.md`, mais non confirme par la lecture retenue de `webhook_server.py` |
| Origine precise des `POST /tv` observes en systemd | HYPOTHESIS | activite locale visible, mais sans attribution metier prouvee dans ce GO |
| Timestamp source TradingView distinct du `_ts` serveur | HYPOTHESIS | aucun champ horodatage amont distinct n'est lu dans la route webhook |

## Chemins et fonctions pertinents

- `webhook_server.py:338-351` -> `require_key()`
- `webhook_server.py:364-493` -> `tv_webhook()`
- `webhook_server.py:143-148` -> `append_jsonl()` / `record_event()`
- `webhook_server.py:233-335` -> `read_events()` / `metrics()`
- `webhook_server.py:507-514` -> `/api/events`, `/api/metrics`
- `docs/API.md`
- `docs/ARCHITECTURE.md`

## Conclusion

La source productrice confirmee est le webhook `TradingView -> POST /tv`, avec normalisation locale puis persistance append-only dans `state/events.jsonl`. Les signaux exposes downstream sont donc des evenements normalises serveur-side, pas des payloads TradingView bruts.
