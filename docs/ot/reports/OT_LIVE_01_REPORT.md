# OT-LIVE-01 — REPORT (DRILL LIVE SYSTEMD / WRAPPERS)

Date (America/Montreal) : 2026-03-12

## 1. RÉSUMÉ EXÉCUTIF
- **Machine inspectée** : `admin-trading` (preuve SSH collectée).
- **Systemd live** : `vision_bot.service` et `desk_retention.timer/service` sont **présents et configurés** ; `shared-sshfs.service` et mount `/shared` sont **absents**.
- **Wrappers live** : wrappers opérateur Desk Pro et Prompt Factory sont présents et exécutables ; wrappers `shared_sshfs_permanent` sont présents mais **cassés en exécution via symlink** (preuve `name=local/path=/usr/local`).
- **Réserve OT-SVC-01** : **réduite** (vision_bot + desk_retention prouvés live) mais **maintenue** pour `shared_sshfs_permanent`.
- **Réserve OT-DOC-01** : **inchangée** (corpus local/kanban absent reste hors preuve live).

## 2. MÉTHODE
- Accès : SSH batch vers `ghost@admin-trading`.
- Actions : lecture uniquement (`systemctl`, `command -v`, `readlink -f`, exécutions non destructives de commandes “status/list-modes/info”).
- Preuve brute : [OT_LIVE_01_MACHINE_DRILL.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_LIVE_01_MACHINE_DRILL.md).

## 3. INVENTAIRE LIVE SYSTEMD (ADMIN-TRADING)

| Élément | Attendu (repo/package) | Observé live | Classification |
| :--- | :--- | :--- | :--- |
| `vision_bot.service` | Service versionné | présent, enabled, active (running) | **A. ÉTABLI LIVE** |
| `desk_retention.timer` | Timer versionné | présent, enabled, active (waiting) | **A. ÉTABLI LIVE** |
| `desk_retention.service` | oneshot déclenché par timer | présent, static, dernière exécution OK | **A. ÉTABLI LIVE** |
| `shared-sshfs.service` | service (template) attendu | absent (unit not found) | **D. ABSENT / NON DÉPLOYÉ** |
| `mnt-shared.mount` / `mnt-shared.automount` | non requis au repo | absent | **D. ABSENT / NON DÉPLOYÉ** |
| `desk_snapshot_ingest.service` | non fourni au repo | absent | **B. ÉTABLI AU REPO UNIQUEMENT** (hybride, pas de service officiel) |

### Écart critique prouvé : `desk_retention.timer` (repo vs live)
- Repo : `desk_retention.timer` documenté “10min” dans [OT_SVC_01_CANONICAL_RUNTIME_MAP.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_SVC_01_CANONICAL_RUNTIME_MAP.md#L47-L53).
- Live : `OnCalendar=*-*-* 03:00:00` (quotidien 03:00) prouvé par `systemctl cat desk_retention.timer` (voir [OT_LIVE_01_MACHINE_DRILL.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_LIVE_01_MACHINE_DRILL.md)).
- Conclusion : la carte repo doit conserver une réserve “fréquence live non garantie” tant qu’elle n’est pas harmonisée.

## 4. INVENTAIRE LIVE WRAPPERS (ADMIN-TRADING)

### 4.1 Wrappers Desk Pro (prouvés live)
- `menu-ops_menu_hub` : présent, symlink vers `/opt/trading/modules/ops_menu_hub/scripts/menu.sh` → **A. ÉTABLI LIVE**
- `cmd-desk_pro_runner` : présent ; `cmd-desk_pro_runner status` retourne JSON `runner_status: OK` → **A. ÉTABLI LIVE**
- `sanity-desk_pro_runner` : présent ; exécution retourne “Sanity Check Passed.” → **A. ÉTABLI LIVE**
- `cmd-desk_pro_dashboard` : présent (exécution non testée ici) → **C. À CONFIRMER**

### 4.2 Wrappers validated_prompt_factory / trae_module_validator (prouvés live)
- `cmd-validated_prompt_factory list-modes` : OK → **A. ÉTABLI LIVE**
- `menu-validated_prompt_factory` : présent (menu interactif non testé) → **C. À CONFIRMER**
- `cmd/menu/sanity-trae_module_validator` : présents (exécution non testée) → **C. À CONFIRMER**

### 4.3 Wrappers shared_sshfs_permanent (présents mais écart critique prouvé)
- Présence : `menu/cmd/sanity-shared_sshfs_permanent` existent et pointent vers `modules/shared_sshfs_permanent/scripts/*`.
- Exécution : `cmd-shared_sshfs_permanent info` retourne `name=local path=/usr/local` (preuve).
- Sanity : `sanity-shared_sshfs_permanent` retourne `FAIL: scripts missing` (preuve).
- Cause probable (repo) : scripts `cmd.sh`/`sanity_check.sh` utilisent `${0%/*}/..` sans résolution `readlink -f` → casse quand invoqué via symlink `/usr/local/bin`.
- Classification : **Repo oui / Live oui / Exécutable correct = NON** → **Écart critique**.

### 4.4 Wrappers présents live mais non décrits dans wrappers_registry
- Exemple prouvé : `cmd-perf_engine` existe et est exécutable (`cmd-perf_engine status` retourne “Perf Engine Status: OK”).
- Observation : `wrappers_registry.yaml` ne contient pas d’entrées pour `perf_engine`, `desk_snapshot_ingest`, `vision_bot`, `desk_retention`, `shared_sshfs_permanent` (lecture repo).
- Classification : **Live oui / Registry non** (registry incomplet pour ces wrappers).

## 5. COMPARAISON REPO VS LIVE (ÉLÉMENTS CLÉS)

| Élément clé | Repo/package | Live | Résultat |
| :--- | :--- | :--- | :--- |
| vision_bot service | Oui (unit file versionné) | Oui (enabled+active) | **Repo oui / Live oui** |
| desk_retention timer | Oui (unit file versionné) | Oui (enabled+active) | **Repo oui / Live oui** + **écart de schedule** |
| shared_sshfs_permanent systemd | Oui (template + INSTALL) | Non (unit absente, /shared non monté) | **Repo oui / Live absent** |
| shared_sshfs_permanent wrappers | Non déclaré registry | Oui (symlinks) | **Live oui / Repo registry non** + **wrappers cassés** |

## 6. ÉCARTS CRITIQUES
1. `desk_retention.timer` : fréquence live ≠ fréquence repo (03:00 daily vs 10min).
2. `shared_sshfs_permanent` : absence de `shared-sshfs.service` + absence de montage `/shared`.
3. `shared_sshfs_permanent` : wrappers présents mais non fonctionnels via symlink (non conformité à la “règle d’or” `readlink -f`).
4. Registry wrappers : couverture incomplète des wrappers live (au moins `perf_engine`, `desk_snapshot_ingest`, `shared_sshfs_permanent`).

## 7. RÉSERVES LEVÉES / MAINTENUES
- **OT-SVC-01** : réserve **réduite** (vision_bot + desk_retention prouvés live) ; réserve **maintenue** pour `shared_sshfs_permanent` (service/mount absents + wrapper bug).
- **OT-DOC-01** : réserve **inchangée** (corpus local/kanban absent non résolu par un drill live).

## 8. FICHIERS MODIFIÉS
- Aucun (mission lecture/preuve uniquement).

## 9. COMMANDES EXÉCUTÉES
- Voir [OT_LIVE_01_MACHINE_DRILL.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_LIVE_01_MACHINE_DRILL.md).

## 10. VERDICT FINAL
Drill live réussi sur `admin-trading` : preuves concrètes collectées pour systemd et wrappers. Les réserves sont requalifiées strictement : levée partielle (vision_bot/desk_retention), maintien (shared_sshfs_permanent + divergence schedule + registry wrappers incomplet).

## 11. POINT DE REPRISE SUIVANT
Micro-mission documentaire (sans refactor) : mettre à jour la carte `OT_SVC_01_CANONICAL_RUNTIME_MAP.md` en distinguant “repo schedule” vs “live schedule observé”, et ouvrir un point “À corriger plus tard” pour `shared_sshfs_permanent` (résolution symlink + installation systemd).


## RISKS

- À qualifier.
