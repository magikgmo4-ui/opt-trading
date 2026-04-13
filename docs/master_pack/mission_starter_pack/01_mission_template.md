# TEMPLATE DE MISSION TRAE

**ID MISSION :** GO_OT_[MISSION_CLASS]_[ID]_[NOM_COURT]
**MISSION_CLASS :** [DIAGNOSTIC / PATCH_LOCAL / MODULE_DURABLE / BUNDLE_TRANSFERT / AUDIT_REALIGNEMENT]
**TYPE (legacy, déprécié) :** [AUDIT / PATCH / MODULE / SIGNALISATION / RUNBOOK] (optionnel)
**OBJECTIF :** [Description courte et précise]

## 1. BESOIN INITIAL
- [Quel besoin concret justifie cette mission ?]
- [Pourquoi faut-il le traiter maintenant ?]

## 2. OBJECTIF FINAL VISÉ
- [Quel résultat concret et mesurable est attendu à la fin ?]
- [Quelle est la cible finale / état cible ?]

## 3. PLAN VALIDÉ
- [Comment va-t-on atteindre l'objectif ?]
- [Quelle méthode / quel chemin ?]
- [Qu'est-ce qui est validé comme chemin correct ?]

## 4. RÔLES / FILS
- **Machine** : [Quelle machine est impliquée ?]
- **IA** : [Quel modèle / agent est utilisé ?]
- **IDE** : [Quel environnement est favorisé ?]
- **Repo / Produit** : [Quel repo ou produit est concerné ?]

## 5. ÉTAT RÉEL DE DÉPART
- **Sources lues** : `docs/master_pack/00_current_state_and_standards.md`, [Autres sources pertinentes]
- **État supposé** : [Ce qu'on croit savoir avant de commencer]
- **Risques identifiés** : [Ex: Confusion runtime, Impact prod, etc.]

## 6. GAP INITIAL
- [Quel est l'écart entre l'état actuel et l'objectif ?]
- [Qu'est-ce qui manque actuellement ?]

## 7. PROCHAIN GO / SORTIE ATTENDUE
- [Quelle est la prochaine étape GO après cette mission ?]
- [Quel livrable est attendu ?]

## 8. PLAN D'ACTION (5 PASSES)
1.  **Inventaire / Analyse** : Vérifier la réalité terrain.
2.  **Définition de la Cible** : Ce qu'on veut obtenir exactement.
3.  **Exécution / Rédaction** : Le travail proprement dit.
4.  **Validation / Vérification** : Prouver que ça marche (ou que c'est cohérent).
5.  **Clôture / Documentation** : Figer le résultat et mettre à jour le Master Pack.

Règle d'exécution : conduire l'implémentation via `workflow_ai/WORKFLOW.md` (gates) et ses templates (`specs.md` / `tasks.md`).
Standard de mission (Orchestrator) : cadrer via `docs/ot/trae/12_ORCHESTRATOR_ENTRYPOINT_V1.txt` avant exécution.
Si la mission comporte 3 étapes ou plus, ou implique repo+shared, ou plusieurs machines, utiliser : `docs/ot/trae/08_MULTI_STEP_MISSION_CHECKLIST_V1.txt`.

## 9. RÈGLES SPÉCIFIQUES
- [Règle 1 : Ne pas toucher à X]
- [Règle 2 : Vérifier Y sur la machine Z]
- [Règle 3 : Format de sortie attendu]

## 10. LIVRABLES ATTENDUS
1.  `OT_[ID]_[NOM]_REPORT.md`
2.  `OT_[ID]_CLOSING.txt`
3.  [Autres fichiers clés]
