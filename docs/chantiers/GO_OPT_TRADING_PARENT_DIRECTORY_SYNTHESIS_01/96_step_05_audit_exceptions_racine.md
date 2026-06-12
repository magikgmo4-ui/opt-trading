---
doc_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01_STEP_05_NOTE
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - step-05
  - racine
  - audit
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/94_plan_execution_step_by_step.md
  - docs/governance/REPO_ROOT_POLICY.md
  - webhook_server.py
  - bitget_bridge.py
---

# Step 05 — audit cible des exceptions racine

## Statut
Complete.

## Objectif
Confirmer les exceptions racine encore legitimes et separer ce qui est clairement actif de ce qui reste sous prudence.

## Scope
- `webhook_server.py`
- `bitget_bridge.py`
- verification des autres fichiers racine observes

## Verifications utilisees
- listing des fichiers racine via `Get-ChildItem -Force -File`
- recherche repo ciblee des references a `webhook_server.py`
- recherche repo ciblee des references a `bitget_bridge.py` et `simex_bitget_bridge`
- lecture de `webhook_server.py`
- lecture de `bitget_bridge.py`
- lecture de `scripts/smoke_tv_engine.py`
- lecture de `scripts/verify_all.sh`
- lecture de `scripts/simex_cmd.sh`
- lecture de `modules/simex_bitget_bridge/README.md`

## Preuves observees

### 1. Fichiers racine observes
- `.env.example`
- `README.md`
- `requirements.txt`
- `webhook_server.py`
- `bitget_bridge.py`

### 2. `webhook_server.py`
References repo explicites observees :
- `docs/API.md` : contrat `POST /tv`
- `docs/ARCHITECTURE.md` : flux `TradingView -> POST /tv -> state/events.jsonl`
- `docs/INDEX.md` : surface `/tv` + `/dash`
- `scripts/smoke_tv_engine.py` : import direct `from webhook_server import app`
- `scripts/verify_all.sh` : `python3 -m py_compile webhook_server.py`
- `scripts/desk_pro_hook.sh` : `webhook_server.py` liste parmi les candidats d'entree
- `tools/emit_tv_payload.py` : commentaire d'usage vers la route FastAPI de `webhook_server.py`

Lecture fonctionnelle observee :
- importe `modules.env.env`, `shared.logger`, `modules.risk_engine`, `modules.execution_engine`, `modules.position_engine`, `modules.engines.registry`, `modules.auth.webhook_key`
- persiste vers `state/events.jsonl`, `state/router_state.json`, `state/risk_config.json`
- emet optionnellement vers `PERF_URL + /perf/event`

Decision :
- `webhook_server.py` est confirme comme entrypoint racine legitime

### 3. `bitget_bridge.py`
Observation code :
- fichier shim minimal vers `modules.simex_bitget_bridge.app.simex_bitget_bridge:main`

References repo observees :
- `modules/simex_bitget_bridge/README.md` indique que le shim `bitget_bridge.py` reste disponible
- la documentation historique et les audits mentionnent encore le shim

Contre-preuve importante :
- les wrappers operateur actuels passent par `scripts/simex_cmd.sh`
- `scripts/simex_cmd.sh` appelle `modules/simex_bitget_bridge/cmd.sh`
- aucun caller repo explicite direct de `bitget_bridge.py` n'est confirme dans les scripts actifs observes

Decision :
- `bitget_bridge.py` reste en place par prudence
- statut retenu : `hold` conservatoire, pas `keep` plein
- aucun move physique tant qu'un lot dedie n'a pas statue sur l'usage hors repo ou sur une compat legacy encore requise

## Decision racine consolidee
- racine minimale stable confirmee : `README.md`, `requirements.txt`, `.env.example`, `webhook_server.py`
- exception encore ouverte : `bitget_bridge.py`
- aucun nouvel artefact opportuniste observe a la racine dans ce step

## Fichiers modifies
- `docs/governance/REPO_ROOT_POLICY.md`
- `docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/94_plan_execution_step_by_step.md`

## Rollback
- revert doc-only de `REPO_ROOT_POLICY.md`
- revert doc-only de `94_plan_execution_step_by_step.md`
- suppression de cette note si le step est annule

## Resultat
La discipline racine est plus nette :
- `webhook_server.py` est valide comme surface active
- `bitget_bridge.py` est explicitement fige sous arbitrage prudent

## Point de reprise
Passer au `Step 06` pour verifier les zones grises : `packages/`, `tests/`, `student/`, `data/`, `audit/`.

## RISKS

- À qualifier.
