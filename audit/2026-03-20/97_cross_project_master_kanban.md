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
| student | ÉTABLI / INTÉGRÉ / PACK VALIDATION LIVRÉ | sous-projet interne | oui | GO_STUDENT_LIVE_VALIDATION_PACK_01 → EXÉCUTER SUR LA MACHINE LINUX CIBLE OÙ /opt/trading/student EST DÉPLOYÉ |
| api collector (`derivatives_collector`) | ÉTABLI / QUALIFIÉ / MOCK FONCTIONNEL | module interne | oui | GO_RUNTIME_SURFACES_CANONICAL_MAP_01 |
| db-layer | ÉTABLI / QUALIFIÉ / BACKEND ACTIF | machine / runtime Linux | oui | GO_ALGO_HF_AUDIT_01 |
| admin-trading | ÉTABLI / QUALIFIÉ / OPS ACTIF | machine / runtime Linux | non | — |
| cursor-ai | ÉTABLI / QUALIFIÉ / DEV SURFACE | machine / surface opérateur Windows | non | — |
| localcms / feature socle | ÉTABLI / P0 ARCHIVÉ / REPRISE SYNCHRONISÉE | projet séparé | oui | GO_LOCALCMS_M1_1_FORMS_01 (PM) |
| localcms / tools dev-host | ÉTABLI / QUALIFIÉ / SURCOUCHE HOST | projet séparé | non | — |
| openclaw | HORS BUNDLE / À CADRER | chantier séparé | oui | GO_OPENCLAW_CANONICAL_REENTRY_01 |
| hf_trading | À QUALIFIER | repo séparé potentiel | oui | GO_HF_TRADING_AUDIT_01 |
| algo_hf | PARTIELLEMENT QUALIFIÉ / SERVICE PROUVÉ / SOURCE INCONNUE | workstream séparé / runtime db-layer | oui | GO_ALGO_HF_DEEP_AUDIT_01 |
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

### CONFIRMÉ PAR VALIDATION LIVE — 2026-03-23

```
Machine  : student (Debian 12 — 192.168.16.103)
Verdict  : OK avec warnings (exit 0 — 0 erreur — 2 warnings non bloquants)
```

- `readlink -f /usr/local/bin/cmd-deepseek_student` → `/opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh` **CONFORME** — risque principal levé.
- 9/9 raccourcis globaux OK — tous pointent vers les chemins canoniques `student/`.
- 2 warnings non bloquants : alias-based fallback dans `deepseek_hub_cmd.sh` et `sanity_check_deepseek_hub.sh` (item 5 LEGACY_CALLERS_INVENTORY — déféré).
- H01 de `93_student_phase2_migration.md` §6 : **CONFIRMÉ OUI**.
- Condition `94_student_cleanup_duplicates.md` §4.2 remplie : retrait de `deepseek_student/deepseek_student_cmd.sh` comme entrypoint opérateur **activable sur décision PM**.

### À CONFIRMER (résiduel post-live)
- Rewiring alias-based fallback (`deepseek_hub_cmd.sh`, `sanity_check_deepseek_hub.sh`) — toujours déféré, chantier futur.
- H02 (`deepseek_student/deepseek_student_cmd.sh` non appelé en prod) — callers directs non audités en live, condition readlink remplie.
- H03 (modules `deepseek_thinking`/`deepseek_response` présents) — hors périmètre validation live, à confirmer si chantier module-dependency ouvert.

### ÉTABLI PAR GO_STUDENT_PHASE2_MIGRATION_01
- Les 4 items runtime prioritaires du LEGACY_CALLERS_INVENTORY sont déjà corrigés dans les scripts (migration exécutée en amont de cette passe).
- `LEGACY_CALLERS_INVENTORY.md` mis à jour avec état réel.
- `PHASE2_MIGRATION.md` mis à jour avec vérification 2026-03-20.
- PATH fallback `modules/deepseek_thinking` / `modules/deepseek_response` dans `run_logged.sh` = dépendance externe légitime, conservée.

### ÉTABLI PAR GO_STUDENT_CLEANUP_DUPLICATES_01
- Caller audit complet sur les 4 couches de doublons (CMD / Installer / Sanity / Menu).
- Aucun doublon ne justifie de retrait physique sans validation live.
- Risque principal isolé : alias `cmd-deepseek_student` — vérifier `readlink` sur la machine Linux cible où `/opt/trading/student` est effectivement déployé et où les shortcuts `/usr/local/bin` doivent être validés.
- `DUPLICATES_AUDIT.md` mis à jour avec section Caller Audit 2026-03-20 et classification de risque.
- `94_student_cleanup_duplicates.md` livré.

### LIVRÉ PAR GO_STUDENT_LIVE_VALIDATION_PACK_01 (2026-03-20)
- Pack de validation `student/validation/` créé (6 fichiers : runner, cmd, menu, sanity, RUNBOOK, HANDOFF).
- Répertoire `student/validation/` inexistant avant cette mission — créé dans cette passe.
- Couvre : 9 raccourcis globaux (readlink), raccourci critique `cmd-deepseek_student`, callers legacy item 5, entrypoints canoniques live, structure répertoire.
- Archive zip : `audit/2026-03-20/student_validation_pack_20260320.zip` (à transférer sur la machine Linux cible où `/opt/trading/student` est effectivement déployé et où les shortcuts `/usr/local/bin` doivent être validés).
- La validation live réelle reste à exécuter sur la machine Linux cible où `/opt/trading/student` est effectivement déployé et où les shortcuts `/usr/local/bin` doivent être validés.

### POINT DE REPRISE
- `GO_STUDENT_LIVE_VALIDATION_PACK_01` → **LIVRÉ** — pack prêt, à exécuter sur la machine Linux cible où `/opt/trading/student` est effectivement déployé
- `GO_API_COLLECTOR_CANONICAL_MODULE_01` (chantier suivant recommandé du portefeuille)

## 4. ÉTAT — API COLLECTOR

### ÉTABLI PAR GO_API_COLLECTOR_CANONICAL_MODULE_01
- nom canonique réel : `modules/derivatives_collector` (alias PM "api collector").
- classification confirmée : **module interne `opt-trading`**, chaîne Desk Pro core.
- structure saine : `app/derivatives_collector.py`, `config/env.example`, `scripts/{cmd.sh,menu.sh,sanity_check.sh}`.
- état fonctionnel : adapter `mock` opérationnel ; adapters réels (Coinglass, Binance, Bitget) = placeholders non implémentés.
- export JSON/CSV fonctionnel vers `data/derivatives/`.
- consommateurs downstream déclarés : Risk Engine, Strategy.
- pas de shortcut global `/usr/local/bin/` déclaré pour ce module.
- fiche canonique livrée : `A0_api_collector_canonical_module.md`.

### À CONFIRMER (passe ultérieure)
- implémentation des adapters réels ;
- vérification live de l'intégration Risk Engine / Strategy ;
- décision shortcut global et gestion secrets API.

### POINT DE REPRISE
- `GO_RUNTIME_SURFACES_CANONICAL_MAP_01` (chantier suivant recommandé)

## 5. ÉTAT — RUNTIME SURFACES

### ÉTABLI PAR GO_RUNTIME_SURFACES_CANONICAL_MAP_01
- **`admin-trading`** — Debian 12, HP EliteBook. OPS/bastion SSH. Services actifs (snapshot 2026-02-26) : `tv-webhook`, `tv-bitget-runner`, `<REDACTED_TUNNEL>-tv`. Repo `opt-trading` déployé sur `/opt/trading/`. Couche runtime : `scripts/admin_trading/`. IP LAN : 192.168.16.155.
- **`db-layer`** — Ubuntu 24.04, MSI GE62. Backend persistant / DB. Service `algo-hf-api` actif. Repo `opt-trading` non établi sur db-layer. IP LAN : 192.168.16.179.
- **`cursor-ai`** — Windows 10 Pro, Dell. Poste de développement. Tunnel WireGuard vers admin-trading. Repo `opt-trading` local : `C:\Users\ghost\opt-trading\`. Surface d'exécution de la session cowork courante. IP LAN : 192.168.16.224.
- Carte canonique livrée : `A1_runtime_surfaces_canonical_map.md`.

### À CONFIRMER (passe ultérieure)
- Lien `algo-hf-api` (db-layer) ↔ workstream `algo_hf` — déféré à `GO_ALGO_HF_AUDIT_01`.
- État live des services au-delà du snapshot 2026-02-26.
- Repo déployé sur db-layer si nécessaire.
- Correction fiche_machine.md cursor-ai (données manquantes dans le repo).

### POINT DE REPRISE
- `GO_LOCALCMS_CANON_DECISION_01` ou `GO_ALGO_HF_AUDIT_01` selon priorité PM

## 6. ÉTAT — LOCALCMS

### ÉTABLI PAR GO_LOCALCMS_CANON_DECISION_01
- `localcms` = projet séparé — repo autonome, NON intégré à `opt-trading`.
- 2 branches complémentaires à topologie **linéaire** (non concurrentes) :
  - `feature/localcms-shared-explorer-cms-installer-v1` = **base produit** (M1 + M2 + frontend patché). HEAD : `d26f07f`.
  - `tools/localcms-dev-host` = **surcouche dev host** (ajoute main.py + run.sh + run.bat + requirements.txt). HEAD : `54da71f` — 1 commit en avance sur `feature/...`.
- M1 (Shared Explorer V1) : validé live sandbox.
- M2 (CMS Installer V1) : install live prouvée.
- Arbitrage host FastAPI validé opérateur 2026-03-18 : versionnement en branche dédiée `tools/...` décidé.
- Clone canonique : `C:\Users\ghost\localcms\` — branche courante : `feature/...`.
- Décision canonique livrée : `A2_localcms_canon_decision.md`.

### CLOS — GO_P0_ARCHIVE_01 (2026-03-21)
- P0 archivé sous `docs/p0-compatibility-contract.html` dans `feature/localcms-shared-explorer-cms-installer-v1`.
- Commit pushé : `447c8c1` — branche : `feature/localcms-shared-explorer-cms-installer-v1`.
- Ne pas rouvrir Trae ni P0.
- Reprise LocalCMS synchronisée sur cette base.

### DÉCISION PM EN ATTENTE
- Validation explicite de P0 par le PM.
- Puis ouverture de `GO_LOCALCMS_M1_1_FORMS_01`.

### POINT DE REPRISE
- `GO_LOCALCMS_M1_1_FORMS_01` (conditionnel — validation PM de P0 requise)

## 7. ÉTAT — OPENCLAW

### ÉTABLI
- `openclaw` n’est pas dans le bundle canonique de cette passe.

### À CONFIRMER
- repo / bundle / support canonique de réentrée.

### POINT DE REPRISE
- `GO_OPENCLAW_CANONICAL_REENTRY_01`

## 8. ÉTAT — HF_TRADING / ALGO_HF

### ÉTABLI POUR `algo_hf` PAR GO_ALGO_HF_AUDIT_01
- `algo-hf-api.service` actif sur db-layer (snapshot 2026-02-26) : `loaded active running algo_hf API (FastAPI webhook)`.
- Processus Python sur port 9100 sur db-layer — probablement le service, non formellement prouvé.
- `algo_hf` est **absent de `opt-trading`** (aucun module, doc, script dans le repo).
- `/opt/trading/` est absent de db-layer — le code `algo_hf` ne provient pas d’un déploiement de `opt-trading`.
- Chemin réel du code sur db-layer : **NON ÉTABLI** depuis les sources disponibles.
- Repo local sur cursor-ai : **ABSENT** — aucun clone trouvé dans `C:\Users\ghost\`.
- Repo GitHub : mentionné par PM mais non vérifié terrain dans cette passe.
- Fiche de qualification livrée : `A3_algo_hf_audit.md`.

### ÉTABLI POUR `hf_trading`
- Mentionné comme "visible côté GitHub" par le PM.
- Non exploré en terrain dans cette passe.
- Relation avec `algo_hf` : non documentée.

### À CONFIRMER (passe ultérieure)
- Chemin code `algo_hf` sur db-layer (SSH live requis) ;
- Contenu repo GitHub `algo_hf` et `hf_trading` ;
- Relation `algo_hf` ↔ `hf_trading` ;
- Priorité de qualification si le workstream doit être activé.

### POINTS DE REPRISE
- `GO_ALGO_HF_DEEP_AUDIT_01` (SSH live + GitHub si besoin)
- `GO_HF_TRADING_AUDIT_01` (non démarré)

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
- **PASSE 2026-03-20 CLÔTURÉE** — `GO_AUDIT_2026_03_20_FORMAL_CLOSE_01` livré dans `A4_audit_2026_03_20_formal_close.md`
- **`GO_STUDENT_LIVE_VALIDATION_PACK_01` LIVRÉ** — pack `student/validation/` créé (2026-03-20)
- **`GO_STUDENT_VALIDATION_PACK_MATERIALIZE_01` LIVRÉ** — artefacts parasites supprimés, pack figé (2026-03-23)
- **`GO_STUDENT_LIVE_RESULT_CAPTURE_01` LIVRÉ** — template `student/validation/LIVE_RESULT_CAPTURE_TEMPLATE.md` produit (2026-03-23)
- **`GO_STUDENT_LIVE_AUDIT_UPDATE_01` LIVRÉ** — validation live exécutée sur machine `student` (2026-03-23) — verdict : **OK avec warnings** — 9/9 raccourcis OK — `cmd-deepseek_student` CONFORME — 2 warnings alias-based fallback non bloquants — `93`, `94`, `97` mis à jour
- **`GO_P0_ARCHIVE_01` CLOS** — P0 archivé sous `docs/p0-compatibility-contract.html`, commit `447c8c1`, branche `feature/localcms-shared-explorer-cms-installer-v1`. Ne pas rouvrir Trae ni P0.
- Décisions PM en attente :
  - retrait de `deepseek_student/deepseek_student_cmd.sh` comme entrypoint opérateur — condition readlink remplie — décision PM requise
  - `GO_STUDENT_PHASE2_MIGRATION_01` : PARTIEL → ÉTABLI — validation PM requise (H01 confirmé, H02/H03 résiduels non bloquants)
  - validation explicite P0 → ouverture `GO_LOCALCMS_M1_1_FORMS_01`
  - ou `GO_ALGO_HF_DEEP_AUDIT_01` (SSH db-layer + GitHub algo_hf)
