# INDEX — Documentation Magikgmo

- **docs/ROADMAP.md** : roadmap annotée + critères Done
- **docs/ARCHITECTURE.md** : architecture (flux, persistance, composants)
- **docs/API.md** : endpoints + exemples `curl`
- **docs/RUNBOOK.md** : ops/debug (systemd, logs, réseau Windows/LAN)
- **docs/SCHEMAS.md** : schéma unique Event → Trade → Perf + adaptateur
- **schemas/webhook_event_v1.json** : JSON Schema v1 (source de vérité)

## Code — repères
- `webhook_server.py` : webhook `/tv` + UI `/dash` + persistance JSONL
- `perf/perf_app.py` : API perf + SQLite + UI `/perf/ui`
- `adapters/webhook_to_perf.py` : mapping webhook → perf_event
- `shared/telegram_notify.py` : notifications Telegram
- `tools/journal_from_paste.py` : génération d’entrées `journal.md`
