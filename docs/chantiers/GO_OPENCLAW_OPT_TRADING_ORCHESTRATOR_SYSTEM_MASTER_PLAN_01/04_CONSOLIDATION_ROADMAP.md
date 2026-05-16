---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01_CONSOLIDATION
doc_type: roadmap
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
status: open
updated_at: 2026-05-16
---

# 04_CONSOLIDATION_ROADMAP

## Objet

Transformer les 10 familles fragmentées en produits/modules cohérents.
Chaque famille constitue un seul produit fonctionnel dispersé en plusieurs modules/versions.
Ce document définit la décision canonique, le point d'entrée unique, et les modules à archiver/réduire/fusionner.

---

## RÈGLE CONSOLIDATION

```text
1 PRODUIT = 1 POINT D'ENTRÉE CANONIQUE
Modules satellites : deprecated, archived, ou fusionnés dans le module central.
GO de consolidation ≠ réécriture — c'est un redirect + cleanup.
```

---

## E1 — DESK PRO (PRIORITÉ HAUTE)

### Situation actuelle

```text
10 modules pour 1 produit trading observation + décision.
3 modules avec cmd.sh opérationnel (desk_pro, desk_pro_runner, desk_pro_orchestrator).
7 modules partiellement implémentés (desk_analyze, desk_capture_inputs, desk_common,
  desk_retention, desk_snapshot_ingest, desk_state, desk_pro_dashboard).
```

### Décision

```text
PRODUIT CANONIQUE: Desk Pro — observation + décision + UI trading
POINT D'ENTRÉE: desk_pro_runner (cmd.sh run / run-and-show)
CONDUCTOR: desk_pro_orchestrator (séquence pipeline déterministe)
CENTRE UI: desk_pro (FastAPI + HTML → admin-trading)
```

### Action par module

| Module | Action | Cible |
| --- | --- | --- |
| `desk_pro` | CONSERVER — centre UI | centre de gravité |
| `desk_pro_runner` | CONSERVER — entrée opératoire | cmd.sh canonique |
| `desk_pro_orchestrator` | CONSERVER — conductor | séquence déterministe |
| `desk_pro_dashboard` | INTÉGRER dans desk_pro | dashboard → mount desk_pro |
| `desk_analyze` | INTÉGRER dans desk_pro | analyse → module interne |
| `desk_capture_inputs` | INTÉGRER dans desk_pro | capture → module interne |
| `desk_common` | CONSERVER comme lib partagée | desk_pro/shared/ |
| `desk_retention` | INTÉGRER dans desk_pro | rétention → module interne |
| `desk_snapshot_ingest` | INTÉGRER dans desk_pro | ingest → module interne |
| `desk_state` | INTÉGRER dans desk_pro | state → module interne |

### GO requis

```text
GO_OPT_TRADING_DESK_PRO_CONSOLIDATION_01
SCOPE: valider opérationnel desk_pro_runner → desk_pro → dashboard
BLOQUANT: non (parallèle au bridge)
PRÉREQ: aucun
```

---

## E2 — PERF / PERF_ENGINE (PRIORITÉ MOYENNE)

### Situation actuelle

```text
perf = shim de migration (app.py → perf/perf_app.py, engine/ → perf_engine)
perf_engine = moteur réel avec tracking ideas paper, scripts/cmd.sh
Migration en cours — perf est un wrapper temporaire
```

### Décision

```text
PRODUIT CANONIQUE: perf_engine (moteur réel)
POINT D'ENTRÉE: perf_engine/scripts/cmd.sh (cible finale)
TRANSITION: perf/scripts/cmd.sh jusqu'à migration complète
UI: perf_app.py → intégrée dans Desk Pro via mount
```

### Action par module

| Module | Action | Cible |
| --- | --- | --- |
| `perf` | DEPRECATED progressif — shim temporaire | redirect vers perf_engine |
| `perf_engine` | CANONIQUE — moteur réel | target finale |

### GO requis

```text
GO_OPT_TRADING_PERF_ENGINE_MIGRATION_01
SCOPE: compléter migration perf shim → perf_engine ; valider cmd.sh perf_engine
BLOQUANT: non
PRÉREQ: desk_pro consolidation (perf monté dans desk_pro)
```

---

## E3 — VISION / BOT (PRIORITÉ MOYENNE)

### Situation actuelle

```text
bot_vision     → impl principale, smoke PASS admin-trading (OPÉRATIONNEL)
bot_vision_step2 → FastAPI, app/, statut inconnu
vision_bot     → variante alternative, statut inconnu
```

### Décision

```text
PRODUIT CANONIQUE: bot_vision
POINT D'ENTRÉE: bot_vision/app/ (direct)
ARCHIVER: vision_bot (si doublon non prouvé utile)
ÉVALUER: bot_vision_step2 (garder si step2 apporte fonctionnalité réelle)
```

### Action par module

| Module | Action | Cible |
| --- | --- | --- |
| `bot_vision` | CONSERVER — module principal | opérationnel confirmé |
| `bot_vision_step2` | ÉVALUER — fonctionnalité step2 réelle ? | garder si delta prouvé, sinon archiver |
| `vision_bot` | ARCHIVER — doublon non prouvé | archive/vision_bot/ |

### GO requis

```text
GO_OPT_TRADING_BOT_VISION_CONSOLIDATION_01
SCOPE: smoke step2 + vision_bot, décider survie, archiver le cas échéant
BLOQUANT: non
PRÉREQ: aucun
```

---

## E4 — OPENCLAW RUNTIME (PRIORITÉ HAUTE)

### Situation actuelle

```text
8 modules pour 1 runtime IA (gateway + menus + config + doctor + evidence + install + provider + config_modulaire)
gateway_openclaw = OPÉRATIONNEL (ws://127.0.0.1:18789)
openclaw_operator_bridge = SPEC COMPLÈTE — IMPL MANQUANTE (PRIORITÉ 1 absolue)
```

### Décision

```text
PRODUIT CANONIQUE: OpenClaw runtime (gateway + bridge)
POINT D'ENTRÉE:
  runtime  → gateway_openclaw/cmd.sh (start/stop/health/attach)
  bridge   → openclaw_operator_bridge/ (à implémenter)
  menus    → menu_openclaw/scripts/
  config   → configure_openclaw/scripts/
DIAGNOSTIC: doctor_openclaw/scripts/
```

### Action par module

| Module | Action | Cible |
| --- | --- | --- |
| `gateway_openclaw` | CONSERVER — backbone opérationnel | runtime canonique |
| `openclaw_operator_bridge` | IMPLÉMENTER — PRIORITÉ 1 | modules/openclaw_operator_bridge/ |
| `menu_openclaw` | CONSERVER + documenter | menus CLI |
| `model_provider_openclaw` | CONSERVER + valider opérationnel | routing modèle |
| `configure_openclaw` | CONSERVER + documenter | config runtime |
| `doctor_openclaw` | CONSERVER + documenter | diagnostic |
| `evidence_openclaw` | CONSERVER + documenter | preuves runtime |
| `install_module_openclaw` | CONSERVER + documenter | install |
| `openclaw_config_modulaire` | ÉVALUER — overlap avec configure_openclaw ? | fusionner si doublon |
| `tradingview_observer_openclaw` | ÉVALUER — statut Windows | garder si TV bridge prouvé |

### GO requis

```text
GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_IMPL_V1_01   ← DÉBLOQUANT — ouvrir en premier
GO_OPENCLAW_OPT_TRADING_RUNTIME_CONSOLIDATION_01            ← consolider 8 modules → runtime cohérent
```

---

## E5 — MARKET DATA (PRIORITÉ HAUTE)

### Situation actuelle

```text
7 modules pour 1 pipeline marché (collecte → scan → enrichissement → signal)
collector_binance_spot = impl V1 minimal, PARTIEL opérationnel
6 autres = impl app/, statut inconnu
```

### Décision

```text
PRODUIT CANONIQUE: Market Data Pipeline
POINT D'ENTRÉE: market_scanner (orchestre les collectors)
FLUX CANONIQUE: collector_* → marketdata (hub) → market_scanner → derivatives/liquidation → signal_router
```

### Action par module

| Module | Action | Cible |
| --- | --- | --- |
| `marketdata` | CONSERVER — hub données | orchestrateur collectors |
| `market_scanner` | CONSERVER — entrée signal | feed → signal_router |
| `collector_binance_spot` | VALIDER runtime V1 | pipeline primaire |
| `collector_coingecko` | VALIDER runtime | enrichissement |
| `derivatives_collector` | VALIDER runtime | dérivés |
| `derivatives_analyzer` | VALIDER runtime | enrichissement signal |
| `liquidation_analyzer` | VALIDER runtime | enrichissement signal |

### GO requis

```text
GO_OPT_TRADING_MARKET_DATA_PIPELINE_SMOKE_01
SCOPE: smoke binance + coingecko → marketdata → scanner ; valider opérationnel
BLOQUANT: oui pour signal_router (signal_router dépend du marketdata enrichi)
PRÉREQ: aucun (indépendant du bridge)
```

---

## E6 — SSH / RÉSEAU (EN COURS)

### Situation actuelle

```text
GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 OUVERT
reseau_ssh = OPÉRATIONNEL (modules/reseau_ssh/scripts/)
reseau_ssh_step1b = compat à réduire
scripts/reseau_ssh = héritage à réduire
```

### Décision

```text
PRODUIT CANONIQUE: reseau_ssh (modules/)
POINT D'ENTRÉE: modules/reseau_ssh/scripts/
ARCHIVER: reseau_ssh_step1b + scripts/reseau_ssh héritage
```

### Action par module

| Module | Action | Cible |
| --- | --- | --- |
| `reseau_ssh` (modules/) | CONSERVER — canonique | backbone SSH |
| `reseau_ssh_step1b` | DEPRECATED — redirect → modules/ | archiver après compat prouvée |
| `scripts/reseau_ssh` | DEPRECATED — héritage | archiver |

### GO requis

```text
GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 (DÉJÀ OUVERT)
SCOPE: réduire step1b + héritage scripts
```

---

## E7 — REGISTRES / READERS (PRIORITÉ BASSE)

### Situation actuelle

```text
5 readers pour 1 surface registre (router, meta, modules, machines, wrappers)
Impl app/ présent — opérationnel inconnu
```

### Décision

```text
PRODUIT CANONIQUE: registry system
POINT D'ENTRÉE: registry_router (point central)
FUSION: registry_meta_reader + modules_registry_reader + machines_registry_reader → sous registry_router
```

### Action par module

| Module | Action | Cible |
| --- | --- | --- |
| `registry_router` | CONSERVER — point central | orchestrateur readers |
| `registry_meta_reader` | INTÉGRER sous registry_router | sous-module |
| `modules_registry_reader` | INTÉGRER sous registry_router | sous-module |
| `machines_registry_reader` | INTÉGRER sous registry_router | sous-module |
| `wrappers_registry_reader` | INTÉGRER sous registry_router | sous-module |

### GO requis

```text
GO_OPT_TRADING_REGISTRY_CONSOLIDATION_01
SCOPE: valider opérationnel ; fusionner 4 readers sous registry_router
PRIORITÉ: BASSE (non bloquant pipeline)
```

---

## E8 — DEEPSEEK (PRIORITÉ BASSE)

### Situation actuelle

```text
deepseek_hub, deepseek_response, deepseek_thinking = providers IA alternatifs
deepseek_student = CLOSED (surface student fermée)
mimo_open_observer = CLOSED (student)
```

### Décision

```text
PRODUIT CANONIQUE: deepseek_hub (hub provider IA alternatif)
ARCHIVER: deepseek_student + mimo_open_observer (CLOSED définitif)
CONSERVER: hub + response + thinking (providers pour proposition_engine)
```

### Action par module

| Module | Action | Cible |
| --- | --- | --- |
| `deepseek_hub` | CONSERVER — hub alternatif | provider proposition_engine |
| `deepseek_response` | CONSERVER — handling | sous deepseek_hub |
| `deepseek_thinking` | CONSERVER — thinking mode | sous deepseek_hub |
| `deepseek_student` | ARCHIVER — CLOSED | archive/closed/ |
| `mimo_open_observer` | ARCHIVER — CLOSED | archive/closed/ |

### GO requis

```text
GO_OPT_TRADING_DEEPSEEK_CLEANUP_01
SCOPE: archiver closed, valider hub opérationnel
PRIORITÉ: BASSE
```

---

## E9 — OPS MENUS (PRIORITÉ BASSE)

### Situation actuelle

```text
ops_menu_hub + ops_super_menu + ops_wrappers/ops_wrappers.bak
ops_wrappers.bak = dette technique explicite (.bak = non nettoyé)
```

### Décision

```text
PRODUIT CANONIQUE: ops_menu_hub (hub central)
SUPPRIMER: ops_wrappers.bak (dette .bak)
ÉVALUER: ops_super_menu vs ops_menu_hub (doublon ?)
```

### Action par module

| Module | Action | Cible |
| --- | --- | --- |
| `ops_menu_hub` | CONSERVER — hub central | menus CLI |
| `ops_super_menu` | ÉVALUER — overlap avec hub ? | fusionner ou garder distinct |
| `ops_wrappers` | CONSERVER si utile | wrappers ops |
| `ops_wrappers.bak` | SUPPRIMER — dette .bak | rm ou archive |

### GO requis

```text
GO_OPT_TRADING_OPS_MENUS_CLEANUP_01
SCOPE: supprimer .bak, évaluer super_menu, documenter menus
PRIORITÉ: BASSE
```

---

## E10 — SHARED / TRANSFER (PRIORITÉ BASSE)

### Situation actuelle

```text
shared + shared_files_sftp + shared_sshfs_permanent
Rôle : transfert fichiers inter-machines (dépend reseau_ssh)
```

### Décision

```text
PRODUIT CANONIQUE: shared_files_sftp (SFTP primaire) + shared_sshfs_permanent (mount permanent)
CLARIFIER: shared/ = données partagées vs shared_files_sftp = transport
```

### Action par module

| Module | Action | Cible |
| --- | --- | --- |
| `shared` | CLARIFIER — données vs transport | répertoire données partagées |
| `shared_files_sftp` | CONSERVER — SFTP primaire | transport inter-machine |
| `shared_sshfs_permanent` | CONSERVER — mount permanent | mount SSHFS |

### GO requis

```text
GO_OPT_TRADING_SHARED_TRANSFER_VALIDATION_01
SCOPE: valider SFTP + SSHFS opérationnel, clarifier rôle shared/
PRÉREQ: reseau_ssh consolidation
PRIORITÉ: BASSE
```

---

## SYNTHÈSE — ORDRE DE CONSOLIDATION

```text
PHASE 1 — DÉBLOQUANT (ouvrir en premier)
  E4-a: GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_IMPL_V1_01   ← PRIORITÉ 1
  E1:   GO_OPT_TRADING_DESK_PRO_CONSOLIDATION_01                    ← parallèle
  E5:   GO_OPT_TRADING_MARKET_DATA_PIPELINE_SMOKE_01                ← parallèle

PHASE 2 — POST-BRIDGE
  E4-b: GO_OPENCLAW_OPT_TRADING_RUNTIME_CONSOLIDATION_01
  E3:   GO_OPT_TRADING_BOT_VISION_CONSOLIDATION_01

PHASE 3 — NETTOYAGE
  E2:   GO_OPT_TRADING_PERF_ENGINE_MIGRATION_01
  E8:   GO_OPT_TRADING_DEEPSEEK_CLEANUP_01
  E9:   GO_OPT_TRADING_OPS_MENUS_CLEANUP_01

PHASE 4 — BASSE PRIORITÉ
  E7:   GO_OPT_TRADING_REGISTRY_CONSOLIDATION_01
  E10:  GO_OPT_TRADING_SHARED_TRANSFER_VALIDATION_01
  E6:   GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 (DÉJÀ OUVERT)
```
