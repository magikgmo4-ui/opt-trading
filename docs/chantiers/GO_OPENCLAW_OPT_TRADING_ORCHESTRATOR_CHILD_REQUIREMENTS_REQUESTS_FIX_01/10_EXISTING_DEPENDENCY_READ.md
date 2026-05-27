---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_REQUIREMENTS_REQUESTS_FIX_01_DEP_READ
doc_type: dependency_inventory
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_REQUIREMENTS_REQUESTS_FIX_01
status: closed
created_at: 2026-05-26
---

# 10_EXISTING_DEPENDENCY_READ — Inventaire des usages de `requests`

## Fichier canonique de dépendances

`requirements.txt` (racine repo) — convention repo, pas de pyproject.toml ni setup.cfg.

## État constaté

`requests==2.32.5` est présent dans `requirements.txt` à la ligne 14.

Le gap documenté dans la revue parent (« non dans venv ») est un gap **d'environnement**, pas de déclaration : le venv n'avait pas été synchronisé avec `pip install -r requirements.txt`.

## Inventaire des usages de `import requests`

| Fichier | Import | Type |
|---------|--------|------|
| `shared/telegram_notify.py:2` | `import requests` | eager, top-level |
| `modules/notification_dispatcher/app/dispatcher.py:8` | via `send_telegram_html` | indirect (telegram_notify) |
| `webhook_server.py:9` | `import requests` | eager, entry-point |
| `modules/openclaw_github_actions_bridge/app/bridge.py:4` | `import requests` | eager |
| `modules/simex_bitget_bridge/app/simex_bitget_bridge.py:4` | `import requests` | eager |
| `adapter_botpress_openclaw.py:233` | `import requests as r` | lazy (inside function) |
| `scripts/openclaw_gh_actions_*.py` | `import requests` | lazy ou eager |
| `tools/strategy/daily_scalping/fetch_bitget.py:28` | `import requests` | eager |

## Chaîne critique pour notification_dispatcher

```
notification_dispatcher/app/__init__.py
  → try: dispatcher.py
    → from shared.telegram_notify import send_telegram_html
      → import requests  ← point de rupture si requests absent
```

## Isolation réalisée (PR #830)

`notification_dispatcher/app/__init__.py` :
```python
from .events import PipelineEvent, EventType  # pas de deps externes

try:
    from .dispatcher import NotificationDispatcher
except ImportError:
    NotificationDispatcher = None  # fallback si requests absent
```

`events.py` — stdlib only (`dataclasses`, `typing`). Toujours importable.

## Conclusion

- `requests` est déclaré dans `requirements.txt` ✓
- Aucun ajout nécessaire dans requirements.txt
- Gap réel : venv non synchronisé → `pip install -r requirements.txt` résout
- Gap test : aucun test ne prouvait la robustesse de l'import sans requests → ajouté dans ce GO
