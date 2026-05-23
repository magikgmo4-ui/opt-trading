---
doc_id: GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01_NEXT_GO_SPEC
doc_type: next_go_spec
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_SELECTION_AUTOMATION_PRIORITY_01
status: active
updated_at: 2026-05-23
---

# 50_NEXT_IMPLEMENTATION_GO_SPEC

## Spécification du prochain GO

**Candidat prioritaire n°1** : `Constraint Checking Lite`

### Objectifs du prochain GO
1. Créer un script `scripts/ai/workers/doc_ops_constraint_check.py`.
2. Le script doit :
   - Lire les contraintes dans `00_INITIAL_PROJECT_DOC.md`.
   - Si `DOC_ONLY` est présent, vérifier via `git diff` qu'aucun fichier hors `docs/` n'est modifié.
   - Si `READ_ONLY` est présent, vérifier qu'aucun fichier n'est modifié.
   - Retourner un code de sortie non nul en cas de violation.
3. Intégrer ce script dans le flux de validation recommandé.

---

**Candidat prioritaire n°2** : `GO Naming + Directory Creation`

### Objectifs du prochain GO
1. Créer un script `scripts/ai/workers/doc_ops_create_chantier.py`.
2. Le script doit :
   - Accepter un `GO_ID` en argument.
   - Valider le format via Regex (`GO_[A-Z0-9_]+_[0-9]{2}`).
   - Créer `docs/chantiers/<GO_ID>/`.
   - Créer `docs/chantiers/<GO_ID>/00_INITIAL_PROJECT_DOC.md` à partir d'un template pré-rempli.
   - Optionnel : créer l'entrée inbox correspondante.
