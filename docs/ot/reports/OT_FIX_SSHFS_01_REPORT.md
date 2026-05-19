# OT-FIX-SSHFS-01 — REPORT (RÉALIGNEMENT PACKAGE/LIVE)

Date (America/Montreal) : 2026-03-12

## 1. RÉSUMÉ EXÉCUTIF
- `shared_sshfs_permanent` : incohérence expliquée par un **déploiement non conforme** (wrappers installés vs service absent) + scripts non robustes aux symlinks.
- `desk_retention` : preuve live admin-trading = **timer quotidien 03:00** ; le repo versionne **10min** → divergence repo/live explicitée et corrigée dans la map.

## 2. PREUVES RELUES
- Diagnostic complet : [OT_FIX_SSHFS_01_DIAGNOSTIC.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_FIX_SSHFS_01_DIAGNOSTIC.md)
- Preuves live : [OT_LIVE_01_MACHINE_DRILL.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_LIVE_01_MACHINE_DRILL.md)

## 3. DIAGNOSTIC (SYNTHÈSE)

### shared_sshfs_permanent
- **Repo** : module “installable” = `INSTALL.sh` + `shared-sshfs.service.template` + config `/etc/opt-trading/shared_sshfs_permanent.env`.
- **Live admin-trading** : unit `shared-sshfs.service` absente, `/shared` non monté, wrappers présents mais pointent vers `modules/.../scripts/cmd.sh` et cassent via symlink.
- **Cause retenue** : déploiement incomplet + mauvais ciblage wrappers + scripts famille A non symlink-safe.

### desk_retention (schedule)
- **Repo** : `modules/desk_retention/systemd/desk_retention.timer` = every 10 minutes.
- **Live admin-trading** : `/etc/systemd/system/desk_retention.timer` = daily 03:00.
- **Conclusion** : le schedule live doit être documenté comme preuve machine, sans effacer le packaging repo.

## 4. CLASSIFICATION CANONIQUE CORRIGÉE (MAP)
- `desk_retention` : Timer (repo 10min ; live admin-trading daily 03:00).
- `vision_bot` : Service (live admin-trading prouvé).
- `shared_sshfs_permanent` : Service **installable au repo**, mais **absent en live sur admin-trading** à date du drill ; wrappers présents mais incohérents.

## 5. CORRECTIONS DOCUMENTAIRES APPLIQUÉES
- [OT_SVC_01_CANONICAL_RUNTIME_MAP.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_SVC_01_CANONICAL_RUNTIME_MAP.md) :
  - correction `desk_retention` (repo vs live schedule),
  - requalification prudente `shared_sshfs_permanent` (repo installable vs live absent + wrappers incohérents),
  - ajout explicite des écarts prouvés.
- [OT_SVC_01_CLOSING.txt](file:///c:/Users/ghost/opt-trading/docs/ot/closings/OT_SVC_01_CLOSING.txt) :
  - réserve déploiement live reformulée (réduite sur admin-trading, maintenue pour shared_sshfs_permanent).

## 6. FICHIERS MODIFIÉS
- `OT_SVC_01_CANONICAL_RUNTIME_MAP.md`
- `OT_SVC_01_CLOSING.txt`

## 7. COMMANDES EXÉCUTÉES
- Aucune nouvelle (réutilisation des preuves OT-LIVE-01).

## 8. VERDICT FINAL
Diagnostic précis et proportionné : `shared_sshfs_permanent` n’est pas “cassé globalement”, mais **non déployé en mode service** sur admin-trading et **mal exposé** via wrappers actuels ; la runtime map est réalignée sur la preuve live, incluant le schedule réel de `desk_retention` sur admin-trading.

## 9. POINT DE REPRISE SUIVANT
- Micro-mission ultérieure (si décidée) : corriger la robustesse symlink des scripts famille A (ou supprimer leur usage) et clarifier quel système doit porter `shared-sshfs.service` (admin-trading vs autres machines), avant toute activation live.

