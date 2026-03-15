# OPT-TRADING — KANBAN (SOURCE OF TRUTH)

Date (America/Montreal) : 2026-03-14

## 1. RÔLE
Ce fichier est la **source de vérité kanban** du repo : statut des briques/missions et points de reprise.

Règle : une brique n’est pas considérée “clôturée proprement” tant que :
1) la doc canonique touchée est mise à jour,
2) ce kanban est mis à jour,
3) un point de reprise propre est laissé.

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
  - relire `opt_trading_kanban_source_of_truth_2026-03-13_updated.md` + dernier `OT_*_CLOSING*.txt`
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
