---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_06_RUNTIME_EDGE_PLATFORM
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - modules
  - step-06
  - runtime-edge
  - platform
  - contracts
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
  - docs/ARCHITECTURE.md
  - webhook_server.py
  - perf/perf_app.py
  - modules/auth/README.md
  - modules/env/README.md
  - modules/health/README.md
  - modules/perf/README.md
  - modules/router/README.md
  - modules/scripts/README.md
  - modules/shared/README.md
  - modules/webhook/README.md
---

# Step 06 - family contracts `Runtime edge / platform`

## Statut
Complete.

## Objet
Durcir les frontieres `Runtime edge / platform` par contrats de couche et d'entrypoints, sans fusionner des surfaces fines qui portent des responsabilites differentes.

## Verifications utilisees
- lecture de `docs/ARCHITECTURE.md`
- lecture de `webhook_server.py`
- lecture de `perf/perf_app.py`
- lecture des README de :
  - `modules/auth`
  - `modules/env`
  - `modules/health`
  - `modules/perf`
  - `modules/router`
  - `modules/scripts`
  - `modules/shared`
  - `modules/webhook`

## Carte de famille
| Surface | Role retenu |
|---|---|
| `env` | bootstrap environnement et repertoires |
| `auth` | secrets et validation d'acces |
| `webhook` | logique reusable de parsing / handling du flux webhook |
| `webhook_server.py` | entrypoint applicatif racine du flux TV webhook |
| `health` | checks locaux de coherence runtime |
| `perf` | facade module pour la surface applicative Perf |
| `perf/perf_app.py` | application Perf reelle |
| `router` | facade shell d'inspection / routage local |
| `shared` | surface canonique inter-machines |
| `scripts` | facade module d'exploration, distincte de la racine `scripts/` |

## Contrats de couche
### 1. Bootstrap
- `env` charge `.env`, expose `project_root`, garantit `tmp/` et `data/`.
- `auth` consomme ensuite l'environnement et les secrets. Il ne doit pas devenir un bootstrap generaliste.

### 2. Bord d'entree webhook
- `webhook_server.py` reste l'entrypoint applicatif.
- `modules/webhook` reste la couche reusable et testable.
- le contrat doit rester :
  - `webhook_server.py` = wiring applicatif, IO, endpoints FastAPI
  - `modules/webhook` = parse, schema, handlers, logique reusable

### 3. Sante / monitoring
- `health` reste un check local de coherence.
- `perf/perf_app.py` reste l'application de monitoring / persistance Perf.
- `modules/perf` reste une facade operateur. Il ne doit pas dupliquer l'app Perf.

### 4. Facades shell
- `router` et `scripts` restent des facades legeres d'inspection. Ils ne doivent pas etre surpromus comme coeurs runtime.

### 5. Plateforme inter-machines
- `shared` reste une surface plateforme distincte, deja cadree avec `reseau/share/transfer`.
- il ne doit pas etre rabattu dans `env`, `router` ou `scripts`.

## Conventions a durcir
- entrypoints explicites :
  - `webhook_server.py` pour le webhook
  - `perf/perf_app.py` pour Perf
  - wrappers `cmd/menu/sanity` pour les facades module
- vocabulary de couche :
  - bootstrap
  - secret / auth
  - handler reusable
  - app entrypoint
  - health check
  - facade shell
- ownership clair des fichiers `state/`, `tmp/`, `data/`, `perf/perf.db`

## Ce qui doit rester separe
- `env` et `auth`
- `modules/webhook` et `webhook_server.py`
- `modules/perf` et `perf/perf_app.py`
- `health` et `perf`
- `scripts` module et racine `scripts/`
- `shared` et les autres surfaces runtime edge

## Risques a eviter
- faire grossir `env` jusqu'a englober secrets, runtime et logique produit
- reabsorber `modules/webhook` dans `webhook_server.py`
- confondre la facade `perf` avec l'application `perf`
- traiter `router` ou `scripts` comme modules produits alors qu'ils restent des facades structurelles

## Decision retenue
- oui a un durcissement de contrats et d'entrypoints
- non a une fusion physique
- prochaine execution utile si besoin :
  - documenter les fichiers de state possedes par chaque couche
  - normaliser les wrappers `status/info/path`
  - verifier les callers directs de `webhook_server.py` et `perf/perf_app.py`

## Rollback
- revert doc-only de cette note
- revert doc-only du plan si besoin

## Point de reprise
Contrats `Runtime edge / platform` cadres. Basculer vers `Repo / tooling / authoring`.

## RISKS

- À qualifier.
