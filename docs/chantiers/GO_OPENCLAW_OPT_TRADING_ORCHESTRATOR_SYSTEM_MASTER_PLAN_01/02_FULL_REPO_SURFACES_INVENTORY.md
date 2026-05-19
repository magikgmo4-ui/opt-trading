---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01_FULL_INVENTORY
doc_type: inventory
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
status: open
updated_at: 2026-05-14
---

# 02_FULL_REPO_SURFACES_INVENTORY

## Objet

Inventaire complet de toutes les surfaces du repo `opt-trading`.
L'audit `01_AUDIT_SURFACES_AND_STATE.md` couvrait uniquement le domaine OpenClaw/orchestration.
Ce document complète le scope manquant et valide la couverture dans le plan d'orchestration.

---

## GAP CRITIQUE — CE QUI MANQUAIT DANS L'AUDIT INITIAL

```text
MANQUANT:
1. Pipeline trading (execution, decision, risk, position, portfolio, kil, etc.)
2. Market data (collectors, derivatives, liquidation, marketdata, scanner)
3. Desk Pro / UI observation (desk_pro, bot_vision, journal_engine, perf)
4. Strict workers (GO déjà ouvert, DRAFT_ONLY, smoke PASS)
5. DB-layer ingestion architecture (5 governance docs)
6. Multi-agents matrix complète (02_AGENT_SKILL_PROVIDER_MATRIX.md)
7. Product targets (OPENCLAW_TARGET_CANON, DEEPSEEK, STUDENT)
8. Infra connectivity étendue (simex_bitget_bridge, auth, health, registry)
```

---

## DOMAINE 1 — PIPELINE TRADING (EXECUTION)

| Module | Impl | Opérationnel | Dans plan orchestration |
| --- | --- | --- | --- |
| `execution_engine` | app/, adapters/, executor.py | ? (non prouvé) | ✓ trade_executor |
| `decision_engine` | app/, config/, scripts/ | ? | ✓ proposition_engine (overlap) |
| `risk_engine` | app/, config/, scripts/ | ? | ✓ validation_gate (risk limits) |
| `position_engine` | app/, config/ | ? | ✓ result_tracker |
| `portfolio_engine` | app/, config/ | ? | ✓ result_tracker |
| `opportunity_ranker` | app/, config/ | ? | ✓ proposition_engine (amont) |
| `probability_engine` | app/, config/ | ? | ✓ proposition_engine |
| `kil_v1` | cmd.sh, menu.sh, examples/ | **IMPL** (cmd.sh) | ✓ validation_gate kill switch |
| `trading_realtime_v1` | app/ | ? | ✓ trade_executor aval |
| `trading_lab_v1` | app/ | ? | ✓ smoke/test |
| `simex_bitget_bridge` | cmd.sh, sanity.sh, app/ | **IMPL** | ✓ trade_executor → exchange |

**Note critique :** `kil_v1` et `simex_bitget_bridge` ont des `cmd.sh` et `sanity.sh` — impl réelle.
Les moteurs core (execution, decision, risk) ont une structure mais leur état opérationnel n'est pas prouvé dans ce scan.

**Gap plan orchestration :**
```text
Le plan maître nomme des workers (proposition_engine, trade_executor, validation_gate, result_tracker)
MAIS ces workers sont à créer DESSUS les moteurs existants — pas à la place.
Architecture réelle :
  signal_router → decision_engine/opportunity_ranker → proposition_engine (worker)
  validation_gate (worker) → kil_v1 check → execution_engine → simex_bitget_bridge
  result_tracker (worker) → position_engine/portfolio_engine
```

---

## DOMAINE 2 — MARKET DATA

| Module | Impl | Opérationnel | Dans plan orchestration |
| --- | --- | --- | --- |
| `collector_binance_spot` | app/ | ? | ✓ source données signal |
| `collector_coingecko` | app/ | ? | ✓ source données enrichissement |
| `derivatives_analyzer` | app/ | ? | ✓ enrichissement signal |
| `derivatives_collector` | app/ | ? | ✓ collecte |
| `liquidation_analyzer` | app/ | ? | ✓ enrichissement signal |
| `marketdata` | app/ | ? | ✓ hub données |
| `market_scanner` | app/ | ? | ✓ amont signal_router |

**Gap plan orchestration :**
```text
signal_router reçoit un webhook TradingView MAIS le signal brut doit être enrichi
par market_scanner + marketdata avant d'atteindre proposition_engine.
Flux réel :
  TradingView webhook → signal_router → marketdata enrichissement → proposition_engine
```

---

## DOMAINE 3 — DESK PRO / OBSERVATION UI

| Module | Impl | Opérationnel | Dans plan orchestration |
| --- | --- | --- | --- |
| `desk_pro` | api/, scripts/, dry_run.py | **IMPL** (dry_run PASS admin-trading) | ✓ ui_renderer |
| `desk_pro_dashboard` | app/ | ? | ✓ ui dashboard |
| `desk_pro_orchestrator` | app/ | ? | ✓ orchestrateur desk |
| `desk_pro_runner` | app/ | ? | ✓ runner |
| `desk_state` | app/ | ? | ✓ état partagé |
| `desk_analyze` | app/ | ? | ✓ analyse |
| `desk_capture_inputs` | app/ | ? | ✓ capture |
| `desk_common` | app/ | ? | ✓ shared |
| `desk_retention` | app/ | ? | ✓ rétention |
| `desk_snapshot_ingest` | app/ | ? | ✓ ingestion snapshot |
| `bot_vision` | app/ | IMPL (smoke PASS admin-trading) | ✓ vision/screenshot |
| `bot_vision_step2` | app/ | ? | ✓ vision avancée |
| `vision_bot` | app/ | ? | ✓ vision alternative |
| `journal_engine` | app/ | ? | ✓ datasheet_writer amont |
| `perf` | app/ | ? | ✓ perf_tracker |
| `perf_engine` | app/ | ? | ✓ perf analyse |

**Gap plan orchestration :**
```text
desk_pro est un consumer UI de données réelles — il manque dans le plan maître.
Il lit les positions, le P&L, les snapshots.
Il n'est pas LocalCMS — c'est la surface UI trading réelle sur admin-trading.

Plan maître doit distinguer :
  desk_pro → UI trading réelle (admin-trading) 
  LocalCMS consumer → UI lecture générale (db-layer)
```

---

## DOMAINE 4 — AI / MODÈLES

| Module | Impl | Opérationnel | Dans plan orchestration |
| --- | --- | --- | --- |
| `deepseek_hub` | app/ | ? | ✓ provider alternatif |
| `deepseek_response` | app/ | ? | ✓ provider alternatif |
| `deepseek_student` | app/ | CLOSED (student surface fermée) | N/A |
| `deepseek_thinking` | app/ | ? | ✓ provider thinking mode |
| `hf_free_platform` | app/ | ? | ✓ provider HF gratuit |
| `memory_bricks` | cmd.sh, sanity.sh, app/ | **IMPL** | ✓ learning_feeder mémoire |
| `mimo_open_observer` | app/ | CLOSED (student) | Hors scope |
| `workflow_post_change_v2` | scripts/ | ? | ✓ post-change workflow |

**Gap plan orchestration :**
```text
memory_bricks est la couche mémoire persistante — elle doit être dans le plan learning.
Flux learning réel :
  result_tracker → learning_feeder → memory_bricks + OpenClaw builder
  (pas seulement OpenClaw — memory_bricks est le store persistant)

deepseek_hub/thinking = providers alternatifs à OpenClaw pour proposition_engine.
```

---

## DOMAINE 5 — STRICT WORKERS (DÉJÀ DOCUMENTÉ — HORS AUDIT INITIAL)

```text
GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
STATUT: DRAFT_ONLY, smoke READ_INVENTORY PASS
BRANCHE: origin/go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01 (KEEP_ACTIVE)
NON MERGÉ dans sot/mainline
```

Artéfacts existants :
- `docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md` — doctrine
- `docs/agents/strict_workers/MODELS_MATRIX_01.md` — matrice modèles
- `docs/agents/strict_workers/MODEL_ID_VALIDATION_01.md` — validation IDs
- `scripts/ai/workers/models.registry.json` — registry modèles (only_verified_models=true)
- `scripts/ai/workers/tasks.index.json` — index tâches
- `scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json` — job packet
- `scripts/ai/workers/run_task.sh` — runner

**Lien direct avec le plan maître :**
```text
Le plan maître définit les workers stricts (signal_router, proposition_engine, etc.)
MAIS le parent GO_OPT_TRADING_STRICT_WORKERS_PARENT_01 pose déjà :
  - le cadre d'autonomie étroite
  - le registry modèle
  - le task index
  - le runner
Ce parent DOIT être repris comme fondation des workers du plan maître.
Pas à recréer — à étendre.
```

---

## DOMAINE 6 — MULTI-AGENTS DOCTRINE (DÉJÀ DOCUMENTÉ)

```text
GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
STATUT: ACTIVE
```

Matrice agents/skills/providers établie (12 docs) :
- `02_AGENT_SKILL_PROVIDER_MATRIX.md` — matrice complète
- `10_CROSS_CHANTIERS_OPENCLAW_TMUX_AGENTS_REVIEW.md`
- `12_SESSION_REPRISE_GO_ORDER.md`

Agents recensés : Codex, Claude (code/claude), Trae, OpenClaw, Ollama (CLOSED)

**Lien plan maître :**
```text
Les workers du plan maître ne sont PAS des agents IA — ce sont des workers process.
La matrice multi-agents gouverne les agents IA qui ALIMENTENT les workers.
Architecture :
  agent (Claude/OpenClaw) → skill → worker → pipeline opt-trading
```

---

## DOMAINE 7 — DB-LAYER INGESTION (GOVERNANCE)

5 docs dans `docs/governance/` :
- `DB_LAYER_INGESTION_ENGINE_DECISION_01.md`
- `DB_LAYER_INGESTION_PHYSICAL_SCHEMA_DECISION_01.md`
- `DB_LAYER_INGESTION_RUNTIME_GATING_01.md`
- `DB_LAYER_INGESTION_SCHEMA_MAPPING_01.md`
- `DB_LAYER_SHARED_TO_DB_INGESTION_SPEC_01.md`

```text
Rôle : définit comment les données shared/SFTP sont ingérées dans db-layer.
Lien plan maître : result_tracker → datasheet_writer → DB ingestion pipeline
Non couvert dans le plan maître — GAP À COMBLER.
```

---

## DOMAINE 8 — PRODUCT TARGETS

| Fichier | Surface | Statut |
| --- | --- | --- |
| `OPENCLAW_TARGET_CANON.md` | OpenClaw cible produit | OPEN |
| `DEEPSEEK_OLLAMA_TARGET_CANON.md` | DeepSeek/Ollama cible | Partiel (Ollama CLOSED) |
| `STUDENT_TARGET_CANON.md` | Student cible | CLOSED_FINAL |
| `RUNTIME_TO_TARGET_MAPPING.md` | Mapping runtime → target | ÉTABLI |

---

## DOMAINE 9 — INFRA CONNECTIVITY

| Module | Rôle | Impl | Dans plan |
| --- | --- | --- | --- |
| `reseau_ssh` | SSH canonical | **OPÉRATIONNEL** | ✓ backbone multi-machine |
| `shared_files_sftp` | SFTP partage fichiers | Impl | ✓ data transfer |
| `shared_sshfs_permanent` | SSHFS permanent | Impl | ✓ data transfer |
| `auth` | Authentification | Impl | ✓ sécurité |
| `health` | Health checks | Impl | ✓ monitoring |
| `machines_registry_reader` | Registry machines | Impl | ✓ multi-machine routing |
| `router` / `registry_router` | Routing | Impl | ✓ dispatch |
| `git_fleet_guard` | Git fleet | Impl | Indirect |
| `trae_module_validator` | Validation Trae | Impl | ✓ validation modules |

---

## DOMAINE 10 — ACTIVE STREAMS (HORS AUDIT INITIAL)

| GO | Statut | Pertinence plan maître |
| --- | --- | --- |
| `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` | DRAFT_ONLY, non mergé | **DIRECTEMENT PERTINENT** — fondation workers |
| `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | ACTIVE | **DIRECTEMENT PERTINENT** — doctrine agents |
| `GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01` | ACTIVE | ✓ robustesse pipeline |
| `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` | P0 ACTIVE | **DIRECTEMENT PERTINENT** — tmux backbone |
| `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01` | Suite P0 | ✓ tmux impl |
| `GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01` | OPEN | ✓ task_tracker |
| `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` | OPEN | ✓ infra backbone |
| `GO_GIT_PROGRESSIVE_MIGRATION_START_13` | ACTIVE | Indirect |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | OPEN | ✓ architecture globale |

---

## VALIDATION COUVERTURE PLAN D'ORCHESTRATION — COMPLET

### Flux réel corrigé

```text
[SOURCE SIGNAL]
  TradingView webhook
  → market_scanner + collector_binance_spot/coingecko
  → signal_router (worker, à créer)
  → signal JSON enrichi

[PROPOSITION]
  signal JSON
  → opportunity_ranker / probability_engine / decision_engine (moteurs existants)
  → proposition_engine (worker, à créer, appelle OpenClaw builder)
  → proposition JSON + confidence

[VALIDATION]
  proposition JSON
  → kil_v1 check (EXISTS cmd.sh)
  → risk_engine check (EXISTS)
  → validation_gate (worker, à créer)
  → Telegram approval si requis
  → APPROVED / REJECTED

[TRADE]
  APPROVED → trade_executor (worker, à créer)
  → simex_bitget_bridge (EXISTS cmd.sh)
  → execution_engine
  → trade_id + fill

[RÉSULTAT]
  fill → result_tracker (worker, à créer)
  → position_engine / portfolio_engine
  → P&L brut

[DATASHEET]
  P&L → datasheet_writer (worker, à créer)
  → journal_engine (EXISTS)
  → Sheets / Airtable
  → DB ingestion pipeline (governance docs existants)

[LEARNING]
  résultat + contexte → learning_feeder (worker, à créer)
  → memory_bricks (EXISTS cmd.sh)
  → OpenClaw builder feedback
```

### Surfaces manquantes ou mal positionnées dans plan maître

| Gap | Correction |
| --- | --- |
| desk_pro absent | Ajouter comme surface UI trading réelle (admin-trading) |
| memory_bricks absent | Ajouter comme store learning (distinct d'OpenClaw) |
| moteurs existants ignorés | Workers à créer DESSUS les moteurs, pas à la place |
| kil_v1 / simex_bitget_bridge ignorés | Déjà impl — workers les wrappent |
| DB ingestion pipeline ignoré | Datasheet_writer branche sur ce pipeline |
| strict_workers parent ignoré | Fondation à reprendre pour les workers à créer |
| Figma | Différer — pas dans le pipeline trade |

---

## SYNTHÈSE FINALE

```text
MODULES REPO: 78
MODULES AVEC CMD.SH/IMPL PROUVÉE: ~20
MODULES STATUT INCONNU: ~40 (structure présente, runtime non prouvé)
MODULES CLOSED/HORS SCOPE: ~8 (student/mimo/ollama surface)

SURFACES DANS PLAN ORCHESTRATION:
  COUVERTES: 100% après corrections ci-dessus
  GAPS RÉSIDUELS: desk_pro UI, memory_bricks learning, DB ingestion

PRIORITÉ ABSOLUE:
  1. Reprendre GO_OPT_TRADING_STRICT_WORKERS_PARENT_01 comme base workers
  2. Ouvrir GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_IMPL_V1_01
  3. Créer signal_router + notification_dispatcher
  4. Valider état opérationnel moteurs (execution, decision, risk, position)
     avant d'ouvrir proposition_engine
```
