---
doc_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01_DEP_TREE
doc_type: chantier_architecture_tree
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01
status: open
lifecycle_stage: analysis
topic_keys:
  - opt-trading
  - references
  - dependances
  - arbre
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/ARCHITECTURE.md
  - docs/architecture/REPO_SURFACES_MAP.md
  - registry/README.md
  - workflow_ai/WORKFLOW.md
  - webhook_server.py
  - adapters/webhook_to_perf.py
  - perf/perf_app.py
  - deploy_module_multi_machine/README.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/10_synthese_repertoires_top_level.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/11_synthese_bloc_a_canoniques.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/12_synthese_bloc_b_runtime.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/13_synthese_bloc_c_state.md
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/14_synthese_bloc_d_local.md
---

# Arbre des references et dependances repo

## Objet
Figer un arbre repo-level des references et dependances structurantes, sans rebasculer dans un audit file-by-file.

## Regle de lecture
- arbre logique et repo-first
- dependances verifiees sur les points d'entree et docs structurantes
- pas d'exhaustivite pretendue sur chaque module interne

## Arbre repo-level

```text
opt-trading
|
|-- racine minimale
|   |-- README.md
|   |-- requirements.txt
|   |-- .env.example
|   |-- webhook_server.py
|   `-- bitget_bridge.py
|
|-- pilotage canonique
|   |-- docs/
|   |   |-- governance/
|   |   |-- architecture/
|   |   |-- index/
|   |   |-- chantiers/
|   |   `-- master_pack/
|   |-- registry/
|   `-- workflow_ai/
|
|-- runtime et execution
|   |-- modules/
|   |-- shared/
|   |-- adapters/
|   |-- schemas/
|   |-- perf/
|   |-- scripts/
|   |-- tools/
|   |-- packages/
|   |-- deploy_module_multi_machine/
|   `-- tradingview/
|
|-- etat, produits et preuves
|   |-- state/
|   |-- data/
|   |-- student/
|   |-- contracts/
|   |-- audit/
|   `-- tests/
|
`-- local, archive, cache
    |-- _archive/
    |-- tmp/
    |-- __pycache__/
    |-- .ruff_cache/
    |-- .uv-cache/
    |-- .uv-python/
    `-- .secrets/
```

## Sens des references

```text
docs/ -------------------------------> gouverne la lecture humaine du repo
registry/ ---------------------------> decrit la structure machine-readable
workflow_ai/ ------------------------> impose la methode d'execution

tradingview/ -> webhook_server.py ---> state/events.jsonl
                                     -> state/router_state.json
                                     -> state/risk_config.json
                                     -> /perf/event (optionnel)

adapters/webhook_to_perf.py --------> normalise la transition webhook -> perf
perf/perf_app.py -------------------> perf/perf.db + UI /perf/* + /desk/*

modules/ <-------------------------- webhook_server.py, perf/perf_app.py, scripts/, tools/
shared/ <--------------------------- webhook_server.py, perf/perf_app.py
registry/ <------------------------- readers modules/* + deploy_module_multi_machine/

state/ -----------------------------> etat runtime durable leger
data/ ------------------------------> sous-produits et sorties metier
student/ ---------------------------> surface machine embarquee
contracts/ + tradingview/ ---------> contrats et compatibilite d'entree
audit/ -----------------------------> preuves ponctuelles et packs d'audit

_archive/ + tmp/ + caches ---------> jamais upstream
```

## Dependances verifiees

### 1. Couche canonique
- `docs/ARCHITECTURE.md` reference `docs/architecture/REPO_SURFACES_MAP.md`, `registry/*`, `state/events.jsonl` et `perf/perf.db`.
- `docs/architecture/REPO_SURFACES_MAP.md` pose la carte humaine, renvoie vers `registry/*`, et traite `workflow_ai/` comme doctrine locale d'execution.
- `workflow_ai/WORKFLOW.md` depend explicitement de `docs/master_pack/mission_starter_pack/00_mission_start_guide.md`, des surfaces kanban dans `docs/ot/*`, de `modules/validated_prompt_factory/README.md`, et de la continuite `deploy_module_multi_machine`.

### 2. Couche declarative
- `registry/machines_registry.yaml` est declare comme source pour les readers machine et pour `deploy_module_multi_machine`.
- `registry/modules_registry.yaml` sert de catalogue declaratif des modules et de leurs dependances.
- `registry/ui_surfaces_registry.yaml` est consomme par `modules/ui_registry_msi`.
- `registry/wrappers_registry.yaml` est consomme par `modules/wrappers_registry_reader`.

### 3. Couche runtime d'entree
- `webhook_server.py` importe `modules.env.env`, `shared.logger`, `modules.risk_engine`, `modules.execution_engine`, `modules.position_engine`, `modules.engines.registry` et `modules.auth.webhook_key`.
- `webhook_server.py` ecrit dans `state/events.jsonl`, `state/router_state.json` et `state/risk_config.json`.
- `webhook_server.py` emet aussi, si la perf est disponible, vers `PERF_URL + /perf/event`.
- `bitget_bridge.py` est un shim racine tres fin vers `modules.simex_bitget_bridge.app.simex_bitget_bridge`.

### 4. Couche runtime perf
- `adapters/webhook_to_perf.py` centralise le mapping `WebhookEvent -> PerfEvent`.
- `perf/perf_app.py` importe `modules.env.env`, `shared.logger`, `modules.desk_pro.api.routes` et `modules.desk_pro.mount`.
- `perf/perf_app.py` persiste dans `perf/perf.db` et expose les surfaces `/perf/*` et `/desk/*`.

### 5. Couche ops et deploiement
- `scripts/` reste la couche de wrappers et de verification autour des modules et des surfaces runtime.
- `tools/` porte des utilitaires et bridges contextuels, en aval du runtime.
- `deploy_module_multi_machine/README.md` declare une dependance explicite a `registry/machines_registry.yaml`, `registry/modules_registry.yaml` et aux modules sources sous `/opt/trading/modules/<module>`.

### 6. Couche downstream
- `state/` recoit l'etat runtime leger et les checkpoints techniques.
- `data/` recoit les artefacts produits par domaine.
- `student/` est une surface machine a part entiere, avec ses propres scripts, exports et validations.
- `contracts/` et `tradingview/` servent de bord d'integration.
- `audit/` contient des preuves ponctuelles, non pilotantes.

## Lecture de dependance retenue
1. `docs/` est upstream humain.
2. `registry/` est upstream declaratif machine.
3. `workflow_ai/` cadre la methode, mais ne remplace ni `docs/` ni `registry/`.
4. `modules/` est le coeur fonctionnel runtime.
5. `scripts/`, `tools/`, `deploy_module_multi_machine/` sont des couches d'orchestration et d'usage, pas la source fonctionnelle primaire.
6. `state/`, `data/`, `audit/` sont downstream.
7. `_archive/`, `tmp/`, caches et secrets locaux ne doivent jamais devenir upstream.

## Points de vigilance
- `modules/` est trop dense pour un arbre interne complet dans ce parent.
- `scripts/` melange wrappers structurants et aides contextuelles; l'arbre reste donc volontairement au niveau repo.
- la racine contient encore deux entrypoints applicatifs (`webhook_server.py`, `bitget_bridge.py`) qui ne doivent pas servir de precedent pour remonter d'autres artefacts au top-level.
- `data/journal/` reste une sous-surface de donnees; ce n'est pas un retour du systeme `journal/` supprime.

## Point de reprise
Utiliser ce document comme carte de dependance avant tout nouveau reclassement physique de surface.

## RISKS

- À qualifier.
