# OT-DOC-01 — GAP REPORT (DOCS HAUT NIVEAU)

## 1. RÉSUMÉ EXÉCUTIF
- Objectif atteint : correction ciblée des docs haut niveau contredites par l’état repo/package.
- Réserve maintenue : aucune correction n’est présentée comme preuve de déploiement live.
- Résultat : formulations “Done”/“canonique” rétrogradées quand non prouvées, et réserves live explicitées.

## 2. PÉRIMÈTRE EXACT
- Inclus : docs haut niveau (registry, roadmap, UI gap) + recroisement avec master pack, runbook Desk Pro, registry YAML, et OT-SVC-01.
- Exclu : audit runtime live (systemd réel, wrappers installés sur machines).

## 3. DOCS INSPECTÉES
- [00_current_state_and_standards.md](file:///c:/Users/ghost/opt-trading/docs/master_pack/00_current_state_and_standards.md)
- [README.md](file:///c:/Users/ghost/opt-trading/registry/README.md)
- [ROADMAP.md](file:///c:/Users/ghost/opt-trading/docs/ROADMAP.md)
- [05_ui_gap_analysis.md](file:///c:/Users/ghost/opt-trading/docs/ui_indexation/05_ui_gap_analysis.md)
- [OT_SVC_01_CANONICAL_RUNTIME_MAP.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_SVC_01_CANONICAL_RUNTIME_MAP.md)
- [OT_SVC_01_CLOSING.txt](file:///c:/Users/ghost/opt-trading/docs/ot/closings/OT_SVC_01_CLOSING.txt)
- [OT_OPS_RUNBOOK_ADMIN_TRADING.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_OPS_RUNBOOK_ADMIN_TRADING.md)
- [modules_registry.yaml](file:///c:/Users/ghost/opt-trading/registry/modules_registry.yaml)
- [wrappers_registry.yaml](file:///c:/Users/ghost/opt-trading/registry/wrappers_registry.yaml)

## 4. ÉCARTS RELEVÉS (CLASSIFICATION)
- **OBSOLÈTE / À CORRIGER** — Roadmap : multiples lignes “Done” non prouvées (déploiement live / access Windows / CI).
  - Preuve : [ROADMAP.md](file:///c:/Users/ghost/opt-trading/docs/ROADMAP.md)
  - Correction : “Done” → “À confirmer”, ajout d’un avertissement de portée repo vs live.
- **OBSOLÈTE / À CORRIGER** — UI gap : “pas encore de registry UI canonique” alors qu’un socle registry existe au repo + module lecteur versionné.
  - Preuve : [05_ui_gap_analysis.md](file:///c:/Users/ghost/opt-trading/docs/ui_indexation/05_ui_gap_analysis.md)
  - Correction : reformulation “ÉTABLI (repo)” + “À CONFIRMER (live)”.
- **OBSOLÈTE / À CORRIGER** — Registry : portée trop “Desk Pro” et absence de réserve explicite repo vs live.
  - Preuve : [README.md](file:///c:/Users/ghost/opt-trading/registry/README.md)
  - Correction : portée “opt-trading” + note explicite “repo/package ≠ preuve live”.
- **ÉTABLI (repo)** — Fichier kanban “source of truth” : `opt_trading_kanban_source_of_truth_2026-03-13_updated.md` présent dans le repo.

## 5. RÉSERVES MAINTENUES (LIVE NON PROUVÉ)
- État réellement déployé des unités systemd sur machines live : non prouvé (repo/package uniquement). Voir [OT_SVC_01_CLOSING.txt](file:///c:/Users/ghost/opt-trading/docs/ot/closings/OT_SVC_01_CLOSING.txt).
- Forme canonique exacte de `shared_sshfs_permanent` en live (template/service/mount/automount) : non prouvée.

