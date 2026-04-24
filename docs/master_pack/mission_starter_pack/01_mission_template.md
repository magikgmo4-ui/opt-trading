# TEMPLATE DE MISSION TRAE

**ID MISSION :** GO_OT_[MISSION_CLASS]_[ID]_[NOM_COURT]
**MISSION_CLASS :** [DIAGNOSTIC / PATCH_LOCAL / MODULE_DURABLE / BUNDLE_TRANSFERT / AUDIT_REALIGNEMENT]
**TYPE (legacy, déprécié) :** [AUDIT / PATCH / MODULE / SIGNALISATION / RUNBOOK] (optionnel)
**OBJECTIF :** [Description courte et précise]

## 1. CONTEXTE DE DÉPART
- **Sources lues** : `docs/master_pack/00_current_state_and_standards.md`, [Autres sources pertinentes]
- **Sources manquantes / non relues** : [Si applicable]
- **État supposé** : [Ce qu'on croit savoir avant de commencer]
- **Risques identifiés** : [Ex: Confusion runtime, Impact prod, etc.]

## 2. PLAN D'ACTION (5 PASSES)
1.  **Inventaire / Analyse** : Vérifier la réalité terrain.
2.  **Définition de la Cible** : Ce qu'on veut obtenir exactement.
3.  **Exécution / Rédaction** : Le travail proprement dit.
4.  **Validation / Vérification** : Prouver que ça marche (ou que c'est cohérent).
5.  **Clôture / Documentation** : Figer le résultat et mettre à jour le Master Pack.

Règle d’exécution : conduire l’implémentation via `workflow_ai/WORKFLOW.md` (gates) et ses templates (`specs.md` / `tasks.md`).
Standard de mission (Orchestrator) : cadrer via `docs/ot/trae/12_ORCHESTRATOR_ENTRYPOINT_V1.txt` avant exécution.
Si la mission comporte 3 étapes ou plus, ou implique repo+shared, ou plusieurs machines, utiliser : `docs/ot/trae/08_MULTI_STEP_MISSION_CHECKLIST_V1.txt`.

## 3. RÈGLES SPÉCIFIQUES
- **Scope autorisé** : [Fichiers / dossiers explicitement autorisés]
- **Hors-scope** : [Ce qui ne doit pas être touché]
- **Preuve attendue** : [Commande, log, diff, screenshot, artefact]
- **Rollback prévu** : [Commande ou procédure explicite]
- [Règle 1 : Ne pas toucher à X]
- [Règle 2 : Vérifier Y sur la machine Z]
- [Règle 3 : Format de sortie attendu]

Rappels :
- une mission doit rester atomique et vérifiable
- une validation du type "ça doit marcher" n'est pas acceptable
- `modules/validated_prompt_factory/README.md` peut aider à générer un prompt structuré, mais ne remplace pas ce contrat de mission
- `docs/ot/trae/trae_pack_texts/README.md` est un support legacy de lecture, non la source canonique de mission

## 4. LIVRABLES ATTENDUS
1.  `OT_[ID]_[NOM]_REPORT.md`
2.  `OT_[ID]_CLOSING.txt`
3.  [Autres fichiers clés]
