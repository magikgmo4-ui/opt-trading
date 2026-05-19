# 10_UI_CURRENT_MAPPING

Generated: 2026-05-19

## Surface 1 — localcms (port 8000)

Repo : `/home/ghost/localcms` — indépendant de opt-trading.

| Endpoint | Méthode | Rôle | État |
|----------|---------|------|------|
| `/` | GET | Index HTML — charge `localcms-v5.html` (SPA) | PASS |
| `/health` | GET | `{"ok": true}` | PASS |
| `/api/shared/list` | GET | Liste les modules partagés | PASS |
| `/api/shared/read` | GET | Lecture d'un fichier module | PASS |
| `/api/shared/download` | GET | Téléchargement fichier | PASS |
| `/api/shared/search` | GET | Recherche dans modules | PASS |
| `/api/config` | GET | Config globale | PASS |
| `/api/config/{module_id}` | GET/POST | Config par module | PASS |
| `/api/installer/scan` | GET | Scan modules installables | PASS |
| `/api/installer/inspect` | GET | Inspection pré-install | PASS |
| `/api/installer/precheck` | POST | Vérification pré-install | PASS |
| `/api/installer/install` | POST | Installation module | PASS |
| `/api/installer/history` | GET | Historique installs | PASS |
| `/api/installer/backups` | GET | Liste backups | PASS |
| `/api/installer/rollback` | POST | Rollback install | PASS |
| `/api/installer/restore` | POST | Restauration backup | PASS |

**UI :** SPA `localcms-v5.html` — sidebar avec sections "use" (vert) et "dev" (violet), navigation par onglets.
**Contrainte port :** Incompatible avec webhook server (port 8000 partagé).

---

## Surface 2 — Desk Pro (port 8010)

Module : `modules/desk_pro/api/routes.py`

### Endpoints HTML (pages)

| Endpoint | Rôle | État |
|----------|------|------|
| `/desk/ui` | Page principale — Pipeline Status + Snapshot + Form | PASS |
| `/desk/toolbox` | Page outils — shortcuts, SSH tunnel, diagnostics | PASS |

### Endpoints API JSON

| Endpoint | Méthode | Rôle | État |
|----------|---------|------|------|
| `/desk/health` | GET | `{"ok": true}` hardcodé — connectivité HTTP seulement | PASS (toujours) |
| `/desk/status` | GET | Santé complète : webhook, perf, webhook_activity, probe_errors | PASS |
| `/desk/errors` | GET | Historique probe errors (max 50) | PASS |
| `/desk/alerts` | GET | État dispatch alertes + historique JSONL | PASS |
| `/desk/alert/test` | POST | Smoke alert (Telegram/webhook) | PASS/skipped selon env |
| `/desk/snapshot` | GET | Desk snapshot (source: fixture/live) | PASS |
| `/desk/form` | POST | Scoring form → ScoreResult | PASS |
| `/desk/logs/latest` | GET | Dernières N lignes log UI | PASS |

**Note `/desk/status/enhanced` :** N'existe pas dans le code — référencé dans bundle mais absent.

### Sections de `/desk/ui`

| Card | Source données | Bouton |
|------|---------------|--------|
| Pipeline Status | `/desk/status` (live poll) | Refresh |
| Snapshot | `/desk/snapshot` | Refresh |
| Scoring Form | `/desk/form` POST | Submit |

---

## Surface 3 — Perf (port 8010, sous-module)

| Endpoint | Rôle | Référence code |
|----------|------|----------------|
| `/perf/summary` | Résumé performance | health-check + simex bridge |
| `/perf/open` | Positions ouvertes | `_probe_url` dans routes.py |
| `/perf/equity` | Points equity | mapping bundle |
| `/perf/event` | Ingestion event perf | simex bridge |
| `/perf/trades` | Liste des trades | mapping bundle |

**Note :** Routes perf définies dans le module FastAPI principal (partagé avec Desk Pro sur 8010).

---

## Surface 4 — Alert Pipeline

| Composant | Mécanisme | État |
|-----------|----------|------|
| Telegram | `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` via `_telegram_send()` | optionnel |
| Webhook générique | `ALERT_WEBHOOK_URL` via `_webhook_send()` | optionnel |
| JSONL fallback | `/opt/trading/tmp/desk_pro_alerts.jsonl` | toujours actif |
| Cooldown | `ALERT_COOLDOWN_SEC` (défaut 300s) | actif |
| Trigger | `health=down` ou `health=degraded` dans `/desk/status` | actif |

---

## Surface 5 — Runtime Supervision

| Script | Rôle | État |
|--------|------|------|
| `scripts/deskpro_watchdog.sh` | Poll actif ports 8000/8010, ALERT/WARN classifié | PASS |
| `scripts/runtime_healthcheck.sh` | Boot healthcheck | PASS |
| `scripts/diagnose.sh` | Diagnostic runtime | PASS |
| `scripts/desk_pro_cmd.sh` | Raccourcis cmd (sanity/health/logs) | PASS |
| `scripts/desk_pro_menu.sh` | Menu interactif | PASS |
| `scripts/desk_pro_sanity.sh` | Sanity check Desk Pro | PASS |

**Classification watchdog (post PR #607):**
- Port DOWN → ALERT
- `/desk/health` fail → ALERT
- `webhook:fail`, `perf:fail`, `probe_errors:fail` avec ports UP → ALERT
- `webhook_activity:fail/warn` seul → WARN (pas d'ALERT spam)
