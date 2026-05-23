---
doc_id: GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01_SOURCE_REVIEW
doc_type: review
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01
status: active
updated_at: 2026-05-23
---

# 10_SOURCE_AUTOMATION_CANDIDATES_REVIEW

## Source d'entrée
Le document `docs/chantiers/GO_OPT_TRADING_DOC_OPS_RECURRENT_OPERATIONS_AUDIT_01/40_AUTOMATION_CANDIDATES.md` liste 12 candidats issus de l'analyse de 566 chantiers.

## Liste des candidats
1. **GO Naming and Directory Creation** : Normalisation du nommage et création de la structure de dossier.
2. **Initial Documentation Generation** : Génération du `00_INITIAL_PROJECT_DOC.md` à partir de templates.
3. **Closeout Documentation Generation** : Génération du `90_CLOSEOUT.md` standardisé.
4. **Inbox Entry Creation** : Création automatique de l'entrée dans `docs/index/inbox/`.
5. **Keyword and Constraint Validation** : Vérification de la présence des mots-clés et respect des contraintes (`READ_ONLY`, `DOC_ONLY`).
6. **Branch State Tracking** : Génération et mise à jour de `BRANCH_STATE.md`.
7. **Surface-Specific Validation** : Règles de validation propres à chaque surface (OpenClaw, Desk Pro, etc.).
8. **Repetition Detection and Deduplication** : Analyse des chantiers existants pour suggérer des travaux similaires.
9. **Metrics and Dashboard Generation** : Rapports sur les taux d'ouverture/fermeture et tendances.
10. **Template Evolution and Versioning** : Gestion centralisée et versionnée des templates Doc Ops.
11. **Git State Verification Automation** : Vérification systématique de l'état Git avant de commencer.
12. **Constraint Checking Lite** : Version légère de la validation de contraintes (ex: `DOC_ONLY` vs modification fichiers runtime).

## Analyse préliminaire
Les candidats 1, 2, 4 et 5 semblent être les plus transverses et fréquents. Les candidats 11 et 12 offrent des gains rapides de sécurité et de conformité sans complexité excessive.
