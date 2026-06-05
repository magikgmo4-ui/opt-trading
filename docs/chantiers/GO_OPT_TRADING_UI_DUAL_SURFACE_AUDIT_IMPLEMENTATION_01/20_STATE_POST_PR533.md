---
go_id: GO_OPT_TRADING_UI_DUAL_SURFACE_AUDIT_IMPLEMENTATION_01
doc_type: state_update
repo: opt-trading
created_at: 2026-05-18
status: open
---

# 20_STATE_POST_PR533

---

## 7_CANONICAL_STATE — post-PRs #531-533

### Repos

| Repo | Path | État |
| --- | --- | --- |
| opt-trading | `/opt/trading` | `sot/mainline @ fb890c4d` — propre |
| localcms | `/home/ghost/localcms` | branche `go/GO_LOCALCMS_DATA_SOURCES_M4_ACCEPTANCE_01` |
| db-layer | `/home/ghost/db-layer` | **NON EXISTANT** — Desk Pro = modules opt-trading, pas repo séparé |

### Test runner canonique

```
python3 -m unittest discover -s tests -p "test_*.py"
→ 92/92 PASS
pytest : non installé, non requis, ne pas ajouter
```

### Desk Pro (perf_app.py)

| Élément | Valeur |
| --- | --- |
| App | `modules.perf.app:app` (alias `perf.perf_app:app`) |
| Port | **8010** |
| URL | `http://127.0.0.1:8010` |
| Lancement | `python -m uvicorn modules.perf.app:app --host 0.0.0.0 --port 8010` |
| Script opérateur | `scripts/desk_pro_ui_toolbox_final_cmd.sh` |
| venv officiel | `/opt/trading/venv/` — absent, **non requis** (uvicorn/fastapi natifs) |
| Log | `/opt/trading/tmp/uvicorn_8010.log` |
| Routes Desk Pro | `GET /desk/*` via `modules/desk_pro/api/routes.py` |

### localcms

| Élément | Valeur |
| --- | --- |
| Port | 8000 |
| Lancement | `uvicorn main:app --host 0.0.0.0 --port 8000` |
| Modules actifs | M1 shared_explorer, M2 cms_installer, M3 config_store |
| Tests | adopt 8/8 PASS, shared_explorer 23/23 PASS, config_store 11/11 PASS |
| Lien opt-trading | AUCUN live — indépendant par design |

---

## 13_ESTABLISHED

| Fait | Preuve |
| --- | --- |
| Desk Pro port = 8010 | `scripts/desk_pro_ui_toolbox_final_cmd.sh` ligne 5-6 |
| Lancement via `modules.perf.app:app` | même script ligne 30 |
| venv `/opt/trading/venv/` absent — non requis | app lancée avec python natif (uvicorn/fastapi natifs) |
| `env/` présent mais non qualifié | `ls /opt/trading/` → `env`, `env.bak` |
| Desk Pro UI smoke PASS — port 8010 | `30_DESKPRO_UI_SMOKE_PORT8010.md` — 6 routes HTTP 200 |
| 92/92 unittest PASS post-PR #533 | `python3 -m unittest discover` → OK |
| pytest gap résolu — dead import supprimé | PR #533 — 2 lignes supprimées |
| db-layer = pas de repo séparé | `ls /home/ghost/db-layer` → NOT FOUND |

---

## 15_REMAINING_GAP

| Gap | Criticité | Action |
| --- | --- | --- |
| ~~`/opt/trading/venv/` absent — perf_app non lançable ici~~ | ~~haute~~ | **RÉSOLU** — venv absent OK, app lancée avec python natif (voir `30_DESKPRO_UI_SMOKE_PORT8010.md`) |
| `env/` présent — rôle non qualifié | moyenne | `ls /opt/trading/env/` → vérifier si venv ou module |
| Tests pytest-style (8 fichiers) non couverts par unittest | basse | non bloquant, campagne 92/92 suffit |
| localcms → observation consumer (bloc observation) | post-seuil | attendre ≥2026-05-30 |

---

## 16_TODO

```text
[Immédiat]
1. Qualifier /opt/trading/env/ — venv ou module Python ?
   → Si venv : vérifier si uvicorn disponible dedans
   → Tenter : /opt/trading/env/bin/python -m uvicorn modules.perf.app:app --port 8010

[Post-seuil ≥2026-05-30]
2. Axe B localcms consumer — si besoin prouvé post-Phase 1
3. Campagne pytest-style si pytest installé dans venv
```

---

## 17_RESUME_POINT

```text
Audit dual UI PASS — état documenté post-PRs #531-533.
Desk Pro : port 8010 confirmé, venv absent sur cette machine.
localcms : opérationnel port 8000, indépendant.
Prochaine action : qualifier env/ → tenter lancement perf_app port 8010.
```

## RISKS

- À qualifier.
