# ARCHITECTURE — Vue d’ensemble

## Flux principal
TradingView → `POST /tv` → `state/events.jsonl` + `journal.md` (+ optional: perf OPEN) → UI `/dash`

## Performance
`POST /perf/event` → SQLite `perf/perf.db` → endpoints `/perf/*` + UI `/perf/ui`

## Persistance
- `logs/tv_webhooks.jsonl` : brut (si activé)
- `state/events.jsonl` : normalisé
- `perf/perf.db` : trades + events perf

## Modules
- `shared/telegram_notify.py` : notifications
- `tools/journal_from_paste.py` : journalisation assistée
