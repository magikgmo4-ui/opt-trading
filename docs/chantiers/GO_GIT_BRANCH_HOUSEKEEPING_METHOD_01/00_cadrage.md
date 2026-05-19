---
doc_id: OPT_TRADING_GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01_CADRAGE
doc_type: chantier
repo: opt-trading
project: opt-trading
go_id: GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01
status: pass
lifecycle_stage: cadrage
topic_keys:
  - git
  - branches
  - housekeeping
  - workflow
  - skill
surface: chantier
source_kind: canonical
updated_at: 2026-04-17
links:
  - docs/governance/SESSION_DOCUMENTATION_GATE.md
  - docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md
  - docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/04_branch_trunk_cross_audit_target.md
  - docs/index/GO_INDEX.md
---

# GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01 — cadrage

## Besoin initial

Figer proprement dans le repo une méthode récurrente de ménage des branches Git :
- repo-first
- alignée sur `origin/sot/mainline`
- sans suppression aveugle
- réutilisable ensuite via Skill si le besoin devient durable

## Cible finale

Sortir entièrement cette logique de la session et obtenir :
- une méthode canonique de ménage des branches
- des critères de décision stables
- une frontière claire entre doc et future Skill
- un point d’entrée durable pour les prochaines passes de nettoyage

## Plan validé

1. partir du canon réel `opt-trading` / `sot/mainline`
2. rattacher la méthode à la cible de convergence `branches ↔ trunk`
3. figer une fiche de gouvernance dédiée
4. enregistrer le chantier de figement dans l’index canonique
5. réserver l’extraction Skill à une étape ultérieure, une fois la méthode stabilisée

## ETABLI

- la gate de session demande déjà d’ancrer la documentation durable dans le repo
- la cible GitHub Park pose déjà la convergence `branches ↔ trunk` comme besoin canonique
- la méthode détaillée de tri `DELETE_NOW / KEEP / REVIEW` n’était pas encore figée dans une fiche dédiée
- le principe retenu pour cette session est : **doc canonique d’abord, Skill ensuite**

## Gap restant

- appliquer cette méthode aux branches réelles du repo quand un ménage effectif sera lancé
- extraire une Skill seulement si la fréquence et le périmètre se stabilisent réellement

## Next GO

- utiliser `docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md` comme base unique pour tout futur audit ou ménage réel de branches
- si besoin récurrent confirmé : ouvrir un GO séparé d’extraction Skill adossé à cette fiche, sans redéfinir la méthode
