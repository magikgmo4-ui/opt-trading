---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_REQUIREMENTS_REQUESTS_FIX_01_GAPS
doc_type: gaps_and_next
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_REQUIREMENTS_REQUESTS_FIX_01
status: closed
created_at: 2026-05-26
---

# 40_GAPS_AND_NEXT_GO

## Gap ciblé — CLOSED

| Gap | Statut avant ce GO | Statut après |
|-----|--------------------|--------------|
| `requests absent du venv` (gap env) | OPEN | **CLOSED** |
| `notification_dispatcher` import non prouvé resilient | OPEN | **CLOSED** |

**Root cause** : `requests==2.32.5` était déjà déclaré dans `requirements.txt` depuis la création du repo. Le gap réel était un venv non synchronisé et l'absence de tests prouvant la résilience du système d'import lazy introduit en PR #830.

**Résolution** :
1. `requirements.txt` — aucun changement nécessaire (requests déjà présent).
2. `notification_dispatcher/app/__init__.py` — aucun changement nécessaire (lazy import déjà en place).
3. `modules/notification_dispatcher/tests/test_import_safety.py` — **9 tests ajoutés**, prouvent le contrat sans modifier le venv.

## Gaps restants (non ciblés par ce GO)

| Gap | Statut | Résolution suggérée |
|-----|--------|---------------------|
| `test_strategy_adapter.py` — 4 failures count mismatch | Pré-existant | GO dédié registry count |
| `test_desk_pro_*.py` — 3 failures | Pré-existant | GO dédié desk_pro |
| PF_OPENCLAW_ORCHESTRATOR_FULL : pas de run live E2E | Extension | GO E2E live (post gate papier) |
| `shared/telegram_notify.py` — import requests eager | Acceptable | Optionnel : rendre lazy si souhaité |

## Prochaine étape suggérée

Aucun GO fils immédiat requis sur ce périmètre. Le parent `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` reste CLOSED/REVIEWED.

Si un GO live E2E est planifié, il devra s'assurer que `pip install -r requirements.txt` est exécuté dans l'environnement cible avant tout lancement.
