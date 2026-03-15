# OT-DOC-01 — REPORT (RÉALIGNEMENT DOCS HAUT NIVEAU)

## 1. RÉSUMÉ EXÉCUTIF
- Docs haut niveau réalignées sur l’état repo/package, sans sur-interpréter le live.
- Réserves live conservées explicitement (systemd/wrappers live non prouvés).

## 2. MÉTHODE
- Lecture des sources canoniques (master pack, registries YAML).
- Détection d’écarts par contradiction explicite (assertion “Done”, absence de réserve live, gap dépassé par le repo).
- Micro-corrections uniquement, sans réécriture totale.

## 3. PROPOSITION CANONIQUE COMPACTE (REPO/PACKAGE)
- **Contexte canonique** : [00_current_state_and_standards.md](file:///c:/Users/ghost/opt-trading/docs/master_pack/00_current_state_and_standards.md)
- **Source de vérité versionnée** : [registry/README.md](file:///c:/Users/ghost/opt-trading/registry/README.md) + [modules_registry.yaml](file:///c:/Users/ghost/opt-trading/registry/modules_registry.yaml) + [wrappers_registry.yaml](file:///c:/Users/ghost/opt-trading/registry/wrappers_registry.yaml)
- **Opérateur Desk Pro (admin-trading)** : [OT_OPS_RUNBOOK_ADMIN_TRADING.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_OPS_RUNBOOK_ADMIN_TRADING.md)
- **Service/Timer/On-Demand (repo)** : [OT_SVC_01_CANONICAL_RUNTIME_MAP.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_SVC_01_CANONICAL_RUNTIME_MAP.md) avec réserve live (voir closing OT-SVC-01).

## 4. CORRECTIONS APPLIQUÉES (DOCS)
- [registry/README.md](file:///c:/Users/ghost/opt-trading/registry/README.md) : portée “opt-trading” + réserve repo/package ≠ preuve live.
- [ROADMAP.md](file:///c:/Users/ghost/opt-trading/docs/ROADMAP.md) : “Done” rétrogradé en “À confirmer” + note de prudence.
- [05_ui_gap_analysis.md](file:///c:/Users/ghost/opt-trading/docs/ui_indexation/05_ui_gap_analysis.md) : Gap A réaligné (registry UI existe au repo ; adoption live à confirmer).

## 5. RÉSERVES MAINTENUES
- Aucun document n’affirme que les timers/services sont “prouvés live” sur la seule base du repo.
- Le statut de déploiement live reste explicitement un point à confirmer (cf. OT-SVC-01).

