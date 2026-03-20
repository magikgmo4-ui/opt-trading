# CROSS-PROJECT — KANBAN MAÎTRE (ALIGNÉ SUR `sot/mainline`)

Date (America/Montreal) : 2026-03-20

## 1. RÔLE
Ce fichier est le **kanban maître transversal** de la passe actuelle.

Rôle :
- fournir une lecture unique et non ambiguë des périmètres du projet ;
- reprendre la logique de `sot/mainline` pour que toutes les IA lisent les statuts de la même façon ;
- séparer clairement : repo / branche, sous-projet intégré, module, machine/runtime, projet séparé ;
- fixer l’ordre des chantiers ;
- fixer le premier chantier recommandé.

Règle : un chantier n’est pas considéré **clôturé proprement** tant que :
1. la doc canonique touchée est mise à jour,
2. ce kanban est mis à jour,
3. un point de reprise propre est laissé.

## 1B. SYNTHÈSE OPÉRATIONNELLE DU KANBAN

### Tableau de synthèse

| Bloc | État | Nature | Réouverture | Suite |
|---|---|---|---|---|
| opt-trading / sot-mainline | ÉTABLI / CANONIQUE / ACTIVE | repo pivot | non | GO_CROSS_TOPLOGY_CANON_01 |
| opt-trading / branches secondaires auditées | ÉTABLI / CLASSÉ | historique / absorption / archive | selon branche | suivre `95_repo_branch_pm_kanban.md` |
| student | ÉTABLI / INTÉGRÉ / FORMALISÉ | sous-projet interne | oui | GO_STUDENT_PHASE2_MIGRATION_01 |
| api collector | ÉTABLI / PRÉSENT / À QUALIFIER | module interne | oui | GO_API_COLLECTOR_CANONICAL_MODULE_01 |
| db-layer | ÉTABLI / DOCUMENTÉ | machine / runtime | oui | GO_RUNTIME_SURFACES_CANONICAL_MAP_01 |
| admin-trading | ÉTABLI / DOCUMENTÉ | hub runtime | oui | GO_RUNTIME_SURFACES_CANONICAL_MAP_01 |
| cursor-ai | ÉTABLI / DOCUMENTÉ | surface opérateur Windows | oui | GO_RUNTIME_SURFACES_CANONICAL_MAP_01 |
| localcms / feature socle | ÉTABLI / FONCTIONNEL | projet séparé | oui | GO_LOCALCMS_CANON_DECISION_01 |
| localcms / tools dev-host | ÉTABLI / SURCOUCHE | exécution locale | oui | GO_LOCALCMS_CANON_DECISION_01 |
| openclaw | HORS BUNDLE / À CADRER | chantier séparé | oui | GO_OPENCLAW_CANONICAL_REENTRY_01 |
| hf_trading | À QUALIFIER | repo séparé potentiel | oui | GO_HF_TRADING_AUDIT_01 |
| algo_hf | À QUALIFIER | repo séparé potentiel | oui | GO_ALGO_HF_AUDIT_01 |
| Magikgmo | HISTORIQUE / ABSORBÉ | héritage ancien | non | aucune |

### Règle de maintenance de la synthèse
- cette synthèse est un résumé vivant ;
- elle doit être mise à jour à chaque fois qu’un statut réel change, qu’un support canonique est fixé, qu’un chantier est ouvert/fermé, ou qu’un point de reprise est modifié ;
- elle ne remplace pas les rapports détaillés ;
- en cas de conflit, les rapports détaillés et la décision PM finale priment.

## 2. ÉTAT — OPT-TRADING

### ÉTABLI
- `sot/mainline` est le pivot canonique.
- les branches `feat/*` auditées sont absorbées.
- `main`, `sot/build`, `fix/desk-ui-toolbox`, `antigravity/main`, `backup/main-before-filter` sont classées.

### CLOSE (CLASSÉ)
- `feat/risk-engine`
- `feat/execution-engine`
- `feat/position-engine`
- `feat/position-guard`
- `feat/persistent-state`
- `feat/engines-plugin`

### À CONFIRMER
- rien d’autre n’a besoin d’être rouvert côté branches `opt-trading` sans besoin concret.

### POINT DE REPRISE
- `GO_CROSS_TOPLOGY_CANON_01`

## 3. ÉTAT — STUDENT

### ÉTABLI
- `student` existe comme surface structurée dans `opt-trading`.
- racine canonique formalisée : `/opt/trading/student/`.
- façade canonique : `student_cmd.sh`, `student_menu.sh`, `student_sanity_check.sh`.
- wrappers opérateur : `student/scripts/wrappers/`.
- legacy locations identifiées : `modules/deepseek_hub/scripts/`, `modules/deepseek_student/scripts/`, `scripts/student/`.
- frontière canonique / toléré / legacy documentée dans `92_student_canonical_surface.md`.
- fiche canonique `GO_STUDENT_CANONICAL_SURFACE_01` livrée.

### À CONFIRMER
- Phase 2 migration : cleanup legacy locations, repoint installers internes, purge doublons — non démarrée.

### POINT DE REPRISE
- `GO_STUDENT_PHASE2_MIGRATION_01` (si chantier migration Phase 2 ouvert)

## 4. ÉTAT — API COLLECTOR

### ÉTABLI
- un collector est présent comme module interne du périmètre `opt-trading`.
- dans cette passe, il est classé comme **module**, pas comme repo séparé.

### À CONFIRMER
- nom canonique du module collector ;
- état fonctionnel réel ;
- runbook minimal et point de reprise dédié si le chantier reprend.

### POINT DE REPRISE
- `GO_API_COLLECTOR_CANONICAL_MODULE_01`

## 5. ÉTAT — RUNTIME SURFACES

### ÉTABLI
- `admin-trading`, `db-layer`, `cursor-ai` sont des surfaces runtime/machines documentées.
- elles apparaissent dans runbooks, matrices, snapshots, mappings.

### À CONFIRMER
- carte canonique minimale machine → rôle → surface active → repo associé.

### POINT DE REPRISE
- `GO_RUNTIME_SURFACES_CANONICAL_MAP_01`

## 6. ÉTAT — LOCALCMS

### ÉTABLI
- `feature/localcms-shared-explorer-cms-installer-v1` = socle fonctionnel.
- `tools/localcms-dev-host` = surcouche d’hébergement local.

### À CONFIRMER
- décision canonique future si reprise CMS :
  - garder `feature/...` comme base produit,
  - ou promouvoir une branche consolidée plus tard.

### POINT DE REPRISE
- `GO_LOCALCMS_CANON_DECISION_01`

## 7. ÉTAT — OPENCLAW

### ÉTABLI
- `openclaw` n’est pas dans le bundle canonique de cette passe.

### À CONFIRMER
- repo / bundle / support canonique de réentrée.

### POINT DE REPRISE
- `GO_OPENCLAW_CANONICAL_REENTRY_01`

## 8. ÉTAT — HF_TRADING / ALGO_HF

### ÉTABLI
- repos visibles côté GitHub.
- non qualifiés par l’archive de cette passe.

### À CONFIRMER
- contenu réel ;
- relation éventuelle avec `opt-trading` ;
- priorité réelle ou non.

### POINTS DE REPRISE
- `GO_HF_TRADING_AUDIT_01`
- `GO_ALGO_HF_AUDIT_01`

## 9. DÉCISION D’EXÉCUTION / DÉPLOIEMENT

### Règle retenue
- **cadrage / pilotage / validation / kanban / mémoire** = ici, dans la logique `sot/mainline`
- **déploiement / cowork d’exécution** = avec Claude

### Doctrine de cowork
- ChatGPT garde le rôle chef de projet / cadrage / source de lecture / priorisation / validation PM.
- Claude est utilisé en **cowork de déploiement** pour produire ou exécuter les changements une fois le chantier clairement cadré.
- Toute mission envoyée à Claude doit partir :
  1. du kanban courant,
  2. du point de reprise,
  3. du périmètre exact,
  4. du livrable attendu,
  5. des limites à respecter.

## 10. PLAN OPÉRATIONNEL

### Phase 1 — Geler la topologie canonique
1. garder `opt-trading / sot/mainline` comme pivot ;
2. traiter `student` comme sous-projet interne ;
3. traiter `api collector` comme module interne ;
4. traiter `admin-trading`, `db-layer`, `cursor-ai` comme surfaces runtime ;
5. garder `localcms` séparé ;
6. laisser `openclaw`, `hf_trading`, `algo_hf` hors plan actif tant qu’ils ne sont pas qualifiés.

### Phase 2 — Réduire la confusion documentaire
1. ne plus mélanger branches, machines, modules et projets ;
2. utiliser une taxonomie opposable :
   - repo/branche,
   - sous-projet intégré,
   - module,
   - machine/runtime,
   - projet séparé.

### Phase 3 — Formaliser les surfaces à reprendre
1. `student` → fiche canonique interne ;
2. `api collector` → fiche module + état réel ;
3. runtime surfaces → carte canonique minimale ;
4. `localcms` → décision canonique de maintien du socle/surcouche.

### Phase 4 — Ordre conseillé des chantiers
1. **Topologie canonique transverse**
2. **Student**
3. **API Collector**
4. **Runtime surfaces**
5. **LocalCMS**
6. **OpenClaw**
7. **hf_trading / algo_hf** si besoin réel

## 11. PREMIER CHANTIER RECOMMANDÉ

### Nom
- `CROSS-TOPOLOGY-CANON-01`

### Objet
Fixer une **carte canonique minimale** de tout le périmètre pour que toutes les IA lisent exactement la même structure de projet.

### Livrable attendu
Un document canonique court qui dit, sans ambiguïté :
- ce qui est repo/branche,
- ce qui est sous-projet interne,
- ce qui est module,
- ce qui est machine/runtime,
- ce qui est projet séparé,
- ce qui est hors bundle.

### Pourquoi c’est le premier chantier
Parce que sans cette couche, les prochains chantiers risquent de mélanger :
- `student`,
- `db-layer`,
- `api collector`,
- `localcms`,
- `openclaw`,
- et les branches `opt-trading`.

### Exécution recommandée
- cadrage ici ;
- déploiement documentaire / production finale avec Claude en cowork.

### Point de reprise
- `GO_CROSS_TOPLOGY_CANON_01`

## 12. POINT ACTIF CONSERVÉ
- `GO_CROSS_TOPLOGY_CANON_01`
