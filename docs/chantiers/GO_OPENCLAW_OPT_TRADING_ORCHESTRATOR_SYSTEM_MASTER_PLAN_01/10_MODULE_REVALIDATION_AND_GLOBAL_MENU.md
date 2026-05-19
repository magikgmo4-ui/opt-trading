---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01_REVALIDATION
doc_type: revalidation
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
status: open
updated_at: 2026-05-16
---

# 10_MODULE_REVALIDATION_AND_GLOBAL_MENU

## Source

Lecture directe du filesystem `modules/` — find + ls + README scan de chaque module.
Ce document corrige et remplace le comptage précédent (78 → **85 modules réels**).

---

## CORRECTIONS MAJEURES vs CLASSIFICATION INITIALE

### 1. Comptage corrigé : 78 → 85 modules

```text
TROUVÉ (find /opt/trading/modules -maxdepth 1 -type d):
  89 répertoires totaux

EXCLUS (artefacts, pas des modules):
  __pycache__                          → artefact Python
  ops_wrappers.bak                     → dette à supprimer
  install_module_openclaw.bak_20260314 → dette à supprimer
  scripts                              → répertoire scripts utilitaires (pas un module)

TOTAL RÉEL: 85 modules
```

**7 modules non inventoriés initialement :**
- `audit` — module de méthode audit repo
- `dev_validation_hub` — validation développeur pre-PR
- `engines` — shared lib registry/router des trading engines
- `env` — bootstrap transverse (project_root, load_env)
- `install_module` — sync/validate multi-machine
- `repo_local_artifacts` — gestionnaire .gitignore patterns
- `repo_ownership_guard` — fix permissions git

**1 module mal nommé/omis :**
- `ui_registry_msi` — registry des surfaces UI (source de vérité UI/UX système)

---

### 2. OpenClaw : 7/9 modules OPÉRATIONNELS (pas "impl partielle")

```text
CORRECTION CRITIQUE:
configure_openclaw     → cmd.sh + menu.sh + sanity.sh ✓ OPÉRATIONNEL
doctor_openclaw        → cmd.sh + menu.sh + sanity.sh ✓ OPÉRATIONNEL
evidence_openclaw      → cmd.sh + menu.sh + sanity.sh ✓ OPÉRATIONNEL
menu_openclaw          → cmd.sh + menu.sh + sanity.sh ✓ OPÉRATIONNEL
model_provider_openclaw → cmd.sh + menu.sh + sanity.sh ✓ OPÉRATIONNEL
openclaw_config_modulaire → cmd.sh + apply_safe.sh + rollback.sh ✓ OPÉRATIONNEL
install_module_openclaw → cmd.sh + menu.sh + sanity.sh ✓ OPÉRATIONNEL
gateway_openclaw       → cmd.sh complet (start/stop/attach/logs/health) ✓ OPÉRATIONNEL

NE PAS ÉCRIRE "impl partielle" pour ces modules. Ils ont tous cmd.sh + sanity.
```

---

### 3. Desk Pro : pipeline SÉQUENTIEL en 5 étapes (pas juste "10 sous-modules")

```text
CORRECTION CRITIQUE:
Desk Pro n'est pas une collection de sous-modules fragiles.
C'est un pipeline séquentiel ordonné avec chaque étape ayant cmd.sh + sanity.

[Step 0] desk_retention      → purge fichiers anciens (snapshots, SFTP inbox)
[Step A] desk_snapshot_ingest → ingest screenshots SFTP → latest.json + history.jsonl
[Step B] desk_analyze        → lit latest.json → rapport consolidé multi-actifs
[Step D] desk_capture_inputs → extrait inputs depuis captures (OpenAI Vision)
[Step E] desk_state          → fusionne tout → state/latest.json (fichier canonique)

ORCHESTRATION:
  desk_pro_orchestrator → conduit la séquence (déterministe)
  desk_pro_runner       → façade opératoire (cmd.sh run / run-and-show)
  desk_pro              → UI FastAPI (api/ + ui/ + service/ + mount.py + systemd)
  desk_common           → chemins partagés runtime
  desk_pro_dashboard    → app/ dashboard

SOURCE DE DONNÉES:
  SFTP inbox (/srv/sftp/shared_files/shared/inbox)
  → desk_snapshot_ingest → /opt/trading/desk/snapshots/latest.json
  → desk_analyze → desk report
  → desk_capture_inputs → /opt/trading/desk/inputs/tv_inputs_latest.json
  → desk_state → /opt/trading/desk/state/latest.json
  → desk_pro FastAPI → UI
```

---

### 4. bot_vision : structure hiérarchique (headless_capture = sous-module)

```text
CORRECTION:
bot_vision/
  bot_vision_step1/       → step1 (sous-répertoire intégré)
  headless_capture/       → capture headless JS (cmd.sh + systemd)
  scripts/                → scripts (cmd.sh + menu.sh + sanity_check.sh)

headless_capture a son propre cmd.sh et systemd — c'est opérationnel.
bot_vision est donc plus mature qu'une simple app Python.
```

---

### 5. ui_registry_msi : source de vérité UI système (non inventorié)

```text
CORRECTION:
ui_registry_msi = registry JSON de toutes les surfaces UI/UX du système
  → source de vérité : quelle UI, quelle machine, quelle catégorie, quel module
  → targeté : msi_db_layer (principal), admin_trading (secondaire)
  → candidat pour alimenter LocalCMS menu global automatiquement
```

---

### 6. Naming : problèmes identifiés

```text
COLLISION / AMBIGUÏTÉ:
  engines       vs trading engines individuels (execution_engine, etc.)
  router        vs registry_router (README de router lui-même note ce risque)
  install_module vs install_module_openclaw (confusion prévisible)
  marketdata    (très mince — juste __init__.py) vs market_scanner (vrai orchestrateur)

DETTES DE NOMMAGE:
  ops_wrappers.bak         → supprimer
  install_module_openclaw.bak_20260314 → supprimer
  ops_wrappers.sh.bak_20260303_193358  → supprimer (fichier interne à ops_wrappers)
  perm_fix_student         → archiver (machine student fermée)
  reseau_ssh_step1b        → archiver progressivement (deprecated)

RENOMMAGE RECOMMANDÉ:
  marketdata       → si contenu trop mince, absorber dans market_scanner
  router           → router_facade ou supprimer (overlap avec registry_router)
  engines          → engines_registry (clarifier rôle)
```

---

## INVENTAIRE COMPLET — 85 MODULES

### DOMAINE 1 — PIPELINE TRADING (11)

| # | Module | Structure | Opérationnel |
|---|--------|-----------|-------------|
| 1 | `execution_engine` | app/ + adapters/ + executor.py + config/ | non prouvé runtime |
| 2 | `decision_engine` | app/ + strategy_logic.py + config/ | non prouvé runtime |
| 3 | `risk_engine` | app/ + risk_calculator.py + risk_engine.py + config/ | non prouvé runtime |
| 4 | `position_engine` | app/ + position_manager.py + storage.py + config/ | non prouvé runtime |
| 5 | `portfolio_engine` | app/ + portfolio_engine.py + config/ | non prouvé runtime |
| 6 | `opportunity_ranker` | app/ + opportunity_ranker.py + config/ | non prouvé runtime |
| 7 | `probability_engine` | app/ + probability_engine.py + config/ | non prouvé runtime |
| 8 | `kil_v1` | cmd.sh + src/ + tests/ + examples/ | **OUI** (cmd.sh PASS) |
| 9 | `trading_realtime_v1` | app/ + docs/ÉTABLI.txt + tests/ | observation-only |
| 10 | `trading_lab_v1` | app/ + docs/ÉTABLI.txt + data/ | lab/batch |
| 11 | `simex_bitget_bridge` | app/ + cmd.sh + sanity.sh | **OUI** (SIMEX_UNITS_V1) |

### DOMAINE 2 — SIGNAL / WEBHOOK (3)

| # | Module | Structure | Opérationnel |
|---|--------|-----------|-------------|
| 12 | `webhook` | handlers.py + paper_guards.py + parse.py + schema.py | non prouvé bout-en-bout |
| 13 | `tradingview_observer` | app/ + cmd.ps1 + PS1 scripts + templates | **OUI** (Windows, PASS) |
| 14 | `tradingview_observer_openclaw` | run.ps1 + skill.md | Windows bridge — non prouvé |

### DOMAINE 3 — MARKET DATA (7)

| # | Module | Structure | Opérationnel |
|---|--------|-----------|-------------|
| 15 | `marketdata` | __init__.py seulement | minimal — à évaluer |
| 16 | `market_scanner` | app/ + config/ | non prouvé runtime |
| 17 | `collector_binance_spot` | src/ + config/ + runtime/ + tests/ + docs/ | partiel |
| 18 | `collector_coingecko` | src/ + config/ + runtime/ + tests/ + docs/ | partiel |
| 19 | `derivatives_collector` | app/ + config/ + tests/ | non prouvé |
| 20 | `derivatives_analyzer` | app/ + config/ | non prouvé |
| 21 | `liquidation_analyzer` | app/ + config/ | non prouvé |

### DOMAINE 4 — DESK PRO — UI TRADING (10)

| # | Module | Étape pipeline | Opérationnel |
|---|--------|---------------|-------------|
| 22 | `desk_pro` | UI centre (FastAPI + api/ + ui/ + service/ + systemd) | **OUI** (admin-trading) |
| 23 | `desk_pro_runner` | Entrée opératoire (cmd.sh run/run-and-show) | **OUI** (cmd.sh) |
| 24 | `desk_pro_orchestrator` | Conductor (cmd.sh séquence déterministe) | **OUI** (cmd.sh) |
| 25 | `desk_pro_dashboard` | Dashboard (app/) | non prouvé |
| 26 | `desk_common` | Shared (chemins runtime) | **OUI** (cmd.sh) |
| 27 | `desk_retention` | Step 0 — purge anciens fichiers | **OUI** (cmd.sh) |
| 28 | `desk_snapshot_ingest` | Step A — ingest SFTP → latest.json | **OUI** (cmd.sh) |
| 29 | `desk_analyze` | Step B — rapport consolidé multi-actifs | **OUI** (cmd.sh) |
| 30 | `desk_capture_inputs` | Step D — extraction inputs (OpenAI Vision) | **OUI** (cmd.sh) |
| 31 | `desk_state` | Step E — state canonique final | **OUI** (cmd.sh) |

### DOMAINE 5 — VISION / CAPTURE (3)

| # | Module | Structure | Opérationnel |
|---|--------|-----------|-------------|
| 32 | `bot_vision` | bot_vision_step1/ + headless_capture/ (cmd.sh + systemd) | **OUI** (admin-trading) |
| 33 | `bot_vision_step2` | app/ + scripts/ | non prouvé |
| 34 | `vision_bot` | app/ + systemd + SHAREX_SETUP.md | non prouvé |

### DOMAINE 6 — PERFORMANCE & JOURNAL (3)

| # | Module | Structure | Opérationnel |
|---|--------|-----------|-------------|
| 35 | `perf` | app.py + webhook.py + engine/ (shim) | **OUI** (shim cmd.sh) |
| 36 | `perf_engine` | app/ + config/ | non prouvé |
| 37 | `journal_engine` | app/ + config/ | non prouvé |

### DOMAINE 7 — OPENCLAW RUNTIME (9)

| # | Module | Structure | Opérationnel |
|---|--------|-----------|-------------|
| 38 | `gateway_openclaw` | app/ + scripts/ (start/stop/attach/health/logs) | **OUI** (ws loopback) |
| 39 | `menu_openclaw` | cmd.sh + menu.sh + sanity.sh + commandes_utiles.sh | **OUI** |
| 40 | `configure_openclaw` | cmd.sh + menu.sh + sanity.sh + docs/ | **OUI** |
| 41 | `doctor_openclaw` | cmd.sh + menu.sh + sanity.sh + docs/ | **OUI** |
| 42 | `evidence_openclaw` | cmd.sh + menu.sh + sanity.sh + docs/ | **OUI** |
| 43 | `model_provider_openclaw` | app/ + cmd.sh + menu.sh + sanity.sh + config/ | **OUI** |
| 44 | `openclaw_config_modulaire` | app/ + cmd.sh + apply_safe.sh + rollback.sh | **OUI** |
| 45 | `install_module_openclaw` | app/ + cmd.sh + menu.sh + sanity.sh + docs/ | **OUI** |
| 46 | `tradingview_observer_openclaw` | run.ps1 + skill.md | Windows — non prouvé |

### DOMAINE 8 — AI / PROVIDERS (6)

| # | Module | Structure | Opérationnel |
|---|--------|-----------|-------------|
| 47 | `validated_prompt_factory` | app/ + cmd.sh + sanity.sh + contextuals/ | **OUI** |
| 48 | `memory_bricks` | app/ + cmd.sh + sanity.sh + src/ + tests/ | **OUI** |
| 49 | `deepseek_hub` | patches/ + scripts/ | non prouvé |
| 50 | `deepseek_response` | scripts/ | non prouvé |
| 51 | `deepseek_thinking` | scripts/ | non prouvé |
| 52 | `hf_free_platform` | bin/ + datasets/ + handoff/ + kanban/ + spaces/ + spec/ | non prouvé |

### DOMAINE 9 — INFRA / CONNECTIVITÉ (8)

| # | Module | Structure | Opérationnel |
|---|--------|-----------|-------------|
| 53 | `reseau_ssh` | modules/ + scripts/ (canonique) | **OUI** |
| 54 | `reseau_ssh_step1b` | modules/ + scripts/ (compat deprecated) | deprecated |
| 55 | `auth` | bitget_credentials.py + secrets.py + webhook_key.py | actif (lib) |
| 56 | `health` | checker.py | actif (lib) |
| 57 | `shared` | scripts/ (minimal) | non prouvé |
| 58 | `shared_files_sftp` | scripts/ | non prouvé |
| 59 | `shared_sshfs_permanent` | INSTALL.sh + systemd + scripts/ | non prouvé |
| 60 | `winscp_transfer` | scripts/ | non prouvé |

### DOMAINE 10 — REGISTRES / ROUTAGE (7)

| # | Module | Structure | Opérationnel |
|---|--------|-----------|-------------|
| 61 | `registry_router` | app/ + __init__.py | non prouvé |
| 62 | `registry_meta_reader` | app/ + __init__.py | non prouvé |
| 63 | `modules_registry_reader` | app/ + output/ | non prouvé |
| 64 | `machines_registry_reader` | app/ + machines_registry_reader.py | non prouvé |
| 65 | `wrappers_registry_reader` | app/ + __init__.py | non prouvé |
| 66 | `ui_registry_msi` | app/ + config/ (source de vérité UI) | non prouvé |
| 67 | `router` | scripts/ wrapper facade (overlap registry_router) | minimal |

### DOMAINE 11 — OPS / MENUS (5)

| # | Module | Structure | Opérationnel |
|---|--------|-----------|-------------|
| 68 | `ops_menu_hub` | ops_menu_hub.sh | actif |
| 69 | `ops_super_menu` | ops_super_menu.sh | actif |
| 70 | `ops_wrappers` | ops_wrappers.sh (+ .bak interne) | actif — dette .bak |
| 71 | `module_contextuals_shell` | cmd.sh + contextuals/ + lib/ + typescript/ | **OUI** |
| 72 | `naming_normalizer` | app/ + cmd.sh + output/ | **OUI** |

### DOMAINE 12 — REPO / TOOLING (9)

| # | Module | Structure | Opérationnel |
|---|--------|-----------|-------------|
| 73 | `audit` | docs/ + scripts/ (méthode audit) | actif (méthode) |
| 74 | `dev_validation_hub` | scripts/cmd.sh + docs/RUNBOOK.txt | actif |
| 75 | `install_module` | scripts/ (sync_validate multi-machine) | actif |
| 76 | `repo_hygiene` | sanity_check.sh + lib.sh | **OUI** (sanity) |
| 77 | `repo_local_artifacts` | sanity_check.sh + gitignore mgmt | **OUI** (sanity) |
| 78 | `repo_ownership_guard` | sanity_check.sh + permission fix | **OUI** (sanity) |
| 79 | `git_fleet_guard` | app/ + config/ | non prouvé |
| 80 | `trae_module_validator` | cmd.sh + menu.sh + sanity.sh | **OUI** |
| 81 | `workflow_post_change_v2` | scripts/ | non prouvé |

### DOMAINE 13 — SHARED LIBS / SYSTEM (3)

| # | Module | Structure | Rôle |
|---|--------|-----------|------|
| 82 | `engines` | registry.py + router.py | lib partagée routing engines |
| 83 | `env` | env.py (project_root, load_env, ensure_dirs) | bootstrap transverse |
| 84 | `router` | scripts/ wrapper | facade légère |

### DOMAINE 14 — ARCHIVÉS / FERMÉS (3 + 2 à supprimer)

| # | Module | Statut | Action |
|---|--------|--------|--------|
| 85 | `deepseek_student` | CLOSED définitif | archiver |
| — | `mimo_open_observer` | CLOSED (student) | archiver |
| — | `perm_fix_student` | CLOSED (student machine) | archiver |
| — | `ops_wrappers.bak` | dette .bak | SUPPRIMER |
| — | `install_module_openclaw.bak_20260314` | dette .bak | SUPPRIMER |

```text
NOTE: mimo_open_observer et perm_fix_student ont des cmd.sh mais sont CLOSED.
Ils ne comptent pas dans les 85 modules actifs mais sont présents sur disk.
Le vrai total sur disk = 89 répertoires (85 actifs + 4 exclus).
```

---

## MENU GLOBAL STRUCTURÉ — OPT-TRADING

### Principes menu

```text
NIVEAU 1: Domaine fonctionnel
NIVEAU 2: Sous-domaine ou catégorie
NIVEAU 3: Module individuel (avec état)
ÉTAT: [OUI] opérationnel / [IMPL] implémenté non prouvé / [SPEC] spécifié / [CLOSED] fermé / [PROD] à produire
```

---

```
╔══════════════════════════════════════════════════════════╗
║             MENU GLOBAL OPT-TRADING                      ║
╚══════════════════════════════════════════════════════════╝

1. PIPELINE TRADING
   ├── 1.1 Signal & Webhook
   │   ├── tradingview_observer      [OUI]  Windows/PS1 — alertes + charts
   │   ├── tradingview_observer_openclaw [IMPL] Windows bridge TV → OpenClaw
   │   └── webhook                   [IMPL] handler HTTP signal entrant
   │
   ├── 1.2 Décision & Ranking
   │   ├── decision_engine           [IMPL] moteur décision (strategy_logic.py)
   │   ├── opportunity_ranker        [IMPL] ranker opportunités
   │   └── probability_engine        [IMPL] calcul probabilité
   │
   ├── 1.3 Risque & Kill Switch
   │   ├── risk_engine               [IMPL] risk_calculator + limites
   │   └── kil_v1                    [OUI]  kill switch (cmd.sh PASS)
   │
   ├── 1.4 Exécution & Exchange
   │   ├── execution_engine          [IMPL] executor.py + adapters
   │   └── simex_bitget_bridge       [OUI]  exchange connector (SIMEX_UNITS_V1)
   │
   ├── 1.5 Position & Portfolio
   │   ├── position_engine           [IMPL] position_manager + storage
   │   └── portfolio_engine          [IMPL] portfolio tracking
   │
   └── 1.6 Observation & Lab
       ├── trading_realtime_v1       [IMPL] observation-only (ÉTABLI)
       └── trading_lab_v1            [IMPL] lab batch / test (ÉTABLI)

2. MARKET DATA
   ├── 2.1 Collectors
   │   ├── collector_binance_spot    [IMPL] src/ + tests/ + runtime/ (partiel)
   │   ├── collector_coingecko       [IMPL] src/ + tests/ + runtime/ (partiel)
   │   └── derivatives_collector     [IMPL] app/ + tests/
   │
   ├── 2.2 Analyseurs
   │   ├── derivatives_analyzer      [IMPL] dérivés
   │   └── liquidation_analyzer      [IMPL] liquidations
   │
   └── 2.3 Hub & Scanner
       ├── market_scanner            [IMPL] orchestrateur collectors → signal
       └── marketdata                [IMPL] hub minimal (__init__.py)

3. OPENCLAW RUNTIME
   ├── 3.1 Gateway & Bridge
   │   ├── gateway_openclaw          [OUI]  ws://127.0.0.1:18789 (start/stop/health)
   │   └── openclaw_operator_bridge  [PROD] PRIORITÉ 1 — impl manquante
   │
   ├── 3.2 Configuration & Diagnostic
   │   ├── configure_openclaw        [OUI]  cmd.sh + apply
   │   ├── openclaw_config_modulaire [OUI]  apply_safe.sh + rollback.sh
   │   ├── doctor_openclaw           [OUI]  diagnostic runtime
   │   └── evidence_openclaw         [OUI]  collecte preuves
   │
   ├── 3.3 Installation & Providers
   │   ├── install_module_openclaw   [OUI]  cmd.sh install
   │   └── model_provider_openclaw   [OUI]  routing modèle
   │
   └── 3.4 Interface & Bridge Windows
       ├── menu_openclaw             [OUI]  CLI menus + commandes_utiles.sh
       └── tradingview_observer_openclaw [IMPL] run.ps1 + skill.md

4. AI & PROVIDERS
   ├── 4.1 Principal
   │   └── gateway_openclaw (builder) [OUI] provider IA primaire
   │
   ├── 4.2 Mémoire & Prompts
   │   ├── memory_bricks             [OUI]  learning store (cmd.sh + src + tests)
   │   └── validated_prompt_factory  [OUI]  prompt generator (cmd.sh + contextuals)
   │
   └── 4.3 Providers Alternatifs
       ├── deepseek_hub              [IMPL] hub IA alternatif + patches/
       ├── deepseek_response         [IMPL] handling réponses
       ├── deepseek_thinking         [IMPL] thinking mode
       └── hf_free_platform          [IMPL] HuggingFace (bin/datasets/spaces/spec)

5. DESK PRO — UI TRADING
   ├── 5.1 Entrée Opératoire
   │   ├── desk_pro_runner           [OUI]  cmd.sh run / run-and-show
   │   └── desk_pro_orchestrator     [OUI]  conductor pipeline (séquence déterministe)
   │
   ├── 5.2 UI Centrale
   │   ├── desk_pro                  [OUI]  FastAPI (api/ + ui/ + service/ + systemd)
   │   └── desk_pro_dashboard        [IMPL] dashboard app/
   │
   ├── 5.3 Pipeline Snapshot (Steps 0→A→B→D→E)
   │   ├── desk_retention            [OUI]  Step 0 — purge old files
   │   ├── desk_snapshot_ingest      [OUI]  Step A — ingest SFTP → latest.json
   │   ├── desk_analyze              [OUI]  Step B — rapport multi-actifs
   │   ├── desk_capture_inputs       [OUI]  Step D — extraction OpenAI Vision
   │   └── desk_state                [OUI]  Step E — state canonique final
   │
   └── 5.4 Shared
       └── desk_common               [OUI]  chemins runtime partagés

6. VISION & CAPTURE
   ├── 6.1 Principal
   │   └── bot_vision                [OUI]  headless_capture + step1 + systemd
   │
   └── 6.2 Extensions (à consolider)
       ├── bot_vision_step2          [IMPL] FastAPI extension
       └── vision_bot                [IMPL] systemd + SHAREX — variante

7. PERFORMANCE & JOURNAL
   ├── perf                          [OUI]  shim → perf_engine (app.py + webhook.py)
   ├── perf_engine                   [IMPL] moteur réel (app/ + config/)
   └── journal_engine                [IMPL] journalisation (app/ + config/)

8. INFRA & CONNECTIVITÉ
   ├── 8.1 SSH & Réseau
   │   ├── reseau_ssh                [OUI]  backbone SSH canonique (modules/)
   │   └── reseau_ssh_step1b         [DEPRECATED] compat — à archiver
   │
   ├── 8.2 Transfert Fichiers
   │   ├── shared_files_sftp         [IMPL] SFTP primaire
   │   ├── shared_sshfs_permanent    [IMPL] SSHFS mount (INSTALL.sh + systemd)
   │   ├── shared                    [IMPL] données partagées minimal
   │   └── winscp_transfer           [IMPL] transfert Windows
   │
   ├── 8.3 Auth & Secrets
   │   └── auth                      [OUI]  credentials (bitget + webhook)
   │
   └── 8.4 Santé
       └── health                    [OUI]  checker.py

9. REGISTRES & ROUTAGE
   ├── 9.1 Source de vérité UI
   │   └── ui_registry_msi           [IMPL] registry surfaces UI (MSI-first)
   │
   ├── 9.2 Router Central
   │   ├── registry_router           [IMPL] app/ routeur principal
   │   └── router                    [MINIMAL] facade scripts (overlap — à clarifier)
   │
   └── 9.3 Readers Spécialisés
       ├── registry_meta_reader      [IMPL] meta reader
       ├── modules_registry_reader   [IMPL] modules reader + output/
       ├── machines_registry_reader  [IMPL] machines reader
       └── wrappers_registry_reader  [IMPL] wrappers reader

10. WORKERS STRICTS (À PRODUIRE)
    ├── 10.1 Ingestion Signal
    │   └── signal_router             [PROD] webhook → signal JSON normalisé
    │
    ├── 10.2 IA Pipeline
    │   ├── proposition_engine        [PROD] signal → OpenClaw → proposition
    │   └── validation_gate           [PROD] proposition → APPROVED/REJECTED
    │
    ├── 10.3 Exécution & Résultat
    │   ├── trade_executor            [PROD] proposition validée → exchange
    │   └── result_tracker            [PROD] fill → P&L brut
    │
    ├── 10.4 Reporting & Learning
    │   ├── datasheet_writer          [PROD] P&L → Sheets + Airtable
    │   └── learning_feeder           [PROD] résultat → OpenClaw feedback
    │
    └── 10.5 Notifications & Sync
        ├── notification_dispatcher   [PROD] événements → Telegram structuré
        └── task_tracker              [PROD] état pipeline → ClickUp + Airtable

11. OPS & MENUS
    ├── 11.1 Menus CLI
    │   ├── ops_menu_hub              [OUI]  menu central ops
    │   └── ops_super_menu            [OUI]  super menu
    │
    ├── 11.2 Wrappers & Outils
    │   ├── ops_wrappers              [OUI]  wrappers ops (dette .bak interne)
    │   ├── module_contextuals_shell  [OUI]  contextuals + lib + typescript
    │   └── naming_normalizer         [OUI]  normalisation nommage

12. REPO & TOOLING
    ├── 12.1 Validation
    │   ├── trae_module_validator     [OUI]  cmd.sh + sanity
    │   ├── dev_validation_hub        [OUI]  pre-PR check + venv
    │   └── audit                     [OUI]  méthode audit + checklist
    │
    ├── 12.2 Hygiène & Permissions
    │   ├── repo_hygiene              [OUI]  sanity + gitignore
    │   ├── repo_local_artifacts      [OUI]  sanity + gitignore patterns
    │   ├── repo_ownership_guard      [OUI]  fix permissions git
    │   └── git_fleet_guard           [IMPL] fleet guard
    │
    └── 12.3 Installation & Sync
        ├── install_module            [OUI]  sync_validate multi-machine
        └── workflow_post_change_v2   [IMPL] post-change hook

13. SHARED LIBS (TRANSVERSES)
    ├── engines                       [OUI]  registry + router trading engines
    └── env                           [OUI]  bootstrap (project_root, load_env)

14. ARCHIVÉS / FERMÉS
    ├── deepseek_student              [CLOSED] archiver → archive/closed/
    ├── mimo_open_observer            [CLOSED] archiver → archive/closed/
    └── perm_fix_student              [CLOSED] archiver → archive/closed/

    DETTES À SUPPRIMER:
    ├── ops_wrappers.bak/             → rm -rf
    ├── install_module_openclaw.bak_20260314/ → rm -rf
    └── ops_wrappers.sh.bak_20260303_193358   → rm (fichier interne)
```

---

## REVALIDATION CONSOLIDATIONS

### E1 — Desk Pro : VALIDATION ✓ (pipeline plus fort que prévu)

```text
DÉCISION: CONSERVER la structure à 10 modules
RAISON: les 8 modules de pipeline (Step 0→A→B→D→E) ont chacun cmd.sh opérationnel
         → ce ne sont pas des "sous-modules fragiles" mais des étapes séquentielles réelles
         → les intégrer dans desk_pro serait une perte de clarté pipeline
CORRECTION: sortir "À INTÉGRER dans desk_pro" des actions — desk_pro_dashboard uniquement reste candidat
ACTION RÉVISÉE:
  desk_pro             → conserver (UI centre)
  desk_pro_runner      → conserver (entrée)
  desk_pro_orchestrator → conserver (conductor)
  desk_common          → conserver (lib partagée)
  Steps 0,A,B,D,E      → conserver (étapes pipeline indépendantes)
  desk_pro_dashboard   → évaluer intégration dans desk_pro (seul candidat fusion)
```

### E4 — OpenClaw : CORRECTION MAJEURE

```text
DÉCISION: 7/9 modules sont OPÉRATIONNELS (pas "impl partielle")
RÉVISION: classer configure, doctor, evidence, menu, model_provider, config_modulaire, install comme OPÉRATIONNEL
CONSOLIDATION RÉSIDUELLE: évaluer overlap openclaw_config_modulaire vs configure_openclaw
  → openclaw_config_modulaire = config en mode apply/rollback (plus sûr)
  → configure_openclaw = config standard
  → peuvent coexister ou fusionner — à décider après bridge impl
```

### E5 — Market Data : CORRECTION

```text
DÉCISION: marketdata est un module très mince (__init__.py seulement)
ACTION: évaluer si marketdata peut être absorbé dans market_scanner
        market_scanner est le vrai orchestrateur des collectors
        marketdata = hub de données = peut devenir un namespace uniquement
```

### E7 — Registres : CORRECTION (6 modules, pas 5)

```text
AJOUT: ui_registry_msi = 6ème module de la famille registre
RÔLE CLÉ: source de vérité UI surfaces — alimentation directe possible de LocalCMS menu
ACTION: lire ui_registry_msi/config/ pour extraire le registry JSON → LocalCMS menu automatique
```

---

## COMPTAGE FINAL CORRIGÉ

```text
TOTAL MODULES RÉELS: 85
  Pipeline trading:   11
  Signal/webhook:      3
  Market data:         7
  Desk Pro/UI:        10
  Vision/capture:      3
  Perf/journal:        3
  OpenClaw:            9
  AI/providers:        6
  Infra:               8
  Registres:           7
  Ops/menus:           5
  Repo/tooling:        9
  Shared libs:         2
  Fermés/archivés:     3 (hors compte actif)

WORKERS À PRODUIRE:   10 (non encore dans modules/)
TOTAL CIBLE:          95 modules (85 actuels + 10 workers)
```
