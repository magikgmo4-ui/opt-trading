# ARCHITECTURE — Vue d’ensemble

## Carte des surfaces
- carte humaine : `docs/architecture/REPO_SURFACES_MAP.md`
- registres machine-readable : `registry/*`

## Flux principal
TradingView → `POST /tv` → `state/events.jsonl` (+ optional: perf OPEN) → UI `/dash`

## Performance
`POST /perf/event` → SQLite `perf/perf.db` → endpoints `/perf/*` + UI `/perf/ui`

## Persistance
- `logs/tv_webhooks.jsonl` : brut (si activé)
- `state/events.jsonl` : normalisé
- `perf/perf.db` : trades + events perf

## Modules
- `shared/telegram_notify.py` : notifications
