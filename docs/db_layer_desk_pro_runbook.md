# DB Layer Desk Pro - Runbook

## 1. Objectif
Ce document guide l'opérateur pour utiliser le pack **Desk Pro DB Layer** sur la machine `db-layer` (Linux Headless).
Le rôle principal est la **consultation** des analyses produites par `admin-trading`, la vérification de l'état local, et la préparation à l'ingestion future.

## 2. Pré-requis
- Accès SSH à `db-layer`
- Montage `/shared` actif (pour lire les résultats d'`admin-trading`)
- Pack `desk-pro-db` installé

## 3. Commandes Globales
Les wrappers suivants sont disponibles après installation :

| Commande | Description |
|---|---|
| `desk-pro-db` | Wrapper principal (status, summary) |
| `menu-desk-pro-db` | Menu interactif simple |
| `sanity-desk-pro-db` | Vérification de l'environnement local |
| `desk-pro-db-shared-info` | Lire les derniers résultats partagés |

## 4. Flux Opérateur : Consultation Quotidienne

1. **Connexion SSH**
   ```bash
   ssh user@db-layer
   ```

2. **Vérification de Santé**
   ```bash
   sanity-desk-pro-db
   ```
   *Attendu : "DB Layer Sanity Check Passed"*

3. **Lire les Résultats du Hub (Admin)**
   ```bash
   desk-pro-db-shared-info
   ```
   *Affiche le résumé du dernier run, l'état du portefeuille et les risques, lus depuis `/shared/desk_pro/latest`.*

4. **Vérifier l'État Local**
   ```bash
   desk-pro-db status
   ```

## 5. Gestion des Incidents Courants

### Cas : Shared Info Vide / Missing
**Symptôme** : `desk-pro-db-shared-info` retourne "WARN: Shared directory not found".
**Diagnostic** :
1. Le montage NFS/SSHFS vers `admin-trading` est tombé.
2. `admin-trading` n'a pas encore exporté de run.

**Action** :
1. Vérifier le montage : `ls -ld /shared`
2. Si le montage est OK, attendre qu'`admin-trading` termine un run et fasse un `copy-latest`.

### Cas : Command not found
**Action** :
1. Réinstaller les wrappers :
   ```bash
   sudo ./scripts/db_layer/desk_pro_db_install.sh
   ```

## 6. Emplacements Clés

- **Racine Repo** : `/opt/trading` (typique)
- **Partage Lecture** : `/shared/desk_pro/latest/`
- **Scripts DB Layer** : `scripts/db_layer/`

## 7. Contrat Source Minimal Pour Ingestion Future

- **Surface source canonique** : `/shared/desk_pro/latest/`
- **Artefacts source candidats** :
  - `run_summary.json`
  - `portfolio_engine.json`
  - `journal_engine.json`
  - `perf_engine.json`
- **Producteur source** : `admin-trading` publie ces artefacts via `scripts/admin_trading/desk_pro_cmd.sh copy-latest-to-shared`.
- **Point d'entrée machine actuel** : `desk-pro-db` / `desk-pro-db-shared-info` permettent la consultation de cette surface.
- **Limite canonique actuelle** : l'ingestion DB de ces artefacts n'est pas encore implémentée dans le repo ; cette section formalise seulement le contrat source minimal.

---
*Dernière mise à jour : 2026-03-06*
