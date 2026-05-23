---
doc_id: GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01
status: active
lifecycle_stage: planning
topic_keys:
  - doc_ops
  - automation
  - priority
  - selection
surface: chantiers
source_kind: canonical
updated_at: 2026-05-23
---

# 00_INITIAL_PROJECT_DOC — GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01

## Mission
Prioriser et sélectionner les candidats à l'automatisation identifiés lors de l'audit des opérations récurrentes (`GO_OPT_TRADING_DOC_OPS_RECURRENT_OPERATIONS_AUDIT_01`).

## Contexte
L'audit a révélé 12 candidats potentiels pour automatiser les tâches Doc Ops répétitives (création de chantiers, génération de templates, vérification de contraintes, etc.). Ce présent GO doit évaluer ces candidats pour identifier les plus pertinents à implémenter en priorité.

## Objectif
Produire une matrice de décision scorée et sélectionner un maximum de 2 automatisations prioritaires pour le prochain cycle d'implémentation.

## Contraintes
- **DOC_ONLY** : Aucune implémentation de script, code ou configuration n'est autorisée.
- Ne pas modifier le runtime ou les index globaux.
- Respecter strictement la matrice de gouvernance `MATRICE_DOC_OPS_MASTER_MATRIX_01`.

## Livrables
1. Matrice de scoring des candidats.
2. Shortlist des automatisations sélectionnées (max 2).
3. Spécifications pour le prochain GO d'implémentation.

## État de départ
- Audit des opérations récurrentes terminé.
- Liste de 12 candidats disponible dans `40_AUTOMATION_CANDIDATES.md`.
- Branche `go/GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01` créée.
