---
GO_ID: GO_OPT_TRADING_DOC_OPS_IMPL_CONSTRAINT_CHECKING_LITE_01
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: null
MASTER_TARGET_ID: MT_DOC_OPS_AUTOMATION_LITE_01
MASTER_PROJECT_PLAN_ID: MPP_DOC_OPS_AUTOMATION_01
PARENT_GO_ID: GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01
NEXT_ATTACH_TARGET: null
6_FINAL_TARGET: "Script de contrôle de contraintes opérationnel"
BUNDLE_TARGET: "scripts/ai/workers/doc_ops_constraint_check.py"
TRANSPORT_MODE: patch_only
CLOSE_GATE_MASTER_TARGET: pending
---

# 00_INITIAL_PROJECT_DOC

## Objet
Implémenter le premier candidat d'automatisation Doc Ops : le vérificateur de contraintes léger.

## Contexte
Le projet `opt-trading` suit des règles strictes de modification. Certaines sessions sont limitées à la documentation (`DOC_ONLY`) ou sont en lecture seule (`READ_ONLY`). Actuellement, aucun outil ne valide ces contraintes avant le commit, ce qui peut mener à des dérives de périmètre accidentelles.

## Objectifs
1. Créer un script Python autonome capable de détecter les violations de périmètre.
2. Supporter les modes `DOC_ONLY` et `READ_ONLY`.
3. Utiliser les métadonnées de ce fichier ou des arguments CLI pour déterminer le mode.
4. Fournir une sortie claire pour l'opérateur et un code de sortie exploitable par des scripts de validation.

## Contraintes du GO
- **DOC_ONLY** : Si activé, seuls les fichiers sous `docs/` sont autorisés.
- **READ_ONLY** : Si activé, aucune modification n'est autorisée.
- Ne pas modifier le runtime ou les modules trading.
- Ne pas installer de hook Git global de force.

## Cible (6_FINAL_TARGET)
Un script `scripts/ai/workers/doc_ops_constraint_check.py` validé par des tests unitaires et prêt à être utilisé manuellement par les opérateurs.
