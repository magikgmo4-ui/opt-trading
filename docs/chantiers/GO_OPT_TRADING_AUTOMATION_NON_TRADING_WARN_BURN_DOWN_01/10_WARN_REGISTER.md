# 10_WARN_REGISTER

Inventaire des 13 WARN issus du rollout non-trading (PR #690).

## Registre

| # | WARN | Phase | Gate | Description | Priorité |
|---|------|-------|------|-------------|----------|
| 1 | `strict-worker-readonly-smoke` | 01 | PRECHECK_PASS | strict_worker readonly smoke test passé en precheck uniquement, pas en E2E réel | P3 |
| 2 | `.env permissions 0644` | 03 | WARN | `.env` world-readable (0o644) contient `AIRTABLE_API_KEY` | P0 |
| 3 | `REVIEW_DRAFT absent de tasks.index.json` | 05 | WARN | Capability drift : capability `REVIEW_DRAFT` déclarée dans le code mais absente du registre | P1 |
| 4 | `CLOSEOUT_DRAFT absent de tasks.index.json` | 05 | WARN | Capability drift : capability `CLOSEOUT_DRAFT` déclarée dans le code mais absente du registre | P1 |
| 5 | `handoff_bricks.py source manquante` | 05 | WARN | Service handoff référencé mais seul `.pyc` présent, source `.py` absente | P1 |
| 6 | `handoff_renderer.py source manquante` | 05 | WARN | Service handoff référencé mais seul `.pyc` présent, source `.py` absente | P1 |
| 7 | `FastAPI absent dans venv cible` | 06 | WARN | `fastapi_available: false` dans le venv ; localcms conçu pour uvicorn | P2 |
| 8 | `kill switch widget absent LocalCMS` | 06 | WARN | Aucun widget d'arrêt d'urgence dans l'UI LocalCMS | P2 |
| 9 | `Gmail bridge non implémenté` | 07 | WARN | Target `gmail` déclarée mais bridge inexistant | P1 |
| 10 | `Calendar bridge non implémenté` | 07 | WARN | Target `calendar` déclarée mais bridge inexistant | P1 |
| 11 | `Drive bridge non implémenté` | 07 | WARN | Target `drive` déclarée mais bridge inexistant | P1 |
| 12 | `KG repo index entries sans bricks` | 07 | WARN | 3 entrées dans l'index sans implémentation de bricks correspondantes | P1 |
| 13 | `Gmail/Calendar/Drive canary non implémentés` | 08 | WARN | Canary tests pour gmail/calendar/drive absents | P1 |

## Statuts possibles

- `CLOSED` — corrigé et vérifié
- `DECLASSIFIED` — déterminé comme non-bloquant avec justification
- `CARRIED_FORWARD_WITH_REASON` — reporté à un futur GO avec raison documentée
