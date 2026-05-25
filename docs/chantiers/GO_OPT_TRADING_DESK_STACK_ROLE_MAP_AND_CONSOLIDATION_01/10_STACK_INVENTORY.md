---
doc_id: GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01_STACK_INVENTORY
doc_type: stack_inventory
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - desk
  - desk_pro
  - inventory
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_DESK_STACK_ROLE_MAP_AND_CONSOLIDATION_01/00_INITIAL_PROJECT_DOC.md
---

# 10_STACK_INVENTORY

## Baseline current

| Module | Baseline current | Registry modules | Family guess |
| --- | --- | --- | --- |
| `desk_analyze` | oui | oui | `desk` |
| `desk_capture_inputs` | oui | oui | `desk` |
| `desk_common` | oui | non | `desk` |
| `desk_retention` | oui | oui | `desk` |
| `desk_snapshot_ingest` | oui | oui | `desk` |
| `desk_state` | oui | oui | `desk` |
| `desk_pro` | oui | non | `desk_pro` |
| `desk_pro_dashboard` | oui | oui | `desk_pro` |
| `desk_pro_orchestrator` | oui | non | `desk_pro` |
| `desk_pro_runner` | oui | oui | `desk_pro` |

## Vue d'ensemble de stack

| Module | Role constate | Classement retenu |
| --- | --- | --- |
| `desk_pro` | coeur partage API/UI/service | owner canonique de stack |
| `desk_pro_runner` | facade operateur et entrypoint CLI | facade operateur canonique |
| `desk_pro_orchestrator` | backbone d'execution pipeline | orchestrateur coeur |
| `desk_pro_dashboard` | visualisation et export des runs | surface dashboard complementaire |
| `desk_common` | chemins runtime et support shared minimal | support shared |
| `desk_snapshot_ingest` | ingestion snapshots en amont | satellite ingest |
| `desk_capture_inputs` | extraction inputs Vision depuis snapshots | satellite ingest/analysis |
| `desk_state` | fabrication state canonique `/desk/state/latest.json` | satellite state |
| `desk_retention` | hygiene et retention artefacts | satellite retention |
| `desk_analyze` | analyse consolidee a partir des snapshots locaux | satellite analysis |

## Coeur `desk_pro*`

### `desk_pro`

- `README.md` le decrit comme surface partagee pour l'API `/desk/*`, le rendu UI et la logique de service
- `mount.py` monte directement le router FastAPI
- `api/routes.py` porte les endpoints `/desk/*`
- `service/aggregator.py` agrege snapshots, market metrics et vision context

Lecture:

- `desk_pro` est le centre de gravite fonctionnel de la stack
- il n'est pas une facade operateur
- il ne remplace pas `desk_pro_runner` ni `desk_pro_dashboard`

### `desk_pro_runner`

- expose l'entrypoint CLI operateur
- orchestre `desk_pro_orchestrator` et `desk_pro_dashboard`
- README: facade operateur module-level de la stack Desk Pro

### `desk_pro_orchestrator`

- execute le pipeline complet des engines
- produit les runs `data/desk_runs/*`
- alimente `desk_pro_dashboard`

### `desk_pro_dashboard`

- rend les sorties du run en terminal/JSON/HTML
- consomme `run_summary.json`, `portfolio_engine.json`, `journal_engine.json`, `perf_engine.json`
- n'est pas autonome; il consomme l'orchestrateur et est surfe par le runner

## Satellites `desk_*`

### `desk_common`

- support shared minimal pour chemins runtime `/opt/trading/desk/*`
- pas d'entrypoint produit principal
- role support confirme par README

### `desk_snapshot_ingest`

- Step A
- ingere les captures SFTP et maintient `latest.json` + `history.jsonl`
- sert l'amont des snapshots locaux

### `desk_capture_inputs`

- Step D
- extrait des `tv_inputs` depuis les snapshots via OpenAI Vision
- alimente les inputs Desk

### `desk_state`

- Step E
- fusionne snapshots + inputs optionnels vers `/opt/trading/desk/state/latest.json`
- reste adjacent a la stack, sans remplacer les surfaces `desk_pro*`

### `desk_retention`

- Step 0 hygiene
- gere prune et retention des artefacts

### `desk_analyze`

- Step B
- analyse consolidee a partir de `desk/snapshots/latest.json`
- module adjacent, pas centre de gravite de la suite

## Nature de l'ensemble

Verdict d'inventaire:

- il ne s'agit pas d'une famille simple a survivant unique
- il s'agit d'une stack complementaire avec :
  - un coeur partage `desk_pro`
  - une facade operateur `desk_pro_runner`
  - une execution `desk_pro_orchestrator`
  - une visualisation `desk_pro_dashboard`
  - plusieurs satellites `desk_*`
