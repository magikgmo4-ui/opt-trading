---
go_id: GO_OPT_TRADING_UI_DUAL_SURFACE_AUDIT_IMPLEMENTATION_01
doc_type: initial_project_doc
repo: opt-trading
status: open
created_at: 2026-05-18
surface: doc-only / audit
runtime_mutation: false
---

# 00_INITIAL_PROJECT_DOC
## GO_OPT_TRADING_UI_DUAL_SURFACE_AUDIT_IMPLEMENTATION_01

---

## 1_MASTER_TARGET

```text
Auditer les deux surfaces UI distinctes — Desk Pro (modules opt-trading) et localcms
(/home/ghost/localcms) — puis préparer une implémentation minimale basée uniquement
sur les docs, scripts et contrats existants, pour visualisation, utilisation UI et test.
```

---

## 2_INITIAL_PROJECT_DOC

Document initial figé. Correction factuelle prouvée uniquement.

---

## 3_INITIAL_NEED

```text
Le projet dispose de deux UI distinctes avec des rôles différents.
Il faut auditer l'existant, identifier ce qui fonctionne déjà,
puis implémenter une visualisation et un usage UI testable
sans casser les rôles existants ni fusionner les surfaces.
```

---

## 4_MASTER_PROJECT_PLAN

```text
1. Vérifier les repos (git status).
2. Auditer Desk Pro (modules opt-trading).
3. Auditer localcms (/home/ghost/localcms).
4. Identifier scripts, routes, tests existants.
5. Identifier les gaps.
6. Proposer implémentation minimale par surface.
7. Smoke test uniquement si scripts existants le permettent.
```

---

## 7_CANONICAL_STATE

### Correction critique : "Desk Pro" ≠ repo séparé

```text
Desk Pro n'est PAS un repo séparé.
Desk Pro est une famille de modules DANS opt-trading.
db-layer est la machine d'hébergement, pas un repo UI.
```

### Repos impliqués

| Repo | Path | Branche courante | État |
| --- | --- | --- | --- |
| opt-trading | `/opt/trading` | `go/GO_OPT_TRADING_UI_DUAL_SURFACE_AUDIT_IMPLEMENTATION_01` | propre |
| localcms | `/home/ghost/localcms` | `go/GO_LOCALCMS_DATA_SOURCES_M4_ACCEPTANCE_01` | propre, chantier M4 en cours |
| localcms_runtime | `/home/ghost/localcms_runtime` | — (non git) | dossier partagé de validation |

### Surface 1 — Desk Pro (modules opt-trading)

| Module | Path | Rôle |
| --- | --- | --- |
| `desk_pro` | `modules/desk_pro/` | Core — FastAPI routes `/desk/*`, UI HTML, service aggregator/scoring |
| `desk_pro_dashboard` | `modules/desk_pro_dashboard/` | Visualization — metrics, positions, risk |
| `desk_pro_orchestrator` | `modules/desk_pro_orchestrator/` | Orchestration des runs |
| `desk_pro_runner` | `modules/desk_pro_runner/` | Façade opératoire principale |
| `desk_analyze` | `modules/desk_analyze/` | Analyse |
| `desk_capture_inputs` | `modules/desk_capture_inputs/` | Capture inputs |
| `desk_common` | `modules/desk_common/` | Commun |
| `desk_snapshot_ingest` | `modules/desk_snapshot_ingest/` | Ingestion snapshots |
| `desk_state` | `modules/desk_state/` | État desk |
| `desk_retention` | `modules/desk_retention/` | Rétention |

**Point d'intégration** : `perf/perf_app.py` monte `modules.desk_pro.api.routes` et `modules.desk_pro.mount`.

**Routes exposées** : `GET /desk/*` via `modules/desk_pro/api/routes.py`

**UI** : `modules/desk_pro/ui/page.py` → rendu `HTMLResponse`

**Scripts** :
- `modules/desk_pro/scripts/sanity_check.sh`
- `modules/desk_pro_dashboard/scripts/menu.sh`, `cmd.sh`, `sanity_check.sh`

**Tests existants** :
- `tests/test_desk_pro_dry_run.py`
- `tests/test_desk_pro_combined_input_smoke.py`
- `tests/test_desk_pro_artifact_output.py`
- `tests/fixtures/admin_trading_contract_smoke/desk_snapshot_minimal.json`

**Data** : `data/desk_runs/` — runs `desk_run_YYYYMMDD_HHMMSS`

### Surface 2 — localcms (/home/ghost/localcms)

| Module | Path | Rôle |
| --- | --- | --- |
| M1 — shared_explorer | `api/shared_explorer.py` | `/api/shared/*` — lecture `/home/ghost/localcms_runtime/shared` |
| M2 — cms_installer | `api/cms_installer.py` | `/api/installer/*` — installation modules |
| M3 — config_store | `api/config_store.py` | `/api/config/*` — gestion config |
| M4 — data-sources | `modules/data-sources.js` | `52/52 PASS` — sélectionné, non formalisé |

**Frontend** : `localcms-v5.html` — sert les modules JS via `/modules/*.js`

**Port** : 8000 — `uvicorn main:app --host 0.0.0.0 --port 8000`

**Tests** : adopt 8/8 PASS, shared_explorer integration 23/23 PASS, config_store 11/11 PASS

**Lien avec opt-trading** : AUCUN live — indépendants par design (`DOC_ONLY_IMPLEMENTATION_READY`)

### localcms_runtime (/home/ghost/localcms_runtime)

```text
Dossier partagé de validation — non git.
modules/ : hello-mod.js, test-module.js
shared/  : readme.md, docs/, install-backups/, install-logs/, install-queue/
Rôle : sandbox de validation pour GO_LOCALCMS_DBLAYER_ENV_SETUP_01
```

---

## 9_SELECTED_SOLUTION

```text
Ne pas fusionner les deux surfaces.
Deux axes indépendants :

Axe A — Desk Pro (opt-trading) :
  visualisation opérationnelle basée sur routes /desk/* existantes
  smoke via tests existants (test_desk_pro_dry_run.py etc.)

Axe B — localcms :
  viewer / navigation docs
  implémentation post-seuil Phase 1 (≥2026-05-30) si besoin prouvé
```

---

## 10_SELECTED_SETUP

| Surface | Lancement | Port | Tests |
| --- | --- | --- | --- |
| Desk Pro (perf_app) | `uvicorn perf.perf_app:app` | à confirmer | `python3 -m unittest tests/test_desk_pro_dry_run.py` |
| localcms | `uvicorn main:app --host 0.0.0.0 --port 8000` | 8000 | `npm test` (adopt), `pytest tests/integration_test_shared_explorer.py` |
| LocalCMS FastAPI db-layer | `modules/localcms/app/main.py` | 8700 | appel direct `_build_metrics()` |

---

## 11_KEY_DECISIONS

- Desk Pro et localcms restent des surfaces séparées
- Toute intégration passe par contrat/source explicite
- Aucun live sync entre localcms et opt-trading supposé
- Aucun chantier stratégique enfant avant ≥2026-05-30
- Desk Pro : priorité sur l'existant (routes + tests déjà présents)

---

## 12_INVARIANTS

- Ne pas déplacer la logique métier vers localcms
- Ne pas mélanger viewer (localcms) et runtime (Desk Pro)
- Ne pas créer de dépendance implicite non documentée
- Ne pas modifier les index globaux sans nécessité prouvée
- dry-run only pendant Phase 1 observation

---

## 13_ESTABLISHED

| Fait | Preuve |
| --- | --- |
| Desk Pro = modules opt-trading, pas repo séparé | `find /opt/trading/modules -name "desk_*"` |
| Routes `/desk/*` existantes | `modules/desk_pro/api/routes.py` |
| UI HTML existante | `modules/desk_pro/ui/page.py` |
| Tests dry_run, smoke, artifact_output | `tests/test_desk_pro_*.py` |
| sanity_check.sh existant | `modules/desk_pro/scripts/sanity_check.sh` |
| localcms port 8000, M1/M2/M3 PASS | `main.py`, tests adopt |
| localcms ≠ opt-trading indexé | `grep -Rni` → NOT FOUND |
| localcms_runtime = sandbox non-git | `ls /home/ghost/localcms_runtime/` |

---

## 14_HYPOTHESIS

| Hypothèse | Statut |
| --- | --- |
| `perf_app.py` expose `/desk/*` en runtime actif | À vérifier — port inconnu |
| Desk Pro dashboard génère HTML/JSON consultable | Non vérifié en runtime |
| localcms peut consommer `/metrics/daily:8700` via module futur | NON PROUVÉ — DOC_ONLY |

---

## 15_REMAINING_GAP

| Gap | Surface | Priorité |
| --- | --- | --- |
| Port de `perf_app.py` non confirmé | Desk Pro | haute |
| Commande de lancement perf_app documentée ? | Desk Pro | haute |
| localcms → opt-trading : aucun contrat live | localcms | post-seuil |
| M4 data-sources non formalisé dans localcms | localcms | localcms-side |
| `GO_LOCALCMS_FULL_TEST_CAMPAIGN_01` non lancé | localcms | localcms-side |

---

## 16_TODO

```text
[Axe A — Desk Pro — prioritaire]
1. Confirmer port et commande de lancement perf_app.py
2. Lancer sanity_check.sh : modules/desk_pro/scripts/sanity_check.sh
3. Lancer smoke : python3 -m unittest tests/test_desk_pro_dry_run.py
4. Si PASS → Desk Pro viewer opérationnel confirmé

[Axe B — localcms — post-seuil Phase 1]
5. Attendre ≥2026-05-30
6. Décider si module observation consumer à ajouter
7. GO_LOCALCMS_FULL_TEST_CAMPAIGN_01 : lancer côté localcms indépendamment

[Gate]
Aucun GO enfant stratégique avant ≥2026-05-30.
```

---

## 17_RESUME_POINT

```text
Audit PASS — artefacts posés sur branche go/GO_OPT_TRADING_UI_DUAL_SURFACE_AUDIT_IMPLEMENTATION_01.
Desk Pro : modules opt-trading opérationnels, tests existants, routes /desk/* actives.
localcms : M1/M2/M3 PASS, M4 sélectionné, aucun lien live avec opt-trading.
Prochaine action : lancer sanity_check.sh + test_desk_pro_dry_run.py (Axe A).
```

---

## UI_SURFACE_MATRIX

| Surface | Repo | Rôle établi | Scripts | Routes/UI | Tests | Données | Statut |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Desk Pro | opt-trading | Visualisation opérationnelle | `sanity_check.sh`, `menu.sh`, `cmd.sh` | `GET /desk/*`, `ui/page.py` (HTML) | `test_desk_pro_dry_run.py`, `test_desk_pro_combined_input_smoke.py`, `test_desk_pro_artifact_output.py` | `data/desk_runs/` | ACTIF — à confirmer runtime |
| LocalCMS | /home/ghost/localcms | Viewer / navigation / docs | `run.sh`, `run.bat` | `/api/shared/*`, `/api/installer/*`, `/api/config/*`, frontend `localcms-v5.html` | adopt 8/8, shared_explorer 23/23, config_store 11/11 | `localcms_runtime/shared/` | OPÉRATIONNEL |
| LocalCMS FastAPI db-layer | opt-trading `modules/localcms` | Métriques observation | — | `GET /metrics/daily` | smoke PASS (PR #528) | `data/journal/daily/*.json` | OPÉRATIONNEL port 8700 |

---

## IMPLEMENTATION_CANDIDATES

| Candidat | Repo | Type | Base existante | Risque | Test minimal |
| --- | --- | --- | --- | --- | --- |
| Smoke Desk Pro dry-run | opt-trading | test | `test_desk_pro_dry_run.py` | faible | `python3 -m unittest tests/test_desk_pro_dry_run.py` |
| Sanity Desk Pro | opt-trading | script | `modules/desk_pro/scripts/sanity_check.sh` | faible | `bash modules/desk_pro/scripts/sanity_check.sh` |
| Observation consumer localcms | localcms | module | aucune — DOC_ONLY | élevé | post-seuil Phase 1 |

---

## TEST_PLAN

| Test | Repo | Commande | Attendu | Statut |
| --- | --- | --- | --- | --- |
| Desk Pro dry-run | opt-trading | `python3 -m unittest tests/test_desk_pro_dry_run.py` | PASS | À exécuter |
| Desk Pro combined smoke | opt-trading | `python3 -m unittest tests/test_desk_pro_combined_input_smoke.py` | PASS | À exécuter |
| Desk Pro sanity | opt-trading | `bash modules/desk_pro/scripts/sanity_check.sh` | OK | À exécuter |
| localcms adopt | localcms | `npm test` | 8/8 PASS | PASS (établi) |
| localcms shared_explorer | localcms | `pytest tests/integration_test_shared_explorer.py` | 23/23 PASS | PASS (établi) |
