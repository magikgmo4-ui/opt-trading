# TEMPLATE DE MISSION TRAE

**ID MISSION :** GO_OT_[TYPE]_[ID]_[NOM_COURT]
**TYPE :** [AUDIT / PATCH / MODULE / SIGNALISATION / RUNBOOK]
**OBJECTIF :** [Description courte et précise]

## 1. CONTEXTE DE DÉPART
- **Sources lues** : `docs/master_pack/00_current_state_and_standards.md`, [Autres sources pertinentes]
- **État supposé** : [Ce qu'on croit savoir avant de commencer]
- **Risques identifiés** : [Ex: Confusion runtime, Impact prod, etc.]

## 2. PLAN D'ACTION (5 PASSES)
1.  **Inventaire / Analyse** : Vérifier la réalité terrain.
2.  **Définition de la Cible** : Ce qu'on veut obtenir exactement.
3.  **Exécution / Rédaction** : Le travail proprement dit.
4.  **Validation / Vérification** : Prouver que ça marche (ou que c'est cohérent).
5.  **Clôture / Documentation** : Figer le résultat et mettre à jour le Master Pack.

Règle d’exécution : conduire l’implémentation via `workflow_ai/WORKFLOW.md` (gates) et ses templates (`specs.md` / `tasks.md`).

## 3. RÈGLES SPÉCIFIQUES
- [Règle 1 : Ne pas toucher à X]
- [Règle 2 : Vérifier Y sur la machine Z]
- [Règle 3 : Format de sortie attendu]

## 4. LIVRABLES ATTENDUS
1.  `OT_[ID]_[NOM]_REPORT.md`
2.  `OT_[ID]_CLOSING.txt`
3.  [Autres fichiers clés]
