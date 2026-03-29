# Desk Pro - Multi-Machine Map

Ce document cartographie l'architecture d'exploitation multi-machines du système Desk Pro.

## 1. Rôles des Machines

| Machine | Rôle Principal | Accès | Fonction |
|---|---|---|---|
| **admin-trading** | Hub / Orchestration | SSH, Write | Exécute les analyses, génère les logs, exporte vers `/shared`. |
| **student** | Consultation / Vérification | SSH, Read-Only | Lit les rapports depuis `/shared`, vérifie l'intégrité. |
| **db-layer** | Ingestion / Stockage | SSH, Read-Only | (Futur) Ingère les résultats JSON dans une DB temporelle. Actuellement en mode consultation. |

## 2. Flux de Données

1. **Exécution** : `admin-trading` lance un run (`desk-pro-run-logged`).
2. **Export** : Le run produit des JSON/HTML dans `data/`.
3. **Partage** : `admin-trading` copie les artefacts finaux vers `/shared/desk_pro/latest` (`desk-pro-copy-latest`).
4. **Consommation** : `student` et `db-layer` lisent `/shared` via leurs wrappers dédiés (`shared-info`).

## 3. Emplacements Clés

| Ressource | admin-trading | student / db-layer |
|---|---|---|
| **Logs Exécution** | `data/logs/desk_pro/` | N/A |
| **Journal Session** | `data/logs/desk_pro/session_journal.log` | N/A |
| **Artefacts Locaux** | `data/desk_runs/`, `data/dashboard/` | N/A |
| **Artefacts Partagés** | `/shared/desk_pro/latest/` (Source) | `/shared/desk_pro/latest/` (Mount) |

## 4. Wrappers Globaux

Chaque machine dispose de wrappers installés dans `/usr/local/bin` pour faciliter l'exploitation.

| Machine | Wrapper Principal | Menu | Info Partage |
|---|---|---|---|
| **admin-trading** | `desk-pro` | `menu-desk_pro` | N/A (Source) |
| **student** | `desk-pro-student` | `menu-desk-pro-student` | `desk-pro-student-shared-info` |
| **db-layer** | `desk-pro-db` | `menu-desk-pro-db` | `desk-pro-db-shared-info` |

## 5. Documentation de Référence

- **admin-trading** : `docs/admin_trading_desk_pro_runbook.md`
- **student** : `docs/student_desk_pro_runbook.md`
- **db-layer** : `docs/db_layer_desk_pro_runbook.md`

---
*Dernière mise à jour : 2026-03-06*
