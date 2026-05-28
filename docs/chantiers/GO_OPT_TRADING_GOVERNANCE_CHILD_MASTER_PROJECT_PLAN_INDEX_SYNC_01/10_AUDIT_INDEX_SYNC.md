# 10_AUDIT_INDEX_SYNC

## Documents lus

| Document | Rôle |
|---|---|
| `docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md` | Source PF de référence — 22 entrées (P0-P4) |
| `docs/governance/GLOBAL_INDEX_UPDATE_TRIGGER_RULE_01.md` | Règle de mise à jour des index |
| `docs/index/GO_INDEX.md` | Index GO principal — section MASTER_PROJECT_PLAN_INDEX (14 PF) + tableau parents (10 entrées) |
| `docs/index/ACTIVE_STREAMS.md` | Flux actifs — table MASTER_PROJECT_PLAN active streams (14 PF) + historiques |
| `docs/index/NEXT_GO_CANDIDATES.md` | Next GO — table MASTER_PROJECT_PLAN next candidates (14 PF) + matrice historique |
| `docs/index/REPRISE.md` | Reprise — table MASTER_PROJECT_PLAN reprise (14 PF) + parents historiques + reprise architecture |

## Constats

### 1. Cohérence inter-index

Les 4 index partagent les mêmes 14 entrées PF dans leurs tables MASTER_PROJECT_PLAN respectives. Les colonnes PF_ID, MASTER_PROJECT_PLAN_ID et Parent continuité sont identiques à travers les 4 fichiers. **Aucune divergence bloquante.**

| Fichier | Entrées PF | Statut |
|---|---|---|
| GO_INDEX.md | 14 | `updated_at: 2026-05-26` |
| ACTIVE_STREAMS.md | 14 | `updated_at: 2026-05-26` |
| NEXT_GO_CANDIDATES.md | 14 | `updated_at: 2026-05-23` |
| REPRISE.md | 14 | `updated_at: 2026-05-23` |

### 2. Alignement avec le registre PF

Le registre liste 22 entrées dont 14 P1/P2 ayant une ligne dans les index. Les P3 (PF_MULTI_MACHINE_SURFACES) et P4 (PF_GOVERNANCE_TRANSPORT) sont correctement exclus des tables MASTER_PROJECT_PLAN_INDEX car supports, non produits.

### 3. Next GO primaire

`GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_INDEX_SYNC_01` est déjà listé comme NEXT_GO primaire global dans NEXT_GO_CANDIDATES.md et REPRISE.md — cohérent.

### 4. Divergences identifiées

| # | Fichier | Divergence | Action |
|---|---|---|---|
| D1 | NEXT_GO_CANDIDATES.md | `updated_at: 2026-05-23` — pas de reflet du présent GO ni des children Termux/Tasker ouverts depuis | Update métadonnées |
| D2 | REPRISE.md | `updated_at: 2026-05-23` — idem, section "Prochaine action forte" pointe vers un GO différent du présent | Update métadonnées |
| D3 | REPRISE.md | Section "Prochaine action forte" mentionne `GO_OPT_TRADING_GOVERNANCE_CHILD_MASTER_PROJECT_PLAN_CREATION_RULE_MATRIX_01` comme next, mais le next réel est le présent GO | Correction mineure |
| D4 | GO_INDEX.md | Priorité opératoire ligne 139 liste ce GO comme P0, mais les parents du tableau parents n'ont pas tous de NEXT_GO aligné avec la table MPP | Aucune — les parents existent |
| D5 | ACTIVE_STREAMS.md | `GO_OPT_TRADING_ARCHITECTURE_CHILD_AUDIT_FROM_MERMAID_01` listé en flux historiques mais son closeout est mergé | Déplacer en hors pilotage |

### 5. Gap analysis

| Gap | Traitement |
|---|---|
| Parents PF absents (Telegram Screener, Telegram Ingestion, Perf Engine Trading Lab, Data Center) | Créer next GO parent open (hors scope de ce GO) |
| `PF_OPENCLAW_ORCHESTRATOR_FULL` marqué PASS — parent reste OPEN | Garder parent ouvert tant que child datasheet_writer non merged |
| `PF_FIGMA_FINANCIAL_COCKPIT` en TBD_DECISION | Conserver jusqu'à décision produit |
| Parents machines (admin-trading, db-layer) listés mais PF absents | Rattacher comme supports P3 |
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` et `PF_STRICT_WORKERS_AI_TEAM` | Fusion conceptuelle à documenter |

## Conclusion

Les index sont synchronisés à ~95%. Patch mineur requis sur NEXT_GO_CANDIDATES.md et REPRISE.md (métadonnées). Aucune divergence structurelle bloquante.
