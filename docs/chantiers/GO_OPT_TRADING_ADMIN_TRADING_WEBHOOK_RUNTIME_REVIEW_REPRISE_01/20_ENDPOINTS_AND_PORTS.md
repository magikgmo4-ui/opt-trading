---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01_ENDPOINTS_PORTS
doc_type: endpoints_ports_map
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_REPRISE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 20_ENDPOINTS_AND_PORTS - Webhook Endpoints And Ports

## Sources lues

- `docs/API.md`
- `docs/ARCHITECTURE.md`
- `webhook_server.py`
- `systemctl status ...`
- `ss -ltnp | grep -E '(:8000|:8010|:4040)'`

## Ports confirmes

| Port | Surface | Etat | Source de preuve |
| --- | --- | --- | --- |
| `8000` | `tv-webhook` | confirme en ecoute | `ss -ltnp` + `tv-webhook.service` |
| `8010` | `tv-perf` | confirme en ecoute | `ss -ltnp` + `tv-perf.service` |
| `4040` | `ngrok` UI locale | confirme en ecoute | `ss -ltnp` + `ngrok-tv.service` |

## Endpoints confirmes par code ou doc

| Endpoint | Methode | Statut | Preuve |
| --- | --- | --- | --- |
| `/tv` | `POST` | confirme | `docs/API.md` + `webhook_server.py` |
| `/dash` | `GET` | confirme | `docs/API.md` + `webhook_server.py` |
| `/api/state` | `GET` | confirme | `docs/API.md` + `webhook_server.py` |
| `/api/events` | `GET` | confirme | `docs/API.md` + `webhook_server.py` |
| `/api/metrics` | `GET` | confirme | `docs/API.md` + `webhook_server.py` |
| `/api/risk/quote` | `GET` | confirme | `webhook_server.py` |
| `/api/reset_lock` | `POST` | confirme | `webhook_server.py` |
| `/perf/event` | `POST` | confirme, surface adjacente | `docs/API.md` |
| `/perf/summary` | `GET` | confirme, surface adjacente | `docs/API.md` |
| `/perf/equity` | `GET` | confirme, surface adjacente | `docs/API.md` |
| `/perf/open` | `GET` | confirme, surface adjacente | `docs/API.md` |
| `/perf/trades` | `GET` | confirme, surface adjacente | `docs/API.md` |
| `/perf/ui` | `GET` | confirme, surface adjacente | `docs/API.md` |

## Endpoints non confirmes ou non testes

| Endpoint | Etat | Note |
| --- | --- | --- |
| `/health` | non confirme | aucun handler `/health` n'a ete trouve dans `webhook_server.py`; l'ancien chantier stale mentionnait un `404`, mais cette reprise ne l'a pas appele |
| URL publique ngrok | non testee | aucune requete externe ou tunnel public n'a ete emise dans ce GO |

## Distinction confirme / hypothese

- confirme: declaration de route visible dans `webhook_server.py` ou reference explicite dans `docs/API.md`
- hypothese ou historique: route seulement mentionnee par ancien chantier, comportement non reexecute, ou dependance externe non appelee dans cette reprise

## Side effects

NONE
