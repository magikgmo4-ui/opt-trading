---
doc_id: OPT_TRADING_STATUS_DEEPSEEK_STUDENT_CANONIQUE
doc_type: family_status
repo: opt-trading
project: opt-trading
module:
go_id:
status: validated
lifecycle_stage: consolidation
topic_keys:
  - opt-trading
  - status
  - deepseek
  - student
  - module_family
search_tags:
  - surface:module_family
  - doc_role:carte
surface: module_family
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Reprise"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/product_targets/DEEPSEEK_OLLAMA_TARGET_CANON.md
  - docs/student_deepseek_runbook.md
---

# DEEPSEEK_STUDENT — STATUT CANONIQUE

## Role documentaire

- role_actuel: fiche courte de statut pour la lignee `deepseek*` cote student
- role_cible: fiche annexe de consolidation de lignee, non souveraine
- souverainete: ne remplace ni la matrice, ni les runbooks, ni une synthese produit transverse
- lecture_de_reprise: utiliser cette fiche apres `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, puis recroiser `MATRICE_GOUVERNANTE_V2.md` pour relire survivant / transition / legacy sans surpromouvoir la lignee

## Objet
Fiche courte de lignée pour la famille `deepseek*` côté surface student.

## ETABLI
- la famille `deepseek*` est confirmée comme famille parallèle à clarifier
- runbook opératoire student existant et exploitable
- vérité runtime actuelle confirmée dans `scripts/student/`
- `deepseek_hub` confirmé comme façade module unifiée la plus avancée
- `deepseek_response` / `deepseek_thinking` toujours utiles en compatibilité
- `deepseek_student` confirmé comme module de transition incomplet

## Survivant / Transition / Legacy / Archive
- survivant fonctionnel actuel : `scripts/student/` hors `modules/`
- survivant module candidat : `deepseek_hub`
- survivant canonique final : à confirmer plus tard ; non figé dans ce lot
- transition : `deepseek_student`
- legacy : `deepseek_response` et `deepseek_thinking` restent en compatibilité, sans suppression autorisée dans ce lot
- archive : non figé dans ce lot

## Liens de preuve
- `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_module_family_consolidation_audit.md`
- `docs/student_deepseek_runbook.md`

## Reprise
- reprise immédiate documentée dans `GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01`
- arbitrage structurel final à reprendre plus loin si une vraie bascule de `scripts/student/` vers `modules/` est lancée

## RISKS

- À qualifier.
