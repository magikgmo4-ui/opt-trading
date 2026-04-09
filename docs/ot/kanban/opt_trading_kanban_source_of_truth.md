# OPT-TRADING — KANBAN (SOURCE OF TRUTH)

Date (America/Montreal) : 2026-03-14

## 1. RÔLE
Ce fichier est la **source de vérité kanban** du repo : statut des briques/missions et points de reprise.

Règle : une brique n’est pas considérée “clôturée proprement” tant que :
1) la doc canonique touchée est mise à jour,
2) ce kanban est mis à jour,
3) un point de reprise propre est laissé.

## 1B. SYNTHÈSE OPÉRATIONNELLE DU KANBAN

Rôle :
Cette synthèse est un résumé vivant du kanban. Elle permet de voir rapidement ce qui est établi, ce qui est actif, ce qui est manquant, ce qui ne doit pas être rouvert, et dans quel ordre descendre les briques.

### Tableau de synthèse

| Bloc | État | Nature | Réouverture | Suite |
|---|---|---|---|---|
| SHARED / SSHFS | ÉTABLI / STABLE | infra | non | GO_OT_NEXT_MISSION_SELECTION_01 |
| Starter Pack / Opening | ÉTABLI / STABLE | doctrine repo | non | GO_OT_NEXT_MISSION_SELECTION_01 |
| validated_prompt_factory | CLOSE | outil opérateur | non | aucune |
| trae_module_validator | ÉTABLI / ACTIVE (FORMALISÉ) | outil opérateur | non | GO_OT_NEXT_MISSION_SELECTION_01 |
| Socle doctrinal Trae | ÉTABLI / PARTIEL | helper doctrinal | CONFIRMÉ PARTIELLEMENT (adoption) | GO_OT_NEXT_MISSION_SELECTION_01 |
| Runtime vs snapshot repo | DIVERGENT / SUIVI | gouvernance ops | NON CONFIRMÉ MAIS ACCEPTÉ (invariant documenté) | GO_OT_NEXT_MISSION_SELECTION_01 |
| Rules Trae V1 | ÉTABLI / GELÉ (PRE-V1, OPPOSABLE) | couche V1 | oui | gel pré-V1 acté (doc-only) ; suite: GO_OT_NEXT_MISSION_SELECTION_01 |
| Agents Trae V1 | ÉTABLI / GELÉ (PRE-V1, OPPOSABLE) | couche V1 | oui | gel pré-V1 acté (doc-only) ; suite: GO_OT_NEXT_MISSION_SELECTION_01 |
| Skills Trae V1 | ÉTABLI / GELÉ (PRE-V1, OPPOSABLE) | couche V1 | oui | gel pré-V1 acté (doc-only) ; suite: GO_OT_NEXT_MISSION_SELECTION_01 |
| MCP Policy V1 | ÉTABLI / GELÉ (PRE-V1, OPPOSABLE) | gouvernance | oui | gel pré-V1 acté (doc-only) ; suite: GO_OT_NEXT_MISSION_SELECTION_01 |

### Règle de maintenance de la synthèse
- cette synthèse est un résumé vivant ;
- elle doit être mise à jour à chaque closing qui change un statut, une preuve réelle, un point de reprise, une interdiction de réouverture, ou l’ordre logique de la suite ;
- elle ne remplace pas le détail du kanban ;
- en cas de conflit, le détail du kanban et les closings priment.

## 2. ÉTAT — SHARED (SURFACE CANONIQUE INTER-MACHINES)

### ÉTABLI
- Surface canonique `/shared` :
  - admin-trading expose `/srv/sftp/shared_files/shared` (alias `/shared`)
  - db-layer + student montent `/shared` via `shared_sshfs_permanent`
  - Windows (cursor-ai) utilise `C:\Users\ghost\Downloads\SHARED\` + SFTP vers la même surface
- Structure `/shared` :
  - `_bundles/` (zips), `_ops/` (scripts), `_refs/` (références), `_archives/` (archives)
  - dossiers réservés/pipeline inchangés (`inbox/outbox/modules/_logs/vision_*/desk_pro/...`)
- UX minimale repo (Linux) :
  - `cmd-shared ls|get|put|cat|status|path`

### RÉSERVE MINEURE
- Néant spécifique après clôture OT-NET-RECONNECT-03 (coupure “réseau pur” prouvée en fenêtre opérateur sur db-layer et student).

### À CONFIRMER
- Néant spécifique au chantier SHARED.

## 3. MISSIONS — STATUT (SHARED)

### CLOSE (ÉTABLI)
- OT-SHARED-ORGANIZE-01 : arbo cible + classification (sans déplacement).
- OT-SHARED-MIGRATE-01 : création `_bundles/_ops/_refs/_archives` + déplacement zips vers `_bundles`.
- OT-SHARED-MIGRATE-02 : reclassification scripts vers `_ops` + références vers `_refs`.
- OT-SHARED-UX-01 : doctrine officielle + UX minimale `cmd-shared`.
- OT-NET-RECONNECT-02 : connectivité SSH projet prouvée (admin-trading/db-layer/student) + repo OK.
- OT-NET-RECONNECT-03 : CLOSE/PROVED — db-layer PASS/PROVED ; student PASS/PROVED (coupure OUTPUT `192.168.16.155:22` posée/observée/retirée ; SSH bloqué pendant coupure ; `/shared` lisible ; restauration prouvée).

### CLOSE AVEC RÉSERVE
- OT-NET-RECONNECT-01 : preuve “réseau pur” non produite en non-interactif (baseline /shared OK).

## 4. POINT DE REPRISE SUIVANT
- GO_OT_NEXT_MISSION_SELECTION_01 (sélection prudente, sans lancement).

## 5. ÉTAT — STARTER PACK (OUVERTURE / CLÔTURE / CONTINUITÉ)

### ÉTABLI
- Un point d’entrée unique “ouverture de session” est intégré au master pack : `docs/master_pack/mission_starter_pack/00_mission_start_guide.md`.
- La règle “clôture = doc canonique + kanban + point de reprise” est opposable (workflow + starter pack).

### CLOSE (ÉTABLI)
- OT-STARTERPACK-AUDIT-01 : audit du starter pack (diagnostic + gaps + closing).
- OT-STARTERPACK-PATCH-01 : patch minimal de consolidation (index ouverture + liens + naming + checklist).
- OT-STARTERPACK-PATCH-02 : doctrine finale (priorité starter pack vs workflow_ai + packs TRAE helpers).
- OT-STARTERPACK-ADOPTION-01 : validation d’adoption (ouverture/exécution/clôture/continuité) sur le repo.
- OT-SESSION-OPENING-DRILL-01 : drill réel d’ouverture de session “à froid” (frictions relevées, patch minimal).

### À CONFIRMER
- Adoption systématique du gating “GO/STOP” à chaque mission (workflow_ai décrit la règle).

## 6. POINT DE REPRISE SUIVANT (DOCS)
- GO_OT_NEXT_MISSION_SELECTION_01 :
  - relire `docs/ot/kanban/opt_trading_kanban_source_of_truth.md` + dernier `docs/ot/closings/OT_*_CLOSING*.txt`
  - sélectionner la prochaine mission (sans la lancer)

## 7. POINT DE REPRISE SUIVANT (OPS)
- GO_OT_NEXT_MISSION_SELECTION_01 :
  - même objectif (sélection prudente de la prochaine mission)

## 8. MODULES — VALIDATED_PROMPT_FACTORY

### ÉTABLI
- Module présent : `modules/validated_prompt_factory/` (générateur de prompts structurés).
- Wrappers attendus déclarés : `cmd/menu/sanity-validated_prompt_factory` (registry).

### CLOSE (PASS)
- OT-MODULE-01-VALIDATED_PROMPT_FACTORY-REAL-USE : drill réel sur 2 cas (registry central + bundle_transfer) + preuves.
- OT-MODULE-02-VALIDATED_PROMPT_FACTORY-HARDENING : validation stricte des synthèses + test d’échec + compatibilité Markdown headers.
- OT-MODULE-03-VALIDATED_PROMPT_FACTORY-ADOPTION : parcours opérateur nominal + 2–3 cas standard + doc minimale + preuves.
- OT-MODULE-04B-VALIDATED_PROMPT_FACTORY-LINUX_TARGET_SMOKE : smoke wrappers prouvé sur Linux réel (admin-trading) ; réserve MODULE_04 levée ; `menu.sh` non rejoué (interactif).
- OT-MODULE-05-VALIDATED_PROMPT_FACTORY-GLOBAL_WRAPPERS_VALIDATE : wrappers globaux `/usr/local/bin` prouvés sur Linux réel (cmd/sanity).
- OT-MODULE-06-VALIDATED_PROMPT_FACTORY-OPERATOR_RUNBOOK : runbook opérateur minimal canonique (README), non redondant, basé sur wrappers globaux.
- OT-MODULE-07-VALIDATED_PROMPT_FACTORY-MENU_INTERACTIVE_CHECK : menu prouvé (affichage + parcours “List Modes”) via test contrôlé non-interactif (stdin injecté).

### POINT DE REPRISE
- Néant spécifique au module (validé bout-en-bout).

## 9. TRAE — SOCLE / OUTILLAGE / V1

### ÉTABLI
- Un socle doctrinal Trae existe déjà dans le repo (helpers dans `trae_pack_texts/trae_pack/`).
- Le repo canonique reste prioritaire sur les packs helpers Trae.
- `validated_prompt_factory` est réel et clos.
- `trae_module_validator` est réel et exploitable (déclaré `active` en registry, wrappers présents, smoke prouvé via closings wrappers).
- `workflow_ai/WORKFLOW.md` et `.cursorrules` servent déjà de base de gouvernance.

### CONFIRMATION — VERDICTS (2026-03-14)
- `trae_module_validator` : STATUT CANONIQUE = ACTIVE (FORMALISÉ)
  - décision : `docs/ot/trae/OT_TRAE_MODULE_VALIDATOR_STATUS_DECISION_01.md`
  - établi : module présent + wrappers déclarés + smoke wrappers prouvé ; statut `active` en registry.
  - limite : aucune clôture “module” n’est produite (non applicable sans besoin prouvé de gel/archivage).
- Adoption réelle du socle Trae : VERDICT = CONFIRMÉ PARTIELLEMENT
  - décision : `docs/ot/trae/OT_TRAE_SOCLE_ADOPTION_DECISION_01.md`
  - établi : doctrine de gouvernance (workflow/starter pack/templates) + corpus de closings représentatif avec preuve / limites explicites.
  - limite : la formule “sur toutes les missions” et l’application systématique GO/STOP ne sont pas démontrées par les artefacts.
- Alignement runtime / snapshot repo : VERDICT = NON CONFIRMÉ MAIS ACCEPTÉ COMME INVARIANT DOCUMENTÉ
  - décision : `docs/ot/trae/OT_TRAE_RUNTIME_SNAPSHOT_ALIGNMENT_DECISION_01.md`
  - établi : divergences repo/live prouvées ; divergences structurelles déjà cadrées par matrices/note de gel ; runtime = source de vérité finale.
  - limite : “alignement exact” n’est pas démontrable ; l’invariant canonique est “écarts suivis et opposables”.

Reprise de session (canonique) :
- `docs/ot/trae/OT_TRAE_SESSION_REPRISE.md`

### RÉGULARISATION
- Régularisations préalables à CONTRADICTOIRE : complétées (décisions canoniques produites pour module validator, adoption socle Trae, et runtime/snapshot).

### CONTRADICTOIRE (À CADRER — MISSION DÉDIÉE, PAS ICI)
- Décision canonique de cadrage : `docs/ot/trae/OT_TRAE_CONTRADICTOIRE_CADRAGE_DECISION_01.md`
- Taxonomie repo vs taxonomie doctrinale Trae :
  - objectif : définir une table de correspondance stable (où vit quoi : `docs/`, `workflow_ai/`, `modules/`, `registry/`, `trae_pack_texts/`) vs couches Trae (Rules/Agents/Skills/MCP).
  - sortie attendue : un mapping “emplacement → rôle → statut canonique”, sans refactor.
- Standard module récent vs exceptions legacy :
  - objectif : lister ce qui est “standard opposable” (wrappers cmd/menu/sanity, registry, scripts) et ce qui reste “legacy toléré” ;
  - sortie attendue : une règle de compatibilité (grandfathering) + critères d’exception documentés.

### MATÉRIALISÉ & GELÉ (PRE-V1, OPPOSABLE)
- Socle pré-V1 matérialisé dans `docs/ot/trae/01_RULES_V1.txt` à `docs/ot/trae/11_PRE_V1_REPO_LANDING_PLAN.txt`, et gelé en PRE‑V1 opposable via décisions + clôtures.
- Modèle missions longues / multi-étapes : `docs/ot/trae/08_MULTI_STEP_MISSION_CHECKLIST_V1.txt`.
- Consolidation traçabilité audit V1 : `docs/ot/closings/OT_TRAE_V1_AUDIT_TRACEABILITY_CONSOLIDATION_01_CLOSING.txt`.

### DÉCISION (ORDRE V1 FUTUR)
Ordre retenu :
1. Rules
2. Agents
3. Skills
4. MCP

## 10. POINT ACTIF CONSERVÉ
- GO_OT_NEXT_MISSION_SELECTION_01

## 11. POINT CANDIDAT SI OUVERTURE DU CHANTIER TRAE V1
- GO_OT_TRAE_RULES_V1_01 (alias legacy : GO_OT_TRAE_RULES_V1_ADOPTION_01)
