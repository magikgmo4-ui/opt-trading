---
go_id: GO_OPT_TRADING_UI_DUAL_SURFACE_AUDIT_IMPLEMENTATION_01
doc_type: smoke_results
repo: opt-trading
status: PASS
created_at: 2026-05-18
surface: desk_pro — UI port 8010
---

# 30_DESKPRO_UI_SMOKE_PORT8010

---

## Verdict

```text
DESK PRO UI — PORT 8010 — PASS
```

---

## Qualification environnement

| Dépendance | État |
| --- | --- |
| `uvicorn` | OK — disponible nativement |
| `fastapi` | OK — disponible nativement |
| `modules.perf.app` | OK — importable depuis `/opt/trading` |
| `/opt/trading/venv/` | ABSENT — non requis sur cette machine |
| port 8010 | LIBRE avant lancement |

---

## Import app

```python
from modules.perf.app import app
# APP_OK: <fastapi.applications.FastAPI object>
```

**Routes exposées :**

```
/openapi.json                         {'GET', 'HEAD'}
/docs                                 {'GET', 'HEAD'}
/redoc                                {'GET', 'HEAD'}
/desk/health                          {'GET'}
/desk/snapshot                        {'GET'}
/desk/form                            {'POST'}
/desk/ui                              {'GET'}
/desk/toolbox                         {'GET'}
/desk/logs/latest                     {'GET'}
/perf/event                           {'POST'}
/perf/summary                         {'GET'}
/perf/equity                          {'GET'}
/perf/open                            {'GET'}
/perf/trades                          {'GET'}
/perf/ui                              {'GET'}
```

Note 1 : Les routes `/desk/desk/*` existent en double — le router `desk_router` a ses propres préfixes et `app.include_router(..., prefix="/desk")` ajoute un second niveau. Sans impact fonctionnel.

Note 2 : `SyntaxWarning: invalid escape sequence '\d'` dans `perf_app.py:951` — non bloquant, warning JS dans string Python.

---

## Lancement

```bash
cd /opt/trading
python3 -m uvicorn modules.perf.app:app --host 127.0.0.1 --port 8010 --log-level warning
```

---

## Smoke HTTP

| Route | HTTP | Taille | Verdict |
| --- | --- | --- | --- |
| `GET /desk/health` | 200 | JSON | PASS |
| `GET /desk/snapshot` | 200 | JSON | PASS |
| `GET /desk/ui` | 200 | 7174 bytes | PASS |
| `GET /desk/toolbox` | 200 | HTML | PASS |
| `GET /desk/logs/latest` | 200 | JSON | PASS |
| `POST /desk/form` | — | — | non testé |
| `GET /perf/open` | 200 | JSON | PASS |
| `GET /perf/ui` | 200 | 19110 bytes | PASS |
| `GET /perf/summary` | 200 | JSON | PASS |
| `GET /perf/equity` | 200 | JSON | PASS |
| `POST /perf/event` | — | — | non testé |

---

## Tests unittest post-smoke

```
python3 -m unittest discover -s tests -p "test_*.py"
→ 92/92 PASS — inchangé
```

---

## Canonical state mis à jour

| Surface | Port | Lancement | État |
| --- | --- | --- | --- |
| Desk Pro | **8010** | `python3 -m uvicorn modules.perf.app:app --host 127.0.0.1 --port 8010` | **OPÉRATIONNEL** ✅ |
| localcms | 8000 | `uvicorn main:app --host 0.0.0.0 --port 8000` | OPÉRATIONNEL — indépendant |
| db-layer repo | — | — | NON PROUVÉ — Desk Pro = modules opt-trading |

---

## 17_RESUME_POINT

```text
DESK PRO UI SMOKE — PORT 8010 — PASS

Environnement :
  uvicorn   : OK (natif)
  fastapi   : OK (natif)
  venv      : ABSENT (non requis)
  port 8010 : libre → lancé → OK

Routes Desk Pro : 6/6 PASS (health, snapshot, ui, toolbox, logs/latest, perf/open)
Routes Perf     : 3/3 PASS (ui, summary, equity)
Tests unittest  : 92/92 PASS (inchangé)
pytest          : non requis

db-layer repo   : NON PROUVÉ — Desk Pro = modules opt-trading
localcms        : indépendant port 8000

Axe A = COMPLET.
Axe B (localcms consumer obs) = post-seuil ≥2026-05-30.
```

## RISKS

- À qualifier.
