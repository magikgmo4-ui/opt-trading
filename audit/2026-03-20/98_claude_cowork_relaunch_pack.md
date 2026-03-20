# CLAUDE COWORK — PACK DE REPRISE

Date (America/Montreal) : 2026-03-20
Branche de travail : `audit/opt-trading-20260320a`
Mission de départ : `GO_CROSS_TOPLOGY_CANON_01`

## 1. RÔLE DU PACK
Ce fichier sert de **pack de reprise compact** pour relancer proprement le travail dans une nouvelle session, avec Claude en cowork d’exécution.

Rôle des outils :
- **ChatGPT** = chef de projet, cadrage, validation PM, mémoire canonique, kanban
- **Claude** = cowork de production/déploiement sur mission cadrée

## 2. ÉTAT ÉTABLI
La passe d’audit a produit un bundle documentaire stable dans la branche `audit/opt-trading-20260320a`.

Bundle présent :
- `audit/2026-03-20/00_audit_master_index.md`
- `audit/2026-03-20/00_audit_plan.md`
- `audit/2026-03-20/01_sot_mainline.md`
- `audit/2026-03-20/90_convergence_matrix.md`
- `audit/2026-03-20/95_repo_branch_pm_kanban.md`
- `audit/2026-03-20/96_cross_project_inventory_kanban_archive_first.md`
- `audit/2026-03-20/97_cross_project_master_kanban.md`
- `audit/2026-03-20/99_pm_decision.md`

## 3. SYNCHRO DES MACHINES — ÉTAT RÉEL
### OK
- `admin-trading` : branche d’audit pullée, working tree propre
- `cursor-ai` / Windows : branche d’audit pullée, à jour
- `db-layer` : clone séparé `~/opt-trading-audit` créé, branche d’audit pullée, working tree propre

### OK POUR LECTURE / À SURVEILLER
- `student` : branche d’audit pullée et à jour, mais fichiers non suivis présents dans le clone

## 4. DÉCISION PM DÉJÀ FIXÉE
- pivot canonique = `opt-trading / sot/mainline`
- `student` = sous-projet intégré à `opt-trading`
- `api collector` = module interne à `opt-trading`
- `db-layer`, `admin-trading`, `cursor-ai` = surfaces runtime / machines
- `localcms` = projet séparé
- `openclaw` = hors bundle pour cette passe
- `hf_trading` / `algo_hf` = à qualifier plus tard

## 5. PREMIER CHANTIER À LANCER
### Nom
- `CROSS-TOPOLOGY-CANON-01`

### Objet
Fixer une **carte canonique minimale transverse** du périmètre pour que toutes les IA lisent exactement la même structure projet.

### Ce que le document final doit dire explicitement
- ce qui est **repo/branche**
- ce qui est **sous-projet intégré**
- ce qui est **module**
- ce qui est **machine/runtime**
- ce qui est **projet séparé**
- ce qui est **hors bundle**

## 6. LECTURE OBLIGATOIRE AVANT PRODUCTION
Claude doit lire dans cet ordre :
1. `audit/2026-03-20/00_audit_master_index.md`
2. `audit/2026-03-20/99_pm_decision.md`
3. `audit/2026-03-20/97_cross_project_master_kanban.md`
4. `audit/2026-03-20/96_cross_project_inventory_kanban_archive_first.md`
5. `audit/2026-03-20/95_repo_branch_pm_kanban.md`

## 7. CONTRAINTES À RESPECTER
- ne pas réécrire la hiérarchie des branches `opt-trading` déjà classée
- ne pas traiter `student` comme repo séparé sans preuve
- ne pas traiter `db-layer` comme repo
- ne pas fusionner `localcms` dans `opt-trading`
- ne pas réintroduire `openclaw` dans le plan actif sans support canonique
- ne pas inventer de périmètre absent du bundle

## 8. LIVRABLE ATTENDU DE CLAUDE
Claude doit produire un document canonique court, stable et lisible, avec :
1. un tableau de classification de tous les périmètres
2. une colonne “support canonique de référence”
3. une colonne “statut”
4. une colonne “usage / rôle”
5. une colonne “point de reprise suivant”

## 9. SORTIE ATTENDUE DE LA SESSION CLAUDE
Claude doit renvoyer :
1. le document proposé
2. les fichiers créés/modifiés
3. les hypothèses restantes
4. le point de reprise suivant
5. les limites réelles observées

## 10. POINT DE REPRISE
- `GO_CROSS_TOPLOGY_CANON_01`
