# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Valider une première tâche documentaire contrôlée exécutée par le builder OpenClaw via gateway, en mode dry-run strict.

## 3_INITIAL_NEED

Après validation du premier job contrôlé builder, vérifier que le builder peut recevoir une intention documentaire, produire une réponse structurée utile, et rester dans un cadre non destructif.

## 4_MASTER_PROJECT_PLAN

1. Définir une tâche documentaire bornée.
2. Poser une gate avant exécution.
3. Exécuter le dry-run via gateway.
4. Vérifier la structure de réponse.
5. Fermer le child uniquement si aucun patch, SSH ou effet runtime non autorisé n'a été produit.

## 6_FINAL_TARGET

Obtenir une réponse builder structurée pour une tâche documentaire dry-run, avec verdict PASS/FAIL traçable.

## 12_INVARIANTS

- Aucun SSH.
- Aucun patch réel.
- Aucun push.
- Aucune modification runtime.
- Aucune modification index global.
- Dry-run seulement.
- Toute mutation documentaire réelle doit être explicitement séparée dans un GO ultérieur.

## 16_TODO

- Créer la gate.
- Définir la tâche dry-run.
- Exécuter le builder via gateway.
- Journaliser la réponse.
- Produire closeout.

## 17_RESUME_POINT

Reprendre à la création de `01_DOC_TASK_DRY_RUN_GATE.md`.
