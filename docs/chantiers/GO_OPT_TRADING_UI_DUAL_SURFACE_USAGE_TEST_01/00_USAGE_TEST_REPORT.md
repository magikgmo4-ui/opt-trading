---
go_id: GO_OPT_TRADING_UI_DUAL_SURFACE_USAGE_TEST_01
doc_type: usage_test_report
repo: opt-trading
status: PASS
created_at: 2026-05-18
---

# GO_OPT_TRADING_UI_DUAL_SURFACE_USAGE_TEST_01

## 1_MASTER_TARGET

Tester l'usage réel contrôlé des deux UI validées par PR #534 : localcms port 8000 et Desk Pro port 8010.

## 3_INITIAL_NEED

Passer du smoke technique à une validation d'utilisation UI : navigation, endpoints, pages disponibles, données visibles et limites mock/live.

## 7_CANONICAL_STATE

- PR #534 mergée (merge commit `8bd4d41a`)
- localcms port 8000 — FastAPI, routes `/`, `/health`, `/api/shared/`, `/api/installer/`, `/api/config/`
- Desk Pro port 8010 — FastAPI, routes `/desk/*`, `/perf/*`
- tests unittest 92/92 PASS
- pytest non requis
- db-layer non prouvé
- secrets/ untracked à exclure

## LOCALCMS_USAGE_RESULT

| Check | Résultat |
|---|---|
| port 8000 | OPÉRATIONNEL — lancé et répondu |
| `GET /` | 200 — page HTML LocalCMS v5 complète |
| `GET /health` | 200 — `{"status":"ok"}` |
| `GET /api/shared/` | 404 (pas de route racine, nécessite sous-chemin) |
| `GET /api/installer/` | 404 (pas de route racine, nécessite sous-chemin) |
| `GET /api/config/` | 307 redirect |

Page d'accueil LocalCMS v5 complète avec thème sombre, panneaux Config/Use/Dev. Navigation fonctionnelle. API accessible mais nécessite exploration des sous-routes.

**Verdict : PASS** — localcms UI opérationnelle et navigable sur port 8000.

## DESKPRO_USAGE_RESULT

| Check | Résultat |
|---|---|
| port 8010 | OPÉRATIONNEL — lancé et répondu |
| `GET /desk/health` | 200 — `{"ok":true,"module":"desk_pro","mode":"step2_mock"}` |
| `GET /desk/snapshot` | 200 — JSON avec metrics mock (BTC, DXY) |
| `GET /desk/ui` | 200 — page HTML Desk Pro complète |
| `GET /desk/toolbox` | 200 — page HTML Toolbox |
| `GET /desk/logs/latest` | 200 — JSON |
| `GET /perf/open` | 200 — `{"open":[]}` |
| `GET /perf/ui` | 200 — page HTML Perf Control Center complète |
| `GET /perf/summary` | 200 — JSON (equity=10000, zéro trades) |
| `GET /perf/equity` | 200 — JSON |
| `GET /` | 404 (pas de route racine — attendu) |

Page Desk Pro complète avec grille de cards, endpoints listés, style sombre.
Page Perf Control Center complète avec topbar, thème sombre, structure UI.

**Verdict : PASS** — Desk Pro UI opérationnelle et navigable sur port 8010.

## DATA_SOURCE_CLASSIFICATION

| Surface | Source | Type | Statut |
|---|---|---|---|
| localcms | frontend HTML (`localcms-v5.html`) | page statique + API | PASS |
| localcms | health | endpoint | PASS |
| Desk Pro | `step2_mock` | mock | PASS |
| Desk Pro | health/snapshot | mock + placeholders | PASS |
| Desk Pro | perf/ UI | vide (zéro trades) | PASS — attendu sans data live |
| Desk Pro | live data | live | NOT_PROVED — mode step2_mock uniquement |

Les deux UI sont fonctionnelles et navigables. Aucune donnée live réelle n'est branchée sur Desk Pro en local (mode `step2_mock`).

## 13_ESTABLISHED

| Fait | Preuve |
|---|---|
| localcms port 8000 opérationnel | `curl http://127.0.0.1:8000/` → 200 HTML |
| Desk Pro port 8010 opérationnel | `curl http://127.0.0.1:8010/desk/ui` → 200 HTML |
| Desk Pro mode `step2_mock` | `/desk/health` → `{"mode":"step2_mock"}` |
| Les deux UI lancées simultanément | ss-ltnp confirme 8000 et 8010 |
| unittest 92/92 PASS | `python3 -m unittest discover` → OK |
| PR #534 mergée | merge commit 8bd4d41a |

## 14_HYPOTHESIS

| Hypothèse | Statut |
|---|---|
| localcms API sous-routes fonctionnelles | NON TESTÉ — routes `/api/shared/...` non explorées |
| Desk Pro peut accepter des events live POST /perf/event | NON TESTÉ |
| desk_bridge service peut connecter data live | NON TESTÉ |
| db-layer est requis pour data live | HYPOTHÈSE NON PROUVÉE |

## 15_REMAINING_GAP

| Gap | Criticité | Action |
|---|---|---|
| Données Desk Pro en mode mock uniquement | haute | qualifier source live ou documenter step2_mock comme mode actuel |
| Routes API localcms non sondées (`/api/shared/files`, `/api/installer/bundle`, etc.) | basse | test d'exploration API si besoin |
| localcms M3 config_store non testé | basse | endpoint `/api/config/` répond mais retour non vérifié |
| Aucun POST event Desk Pro testé | moyenne | `POST /perf/event` non testé |

## 16_TODO

1. Décider si step2_mock est suffisant pour l'usage courant ou si data live est requise.
2. Si data live : qualifier la chaîne tv-webhook → `/perf/event`.
3. Si besoin API localcms : sonder sous-routes `/api/shared/`, `/api/installer/`, `/api/config/`.
4. Prochaine GO candidate : qualifier le flux data/trading réel.

## 17_RESUME_POINT

```text
Dual UI usage test PASS.
localcms : port 8000, page HTML complète, navigation fonctionnelle.
Desk Pro : port 8010, mode step2_mock, pages UI complètes, zéro data live.
92/92 unittest PASS inchangé.
PR #534 mergée (8bd4d41a).
Prochaine décision : suffisance du mode mock ou besoin data live.
```
