---
doc_id: OPT_TRADING_GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_TARGET_01
doc_type: chantier_report
repo: opt-trading
project: opt-trading
go_id: GO_GITHUB_PARK_AUDIT_EXPANSION_01
status: active
lifecycle_stage: planning
topic_keys:
  - github
  - branches
  - trunks
  - convergence
  - canonical
surface: park
source_kind: canonical
updated_at: 2026-04-17
links:
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/01_branch_trunk_cross_audit.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/04_consolidation_targets_and_go_list.md
  - docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/03_decisions.md
---

# 04_branch_trunk_cross_audit_target — cible de convergence

## Besoin initial
- disposer d’une cible explicite pour la convergence `branches ↔ trunk` sans dépendre d’une session
- éviter la création d’un canon parallèle à côté de `opt-trading` / `sot/mainline`

## Cible finale
- le tronc canonique reste `opt-trading` sur `sot/mainline`
- les branches servent à isoler des chantiers, audits ou refactors, puis doivent être rattachées (absorbées, closées ou reclassées)
- aucune surface d’exécution (cockpit local ou distant) ne devient une source de vérité supérieure au repo

### Séparation explicite des couches (rappel)
- Trae : cockpit local de construction (dev / doc / repo)
- OpenClaw : cockpit distant d’exploitation runtime / trading
- tmux : persistance session/runtime
- Telegram : contrôle léger / notification / déclenchement distant
- Git + docs : canon de continuité, de reprise et de vérité

## Plan validé
1. s’appuyer sur l’audit croisé `branches ↔ trunks` comme lecture opératoire (repo par repo)
2. distinguer, pour chaque branche, sa classe réelle : absorbée, utile, historique/parking, ou à requalifier
3. converger vers un tronc lisible en supprimant les ambiguïtés de canon :
   - pas de “canon cockpit”
   - pas de “canon zip”
   - pas de doc de décision hors repo

## ETABLI
- rapport canonique présent : `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/01_branch_trunk_cross_audit.md`
- closeout présent : `docs/ot/closings/OT_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01_CLOSING.txt`
- `docs/index/GO_INDEX.md` référence ce fichier comme cible de convergence du chantier GitHub Park

## Gap restant
- matérialiser, repo par repo, la suite opératoire de convergence à partir de l’audit (actions explicites, bornées, repo-first)
- éviter tout glissement vers un canon parallèle (cockpit, bundles, notes de session)

## Next GO
- se conformer au `Next GO` du chantier parent `GO_GITHUB_PARK_AUDIT_EXPANSION_01` et à la matrice `docs/index/REPRISE.md`
