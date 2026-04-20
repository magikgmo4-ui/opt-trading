# DESK PRO — SYNTHÈSE CANONIQUE PRODUIT

## 1. Objet
- Ce document synthétise le produit **Desk Pro** (multi-machine) dans un format court et opposable.
- Il ne remplace pas les runbooks détaillés (procédures opérateur, commandes, diagnostics).

## 2. Besoin initial
- Dépasser des UI/modules isolés.
- Obtenir un cockpit opérateur réellement exploitable (discipline d’exploitation, runs rejouables, artefacts lisibles).

## 3. Objectif final visé
- Cockpit **paper trading** multi-machine :
  - piloté sur `admin-trading`
  - exporté vers `/shared/desk_pro/latest/`
  - consultable sur `student`
  - préparant l’aval `db-layer` (ingestion future, non implémentée)

## 4. Plan validé
- Hiérarchie canonique des surfaces opératoires (entrypoints/wrappers explicites).
- Runs loggés et rejouables (log horodaté + liens `latest`).
- Dashboard + journal + export.
- Partage via `/shared` comme surface de distribution inter-machines.
- Séparation explicite des usages par machine (production vs consultation).

## 5. État obtenu
Séparation explicite : **fil produit/repo** vs **fil machine**.

### 5.1 Fil produit / repo
- Point d’entrée opérateur canonique : `menu-ops_menu_hub` (session).
- Wrapper admin (orchestration / utilitaires) : `scripts/admin_trading/desk_pro_cmd.sh` (status, run-logged, logs, journal, export/copy vers `/shared`).
- Backend direct (CLI runner) : `cmd-desk_pro_runner` (ex: dashboard-latest).
- Export réseau prouvé : copie des artefacts finaux vers `/shared/desk_pro/latest/`.
- Journal de session prouvé côté admin : `data/logs/desk_pro/session_journal.log`.
- Release ops prouvée (procédure de tag + vérification Linux) : runbook dédié.

### 5.2 Fil machine
- `admin-trading` = **production / pilotage / export**
  - exécute les runs
  - produit logs/artefacts locaux sous `data/`
  - copie vers `/shared/desk_pro/latest/`
- `student` = **consultation**
  - lit `/shared/desk_pro/latest/`
  - wrappers dédiés : `desk-pro-student*` (sanity, status, shared-info)
- `db-layer` = **consultation + préparation à ingestion future**
  - lit `/shared/desk_pro/latest/`
  - wrappers dédiés : `desk-pro-db*` (sanity, status, shared-info)
  - ingestion DB : non implémentée dans l’état établi

## 6. Gap restant
- Synthèse produit “unifiée” encore dispersée entre runbooks (ce document la fixe, mais sans remplacer les runbooks).
- Ingestion réelle côté `db-layer` non faite (seulement consultation + préparation).
- Un closage “produit complet” resterait conditionné à :
  - une spécification opposable de l’ingestion depuis `/shared/desk_pro/latest/` vers une DB (contrat données, fréquence, erreurs, rollback)
  - une preuve de validation end-to-end côté `db-layer` (hors scope ici)

## 7. Ce que Desk Pro n’est pas
- Pas du trading réel prouvé (cible : paper trading opérable).
- Pas une ingestion DB implémentée (seulement une préparation/documentation côté `db-layer`).
- Pas un produit `db-layer` autonome (Desk Pro reste piloté par `admin-trading` et distribué via `/shared`).

## 8. Prochain GO recommandé
> GO_DB_LAYER_SHARED_TO_DB_INGESTION_SPEC_01

## 9. Références canoniques minimales
- [AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md](file:///c:/Users/ghost/opt-trading/docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md)
- [admin_trading_desk_pro_runbook.md](file:///c:/Users/ghost/opt-trading/docs/admin_trading_desk_pro_runbook.md)
- [student_desk_pro_runbook.md](file:///c:/Users/ghost/opt-trading/docs/student_desk_pro_runbook.md)
- [db_layer_desk_pro_runbook.md](file:///c:/Users/ghost/opt-trading/docs/db_layer_desk_pro_runbook.md)
- [desk_pro_multi_machine_map.md](file:///c:/Users/ghost/opt-trading/docs/desk_pro_multi_machine_map.md)
- [desk_pro_release_ops_runbook.md](file:///c:/Users/ghost/opt-trading/docs/desk_pro_release_ops_runbook.md)
- [db_layer_desk_pro_quick_reference.md](file:///c:/Users/ghost/opt-trading/docs/db_layer_desk_pro_quick_reference.md)
