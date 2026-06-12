---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01_REPO_PRODUCT_CANDIDATES
doc_type: product_candidates_addendum
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01
parent_go: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/01_REPO_PRODUCT_CANDIDATES.md
---

# 01b_REPO_PRODUCT_CANDIDATES_ADDENDUM - Surfaces manquantes du premier passage

Ce fichier complete l'inventaire principal (`01_REPO_PRODUCT_CANDIDATES.md`).

---

## Candidat 19 -- market_scanner

| Champ | Valeur |
| --- | --- |
| **Nom** | market_scanner |
| **Type** | Module produit (moteur de scanning) |
| **Modules principaux** | `modules/market_scanner/` |
| **Role final prevu** | Scanner de marches pour identifier les opportunites et setups en temps reel ou batch. |
| **Usage actuel prouve** | Module present, wrapper cmd explicitement liste dans ui_indexation et indexation_desk. Mentionne dans deepseek runbook. |
| **Preuves repo** | `docs/ui_indexation/01_ui_registry_modules.md`, `docs/indexation_desk/01_inventory_modules.md`, `docs/student_deepseek_runbook.md` |
| **Gap principal** | Pas de closeout ou de runbook produit dedie. Preuve d'usage moins explicite que pour Desk Pro. |
| **NEXT_GO ou condition** | Documenter usage et sorties avant de proposer ADD_TO_ATLAS. Rester KEEP_CANDIDATE. |

---

## Candidat 20 -- decision_engine

| Champ | Valeur |
| --- | --- |
| **Nom** | decision_engine |
| **Type** | Module (moteur de decision) |
| **Modules principaux** | `modules/decision_engine/` |
| **Role final prevu** | Moteur de decision pour les signaux et strategies trading. Inclut `strategy_logic.py` (reclasse depuis racine). |
| **Usage actuel prouve** | Module present, wrappers cmd/menu. Reference dans OT_SVC_01_CANONICAL_RUNTIME_MAP comme ON-DEMAND. |
| **Preuves repo** | `docs/ot/trae/OT_SVC_01_CANONICAL_RUNTIME_MAP.md`, `docs/indexation_desk/01_inventory_modules.md`, `docs/governance/REPO_ROOT_POLICY.md` |
| **Gap principal** | Closeout ou runbook produit absent. Relation avec execution_engine a clarifier. |
| **NEXT_GO ou condition** | Documenter l'usage avant promotion. KEEP_CANDIDATE. |

---

## Candidat 21 -- execution_engine

| Champ | Valeur |
| --- | --- |
| **Nom** | execution_engine |
| **Type** | Module (moteur d'execution) |
| **Modules principaux** | `modules/execution_engine/` |
| **Role final prevu** | Moteur d'execution pour les ordres et operations trading. |
| **Usage actuel prouve** | Module present, wrappers cmd/menu. Mentionne dans indexation_desk. |
| **Preuves repo** | `docs/indexation_desk/01_inventory_modules.md`, `docs/indexation_desk/02_inventory_menus.md` |
| **Gap principal** | Preuve d'usage produit explicite manquante. |
| **NEXT_GO ou condition** | Documenter avant promotion. KEEP_CANDIDATE. |

---

## Candidat 22 -- journal_engine

| Champ | Valeur |
| --- | --- |
| **Nom** | journal_engine |
| **Type** | Module (journalisation) |
| **Modules principaux** | `modules/journal_engine/` |
| **Role final prevu** | Journalisation structuree des evenements trading. |
| **Usage actuel prouve** | Module present, wrappers cmd/menu. Mentionne dans indexation_desk et ui_registry. |
| **Preuves repo** | `docs/indexation_desk/01_inventory_modules.md`, `docs/ui_indexation/01_ui_registry_modules.md` |
| **Gap principal** | Preuve d'usage produit explicite manquante. |
| **NEXT_GO ou condition** | Documenter avant promotion. KEEP_CANDIDATE. |

---

## Candidat 23 -- liquidation_analyzer

| Champ | Valeur |
| --- | --- |
| **Nom** | liquidation_analyzer |
| **Type** | Module (analyse de liquidation) |
| **Modules principaux** | `modules/liquidation_analyzer/` |
| **Role final prevu** | Analyse des risques de liquidation pour les positions. |
| **Usage actuel prouve** | Module present, wrappers cmd/menu. Mentionne dans ui_registry et indexation_desk. |
| **Preuves repo** | `docs/ui_indexation/01_ui_registry_modules.md`, `docs/indexation_desk/01_inventory_modules.md` |
| **Gap principal** | Preuve d'usage produit explicite manquante. |
| **NEXT_GO ou condition** | Documenter avant promotion. KEEP_CANDIDATE. |

---

## Candidat 24 -- opportunity_ranker

| Champ | Valeur |
| --- | --- |
| **Nom** | opportunity_ranker |
| **Type** | Module (classement d'opportunites) |
| **Modules principaux** | `modules/opportunity_ranker/` |
| **Role final prevu** | Classement et priorisation des opportunites trading. |
| **Usage actuel prouve** | Module present, wrappers cmd/menu. Mentionne dans indexation_desk. |
| **Preuves repo** | `docs/indexation_desk/01_inventory_modules.md`, `docs/indexation_desk/02_inventory_menus.md` |
| **Gap principal** | Preuve d'usage produit explicite manquante. |
| **NEXT_GO ou condition** | Documenter avant promotion. KEEP_CANDIDATE. |

---

## Candidat 25 -- perf_engine

| Champ | Valeur |
| --- | --- |
| **Nom** | perf_engine |
| **Type** | Module (moteur de performance) |
| **Modules principaux** | `modules/perf_engine/`, `modules/perf/` (associe), `perf/perf_app.py` (racine) |
| **Role final prevu** | Moteur de calcul et suivi de performance. |
| **Usage actuel prouve** | Module prouve live : `cmd-perf_engine status` retourne "Perf Engine Status: OK" (OT_LIVE_01_REPORT.md). Wrapper non declare en registry (gap documente). |
| **Preuves repo** | `docs/ot/reports/OT_LIVE_01_REPORT.md`, `docs/ui_indexation/01_ui_registry_modules.md`, `docs/indexation_desk/01_inventory_modules.md` |
| **Gap principal** | Pas de closeout produit dedie. Wrapper non declare en registry. |
| **NEXT_GO ou condition** | Ajouter l'entree registry wrapper, puis documenter l'usage. KEEP_CANDIDATE. |

---

## Candidat 26 -- marketdata

| Champ | Valeur |
| --- | --- |
| **Nom** | marketdata |
| **Type** | Module (donnees de marche) |
| **Modules principaux** | `modules/marketdata/` |
| **Role final prevu** | Gestion et distribution des donnees de marche. |
| **Usage actuel prouve** | Module present. Mentionne dans ui_registry et indexation_desk. |
| **Preuves repo** | `docs/ui_indexation/01_ui_registry_modules.md`, `docs/indexation_desk/01_inventory_modules.md` |
| **Gap principal** | Preuve d'usage peu documentee. Role exact flou. |
| **NEXT_GO ou condition** | Documenter avant toute promotion. KEEP_CANDIDATE. |

---

## Candidat 27 -- memory_bricks

| Champ | Valeur |
| --- | --- |
| **Nom** | memory_bricks |
| **Type** | Module de support (compaction derivee) |
| **Modules principaux** | `modules/memory_bricks/` |
| **Role final prevu** | Compaction derivee structuree servant a la reprise de session. Subordonnee a la hierarchie produit. |
| **Usage actuel prouve** | Module documente dans la gouvernance. Pilote closeout PASS. Derivation subordonnee aux fiches produit finales. |
| **Preuves repo** | `docs/governance/MEMORY_BRICKS_MAPPING.md`, `docs/governance/REPO_ROLE.md`, `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`, `docs/index/GO_CLOSED_INDEX.md` |
| **Gap principal** | Compaction derivee, pas un produit utilisateur final. Ne releve pas de l'Atlas produit. |
| **NEXT_GO ou condition** | DO_NOT_PROMOTE. Laisser comme couche de support documentee dans la gouvernance. |

---

## Candidat 28 -- workflow_ai

| Champ | Valeur |
| --- | --- |
| **Nom** | workflow_ai |
| **Type** | Doctrine de processus (doc-only) |
| **Modules principaux** | `workflow_ai/` (repertoire racine) : `WORKFLOW.md`, `templates/specs.md`, `templates/tasks.md` |
| **Role final prevu** | Doctrine gated d'execution IA : GO/STOP, gates, templates opposables. |
| **Usage actuel prouve** | Reference dans le starter pack, les audits OT, les closeouts, la doctrine Trae. |
| **Preuves repo** | `workflow_ai/WORKFLOW.md`, `docs/ot/reports/OT_STARTERPACK_AUDIT_01_REPORT.md`, `docs/master_pack/mission_starter_pack/00_mission_start_guide.md` |
| **Gap principal** | Doctrine de processus, pas un produit runtime. |
| **NEXT_GO ou condition** | DO_NOT_PROMOTE. Ce n'est pas un produit, c'est une regle de processus. |

---

## Candidat 29 -- deploy_module_multi_machine

| Champ | Valeur |
| --- | --- |
| **Nom** | deploy_module_multi_machine |
| **Type** | Outillage de deploiement |
| **Modules principaux** | `deploy_module_multi_machine/` (repertoire racine) : wrappers cmd/menu/sanity, preflight, deploy |
| **Role final prevu** | Propagation multi-machine des modules depuis `admin-trading` vers `student`, `db-layer` et cibles declarees. |
| **Usage actuel prouve** | Outillage valide, documente, wrappers operationnels. Reference dans ops_wrappers runbook. |
| **Preuves repo** | `docs/deploy_module_multi_machine_continuity.md`, `docs/ops_wrappers_source_layout_refresh_runbook.md` |
| **Gap principal** | Outillage de support, pas un produit operateur final. |
| **NEXT_GO ou condition** | DO_NOT_PROMOTE. C'est un outil de deploiement, pas un produit Atlas. |

---

## Candidat 30 -- webhook_server.py (runtime racine)

| Champ | Valeur |
| --- | --- |
| **Nom** | webhook_server (racine) |
| **Type** | Runtime historique racine |
| **Modules principaux** | `webhook_server.py` (fichier racine) |
| **Role final prevu** | Entrypoint runtime historique du webhook, toujours actif et reference par la doc canonique. |
| **Usage actuel prouve** | Runtime actif. Reference dans REPO_ROOT_POLICY.md comme entrypoint historique toujours actif. |
| **Preuves repo** | `docs/governance/REPO_ROOT_POLICY.md` |
| **Gap principal** | Runtime racine, deja capture sous TradingView/Telegram Alert Pipeline (module `webhook/`). Pas un produit separe. |
| **NEXT_GO ou condition** | DO_NOT_PROMOTE. Deja couvert par TradingView/Telegram Alert Pipeline. |

---

## Candidat 31 -- bitget_bridge.py (shim legacy)

| Champ | Valeur |
| --- | --- |
| **Nom** | bitget_bridge (shim racine) |
| **Type** | Shim legacy de compatibilite |
| **Modules principaux** | `bitget_bridge.py` (fichier racine) |
| **Role final prevu** | Shim historique pointant vers `modules/simex_bitget_bridge/`. Conserve explicitement comme point d'entree secondaire. |
| **Usage actuel prouve** | Shim legacy. Module canonique = `modules/simex_bitget_bridge/`. |
| **Preuves repo** | `docs/governance/REPO_ROOT_POLICY.md` |
| **Gap principal** | Aucun. Shim de compatibilite, deja couvert par Simex Bitget Bridge. |
| **NEXT_GO ou condition** | DO_NOT_PROMOTE. ARCHIVE_ONLY. |

---

## Candidat 32 -- hf_free_platform

| Champ | Valeur |
| --- | --- |
| **Nom** | hf_free_platform |
| **Type** | Module (plateforme Hugging Face) |
| **Modules principaux** | `modules/hf_free_platform/` |
| **Role final prevu** | Interface vers la plateforme gratuite Hugging Face pour des taches IA. |
| **Usage actuel prouve** | Module present mais aucune reference documentaire explicite dans les docs canoniques scannes. |
| **Preuves repo** | Presence dans `modules/` uniquement. |
| **Gap principal** | Aucune preuve d'usage produit documentee. |
| **NEXT_GO ou condition** | DO_NOT_PROMOTE. Aucune preuve d'usage. Rester comme module technique. |

---

## Candidat 33 -- mimo_open_observer

| Champ | Valeur |
| --- | --- |
| **Nom** | mimo_open_observer |
| **Type** | Module (observateur MIMO) |
| **Modules principaux** | `modules/mimo_open_observer/` |
| **Role final prevu** | Observateur pour le protocole/strategie MIMO. |
| **Usage actuel prouve** | Module present mais aucune reference documentaire explicite dans les docs canoniques scannes. |
| **Preuves repo** | Presence dans `modules/` uniquement. |
| **Gap principal** | Aucune preuve d'usage produit documentee. |
| **NEXT_GO ou condition** | DO_NOT_PROMOTE. Rester comme module technique. |

---

## Candidat 34 -- kil_v1

| Champ | Valeur |
| --- | --- |
| **Nom** | kil_v1 |
| **Type** | Module (role inconnu) |
| **Modules principaux** | `modules/kil_v1/` |
| **Role final prevu** | Inconnu. |
| **Usage actuel prouve** | Module present mais aucune reference documentaire explicite. |
| **Preuves repo** | Presence dans `modules/` uniquement. |
| **Gap principal** | Role et usage totalement inconnus. |
| **NEXT_GO ou condition** | UNKNOWN_NEEDS_RESCAN. A investiguer avant toute decision. |

---

## Candidat 35 -- workflow_post_change_v2

| Champ | Valeur |
| --- | --- |
| **Nom** | workflow_post_change_v2 |
| **Type** | Module (workflow post-modification) |
| **Modules principaux** | `modules/workflow_post_change_v2/` |
| **Role final prevu** | Gestion du workflow apres changement de code ou de config. |
| **Usage actuel prouve** | Module present. Fiche statut canonique dans docs/status. Script sanity associe dans scripts/. |
| **Preuves repo** | `docs/status/workflow_post_change_canonique.md`, `scripts/sanity_check_post_change_v2.sh` |
| **Gap principal** | Module de support operationnel, pas un produit utilisateur final. |
| **NEXT_GO ou condition** | DO_NOT_PROMOTE. Support operationnel. |

---

## Candidat 36 -- Modules de support et infrastructure

Ces modules sont des couches de support technique, pas des produits utilisateur finaux.

| Module | Role | Decision |
| --- | --- | --- |
| `env` | Gestion d'environnement | DO_NOT_PROMOTE |
| `health` | Health check | DO_NOT_PROMOTE |
| `auth` | Authentification | DO_NOT_PROMOTE |
| `install_module` | Installeur generique | DO_NOT_PROMOTE |
| `naming_normalizer` | Normalisation de noms | DO_NOT_PROMOTE |
| `router` | Routage | DO_NOT_PROMOTE |
| `shared` | Support partage | DO_NOT_PROMOTE |
| `shared_files_sftp` | SFTP partage | DO_NOT_PROMOTE |
| `shared_sshfs_permanent` | SSHFS permanent | DO_NOT_PROMOTE |
| `winscp_transfer` | Transfert WinSCP | DO_NOT_PROMOTE |
| `repo_hygiene` | Hygiene repo | DO_NOT_PROMOTE |
| `repo_local_artifacts` | Artefacts locaux | DO_NOT_PROMOTE |
| `repo_ownership_guard` | Garde de propriete | DO_NOT_PROMOTE |
| `audit` | Audit | DO_NOT_PROMOTE |
| `dev_validation_hub` | Hub de validation dev | DO_NOT_PROMOTE |
| `scripts` (in modules/) | Scripts internes | DO_NOT_PROMOTE |
| `engines` | Wrapper moteurs generique | DO_NOT_PROMOTE |
| `trae_module_validator` | Validateur TRAE | DO_NOT_PROMOTE |
| `ui_registry_msi` | UI registry MSI | DO_NOT_PROMOTE |
| `perf` (modules/perf/) | Perf analysis (overlap avec perf_engine) | DO_NOT_PROMOTE |

---

## Candidat 37 -- packages/collectors_core

| Champ | Valeur |
| --- | --- |
| **Nom** | collectors_core |
| **Type** | Fondation partagee (package) |
| **Modules principaux** | `packages/collectors_core/` |
| **Role final prevu** | Base runtime partagee pour les modules collecteurs (coingecko, binance_spot, futur derivatives). |
| **Usage actuel prouve** | Package valide, utilise par collector_coingecko et collector_binance_spot. Doctrine famille reference cette base. |
| **Preuves repo** | `docs/COLLECTORS_FAMILY_DOCTRINE_01.md`, `docs/COLLECTORS_MIGRATION_MAP_01.md` |
| **Gap principal** | Fondation partagee, pas un produit autonome. Deja couvert par la doctrine famille collector. |
| **NEXT_GO ou condition** | DO_NOT_PROMOTE. Deja represente via derivatives_collector et collectors spot. |

---

## Candidat 38 -- adapters/webhook_to_perf.py

| Champ | Valeur |
| --- | --- |
| **Nom** | webhook_to_perf adapter |
| **Type** | Adapter (pont runtime) |
| **Modules principaux** | `adapters/webhook_to_perf.py` |
| **Role final prevu** | Pont entre le webhook entrant et la couche perf/perf_engine. |
| **Usage actuel prouve** | Fichier present dans adapters/. |
| **Preuves repo** | `adapters/webhook_to_perf.py` |
| **Gap principal** | Adapter de connectivite, pas un produit. |
| **NEXT_GO ou condition** | DO_NOT_PROMOTE. Couvert par TradingView Pipeline et perf_engine. |

---

## Zones grises identifiees

### ZG-01 : frontiere desk_pro vs desk_*
- Plusieurs modules `desk_*` ne sont pas `desk_pro*` : `desk_analyze`, `desk_capture_inputs`, `desk_common`, `desk_retention`, `desk_snapshot_ingest`, `desk_state`. La fiche statut les qualifie de "satellites adjacents" sans trancher s'ils forment un produit separe ou un sous-ensemble de Desk Pro.
- Recommandation : les traiter comme partie de la stack Desk Pro jusqu'a clarification structurelle.

### ZG-02 : survivant unique Bot Vision
- La chaine transitoire `vision_bot` + `bot_vision_step2` est active mais aucun survivant unique n'est fige.
- `bot_vision` est explicitement marque legacy.
- Recommandation : maintenir `USABLE_LIMITED` pour le produit Bot Vision, avec NEXT_GO = `VISION_FAMILY_SURVIVOR_DECISION`.

### ZG-03 : kil_v1 role inconnu
- Module present dans `modules/kil_v1/` sans documentation exploitable.
- Recommandation : UNKNOWN_NEEDS_RESCAN. Ne pas promouvoir.

### ZG-04 : hf_free_platform et mimo_open_observer non documentes
- Modules presents sans reference documentaire canonique.
- Recommandation : DO_NOT_PROMOTE tant qu'aucune preuve d'usage n'est apportee.

### ZG-05 : perf vs perf_engine vs perf_app.py
- Trois surfaces distinctes pour la performance : `modules/perf/`, `modules/perf_engine/`, `perf/perf_app.py` (racine).
- `perf_engine` est prouve live.
- Recommandation : traiter comme un seul produit `perf_engine` avec `perf_app.py` comme runtime associe. `modules/perf/` comme support technique.

### ZG-06 : recouvrement TradingView Pipeline et webhook_server.py
- `webhook_server.py` est un runtime historique racine, `modules/webhook/` est le module.
- Le pipeline TradingView inclut deja les deux.
- Recommandation : pas de doublon. Couvert par le candidat TradingView / Telegram Alert Pipeline.

### ZG-07 : scripts hors modules
- `scripts/student/` contient le runtime reel Deepseek, deja couvert.
- `scripts/admin_trading/` contient le runtime admin Desk Pro / Bot Vision, deja couvert.
- `scripts/db_layer/`, `scripts/release_ops/`, `scripts/desk_bridge/` : scripts de support operationnel, pas des produits.
- Recommandation : pas de nouvelle entree Atlas pour les scripts de support.

## RISKS

- À qualifier.
